#!/usr/bin/env python3
"""Generates a neofetch style profile card (dark + light SVG).

Data comes live from the GitHub REST + GraphQL APIs so the card stays
accurate without any third party service. Runs locally or in Actions.
"""
import calendar
import json
import math
import os
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

USER = "jhannesreimann"
OUT_DIR = Path(__file__).parent / "assets"

ASCII_FACE = (Path(__file__).parent / "assets" / "ascii-face.txt").read_text().rstrip("\n")

EMAIL = "reimann.jhannes@gmail.com"
LINKEDIN = "linkedin.com/in/jhannes-reimann"

CHAR_W = 8.4          # monospace advance width at FONT_SIZE
FONT_SIZE = 14.5
LINE_H = 20.0
PAD = 28              # canvas padding
GAP = 42              # gap between face and panel columns
PANEL_W = 58          # panel width in characters, used by rules and wrapping

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "face": "#58a6ff",
        "header": "#58a6ff",
        "rule": "#30363d",
        "label": "#f0883e",
        "value": "#c9d1d9",
        "dim": "#8b949e",
        "plus": "#3fb950",
        "minus": "#f85149",
    },
    "light": {
        "bg": "#ffffff",
        "face": "#0969da",
        "header": "#0969da",
        "rule": "#d0d7de",
        "label": "#bc4c00",
        "value": "#24292f",
        "dim": "#656d76",
        "plus": "#1a7f37",
        "minus": "#cf222e",
    },
}


def api_rest(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"User-Agent": "fetch.py", "Authorization": f"Bearer {token()}"},
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def api_graphql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "User-Agent": "fetch.py",
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""


def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")


def account_age(created, today):
    """Calendar difference like '22 years, 5 months, 29 days'."""
    years = today.year - created.year
    months = today.month - created.month
    days = today.day - created.day
    if days < 0:
        months -= 1
        prev_month = today.month - 1 or 12
        prev_year = today.year - (1 if today.month == 1 else 0)
        days += calendar.monthrange(prev_year, prev_month)[1]
    if months < 0:
        years -= 1
        months += 12
    return years, months, days


def lifetime_commits(created):
    """Sum contributions across all years since account creation."""
    total = 0
    for year in range(created.year, datetime.now(timezone.utc).year + 1):
        start = max(created, datetime(year, 1, 1, tzinfo=timezone.utc))
        end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), datetime.now(timezone.utc))
        data = api_graphql(
            """
            query($login: String!, $from: DateTime!, $to: DateTime!) {
                user(login: $login) {
                    contributionsCollection(from: $from, to: $to) {
                        contributionCalendar { totalContributions }
                    }
                }
            }""",
            {"login": USER, "from": start.isoformat(), "to": end.isoformat()},
        )
        total += data["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return total


def repo_loc(full_name):
    """Additions/deletions on the default branch, paginated."""
    additions = deletions = 0
    cursor = None
    while True:
        after = f'"{cursor}"' if cursor else "null"
        data = api_graphql(
            """
            query($owner: String!, $name: String!) {
                repository(owner: $owner, name: $name) {
                    defaultBranchRef {
                        target {
                            ... on Commit {
                                history(first: 100, after: %s) {
                                    totalCount
                                    edges {
                                        node { additions deletions }
                                    }
                                    pageInfo { hasNextPage endCursor }
                                }
                            }
                        }
                    }
                }
            }"""
            % after,
            {"owner": full_name.split("/")[0], "name": full_name.split("/")[1]},
        )
        history = data["repository"]["defaultBranchRef"]["target"]["history"]
        for edge in history["edges"]:
            additions += edge["node"]["additions"]
            deletions += edge["node"]["deletions"]
        if not history["pageInfo"]["hasNextPage"]:
            break
        cursor = history["pageInfo"]["endCursor"]
    return additions, deletions


def collect_stats():
    profile = api_rest(f"/users/{USER}")
    repos = api_rest(f"/users/{USER}/repos?per_page=100&sort=updated")
    own = [r for r in repos if not r["fork"]]

    stars = sum(r["stargazers_count"] for r in own)

    lang_bytes = {}
    lang_counts = {}
    for r in own:
        try:
            langs = api_rest(f"/repos/{USER}/{r['name']}/languages")
        except Exception:
            continue
        for lang, b in langs.items():
            lang_bytes[lang] = lang_bytes.get(lang, 0) + b
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    contributions = api_graphql(
        '{ user(login: "%s") { contributionsCollection { '
        "contributionCalendar { totalContributions } } } }" % USER
    )["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

    created = datetime.fromisoformat(profile["created_at"].replace("Z", "+00:00"))
    age = account_age(created.date(), date.today())

    commits = lifetime_commits(created)
    added = deleted = 0
    for r in own:
        try:
            a, d = repo_loc(r["full_name"])
            added += a
            deleted += d
        except Exception as exc:
            print(f"loc skipped {r['name']}: {exc}", file=sys.stderr)

    return {
        "followers": profile["followers"],
        "public_repos": len(own),
        "stars": stars,
        "lang_bytes": lang_bytes,
        "lang_counts": lang_counts,
        "contributions": contributions,
        "created": created,
        "age": age,
        "commits": commits,
        "added": added,
        "deleted": deleted,
    }


def top_languages(lang_bytes, lang_counts, limit=6):
    """Rank by how many repos use a language, weighted by volume.

    Raw bytes alone would put Jupyter notebooks (mostly JSON output bloat)
    on top and bury Rust or QML, which power whole projects despite their
    small footprint. Markup and config formats stay out entirely.
    """
    not_programming = {"Jupyter Notebook", "Shell", "CSS", "HTML", "Dockerfile", "Nix"}
    scored = [
        (lang, lang_counts.get(lang, 0) * math.log10(bytes + 1))
        for lang, bytes in lang_bytes.items()
        if lang not in not_programming
    ]
    scored.sort(key=lambda x: -x[1])
    return [lang for lang, _ in scored[:limit]]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def kv_line(label, value):
    """label, dotted leader, value flush against the right panel border."""
    return kv_segments(label, [(value, "value")])


def kv_segments(label, value_segs):
    lab = f"{label}:"
    used = len(lab) + sum(len(text) for text, _ in value_segs)
    dots = PANEL_W - used
    leader = ("." * dots if dots >= 2 else "..", "dim")
    return [(lab, "label"), leader] + value_segs


def rule_line(title):
    """section header like: - Contact ---------------"""
    head = f"- {title} "
    return [
        (head, "header"),
        ("-" * max(4, PANEL_W - len(head)), "rule"),
    ]


def blank():
    return [("", "value")]


def build_panel_lines(s):
    langs = top_languages(s["lang_bytes"], s["lang_counts"])

    def wrap_langs(label, items):
        lab = f"{label}:"
        rest = list(items)
        chunk = ""
        while rest and len(lab) + 2 + len(chunk) + len(rest[0]) <= PANEL_W:
            chunk += (", " if chunk else "") + rest.pop(0)
        dots = max(2, PANEL_W - len(lab) - len(chunk))
        lines = [[(lab, "label"), ("." * dots, "dim"), (chunk, "value")]]
        while rest:
            chunk = ""
            while rest and len(chunk) + len(", ") + len(rest[0]) <= PANEL_W:
                chunk += (", " if chunk else "") + rest.pop(0)
            lines.append([(" " * (PANEL_W - len(chunk)), "dim"), (chunk, "value")])
        return lines

    y, m, d = s["age"]
    uptime = f"{plural(y, 'year')}, {plural(m, 'month')}, {plural(d, 'day')}"

    lines = [[(f"{USER}@github", "header"), (" " + "-" * (PANEL_W - len(USER) - 7), "rule")]]
    lines += [
        kv_line("OS", "Arch Linux + Android"),
        kv_line("Uptime", uptime),
        kv_line("Host", "Hasso Plattner Institute"),
        kv_line("Focus", "MSc Computer Science, Security Engineering"),
        kv_line("Work", "Working student at SAP"),
    ]
    lines.append(blank())
    lines.append(rule_line("Languages"))
    lines += wrap_langs("Programming", langs)
    lines.append(kv_line("Real", "English, German"))
    lines.append(blank())
    lines.append(rule_line("Hobbies"))
    lines.append(kv_line("Software", "Arch ricing, Wayland setups, security labs"))
    lines.append(kv_line("Hardware", "Raspberry Pi builds, RF gear"))
    lines.append(blank())
    lines.append(rule_line("Contact"))
    lines += [
        kv_line("Email.Personal", EMAIL),
        kv_line("Email.Work", "jhannes.reimann@sap.com"),
        kv_line("Email.Uni", "Jhannes.Reimann@student.hpi.de"),
        kv_line("LinkedIn", LINKEDIN),
        kv_line("Discord", "noaa"),
    ]
    lines.append(blank())
    lines.append(rule_line("GitHub Stats"))
    lines += [
        [
            (f"Repos: {s['public_repos']}", "label"),
            ("   ", "dim"),
            (f"Stars: {s['stars']}", "label"),
            ("   ", "dim"),
            (f"Followers: {s['followers']}", "label"),
        ],
        kv_line("Commits", f"{s['commits']:,}"),
        kv_segments(
            "Lines of Code on GitHub",
            [
                (f"{s['added'] + s['deleted']:,} ", "value"),
                ("( ", "dim"),
                (f"{s['added']:,}++", "plus"),
                (",  ", "value"),
                (f"{s['deleted']:,}--", "minus"),
                (" )", "dim"),
            ],
        ),
    ]
    return lines


def svg(theme_name, panel_lines):
    c = THEMES[theme_name]
    face_lines = ASCII_FACE.splitlines()
    face_cols = max(len(l) for l in face_lines)
    face_w = face_cols * CHAR_W
    panel_x = PAD + face_w + GAP
    longest_panel = max(
        sum(len(text) for text, _ in segs) for segs in panel_lines
    )
    width = panel_x + longest_panel * CHAR_W + PAD
    height = PAD * 2 + max(len(face_lines), len(panel_lines)) * LINE_H

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect width="100%" height="100%" fill="{c["bg"]}" rx="12"/>',
        "<style>",
        f"text {{ font-family: ui-monospace, 'JetBrains Mono', 'Cascadia Code', Menlo, Consolas, monospace; font-size: {FONT_SIZE}px; }}",
        f".face {{ fill: {c['face']}; }}",
        f".header {{ fill: {c['header']}; }}",
        f".label {{ fill: {c['label']}; }}",
        f".value {{ fill: {c['value']}; }}",
        f".dim {{ fill: {c['dim']}; }}",
        f".rule {{ fill: {c['rule']}; }}",
        f".plus {{ fill: {c['plus']}; }}",
        f".minus {{ fill: {c['minus']}; }}",
        "</style>",
    ]

    y = PAD + FONT_SIZE
    for line in face_lines:
        parts.append(
            f'<text class="face" x="{PAD:.0f}" y="{y:.1f}" xml:space="preserve">{esc(line)}</text>'
        )
        y += LINE_H

    y = PAD + FONT_SIZE
    for segs in panel_lines:
        spans = "".join(
            f'<tspan class="{cls}">{esc(text)}</tspan>' for text, cls in segs
        )
        parts.append(
            f'<text x="{panel_x:.0f}" y="{y:.1f}" xml:space="preserve">{spans}</text>'
        )
        y += LINE_H

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    s = collect_stats()
    OUT_DIR.mkdir(exist_ok=True)
    panel = build_panel_lines(s)
    for theme in ("dark", "light"):
        out = OUT_DIR / f"fetch-{theme}.svg"
        out.write_text(svg(theme, panel))
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
