#!/usr/bin/env python3
"""漫剧成片合成流水线:
1. 每个分镜:静态画面 + Ken Burns 运镜 + 字幕 + 配音(含地牢混响)-> 片段
2. 片段 concat 成整片
3. 叠加环境音(暗黑氛围低音 + 风声)并做响度归一 -> output/ep01_final.mp4
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shots import SHOTS, TITLE, SUBTITLE, END_CARD

ROOT = Path(__file__).resolve().parent.parent
SHOTS_DIR = ROOT / "assets" / "shots"
VOICE_DIR = ROOT / "audio" / "voice"
OUT_DIR = ROOT / "output"
SEG_DIR = OUT_DIR / "segments"

W, H = 1080, 1920
FPS = 30
LEAD_IN = 0.6   # 配音前静音
TAIL = 1.1      # 配音后停留
MIN_DUR = 4.2


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


def zoompan_expr(cam: str, frames: int) -> str:
    """生成 zoompan 滤镜表达式(先放大原图避免抖动)。"""
    x = "(iw-iw/zoom)/2"
    y = "(ih-ih/zoom)/2"
    if cam == "zoom_in":
        z = f"min(1+0.14*on/{frames},1.14)"
    elif cam == "zoom_in_slow":
        z = f"min(1+0.08*on/{frames},1.08)"
    elif cam == "zoom_in_fast":
        z = f"min(1+0.22*on/{frames},1.22)"
    elif cam == "zoom_out":
        z = f"max(1.14-0.14*on/{frames},1.0)"
    elif cam == "zoom_out_slow":
        z = f"max(1.10-0.10*on/{frames},1.0)"
    else:
        z = "1.0"
    return (f"scale={W * 2}:{H * 2},zoompan=z='{z}':x='{x}':y='{y}'"
            f":d={frames}:s={W}x{H}:fps={FPS}")


def build_segment(idx: int, shot, font: str, tmp: Path) -> Path:
    shot_id, img, speaker, _line, sub, cam = shot
    voice = VOICE_DIR / f"{shot_id}.mp3"
    vdur = probe_duration(voice)
    dur = max(MIN_DUR, LEAD_IN + vdur + TAIL)
    frames = int(dur * FPS)

    subfile = tmp / f"{shot_id}_sub.txt"
    subfile.write_text(sub, encoding="utf-8")

    vf = [zoompan_expr(cam, frames), "format=yuv420p"]
    # 字幕:底部居中,黑色描边
    vf.append(
        f"drawtext=fontfile={font}:textfile={subfile}:fontcolor=white:fontsize=52"
        f":line_spacing=14:borderw=4:bordercolor=black@0.85"
        f":x=(w-text_w)/2:y=h-360"
        f":enable='between(t,{LEAD_IN - 0.2:.2f},{dur - 0.3:.2f})'")
    # 片头标题(S01)与片尾字卡(S10)
    if idx == 0:
        tfile = tmp / "title.txt"
        tfile.write_text(TITLE + "\n" + SUBTITLE, encoding="utf-8")
        vf.append(
            f"drawtext=fontfile={font}:textfile={tfile}:fontcolor=white:fontsize=88"
            f":line_spacing=26:borderw=5:bordercolor=black@0.9"
            f":x=(w-text_w)/2:y=300:enable='between(t,0.4,3.2)'"
            f":alpha='if(lt(t,1),t-0.4,if(gt(t,2.6),(3.2-t)/0.6,1))'")
    if idx == len(SHOTS) - 1:
        efile = tmp / "end.txt"
        efile.write_text(END_CARD, encoding="utf-8")
        vf.append(
            f"drawtext=fontfile={font}:textfile={efile}:fontcolor=white:fontsize=76"
            f":borderw=5:bordercolor=black@0.9:x=(w-text_w)/2:y=560"
            f":enable='gte(t,{dur - 2.2:.2f})'"
            f":alpha='if(gte(t,{dur - 2.2:.2f}),min((t-{dur - 2.2:.2f})/0.8,1),0)'")
    # 首尾淡入淡出
    if idx == 0:
        vf.append("fade=t=in:st=0:d=0.8")
    if idx == len(SHOTS) - 1:
        vf.append(f"fade=t=out:st={dur - 1.0:.2f}:d=1.0")

    # 配音:延迟入场,非旁白角色加轻微地牢混响
    af = f"adelay={int(LEAD_IN * 1000)}|{int(LEAD_IN * 1000)},"
    if speaker != "narr":
        af += "aecho=0.7:0.28:40|75:0.22|0.12,"
    af += f"apad,atrim=0:{dur:.3f},aresample=44100"

    # 注意:图片只读入单帧,由 zoompan 的 d 参数复制出全部帧;
    # 不能与 -loop 1 组合,否则每帧输入都会被扩展 d 倍导致时长爆炸
    seg = SEG_DIR / f"{idx:02d}_{shot_id}.mp4"
    run(["ffmpeg", "-y",
         "-i", str(SHOTS_DIR / img), "-i", str(voice),
         "-filter_complex",
         f"[0:v]{','.join(vf)}[v];[1:a]{af}[a]",
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "faster", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "44100",
         "-r", str(FPS), "-t", f"{dur:.3f}", str(seg)])
    print(f"segment {seg.name}: {dur:.2f}s")
    return seg


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    SEG_DIR.mkdir(exist_ok=True)
    font = find_cjk_font()
    print(f"font: {font}")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        segs = [build_segment(i, s, font, tmp) for i, s in enumerate(SHOTS)]

        concat_list = tmp / "concat.txt"
        concat_list.write_text(
            "".join(f"file '{s}'\n" for s in segs), encoding="utf-8")
        merged = OUT_DIR / "ep01_merged.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", str(concat_list), "-c", "copy", str(merged)])

        total = probe_duration(merged)
        print(f"merged: {total:.2f}s")

        # 环境音:低频暗黑氛围 + 风声(棕噪声低通),整体轻量铺底
        final = OUT_DIR / "ep01_final.mp4"
        ambient = (
            f"sine=frequency=52:duration={total:.2f},volume=0.16,"
            f"tremolo=f=0.15:d=0.6[drone];"
            f"anoisesrc=color=brown:duration={total:.2f}:seed=7,"
            f"lowpass=f=380,volume=0.30,tremolo=f=0.12:d=0.7[wind];"
            f"[drone][wind]amix=inputs=2:duration=shortest,"
            f"afade=t=in:st=0:d=1.5,afade=t=out:st={total - 2.0:.2f}:d=2.0[amb];"
            f"[0:a][amb]amix=inputs=2:duration=first:normalize=0,"
            f"loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
        run(["ffmpeg", "-y", "-i", str(merged),
             "-filter_complex", ambient,
             "-map", "0:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final)])
        print(f"final: {final} ({probe_duration(final):.2f}s)")


if __name__ == "__main__":
    main()
