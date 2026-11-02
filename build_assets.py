#!/usr/bin/env python3
"""Malik Zain: GitHub profile README generator.

    pip install fonttools brotli
    python3 build_assets.py     ->  assets/*.svg  and  README.md

Everything you will ever edit lives in the DATA block below. Edit, run, push.
The design is the portfolio page (blue / orange / mint, Unbounded + Hanken Grotesk), redrawn as SVG tiles,
because a GitHub README can't run CSS or JavaScript. The "Live from GitHub" tile is redrawn by a GitHub Action.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".github", "scripts"))
from ui import *  # noqa: E402,F401,F403
import live  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))  # ui.py also defines HERE, so set ours after the star-import
ME = "malik-zain-555"
GH = "https://github.com/Malik-Zain-555"
OUT = os.path.join(HERE, "assets")
S = lambda d, name: d.save(os.path.join(OUT, name))

# ═════════════════════════════ DATA (edit here) ═════════════════════════════
HERO_H1 = "I learn by building, not by theory."
HERO_P = "Malik Zain. BS CS student at Riphah and AI/ML intern at FlyRank, in Islamabad. I build small machine-learning projects, then measure where they break."
HERO_CHIPS = ["Now: NLP", "Building: Sahi Daam", "Later, inshallah: deep learning, RAG"]
RESULTS = [("74.4%", "Resume classifier with embeddings, up from 71.8% with TF-IDF"), ("~98%", "Fake-news classifier. The investigation says why that overstates it"),
           ("0.86", "Churn ROC-AUC, with 83% recall on churners"), ("6", "Repos pinned, each with its caveat written down")]
PROJECTS = [  # art: bars | ring | roc | scatter | cap | nodes     c: card colour
    dict(name="Sahi Daam Fair-Price Detector", repo="sahi-daam-fair-price-detector", m="New", u="in progress", art="scatter", c=TG2,
         blurb="Estimates fair prices for Pakistani property listings and flags ones priced far above similar listings.", tags=["Python", "scikit-learn", "XGBoost", "Streamlit"],
         notes=[("Data", "Scraped from zameen.com with requests + BeautifulSoup, starting with DHA Islamabad rentals."), ("Status", "No headline metric yet. I will publish one when I can defend it.")]),
    dict(name="Resume Category Classifier", repo="resume-category-classifier", m="74.4%", u="test accuracy", art="bars", c=CB2,
         blurb="Sorts resumes into 24 job categories and answers UNSURE when confidence is low.", tags=["scikit-learn", "embeddings", "FastAPI", "Docker"],
         notes=[("Result", "74.4% with sentence embeddings, up from 71.8% with TF-IDF."), ("Caveat", "Reading the model weights showed which words it leans on, so I trust it where it says UNSURE, not blindly.")]),
    dict(name="Fake News Style Detector", repo="fake_news_style_detector", m="~98%", u="accuracy", art="ring", c=PK,
         blurb="TF-IDF + Logistic Regression for fake vs real news, plus an investigation of what it learned.", tags=["scikit-learn", "TF-IDF"],
         notes=[("Result", "About 98% accuracy."), ("Caveat", "It learns the source's writing style, not truth. A \"Reuters\" shortcut sits in the top weights, so 98% overstates what it knows.")]),
    dict(name="Churn Prediction Pipeline", repo="churn-prediction-pipeline", m="0.86", u="ROC-AUC", art="roc", c=MT,
         blurb="Predicts which customers will churn, from raw data to a live app.", tags=["Pipeline", "LogReg", "Streamlit"],
         notes=[("Result", "0.86 ROC-AUC with 83% recall on churners."), ("Built with", "ColumnTransformer + Pipeline, deployed as an interactive Streamlit app.")]),
    dict(name="MUDABBIR-FYP", repo="MUDABBIR-FYP", m="FYP", u="university", art="cap", c=YE,
         blurb="The repository for my university final year project.", tags=["BS CS", "Riphah"],
         notes=[("Status", "Work in progress. I will add a description here when it is ready to show.")]),
    dict(name="Zylo", repo="Zylo", m="Web", u="full-stack", art="nodes", c=LC,
         blurb="A social platform: auth, posts, likes, comments, follows, notifications, media uploads.", tags=["Node.js", "Express", "EJS", "MySQL"],
         notes=[("How it was made", "Tutorial-guided. This is where I learned full-stack basics.")]),
]
SAHI = [  # label, fair (crore), asking as % of fair
    ("10 marla, Islamabad", 2.7, 119), ("5 marla, Rawalpindi", 1.5, 100), ("1 kanal, Lahore", 6.9, 88)]
CONCEPTS = [("Inventory OS", "Offline-first POS and inventory concept for small shops.", "NestJS · Electron · Expo React Native · Railway + Neon PostgreSQL"),
            ("NOVA DOCK", "A Windows dock in the style of the iPhone Dynamic Island. v2.0 rebuild planned.", "Python · PySide6"),
            ("Bill splitter + budget tracker", "Two ideas on my list: who-owes-whom settlements, and a monthly budget tracker.", "not started")]
ROUTE = [  # title, state d/n/l, when, solid, shaky, checkpoint
    ("HTML, CSS, JS", "d", "Aug 2023", "Solid on HTML, CSS and Tailwind basics. I love JavaScript.", "Advanced JavaScript is rusty.", "Revisit it when a build needs it."),
    ("React", "d", "2024 to mid 2025", "I can build React sites, with a lot of frontend and animation work.", "The concepts underneath are not deep yet.", "Go deeper, until my ML apps need a real front end."),
    ("Python", "d", "Feb 2026", "Python, NumPy, Matplotlib. pandas is partial.", "Heavy data wrangling.", "Own CLI tools and scripts."),
    ("Machine learning", "d", "Jun 2026", "scikit-learn, Pipelines, Logistic Regression, tree models. Interning at FlyRank.", "Training big models from scratch.", "Six repos with honest numbers."),
    ("NLP", "n", "Now", "TF-IDF vs embeddings, evaluation beyond accuracy, reading model weights.", "Training transformers: no GPU, so Colab if ever.", "A grammar and punctuation error explainer."),
    ("Deep learning", "l", "Later, inshallah", "ANN basics, CNNs for images, RNNs for sequences.", "Custom GPU code.", "A small CNN and RNN explained in my own words."),
    ("RAG apps", "l", "Later, inshallah", "Embeddings, chunking, vector search, evaluating answers.", "Training LLMs.", "A small RAG app over documents I choose, with a written evaluation."),
]
SKILLS = [("Python", 2), ("scikit-learn + Pipelines", 2), ("NumPy, Matplotlib", 2), ("Streamlit", 2), ("pandas", 1), ("NLP: TF-IDF, embeddings", 1),
          ("FastAPI + Docker (one repo)", 1), ("HTML, CSS", 3), ("JavaScript, React, Tailwind", 2), ("Git + GitHub", 2)]
LINKS = [("GitHub", "https://github.com/Malik-Zain-555"), ("LinkedIn", "https://www.linkedin.com/in/malikzain555/"), ("itch.io", "https://zikakito.itch.io/")]
SECTION_TXT = dict(
    builds=("What I built, and what the numbers hide", "The six repos pinned on my GitHub. Under every card is the caveat: the part the metric doesn't say. Click a card to open the repo."),
    sahi=("Sahi Daam: is it overpriced?", "The model estimates a fair price; the gap to the asking price is the product. Watch the price move and the whole tile react. Example numbers, not real listings and not my model's output."),
    lab=("Concept lab", "Ideas I design. Div Space is still only an idea: watch what the floor does."),
    route=("Where I've been, where I'm going", "Since June my focus is only AI/ML. Stopping halfway was my pattern, so every stop has a checkpoint before the next one."),
    skills=("Skills, honestly", "Only things I can do myself. Tools I met in courses or built with AI help are not listed on purpose."),
    live=("Live from GitHub", "Pulled from the GitHub API and redrawn by a GitHub Action every few hours."),
)
LEVEL_COL = {1: TG, 2: YE, 3: MT}


# ═════════════════════════════ SHARED PIECES ═════════════════════════════
def header(d, key, x, y, fg=INK, w=800, tsize=60, sub_w=760):
    title, sub = SECTION_TXT[key]
    return section_header(d, title, sub, x, y, fg, w, tsize, sub_w)


def blobs(d, W, H, rx=44, dur=1.0):
    """Animated blue / orange / lilac field, a soft stand-in for the portfolio's shader."""
    cp, fl = d.uid("c"), d.uid("f")
    d.defs.append(f'<clipPath id="{cp}"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>')
    d.defs.append(f'<filter id="{fl}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="62"/></filter>')

    def el(cx, cy, rx_, ry, col, op, path_x, path_y, t):
        return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx_}" ry="{ry}" fill="{col}" fill-opacity="{op}">'
                f'{anim("cx", path_x, t * dur)}{anim("cy", path_y, t * dur)}</ellipse>')
    g = (el(790, 150, 330, 210, TG, 1, [790, 640, 860, 790], [150, 260, 110, 150], 17)
         + el(330, H - 90, 300, 170, "#1620c4", 1, [330, 470, 250, 330], [H - 90, H - 170, H - 60, H - 90], 21)
         + el(640, H * .55, 250, 140, "#fbe9ff", .92, [640, 520, 720, 640], [H * .55, H * .42, H * .62, H * .55], 14)
         + el(930, H - 70, 220, 150, TG, .9, [930, 820, 960, 930], [H - 70, H - 130, H - 40, H - 70], 19)
         + el(70, 90, 230, 160, CB2, .55, [70, 150, 40, 70], [90, 60, 130, 90], 23))
    d.add(f'<g clip-path="url(#{cp})"><rect width="{W}" height="{H}" fill="{CB}"/><g filter="url(#{fl})">{g}</g></g>')


def pill_img(name, label, bg=INK, fg=WHITE, stroke="#ffffff38", font="f6", size=17, h=46, pad=22, arrow_=False, shadow=None):
    pw = tw(font, label, size) + 2 * pad + (30 if arrow_ else 0)
    W = int(math.ceil(pw)) + (6 if shadow else 0)
    H = h + (6 if shadow else 0)
    d = Doc(W, H, label)
    if shadow:
        d.add(f'<rect x="5" y="6" width="{pw:.1f}" height="{h}" rx="{h / 2}" fill="{shadow}"/>')
    d.add(f'<rect x="1.5" y="1.5" width="{pw - 3:.1f}" height="{h - 3}" rx="{(h - 3) / 2}" fill="{bg}" stroke="{stroke}" stroke-width="3" />')
    d.T(pad + 1, h / 2 + size * .35, label, font, size, fg, ls=(-0.5 if font == "d" else None))
    if arrow_:
        d.add(arrow(pad + tw(font, label, size) + 12, h / 2, fg, 7.5, 2.4))
    S(d, name)
    return W, H


# ═════════════════════════════ HERO ═════════════════════════════
def hero():
    W, size = 1000, 86
    ls = -0.04 * size
    h1 = wrap("d", HERO_H1, size, 880, ls)
    pl = wrap("f4", HERO_P, 26, 600)
    top = 96
    H = int(top + len(h1) * 90 + 30 + len(pl) * 37 + 26 + 40 + 62)
    d = Doc(W, H, f"{HERO_H1} Malik Zain, BS CS student at Riphah and AI/ML intern at FlyRank in Islamabad.")
    blobs(d, W, H)
    y = top + size * .9
    g = ""
    for i, l in enumerate(h1):
        g += (f'<g opacity="0">{anim("opacity", [0, 1], .6, begin=f"{.15 + i * .14}s", repeat=None, freeze=True)}'
              f'<g>{anim_t("translate", ["0 46", "0 0"], .9, begin=f"{.15 + i * .14}s", repeat=None, freeze=True, spline="0.2 0.9 0.2 1")}'
              + d.text(56, y + i * 90, l, "d", size, WHITE, ls=ls) + "</g></g>")
    d.add(f'<g style="mix-blend-mode:difference">{g}</g>')
    y = top + len(h1) * 90 + 30
    d.lines(56, y + 20, pl, "f4", 26, WHITE, 37, op=.96)
    y += len(pl) * 37 + 26
    x = 56
    for i, c in enumerate(HERO_CHIPS):
        w = tw("f6", c, 17) + 34
        d.add(f'<g>{anim_t("translate", ["0 0", "0 -5", "0 0"], 4 + i * .6, begin=f"{i * .7}s")}<rect x="{x}" y="{y}" width="{w:.1f}" height="38" rx="19" fill="#fff"/>'
              + d.text(x + 17, y + 25, c, "f6", 17, INK) + "</g>")
        x += w + 10
    S(d, "hero.svg")


# ═════════════════════════════ NUMBERS ═════════════════════════════
def numbers():
    W, H = 1000, 232
    d = Doc(W, H, "Results: " + "; ".join(f"{a}: {b}" for a, b in RESULTS))
    tile(d, INK, stroke="#ffffff22")
    colw = 222
    size = min(60, min(196 / adv("d", a) / 1.0 for a, _ in RESULTS) * 0.98)
    for i, (a, b) in enumerate(RESULTS):
        x = 56 + i * colw
        d.T(x, 108, a, "d", size, YE, ls=-0.05 * size)
        d.lines(x, 142, wrap("f4", typo(b), 17, 192), "f4", 17, WHITE, 24, op=.78)
    S(d, "numbers.svg")


# ═════════════════════════════ BUILDS ═════════════════════════════
def art(d, kind, x, y, w, h):
    """Mini chart for a project card. Drawn on a 360x170 grid, centred in the box."""
    ax = f'<path d="M30 150H330M30 20V150" stroke="{INK}" stroke-width="3" fill="none"/>'
    if kind == "bars":
        s = (ax + f'<rect x="90" y="70" width="80" height="80" fill="{INK}" fill-opacity=".33"/>'
             f'<rect x="200" y="50" width="80" height="100" fill="{INK}"><animate attributeName="height" values="0;0;100;100" keyTimes="0;.1;.4;1" dur="5s" repeatCount="indefinite"/><animate attributeName="y" values="150;150;50;50" keyTimes="0;.1;.4;1" dur="5s" repeatCount="indefinite"/></rect>'
             + d.text(130, 62, "71.8", "f6", 16, INK, "middle") + d.text(240, 42, "74.4", "f6", 16, INK, "middle"))
    elif kind == "ring":
        s = (f'<circle cx="110" cy="85" r="52" fill="none" stroke="{INK}" stroke-opacity=".2" stroke-width="18"/>'
             f'<circle cx="110" cy="85" r="52" fill="none" stroke="{INK}" stroke-width="18" stroke-dasharray="320 327" transform="rotate(-90 110 85)">'
             f'<animate attributeName="stroke-dasharray" values="0 327;320 327;320 327" keyTimes="0;.35;1" dur="6s" repeatCount="indefinite"/></circle>'
             + d.text(110, 92, "~98%", "d", 20, INK, "middle", ls=-.8) + d.text(190, 70, "truth?", "f4", 20, INK)
             + f'<path d="M188 76H254" stroke="#e5383b" stroke-width="5"/>' + d.text(190, 116, "source's style", "f6", 17, "#c1121f"))
    elif kind == "roc":
        p = 1 / .86 - 1
        pts = "M30 150" + "".join(f"L{30 + 300 * i / 40:.1f} {150 - 130 * (i / 40) ** p:.1f}" for i in range(1, 41))
        s = (ax + f'<path d="M30 150L330 20" stroke="{INK}" stroke-opacity=".4" stroke-dasharray="5 6" fill="none"/>'
             f'<path d="{pts}" fill="none" stroke="{INK}" stroke-width="5" pathLength="1" stroke-dasharray="1 1"><animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="0;.4;1" dur="5s" repeatCount="indefinite"/></path>')
    elif kind == "scatter":
        dots = ""
        for i in range(20):
            red = i in (16, 18)
            cx, cy = 50 + i * 14, 140 - i * 5.2 + ((i * 37) % 19 - 9)
            dots += (f'<circle cx="{cx}" cy="{cy:.1f}" r="5" fill="{"#c1121f" if red else INK}">'
                     + (f'<animate attributeName="r" values="5;8;5" dur="1.8s" repeatCount="indefinite"/>' if red else "") + "</circle>")
        s = ax + dots + f'<path d="M40 140L320 36" stroke="{INK}" stroke-dasharray="5 6" stroke-width="3" fill="none"/>'
    elif kind == "cap":
        s = (f'<path d="M180 30L300 80 180 130 60 80z" fill="{INK}"/><path d="M120 104v28c36 24 84 24 120 0v-28" fill="none" stroke="{INK}" stroke-width="6"/>'
             f'<g><animateTransform attributeName="transform" type="rotate" values="-5 290 84;5 290 84;-5 290 84" dur="2.4s" repeatCount="indefinite"/><path d="M290 84v44" stroke="#c1121f" stroke-width="5"/></g>')
    else:  # nodes
        names = ["auth", "posts", "likes", "comments", "follows", "alerts", "media"]
        s = ""
        for i, n in enumerate(names):
            a = -1.57 + i * 6.283 / 7
            c = math.cos(a)
            nx, ny = 180 + 120 * c, 85 + 58 * math.sin(a)
            anc = "start" if c > .3 else "end" if c < -.3 else "middle"
            tx = nx + (12 if c > .3 else -12 if c < -.3 else 0)
            ty = ny + (5 if abs(c) >= .3 else (-12 if ny < 85 else 22))
            s += (f'<path d="M180 85L{nx:.1f} {ny:.1f}" stroke="{INK}" stroke-opacity=".33" stroke-width="3"/>'
                  f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="7" fill="{INK}"><animate attributeName="r" values="7;10;7;7" keyTimes="0;.08;.16;1" dur="5s" begin="{i * .6:.1f}s" repeatCount="indefinite"/></circle>'
                  + d.text(tx, ty, n, "f4", 14, INK, anc))
        s += f'<circle cx="180" cy="85" r="26" fill="#fff" stroke="{INK}" stroke-width="4"/>' + d.text(180, 91, "Zylo", "f6", 16, INK, "middle")
    sc = min(w / 360, h / 170)
    ox, oy = x + (w - 360 * sc) / 2, y + (h - 170 * sc) / 2
    return f'<g transform="translate({ox:.1f} {oy:.1f}) scale({sc:.3f})">{s}</g>'


CARD_W, CARD_IW = 496, 436


def card_geo(p):
    blurb = wrap("f4", typo(p["blurb"]), 17.5, CARD_IW)
    name = wrap("d", p["name"], 20, CARD_IW, -.6)
    notes = [(a, wrap("f4", typo(b), 16.5, CARD_IW - 8)) for a, b in p["notes"]]
    sheet = 36 + sum(24 + len(l) * 23 for _, l in notes) + 14 * (len(notes) - 1) + 14
    # tag rows
    rows, x = 1, 0
    for t in p["tags"]:
        w = tw("f6", t, 14) + 22
        if x + w > CARD_IW:
            rows, x = rows + 1, 0
        x += w + 6
    tags_h = rows * 32
    top = 30 + 206 + 18 + 40 + 14 + len(name) * 25 + 8 + len(blurb) * 25
    return dict(blurb=blurb, name=name, notes=notes, sheet=sheet, tags_h=tags_h, need=top + 14 + tags_h + 10 + 40 + 14 + sheet + 12)


def project_cards():
    geos = [card_geo(p) for p in PROJECTS]
    H = int(max(g["need"] for g in geos))
    for p, g in zip(PROJECTS, geos):
        d = Doc(CARD_W, H, f"{p['name']}: {p['m']} {p['u']}. {p['blurb']} " + " ".join(f"{a}: {b}" for a, b in p["notes"]))
        tile(d, SN, rx=36)
        cx, cw, ch = 12, CARD_W - 24, H - 24
        cp = d.uid("c")
        d.defs.append(f'<clipPath id="{cp}"><rect x="{cx}" y="12" width="{cw}" height="{ch}" rx="30"/></clipPath>')
        d.add(f'<rect x="{cx}" y="12" width="{cw}" height="{ch}" rx="30" fill="#fff"/>')
        ix = 30
        d.add(f'<rect x="{ix}" y="30" width="{CARD_IW}" height="206" rx="20" fill="{p["c"]}"/>')
        d.add(art(d, p["art"], ix, 30, CARD_IW, 206))
        y = 236 + 18 + 40
        d.T(ix, y, p["m"], "d", 42, INK, ls=-2.1)
        d.T(ix + tw("d", p["m"], 42, -2.1) + 10, y, p["u"], "f4", 15, INK, op=.6)
        y += 14 + 20
        d.lines(ix, y, g["name"], "d", 20, INK, 25, ls=-.6)
        y += (len(g["name"]) - 1) * 25 + 10 + 17
        d.lines(ix, y, g["blurb"], "f4", 17.5, INK, 25, op=.78)
        # bottom stack (anchored)
        sheet_y = H - 12 - g["sheet"]
        by = sheet_y - 14 - 40
        ty = by - 10 - g["tags_h"]
        x, row = ix, 0
        for t in p["tags"]:
            w = tw("f6", t, 14) + 22
            if x + w > ix + CARD_IW:
                x, row = ix, row + 1
            d.add(f'<rect x="{x + .75:.1f}" y="{ty + row * 32 + .75:.1f}" width="{w - 1.5:.1f}" height="26" rx="13" fill="none" stroke="{INK}" stroke-width="1.5"/>')
            d.T(x + 11, ty + row * 32 + 18.5, t, "f6", 14, INK)
            x += w + 6
        bw = tw("f6", "Repo", 16) + 28 + 30
        d.add(f'<rect x="{ix + 1}" y="{by + 1}" width="{bw:.1f}" height="38" rx="19" fill="{INK}" stroke="{INK}" stroke-width="2"/>')
        d.T(ix + 16, by + 25, "Repo", "f6", 16, "#fff")
        d.add(arrow(ix + 16 + tw("f6", "Repo", 16) + 9, by + 20, "#fff", 6, 2.2))
        # caveat sheet, like the portfolio's slide-up note
        d.add(f'<g clip-path="url(#{cp})"><path d="M{cx} {sheet_y + 24}a24 24 0 0 1 24-24H{cx + cw - 24}a24 24 0 0 1 24 24V{H - 12}H{cx}z" fill="{INK}"/></g>')
        ny = sheet_y + 36
        for lab, ls_ in g["notes"]:
            d.T(ix, ny, lab, "f6", 16.5, p["c"])
            ny = d.lines(ix, ny + 24, ls_, "f4", 16.5, "#fff", 23) + 14
        S(d, f"card-{p['repo'].lower().replace('_', '-')}.svg")
    return H


def card_file(p):
    return f"card-{p['repo'].lower().replace('_', '-')}.svg"


# ═════════════════════════════ SAHI DAAM ═════════════════════════════
def sahi():
    W, T, P = 1000, 12.0, 56
    cw = 430
    n = len(SAHI)
    states = []
    for lab, fair, rp in SAHI:
        r = rp / 100
        pct = (r - 1) * 100
        states.append(dict(lab=lab, fair=f"{fair:.2f} crore", ask=f"{fair * r:.2f} crore", pct=("+" if pct > 0 else "") + f"{pct:.0f}%",
                           verdict="Priced above similar listings" if pct > 5 else "Possible bargain" if pct < -5 else "About fair",
                           bg=TG if pct > 5 else MT if pct < -5 else YE, tx=P + (rp - 70) / 60 * cw, bar=cw * min(1, r / 1.3)))
    d0 = Doc(W, 10, "x")
    y = header(d0, "sahi", P, P)  # measure only
    # left column layout
    pre_rows, x, row = [], 0, 0
    pos = []
    for s in states:
        w = tw("f6", s["lab"], 16) + 32
        if x + w > cw:
            x, row = 0, row + 1
        pos.append((x, row, w))
        x += w + 8
    rows = row + 1
    ytop = y + 20
    ly = ytop + rows * 46 + 14
    para = wrap("f4", typo("Data: zameen.com via requests + BeautifulSoup, starting with DHA Islamabad rentals. No headline metric yet; I'll publish one when I can defend it. Flagged means priced above similar listings, never \"scam\"."), 17.5, cw)
    bottom_left = ly + 26 + 10 + 40 + 26 + 8 + 26 + 8 + 26 + 18 + len(para) * 25
    H = int(bottom_left + P)
    d = Doc(W, H, "Sahi Daam fair-price detector demo with example numbers: " + "; ".join(f"{s['lab']}: asking {s['ask']} vs fair {s['fair']}, {s['pct']}, {s['verdict']}" for s in states))
    vals, kts = smooth([s["bg"] for s in states], .04)
    d.add(f'<rect width="{W}" height="{H}" rx="44" fill="{states[0]["bg"]}">{anim("fill", vals, T, kts)}</rect>')
    header(d, "sahi", P, P)
    # preset pills
    for i, s in enumerate(states):
        px, prow, w = pos[i]
        yy = ytop + prow * 46
        on = [INK if k == i else "#0c0c1600" for k in range(n)]
        d.add(f'<rect x="{P + px + 1}" y="{yy + 1}" width="{w - 2:.1f}" height="36" rx="18" fill="none" stroke="{INK}" stroke-width="2">{anim("fill", on, T, [k / n for k in range(n)], discrete=True)}</rect>')
        tcol = [WHITE if k == i else INK for k in range(n)]
        d.add(d.text(P + px + 16, yy + 24.5, s["lab"], "f6", 16, INK).replace("</text>", f'{anim("fill", tcol, T, [k / n for k in range(n)], discrete=True)}</text>'))
    # asking
    def swap(x, y, key, f, size, fill, anchor="start", ls=None, op=None):
        for i, s in enumerate(states):
            d.add(f'<g opacity="{1 if i == 0 else 0}">{window(n, i, T)}' + d.text(x, y, s[key], f, size, fill, anchor, op, ls) + "</g>")
    yy = ly + 20
    d.T(P, yy, "Asking price", "f6", 18, INK)
    swap(P + cw, yy, "ask", "d", 22, INK, "end", ls=-.9)
    # slider
    sy = yy + 26
    d.add(f'<rect x="{P}" y="{sy + 14}" width="{cw}" height="8" rx="4" fill="{INK}" fill-opacity=".22"/>')
    tvals, tk = smooth([s["tx"] for s in states], .04)
    fvals, fk = smooth([s["tx"] - P for s in states], .04)
    d.add(f'<rect x="{P}" y="{sy + 14}" width="0" height="8" rx="4" fill="{INK}">{anim("width", fvals, T, fk)}</rect>')
    d.add(f'<circle cx="{states[0]["tx"]:.1f}" cy="{sy + 18}" r="13" fill="{INK}" stroke="#fff" stroke-width="3">{anim("cx", tvals, T, tk)}</circle>')
    yy = sy + 40 + 26
    d.T(P, yy, "Fair price (example)", "f6", 18, INK)
    swap(P + cw, yy, "fair", "d", 22, INK, "end", ls=-.9)
    by = yy + 18
    bv, bk = smooth([s["bar"] for s in states], .04)
    d.add(f'<rect x="{P}" y="{by}" width="{cw}" height="26" rx="13" fill="{INK}" fill-opacity=".14"/><rect x="{P}" y="{by}" width="{states[0]["bar"]:.1f}" height="26" rx="13" fill="{INK}">{anim("width", bv, T, bk)}</rect>')
    d.add(f'<rect x="{P}" y="{by + 34}" width="{cw}" height="26" rx="13" fill="{INK}" fill-opacity=".14"/><rect x="{P}" y="{by + 34}" width="{cw / 1.3:.1f}" height="26" rx="13" fill="{INK}" fill-opacity=".45"/>')
    d.lines(P, by + 60 + 36, para, "f4", 17.5, INK, 25, op=.8)
    # right column: the verdict
    rx_, rw = 540, 404
    big = min(130, rw / max(adv("d", s["pct"]) for s in states) * .98)
    cy = ytop + 150
    swap(rx_, cy, "pct", "d", big, INK, ls=-.07 * big)
    for i, s in enumerate(states):
        vl = wrap("d", s["verdict"], 28, rw, -1.1)
        inner = "".join(d.text(rx_, cy + 54 + k * 33, l, "d", 28, INK, ls=-1.1) for k, l in enumerate(vl))
        d.add(f'<g opacity="{1 if i == 0 else 0}">{window(n, i, T)}{inner}</g>')
    S(d, "sahi.svg")


# ═════════════════════════════ CONCEPT LAB ═════════════════════════════
def lab():
    W, T, P = 1000, 12.0, 56
    d0 = Doc(W, 10, "x")
    y = header(d0, "lab", P, P)
    sy, sh = y + 20, 340
    cards = []
    cwid, gap = 282, 21
    for name, blurb, stack in CONCEPTS:
        nl = wrap("d", name, 22, cwid - 44, -.9)
        bl = wrap("f4", typo(blurb), 17, cwid - 44)
        sl = []
        cur = ""
        for w in stack.split(" "):
            t = (cur + " " + w).strip()
            if len(t) * 7.9 > cwid - 44 and cur:
                sl.append(cur)
                cur = w
            else:
                cur = t
        sl.append(cur)
        cards.append((name, nl, bl, sl))
    ch = int(max(22 + 28 + 28 + len(c[1]) * 27 + 10 + len(c[2]) * 24 + 10 + len(c[3]) * 20 + 22 for c in cards))
    cy0 = sy + sh + 20 + 44 + 28
    H = int(cy0 + ch + P)
    d = Doc(W, H, "Concept lab: Div Space (stick a chip on the floor and a temporary room appears), Inventory OS, NOVA DOCK, and a bill splitter plus budget tracker. Concepts I design, built with AI.")
    tile(d, LC)
    header(d, "lab", P, P)
    sw = W - 2 * P
    d.add(f'<rect x="{P + 1}" y="{sy + 1}" width="{sw - 2}" height="{sh - 2}" rx="30" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')
    fy = sy + sh - 54
    cp = d.uid("c")
    d.defs.append(f'<clipPath id="{cp}"><rect x="{P + 1}" y="{sy + 1}" width="{sw - 2}" height="{sh - 2}" rx="30"/></clipPath>')
    # everything inside the stage is clipped to its rounded rect
    inner = f'<rect x="{P}" y="{fy}" width="{sw}" height="4" fill="{INK}"/>'
    chip_x = P + sw * .46
    # chip pops in/out
    ev = [(0, 0), (1.4, 0), (1.75, 1.25), (1.95, 1), (5.6, 1), (6.0, 0), (8.0, 0), (8.35, 1.25), (8.55, 1), (11.2, 1), (11.6, 0), (12, 0)]
    cv, ck = track(ev, T)
    inner += (f'<g transform="translate({chip_x:.1f} {fy})"><g><animateTransform attributeName="transform" type="scale" values="{";".join(f"{v} {v}" for v in cv)}" keyTimes="{";".join(f"{k:.4f}" for k in ck)}" dur="{T}s" repeatCount="indefinite"/>'
              f'<rect x="-19" y="-12" width="38" height="12" rx="4" fill="{TG}" stroke="{INK}" stroke-width="3"/></g></g>')
    # room grows up from the floor
    rb = fy - 12
    hv = [(0, 0), (1.5, 0), (2.1, 210), (5.6, 210), (6.1, 0), (8.0, 0), (8.6, 210), (11.2, 210), (11.7, 0), (12, 0)]
    hvals, hk = track(hv, T)
    yv = [rb - v for v in hvals]
    rw_ = 270
    rxl = max(P + 20, min(P + sw - rw_ - 20, chip_x - rw_ / 2))
    rid = d.uid("rc")
    d.defs.append(f'<clipPath id="{rid}"><rect x="{rxl:.1f}" y="{rb}" width="{rw_}" height="0">{anim("y", yv, T, hk)}{anim("height", hvals, T, hk)}</rect></clipPath>')
    inner += (f'<rect x="{rxl + 1.5:.1f}" y="{rb}" width="{rw_ - 3}" height="0" rx="14" fill="{CB}" fill-opacity=".08" stroke="{CB}" stroke-width="3" stroke-dasharray="9 7">{anim("y", yv, T, hk)}{anim("height", hvals, T, hk)}</rect>')
    shapes = ""
    for (col, left, dl, kind) in [(TG, 40, 0, "c"), (CB, 100, .5, "r"), (MT, 165, 1, "l")]:
        bx, by_ = rxl + left, rb - 16 - 36
        if kind == "c":
            sh_ = f'<circle cx="{bx + 18}" cy="{by_ + 18}" r="18" fill="{col}"/>'
        elif kind == "r":
            sh_ = f'<rect x="{bx}" y="{by_}" width="36" height="36" rx="6" fill="{col}"/>'
        else:
            sh_ = f'<path d="M{bx} {by_ + 18}A18 18 0 0 1 {bx + 18} {by_}H{bx + 36}V{by_ + 18}A18 18 0 0 1 {bx + 18} {by_ + 36}H{bx}Z" fill="{col}"/>'
        shapes += (f'<g>{anim_t("translate", ["0 0", "0 -16", "0 0"], 2.3, begin=f"{dl}s")}{anim_t("rotate", [f"0 {bx + 18} {by_ + 18}", f"8 {bx + 18} {by_ + 18}", f"0 {bx + 18} {by_ + 18}"], 2.3, begin=f"{dl}s")}{sh_}</g>')
    inner += f'<g clip-path="url(#{rid})">{shapes}' + d.text(rxl + 14, rb - 210 + 28, "<div>", "m", 15, CB) + "</g>"
    d.add(f'<g clip-path="url(#{cp})">{inner}</g>')
    # hints
    H1, H2, H3 = "Place a chip on the floor and a room appears.", "A temporary room. Remove the chip and it disappears.", "The room is gone, but one chip brings it back."
    sched = [(0, 0), (1.4, 1), (5.6, 2), (8.0, 1), (11.2, 2)]
    for k, hint in enumerate([H1, H2, H3]):
        op = [1 if s == k else 0 for _, s in sched]
        d.add(f'<g opacity="{op[0]}">{anim("opacity", op, T, [t / T for t, _ in sched], discrete=True)}' + d.text(P + sw / 2, sy + sh - 18, hint, "f4", 16, INK, "middle", op=.65) + "</g>")
    # buttons
    by = sy + sh + 20
    for j, (lab_, win) in enumerate([("Remove chip", [(5.5, 6.3), (11.1, 11.9)]), ("Recall room", [(7.9, 8.7)])]):
        bx = P + j * 170
        evs = [(0, 0)]
        for a, b in win:
            evs += [(a, 1), (b, 0)]
        vv, kk = track([(0, 0)] + [(t, v) for a, b in win for t, v in ((a, 1), (b, 0))], T)
        d.add(f'<rect x="{bx + 1}" y="{by + 1}" width="{tw("f6", lab_, 16) + 30:.1f}" height="36" rx="18" fill="none" stroke="{INK}" stroke-width="2">{anim("fill", [INK if v else "#0c0c1600" for v in vv], T, kk, discrete=True)}</rect>')
        d.add(d.text(bx + 16, by + 24.5, lab_, "f6", 16, INK).replace("</text>", f'{anim("fill", [WHITE if v else INK for v in vv], T, kk, discrete=True)}</text>'))
    # concept cards
    for i, (name, nl, bl, sl) in enumerate(cards):
        x = P + i * (cwid + gap)
        d.add(f'<rect x="{x + 1}" y="{cy0 + 1}" width="{cwid - 2}" height="{ch - 2}" rx="26" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        tag = "my concept · built with AI"
        tg_w = tw("f6", tag, 13) + 24
        d.add(f'<rect x="{x + 22}" y="{cy0 + 22}" width="{tg_w:.1f}" height="24" rx="12" fill="{CB}"/>')
        d.T(x + 34, cy0 + 39, tag, "f6", 13, "#fff")
        yy = d.lines(x + 22, cy0 + 22 + 24 + 34, nl, "d", 22, INK, 27, ls=-.9)
        yy = d.lines(x + 22, yy + 2 + 8, bl, "f4", 17, INK, 24, op=.78)
        for k, l in enumerate(sl):
            d.T(x + 22, yy + 6 + 14 + k * 20, l, "m", 13, INK, op=.6)
    S(d, "lab.svg")


# ═════════════════════════════ ROUTE ═════════════════════════════
def route():
    W, P = 1000, 56
    d0 = Doc(W, 10, "x")
    y = header(d0, "route", P, P)
    x0 = P
    bx, bw = x0 + 46, W - P - (x0 + 46)
    colw = (bw - 40 - 2 * 26) / 3
    rows = []
    for t, s, when, a, b, c in ROUTE:
        if s == "n":
            cols = [("Learn deeply", a), ("Skip for now", b), ("Checkpoint", c)]
            wr = [wrap("f4", typo(txt), 17, colw) for _, txt in cols]
            body = 14 + 28 + max(len(w) for w in wr) * 24 + 12
            rows.append((t, s, when, 64 + body, cols, wr))
        else:
            rows.append((t, s, when, 64, None, None))
    y0 = y + 20
    H = int(y0 + sum(r[3] + 14 for r in rows) + P - 14)
    d = Doc(W, H, "Roadmap: " + "; ".join(f"{r[0]} ({r[2]})" for r in rows) + ". Currently on NLP.")
    tile(d, INK, stroke="#ffffff22")
    header(d, "route", P, P, fg="#fff")
    # timeline
    d.add(f'<rect x="{x0 + 12}" y="{y0 + 8}" width="4" height="{H - P - y0 - 8}" rx="2" fill="#fff" fill-opacity=".17"/>')
    cur = y0
    now_y = None
    for t, s, when, h, cols, wr in rows:
        dot = MT if s == "d" else TG if s == "n" else INK
        dstroke = MT if s == "d" else TG if s == "n" else "#ffffff55"
        cyd = cur + 32
        if s == "n":
            now_y = cyd
        d.add(f'<rect x="{bx + .75}" y="{cur + .75}" width="{bw - 1.5}" height="{h - 1.5}" rx="20" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".17" stroke-width="1.5"/>')
        d.add(f'<circle cx="{x0 + 14}" cy="{cyd}" r="10" fill="{dot}" stroke="{dstroke}" stroke-width="4"/>')
        if s == "n":
            d.add(f'<circle cx="{x0 + 14}" cy="{cyd}" r="10" fill="{TG}" fill-opacity=".45">{anim("r", [10, 22, 22], 1.8, [0, .8, 1])}{anim("fill-opacity", [.5, 0, 0], 1.8, [0, .8, 1])}</circle>')
        d.T(bx + 22, cur + 40, t, "d", 20, "#fff", ls=-.6)
        d.T(bx + bw - 22, cur + 38, when, "f4", 15, "#fff", "end", op=.65)
        if cols:
            for k, ((lab_, _), lines_) in enumerate(zip(cols, wr)):
                cx = bx + 22 + k * (colw + 26)
                d.T(cx, cur + 64 + 24, lab_, "f6", 17, TG)
                d.lines(cx, cur + 64 + 24 + 28, lines_, "f4", 17, "#fff", 24, op=.85)
        cur += h + 14
    # progress fill grows to the stop I'm on
    d.add(f'<rect x="{x0 + 12}" y="{y0 + 8}" width="4" height="0" rx="2" fill="{TG}">{anim("height", [0, now_y - y0 - 8], 2.2, repeat=None, freeze=True, spline="0.3 0 0.2 1")}</rect>')
    S(d, "route.svg")


# ═════════════════════════════ SKILLS ═════════════════════════════
def skills():
    W, P = 1000, 56
    d0 = Doc(W, 10, "x")
    y = header(d0, "skills", P, P)
    cols, gap, ph = 2, 14, 60
    pw = (W - 2 * P - gap) / cols
    rows = math.ceil(len(SKILLS) / cols)
    y0 = y + 20
    H = int(y0 + rows * (ph + gap) + 30 + P)
    d = Doc(W, H, "Skills: " + "; ".join(f"{n} ({['', 'learning', 'working', 'comfortable'][l]})" for n, l in SKILLS))
    tile(d, MT)
    header(d, "skills", P, P)
    for i, (n, l) in enumerate(SKILLS):
        x, yy = P + (i % cols) * (pw + gap), y0 + (i // cols) * (ph + gap)
        d.add(f'<rect x="{x:.1f}" y="{yy}" width="{pw:.1f}" height="{ph}" rx="22" fill="{INK}"/>')
        d.T(x + 22, yy + ph / 2 + 6.5, n, "f6", 19, "#fff")
        for k in range(3):
            cx = x + pw - 22 - (2 - k) * 19 - 7
            col = LEVEL_COL[l]
            fill = col if k < l else "none"
            d.add(f'<circle cx="{cx:.1f}" cy="{yy + ph / 2}" r="6" fill="{fill}" stroke="{col if k < l else "#ffffff66"}" stroke-width="2"/>')
    ly = y0 + rows * (ph + gap) + 14
    x = P
    for lab_, col in [("learning", TG), ("working", YE), ("comfortable", MT)]:
        d.add(f'<circle cx="{x + 7}" cy="{ly}" r="7" fill="{col}" stroke="{INK}" stroke-width="2"/>')
        d.T(x + 22, ly + 6, lab_, "f6", 17, INK, op=.8)
        x += 22 + tw("f6", lab_, 17) + 26
    S(d, "skills.svg")


# ═════════════════════════════ SAY HI ═════════════════════════════
def sayhi():
    W, H = 1000, 380
    d = Doc(W, H, "Say hi. Never stop because life is not end yet.")
    blobs(d, W, H, dur=1.3)
    size = 150
    d.add(f'<g style="mix-blend-mode:difference">' + d.text(W / 2, 196, "Say hi.", "d", size, WHITE, "middle", ls=-.07 * size) + "</g>")
    d.T(W / 2, 262, "Never stop because life is not end yet.", "f4", 26, WHITE, "middle")
    S(d, "sayhi.svg")


def buttons():
    pill_img("nav-top.svg", "MZ", font="d", size=14, pad=18)
    for k, lab_ in [("builds", "Builds"), ("sahi", "Sahi Daam"), ("lab", "Lab"), ("route", "Route"), ("skills", "Skills"), ("live", "Live")]:
        pill_img(f"nav-{k}.svg", lab_)
    for lab_, _ in LINKS:
        pill_img(f"btn-{lab_.lower().replace('.', '')}.svg", lab_, bg="#fff", fg=INK, stroke=INK, size=19, h=50, pad=26, shadow=CB)
    pill_img("btn-sahi-repo.svg", "Sahi Daam repo", bg=INK, fg="#fff", size=17, h=46, pad=24, arrow_=True)


# ═════════════════════════════ README ═════════════════════════════
def img(name, alt, w="100%", extra=""):
    return f'<img src="assets/{name}" width="{w}" alt="{alt}"{extra} />' if w else f'<img src="assets/{name}" alt="{alt}" />'


def readme(card_h):
    repo = lambda p: f"{GH}/{p['repo']}"
    cards = "\n".join(f'<a href="{repo(p)}"><img src="assets/{card_file(p)}" width="49.5%" alt="{p["name"]}: {p["m"]} {p["u"]}. {p["blurb"]}" /></a>' for p in PROJECTS)
    nav = " ".join(f'<a href="{h}"><img src="assets/nav-{k}.svg" alt="{a}" /></a>' for h, k, a in
                   [("#top", "top", "MZ"), ("#builds", "builds", "Builds"), ("#sahi", "sahi", "Sahi Daam"), ("#lab", "lab", "Lab"), ("#route", "route", "Route"), ("#skills", "skills", "Skills"), ("#live", "live", "Live")])
    links = " ".join(f'<a href="{u}"><img src="assets/btn-{n.lower().replace(".", "")}.svg" alt="{n}" /></a>' for n, u in LINKS)
    stops = "\n".join(f"<tr><td><b>{t}</b></td><td>{w}</td><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for t, s, w, a, b, c in ROUTE)
    plain_projects = "\n".join(f"- [{p['name']}]({repo(p)}) · {p['m']} {p['u']}. {p['blurb']}" for p in PROJECTS)
    return f"""<!--
  Malik Zain: GitHub profile README. Generated by build_assets.py (edit the DATA block there, run it, push).
  The design is the portfolio page redrawn as SVG tiles; the "Live from GitHub" tile is redrawn by a GitHub Action.
  Fonts: Unbounded and Hanken Grotesk (SIL Open Font License), embedded in the SVGs.
-->

<a id="top"></a>

<p align="center"><img src="assets/hero.svg" width="100%" alt="{HERO_H1} Malik Zain, BS CS student at Riphah and AI/ML intern at FlyRank, in Islamabad. Now: NLP. Building: Sahi Daam. Later, inshallah: deep learning, RAG." /></p>

<p align="center">{nav}</p>

<p align="center"><img src="assets/numbers.svg" width="100%" alt="74.4% resume classifier, about 98% fake-news classifier (which overstates it), 0.86 churn ROC-AUC with 83% recall, 6 repos pinned each with its caveat." /></p>

<a id="builds"></a>
<p align="center">
<img src="assets/h-builds.svg" width="100%" alt="What I built, and what the numbers hide. The six repos pinned on my GitHub, each with its caveat." />
{cards}
</p>

<a id="sahi"></a>
<p align="center">
<img src="assets/sahi.svg" width="100%" alt="Sahi Daam: is it overpriced? A looping demo with example numbers: asking price versus the model's fair price, and the verdict." /><br />
<a href="{GH}/sahi-daam-fair-price-detector"><img src="assets/btn-sahi-repo.svg" alt="Sahi Daam repo" /></a>
</p>

<a id="lab"></a>
<p align="center"><img src="assets/lab.svg" width="100%" alt="Concept lab: Div Space, Inventory OS, NOVA DOCK, and a bill splitter plus budget tracker. Ideas I design, built with AI." /></p>

<a id="route"></a>
<p align="center"><img src="assets/route.svg" width="100%" alt="Roadmap: HTML, CSS, JS; React; Python; Machine learning; NLP (now); Deep learning and RAG apps (later, inshallah)." /></p>

<details>
<summary><b>Open every stop</b> (solid, still shaky, checkpoint)</summary>
<br />

<table>
<tr><th>Stop</th><th>When</th><th>Solid / learning deeply</th><th>Still shaky / skipping for now</th><th>Checkpoint</th></tr>
{stops}
</table>

</details>

<a id="skills"></a>
<p align="center"><img src="assets/skills.svg" width="100%" alt="Skills, honestly. Only things I can do myself." /></p>

<a id="live"></a>
<p align="center">
<img src="assets/live.svg" width="100%" alt="Live from GitHub: public repos, followers, stars earned, top languages and recently pushed repos." /><br />
<img src="https://ghchart.rshah.org/2b3cff/Malik-Zain-555" width="100%" alt="GitHub contribution graph" />
</p>

<p align="center"><img src="assets/sayhi.svg" width="100%" alt="Say hi. Never stop because life is not end yet." /></p>

<p align="center">{links}</p>

<p align="center"><sub>Built by hand. Generated by <code>build_assets.py</code>; the live tile is redrawn by a GitHub Action.</sub></p>

<details>
<summary>Plain-text version</summary>
<br />

**Malik Zain.** BS CS student at Riphah and AI/ML intern at FlyRank, in Islamabad. I learn by building, not by theory. I build small machine-learning projects, then measure where they break.

Now: NLP. Building: Sahi Daam. Later, inshallah: deep learning, RAG.

{plain_projects}

[GitHub]({LINKS[0][1]}) · [LinkedIn]({LINKS[1][1]}) · [itch.io]({LINKS[2][1]})

</details>
"""


def builds_header():
    d0 = Doc(1000, 10, "x")
    y = header(d0, "builds", 56, 56)
    H = int(y + 40)
    d = Doc(1000, H, "What I built, and what the numbers hide. " + SECTION_TXT["builds"][1])
    tile(d, SN)
    header(d, "builds", 56, 56)
    S(d, "h-builds.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("tiles")
    hero()
    numbers()
    builds_header()
    ch = project_cards()
    sahi()
    lab()
    route()
    skills()
    sayhi()
    buttons()
    live.render_live(live.seed_data(), os.path.join(OUT, "live.svg"))
    with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(readme(ch))
    print("README.md written")
