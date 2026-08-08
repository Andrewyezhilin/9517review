#!/usr/bin/env python3
"""生成动态氛围叠加素材:
- fog.png : 宽幅灰度噪声雾(横向缓慢平移,低透明度叠加)
- snow.png: 竖长条透明雪花点阵(纵向滚动模拟飘雪,两层不同速度产生视差)
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "overlays"

FOG_W, FOG_H = 2400, 1920
SNOW_W, SNOW_H = 1080, 5760

rng = random.Random(42)


def make_fog() -> None:
    img = Image.new("L", (FOG_W // 4, FOG_H // 4))
    img.putdata([rng.randint(0, 255) for _ in range(img.width * img.height)])
    img = img.resize((FOG_W, FOG_H), Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(60))
    # 拉开对比让雾有团块感
    lo, hi = img.getextrema()
    scale = 255.0 / max(1, hi - lo)
    img = img.point(lambda p: int((p - lo) * scale))
    img.convert("RGB").save(OUT / "fog.png")
    print("fog.png", img.size)


def make_snow() -> None:
    img = Image.new("RGBA", (SNOW_W, SNOW_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for _ in range(900):
        x, y = rng.randint(0, SNOW_W - 1), rng.randint(0, SNOW_H - 1)
        r = rng.uniform(1.2, 4.2)
        a = rng.randint(90, 200)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    img.save(OUT / "snow.png")
    print("snow.png", img.size)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_fog()
    make_snow()
