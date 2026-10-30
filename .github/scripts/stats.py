#!/usr/bin/env python3
"""Contribution log — real numbers from GitHub, redrawn into assets/stats.svg and assets/heatmap.svg.
Source 1: GraphQL API (needs GITHUB_TOKEN).  Source 2 (automatic fallback): public REST API + the public
contribution calendar page.  Fails (non-zero exit) only if BOTH fail, and prints why."""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ui import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parents[2]
QUERY = """query($login:String!){user(login:$login){
 followers{totalCount}
 repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){totalCount nodes{stargazerCount
  languages(first:8,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
 contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date weekday contributionCount}}}}}}"""
LANG_COLORS = {"JavaScript": "#f1e05a", "Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "TypeScript": "#3178c6", "HTML": "#e34c26",
               "CSS": "#563d7c", "EJS": "#a91e50", "Java": "#b07219", "C#": "#178600", "Dart": "#00B4AB", "Shell": "#89e051"}


def http(url, token="", accept=None, data=None):
    h = {"User-Agent": "profile-contribution-log"}
    if token and "api.github.com" in url:
        h["Authorization"] = f"Bearer {token}"
    if accept:
        h["Accept"] = accept
    if data is not None:
        h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def streaks(counts):
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today may not be finished yet
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur, i = cur + 1, i - 1
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    return cur, best


def finish(repos, followers, stars, days, langs_bytes, colors, year_total=None):
    days.sort(key=lambda d: d["date"])
    cur, best = streaks([d["contributionCount"] for d in days])
    total = sum(langs_bytes.values()) or 1
    top = sorted(((k, v / total, colors.get(k) or LANG_COLORS.get(k, "#80848E")) for k, v in langs_bytes.items()), key=lambda t: -t[1])[:6]
    return {"repos": repos, "followers": followers, "stars": stars, "year": year_total if year_total is not None else sum(d["contributionCount"] for d in days),
            "streak": cur, "best": best, "langs": top, "days": days}


def from_graphql(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    data = json.loads(http("https://api.github.com/graphql", token, data=body))
    u = (data.get("data") or {}).get("user")
    if "errors" in data or not u:
        raise RuntimeError(f"GraphQL returned errors: {data.get('errors')}")
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    langs, colors = {}, {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
            colors[e["node"]["name"]] = e["node"]["color"]
    return finish(u["repositories"]["totalCount"], u["followers"]["totalCount"], sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
                  days, langs, colors, u["contributionsCollection"]["contributionCalendar"]["totalContributions"])


def parse_calendar(page):
    """Parse GitHub's public contribution calendar HTML into day dicts."""
    tips = {m.group(1): m.group(2) for m in re.finditer(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page)}
    approx = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}
    days = []
    for m in re.finditer(r"<td\b[^>]*ContributionCalendar-day[^>]*>", page):
        tag = m.group(0)
        date, lvl, cid = (re.search(p, tag) for p in (r'data-date="([^"]+)"', r'data-level="(\d)"', r'\bid="([^"]+)"'))
        if not date:
            continue
        d = dt.date.fromisoformat(date.group(1))
        count = None
        if cid and cid.group(1) in tips:
            t = tips[cid.group(1)]
            n = re.search(r"(\d[\d,]*)\s+contribution", t)
            count = int(n.group(1).replace(",", "")) if n else (0 if "No contribution" in t else None)
        if count is None:
            count = approx.get(int(lvl.group(1)) if lvl else 0, 0)
        days.append({"date": d.isoformat(), "weekday": (d.weekday() + 1) % 7, "contributionCount": count})
    if not days:
        raise RuntimeError("could not parse the contribution calendar")
    m = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", page)
    return days, int(m.group(1).replace(",", "")) if m else None


def from_public(login, token):
    user = json.loads(http(f"https://api.github.com/users/{login}", token))
    repos = [r for r in json.loads(http(f"https://api.github.com/users/{login}/repos?per_page=100&type=owner", token)) if not r["fork"]]
    langs = {}
    for r in repos[:40]:
        try:
            for k, v in json.loads(http(r["languages_url"], token)).items():
                langs[k] = langs.get(k, 0) + v
        except Exception:
            pass
    days, total = parse_calendar(http(f"https://github.com/users/{login}/contributions"))
    return finish(user["public_repos"], user["followers"], sum(r["stargazers_count"] for r in repos), days, langs, {}, total)


def collect(login, token):
    errors = []
    for name, fn in (("GraphQL", from_graphql), ("public REST + calendar", from_public)):
        try:
            d = fn(login, token)
            print(f"source: {name}")
            return d
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {e}")
            print(f"[warn] {name} failed -> {e}")
    raise RuntimeError(" | ".join(errors))


def render_stats(d):
    W, H = 880, 236
    cols = [("REPOS", "repos", TX), ("FOLLOWERS", "followers", TX), ("STARS", "stars", TX), ("LAST 12 MONTHS", "year", OR), ("CURRENT STREAK", "streak", MINT), ("BEST STREAK", "best", AMB)]
    cw = (W - 64) / 6
    body = ""
    for i, (lab, key, col) in enumerate(cols):
        x = 32 + i * cw
        val = f"{d[key]:,}" if d else "–"
        if i:
            body += f'<line x1="{x:.0f}" y1="34" x2="{x:.0f}" y2="104" stroke="{LINE}"/>'
        body += serif(x + cw / 2, 78, val, fit(val, cw - 18, 44, .5), col, "middle") + mono(x + cw / 2, 100, lab, 10.5, MUT, "middle", 1.5)
    body += f'<line x1="32" y1="126" x2="{W - 32}" y2="126" stroke="{LINE}"/>' + mono(32, 152, "LANGUAGES BY CODE SIZE", 11, MUT, ls=2.5)
    if d and d["langs"]:
        x, bw, lx = 32, W - 64, 32
        for j, (name, pct, col) in enumerate(d["langs"]):
            w = max(4, bw * pct)
            body += f'<rect x="{x:.1f}" y="164" width="0" height="10" rx="2" fill="{col}">{A("width", [0, f"{max(1, w - 3):.1f}", f"{max(1, w - 3):.1f}", 0], [0, .15, .9, 1], 10, j * .12)}</rect>'
            x += w
            label = f"{name} {pct * 100:.0f}%"
            body += f'<circle cx="{lx + 5}" cy="198" r="4.5" fill="{col}"/>' + mono(lx + 15, 202, label, 12, SOFT)
            lx += 15 + len(label) * 7.4 + 22
    else:
        body += f'<rect x="32" y="164" width="{W - 64}" height="10" rx="2" fill="{LINE}"/>' + mono(32, 202, "Loads after the first GitHub Action run (Actions → Contribution log → Run workflow).", 12, MUT)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if d else "not synced yet"
    body += mono(32, 224, f"LAST SYNC  {stamp}", 10.5, MUT, ls=1) + mono(W - 32, 224, "AUTO-UPDATES EVERY 6 HOURS", 10.5, MUT, "end", 1)
    return svg(W, H, body, "Contribution numbers: repos, followers, stars, last 12 months, streaks, languages")


HEAT = ["#1A1D23", "#4B2B22", "#8E3B26", "#E0552F", "#FFB27A"]


def render_heatmap(d):
    W, H = 880, 214
    levels, days, ncols = {}, (d["days"] if d else []), 53
    if days:
        mx = max(x["contributionCount"] for x in days) or 1
        first = dt.date.fromisoformat(days[0]["date"])
        start = first - dt.timedelta(days=(first.weekday() + 1) % 7)
        for x in days:
            dd = dt.date.fromisoformat(x["date"])
            c = x["contributionCount"]
            lv = 0 if c == 0 else 1 if c <= mx * .25 else 2 if c <= mx * .5 else 3 if c <= mx * .75 else 4
            levels.setdefault(lv, []).append(((dd - start).days // 7, (dd.weekday() + 1) % 7))
        ncols = max(c for lv in levels.values() for c, _ in lv) + 1
    else:
        levels[0] = [(c, r) for c in range(53) for r in range(7)]
    x0, y0, pitch = 16, 58, 16
    body = mono(32, 36, "CONTRIBUTION LOG  ·  LAST 12 MONTHS", 11.5, OR, ls=2.5) + mono(W - 32, 36, f"{d['year']:,} CONTRIBUTIONS" if d else "NOT SYNCED YET", 11.5, SOFT, "end", 1.5)
    for lv in sorted(levels):
        rects = "".join(f'<rect x="{x0 + c * pitch}" y="{y0 + r * pitch}" width="13" height="13" rx="3"/>' for c, r in levels[lv])
        body += f'<g fill="{HEAT[lv]}">{rects}{A("opacity", [1, .6, 1], dur=3 + lv * .6, begin=lv * .4) if lv >= 2 else ""}</g>'
    ly = y0 + 7 * pitch + 22
    body += mono(W - 164, ly + 4, "LESS", 10.5, MUT, "end", 1) + "".join(f'<rect x="{W - 154 + i * 18}" y="{ly - 7}" width="13" height="13" rx="3" fill="{c}"/>' for i, c in enumerate(HEAT)) + mono(W - 58, ly + 4, "MORE", 10.5, MUT, ls=1)
    return svg(W, H, body, "Contribution heatmap, last 12 months")


def write_all(d):
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "stats.svg").write_text(render_stats(d), encoding="utf-8")
    (ROOT / "assets" / "heatmap.svg").write_text(render_heatmap(d), encoding="utf-8")


def main():
    login = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "Malik-Zain-555"
    write_all(collect(login, os.environ.get("GITHUB_TOKEN", "")))
    print("contribution log updated for", login)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        sys.exit(f"contribution log FAILED: {e}")
