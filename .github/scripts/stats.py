#!/usr/bin/env python3
"""Battle Log — pulls real numbers from the GitHub GraphQL API and redraws
assets/stats.svg and assets/heatmap.svg in the arcade style. No third-party widgets."""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arcade import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parents[2]
QUERY = """query($login:String!){user(login:$login){
 followers{totalCount}
 repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){totalCount nodes{stargazerCount
  languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount}}}}}}"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-battle-log"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data or not data.get("data", {}).get("user"):
        raise RuntimeError(f"GraphQL error: {data.get('errors')}")
    return data["data"]["user"]


def summarize(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    cur = 0
    seq = [d["contributionCount"] for d in days]
    i = len(seq) - 1
    if i >= 0 and seq[i] == 0:  # today may not be finished yet
        i -= 1
    while i >= 0 and seq[i] > 0:
        cur += 1
        i -= 1
    best = run = 0
    for c in seq:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]
            langs.setdefault(n["name"], [0, n["color"] or "#8F88AD"])
            langs[n["name"]][0] += e["size"]
    total = sum(v[0] for v in langs.values()) or 1
    top = sorted(((k, v[0] / total, v[1]) for k, v in langs.items()), key=lambda t: -t[1])[:6]
    return {
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "year": u["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "streak": cur,
        "best": best,
        "langs": top,
        "days": days,
    }


def render_stats(d):
    W, H = 880, 300
    tiles = [("REPOS", "repos", CYA), ("FOLLOWERS", "followers", PUR), ("STARS", "stars", GOLD),
             ("THIS YEAR", "year", ORG), ("STREAK", "streak", RED), ("BEST STREAK", "best", PINK)]
    body = ""
    tw, gap = 138, 10
    for i, (lab, key, col) in enumerate(tiles):
        x = i * (tw + gap) + 1
        val = f"{d[key]:,}" if d else "--"
        body += (f'<g transform="translate({x} 22)"><polygon points="{poly(tw, 92, 10)}" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>'
                 + disp(tw / 2, 60, val, fit(val, tw - 20, 44, 0.62), col, "middle")
                 + mono(tw / 2, 82, lab, 11.5, SOFT, "middle", 2) + "</g>")
    body += mono(28, 150, "TOP LANGUAGES", 13, GOLD, ls=4)
    if d and d["langs"]:
        x, bw = 28, W - 56
        leg_x = 28
        for j, (name, pct, col) in enumerate(d["langs"]):
            w = max(4, bw * pct)
            body += f'<rect x="{x:.1f}" y="164" width="0" height="22" fill="{col}">{A("width", [0, f"{w - 2:.1f}", f"{w - 2:.1f}", 0], [0, .15, .9, 1], 9, j * .15)}</rect>'
            x += w
            body += f'<circle cx="{leg_x + 6}" cy="218" r="6" fill="{col}"/>' + mono(leg_x + 18, 223, f"{name} {pct * 100:.0f}%", 13, SOFT)
            leg_x += 18 + len(f"{name} {pct * 100:.0f}%") * 8.2 + 22
    else:
        body += f'<rect x="28" y="164" width="{W - 56}" height="22" fill="{EDGE}"/>'
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if d else "waiting for first sync"
    body += f'<line x1="28" y1="250" x2="{W - 28}" y2="250" stroke="{EDGE}"/>'
    body += mono(28, 278, f"LAST SYNC  {stamp}", 12, DIM, ls=1.5) + mono(W - 28, 278, "AUTO-UPDATES EVERY 6 HOURS", 12, DIM, "end", 1.5)
    body += sweep(W, H, dur=6)
    return svg(W, H, body, "Battle log: live GitHub numbers", glows=[(780, 40, 140, ORG, 0.12)])


def render_heatmap(d):
    W, H = 880, 214
    pal = ["#1A1426", "#4C1D95", PUR, ORG, GOLD]
    weeks = {}
    days = d["days"] if d else []
    if days:
        mx = max(x["contributionCount"] for x in days) or 1
        first = dt.date.fromisoformat(days[0]["date"])
        start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # Sunday on/before first day
        for x in days:
            dd = dt.date.fromisoformat(x["date"])
            col = (dd - start).days // 7
            c = x["contributionCount"]
            lvl = 0 if c == 0 else 1 if c <= mx * .25 else 2 if c <= mx * .5 else 3 if c <= mx * .75 else 4
            weeks.setdefault(lvl, []).append((col, (dd.weekday() + 1) % 7))
        ncols = max(c for lv in weeks.values() for c, _ in lv) + 1
    else:
        ncols = 53
        weeks[0] = [(c, r) for c in range(53) for r in range(7)]
    x0, y0, pitch = 16, 56, 16
    body = mono(28, 34, "BATTLE LOG  //  LAST 12 MONTHS", 13, GOLD, ls=4)
    total = f"{d['year']:,} CONTRIBUTIONS" if d else "SYNCING..."
    body += mono(W - 28, 34, total, 13, SOFT, "end", 2)
    for lvl in sorted(weeks):
        rects = "".join(f'<rect x="{x0 + c * pitch}" y="{y0 + r * pitch}" width="13" height="13" rx="2"/>' for c, r in weeks[lvl])
        anim = A("opacity", [1, .55, 1], dur=2.8 + lvl * .7, begin=lvl * .4) if lvl >= 2 else ""
        body += f'<g fill="{pal[lvl]}">{rects}{anim}</g>'
    gh = 7 * pitch
    body += f'<clipPath id="grid"><rect x="{x0}" y="{y0}" width="{ncols * pitch}" height="{gh}"/></clipPath>'
    body += (f'<g clip-path="url(#grid)"><defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
             f'<rect x="-90" y="{y0}" width="90" height="{gh}" fill="url(#sw)">{A("x", [-90, ncols * pitch + 20], dur=5)}</rect></g>')
    ly = y0 + gh + 22
    body += mono(W - 160, ly + 4, "LESS", 11, DIM, "end", 1)
    for i, c in enumerate(pal):
        body += f'<rect x="{W - 150 + i * 18}" y="{ly - 7}" width="13" height="13" rx="2" fill="{c}"/>'
    body += mono(W - 56, ly + 4, "MORE", 11, DIM, ls=1)
    return svg(W, H, body, "Contribution heatmap, last 12 months")


def write_all(d):
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "stats.svg").write_text(render_stats(d), encoding="utf-8")
    (ROOT / "assets" / "heatmap.svg").write_text(render_heatmap(d), encoding="utf-8")


def main():
    login = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "Malik-Zain-555"
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        sys.exit("GITHUB_TOKEN missing")
    write_all(summarize(fetch(login, token)))
    print("battle log updated for", login)


if __name__ == "__main__":
    main()
