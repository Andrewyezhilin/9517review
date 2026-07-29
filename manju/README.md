# 《猎人》漫剧项目

竖屏(9:16)动态漫画短剧。第一集《地牢》:少年卓峰被囚三年,深夜被神秘黑斗篷男人解开锁链,踏出地牢走向未知命运。

## 目录结构

```
manju/
├── script/ep01_storyboard.md   # 分镜脚本(10 镜头,含角色设定与配音分配)
├── assets/
│   ├── characters/             # 角色设定图(卓峰、黑斗篷男人)——后续各集画面以此为参考保证形象一致
│   └── shots/                  # 10 个分镜画面(1080x1920 以上,AI 生成)
├── audio/voice/                # edge-tts 生成的各镜头配音
├── pipeline/
│   ├── shots.py                # 分镜数据:台词、字幕、音色、运镜方式
│   ├── gen_voice.py            # 配音生成(edge-tts)
│   └── build_video.py          # 成片合成(ffmpeg:运镜+字幕+混响+环境音+响度归一)
└── output/ep01_final.mp4       # 第一集成片(约 68 秒)
```

## 复现步骤

```bash
pip3 install edge-tts            # 需要 ffmpeg 和中文字体(如 fonts-wqy-microhei)
cd manju
python3 pipeline/gen_voice.py    # 1. 生成配音
python3 pipeline/build_video.py  # 2. 合成成片 -> output/ep01_final.mp4
```

## 制作说明

- **角色一致性**:先生成角色设定图,再把设定图作为参考图生成每个分镜,保证卓峰(凌乱黑发、琥珀色眼睛、破旧灰囚衣、伤痕)全片形象统一。续集沿用 `assets/characters/` 下的设定图即可。
- **运镜**:静态画面先放大 2 倍再用 zoompan 做慢速推拉(Ken Burns),避免抖动;注意不要与 `-loop 1` 组合使用。
- **音频**:四个角色四种音色(见 `pipeline/shots.py` 的 `VOICES`);非旁白台词加轻微地牢混响;整片铺低音氛围+风声,最后 loudnorm 响度归一。

## 续集扩展

在 `pipeline/shots.py` 中新增分镜数据(或复制一份 `shots_ep02.py`),生成新分镜画面时引用 `assets/characters/` 的设定图,然后重跑两个流水线脚本即可。
