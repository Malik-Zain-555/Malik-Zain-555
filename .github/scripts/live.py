#!/usr/bin/env python3
"""The "Live from GitHub" tile.

    python .github/scripts/live.py        ->  assets/live.svg   (run by the GitHub Action; GITHUB_TOKEN is optional)
build_assets.py calls render_live() too, so a fresh checkout already has a tile before the first Action run.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ui import *  # noqa: E402,F401,F403

USER = os.environ.get("GH_USER", "Malik-Zain-555")
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "assets", "live.svg"))
LANG_COL = [CB, TG, MT, LC, YE, PK]
FALLBACK_REPOS = ["sahi-daam-fair-price-detector", "resume-category-classifier", "fake_news_style_detector", "churn-prediction-pipeline", "MUDABBIR-FYP"]
TITLE = "Live from GitHub"
SUB = "Pulled from the GitHub API and redrawn by a GitHub Action every few hours."


def _get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-readme"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fetch():
    u = _get(f"https://api.github.com/users/{USER}")
    rp = _get(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed")
    if not isinstance(rp, list):
        raise RuntimeError("repos not a list")
    own = [r for r in rp if not r.get("fork")]
    langs = {}
    for r in own:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    return dict(repos=u.get("public_repos"), followers=u.get("followers"), stars=sum(r.get("stargazers_count", 0) for r in own),
                langs=sorted(langs.items(), key=lambda kv: -kv[1])[:6], recent=[(r["name"], r.get("pushed_at")) for r in own[:5]],
                updated=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))


def seed_data():
    """Real numbers when the API answers, otherwise dashes until the Action runs."""
    try:
        return fetch()
    except Exception as e:  # rate limit, offline...
        print("  (live tile seeded without API data:", str(e)[:60] + ")")
        return dict(repos=None, followers=None, stars=None, langs=[], recent=[(n, None) for n in FALLBACK_REPOS], updated=None)


def ago(iso):
    if not iso:
        return "waiting for the first sync"
    days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 86400
    return "pushed today" if days < 1 else "pushed yesterday" if days < 2 else f"pushed {round(days)} days ago"


def render_live(data, path=OUT):
    W, P = 1000, 56
    d0 = Doc(W, 10, "x")
    y = section_header(d0, TITLE, SUB, P, P)
    langs = data["langs"]
    tot = sum(c for _, c in langs) or 1
    y0 = y + 20
    card_h, rowh = 132, 50
    ly = y0 + card_h + 30
    legend_rows, x = 1, 0
    for n, c in langs:
        w = 22 + tw("f6", f"{n} {c}", 16) + 22
        if x + w > W - 2 * P:
            legend_rows, x = legend_rows + 1, 0
        x += w
    ry = ly + 22 + 14 + legend_rows * 30 + 18
    n_rec = len(data["recent"])
    H = int(ry + n_rec * (rowh + 8) + (30 if data.get("updated") else 0) + P - 8)
    d = Doc(W, H, "Live from GitHub: " + f"{data['repos']} public repos, {data['followers']} followers, {data['stars']} stars earned. Languages: " + ", ".join(n for n, _ in langs) + ". Recently pushed: " + ", ".join(n for n, _ in data["recent"]) + ".")
    tile(d, SN)
    section_header(d, TITLE, SUB, P, P)
    gap = 20
    cw = (W - 2 * P - 2 * gap) / 3
    for i, (val, lab_) in enumerate([(data["repos"], "public repos"), (data["followers"], "followers"), (data["stars"], "stars earned")]):
        x = P + i * (cw + gap)
        d.add(f'<rect x="{x + 1:.1f}" y="{y0 + 1}" width="{cw - 2:.1f}" height="{card_h - 2}" rx="24" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        d.T(x + 22, y0 + 76, "—" if val is None else str(val), "d", 46, INK, ls=-2.3)
        d.T(x + 22, y0 + 108, lab_, "f4", 19, INK, op=.78)
    # language bar
    bw = W - 2 * P
    cp = d.uid("c")
    d.defs.append(f'<clipPath id="{cp}"><rect x="{P}" y="{ly}" width="{bw}" height="22" rx="11"/></clipPath>')
    if langs:
        xx, segs = P, ""
        for i, (n, c) in enumerate(langs):
            w = bw * c / tot
            segs += f'<rect x="{xx:.1f}" y="{ly}" width="{w + .5:.1f}" height="22" fill="{LANG_COL[i]}"/>'
            xx += w
        d.add(f'<g clip-path="url(#{cp})">{segs}</g>')
    else:
        d.add(f'<rect x="{P}" y="{ly}" width="{bw}" height="22" rx="11" fill="{INK}" fill-opacity=".12"/>')
    x, row = P, 0
    for i, (n, c) in enumerate(langs):
        lab_ = f"{n} {c}"
        w = 22 + tw("f6", lab_, 16) + 22
        if x + w - 22 > W - P:
            x, row = P, row + 1
        yy = ly + 22 + 14 + row * 30 + 14
        d.add(f'<circle cx="{x + 7}" cy="{yy - 5}" r="7" fill="{LANG_COL[i]}" stroke="{INK}" stroke-width="1.5"/>')
        d.T(x + 22, yy, lab_, "f6", 16, INK, op=.85)
        x += w
    # recently pushed
    for i, (name, iso) in enumerate(data["recent"]):
        yy = ry + i * (rowh + 8)
        d.add(f'<rect x="{P + 1}" y="{yy + 1}" width="{bw - 2}" height="{rowh - 2}" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        d.T(P + 20, yy + 32, name, "f6", 19, INK)
        d.T(P + bw - 20, yy + 32, ago(iso), "f4", 17, INK, "end", op=.65)
    if data.get("updated"):
        d.T(P, H - P + 6, "Last synced " + data["updated"], "f4", 14, INK, op=.5)
    d.save(path)


if __name__ == "__main__":
    render_live(fetch())
