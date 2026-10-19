"""Word-level transcript for a take, in the shape `hyperframes transcribe` imports.

Usage:
    python3 scripts/transcribe.py input/take.mp4 work/take.words.json \
        [--model small] [--language en] [--names "Ideabro, HyperFrames"]

Reads the input file only; never writes next to it.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path, rate=16000):
    # Decode with ffmpeg rather than faster-whisper's PyAV path, which breaks on older system PyAV.
    pcm = subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path,
         "-ac", "1", "-ar", str(rate), "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("media")
    p.add_argument("output")
    p.add_argument("--model", default="small")
    p.add_argument("--language", default=None)
    p.add_argument("--names", default="", help="comma-separated names to bias spelling")
    args = p.parse_args()

    out = Path(args.output)
    if out.resolve().parent == Path("input").resolve():
        sys.exit("refusing to write into input/: originals stay untouched")
    out.parent.mkdir(parents=True, exist_ok=True)

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        load_audio(args.media),
        language=args.language,
        word_timestamps=True,
        hotwords=args.names or None,
    )

    words = [
        {"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
        for seg in segments
        for w in seg.words
    ]
    out.write_text(json.dumps(words, indent=1, ensure_ascii=False))

    for w in words:
        print(f"{w['start']:7.2f}s -> {w['end']:6.2f}s  {w['text']}")
    print(f"\n{len(words)} words, language={info.language}, duration={info.duration:.1f}s -> {out}")


if __name__ == "__main__":
    main()
