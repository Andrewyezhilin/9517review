#!/usr/bin/env python3
"""为每个分镜的每句台词生成配音(edge-tts),输出 audio/voice/<shot_id>_<n>.mp3"""
import asyncio
import sys
from pathlib import Path

import edge_tts

sys.path.insert(0, str(Path(__file__).parent))
from shots import SHOTS, VOICES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "audio" / "voice"


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for shot in SHOTS:
        for i, (speaker, line, _sub) in enumerate(shot["lines"]):
            voice, rate, pitch = VOICES[speaker]
            dest = OUT / f"{shot['id']}_{i}.mp3"
            await edge_tts.Communicate(line, voice, rate=rate, pitch=pitch).save(str(dest))
            print(f"{shot['id']}_{i} [{speaker}] {line[:18]}...")


if __name__ == "__main__":
    asyncio.run(main())
