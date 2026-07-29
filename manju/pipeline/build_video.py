#!/usr/bin/env python3
"""漫剧成片合成流水线 v2:
阶段一(每个分镜):
  - 1~2 张关键帧,各自做 Ken Burns 运镜;双关键帧在动作点交叉溶解,模拟连续动作
  - 动态氛围:火光闪烁(eq 逐帧亮度)、飘雾(噪声图平移)、飘雪(点阵图双层滚动视差)、
    镜头震动(切换点起衰减抖动)
  - 逐句字幕(与每句配音的时间窗对齐)
  - 逐句配音按时间偏移混合,非旁白台词加地牢混响
阶段二(全片):
  - 镜头间 0.45s 交叉淡化(xfade)取代硬切
  - 各镜头音轨按全局偏移混合 + 低音氛围 + 风声 + 响度归一
  - 全片叠加轻胶片颗粒,让画面持续"活"着
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shots import SHOTS, TITLE, SUBTITLE, END_CARD

ROOT = Path(__file__).resolve().parent.parent
SHOTS_DIR = ROOT / "assets" / "shots"
OVERLAY_DIR = ROOT / "assets" / "overlays"
VOICE_DIR = ROOT / "audio" / "voice"
OUT_DIR = ROOT / "output"
SEG_DIR = OUT_DIR / "segments"

W, H = 1080, 1920
FPS = 30
LEAD_IN = 0.55   # 镜头开始到第一句配音
LINE_GAP = 0.35  # 句与句之间
TAIL = 0.95      # 最后一句后的停留
MIN_DUR = 4.0
KF_XFADE = 0.5   # 关键帧动作溶解时长
CUT_XFADE = 0.45 # 镜头间交叉淡化时长


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(f"command failed: {' '.join(cmd[:6])}...")


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def find_cjk_font() -> str:
    """在 fc-list 中查找真正支持中文的字体文件(fc-match 的回退结果不可靠)。"""
    r = subprocess.run(["fc-list", "-f", "%{file}\n", ":lang=zh"],
                       capture_output=True, text=True)
    candidates = [line.strip() for line in r.stdout.splitlines() if line.strip()]
    for pref in ("CJK", "wqy", "microhei"):
        for c in candidates:
            if pref.lower() in c.lower():
                return c
    if candidates:
        return candidates[0]
    raise SystemExit("未找到中文字体,请安装 fonts-noto-cjk 或 fonts-wqy-microhei")


def zoompan_expr(cam: str, frames: int, phase: int = 0) -> str:
    """Ken Burns 运镜(先 2 倍放大避免抖动)。phase=1 表示双关键帧的后半段,起始 zoom 稍高保持连续感。"""
    x = "(iw-iw/zoom)/2"
    y = "(ih-ih/zoom)/2"
    base = 1.0 + (0.05 if phase else 0.0)
    speeds = {"zoom_in": 0.13, "zoom_in_slow": 0.08, "zoom_in_fast": 0.22,
              "zoom_out": -0.13, "zoom_out_slow": -0.09}
    sp = speeds.get(cam, 0.0)
    if sp >= 0:
        z = f"min({base}+{sp}*on/{frames},{base + sp + 0.01})"
    else:
        start = base - sp  # sp 为负,起点更高
        z = f"max({start}{sp}*on/{frames},{base})"
    return (f"scale={W * 2}:{H * 2},zoompan=z='{z}':x='{x}':y='{y}'"
            f":d={frames}:s={W}x{H}:fps={FPS}")


def line_layout(shot) -> tuple[list[tuple[float, float]], float]:
    """计算每句台词的(开始,时长)与镜头总时长。"""
    spans, t = [], LEAD_IN
    for i, (_spk, _line, _sub) in enumerate(shot["lines"]):
        d = probe_duration(VOICE_DIR / f"{shot['id']}_{i}.mp3")
        spans.append((t, d))
        t += d + LINE_GAP
    dur = max(MIN_DUR, t - LINE_GAP + TAIL)
    return spans, dur


def build_segment(idx: int, shot, font: str, tmp: Path) -> tuple[Path, float]:
    sid = shot["id"]
    spans, dur = line_layout(shot)
    fx = shot.get("fx", [])
    kfs = shot["keyframes"]

    inputs: list[str] = []
    fc: list[str] = []

    # ---- 关键帧视频层 ----
    if len(kfs) == 1:
        inputs += ["-i", str(SHOTS_DIR / kfs[0])]
        frames = int(dur * FPS) + 2
        fc.append(f"[0:v]{zoompan_expr(shot['cam'], frames)},trim=duration={dur:.3f}[base]")
        n_img = 1
        switch_t = None
    else:
        # 切换点:第 kf_switch 句台词开始时,或按 kf_frac 比例
        ks = shot.get("kf_switch", -1)
        switch_t = spans[ks][0] if ks >= 0 else dur * shot.get("kf_frac", 0.5)
        d_a = switch_t + KF_XFADE / 2
        d_b = dur - switch_t + KF_XFADE / 2
        inputs += ["-i", str(SHOTS_DIR / kfs[0]), "-i", str(SHOTS_DIR / kfs[1])]
        fa = int(d_a * FPS) + 2
        fb = int(d_b * FPS) + 2
        fc.append(f"[0:v]{zoompan_expr(shot['cam'], fa)},trim=duration={d_a:.3f}[ka]")
        fc.append(f"[1:v]{zoompan_expr(shot['cam'], fb, phase=1)},trim=duration={d_b:.3f}[kb]")
        fc.append(f"[ka][kb]xfade=transition=fade:duration={KF_XFADE}"
                  f":offset={switch_t - KF_XFADE / 2:.3f}[base]")
        n_img = 2

    cur = "base"

    # ---- 火光闪烁 ----
    if "flicker" in fx:
        fc.append(f"[{cur}]eq=eval=frame:brightness='0.028*sin(11*t)+0.02*sin(6.7*t+1.3)'[flk]")
        cur = "flk"

    # ---- 飘雾(横向缓慢平移的噪声图,低透明度) ----
    if "fog" in fx:
        fog_idx = n_img
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 1:.2f}",
                   "-i", str(OVERLAY_DIR / "fog.png")]
        n_img += 1
        fc.append(f"[{fog_idx}:v]crop={W}:{H}:x='mod(t*28,iw-{W})':y=0,"
                  f"format=rgba,colorchannelmixer=aa=0.14[fogc]")
        fc.append(f"[{cur}][fogc]overlay=shortest=1[fgd]")
        cur = "fgd"

    # ---- 飘雪(两层不同速度纵向滚动,产生视差) ----
    if "snow" in fx:
        for li, (speed, alpha, xdrift) in enumerate(
                [(300, 0.75, "12*sin(0.9*t)"), (170, 0.5, "-16*sin(0.6*t+1)")]):
            s_idx = n_img
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur + 1:.2f}",
                       "-i", str(OVERLAY_DIR / "snow.png")]
            n_img += 1
            lbl = f"sn{li}"
            fc.append(f"[{s_idx}:v]crop={W}:{H}:x=0:y='ih-{H}-mod(t*{speed},ih-{H})',"
                      f"format=rgba,colorchannelmixer=aa={alpha}[{lbl}c]")
            fc.append(f"[{cur}][{lbl}c]overlay=x='{xdrift}':y=0:shortest=1[{lbl}d]")
            cur = f"{lbl}d"

    # ---- 镜头震动(从关键帧切换点开始,指数衰减) ----
    if "shake" in fx:
        sw = switch_t if switch_t is not None else 0.0
        fc.append(f"[{cur}]scale={W + 72}:{H + 128},"
                  f"crop={W}:{H}"
                  f":x='36+if(gte(t,{sw:.3f}),26*sin(31*(t-{sw:.3f}))*exp(-2.2*(t-{sw:.3f})),0)'"
                  f":y='64+if(gte(t,{sw:.3f}),30*cos(41*(t-{sw:.3f}))*exp(-2.2*(t-{sw:.3f})),0)'[shk]")
        cur = "shk"

    # ---- 逐句字幕 ----
    vf_tail = []
    for i, (_spk, _line, sub) in enumerate(shot["lines"]):
        subfile = tmp / f"{sid}_sub{i}.txt"
        subfile.write_text(sub, encoding="utf-8")
        st, sd = spans[i]
        vf_tail.append(
            f"drawtext=fontfile={font}:textfile={subfile}:fontcolor=white:fontsize=52"
            f":line_spacing=14:borderw=4:bordercolor=black@0.85"
            f":x=(w-text_w)/2:y=h-360"
            f":enable='between(t,{st - 0.15:.2f},{min(st + sd + 0.55, dur - 0.15):.2f})'")

    # ---- 片头标题 / 片尾字卡 / 首尾淡入淡出 ----
    if idx == 0:
        tfile = tmp / "title.txt"
        tfile.write_text(TITLE + "\n" + SUBTITLE, encoding="utf-8")
        vf_tail.append(
            f"drawtext=fontfile={font}:textfile={tfile}:fontcolor=white:fontsize=88"
            f":line_spacing=26:borderw=5:bordercolor=black@0.9"
            f":x=(w-text_w)/2:y=300:enable='between(t,0.4,3.2)'"
            f":alpha='if(lt(t,1),t-0.4,if(gt(t,2.6),(3.2-t)/0.6,1))'")
        vf_tail.append("fade=t=in:st=0:d=0.8")
    if idx == len(SHOTS) - 1:
        efile = tmp / "end.txt"
        efile.write_text(END_CARD, encoding="utf-8")
        vf_tail.append(
            f"drawtext=fontfile={font}:textfile={efile}:fontcolor=white:fontsize=76"
            f":borderw=5:bordercolor=black@0.9:x=(w-text_w)/2:y=560"
            f":enable='gte(t,{dur - 2.2:.2f})'"
            f":alpha='if(gte(t,{dur - 2.2:.2f}),min((t-{dur - 2.2:.2f})/0.8,1),0)'")
        vf_tail.append(f"fade=t=out:st={dur - 1.0:.2f}:d=1.0")
    fc.append(f"[{cur}]{','.join(vf_tail)},format=yuv420p[v]")

    # ---- 逐句配音混合 ----
    amix_labels = []
    for i, (spk, _line, _sub) in enumerate(shot["lines"]):
        a_idx = n_img + i
        inputs += ["-i", str(VOICE_DIR / f"{sid}_{i}.mp3")]
        st_ms = int(spans[i][0] * 1000)
        chain = f"adelay={st_ms}|{st_ms}"
        if spk != "narr":
            chain += ",aecho=0.7:0.28:40|75:0.22|0.12"
        fc.append(f"[{a_idx}:a]{chain}[a{i}]")
        amix_labels.append(f"[a{i}]")
    n_lines = len(shot["lines"])
    mix = (f"{''.join(amix_labels)}amix=inputs={n_lines}:normalize=0,"
           if n_lines > 1 else f"{amix_labels[0]}")
    fc.append(f"{mix}apad,atrim=0:{dur:.3f},aresample=44100[a]")

    seg = SEG_DIR / f"{idx:02d}_{sid}.mp4"
    run(["ffmpeg", "-y", *inputs,
         "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "faster", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "44100",
         "-r", str(FPS), "-t", f"{dur:.3f}", str(seg)])
    print(f"segment {seg.name}: {dur:.2f}s  lines={n_lines} kf={len(kfs)} fx={fx}")
    return seg, dur


def assemble(segs: list[tuple[Path, float]]) -> None:
    """阶段二:镜头间 xfade + 全局混音 + 胶片颗粒。"""
    inputs, fc = [], []
    for seg, _d in segs:
        inputs += ["-i", str(seg)]

    # 视频 xfade 链
    starts = [0.0]
    for i in range(1, len(segs)):
        starts.append(starts[i - 1] + segs[i - 1][1] - CUT_XFADE)
    cur = "0:v"
    for i in range(1, len(segs)):
        out = f"vx{i}"
        fc.append(f"[{cur}][{i}:v]xfade=transition=fade:duration={CUT_XFADE}"
                  f":offset={starts[i]:.3f}[{out}]")
        cur = out
    total = starts[-1] + segs[-1][1]
    fc.append(f"[{cur}]noise=alls=5:allf=t+u,format=yuv420p[vout]")

    # 音频:按全局偏移混合
    alabels = []
    for i in range(len(segs)):
        ms = int(starts[i] * 1000)
        fc.append(f"[{i}:a]adelay={ms}|{ms}[ga{i}]")
        alabels.append(f"[ga{i}]")
    fc.append(f"{''.join(alabels)}amix=inputs={len(segs)}:normalize=0[voice]")
    # 氛围:低频 drone + 风
    fc.append(f"sine=frequency=52:duration={total:.2f},volume=0.16,"
              f"tremolo=f=0.15:d=0.6[drone]")
    fc.append(f"anoisesrc=color=brown:duration={total:.2f}:seed=7,"
              f"lowpass=f=380,volume=0.30,tremolo=f=0.12:d=0.7[wind]")
    fc.append(f"[drone][wind]amix=inputs=2:duration=shortest,"
              f"afade=t=in:st=0:d=1.5,afade=t=out:st={total - 2.0:.2f}:d=2.0[amb]")
    fc.append("[voice][amb]amix=inputs=2:duration=first:normalize=0,"
              "loudnorm=I=-16:TP=-1.5:LRA=11[aout]")

    final = OUT_DIR / "ep01_final.mp4"
    run(["ffmpeg", "-y", *inputs,
         "-filter_complex", ";".join(fc),
         "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "faster", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", str(final)])
    print(f"final: {final} ({probe_duration(final):.2f}s)")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    SEG_DIR.mkdir(exist_ok=True)
    font = find_cjk_font()
    print(f"font: {font}")
    if not (OVERLAY_DIR / "fog.png").exists():
        raise SystemExit("请先运行 pipeline/gen_overlays.py 生成叠加素材")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        segs = [build_segment(i, s, font, tmp) for i, s in enumerate(SHOTS)]
        assemble(segs)


if __name__ == "__main__":
    main()
