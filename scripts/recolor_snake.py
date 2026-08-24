#!/usr/bin/env python3
"""Recolor snake-and-commits output to match the profile card look.

Keeps the GitHub green commit dots, paints the snake in the card blue,
text in near-white, and drops the whole board on a dark rounded panel so
it reads the same in GitHub light and dark mode.
"""
import re
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

# the generator replays the green intensity ramp after the head passes
# (eaten dot fading out). Swap it for a blue fade so the wake stays blue.
GREEN_RAMP = {"#39d353": "#388bfd", "#26a641": "#1f6feb", "#006d32": "#1158c7"}
STOP_RE = re.compile(r"([\d.]+%\s*\{\s*fill:\s*)(#[0-9a-fA-F]{6})(\s*;)")


def recolor_keyframes(svg):
    """Inside keyframes that animate the snake, fade the post-head ramp blue.

    Cells can be visited more than once, so everything after the FIRST blue
    stop gets the blue treatment - the initial dot state stays green.
    """
    def fix_block(m):
        block = m.group(0)
        if SNAKE_BODY not in block and SNAKE_HEAD not in block:
            return block
        out, pos, seen_blue = [], 0, False
        for s in STOP_RE.finditer(block):
            out.append(block[pos:s.end(1)])
            color = s.group(2)
            if color in (SNAKE_BODY, SNAKE_HEAD):
                seen_blue = True
            elif seen_blue and color in GREEN_RAMP:
                color = GREEN_RAMP[color]
            out.append(color + s.group(3))
            pos = s.end()
        out.append(block[pos:])
        return "".join(out)

    return re.sub(r"@keyframes\s*[\w-]+\s*\{(?:[^{}]|\{[^}]*\})*\}", fix_block, svg)


def main(paths):
    for raw in paths:
        path = Path(raw)
        s = path.read_text()
        for old, new in REPLACEMENTS.items():
            s = s.replace(old, new)
        s = recolor_keyframes(s)
        # dark rounded panel behind everything
        head_end = s.index(">", s.index("<svg")) + 1
        panel = f'<rect x="0" y="0" width="100%" height="100%" fill="{BG}" rx="12"/>'
        s = s[:head_end] + panel + s[head_end:]
        path.write_text(s)
        print(f"recolored {path}")

if __name__ == "__main__":
    main(sys.argv[1:])
