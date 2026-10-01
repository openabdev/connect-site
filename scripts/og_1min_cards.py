#!/usr/bin/env python3
"""Sharing cards for the /1min/ index pages (en, zh).

Same canvas, gradient, watermark and fit-by-measurement as the note cards; the
drawing is og_note_cards.build, only the text and the domain line differ.
Each video page keeps its own card (the video cover, rendered with the video).

    python3 scripts/og_1min_cards.py
"""
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import og_cards as base
import og_note_cards as notes

ROOT = base.ROOT

TEXT = {
    "en": (["1-minute explainers", "One idea per video"],
           "Short vertical videos: ACP or PTY, and how much access an agent gets."),
    "zh": (["一分鐘看懂", "一支影片，只講一件事"],
           "直式短影片：ACP 還是 PTY、Agent 該給多少權限。"),
}
DOMAIN = {"en": "connect.openab.dev/1min", "zh": "connect.openab.dev/zh/1min"}

if __name__ == "__main__":
    base.derive_watermark()
    notes.DOMAIN = DOMAIN
    for lang in ("en", "zh"):
        dest, hs, ss, name, over = notes.build(lang, TEXT[lang], ROOT / "1min")
        im = Image.open(dest)
        print(f"  {lang:3} {dest.relative_to(ROOT)}  {im.size[0]}x{im.size[1]} "
              f"head={hs}px sub={ss}px  {name}" + (f"  OVERFLOW: {over}" if over else ""))
