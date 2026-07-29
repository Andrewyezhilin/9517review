#!/usr/bin/env python3
"""为每个分镜生成配音(edge-tts),输出到 audio/voice/<shot_id>.mp3"""
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
    for shot_id, _img, speaker, line, _sub, _cam in SHOTS:
        voice, rate, pitch = VOICES[speaker]
        dest = OUT / f"{shot_id}.mp3"
        await edge_tts.Communicate(line, voice, rate=rate, pitch=pitch).save(str(dest))
        print(f"{shot_id} [{speaker}] -> {dest.name}")


if __name__ == "__main__":
    asyncio.run(main())
