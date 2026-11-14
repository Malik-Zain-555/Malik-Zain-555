#!/usr/bin/env python3
"""Rebuilds README.md from projects.json (your curated words and numbers) + live data from the GitHub API
(stars, language, last push, latest commit, follower count, recently pushed repos).
Run by GitHub Actions every 6 hours, on every edit of projects.json, or by hand:  python .github/scripts/update_readme.py
Offline preview (no network):  python .github/scripts/update_readme.py --offline"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))


def api(path, token=""):
    h = {"User-Agent": "profile-readme-updater", "Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=h), timeout=30) as r:
        return json.load(r)


def rel(iso):
    if not iso:
        return "unknown"
    d = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    return "today" if d < 1 else "yesterday" if d < 2 else f"{d} days ago" if d < 45 else f"{d // 30} months ago"


def fetch_live(cfg, token):
    u = cfg["user"]
    user = api(f"/users/{u}", token)
    repos = [r for r in api(f"/users/{u}/repos?per_page=100&sort=pushed&type=owner", token) if not r["fork"]]
    per = {}
    for p in cfg["projects"]:
        try:
            r = api(f"/repos/{u}/{p['repo']}", token)
            c = api(f"/repos/{u}/{p['repo']}/commits?per_page=1", token)
            per[p["repo"]] = {"stars": r["stargazers_count"], "lang": r["language"], "pushed": r["pushed_at"],
                              "commit": (c[0]["commit"]["message"].splitlines()[0] if c else ""), "cdate": (c[0]["commit"]["author"]["date"] if c else None)}
        except urllib.error.HTTPError as e:
            print(f"[warn] {p['repo']}: HTTP {e.code} (check the repo name in projects.json)")
    return {"repos": user["public_repos"], "followers": user["followers"], "stars": sum(r["stargazers_count"] for r in repos),
            "per": per, "recent": [{"name": r["name"], "url": r["html_url"], "desc": r["description"] or "", "pushed": r["pushed_at"]} for r in repos[:5]]}


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def short(s, n=64):
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def build(cfg, live):
    u, site = cfg["user"], cfg["site"]
    out = [f'<p align="center"><a href="{site}"><img src="banner.svg" alt="{cfg["name"]}. I learn by building, not by theory. Open the interactive site." width="100%"></a></p>\n',
           f'<h3 align="center">The full experience lives on my site: <a href="{site}">{site.replace("https://", "")}</a></h3>\n']
    if live:
        today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        out.append(f'<p align="center"><b>{live["repos"]}</b> public repos · <b>{live["followers"]}</b> followers · <b>{live["stars"]}</b> stars earned · <sub>synced automatically, last on {today}</sub></p>\n')
    out.append(f"## Hi, I'm {cfg['name']}\n\n{cfg['intro']}\n\n## What I built\n")
    out.append("| Project | Result | The honest caveat | Live from GitHub |\n|---|---|---|---|")
    for p in cfg["projects"]:
        d = (live or {}).get("per", {}).get(p["repo"])
        if d:
            bits = [f"★ {d['stars']}"] + ([d["lang"]] if d["lang"] else []) + [f"pushed {rel(d['pushed'])}"]
            lv = " · ".join(bits) + (f"<br><sub>last commit: “{esc(short(d['commit']))}”</sub>" if d["commit"] else "")
        else:
            lv = "–"
        out.append(f"| [{p['repo']}](https://github.com/{u}/{p['repo']}) | {esc(p['result'])} | {esc(p['caveat'])} | {lv} |")
    if live and live["recent"]:
        out.append("\n## Recently pushed\n")
        out += [f"- [{r['name']}]({r['url']}) · {esc(short(r['desc'], 70)) + ' · ' if r['desc'] else ''}pushed {rel(r['pushed'])}" for r in live["recent"]]
    out.append(f'\n## Activity\n\n<p align="center"><img src="https://ghchart.rshah.org/2b3cff/{u}" alt="Contribution graph for {u}" width="100%"></p>\n')
    out.append(f"## Now, next, later\n\n- **Now:** {cfg['now']}.\n- **Next:** {cfg['next']}.\n- **Later:** {cfg['later']}.\n\nI label anything built with AI as AI-built, and tutorial work as tutorial-guided.\n")
    out.append('<p align="center">' + " · ".join(f'<a href="{h}">{n}</a>' for n, h in cfg["links"]) + f'</p>\n<p align="center"><sub><i>{cfg["quote"]}</i></sub></p>\n')
    return "\n".join(out)


def main():
    live = None
    if "--offline" not in sys.argv:
        try:
            live = fetch_live(CFG, os.environ.get("GITHUB_TOKEN", ""))
        except Exception as e:  # noqa: BLE001
            sys.exit(f"README update FAILED (README left unchanged): {e}")
    (ROOT / "README.md").write_text(build(CFG, live), encoding="utf-8")
    print("README.md rebuilt", "(live data)" if live else "(offline preview)")


if __name__ == "__main__":
    main()
