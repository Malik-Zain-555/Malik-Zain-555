#!/usr/bin/env python3
"""Zain Ali — profile README generator ("Workbench").
    python3 build_assets.py   ->  writes ./assets/*.svg and ./README.md
Edit the DATA blocks below (BUILDS, AI_BUILT, SKILLS, ...), run again, push.
Live graphics (stats, heatmap, scoreboard) are redrawn by GitHub Actions and never overwritten here."""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".github", "scripts"))
from ui import *  # noqa: E402,F401,F403
import fight, stats  # noqa: E402

OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)
S = lambda name, content: save(os.path.join(OUT, name), content)
ME = "https://github.com/Malik-Zain-555"
PROFILE_REPO = "https://github.com/Malik-Zain-555/Malik-Zain-555"

# ═════════════════════════════ DATA ═════════════════════════════
BUILDS = [  # same order as my pinned repos
    dict(key="resume", n="01", kind="NLP · DEPLOYED", title="Resume Category Classifier", repo="resume-category-classifier", status=("SHIPPED", MINT),
         big="74.4%", delta=["test accuracy, up from", "71.8% with TF-IDF"],
         problem="Sorts resumes into 24 job categories, and answers UNSURE when it isn't confident.",
         insight="Compared TF-IDF with sentence embeddings, inspected the weights, then shipped it as a FastAPI + Docker service.",
         rail=["DATA", "TF-IDF", "EMBEDDINGS", "API + DOCKER"], reached=4, tags=["scikit-learn", "embeddings", "FastAPI", "Docker"]),
    dict(key="fake", n="02", kind="NLP · ANALYSIS", title="Fake News Style Detector", repo="fake_news_style_detector", status=("INVESTIGATED", SKY),
         big="~98%", delta=["accuracy, and why that", "number can mislead"],
         problem="A fake/real news classifier (TF-IDF + Logistic Regression).",
         insight="Investigation: it learns the source's writing style, not truth. A \"Reuters\" shortcut shows in the top weights.",
         rail=["DATA", "TF-IDF + LR", "~98%", "INVESTIGATE"], reached=4, tags=["scikit-learn", "TF-IDF", "error analysis"]),
    dict(key="churn", n="03", kind="TABULAR ML · DEPLOYED", title="Churn Prediction Pipeline", repo="churn-prediction-pipeline", status=("SHIPPED", MINT),
         big="0.86", delta=["ROC-AUC, with 83%", "recall on churners"],
         problem="Predicts which customers are likely to churn, end to end, from raw data to a usable app.",
         insight="sklearn ColumnTransformer + Pipeline + Logistic Regression, deployed as an interactive Streamlit app.",
         rail=["PIPELINE", "LOGREG", "EVALUATE", "STREAMLIT"], reached=4, tags=["scikit-learn", "Pipeline", "Streamlit"]),
    dict(key="eda", n="04", kind="DATA ANALYSIS", title="Heart Disease EDA", repo="EDA-Heart_Disease", status=("NOTEBOOK", SKY),
         big="EDA", delta=["exploratory analysis", "of a heart disease dataset"],
         problem="Looking at what a heart disease dataset says before any modelling starts.",
         insight=None, rail=None, reached=0, tags=["Python", "pandas", "Jupyter"]),
    dict(key="fyp", n="05", kind="UNIVERSITY", title="Final Year Project", repo="MUDABBIR-FYP", status=("UNIVERSITY", SKY),
         big="FYP", delta=["my final year", "project repository"],
         problem="The repository for my university final year project.",
         insight=None, rail=None, reached=0, tags=["BS CS", "Riphah"]),
    dict(key="zylo", n="06", kind="FULL-STACK WEB", title="Zylo", repo="Zylo", status=("TUTORIAL-GUIDED", AMB),
         big="Web", delta=["full-stack social", "media platform"],
         problem="User auth, posts, likes, comments, follows, notifications and media uploads.",
         insight=None, rail=None, reached=0, tags=["Node.js", "Express", "EJS", "MySQL"]),
]
AI_BUILT = [  # concepts I design, code written with AI help (edit / add yours)
    ("inventory", "Inventory OS", "Offline-first POS and inventory concept for small shops.", "NestJS · Electron · Expo React Native · Railway + Neon PostgreSQL"),
    ("nova", "NOVA DOCK", "A Windows dock in the style of the iPhone Dynamic Island. A v2.0 rebuild is planned.", "Python · PySide6"),
]
SKILLS = {  # 3 comfortable, 2 working, 1 learning
    "AI / ML": ([("Python", 2), ("scikit-learn + Pipelines", 2), ("NumPy", 2), ("Matplotlib", 2), ("Streamlit", 2), ("pandas", 1),
                 ("NLP: TF-IDF, embeddings", 1), ("FastAPI + Docker (resume repo)", 1)], VIO),
    "WEB + TOOLS": ([("HTML", 3), ("CSS", 3), ("Tailwind CSS", 2), ("JavaScript", 2), ("React", 2), ("Node + Express (via Zylo)", 1),
                     ("SQL (MySQL), MongoDB basics", 1), ("Git + GitHub", 2), ("VS Code · Google Colab", 3)], SKY),
}


# ═════════════════════════════ HERO ═════════════════════════════
def hero():
    W, H, T = 880, 500, 14.0
    body = f'<circle cx="56" cy="44" r="6" fill="{OR}"/>' + serif(72, 51, "Zain Ali", 24, TX, weight=700)
    body += mono(W - 48, 49, "AI/ML INTERN  ·  ISLAMABAD  ·  PAKISTAN", 11.5, MUT, "end", 1.5) + f'<line x1="48" y1="72" x2="{W - 48}" y2="72" stroke="{LINE}"/>'
    body += serif(56, 158, "I learn by", 64, TX) + serif(56, 226, "building,", 64, OR, italic=True, extra='textLength="288" lengthAdjust="spacingAndGlyphs"')
    body += f'<line x1="56" y1="240" x2="344" y2="240" stroke="{OR}" stroke-width="3" stroke-dasharray="288" stroke-dashoffset="288">{A("stroke-dashoffset", [288, 288, 0, 0, 288], [0, .05, .2, .93, 1], T)}</line>'
    body += serif(56, 294, "not by theory.", 64, SOFT, italic=True)
    # terminal
    tx, ty, tw, th = 520, 98, 320, 236
    body += f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="14" fill="{SURF2}" stroke="{LINE}"/><line x1="{tx}" y1="{ty + 34}" x2="{tx + tw}" y2="{ty + 34}" stroke="{LINE}"/>'
    body += "".join(f'<circle cx="{tx + 18 + i * 16}" cy="{ty + 17}" r="4.5" fill="{c}"/>' for i, c in enumerate([ROSE, AMB, MINT]))
    body += mono(tx + tw - 16, ty + 21, "workbench", 10.5, MUT, "end", 1)
    rows = [("$ zain build --real-problems", TX, None), ("✓ resume-category-classifier", MINT, "74.4%"), ("✓ fake_news_style_detector", MINT, "~98%"),
            ("✓ churn-prediction-pipeline", MINT, "0.86 AUC"), ("▶ sahi-daam-fair-price-detector", AMB, None)]
    for i, (txt, col, val) in enumerate(rows):
        t0 = 0.6 + i * 0.8
        v, k = window(t0, 13.2, T, .3)
        y = ty + 66 + i * 30
        line = mono(tx + 18, y, txt, 12, col if i else TX) + (mono(tx + tw - 18, y, val, 12, TX, "end") if val else "")
        body += f'<g opacity="0">{A("opacity", v, k, T)}{AT("translate", ["-10 0", "-10 0", "0 0", "0 0"], [0, t0 / T, (t0 + .35) / T, 1], T)}{line}</g>'
    by = ty + 66 + 4 * 30 + 16
    body += (f'<g opacity="0">{A("opacity", *window(4.2, 13.2, T, .3), T)}<rect x="{tx + 18}" y="{by}" width="{tw - 36}" height="6" rx="3" fill="{LINE}"/>'
             f'<rect x="{tx + 18}" y="{by}" width="0" height="6" rx="3" fill="{AMB}">{A("width", [0, 0, tw - 36, tw - 36, 0], [0, 4.4 / T, 10.5 / T, 13.2 / T, 1], T)}</rect></g>')
    body += f'<g>{blink(1)}<rect x="{tx + 18}" y="{ty + th - 30}" width="8" height="15" fill="{OR}"/></g>'
    body += f'<line x1="48" y1="368" x2="{W - 48}" y2="368" stroke="{LINE}"/>'
    for j, ln in enumerate(wrap_text("AI/ML intern building machine-learning systems that solve real problems: NLP, tabular ML and deployment. Going deeper into ML and NLP now, with deep learning and RAG next.", 96)):
        body += sans(56, 402 + j * 25, ln, 16, SOFT)
    x, y = 56, 440
    for t, c in [("AI/ML INTERN @ FLYRANK", MINT), ("BS CS · RIPHAH UNIVERSITY", SKY), ("SHIPPED: FASTAPI + DOCKER", VIO), ("NOW BUILDING: SAHI DAAM", AMB)]:
        s, w = chip(x, y, t, c, 10.5, 24)
        body += s
        x += w + 10
    S("hero.svg", svg(W, H, body, "Zain Ali. I learn by building, not by theory. AI/ML intern in Islamabad. A terminal shows shipped builds and the one in progress.", r=22, grid=True))


def numbers():
    W, H = 880, 128
    items = [("74.4%", "RESUME CLASSIFIER", "up from 71.8% with TF-IDF", OR), ("~98%", "FAKE NEWS CLASSIFIER", "and why it can mislead", TX),
             ("0.86", "CHURN ROC-AUC", "83% recall on churners", TX), ("3", "PROJECTS DEPLOYED", "Streamlit ×2 · FastAPI + Docker", MINT)]
    body = ""
    for i, (n, lab, sub, col) in enumerate(items):
        x = 24 + i * 208
        if i:
            body += f'<line x1="{x - 12}" y1="26" x2="{x - 12}" y2="102" stroke="{LINE}"/>'
        body += serif(x + 8, 70, n, 50, col) + mono(x + 8, 92, lab, 10.5, TX, ls=1.5) + sans(x + 8, 111, sub, 12, MUT)
    S("numbers.svg", svg(W, H, body, "Results: 74.4 percent resume classifier, about 98 percent fake news classifier, 0.86 churn ROC-AUC, 3 deployed projects"))


def role_tile(file, kicker, title, sub, col):
    W, H = 280, 128
    body = f'<rect x="0" y="0" width="4" height="{H}" fill="{col}"/>' + mono(24, 34, kicker, 10.5, col, ls=2.5) + serif(24, 72, title, fit(title, 210, 27), TX)
    body += sans(24, 98, sub, 13.5, SOFT) + f'<g>{AT("translate", ["0 0", "6 0", "0 0"], dur=1.6)}' + serif(W - 24, 44, "→", 26, col, "end") + "</g>"
    S(file, svg(W, H, body, f"{kicker}: {title}. {sub}", r=14))


def principles():
    W, H = 880, 188
    items = [("01", "Build first.", "I learn by building, not by theory. No offense to theory, it just isn't how I learn."),
             ("02", "Real problems.", "Nothing meaningless. Each project solves something a real person would care about."),
             ("03", "Honest labels.", "AI-built, tutorial-guided or mine, I say which. Every time.")]
    body = ""
    for i, (n, h, t) in enumerate(items):
        x = 32 + i * 288
        if i:
            body += f'<line x1="{x - 16}" y1="28" x2="{x - 16}" y2="{H - 28}" stroke="{LINE}"/>'
        body += mono(x, 44, n, 11, OR, ls=2) + serif(x, 80, h, 28, TX)
        for j, ln in enumerate(wrap_text(t, 34)[:4]):
            body += sans(x, 108 + j * 21, ln, 14, SOFT)
    S("principles.svg", svg(W, H, body, "How I work: build first, real problems, honest labels"))


# ═════════════════════════════ HEADERS / BUTTONS ═════════════════════════════
def header(file, idx, title, why):
    W, H = 880, 84
    body = mono(32, 32, idx, 11.5, OR, ls=3) + serif(32, 62, title, 36, TX) + mono(W - 32, 54, why, 11.5, MUT, "end", 1) + tick(W, H - 1, OR, 5.5)
    S(file, svg(W, H, body, f"{idx} {title}. {why}", r=16))


def button(file, label, col):
    W, H = 200, 46
    body = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="{SURF}" stroke="{col}" stroke-opacity=".8" stroke-width="1.5"/>'
    body += sans(26, 29, label, 14, TX, weight=600) + f'<g>{AT("translate", ["0 0", "5 0", "0 0"], dur=1.8)}' + sans(W - 30, 30, "→", 18, col, "end", 700) + "</g>"
    S(file, svg(W, H, body, label, frame=False))


# ═════════════════════════════ BUILD CARDS ═════════════════════════════
def build_card(i, d, H=410):
    W = 430
    sc = d["status"][1]
    w = len(d["status"][0]) * 7.4 + 22
    body = mono(24, 38, f"{d['n']}  ·  {d['kind']}", 10.5, MUT, ls=1.5)
    body += f'<rect x="{W - 24 - w}" y="21" width="{w}" height="24" rx="12" fill="{sc}" fill-opacity=".12" stroke="{sc}" stroke-opacity=".6"/>' + mono(W - 24 - w / 2, 37, d["status"][0], 10.5, sc, "middle", 1)
    body += serif(24, 84, d["title"], fit(d["title"], W - 48, 28), TX) + mono(24, 106, d["repo"] + " ↗", 12, OR)
    body += f'<line x1="24" y1="122" x2="{W - 24}" y2="122" stroke="{LINE}"/>'
    body += serif(24, 184, d["big"], fit(d["big"], 190, 62, .52), OR) + sans(222, 158, d["delta"][0], 13.5, SOFT) + sans(222, 178, d["delta"][1], 13.5, MUT)
    for j, ln in enumerate(wrap_text(d["problem"], 50)[:3]):
        body += sans(24, 216 + j * 20, ln, 14, TX)
    y = 216 + len(wrap_text(d["problem"], 50)[:3]) * 20 + 10
    if d["insight"]:
        for j, ln in enumerate(wrap_text(d["insight"], 58)[:2]):
            body += serif(24, y + 8 + j * 19, ("↳ " if j == 0 else "   ") + ln, 13.5, SOFT, italic=True)
    if d["rail"]:
        ry = H - 84
        x0, x1 = 44, W - 44
        step = (x1 - x0) / 3
        body += f'<line x1="{x0}" y1="{ry}" x2="{x1}" y2="{ry}" stroke="{LINE}" stroke-width="2"/><line x1="{x0}" y1="{ry}" x2="{x0 + step * (d["reached"] - 1)}" y2="{ry}" stroke="{MINT}" stroke-width="2"/>'
        for k, lab in enumerate(d["rail"]):
            cx = x0 + k * step
            on = k < d["reached"]
            body += f'<circle cx="{cx}" cy="{ry}" r="6" fill="{MINT if on else SURF}" stroke="{MINT if on else MUT}" stroke-width="2"/>' + mono(cx, ry + 22, lab, 9.5, TX if on else MUT, "middle", .5)
    if not d["rail"] and H >= 400:
        rnd = random.Random(2)
        for k in range(16):
            bh = 20 + int(52 * math.exp(-((k - 7.5) / 4.2) ** 2)) + rnd.randint(0, 12)
            body += f'<rect x="{24 + k * 24}" y="{H - 62 - bh}" width="18" height="{bh}" rx="3" fill="{SKY}" opacity=".55">{A("opacity", [.25, .8, .25], dur=3, begin=k * .15)}</rect>'
        body += mono(24, H - 56 + 4, "illustration: a distribution, the first thing EDA looks at", 10, MUT)
    x = 24
    for t in d["tags"]:
        s, tw = chip(x, H - 42, t, SKY if not d["rail"] else MUT, 10.5, 22, fill=False)
        body += s
        x += tw + 6
    S(f"build-{d['key']}.svg", svg(W, H, body, f"{d['title']}: {d['big']}. {' '.join(d['delta'])}. {d['problem']}", r=18))


def sahi():
    W, H = 880, 440
    body = pulse(56, 50, AMB, 4.5, 1.8) + mono(72, 55, "NOW BUILDING  ·  IN PROGRESS", 11.5, AMB, ls=2.5)
    body += serif(54, 128, "Sahi Daam", 66, TX) + serif(56, 168, "Is this listing overpriced?", 24, OR, italic=True)
    for j, ln in enumerate(wrap_text("A fair-price detector for Pakistani house listings from Zameen.com. A model predicts what each listing should cost, and the gap between that prediction and the asking price becomes the product.", 54)):
        body += sans(56, 208 + j * 24, ln, 15, SOFT)
    x = 56
    for t in ["Python", "scikit-learn", "XGBoost", "Streamlit"]:
        s, w = chip(x, 322, t, MUT, 11, 24, fill=False)
        body += s
        x += w + 8
    body += serif(56, 378, "Flags mean “priced above similar listings”, never “scam”.", 14, MUT, italic=True)
    # scatter illustration
    px, py, pw, ph = 520, 56, 320, 250
    body += f'<line x1="{px}" y1="{py + ph}" x2="{px + pw}" y2="{py + ph}" stroke="{LINE}"/><line x1="{px}" y1="{py}" x2="{px}" y2="{py + ph}" stroke="{LINE}"/>'
    body += f'<line x1="{px}" y1="{py + ph}" x2="{px + pw}" y2="{py}" stroke="{MUT}" stroke-dasharray="4 5"/>'
    rnd = random.Random(5)
    pts = []
    for k in range(34):
        t = rnd.uniform(.06, .94)
        pts.append((t, t + rnd.uniform(-.09, .09), None))
    pts += [(.30, .62, OR), (.56, .90, OR), (.72, .93, OR), (.52, .20, MINT), (.80, .44, MINT), (.38, .06, MINT)]
    for k, (a, b, col) in enumerate(pts):
        cx, cy = px + a * pw, py + ph - max(.02, min(.98, b)) * ph
        c = col or MUT
        r = 5 if col else 3.5
        body += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{c}" opacity="0">{A("opacity", [0, 1, 1, 0], [0, .04, .95, 1], 10, .2 + k * .06)}</circle>'
        if col:
            body += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 4}" stroke="{col}" stroke-width="1.5" opacity="0">{A("opacity", [0, 0, .9, 0], [0, .35, .5, 1], 4, k * .3)}</circle>'
    body += mono(px + pw, py + ph + 20, "model's predicted price →", 10.5, MUT, "end") + mono(px, py - 12, "asking price ↑", 10.5, MUT)
    body += f'<circle cx="{px + 8}" cy="{py + ph + 44}" r="4.5" fill="{OR}"/>' + mono(px + 20, py + ph + 48, "priced above similar", 10.5, SOFT) + f'<circle cx="{px + 176}" cy="{py + ph + 44}" r="4.5" fill="{MINT}"/>' + mono(px + 188, py + ph + 48, "possible bargain", 10.5, SOFT)
    body += mono(px + pw, py - 12, "illustration of the idea", 10, MUT, "end")
    # plan rail
    ry = 440
    phases = ["COLLECT", "CLEAN", "EXPLORE", "MODEL", "INVESTIGATE", "SHIP"]
    body += mono(32, ry - 26, "THE 6-WEEK PLAN", 10.5, MUT, ls=2.5) + f'<line x1="70" y1="{ry}" x2="{W - 70}" y2="{ry}" stroke="{LINE}" stroke-width="2"/>'
    for k, p in enumerate(phases):
        cx = 70 + k * (W - 140) / 5
        body += f'<circle cx="{cx}" cy="{ry}" r="6" fill="{SURF}" stroke="{AMB if k == 0 else MUT}" stroke-width="2"/>' + mono(cx, ry + 22, p, 10, TX if k == 0 else MUT, "middle", 1)
    body += f'<line x1="{W - 70}" y1="{ry - 26}" x2="{W - 70}" y2="{ry - 26}"/>' + mono(W - 32, ry - 26, "REPO IS LIVE", 10.5, MINT, "end", 2)
    S("sahi.svg", svg(W, H + 34, body, "Sahi Daam, the fair-price detector: now building. Predicts fair prices for Pakistani house listings from Zameen.com and flags listings priced above similar ones.", r=22, grid=True))


# ═════════════════════════════ CONCEPT LAB ═════════════════════════════
def divspace():
    W, H, T = 880, 380, 10.0
    body = mono(48, 52, "CONCEPT  ·  NOT BUILT", 11.5, VIO, ls=3) + serif(46, 122, "Div Space", 60, TX) + serif(48, 160, "A <div> for the real world.", 22, VIO, italic=True)
    for j, ln in enumerate(wrap_text("In HTML, a div is a container. What if a physical one existed? Stick a chip anywhere, on a floor, on a group, anywhere, and a temporary room appears. Work inside it, pick things up, do anything. Remove the chip and the room is gone, and it is always one chip away.", 50)):
        body += sans(48, 204 + j * 24, ln, 15, SOFT)
    cx, fy = 670, 300
    body += f'<line x1="500" y1="{fy}" x2="840" y2="{fy}" stroke="{MUT}" stroke-width="2"/>'
    room_kt = [0, .12, .26, .66, .78, 1]
    items = f'<circle cx="-60" cy="-26" r="14" fill="{OR}"/><rect x="-14" y="-52" width="34" height="34" rx="4" fill="{SKY}"/><path d="M50 -10 L74 -10 L62 -44Z" fill="{MINT}"/>'
    body += (f'<g transform="translate({cx} {fy})"><g>{AT("scale", ["0 0", "0 0", "1 1", "1 1", "0 0", "0 0"], room_kt, T)}'
             f'<rect x="-130" y="-190" width="260" height="190" rx="6" fill="{VIO}" fill-opacity=".08" stroke="{VIO}" stroke-width="2" stroke-dasharray="7 6"/>'
             + mono(-118, -168, "<div>", 12, VIO) + f'<g>{AT("translate", ["0 0", "0 -6", "0 0"], dur=2.4)}{items}</g></g></g>')
    drop = [-170, -170, 0, 0, -170, -170]
    body += (f'<g transform="translate({cx} {fy})"><g>{AT("translate", [f"0 {v}" for v in drop], [0, .05, .12, .66, .74, 1], T)}'
             f'<rect x="-15" y="-9" width="30" height="9" rx="3" fill="{AMB}" filter="url(#glow)"/></g></g>')
    for txt, t0, t1 in [("1 · stick a chip anywhere", 0.6, 2.6), ("2 · a temporary room appears", 2.6, 6.3), ("3 · remove the chip, the room is gone", 6.6, 9.4)]:
        v, k = window(t0, t1, T, .25)
        body += f'<g opacity="0">{A("opacity", v, k, T)}' + mono(cx, fy + 34, txt, 12, SOFT, "middle", 1) + "</g>"
    body += mono(cx, fy + 62, "the room is always one chip away", 10.5, MUT, "middle", 1.5)
    S("divspace.svg", svg(W, H, body, "Div Space concept: a chip placed anywhere creates a temporary room, like an HTML div for the real world. Remove the chip and the room is gone.", r=22, grid=True))


def ai_card(i, key, title, desc, stack):
    W, H = 430, 214
    col = VIO
    body = f'<rect x="24" y="24" width="214" height="24" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".6"/>' + mono(131, 40, "MY CONCEPT · BUILT WITH AI", 10, col, "middle", 1)
    body += serif(24, 92, title, 28, TX)
    for j, ln in enumerate(wrap_text(desc, 52)[:2]):
        body += sans(24, 118 + j * 20, ln, 14, SOFT)
    for j, ln in enumerate(wrap_text(stack, 52)[:2]):
        body += mono(24, 166 + j * 16, ln, 11, col)
    body += mono(24, H - 14, "stack shown for transparency, not as my skills", 10, MUT)
    S(f"ai-{key}.svg", svg(W, H, body, f"{title}: my concept, built with AI. {stack}", r=18))


# ═════════════════════════════ SKILLS / JOURNEY ═════════════════════════════
def skills():
    W, H, pw = 880, 482, 430
    body = ""
    for pi, (title, (items, col)) in enumerate(SKILLS.items()):
        x = pi * (pw + 20)
        body += f'<g transform="translate({x} 0)"><rect x=".5" y=".5" width="{pw - 1}" height="410" rx="18" fill="{SURF}" stroke="{LINE}"/>' + serif(24, 50, title, 26, col)
        body += f'<line x1="24" y1="66" x2="{pw - 24}" y2="66" stroke="{LINE}"/>'
        for r, (name, lv) in enumerate(items):
            y = 98 + r * 34
            body += sans(24, y, name, 14.5, TX, weight=500)
            for p in range(3):
                on = p < lv
                body += f'<rect x="{pw - 24 - 3 * 26 + p * 26}" y="{y - 10}" width="22" height="8" rx="4" fill="{col if on else LINE}" opacity="{1 if on else .8}"/>'
        body += "</g>"
    body += f'<rect x=".5" y="426.5" width="{W - 1}" height="54" rx="14" fill="{SURF}" stroke="{LINE}"/>'
    for x, n, lab in [(32, 3, "COMFORTABLE"), (230, 2, "WORKING"), (390, 1, "LEARNING")]:
        for p in range(3):
            body += f'<rect x="{x + p * 14}" y="448" width="11" height="8" rx="4" fill="{MUT if p < n else LINE}"/>'
        body += mono(x + 52, 457, lab, 11, SOFT, ls=1.5)
    body += mono(W - 32, 457, "conservative on purpose", 11, MUT, "end", 1)
    S("skills.svg", svg(W, H, body, "Skills with honest levels. AI/ML: Python, scikit-learn, NumPy, Matplotlib, Streamlit working; pandas, NLP, FastAPI and Docker learning. Web: HTML and CSS comfortable.", frame=False))


def journey():
    W, H = 880, 386
    ym = 200
    main = [(60, "AUG 2023", "init:", "html·css·js"), (160, "2024 – MID 25", "feat:", "react + motion"), (380, "FEB 2026", "feat:", "python"),
            (490, "JUN 2026", "feat:", "machine learning"), (600, "NOW", "HEAD:", "nlp · docker")]
    body = mono(32, 40, "GIT LOG OF MY LEARNING", 11, OR, ls=3) + mono(W - 32, 40, "solid = done  ·  dashed = planned", 10.5, MUT, "end", 1)
    body += f'<line x1="60" y1="{ym}" x2="600" y2="{ym}" stroke="{OR}" stroke-width="3"/>'
    sy = ym - 78
    body += f'<path d="M160 {ym} C200 {ym}, 215 {sy}, 255 {sy} H290 C330 {sy}, 345 {ym}, 380 {ym}" stroke="{ROSE}" stroke-width="3"/><circle cx="272" cy="{sy}" r="7" fill="{SURF}" stroke="{ROSE}" stroke-width="3"/>'
    body += mono(272, sy - 20, "AUG – DEC 2025", 10.5, MUT, "middle", 1) + sans(272, sy + 28, "mobile + unity", 12.5, TX, "middle") + sans(272, sy + 45, "(side branch)", 12, MUT, "middle")
    gx = 820
    for name, dy, sub in [("deep-learning", -92, "ann · cnn · rnn (later)"), ("rag", 92, "retrieval + llm apps (later)")]:
        yy, ex = ym + dy, 725
        body += f'<path d="M600 {ym} C650 {ym}, 668 {yy}, {ex - 8} {yy}" stroke="{VIO}" stroke-width="3" stroke-dasharray="7 7"/><circle cx="{ex}" cy="{yy}" r="7" fill="{SURF}" stroke="{VIO}" stroke-width="3" stroke-dasharray="3 3"/>'
        body += mono(ex, yy + (-20 if dy < 0 else 30), f"feature/{name}", 11.5, VIO, "middle") + sans(ex, yy + (-38 if dy < 0 else 48), sub, 12, MUT, "middle")
        body += f'<path d="M{ex + 8} {yy} C770 {yy}, {gx} {ym + (-50 if dy < 0 else 50)}, {gx} {ym + (-10 if dy < 0 else 10)}" stroke="{VIO}" stroke-width="2" stroke-dasharray="5 6" opacity=".8"/>'
    body += f'<g>{A("opacity", [1, .35, 1], dur=1.8)}<circle cx="600" cy="{ym}" r="13" fill="{OR}" opacity=".3"/></g><circle cx="600" cy="{ym}" r="8" fill="{OR}"/>'
    for i, (x, date, kind, msg) in enumerate(main):
        if i < 4:
            body += f'<circle cx="{x}" cy="{ym}" r="7" fill="{SURF}" stroke="{OR}" stroke-width="3"/>'
        body += mono(x, ym + 34, date, 10.5, MUT, "middle", 1) + mono(x, ym + 54, kind, 11, OR if i < 4 else TX, "middle") + mono(x, ym + 72, msg, 11, TX, "middle")
    body += f'<g>{AT("translate", ["0 0", "0 -4", "0 0"], dur=1.4)}<rect x="570" y="{ym - 56}" width="60" height="22" rx="11" fill="{OR}"/>' + mono(600, ym - 41, "HEAD", 11, BG, "middle", 2) + "</g>"
    body += f'<circle cx="{gx}" cy="{ym}" r="10" fill="{AMB}" filter="url(#glow)"/>' + serif(gx, ym + 40, "AI Engineer", 20, AMB, "middle", True) + mono(gx, ym + 60, "the goal", 10.5, MUT, "middle", 1.5)
    body += mono(32, H - 26, "A public roadmap keeps the next step in sight.", 12, MUT)
    S("journey.svg", svg(W, H, body, "Git-style journey: html, css, js in Aug 2023; react; a mobile and Unity side branch; Python in Feb 2026; machine learning in Jun 2026; now NLP and Docker; planned branches for deep learning and RAG leading to AI Engineer.", r=22))


def offclock():
    W, H = 880, 112
    cols = [("Tekken", "Kazuya main. Movement, timing, execution.", ROSE), ("Games", "Free Fire, Clash of Clans, Clash Royale.", AMB), ("Anime & movies", "High-energy action and darker stories.", SKY)]
    body = ""
    for i, (t, d, c) in enumerate(cols):
        x = 32 + i * 288
        if i:
            body += f'<line x1="{x - 16}" y1="26" x2="{x - 16}" y2="{H - 26}" stroke="{LINE}"/>'
        body += f'<circle cx="{x + 5}" cy="36" r="4.5" fill="{c}"/>' + serif(x + 18, 42, t, 20, TX)
        for j, ln in enumerate(wrap_text(d, 34)[:2]):
            body += sans(x, 68 + j * 19, ln, 13.5, SOFT)
    S("offclock.svg", svg(W, H, body, "Off the clock: Tekken with Kazuya as my main, games, anime and movies"))


# ═════════════════════════════ ARENA / FOOTER ═════════════════════════════
def arena_button(file, label, beats, col, icon):
    W, H = 280, 104
    body = f'<g transform="translate(24 28) scale(.62)">{icon}</g>' + serif(92, 50, label, 28, TX) + mono(92, 72, f"beats {beats}", 11.5, col, ls=1)
    body += f'<g>{AT("translate", ["0 0", "5 0", "0 0"], dur=1.6)}' + mono(W - 22, 88, "play →", 11.5, OR, "end", 1) + "</g>" + f'<rect x="0" y="0" width="4" height="{H}" fill="{col}"/>'
    S(file, svg(W, H, body, f"{label}: beats {beats.lower()}. Click to play a round.", r=14))


def arena_icons():
    star = " ".join(f"{39 + (36 if k % 2 == 0 else 15) * math.cos(math.radians(36 * k - 90)):.1f},{39 + (36 if k % 2 == 0 else 15) * math.sin(math.radians(36 * k - 90)):.1f}" for k in range(10))
    return (f'<polygon points="{star}" fill="{ROSE}"/>',
            f'<path d="M12 28 A28 28 0 0 1 62 24" stroke="{AMB}" stroke-width="7" stroke-linecap="round"/><path d="M66 50 A28 28 0 0 1 16 54" stroke="{AMB}" stroke-width="7" stroke-linecap="round"/><path d="M52 12 L64 26 L46 30Z" fill="{AMB}"/><path d="M26 66 L14 52 L32 48Z" fill="{AMB}"/>',
            f'<path d="M39 4 L70 16 V40 C70 58 56 70 39 76 C22 70 8 58 8 40 V16 Z" fill="{SKY}" fill-opacity=".25" stroke="{SKY}" stroke-width="6" stroke-linejoin="round"/>')


def footer():
    W, H = 880, 140
    body = serif(W / 2, 62, "Never stop because life is not end yet.", 30, TX, "middle", True) + mono(W / 2, 96, "ZAIN ALI  ·  ISLAMABAD  ·  I LEARN BY BUILDING", 11.5, MUT, "middle", 3)
    body += tick(W, H - 1, OR, 7)
    S("footer.svg", svg(W, H, body, "Never stop because life is not end yet. Zain Ali, Islamabad, I learn by building.", r=22))


# ═════════════════════════════ README ═════════════════════════════
def img(f, alt, w="100%"):
    return '<img src="assets/%s" width="%s" alt="%s" />' % (f, w, alt)


def grp(*items):
    return '<p align="center">\n' + "\n".join(items) + "\n</p>\n"


def trow(k, v):
    return "<tr><td><b>%s</b></td><td>%s</td></tr>" % (k, v)


def table(rows):
    return "<table>\n" + "\n".join(trow(k, v) for k, v in rows) + "\n</table>"


def readme():
    fu = lambda m: PROFILE_REPO + "/issues/new?title=fight%7C" + m + "&body=Just+press+%22Submit+new+issue%22.+Don%27t+change+the+title%3A+the+arcade+bot+plays+your+round+and+replies+here."
    cards = "\n".join('<a href="%s/%s">%s</a>' % (ME, d["repo"], img("build-%s.svg" % d["key"], "%s: %s. %s" % (d["title"], d["big"], d["problem"]), "49.5%")) for d in BUILDS)
    ai = "\n".join(img("ai-%s.svg" % k, "%s: my concept, built with AI" % t, "49.5%") for k, t, *_ in AI_BUILT)
    glance = table([("Name", "Zain Ali (online: Malik Zain)"), ("Based in", "Islamabad, Pakistan"), ("Studying", "BS Computer Science, Riphah International University"),
                    ("Working as", "AI/ML Intern, FlyRank AI Internship Program (since mid-June 2026)"), ("Before", "Python internship at HexSoftwares"),
                    ("Freelance", "Responsive landing pages (Fiverr)"), ("Focus now", "Going deeper into ML and NLP"),
                    ("Later", "Deep learning (ANN, CNN, RNN) and RAG, inshallah"), ("Goal", "AI Engineer"),
                    ("Method", "I learn by building, not by theory"), ("Off the clock", "Tekken (Kazuya main), games, anime and movies")])
    nlp = table([("Learn deeply", "Text representations (TF-IDF vs embeddings), evaluation beyond accuracy (precision, recall, error analysis), reading model weights"),
                 ("Understand lightly", "How transformer models work"), ("Skip for now", "Training big models from scratch (no GPU, so Colab if ever needed)"),
                 ("Checkpoint", "A grammar and punctuation error explainer: finds mistakes and says why"),
                 ("If I skip this", "Deep learning and RAG both build on text representations. Skipping means copying code I can't debug."),
                 ("Next single step", "Start the grammar and punctuation explainer: collect examples of mistakes and the rule behind each")])
    dl = table([("Learn deeply", "ANN basics and backpropagation intuition, CNNs for images, RNNs for sequences"), ("Understand lightly", "Transformers and attention"),
                ("Skip for now", "Custom GPU code, training large models from scratch"),
                ("Checkpoint", "A small CNN on an image dataset and a small RNN on text, each explained in my own words"),
                ("If I skip this", "I'd stay a classic-ML person who can't explain why modern models work.")])
    rag = table([("Learn deeply", "Embeddings, chunking, vector search, and how to evaluate answers"), ("Understand lightly", "Agent frameworks"),
                 ("Skip for now", "Training LLMs"), ("Checkpoint", "A small RAG app over documents I choose, with a written evaluation"),
                 ("If I skip this", "I'd be able to classify text but not build the retrieval apps people ask for today.")])
    done = ("<table>\n<tr><th>Stage</th><th>Solid</th><th>Still shaky</th></tr>\n"
            "<tr><td>HTML · CSS · JS</td><td>HTML, CSS, Tailwind basics; I love JavaScript</td><td>Advanced JavaScript is rusty</td></tr>\n"
            "<tr><td>React basics</td><td>I can build sites</td><td>The concepts underneath aren't deep yet</td></tr>\n"
            "<tr><td>Python</td><td>Python since Feb 2026, NumPy, Matplotlib</td><td>pandas is partial</td></tr>\n"
            "<tr><td>ML fundamentals</td><td>scikit-learn, Pipelines, Logistic Regression, Random Forest, Gradient Boosting</td><td>Evaluation depth, which is what the NLP stage trains</td></tr>\n"
            "<tr><td>Deployment</td><td>FastAPI + Docker, done once in the resume classifier repo; Streamlit apps</td><td>Only done once so far</td></tr>\n</table>")
    plan = ("<table>\n<tr><th>Week</th><th>Phase</th><th>Output</th></tr>\n<tr><td>1</td><td>Set up and collect data</td><td>raw listings CSV</td></tr>\n"
            "<tr><td>2</td><td>Clean the data</td><td>clean listings CSV and a cleaning log</td></tr>\n<tr><td>3</td><td>Explore and engineer features</td><td>EDA notebook</td></tr>\n"
            "<tr><td>4</td><td>Baseline and models</td><td>results table (baseline vs models)</td></tr>\n<tr><td>5</td><td>Investigate errors and flag deals</td><td>error analysis, overpriced and bargain lists</td></tr>\n"
            "<tr><td>6</td><td>Build the app and write the README</td><td>live Streamlit app, finished repo</td></tr>\n</table>")
    return f"""<!--
  ZAIN ALI — GitHub profile README ("Workbench")
  Generated by build_assets.py. Edit the DATA blocks there and re-run.
  Live parts (contribution log, play-a-round scoreboard) are redrawn by GitHub Actions.
-->

<a id="top"></a>

{img("hero.svg", "Zain Ali. I learn by building, not by theory. AI/ML intern in Islamabad.")}

{img("numbers.svg", "74.4 percent resume classifier, about 98 percent fake news classifier, 0.86 churn ROC-AUC, 3 projects deployed.")}

<p align="center"><sub>All numbers are from my own repos. Each build below says what they mean and where they fall short.</sub></p>

<p align="center"><b>Who's reading?</b> <sub>&nbsp;pick one and I'll take you to the right place</sub></p>

<p align="center">
<a href="#builds"><img src="assets/role-hire.svg" width="32.6%" alt="Hiring? Read the builds." /></a>
<a href="#web"><img src="assets/role-client.svg" width="32.6%" alt="Need a website? See the web work." /></a>
<a href="#play"><img src="assets/role-play.svg" width="32.6%" alt="Just curious? Play a round against me." /></a>
</p>

<!-- ───────── 01 · ABOUT ───────── -->
<a id="about"></a>
{img("h-about.svg", "01 About: who I am, and how I work")}

### Hi, I'm Zain. 👋

I'm a BS Computer Science student in Islamabad and an AI/ML intern at FlyRank. I started coding in August 2023 with HTML, CSS and JavaScript, spent a couple of years on frontend and animation, tried mobile and game development, and found my direction in 2026: Python in February, machine learning in June. Since then everything I build is ML, NLP and the engineering around it.

**My method is simple: I learn by building, not by theory.** No offense to theory, it just isn't how I learn. I pick a real problem, build the smallest version that works, measure it honestly, then go looking for where it breaks. That's why my fake-news classifier comes with an investigation into a "Reuters" shortcut instead of a victory lap around 98% accuracy.

I only want to build things that mean something and solve real problems, and the next ones are going to be bigger. Right now that's **Sahi Daam**, a fair-price detector for Pakistani house listings. After that I'm going deeper into ML and NLP, and later (inshallah) deep learning (ANN, CNN, RNN) and RAG, on the way to becoming an AI Engineer.

I also build with AI, openly. Concepts I design and use AI to code (anything TypeScript here, for example) sit in their own labelled section, and tutorial-guided work is marked as tutorial-guided.

{img("principles.svg", "How I work: build first, real problems, honest labels.")}

<details>
<summary><b>At a glance</b></summary>
<br />

{glance}

</details>

<!-- ───────── 02 · BUILDS ───────── -->
<a id="builds"></a>
{img("h-builds.svg", "02 Builds: what I have built, with real numbers")}

{grp(cards)}
<p align="center"><sub>Same order as my pinned repos. Click a card to open the repo. &nbsp;·&nbsp; <a href="{ME}?tab=repositories"><b>All repositories →</b></a><br />More ML work lives in other repos: a Titanic survival app (Streamlit, 82.68% with Random Forest and Gradient Boosting) and my FlyRank internship notebooks.</sub></p>

<!-- ───────── 03 · NOW BUILDING ───────── -->
<a id="now"></a>
{img("h-now.svg", "03 Now building: Sahi Daam")}

<p align="center"><a href="{ME}/sahi-daam-fair-price-detector">{img("sahi.svg", "Sahi Daam, the fair-price detector, now building.")}</a></p>

<details>
<summary><b>The plan behind Sahi Daam</b> (six weeks, in order)</summary>
<br />

The idea: <b>the model's mistakes become the product.</b> Most beginner projects stop at "predict the price". Sahi Daam goes one step further and uses the errors to find deals.

{plan}

<br />

I'm collecting house listings from Zameen.com, so cleaning messy units (marla, kanal, lakh, crore) is the first real test. I check the site's rules before collecting anything, keep requests polite, and never store personal data. The final repo will carry a results table against a simple baseline, an error analysis ("where the model fails"), and a Streamlit app.

</details>

<!-- ───────── 04 · CONCEPT LAB ───────── -->
<a id="lab"></a>
{img("h-lab.svg", "04 Concept lab: ideas I design, some built with AI")}

{img("divspace.svg", "Div Space concept: stick a chip anywhere and a temporary room appears, like an HTML div for the real world.")}

<p align="center"><b>Built with AI, from my concepts</b></p>

{grp(ai)}
<p align="center"><sub>I come up with the concept and the problem; AI writes most of the code. Anything TypeScript on my profile falls in this bucket. More ideas on my list: a bill splitter and a monthly budget tracker.</sub></p>

<!-- ───────── 05 · STACK ───────── -->
<a id="stack"></a>
{img("h-stack.svg", "05 Stack: honest levels, nothing inflated")}
{img("skills.svg", "Skills with honest levels. AI/ML: Python, scikit-learn, NumPy, Matplotlib, Streamlit working. Web: HTML and CSS comfortable.")}

<p align="center"><sub>Not listed on purpose: tools I've only met in courses or built with AI help (for example NestJS, AWS, Kubernetes). They appear on the labelled AI-built cards instead.</sub></p>

<a id="web"></a>
<details>
<summary><b>Web work</b> (where I started: tutorial-guided, clones and practice)</summary>
<br />

<table>
<tr><th>Project</th><th>How it was made</th><th>Stack</th></tr>
<tr><td><a href="{ME}/Zylo">Zylo</a></td><td>Tutorial-guided</td><td>Node.js, Express, EJS, MySQL</td></tr>
<tr><td><a href="{ME}/Ochi-website-Clone">Ochi website clone</a></td><td>Clone</td><td>React, GSAP</td></tr>
<tr><td><a href="{ME}/Grid-ScrollAnimation-using-Lenis">Grid scroll animation</a></td><td>Practice</td><td>JavaScript, GSAP, Lenis</td></tr>
<tr><td><a href="{ME}/twogood_website_clone">Two Good website clone</a></td><td>Clone</td><td>HTML, CSS, JavaScript</td></tr>
<tr><td><a href="{ME}/Bubble-Game">Bubble Game</a></td><td>Practice</td><td>JavaScript, HTML, CSS</td></tr>
<tr><td><a href="{ME}/LMS">Library Management System</a></td><td>University project</td><td>Java, MySQL</td></tr>
</table>

I also freelance, building responsive landing pages (Fiverr).

</details>

<!-- ───────── 06 · JOURNEY ───────── -->
<a id="roadmap"></a>
{img("h-journey.svg", "06 Journey: where I've been, where I'm headed")}
{img("journey.svg", "Git-style journey from Aug 2023 to now, with planned branches for deep learning and RAG leading to AI Engineer.")}

<details open>
<summary><b>Now · NLP, going deeper</b></summary>
<br />

{nlp}

</details>

<details>
<summary><b>Later · Deep learning</b> (ANN, CNN, RNN)</summary>
<br />

{dl}

</details>

<details>
<summary><b>Later · RAG apps</b></summary>
<br />

{rag}

</details>

<details>
<summary><b>Already cleared</b> (what's solid, what's still shaky)</summary>
<br />

{done}

</details>

<!-- ───────── 07 · CONTRIBUTION LOG ───────── -->
<a id="log"></a>
{img("h-log.svg", "07 Contribution log: live from GitHub, every 6 hours")}
{img("stats.svg", "Live GitHub numbers: repositories, followers, stars, last 12 months, streaks, languages")}
{img("heatmap.svg", "Contribution heatmap for the last 12 months")}

<!-- ───────── 08 · PLAY ───────── -->
<a id="play"></a>
{img("h-play.svg", "08 Play a round: a game that runs on GitHub Actions")}

<!-- CHALLENGE-ZAIN:START -->
<p align="center"><b>Pick a move. A GitHub Action plays the round against me and updates the scoreboard.</b><br />
<sub>STRIKE beats THROW · THROW beats GUARD · GUARD beats STRIKE</sub></p>

<p align="center">
<a href="{fu("strike")}"><img src="assets/btn-strike.svg" width="32.6%" alt="Strike. Beats throw. Click to play." /></a>
<a href="{fu("throw")}"><img src="assets/btn-throw.svg" width="32.6%" alt="Throw. Beats guard. Click to play." /></a>
<a href="{fu("guard")}"><img src="assets/btn-guard.svg" width="32.6%" alt="Guard. Beats strike. Click to play." /></a>
</p>

<p align="center"><img src="assets/scoreboard.svg" width="100%" alt="Scoreboard: challengers versus Zain, with the latest rounds" /></p>
<!-- CHALLENGE-ZAIN:END -->

<details>
<summary><b>How does this work?</b></summary>
<br />

Clicking a move opens a pre-filled GitHub issue. Press <b>Submit new issue</b> (you need a GitHub account). A GitHub Action picks my move at random, decides the winner, comments the result on your issue, closes it, and redraws the scoreboard above. It can take a minute or two to refresh because GitHub caches images. Code: <a href="{PROFILE_REPO}/blob/main/.github/scripts/fight.py"><code>.github/scripts/fight.py</code></a>.

</details>

<!-- ───────── 09 · OFF THE CLOCK ───────── -->
{img("h-off.svg", "09 Off the clock: what I do when I'm not coding")}
{img("offclock.svg", "Off the clock: Tekken with Kazuya as my main, games, anime and movies.")}

<br />

<!-- ───────── CONNECT ───────── -->
<a id="connect"></a>
<p align="center"><b>Want to talk, collaborate or tell me my model is overfitting?</b></p>

<p align="center">
<a href="https://www.linkedin.com/in/malikzain555/"><img src="assets/btn-linkedin.svg" width="24%" alt="LinkedIn" /></a>
<a href="{ME}?tab=repositories"><img src="assets/btn-repos.svg" width="24%" alt="GitHub repositories" /></a>
<a href="https://zikakito.itch.io/"><img src="assets/btn-itch.svg" width="24%" alt="Games on itch.io" /></a>
</p>

{img("footer.svg", "Never stop because life is not end yet.")}

<p align="center"><a href="#top"><sub>⬆ back to top</sub></a></p>
"""


# ═════════════════════════════ BUILD ═════════════════════════════
if __name__ == "__main__":
    hero(); numbers(); principles(); sahi(); divspace(); skills(); journey(); offclock(); footer()
    role_tile("role-hire.svg", "RECRUITERS", "Hiring?", "Read the builds and the numbers.", OR)
    role_tile("role-client.svg", "CLIENTS", "Need a website?", "See the web work.", SKY)
    role_tile("role-play.svg", "EVERYONE ELSE", "Just curious?", "Play a round against me.", MINT)
    for f, i, t, w in [("h-about.svg", "01", "About", "who I am, and how I work"), ("h-builds.svg", "02", "Builds", "what I've built, with real numbers"),
                       ("h-now.svg", "03", "Now building", "Sahi Daam: what comes next"), ("h-lab.svg", "04", "Concept lab", "ideas I design, some built with AI"),
                       ("h-stack.svg", "05", "Stack", "honest levels, nothing inflated"), ("h-journey.svg", "06", "Journey", "where I've been, where I'm headed"),
                       ("h-log.svg", "07", "Contribution log", "live from GitHub, every 6 hours"), ("h-play.svg", "08", "Play a round", "a game that runs on GitHub Actions"),
                       ("h-off.svg", "09", "Off the clock", "what I do when I'm not coding")]:
        header(f, i, t, w)
    for f, lab, col in [("btn-linkedin.svg", "LinkedIn", SKY), ("btn-itch.svg", "itch.io", ROSE), ("btn-repos.svg", "All repos", OR)]:
        button(f, lab, col)
    for i, d in enumerate(BUILDS):
        row = BUILDS[(i // 2) * 2:(i // 2) * 2 + 2]
        build_card(i, d, 410 if any(r["rail"] or r["key"] == "eda" for r in row) else 304)
    for i, a in enumerate(AI_BUILT):
        ai_card(i, *a)
    s_i, t_i, g_i = arena_icons()
    arena_button("btn-strike.svg", "Strike", "THROW", ROSE, s_i)
    arena_button("btn-throw.svg", "Throw", "GUARD", AMB, t_i)
    arena_button("btn-guard.svg", "Guard", "STRIKE", SKY, g_i)
    stats.ROOT = __import__("pathlib").Path(HERE)
    if not (os.path.exists(os.path.join(OUT, "stats.svg")) and os.path.exists(os.path.join(OUT, "heatmap.svg"))):
        stats.write_all(None)
    sb = os.path.join(OUT, "scoreboard.svg")
    if not os.path.exists(sb):
        save(sb, fight.render_scoreboard(fight.DEFAULT))
    save(os.path.join(HERE, "README.md"), readme())
    print("Generated", len(os.listdir(OUT)), "assets + README.md")
