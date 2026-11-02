#!/usr/bin/env python3
"""The three live tiles: live.svg (numbers, languages, recent), year.svg (animated year) and compare.svg (comparisons, milestones).

    python .github/scripts/live.py        ->  assets/live.svg, assets/year.svg, assets/compare.svg   (run by the GitHub Action)

All numbers are real. Contribution calendars come from github.com/users/<you>/contributions (public, no token), one per year, so
streaks and totals can go back to when I started. Repo data comes from the REST API when it answers (token in the Action),
otherwise from the public profile pages.
"""
import datetime as dt
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ui import *  # noqa: E402,F401,F403

USER = os.environ.get("GH_USER", "Malik-Zain-555")
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", "assets"))
LANG_COL = [CB, TG, MT, LC, YE, PK, "#9aa0b5"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY3 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HEAT_DARK = ["#22253d", "#4452e6", "#7c8cff", "#b9c4ff", MT]
W, P = 1000, 56
BW = W - 2 * P


# ═════════════════════════ fetching ═════════════════════════
def _req(url, api=False):
    h = {"User-Agent": "profile-readme"}
    if api:
        h["Accept"] = "application/vnd.github+json"
        if os.environ.get("GITHUB_TOKEN"):
            h["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    last = None
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def contributions(frm=None, to=None):
    url = f"https://github.com/users/{USER}/contributions" + (f"?from={frm}&to={to}" if frm else "")
    h = _req(url)
    tips = {m.group(1): m.group(2) for m in re.finditer(r'for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)</tool-tip>', h)}
    days = []
    for m in re.finditer(r'<td[^>]*data-date="([\d-]+)"[^>]*id="(contribution-day-component-[\d-]+)"[^>]*data-level="(\d)"', h):
        t = tips.get(m.group(2), "")
        n = re.match(r"(\d+) contribution", t)
        days.append((m.group(1), int(m.group(3)), int(n.group(1)) if n else 0))
    days.sort()
    if not days:
        raise RuntimeError("no contribution cells found")
    return days


def repos_api():
    u = json.loads(_req(f"https://api.github.com/users/{USER}", True))
    rp = []
    for page in (1, 2, 3):
        chunk = json.loads(_req(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=pushed&page={page}", True))
        if not isinstance(chunk, list):
            raise RuntimeError("repos not a list")
        rp += chunk
        if len(chunk) < 100:
            break
    own = [r for r in rp if not r.get("fork")]
    bytes_ = {}
    for r in own[:60]:
        try:
            for k, v in json.loads(_req(f"https://api.github.com/repos/{USER}/{r['name']}/languages", True)).items():
                bytes_[k] = bytes_.get(k, 0) + v
        except Exception:  # noqa: BLE001
            pass
    basis = "code size"
    if not bytes_:
        basis = "repo count"
        for r in own:
            if r.get("language"):
                bytes_[r["language"]] = bytes_.get(r["language"], 0) + 1
    return dict(repos=u.get("public_repos"), followers=u.get("followers"), stars=sum(r.get("stargazers_count", 0) for r in own), langs=sorted(bytes_.items(), key=lambda kv: -kv[1]),
                lang_basis=basis, all_repos=[(r["name"], r.get("pushed_at"), r.get("language")) for r in own])


def repos_scrape():
    """Fallback that reads the public pages (no API quota)."""
    prof = _req(f"https://github.com/{USER}")
    m = re.search(r'<span class="text-bold color-fg-default">([\d,]+)</span>\s*followers', prof)
    followers = int(m.group(1).replace(",", "")) if m else None
    repos, stars = [], 0
    for page in range(1, 6):
        h = _req(f"https://github.com/{USER}?tab=repositories&page={page}")
        blocks = h.split('<li class="col-12 d-flex')[1:]
        if not blocks:
            break
        for b in blocks:
            name = re.search(r'itemprop="name codeRepository"\s*>\s*([^<\s]+)', b)
            if not name:
                continue
            lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', b)
            when = re.search(r'<relative-time datetime="([^"]+)"', b)
            st = re.search(r'/stargazers"[^>]*>(?:.|\n)*?([\d,]+)\s*</a>', b)
            repos.append(dict(name=name.group(1), lang=htmllib.unescape(lang.group(1)) if lang else None, pushed=when.group(1) if when else None, fork="Forked from" in b))
            if st and not repos[-1]["fork"]:
                stars += int(st.group(1).replace(",", ""))
        if len(blocks) < 30:
            break
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        if r["lang"]:
            langs[r["lang"]] = langs.get(r["lang"], 0) + 1
    return dict(repos=len(repos), followers=followers, stars=stars, langs=sorted(langs.items(), key=lambda kv: -kv[1]), lang_basis="repo count",
                all_repos=[(r["name"], r["pushed"], r["lang"]) for r in own])


def streak_runs(dates_counts):
    """dates_counts: sorted [(date, count)] with consecutive dates. Returns (longest, longest_start_idx)."""
    best = run = 0
    bs = 0
    for i, (_, c) in enumerate(dates_counts):
        run = run + 1 if c > 0 else 0
        if run > best:
            best, bs = run, i - run + 1
    return best, bs


def analyse(days, years, today):
    """Everything the tiles show, computed from real calendar data."""
    counts = [c for _, _, c in days]
    n = len(days)
    cur, i = 0, n - 1
    if counts[i] == 0:  # today may not have a contribution yet
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur, i = cur + 1, i - 1
    longest, ls = streak_runs([(d, c) for d, _, c in days])
    wk = [0] * 7
    for d, _, c in days:
        wk[dt.date.fromisoformat(d).weekday()] += c
    bi = max(range(n), key=lambda k: counts[k])
    months, order = {}, []
    for k, (d, _, c) in enumerate(days):
        key = d[:7]
        if key not in months:
            months[key] = [0, k]
            order.append(key)
        months[key][0] += c
    mlist = [(dt.date.fromisoformat(k + "-01").strftime("%b"), months[k][0], months[k][1]) for k in order]
    last = lambda a, b: sum(counts[max(0, n - a):n - b] if b else counts[max(0, n - a):])
    # lifetime, stitched from the per-year calendars
    merged = {}
    for y, ds in years.items():
        for d, _, c in ds:
            if d <= today.isoformat():
                merged[d] = c
    seq = sorted(merged.items())
    life_longest = streak_runs(seq)[0] if seq else None
    ytd = None
    ty, ly = today.year, today.year - 1
    if ty in years and ly in years:
        cut = lambda y: sum(c for d, _, c in years[y] if d <= today.replace(year=y).isoformat())
        try:
            ytd = (cut(ty), cut(ly))
        except ValueError:
            ytd = None
    by_year = {y: sum(c for d, _, c in ds if d <= today.isoformat()) for y, ds in years.items()}
    first = next((y for y in sorted(by_year) if by_year[y] > 0), None)
    by_year = {y: v for y, v in by_year.items() if first and y >= first}
    return dict(total=sum(counts), current=cur, longest=longest, longest_start=ls, best=counts[bi], best_idx=bi, best_date=days[bi][0], active=sum(1 for c in counts if c),
                top_weekday=DAYS[wk.index(max(wk))] if sum(wk) else None, weekday=wk, months=mlist, l30=(last(30, 0), sum(counts[max(0, n - 60):n - 30])),
                l90=(last(90, 0), sum(counts[max(0, n - 180):n - 90])), ytd=ytd, by_year=by_year, life_total=sum(merged.values()) if merged else None, life_longest=life_longest,
                life_active=sum(1 for v in merged.values() if v) if merged else None)


def fetch():
    try:
        data = repos_api()
    except Exception as e:  # noqa: BLE001
        print("  api unavailable, reading public pages:", str(e)[:60])
        data = repos_scrape()
    today = dt.datetime.now(dt.timezone.utc).date()
    days = contributions()
    years = {}
    for y in range(today.year - 4, today.year + 1):
        try:
            years[y] = contributions(f"{y}-01-01", f"{y}-12-31")
        except Exception as e:  # noqa: BLE001
            print(f"  year {y} unavailable:", str(e)[:50])
    data.update(analyse(days, years, today))
    data["days"] = days
    now = dt.datetime.now(dt.timezone.utc)
    data["updated"] = now.strftime("%Y-%m-%d %H:%M UTC")
    data["today"] = days[-1][0]
    rep = []
    for nm, iso, lang in data["all_repos"]:
        rep.append((nm, iso, lang))
    data["recent"] = rep[:5]
    ages = [(now - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).days for _, iso, _ in rep if iso]
    data["active7"], data["active30"], data["active90"] = (sum(1 for a in ages if a < k) for k in (7, 30, 90))
    data["n_langs"] = len(data["langs"])
    return data


def empty_data():
    keys = "repos followers stars current longest total best active top_weekday life_total life_longest active30 n_langs best_date".split()
    d = {k: None for k in keys}
    d.update(langs=[], lang_basis="", recent=[], days=[], weekday=[0] * 7, months=[], l30=(0, 0), l90=(0, 0), ytd=None, by_year={}, updated=None, longest_start=0, best_idx=0, life_active=None, active7=None, active90=None, today=None)
    return d


def seed_data():
    try:
        return fetch()
    except Exception as e:  # noqa: BLE001
        print("  (live tiles seeded empty:", str(e)[:70] + ")")
        return empty_data()


# ═════════════════════════ small drawing helpers ═════════════════════════
def ago(iso):
    if not iso:
        return ""
    days = (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 86400
    return "pushed today" if days < 1 else "pushed yesterday" if days < 2 else f"pushed {round(days)} days ago"


def grow(final, T, t0, dur=.9, hold=10.6, back=11.3):
    """(values, keyTimes) for a looping 0 -> final -> hold -> 0 growth."""
    return [0, 0, final, final, 0, 0], [0, t0 / T, (t0 + dur) / T, hold / T, back / T, 1]


def a_grow(attr, final, T, t0, **k):
    v, kt = grow(final, T, t0, **k)
    return anim(attr, v, T, kt)


def a_bar_up(base, h, T, t0, **k):
    """y + height animation for a bar rising from `base`."""
    v, kt = grow(h, T, t0, **k)
    return anim("height", v, T, kt) + anim("y", [base - x for x in v], T, kt)


def fmt_int(v):
    return f"{round(v):,}"


def delta_pill(d, x, y, now, before, T, t0):
    """Pill with the change vs `before`. Returns the width."""
    if before == 0:
        lab, col, up = ("new" if now else "same"), (MT if now else "#e8e8e1"), now > 0
    else:
        pct = (now - before) * 100 / before
        lab = f"{'+' if pct > 0 else '−' if pct < 0 else ''}{abs(pct):.0f}%"
        col, up = (MT if pct > 0 else TG2 if pct < 0 else "#e8e8e1"), pct >= 0
    w = tw("d", lab, 17, -.5) + 50
    d.add(f'<g opacity="0">{win_anim([(t0 + .8, 10.6)], T)}<rect x="{x - w:.1f}" y="{y}" width="{w:.1f}" height="36" rx="18" fill="{col}" stroke="{INK}" stroke-width="2"/>')
    tri = f'M{x - w + 18:.1f} {y + 23}l6-10 6 10z' if up else f'M{x - w + 18:.1f} {y + 13}l6 10 6-10z'
    d.add(f'<path d="{tri}" fill="{INK}"/>')
    d.T(x - w + 36, y + 25, lab, "d", 17, INK, ls=-.5)
    d.add("</g>")
    return w


# ═════════════════════════ live.svg ═════════════════════════
LIVE_T, LIVE_SUB = "Live from GitHub", "Real numbers from my GitHub account. A GitHub Action redraws this every few hours."


def render_live(data, path=None):
    path = path or os.path.join(ASSETS, "live.svg")
    T = 10.0
    d0 = Doc(W, 10, "x")
    y = section_header(d0, LIVE_T, LIVE_SUB, P, P)
    gap, ch = 18, 124
    cw = (BW - 2 * gap) / 3
    y0 = y + 22
    nv = lambda k: data.get(k)
    best_note = dt.date.fromisoformat(data["best_date"]).strftime("%b %-d, %Y") if data.get("best_date") else ""
    cards = [
        (nv("repos"), "public repos", "#fff"), (nv("followers"), "followers", "#fff"), (nv("stars"), "stars earned", "#fff"),
        (nv("current"), "current streak, days", TG2), (nv("life_longest") or nv("longest"), "longest streak ever, days", YE), (nv("life_total") or nv("total"), "contributions since I started", LC),
        (nv("total"), "contributions, last year", "#fff"), (nv("active"), "active days, last 12 months", "#fff"), (nv("best"), "best day" + (f", {best_note}" if best_note else ""), "#fff"),
        (nv("active30"), "repos pushed in 30 days", "#fff"), (data.get("top_weekday") or None, "most active weekday", MT), (nv("n_langs"), "languages across my repos", "#fff")]
    rows = 4
    ly = y0 + rows * (ch + gap) + 14
    langs = data["langs"][:6]
    other = sum(c for _, c in data["langs"][6:])
    langs = langs + ([("Other", other)] if other else [])
    tot = sum(c for _, c in langs) or 1
    legend, x, row = [], 0, 0
    for i, (nme, c) in enumerate(langs):
        lab = f"{nme} {c * 100 / tot:.0f}%"
        w = 24 + tw("f6", lab, 18) + 20
        if x + w > BW:
            x, row = 0, row + 1
        legend.append((x, row, lab, i))
        x += w
    leg_rows = (row + 1) if langs else 1
    ry = ly + 34 + 26 + 16 + leg_rows * 32 + 34
    rec = data["recent"]
    rowh = 56
    act = ry + 38
    H = int(act + len(rec) * (rowh + 10) + (34 if data.get("updated") else 0) + P - 10)
    d = Doc(W, H, "Live from GitHub: " + f"{data['repos']} public repos, {data['followers']} followers, {data['stars']} stars, current streak {data['current']} days, {data['total']} contributions in the last 12 months. Languages: " + ", ".join(n for n, _ in langs) + ".")
    tile(d, SN)
    section_header(d, LIVE_T, LIVE_SUB, P, P)
    d.add(sparkles(d, 10, W - 330, 40, W - 40, 150, 3, CB, 2, 4.5))
    for i, (val, lab_, bg) in enumerate(cards):
        x, yy = P + (i % 3) * (cw + gap), y0 + (i // 3) * (ch + gap)
        d.add(f'<rect x="{x + 1:.1f}" y="{yy + 1}" width="{cw - 2:.1f}" height="{ch - 2}" rx="26" fill="{bg}" stroke="{INK}" stroke-width="2"/>')
        d.add(sheen(d, x + 1, yy + 1, cw - 2, ch - 2, 26, T=7, delay=.4 * i, op=.28))
        lab_t = typo(lab_)
        while tw("f4", lab_t, 19) > cw - 44:  # keep it on one line
            lab_t = lab_t.rsplit(",", 1)[0] if "," in lab_t else lab_t[:-1]
        if val is None:
            d.T(x + 24, yy + 68, "—", "d", 44, INK)
        elif isinstance(val, str):
            size = min(40, (cw - 48) / adv("d", val) * .96)
            d.T(x + 24, yy + 68, val, "d", size, INK, ls=-.05 * size)
        else:
            size = min(46, (cw - 48) / max(adv("d", str(val)), .1) * .96)
            d.add(countup(d, x + 24, yy + 68, val, fmt_int, size, INK, T, t0=.3 + (i % 3) * .15, dur=1.5, reset=9.2, ls=-.05 * size))
        d.T(x + 24, yy + 100, lab_t, "f4", 19, INK, op=.78)
    # languages
    d.T(P, ly + 22, "Most used languages", "f6", 22, INK)
    if data.get("lang_basis"):
        d.T(W - P, ly + 22, "by " + data["lang_basis"] + ", my own repos", "f4", 17, INK, "end", op=.62)
    by = ly + 34
    cp = d.uid("c")
    d.defs.append(f'<clipPath id="{cp}"><rect x="{P}" y="{by}" width="{BW}" height="26" rx="13"/></clipPath>')
    segs, xx = "", P
    for i, (nme, c) in enumerate(langs):
        w = BW * c / tot
        segs += f'<rect x="{xx:.1f}" y="{by}" width="{w + .6:.1f}" height="26" fill="{LANG_COL[i]}"/>'
        xx += w
    d.add(f'<rect x="{P}" y="{by}" width="{BW}" height="26" rx="13" fill="{INK}" fill-opacity=".12"/><g clip-path="url(#{cp})">{segs}'
          f'<rect x="{P}" y="{by}" width="{BW}" height="26" fill="{SN}">{anim("width", [BW, 0, 0, BW], T, [0, .12, .88, 1])}{anim("x", [P, P + BW, P + BW, P], T, [0, .12, .88, 1])}</rect></g>')
    for x, row, lab, i in legend:
        yy = by + 26 + 20 + row * 32 + 14
        d.add(f'<circle cx="{P + x + 8}" cy="{yy - 6}" r="8" fill="{LANG_COL[i]}" stroke="{INK}" stroke-width="1.5"/>')
        d.T(P + x + 24, yy, lab, "f6", 18, INK, op=.9)
    # recent pushes
    d.T(P, act - 12, "Recently pushed", "f6", 22, INK)
    chips = [(f"{data[k]} in 7 days" if k == "active7" else f"{data[k]} in 30 days" if k == "active30" else f"{data[k]} in 90 days") for k in ("active7", "active30", "active90") if data.get(k) is not None]
    cx_ = W - P
    for c in reversed(chips):
        w = tw("f6", c, 16) + 26
        d.add(f'<rect x="{cx_ - w:.1f}" y="{act - 34}" width="{w:.1f}" height="30" rx="15" fill="none" stroke="{INK}" stroke-width="1.5"/>')
        d.T(cx_ - w + 13, act - 13, c, "f6", 16, INK, op=.8)
        cx_ -= w + 8
    names = [n for n, _ in data["langs"]]
    for i, (name, iso, lang) in enumerate(rec):
        yy = act + i * (rowh + 10)
        d.add(f'<g><animate attributeName="opacity" values="0;1;1" keyTimes="0;{.04 + i * .02:.3f};1" dur="{T}s" repeatCount="indefinite"/>'
              f'<rect x="{P + 1}" y="{yy + 1}" width="{BW - 2}" height="{rowh - 2}" rx="20" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        d.T(P + 22, yy + 35, name, "f6", 21, INK)
        right = ago(iso)
        d.T(P + BW - 22, yy + 35, right, "f4", 19, INK, "end", op=.65)
        if lang:
            lx_ = P + BW - 22 - tw("f4", right, 19) - 26 - tw("f6", lang, 17)
            col = LANG_COL[names.index(lang)] if lang in names and names.index(lang) < 6 else "#9aa0b5"
            d.add(f'<circle cx="{lx_ - 14:.1f}" cy="{yy + 28}" r="7" fill="{col}" stroke="{INK}" stroke-width="1.5"/>')
            d.T(lx_, yy + 34, lang, "f6", 17, INK, op=.85)
        d.add("</g>")
    if data.get("updated"):
        d.T(P, H - P + 8, "Last synced " + data["updated"], "f4", 15, INK, op=.55)
    d.save(path)


# ═════════════════════════ year.svg ═════════════════════════
YEAR_T, YEAR_SUB = "My year, week by week", "Every square is one day from the last 12 months of my public GitHub calendar. Watch the scan: the counter, the running total and the monthly bars fill in as it passes."


def render_year(data, path=None):
    path = path or os.path.join(ASSETS, "year.svg")
    days = data["days"]
    T, SCAN, OUT, BACK = 14.0, 6.5, 12.4, 13.2
    d0 = Doc(W, 10, "x")
    y = section_header(d0, YEAR_T, YEAR_SUB, P, P, fg="#fff", w=900)
    cell, g = 13, 3
    step = cell + g
    gx0 = P + 40
    cols = 53
    gw = cols * step - g
    yc = y + 22
    gy0 = yc + 148
    chart_y = gy0 + 7 * step + 108
    chart_h = 190
    bars_y = chart_y + chart_h + 70
    bar_h = 150
    H = int(bars_y + bar_h + 64 + P - 20)
    d = Doc(W, H, f"My year week by week: {data['total']} public contributions in the last 12 months across {data['active']} active days; current streak {data['current']} days; best day {data['best']} contributions.")
    tile(d, INK, stroke="#ffffff22")
    section_header(d, YEAR_T, YEAR_SUB, P, P, fg="#fff", w=900)
    if not days:
        d.T(P, yc + 60, "Waiting for the first sync.", "f4", 22, "#fff", op=.7)
        d.save(path)
        return
    off = (dt.date.fromisoformat(days[0][0]).weekday() + 1) % 7  # weeks start on Sunday
    colof = lambda k: (k + off) // 7
    rowof = lambda k: (k + off) % 7
    tcol = lambda c: c / cols * SCAN
    # running total per week
    cum, acc = [], 0
    wk_cum = {}
    for k, (_, _, cnt) in enumerate(days):
        acc += cnt
        wk_cum[colof(k)] = acc
    for c in range(cols):
        cum.append(wk_cum.get(c, acc))
    total = max(acc, 1)
    # big counter + month label that follow the scan
    d.T(P, yc + 40, "contributions so far", "f6", 19, "#fff", op=.65)
    for c in range(cols):
        wins = [(tcol(c), tcol(c + 1) if c < cols - 1 else BACK)]
        if c == 0:
            wins = [(0, tcol(1)), (BACK, T)]
        d.add(f'<g opacity="{1 if c == 0 else 0}">{win_anim(wins, T)}' + d.text(P, yc + 104, f"{cum[c]:,}", "d", 64, MT, ls=-3) + "</g>")
    mlab = {}
    for k, (ds, _, _) in enumerate(days):
        dd = dt.date.fromisoformat(ds)
        mlab.setdefault(colof(k), dd.strftime("%b %Y"))
    runs, prev = [], None
    for c in range(cols):
        lab = mlab.get(c, prev)
        if lab != prev:
            runs.append([lab, c, c])
            prev = lab
        else:
            runs[-1][2] = c
    for lab, a, b in runs:
        wins = [(tcol(a), tcol(b + 1) if b < cols - 1 else BACK)]
        if a == 0:
            wins = [(0, tcol(b + 1)), (BACK, T)]
        d.add(f'<g opacity="{1 if a == 0 else 0}">{win_anim(wins, T)}' + d.text(W - P, yc + 104, lab, "d", 30, "#fff", "end", ls=-1) + "</g>")
    # month labels and weekday labels
    seen = None
    for k, (ds, _, _) in enumerate(days):
        dd = dt.date.fromisoformat(ds)
        if rowof(k) == 0 and dd.day <= 7 and dd.month != seen:
            d.T(gx0 + colof(k) * step, gy0 - 12, dd.strftime("%b"), "f4", 15, "#fff", op=.6)
            seen = dd.month
    for r_, nm in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        d.T(P, gy0 + r_ * step + 11, nm, "f4", 14, "#fff", op=.55)
    # heatmap columns appear as the scan passes
    colsvg = {}
    for k, (ds, lvl, cnt) in enumerate(days):
        colsvg.setdefault(colof(k), []).append(f'<rect x="{gx0 + colof(k) * step}" y="{gy0 + rowof(k) * step}" width="{cell}" height="{cell}" rx="3.5" fill="{HEAT_DARK[lvl]}"/>')
    for c in range(cols):
        t = tcol(c)
        d.add(f'<g opacity="0">{anim("opacity", [0, 0, 1, 1, 0, 0], T, [0, t / T, (t + .3) / T, OUT / T, BACK / T, 1])}{"".join(colsvg.get(c, []))}</g>')
    # longest streak outline + best day ring, after the scan
    ls_, ll = data["longest_start"], data["longest"]
    outl = "".join(f'<rect x="{gx0 + colof(k) * step - 1.5}" y="{gy0 + rowof(k) * step - 1.5}" width="{cell + 3}" height="{cell + 3}" rx="5" fill="none" stroke="{TG}" stroke-width="2.4"/>' for k in range(ls_, ls_ + ll))
    d.add(f'<g opacity="0">{win_anim([(SCAN + .2, OUT)], T)}{outl}</g>')
    bk = data["best_idx"]
    bx, by_ = gx0 + colof(bk) * step + cell / 2, gy0 + rowof(bk) * step + cell / 2
    d.add(f'<g opacity="0">{win_anim([(SCAN + .2, OUT)], T)}<circle cx="{bx}" cy="{by_}" r="12" fill="none" stroke="{YE}" stroke-width="3">{anim("r", [10, 17, 10], 1.6)}{anim("stroke-opacity", [1, .2, 1], 1.6)}</circle></g>')
    # scanner
    sx = anim("x", [gx0 - 2, gx0 + gw, gx0 + gw], T, [0, SCAN / T, 1])
    so = anim("opacity", [1, 1, 0, 0], T, [0, SCAN / T, (SCAN + .4) / T, 1])
    d.add(f'<rect x="{gx0 - 2}" y="{gy0 - 6}" width="3" height="{7 * step + 6}" rx="1.5" fill="{MT}">{sx}{so}</rect>'
          f'<rect x="{gx0 - 12}" y="{gy0 - 6}" width="22" height="{7 * step + 6}" fill="{MT}" fill-opacity=".14">{anim("x", [gx0 - 12, gx0 + gw - 10, gx0 + gw - 10], T, [0, SCAN / T, 1])}{so}</rect>')
    # legend row
    ly = gy0 + 7 * step + 34
    d.T(P, ly, "Less", "f4", 15, "#fff", op=.6)
    for lv in range(5):
        d.add(f'<rect x="{P + 44 + lv * step}" y="{ly - 12}" width="{cell}" height="{cell}" rx="3.5" fill="{HEAT_DARK[lv]}"/>')
    d.T(P + 44 + 5 * step + 4, ly, "More", "f4", 15, "#fff", op=.6)
    lx = P + 230
    d.add(f'<rect x="{lx}" y="{ly - 13}" width="{cell + 3}" height="{cell + 3}" rx="5" fill="none" stroke="{TG}" stroke-width="2.4"/>')
    sd = dt.date.fromisoformat(days[ls_][0]).strftime("%b %-d")
    ed = dt.date.fromisoformat(days[ls_ + ll - 1][0]).strftime("%b %-d")
    d.T(lx + 26, ly, f"longest streak this year: {ll} days ({sd} to {ed})", "f4", 15.5, "#fff", op=.75)
    rx_ = P + 230 + 26 + tw("f4", f"longest streak this year: {ll} days ({sd} to {ed})", 15.5) + 30
    d.add(f'<circle cx="{rx_ + 8}" cy="{ly - 5}" r="8" fill="none" stroke="{YE}" stroke-width="3"/>')
    d.T(rx_ + 26, ly, f"best day: {data['best']}", "f4", 15.5, "#fff", op=.75)
    # running total chart
    base = chart_y + chart_h - 34
    top = chart_y + 30
    d.T(P, chart_y - 4, "Running total", "f6", 22, "#fff")
    d.T(W - P, chart_y - 4, "cumulative contributions", "f4", 17, "#fff", "end", op=.6)
    for frac in (0, .5, 1):
        yy = base - (base - top) * frac
        d.add(f'<line x1="{gx0}" y1="{yy:.1f}" x2="{gx0 + gw}" y2="{yy:.1f}" stroke="#fff" stroke-opacity=".14" stroke-dasharray="3 6"/>')
        d.T(P, yy + 5, str(round(total * frac)), "f4", 14, "#fff", op=.55)
    pts = [(gx0 + c * step + cell / 2, base - (base - top) * cum[c] / total) for c in range(cols)]
    line = "M" + "L".join(f"{x:.1f} {y_:.1f}" for x, y_ in pts)
    area = line + f"L{pts[-1][0]:.1f} {base}L{pts[0][0]:.1f} {base}Z"
    gid, cid = d.uid("ag"), d.uid("cc")
    d.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MT}" stop-opacity=".45"/><stop offset="1" stop-color="{MT}" stop-opacity="0"/></linearGradient>')
    d.defs.append(f'<clipPath id="{cid}"><rect x="{gx0 - 4}" y="{top - 20}" width="0" height="{chart_h}">{anim("width", [0, gw + 8, gw + 8, 0, 0], T, [0, SCAN / T, OUT / T, BACK / T, 1])}</rect></clipPath>')
    d.add(f'<g clip-path="url(#{cid})"><path d="{area}" fill="url(#{gid})"/><path d="{line}" fill="none" stroke="{MT}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></g>')
    d.add(f'<circle r="8" fill="{YE}" stroke="{INK}" stroke-width="3"><animateMotion dur="{T}s" repeatCount="indefinite" path="{line}" keyPoints="0;1;1" keyTimes="0;{SCAN / T:.4f};1" calcMode="linear"/>{anim("opacity", [1, 1, 0, 0], T, [0, OUT / T, BACK / T, 1])}</circle>')
    d.add(f'<g opacity="0">{win_anim([(SCAN, OUT)], T)}' + d.text(pts[-1][0] - 22, pts[-1][1] + 9, f"{total:,}", "d", 26, YE, "end", ls=-1) + "</g>")
    # months
    d.T(P, bars_y - 28, "Contributions per month", "f6", 22, "#fff")
    months = data["months"]
    mx = max((v for _, v, _ in months), default=1) or 1
    best_m = max(range(len(months)), key=lambda i: months[i][1])
    colw = gw / len(months)
    bb = bars_y + bar_h
    d.add(f'<line x1="{gx0}" y1="{bb}" x2="{gx0 + gw}" y2="{bb}" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>')
    for i, (lab, v, k0) in enumerate(months):
        h = max(4, bar_h * v / mx) if v else 3
        bx_ = gx0 + i * colw + (colw - 38) / 2
        t0 = tcol(colof(k0))
        col = TG if i == best_m else LC
        d.add(f'<rect x="{bx_:.1f}" y="{bb}" width="38" height="0" rx="8" fill="{col}">{a_bar_up(bb, h, T, t0, dur=.7, hold=OUT, back=BACK)}</rect>')
        d.add(f'<g opacity="0">{win_anim([(t0 + .5, OUT)], T)}' + d.text(bx_ + 19, bb - h - 10, str(v), "f6", 17, "#fff", "middle") + "</g>")
        if i in (0, len(months) - 1):
            yy2 = dt.date.fromisoformat(days[k0][0]).strftime("%y")
            lab = f"{lab} \u2019{yy2}"
        d.T(bx_ + 19, bb + 26, lab, "f4", 16, "#fff", "middle", op=.7)
    d.T(W - P, bars_y - 28, f"best month: {months[best_m][0]} ({months[best_m][1]})", "f4", 17, "#fff", "end", op=.65)
    d.add(sparkles(d, 14, W - 360, 30, W - 30, 170, 8, MT, 1.6, 3.4))
    d.save(path)


# ═════════════════════════ compare.svg ═════════════════════════
CMP_T, CMP_SUB = "How I compare with myself", "Same real calendar, sliced four ways: recent vs earlier, this year vs last year, weekdays vs weekends, and year by year. It counts what my public profile shows."
GOALS = [("Day streak", "current", [3, 7, 14, 30, 60, 100], "days"), ("Contributions, 12 months", "total", [100, 250, 500, 1000], ""), ("Public repos", "repos", [10, 25, 50, 100], ""),
         ("Stars earned", "stars", [1, 5, 10, 25, 50], ""), ("Followers", "followers", [5, 10, 25, 50, 100], ""), ("Languages used", "n_langs", [5, 10, 15, 20], "")]


def pair_card(d, x, y, w, h, title, a, b, T, t0):
    """Two animated horizontal bars (now vs before) with a delta pill."""
    d.add(f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    d.T(x + 24, y + 40, title, "f6", 20, INK)
    mx = max(a[1], b[1], 1)
    bw = w - 48
    for j, (lab, v, col) in enumerate([(a[0], a[1], INK), (b[0], b[1], CB2)]):
        yy = y + 62 + j * 58
        d.T(x + 24, yy + 15, lab, "f6", 17, INK, op=.75)
        d.add(f'<rect x="{x + 24}" y="{yy + 24}" width="{bw}" height="20" rx="10" fill="{INK}" fill-opacity=".08"/>')
        d.add(f'<rect x="{x + 24}" y="{yy + 24}" width="0" height="20" rx="10" fill="{col}" stroke="{INK}" stroke-width="1.5">{a_grow("width", max(bw * v / mx, 14), T, t0 + j * .2)}</rect>')
        d.add(f'<g opacity="0">{win_anim([(t0 + .9 + j * .2, 10.6)], T)}' + d.text(x + w - 24, yy + 15, f"{v:,}", "d", 19, INK, "end", ls=-.6) + "</g>")


def render_compare(data, path=None):
    path = path or os.path.join(ASSETS, "compare.svg")
    T = 12.0
    d0 = Doc(W, 10, "x")
    y = section_header(d0, CMP_T, CMP_SUB, P, P)
    gap = 18
    cw = (BW - gap) / 2
    y0 = y + 22
    ch = 196
    wk_y = y0 + 2 * (ch + gap)
    wk_h = 300
    yr_y = wk_y + wk_h + gap
    yr_h = 320
    ms_y = yr_y + yr_h + gap
    ms_h = 78 + len(GOALS) * 62
    H = int(ms_y + ms_h + P)
    d = Doc(W, H, "Comparisons from my real GitHub calendar: last 30 and 90 days vs the periods before, this year vs last year, weekdays vs weekends, contributions per weekday, year by year, and milestone progress.")
    tile(d, PK)
    section_header(d, CMP_T, CMP_SUB, P, P)
    d.add(sparkles(d, 10, W - 330, 40, W - 40, 150, 5, INK, 1.6, 3.4))
    if not data["days"]:
        d.T(P, y0 + 40, "Waiting for the first sync.", "f4", 22, INK, op=.7)
        d.save(path)
        return
    l30, l90, ytd = data["l30"], data["l90"], data["ytd"]
    cards = [("Last 30 days", ("Last 30 days", l30[0]), ("The 30 before", l30[1]), l30),
             ("Last 90 days", ("Last 90 days", l90[0]), ("The 90 before", l90[1]), l90)]
    ty = dt.date.fromisoformat(data["today"]).year if data.get("today") else dt.date.today().year
    if ytd:
        cards.append((f"This year so far", (f"{ty} so far", ytd[0]), (f"{ty - 1}, same dates", ytd[1]), ytd))
    for i, (title, a, b, pair) in enumerate(cards):
        x, yy = P + (i % 2) * (cw + gap), y0 + (i // 2) * (ch + gap)
        pair_card(d, x, yy, cw, ch, title, a, b, T, .4 + i * .25)
        delta_pill(d, x + cw - 20, yy + 18, pair[0], pair[1], T, .4 + i * .25)
    # weekdays vs weekends
    wk = data["weekday"]
    tot = sum(wk) or 1
    wd, we = sum(wk[:5]), sum(wk[5:])
    i = 3
    x, yy = P + (i % 2) * (cw + gap), y0 + (i // 2) * (ch + gap)
    d.add(f'<rect x="{x + 1}" y="{yy + 1}" width="{cw - 2}" height="{ch - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    d.T(x + 24, yy + 40, "Weekdays vs weekends", "f6", 20, INK)
    bw_ = cw - 48
    wdw = bw_ * wd / tot
    cp = d.uid("c")
    d.defs.append(f'<clipPath id="{cp}"><rect x="{x + 24}" y="{yy + 66}" width="{bw_}" height="34" rx="17"/></clipPath>')
    d.add(f'<g clip-path="url(#{cp})"><rect x="{x + 24}" y="{yy + 66}" width="{bw_}" height="34" fill="{TG}"/><rect x="{x + 24}" y="{yy + 66}" width="{wdw:.1f}" height="34" fill="{CB}">{anim("width", [0, 0, wdw, wdw, 0, 0], T, [0, .5 / T, 1.7 / T, 10.6 / T, 11.3 / T, 1])}</rect></g>')
    d.add(f'<rect x="{x + 24}" y="{yy + 66}" width="{bw_}" height="34" rx="17" fill="none" stroke="{INK}" stroke-width="2"/>')
    d.add(f'<circle cx="{x + 32}" cy="{yy + 128}" r="8" fill="{CB}" stroke="{INK}" stroke-width="1.5"/>')
    d.T(x + 48, yy + 134, f"Mon to Fri: {wd * 100 / tot:.0f}% ({wd})", "f6", 18, INK)
    d.add(f'<circle cx="{x + 32}" cy="{yy + 160}" r="8" fill="{TG}" stroke="{INK}" stroke-width="1.5"/>')
    d.T(x + 48, yy + 166, f"Sat and Sun: {we * 100 / tot:.0f}% ({we})", "f6", 18, INK)
    # weekday rhythm
    d.add(f'<rect x="{P + 1}" y="{wk_y + 1}" width="{BW - 2}" height="{wk_h - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    d.T(P + 24, wk_y + 42, "My week, day by day", "f6", 22, INK)
    d.T(P + BW - 24, wk_y + 42, "total contributions by weekday, last 12 months", "f4", 17, INK, "end", op=.6)
    mxw = max(wk) or 1
    bb = wk_y + wk_h - 58
    colw = (BW - 48) / 7
    top_i = wk.index(max(wk))
    for i in range(7):
        hh = max(4, 150 * wk[i] / mxw)
        bx_ = P + 24 + i * colw + (colw - 56) / 2
        col = TG if i == top_i else CB
        d.add(f'<rect x="{bx_:.1f}" y="{bb}" width="56" height="0" rx="12" fill="{col}" stroke="{INK}" stroke-width="2">{a_bar_up(bb, hh, T, .6 + i * .12)}</rect>')
        d.add(f'<g opacity="0">{win_anim([(1.4 + i * .12, 10.6)], T)}' + d.text(bx_ + 28, bb - hh - 12, str(wk[i]), "d", 19, INK, "middle", ls=-.6) + "</g>")
        d.T(bx_ + 28, bb + 30, DAY3[i], "f6", 18, INK, "middle")
    # year by year
    d.add(f'<rect x="{P + 1}" y="{yr_y + 1}" width="{BW - 2}" height="{yr_h - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    d.T(P + 24, yr_y + 42, "Year by year", "f6", 22, INK)
    by = data["by_year"]
    yrs = sorted(by)
    mxy = max(by.values(), default=1) or 1
    pw = 580
    bb = yr_y + yr_h - 58
    cwid = pw / max(len(yrs), 1)
    for i, yv in enumerate(yrs):
        hh = max(4, 190 * by[yv] / mxy)
        bx_ = P + 24 + i * cwid + (cwid - 70) / 2
        col = TG if by[yv] == mxy else MT if yv == yrs[-1] else LC
        d.add(f'<rect x="{bx_:.1f}" y="{bb}" width="70" height="0" rx="14" fill="{col}" stroke="{INK}" stroke-width="2">{a_bar_up(bb, hh, T, .6 + i * .2, dur=1.1)}</rect>')
        d.add(f'<g opacity="0">{win_anim([(1.5 + i * .2, 10.6)], T)}' + d.text(bx_ + 35, bb - hh - 12, f"{by[yv]:,}", "d", 20, INK, "middle", ls=-.6) + "</g>")
        d.T(bx_ + 35, bb + 30, str(yv) + ("*" if yv == yrs[-1] else ""), "f6", 18, INK, "middle")
    d.T(P + 24, yr_y + yr_h - 14, "* this year so far", "f4", 15, INK, op=.55)
    sx = P + 24 + pw + 40
    sw = P + BW - 24 - sx
    stats = [("since I started", data.get("life_total")), ("longest streak ever", data.get("life_longest")), ("active days, ever", data.get("life_active"))]
    for j, (lab, val) in enumerate(stats):
        sy = yr_y + 66 + j * 80
        d.add(f'<rect x="{sx}" y="{sy}" width="{sw}" height="68" rx="18" fill="{[YE, MT, LC][j]}" stroke="{INK}" stroke-width="2"/>')
        d.T(sx + 18, sy + 32, "—" if val is None else f"{val:,}", "d", 26, INK, ls=-1)
        d.T(sx + 18, sy + 56, lab, "f4", 16.5, INK, op=.78)
    # milestones
    d.add(f'<rect x="{P + 1}" y="{ms_y + 1}" width="{BW - 2}" height="{ms_h - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    d.T(P + 24, ms_y + 42, "Milestones", "f6", 22, INK)
    d.T(P + BW - 24, ms_y + 42, "automatic ladder, next goal for each number", "f4", 17, INK, "end", op=.6)
    for j, (lab, key, goals, unit) in enumerate(GOALS):
        val = data.get(key) or 0
        nxt = next((g for g in goals if g > val), None)
        got = sum(1 for g in goals if g <= val)
        yy = ms_y + 66 + j * 62
        d.T(P + 24, yy + 22, lab, "f6", 19, INK)
        d.T(P + 24, yy + 44, f"{got} of {len(goals)} levels unlocked", "f4", 15.5, INK, op=.6)
        bx_, bw2 = P + 300, 360
        frac = 1 if nxt is None else val / nxt
        d.add(f'<rect x="{bx_}" y="{yy + 12}" width="{bw2}" height="22" rx="11" fill="{INK}" fill-opacity=".1"/>')
        d.add(f'<rect x="{bx_}" y="{yy + 12}" width="0" height="22" rx="11" fill="{MT if nxt is None else TG}" stroke="{INK}" stroke-width="1.5">{a_grow("width", max(bw2 * frac, 22), T, .5 + j * .15)}</rect>')
        d.T(P + BW - 24, yy + 34, "all levels done" if nxt is None else f"{val} / {nxt} {unit}".strip(), "d", 19, INK, "end", ls=-.6)
    d.save(path)


def render_all(data):
    render_live(data)
    render_year(data)
    render_compare(data)


if __name__ == "__main__":
    render_all(fetch())
