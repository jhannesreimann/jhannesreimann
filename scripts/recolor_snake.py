#!/usr/bin/env python3
"""Recolor snake-and-commits output to match the profile card.

Two themes so the <picture> switch on the profile actually changes looks:
- dark: dark panel, near-white text, GitHub green dots, card-blue snake
- light: white panel, dark text, GitHub light dot palette, darker blue snake

Keeps the GitHub green commit dots, paints the snake blue, and rewrites the
post-head fade inside keyframes so the wake never flashes green.
"""
import argparse
import re
from pathlib import Path

RAW_TEXT = "#7d8590"
RAW_HEAD = "#8affc1"
RAW_BODY = "#b7ffd0"

THEMES = {
    "dark": {
        "panel": "#0d1117",
        "text": "#f0f6fc",
        "head": "#79c0ff",
        "body": "#58a6ff",
        # eaten-dot fade, bright to dim
        "wake": {"#39d353": "#388bfd", "#26a641": "#1f6feb", "#006d32": "#1158c7"},
        # dark theme keeps the raw GitHub dark dot palette as is
        "palette": {},
    },
    "light": {
        "panel": "#ffffff",
        "text": "#24292f",
        "head": "#218bff",
        "body": "#0969da",
        "wake": {"#39d353": "#0969da", "#26a641": "#0550ae", "#006d32": "#033e8c"},
        # GitHub light dot palette + light empty cells
        "palette": {
            "#0e4429": "#9be9a8",
            "#006d32": "#40c463",
            "#26a641": "#30a14e",
            "#39d353": "#216e39",
            "#161b22": "#ebedf0",
        },
    },
}

STOP_RE = re.compile(r"([\d.]+%\s*\{\s*fill:\s*)(#[0-9a-fA-F]{6})(\s*;)")
KF_RE = re.compile(r"@keyframes\s*[\w-]+\s*\{(?:[^{}]|\{[^}]*\})*\}")


def recolor_keyframes(svg, theme):
    """Rewrite snake keyframes: blue wake after first blue stop.

    Runs after the raw snake colors were swapped to theme colors, so detect
    blues via the theme palette. Cells can be visited more than once, so
    everything after the FIRST blue stop gets the wake treatment - the
    initial dot state keeps its palette.
    """
    def fix_block(m):
        block = m.group(0)
        if theme["body"] not in block and theme["head"] not in block:
            return block
        out, pos, seen_blue = [], 0, False
        for s in STOP_RE.finditer(block):
            out.append(block[pos:s.end(1)])
            color = s.group(2)
            if color in (theme["body"], theme["head"]):
                seen_blue = True
            elif seen_blue and color in theme["wake"]:
                color = theme["wake"][color]
            out.append(color + s.group(3))
            pos = s.end()
        out.append(block[pos:])
        return "".join(out)

    return KF_RE.sub(fix_block, svg)


def recolor(path, theme_name):
    theme = THEMES[theme_name]
    s = path.read_text()
    s = s.replace(RAW_HEAD, theme["head"]).replace(RAW_BODY, theme["body"])
    s = s.replace(RAW_TEXT, theme["text"])
    s = recolor_keyframes(s, theme)
    for old, new in theme["palette"].items():
        s = s.replace(old, new)
    head_end = s.index(">", s.index("<svg")) + 1
    panel = f'<rect x="0" y="0" width="100%" height="100%" fill="{theme["panel"]}" rx="12"/>'
    s = s[:head_end] + panel + s[head_end:]
    path.write_text(s)
    print(f"recolored {path} ({theme_name})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", choices=THEMES, default="dark")
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()
    for p in args.paths:
        recolor(Path(p), args.theme)


if __name__ == "__main__":
    main()
