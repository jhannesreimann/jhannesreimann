#!/usr/bin/env python3
"""Recolor snake-and-commits output to match the profile card look.

Keeps the GitHub green commit dots, paints the snake in the card blue,
text in near-white, and drops the whole board on a dark rounded panel so
it reads the same in GitHub light and dark mode.
"""
import sys
from pathlib import Path

BG = "#0d1117"
TEXT = "#f0f6fc"
SNAKE_HEAD = "#79c0ff"   # was #8affc1, bright mint
SNAKE_BODY = "#58a6ff"   # was #b7ffd0, pale mint

REPLACEMENTS = {
    "#8affc1": SNAKE_HEAD,
    "#b7ffd0": SNAKE_BODY,
    "#7d8590": TEXT,
}

def main(paths):
    for raw in paths:
        path = Path(raw)
        s = path.read_text()
        for old, new in REPLACEMENTS.items():
            s = s.replace(old, new)
        # dark rounded panel behind everything
        head_end = s.index(">", s.index("<svg")) + 1
        panel = f'<rect x="0" y="0" width="100%" height="100%" fill="{BG}" rx="12"/>'
        s = s[:head_end] + panel + s[head_end:]
        path.write_text(s)
        print(f"recolored {path}")

if __name__ == "__main__":
    main(sys.argv[1:])
