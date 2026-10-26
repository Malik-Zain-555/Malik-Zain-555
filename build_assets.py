#!/usr/bin/env python3
"""Zain Ali — "Arcade" profile asset generator.   python3 build_assets.py  ->  ./assets/*.svg
Edit the DATA lists, re-run, push. Live graphics (stats / heatmap / scoreboard) are placeholders here;
GitHub Actions redraws them with real data (see .github/workflows)."""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".github", "scripts"))
from arcade import *  # noqa: E402,F401,F403
import fight, stats  # noqa: E402

OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)
S = lambda name, content: save(os.path.join(OUT, name), content)


# ═════════════════════════════ HERO ═════════════════════════════
def hero():
    T, W, H = 13.0, 880, 470
    rnd = random.Random(11)
    rays = "".join(
        f'<polygon points="440,250 {440 + 900 * math.cos(a - .035):.0f},{250 + 900 * math.sin(a - .035):.0f} {440 + 900 * math.cos(a + .035):.0f},{250 + 900 * math.sin(a + .035):.0f}" fill="{GOLD}" fill-opacity=".05"/>'
        for a in [i * 2 * math.pi / 18 for i in range(18)])
    sun = f'<g>{AT("rotate", ["0 440 250", "360 440 250"], dur=120)}{rays}</g>'
    floor = f'<g stroke="{PUR}" stroke-opacity=".5">' + "".join(
        f'<line x1="{440 + i * 14}" y1="318" x2="{440 + i * 95}" y2="470"/>' for i in range(-12, 13)) + "</g>"
    floor += f'<line x1="0" y1="318" x2="{W}" y2="318" stroke="{PINK}" stroke-opacity=".7"/>'
    for k in range(6):
        sp = 'calcMode="spline" keyTimes="0;1" keySplines="0.6 0 0.9 0.5"'
        floor += (f'<line x1="0" x2="{W}" y1="318" y2="318" stroke="{CYA}" stroke-width="1.6">'
                  f'<animate attributeName="y1" values="318;470" dur="5.4s" begin="-{k * .9}s" repeatCount="indefinite" {sp}/>'
                  f'<animate attributeName="y2" values="318;470" dur="5.4s" begin="-{k * .9}s" repeatCount="indefinite" {sp}/>'
                  f'<animate attributeName="stroke-opacity" values="0;.8" dur="5.4s" begin="-{k * .9}s" repeatCount="indefinite"/></line>')
    embers = "".join(
        f'<circle cx="{rnd.randint(20, W - 20)}" cy="470" r="{rnd.choice([1.5, 2, 2.5])}" fill="{rnd.choice([GOLD, ORG, PINK])}">'
        f'<animate attributeName="cy" values="470;{rnd.randint(120, 260)}" dur="{rnd.uniform(4, 8):.1f}s" begin="-{rnd.uniform(0, 8):.1f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.9;0" dur="{rnd.uniform(4, 8):.1f}s" begin="-{rnd.uniform(0, 8):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(20))

    L, R = "40,34 392,34 380,62 28,62", "488,34 840,34 852,62 500,62"
    wid = [364, 364, 300, 300, 230, 230, 150, 150, 70, 70, 0, 0, 364]
    kts = [0, 3.9, 4.0, 5.1, 5.2, 6.3, 6.4, 7.5, 7.6, 9.0, 9.4, 12.8, 13.0]
    kk = [t / T for t in kts]
    hud = f"""
<polygon points="{L}" fill="#3a0f1c"/><g clip-path="url(#hpL)"><rect x="28" y="34" width="364" height="28" fill="url(#hot)"/><rect x="28" y="34" width="364" height="9" fill="#fff" fill-opacity=".25"/></g><polygon points="{L}" stroke="{WHT}" stroke-opacity=".85" stroke-width="2"/>
<polygon points="{R}" fill="#3a0f1c"/><g clip-path="url(#hpR)"><rect y="34" height="28" fill="url(#hot)" x="488" width="364">{A("width", wid, kk, T)}{A("x", [852 - w for w in wid], kk, T)}</rect></g><polygon points="{R}" stroke="{WHT}" stroke-opacity=".85" stroke-width="2"/>
{disp(36, 26, "ZAIN", 22, GOLD)}{disp(844, 26, "BUGS", 22, RED, "end")}
<polygon points="404,24 476,24 476,72 404,72" fill="#120B1E" stroke="{WHT}" stroke-width="2"/>{disp(440, 62, "99", 38, WHT, "middle")}
<circle cx="44" cy="78" r="5" fill="{GOLD}"/><circle cx="62" cy="78" r="5" stroke="{GOLD}" stroke-width="1.5"/><circle cx="836" cy="78" r="5" stroke="{GOLD}" stroke-width="1.5"/><circle cx="818" cy="78" r="5" stroke="{GOLD}" stroke-width="1.5"/>"""

    def announce(txt, size, fill, t0, t1, slam=False):
        v, k = window(t0, t1, T)
        inner = disp(0, size * .35, txt, size, fill, "middle", 'stroke="#000" stroke-width="7" paint-order="stroke"')
        if slam:
            inner = f'<g>{AT("scale", [2.8, 2.8, 1, 1], [0, t0 / T, (t0 + .2) / T, 1], T)}{inner}</g>'
        return f'<g transform="translate(440 215)" opacity="0">{A("opacity", v, k, T)}{inner}</g>'

    ann = announce("ROUND 1", 92, "url(#gold)", .3, 1.8, True) + announce("FIGHT!", 130, "url(#hot)", 1.9, 3.4, True)
    for i, r in enumerate(["BSCS STUDENT", "WEB DEVELOPER", "AI / ML LEARNER", "KAZUYA MAIN"]):
        ann += announce(r, 46, WHT, 3.5 + i * 1.45, 4.95 + i * 1.45)
    ann += announce("K.O.", 170, RED, 9.5, 11.0, True) + announce("PLAYER 1 WINS", 62, "url(#gold)", 11.0, 12.8)

    combo = ""
    for txt, t0, t1 in [("2 HITS", 4.0, 4.9), ("4 HITS", 5.2, 6.1), ("6 HITS", 6.4, 7.3), ("8 HITS!", 7.6, 8.9)]:
        v, k = window(t0, t1, T, .06)
        combo += (f'<g transform="translate(40 150)" opacity="0">{A("opacity", v, k, T)}<g>{AT("scale", [1.5, 1.5, 1, 1], [0, t0 / T, (t0 + .12) / T, 1], T)}'
                  + disp(0, 0, txt, 52, "url(#gold)", "start", 'stroke="#000" stroke-width="6" paint-order="stroke"') + "</g></g>")
    hits = [4.0, 5.2, 6.4, 7.6, 9.2]
    fv, fk = [0], [0]
    for t in hits:
        fk += [(t - .02) / T, t / T, (t + .16) / T]
        fv += [0, .4, 0]
    flash = f'<rect width="{W}" height="{H}" fill="{WHT}" opacity="0">{A("opacity", fv + [0], fk + [1], T)}</rect>'

    name = f"""
<g transform="translate(-5 0)" opacity=".8">{AT("translate", ["0 0", "0 0", "-7 1", "5 -1", "0 0", "0 0"], [0, .38, .382, .386, .39, 1], T, extra='calcMode="discrete"')}{disp(440, 396, "ZAIN ALI", 118, CYA, "middle")}</g>
<g transform="translate(5 0)" opacity=".8">{AT("translate", ["0 0", "0 0", "7 -1", "-5 1", "0 0", "0 0"], [0, .38, .382, .386, .39, 1], T, extra='calcMode="discrete"')}{disp(440, 396, "ZAIN ALI", 118, PUR, "middle")}</g>
{disp(440, 396, "ZAIN ALI", 118, "url(#gold)", "middle", 'stroke="#000" stroke-width="5" paint-order="stroke"')}
{mono(440, 436, "BSCS  ·  FULL-STACK WEB  ·  AI / ML  ·  KAZUYA MAIN", 14, SOFT, "middle", 4)}"""
    body = f"""{sun}{floor}{embers}{hud}{combo}{ann}{name}{flash}<rect y="{H - 10}" width="{W}" height="10" fill="url(#haz)" opacity=".9"/>"""
    defs = f'<clipPath id="hpL"><polygon points="{L}"/></clipPath><clipPath id="hpR"><polygon points="{R}"/></clipPath>'
    S("hero.svg", svg(W, H, body, "Zain Ali. BSCS student, web developer, AI/ML learner, Kazuya main. A fighting-game intro.", defs, c=22,
                      glows=[(120, 250, 240, PUR, .38), (780, 250, 240, RED, .32)]))


# ═════════════════════════════ BANNERS / BUTTONS ═════════════════════════════
def quote():
    W, H = 880, 200
    body = '<rect width="12" height="200" fill="url(#haz)"/>'
    body += mono(44, 40, "// MOTTO", 13, GOLD, ls=5)
    body += disp(44, 100, "NEVER STOP BECAUSE", 46, "url(#gold)", extra='stroke="#000" stroke-width="5" paint-order="stroke"')
    body += disp(44, 152, "LIFE IS NOT END YET.", 46, "url(#hot)", extra='stroke="#000" stroke-width="5" paint-order="stroke"')
    body += sans(W - 30, 112, "I don't need to know everything today.", 14.5, SOFT, "end")
    body += sans(W - 30, 134, "I need to keep learning, build honestly,", 14.5, SOFT, "end")
    body += sans(W - 30, 156, "and get a little better every project.", 14.5, SOFT, "end")
    body += sweep(W, H, dur=7)
    S("quote.svg", svg(W, H, body, "Never stop because life is not end yet", glows=[(60, 100, 140, RED, .22), (820, 160, 140, PUR, .2)]))


def button(file, label, col, w=210, h=54):
    P = f"14,0 {w},0 {w - 14},{h} 0,{h}"
    body = f"""<polygon points="{P}" fill="{PANEL}"/><polygon points="{P}" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="2"/>
<defs><linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="bp"><polygon points="{P}"/></clipPath></defs>
<g clip-path="url(#bp)"><rect x="-80" width="60" height="{h}" fill="url(#sh)" transform="skewX(-20)">{A("x", [-80, w + 40, w + 40], [0, .4, 1], 4.2)}</rect></g>
{disp(w / 2 - 8, h / 2 + 8, label, 24, WHT, "middle")}
<g>{blink(1)}{mono(w - 34, h / 2 + 5, "▶", 15, col, "middle")}</g>"""
    S(file, svg(w, h, body, label, frame=False))


def header(file, num, title, hint, col=GOLD):
    W, H = 880, 84
    body = f'<polygon points="0,0 118,0 96,{H} 0,{H}" fill="url(#hot)"/>'
    body += disp(50, 62, num, 54, INK, "middle")
    body += disp(142, 60, title.upper(), fit(title, 520, 46), "url(#gold)", extra='stroke="#000" stroke-width="5" paint-order="stroke"')
    body += mono(W - 28, 40, hint, 13, DIM, "end", 1.5)
    body += f'<rect x="{W - 250}" y="{H - 10}" width="250" height="10" fill="url(#haz)" opacity=".85"/>' + sweep(W, H - 7, dur=5)
    S(file, svg(W, H, body, f"{num} {title}", glows=[(780, 20, 120, col, .2)]))


# ═════════════════════════════ CHARACTER SELECT ═════════════════════════════
def select_banner():
    W, H = 880, 86
    body = disp(W / 2, 52, "CHARACTER  SELECT", 46, "url(#gold)", "middle", 'stroke="#000" stroke-width="5" paint-order="stroke"')
    body += f'<g>{A("x", [0, -8, 0], dur=1)}' + disp(70, 54, "◀", 40, RED) + "</g>" + disp(W - 70, 54, "▶", 40, RED, "end")
    body += mono(W / 2, 76, "CLICK A PATH TO JUMP IN", 12, DIM, "middle", 5)
    S("select-banner.svg", svg(W, H, body, "Character select: choose your path", c=16, glows=[(440, 35, 160, RED, .2)]))


def select_tile(i, file, tag, title, sub, col, icon):
    W, H, T = 280, 200, 6.0
    v, k = window(i * 2, i * 2 + 2.2, T, .15)
    br = ""
    for (x, y, dx, dy) in [(10, 10, 1, 1), (W - 10, 10, -1, 1), (10, H - 10, 1, -1), (W - 10, H - 10, -1, -1)]:
        br += f'<path d="M{x} {y + 22 * dy} V{y} H{x + 22 * dx}" stroke="{GOLD}" stroke-width="4"/>'
    body = f'<g opacity="0">{A("opacity", v, k, T)}{br}</g>'
    body += mono(24, 38, tag, 12, col, ls=4) + f'<g transform="translate(190 34)">{icon}</g>'
    body += disp(24, 112, title, 40, WHT, extra='stroke="#000" stroke-width="5" paint-order="stroke"')
    body += mono(24, 140, sub, 12.5, SOFT, ls=1)
    body += f'<g>{blink(1.1)}{mono(24, 178, "▶ PRESS START", 14, GOLD, ls=3)}</g>'
    S(file, svg(W, H, body, f"{title}: {sub}", c=18, border=col, glows=[(230, 40, 100, col, .3)]))


def icons():
    web = f'<rect width="70" height="52" rx="4" stroke="{CYA}" stroke-width="3"/><path d="M0 14H70" stroke="{CYA}" stroke-width="3"/><circle cx="8" cy="7" r="2.5" fill="{CYA}"/><circle cx="16" cy="7" r="2.5" fill="{CYA}"/><text x="35" y="42" text-anchor="middle" font-family="{MONO}" font-size="20" font-weight="700" fill="{CYA}">&lt;/&gt;</text>'
    nodes = [(8, 10), (8, 42), (35, 4), (35, 26), (35, 48), (62, 18), (62, 36)]
    lines = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 5), (3, 5), (3, 6), (4, 6), (2, 6), (4, 5)]
    ai = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{PUR}" stroke-opacity=".7" stroke-width="2"/>' for a, b in lines)
    ai += "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{PUR}">{A("opacity", [1, .4, 1], dur=2, begin=i * .3)}</circle>' for i, (x, y) in enumerate(nodes))
    game = f'<rect x="10" y="20" width="10" height="30" rx="2" fill="{GOLD}"/><rect y="30" x="0" width="30" height="10" rx="2" fill="{GOLD}"/><circle cx="48" cy="28" r="7" fill="{RED}"/><circle cx="62" cy="40" r="7" fill="{CYA}"/>'
    return web, ai, game


# ═════════════════════════════ PROFILE ═════════════════════════════
def profile():
    W, H = 880, 372
    hexpts = lambda r, cx=150, cy=186: " ".join(f"{cx + r * math.cos(math.radians(60 * i - 30)):.1f},{cy + r * math.sin(math.radians(60 * i - 30)):.1f}" for i in range(6))
    body = f'<polygon points="{hexpts(118)}" stroke="{PUR}" stroke-width="2" stroke-dasharray="6 8" opacity=".8"><animateTransform attributeName="transform" type="rotate" from="0 150 186" to="360 150 186" dur="30s" repeatCount="indefinite"/></polygon>'
    body += f'<polygon points="{hexpts(92)}" fill="{INK}" stroke="url(#hot)" stroke-width="5" filter="url(#glow)"/>'
    body += disp(150, 222, "ZA", 92, "url(#gold)", "middle", 'stroke="#000" stroke-width="5" paint-order="stroke"')
    body += mono(150, 322, "PLAYER 1", 14, GOLD, "middle", 6) + f'<g>{blink(1.4)}' + mono(150, 344, "READY", 12, LIME, "middle", 6) + "</g>"
    rows = [("NAME", "ZAIN ALI"), ("STYLE", "FULL-STACK WEB (JAVASCRIPT)"), ("LEARNING", "PYTHON · DATA · MACHINE LEARNING"),
            ("SCHOOL", "RIPHAH INTERNATIONAL UNIVERSITY"), ("ORIGIN", "PAKISTAN"), ("MAIN", "KAZUYA (TEKKEN)"), ("MOTTO", "NEVER STOP — LIFE IS NOT END YET")]
    y = 70
    for i, (lab, val) in enumerate(rows):
        op = A("opacity", [0, 1, 1, 0], [0, .06, .94, 1], 12, i * .35)
        body += f'<g opacity="0">{op}{mono(330, y, lab, 13, GOLD, ls=4)}{mono(470, y, val, 16, WHT)}<line x1="330" y1="{y + 12}" x2="852" y2="{y + 12}" stroke="{EDGE}"/></g>'
        y += 42
    body += sweep(W, H, dur=6)
    S("profile.svg", svg(W, H, body, "Player profile: Zain Ali, BSCS at Riphah International University, Pakistan. Main: Kazuya.", c=20, glows=[(150, 186, 150, PUR, .3), (800, 340, 160, RED, .15)]))


# ═════════════════════════════ MOVE LIST ═════════════════════════════
WEB = [("HTML", 3), ("CSS", 3), ("Tailwind CSS", 3), ("JavaScript", 3), ("React", 3), ("Node.js", 2), ("Express", 2), ("MongoDB", 2), ("MySQL", 2), ("EJS", 2), ("REST APIs", 2), ("JWT + bcrypt", 2)]
AIML = [("Python", 2), ("NumPy", 2), ("pandas", 2), ("Matplotlib", 2), ("scikit-learn", 2), ("Logistic Regression", 2), ("Random Forest", 2)]
SIDE = [("Java + JavaFX", 2), ("Git + GitHub", 2), ("Docker", 1), ("Linux", 1), ("Figma", 1), ("Flutter + Dart", 1), ("Unity + C#", 1)]


def movelist():
    W, H, pw = 880, 560, 280
    body = ""
    for pi, (title, items, col) in enumerate([("WEB", WEB, CYA), ("AI / ML", AIML, PUR), ("SIDE QUESTS", SIDE, GOLD)]):
        x = pi * (pw + 20)
        body += f'<g transform="translate({x} 0)"><polygon points="{poly(pw, 470, 14)}" fill="{PANEL}"/><polygon points="{poly(pw, 470, 14)}" fill="{col}" fill-opacity=".06" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>'
        body += disp(20, 44, title, 30, col) + f'<line x1="20" y1="58" x2="{pw - 20}" y2="58" stroke="{col}" stroke-opacity=".5"/>'
        for r, (name, lv) in enumerate(items):
            y = 92 + r * 34
            body += sans(20, y, name, 16, WHT, weight=600)
            for p in range(3):
                cx = pw - 70 + p * 20
                if p < lv:
                    body += f'<circle cx="{cx}" cy="{y - 5}" r="6.5" fill="{col}" opacity="0">{A("opacity", [0, 1, 1, 0], [0, .05, .95, 1], 10, r * .12 + p * .08)}</circle>'
                else:
                    body += f'<circle cx="{cx}" cy="{y - 5}" r="6" stroke="{col}" stroke-opacity=".45" stroke-width="1.5"/>'
        body += "</g>"
    ly = 520
    body += f'<polygon points="{poly(W, 56, 14)}" transform="translate(0 492)" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
    for x, filled, label in [(150, 3, "COMFORTABLE"), (370, 2, "LEVELLING UP"), (590, 1, "EXPLORING")]:
        for p in range(3):
            body += f'<circle cx="{x + p * 18}" cy="{ly}" r="6" ' + (f'fill="{GOLD}"/>' if p < filled else f'stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.5"/>')
        body += mono(x + 66, ly + 5, label, 13, SOFT, ls=2)
    S("movelist.svg", svg(W, H, body, "Move list: skills by level. Web, AI/ML, and side quests.", frame=False))


def radar():
    W, H = 430, 340
    axes = [("CURIOSITY", 10), ("FRONTEND", 7), ("JAVASCRIPT", 6), ("BACKEND", 5), ("PYTHON/ML", 4), ("CONSISTENCY", 6)]
    cx, cy, R = 215, 182, 100
    pt = lambda i, v: (cx + R * v / 10 * math.cos(math.radians(-90 + 60 * i)), cy + R * v / 10 * math.sin(math.radians(-90 + 60 * i)))
    body = disp(24, 44, "FIGHTER STATS", 28, "url(#gold)") + mono(W - 24, 42, "SELF-ASSESSED", 11.5, DIM, "end", 2)
    for ring in (2, 4, 6, 8, 10):
        body += f'<polygon points="{" ".join("%.1f,%.1f" % pt(i, ring) for i in range(6))}" stroke="{EDGE}" stroke-width="1.5"/>'
    for i in range(6):
        body += f'<line x1="{cx}" y1="{cy}" x2="{pt(i, 10)[0]:.1f}" y2="{pt(i, 10)[1]:.1f}" stroke="{EDGE}"/>'
    shape = " ".join("%.1f,%.1f" % (pt(i, v)[0] - cx, pt(i, v)[1] - cy) for i, (_, v) in enumerate(axes))
    body += (f'<g transform="translate({cx} {cy})"><g>{AT("scale", [0, 1, 1, 0], [0, .2, .9, 1], 9)}'
             f'<polygon points="{shape}" fill="{GOLD}" fill-opacity=".25" stroke="{GOLD}" stroke-width="3" filter="url(#glow)"/></g></g>')
    for i, (lab, v) in enumerate(axes):
        x, y = pt(i, 12.6)
        anc = "middle" if abs(x - cx) < 8 else ("start" if x > cx else "end")
        body += mono(x, y + 4, f"{lab} {v}", 12, SOFT, anc, 1)
    S("radar.svg", svg(W, H, body, "Fighter stats radar: curiosity 10, frontend 7, JavaScript 6, backend 5, Python/ML 4, consistency 6", c=18, glows=[(215, 182, 120, GOLD, .12)]))


def titanic():
    W, H = 430, 340
    r = 72
    c = 2 * math.pi * r
    off = c * (1 - .799)
    body = disp(24, 44, "TRAINING RESULT", 28, "url(#gold)") + mono(24, 66, "TITANIC DATASET · LEARNING CHECKPOINT", 11.5, DIM, ls=1.5)
    body += (f'<g transform="rotate(-90 215 168)"><circle cx="215" cy="168" r="{r}" stroke="{EDGE}" stroke-width="14"/>'
             f'<circle cx="215" cy="168" r="{r}" stroke="url(#hot)" stroke-width="14" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" filter="url(#glow)">'
             f'{A("stroke-dashoffset", [round(c, 1), round(off, 1), round(off, 1), round(c, 1)], [0, .25, .9, 1], 9)}</circle></g>')
    body += disp(215, 182, "79.9%", 46, WHT, "middle") + mono(215, 204, "TEST ACCURACY", 11, DIM, "middle", 3)
    body += sans(215, 280, "Logistic Regression + feature standardisation", 14.5, WHT, "middle", 600)
    body += sans(215, 302, "Held-out test split. A learning checkpoint,", 13, SOFT, "middle") + sans(215, 320, "not a claim of production ML experience.", 13, SOFT, "middle")
    S("titanic.svg", svg(W, H, body, "Titanic experiment: about 79.9 percent accuracy", c=18, glows=[(215, 168, 120, RED, .16)]))


# ═════════════════════════════ PROJECT STAGES ═════════════════════════════
def thumb(kind, col):
    W = 430
    if kind == "net":
        pts = [(50, 60), (120, 24), (170, 70), (240, 30), (290, 72), (350, 26), (400, 62)]
        ed = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 3), (2, 4)]
        return ("".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="{col}" stroke-opacity=".5" stroke-width="2"/>' for a, b in ed)
                + "".join(pulse(x, y, col, 5, 2.4, i * .4) for i, (x, y) in enumerate(pts)))
    if kind == "books":
        return "".join(f'<rect x="{40 + i * 44}" y="96" width="30" height="0" fill="{col}" fill-opacity="{.5 + (i % 3) * .15}">{A("height", [0, 30 + (i * 17) % 46, 0], dur=3.2, begin=i * .25)}{A("y", [96, 96 - (30 + (i * 17) % 46), 96], dur=3.2, begin=i * .25)}</rect>' for i in range(9))
    if kind == "orbit":
        return "".join(f'<circle cy="48" r="{22 + i * 10}" stroke="{col}" stroke-opacity="{.8 - i * .2}" stroke-width="2.5">{A("cx", [150 + i * 20, 280 - i * 20, 150 + i * 20], dur=4 + i, calc="spline", extra=chr(107) + "eySplines=" + chr(34) + "0.5 0 0.5 1;0.5 0 0.5 1" + chr(34) + " keyTimes=" + chr(34) + "0;.5;1" + chr(34))}</circle>' for i in range(3))
    if kind == "grid":
        return "".join(f'<rect x="{60 + c * 36}" y="{14 + r * 26}" width="26" height="18" fill="{col}" opacity=".15">{A("opacity", [.15, 1, .15], dur=2.4, begin=(c + r) * .18)}</rect>' for c in range(10) for r in range(3))
    if kind == "bands":
        return "".join(f'<g>{AT("translate", [f"{-40 * (1 if r % 2 else -1)} 0", f"{40 * (1 if r % 2 else -1)} 0", f"{-40 * (1 if r % 2 else -1)} 0"], dur=5 + r)}<rect x="30" y="{12 + r * 22}" width="{300 + r * 30}" height="14" fill="{col}" fill-opacity="{.25 + r * .15}"/></g>' for r in range(4))
    return "".join(f'<circle cx="{rx}" cy="100" r="{rr}" stroke="{col}" stroke-width="2.5" fill="{col}" fill-opacity=".12">{A("cy", [108, 6], dur=sp, begin=-d, calc="spline", extra="keyTimes=" + chr(34) + "0;1" + chr(34) + " keySplines=" + chr(34) + "0.3 0 0.7 1" + chr(34))}{A("opacity", [0, 1, 0], dur=sp, begin=-d)}</circle>'
                   for rx, rr, sp, d in [(50, 12, 4, 0), (110, 8, 3.2, 1), (170, 16, 5, 2), (240, 10, 3.6, 0.5), (300, 14, 4.4, 1.5), (360, 9, 3, 2.2), (400, 13, 4.8, 3)])


PROJECTS = [
    ("zylo", "ZYLO", "FULL-STACK SOCIAL PLATFORM", "Server-rendered social app: routes, views, auth, and persistent data.", ["Node.js", "Express", "EJS", "MySQL"], CYA, "net"),
    ("lms", "LIBRARY MANAGEMENT SYSTEM", "DESKTOP APP · DATABASE PRACTICE", "JavaFX + MySQL desktop app exploring records, member workflows, and database integration.", ["Java", "JavaFX", "MySQL"], GOLD, "books"),
    ("ochi", "OCHI WEBSITE CLONE", "FRONTEND & MOTION EXPERIMENT", "A recreation inspired by Ochi.design: composition, animation, and polished landing-page interactions.", ["React", "GSAP", "Framer Motion"], PUR, "orbit"),
    ("grid", "GRID SCROLL ANIMATION", "SCROLL INTERACTION EXPERIMENT", "Scroll-driven movement and more expressive browsing, built with an animated grid.", ["JavaScript", "GSAP", "Lenis"], PINK, "grid"),
    ("twogood", "TWO GOOD WEBSITE CLONE", "WEBSITE RECREATION", "Animated sections, scroll interactions, and page composition practice.", ["HTML", "CSS", "JavaScript", "GSAP"], LIME, "bands"),
    ("bubble", "BUBBLE GAME", "BROWSER MINI-GAME", "A small JavaScript game, and proof that learning can be visual, interactive, and fun.", ["JavaScript", "HTML", "CSS"], BLU, "bubbles"),
]


def project(i, key, title, kind, desc, tags, col, th):
    W, H = 430, 246
    body = f'<defs><clipPath id="strip"><rect width="{W}" height="96"/></clipPath></defs><rect width="{W}" height="96" fill="{col}" fill-opacity=".07"/>'
    body += f'<g clip-path="url(#strip)">{thumb(th, col)}</g><rect y="95" width="{W}" height="2" fill="{col}"/>'
    body += f'<polygon points="0,0 96,0 84,24 0,24" fill="{col}"/>' + mono(12, 17, f"STAGE 0{i + 1}", 12, INK, ls=2, extra='font-weight="700"')
    body += f'<g>{blink(1.1)}{mono(W - 16, 20, "▶ ENTER", 12.5, WHT, "end", 2)}</g>'
    body += disp(20, 128, title, fit(title, W - 40, 28), WHT) + mono(20, 148, kind, 11.5, col, ls=1.5)
    for j, ln in enumerate(wrap_text(desc, 54)[:2]):
        body += sans(20, 172 + j * 19, ln, 14, SOFT)
    x = 20
    for t in tags:
        w = round(len(t) * 7.4 + 20)
        body += f'<rect x="{x}" y="{H - 34}" width="{w}" height="22" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>' + mono(x + w / 2, H - 19, t, 11.5, col, "middle")
        x += w + 8
    body += (f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" stroke="{col}" stroke-width="2.5" stroke-dasharray="120 {2 * (W + H)}" filter="url(#glow)">'
             f'{A("stroke-dashoffset", [0, -(2 * (W + H) + 120)], dur=7, begin=-i * 1.2)}</rect>')
    S(f"project-{key}.svg", svg(W, H, body, f"Stage {i + 1}: {title.title()}. {kind.title()}.", c=16, border=col))


# ═════════════════════════════ LADDER ═════════════════════════════
def ladder():
    W, H = 880, 300
    stages = [("HTML·CSS·JS", "", "CLEARED", CYA), ("REACT", "", "IN PROGRESS", PUR), ("NODE +", "EXPRESS", "IN PROGRESS", PUR),
              ("MONGODB +", "AUTH", "IN PROGRESS", PUR), ("PYTHON + ML", "", "IN PROGRESS", PUR), ("NLP + AI", "FEATURES", "UP NEXT", DIM)]
    xs = [70 + i * 117 for i in range(7)]
    body = f'<line x1="70" y1="150" x2="{xs[-1]}" y2="150" stroke="{EDGE}" stroke-width="5"/><line x1="70" y1="150" x2="{xs[1]}" y2="150" stroke="{GOLD}" stroke-width="5"/>'
    body += f'<circle r="6" fill="{CYA}" filter="url(#glow)"><animateMotion dur="6s" repeatCount="indefinite" path="M70 150 H{xs[-1]}"/></circle>'
    for i, (a, b, st, col) in enumerate(stages):
        x = xs[i]
        d = f"{x},128 {x + 22},150 {x},172 {x - 22},150"
        if st == "CLEARED":
            body += f'<polygon points="{d}" fill="{GOLD}" filter="url(#glow)"/><path d="M{x - 8} 150 l6 7 l11-13" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        elif st == "IN PROGRESS":
            body += f'<polygon points="{d}" fill="{INK}" stroke="{PUR}" stroke-width="3">{A("stroke-opacity", [1, .35, 1], dur=1.8, begin=i * .25)}</polygon>' + pulse(x, 150, PUR, 4, 1.8, i * .25)
        else:
            body += f'<polygon points="{d}" fill="{INK}" stroke="{DIM}" stroke-width="2.5" stroke-dasharray="4 4"/>'
        body += mono(x, 100, f"STAGE {i + 1}", 12, GOLD if st != "UP NEXT" else DIM, "middle", 2)
        body += mono(x, 204, a, 12.5, WHT, "middle", 1) + (mono(x, 221, b, 12.5, WHT, "middle", 1) if b else "")
        body += mono(x, 252, st, 11, col if st != "IN PROGRESS" else "#C084FC", "middle", 2)
    bx = xs[-1]
    spikes = " ".join(f"{bx + (40 if k % 2 == 0 else 26) * math.cos(math.radians(30 * k)):.1f},{150 + (40 if k % 2 == 0 else 26) * math.sin(math.radians(30 * k)):.1f}" for k in range(12))
    body += f'<g>{AT("rotate", [f"0 {bx} 150", f"360 {bx} 150"], dur=10)}<polygon points="{spikes}" fill="{RED}" fill-opacity=".85" filter="url(#glow)"/></g>'
    body += f'<circle cx="{bx}" cy="150" r="17" fill="{INK}" stroke="{GOLD}" stroke-width="3"/>' + mono(bx, 155, "☠", 17, GOLD, "middle")
    body += mono(bx, 100, "FINAL BOSS", 12, RED, "middle", 2) + disp(bx, 214, "SHIP A REAL", 17, GOLD, "middle") + disp(bx, 234, "PRODUCT", 17, GOLD, "middle")
    body += f'<g>{AT("translate", ["0 0", "0 -7", "0 0"], dur=1.1)}{mono(xs[1], 70, "▼ YOU ARE HERE", 12.5, GOLD, "middle", 2)}</g>'
    body += mono(28, 42, "ARCADE MODE · 7 STAGES", 13, GOLD, ls=4) + mono(W - 28, 42, "CLEARED = COMFORTABLE", 11.5, DIM, "end", 2)
    S("ladder.svg", svg(W, H, body, "Arcade ladder: HTML/CSS/JS cleared, React and the backend in progress, Python/ML in progress, NLP up next, final boss ship a real product", c=20, glows=[(bx, 150, 130, RED, .22), (xs[1], 150, 120, PUR, .15)]))


# ═════════════════════════════ TRAINING MODE ═════════════════════════════
IDEAS = [
    ("inventory", "INVENTORY OS", "Offline-first inventory & POS for small shops: stock, barcodes, expiry alerts, receipts, and staff roles. Built to stay dependable without internet.", CYA),
    ("habit", "HABIT & DEV TOOLS", "Habit tracking, daily planning, and a developer task tracker. Made to cut friction, not to add more organising.", PINK),
    ("fyp", "PROBLEM-FIRST FYP", "A BSCS final-year product that solves a real student or workflow problem. Users first, tech second, AI only when it adds real capability.", GOLD),
]


def idea(i, key, title, desc, col):
    W, H = 280, 310
    body = f'<polygon points="0,0 150,0 136,24 0,24" fill="{col}"/>' + mono(12, 17, "TRAINING MODE", 12, INK, ls=2, extra='font-weight="700"')
    sway = AT("rotate", [f"{d} 14 70" for d in (0, 8, 0, -8, 0)], dur=2.4, begin=i * .4)
    body += (f'<g transform="translate({W - 56} 40)"><g stroke="{col}" stroke-width="3" stroke-linecap="round">{sway}'
             f'<circle cx="14" cy="8" r="8"/><path d="M14 16V50M0 28H28M14 50L4 70M14 50L24 70"/></g></g>')
    body += disp(20, 104, title, fit(title, W - 40, 26), WHT)
    for j, ln in enumerate(wrap_text(desc, 33)[:6]):
        body += sans(20, 138 + j * 21, ln, 14, SOFT)
    body += mono(20, H - 20, "NOT A LAUNCH · AN IDEA TO BUILD", 11, DIM, ls=1.5) + sweep(W, H, color=col, dur=5 + i, delay=i)
    S(f"idea-{key}.svg", svg(W, H, body, f"Training mode concept: {title.title()}", c=16, border=col, glows=[(W - 20, 10, 100, col, .2)]))


# ═════════════════════════════ ARENA ═════════════════════════════
def arena_button(file, label, beats, col, icon):
    W, H = 280, 130
    body = f'<g transform="translate(26 26)" filter="url(#glow)">{icon}</g>'
    body += disp(110, 62, label, 40, WHT, extra='stroke="#000" stroke-width="5" paint-order="stroke"') + mono(110, 86, f"BEATS {beats}", 12.5, col, ls=2)
    body += f'<g>{blink(1.0)}{mono(110, 112, "CLICK TO FIGHT ▶", 12, GOLD, ls=2)}</g>' + sweep(W, H, color=col, dur=3.5)
    S(file, svg(W, H, body, f"{label.title()}: beats {beats.lower()}. Click to fight.", c=16, border=col, glows=[(50, 50, 80, col, .35)]))


def arena_icons():
    star = " ".join(f"{39 + (36 if k % 2 == 0 else 15) * math.cos(math.radians(36 * k - 90)):.1f},{39 + (36 if k % 2 == 0 else 15) * math.sin(math.radians(36 * k - 90)):.1f}" for k in range(10))
    strike = f'<polygon points="{star}" fill="{RED}" stroke="{GOLD}" stroke-width="3">{AT("scale", [1, 1, 1], dur=1)}</polygon>'
    throw = f'<path d="M12 28 A28 28 0 0 1 62 24" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/><path d="M66 50 A28 28 0 0 1 16 54" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/><path d="M52 12 L64 26 L46 30Z" fill="{GOLD}"/><path d="M26 66 L14 52 L32 48Z" fill="{GOLD}"/>'
    guard = f'<path d="M39 4 L70 16 V40 C70 58 56 70 39 76 C22 70 8 58 8 40 V16 Z" fill="{CYA}" fill-opacity=".25" stroke="{CYA}" stroke-width="5" stroke-linejoin="round"/><path d="M39 22 V58 M24 36 H54" stroke="{CYA}" stroke-width="4" stroke-linecap="round"/>'
    return strike, throw, guard


def favourites():
    W, H = 880, 372
    cards = [("fight", "FIGHTING-GAME ARC", "Tekken is movement, timing, and execution, and learning from losses is its own training path. Kazuya is my main.", RED),
             ("game", "GAMING", "Free Fire, Clash of Clans, Clash Royale, and whatever looks fun to explore next.", PUR),
             ("movie", "ANIME & MOVIES", "High-energy action, darker stories, and films that leave emotional damage.", PINK),
             ("curious", "CURIOSITY MODE", "I like learning how tools work under the hood, not just which button to press.", GOLD)]
    ic = {"fight": f'<path d="M10 10 L42 42 M42 10 L10 42" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>',
          "game": f'<rect x="20" y="6" width="12" height="40" rx="3" fill="{PUR}"/><rect x="6" y="20" width="40" height="12" rx="3" fill="{PUR}"/>',
          "movie": f'<path d="M14 8 L46 26 L14 44Z" fill="{PINK}" stroke="{PINK}" stroke-width="3" stroke-linejoin="round"/>',
          "curious": f'<circle cx="23" cy="23" r="14" stroke="{GOLD}" stroke-width="6"/><path d="M34 34 L48 48" stroke="{GOLD}" stroke-width="6" stroke-linecap="round"/>'}
    body = ""
    for i, (k, t, d, col) in enumerate(cards):
        x, y = (i % 2) * 450, (i // 2) * 196
        body += (f'<g transform="translate({x} {y})"><polygon points="{poly(430, 176, 14)}" fill="{PANEL}"/><polygon points="{poly(430, 176, 14)}" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>'
                 f'<g transform="translate(24 24)" filter="url(#glow)">{ic[k]}</g>' + disp(92, 58, t, 26, WHT))
        for j, ln in enumerate(wrap_text(d, 52)[:3]):
            body += sans(24, 100 + j * 22, ln, 14.5, SOFT)
        body += f'<rect x="24" y="158" width="50" height="4" fill="{col}"/></g>'
    S("favourites.svg", svg(W, H, body, "Player 2 mode: Tekken, gaming, anime and movies, curiosity", frame=False))


def continue_banner():
    W, H = 880, 170
    body = disp(36, 112, "CONTINUE?", 96, "url(#hot)", extra='stroke="#000" stroke-width="6" paint-order="stroke"')
    for i, d in enumerate(range(9, -1, -1)):
        body += (f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="0;{i / 10:.1f};{(i + 1) / 10:.1f};1" dur="10s" repeatCount="indefinite"/>'
                 + disp(770, 128, d, 120, "url(#gold)", "middle", 'stroke="#000" stroke-width="6" paint-order="stroke"') + "</g>")
    body += mono(40, 146, "PRESS ANY BUTTON BELOW TO TALK", 13, SOFT, ls=5) + '<rect y="160" width="880" height="10" fill="url(#haz)" opacity=".85"/>'
    S("continue.svg", svg(W, H, body, "Continue? Nine, eight, seven... press any button to talk.", c=20, glows=[(770, 90, 130, RED, .3)]))


def footer():
    W, H = 880, 220
    floor = f'<g stroke="{PUR}" stroke-opacity=".55">' + "".join(f'<line x1="{440 + i * 12}" y1="120" x2="{440 + i * 90}" y2="220"/>' for i in range(-12, 13)) + "</g>"
    for k in range(4):
        floor += f'<line x1="0" x2="{W}" y1="120" y2="120" stroke="{CYA}" stroke-width="1.5">{A("y1", [120, 220], dur=4, begin=-k, calc="spline", extra="keyTimes=" + chr(34) + "0;1" + chr(34) + " keySplines=" + chr(34) + "0.6 0 0.9 0.5" + chr(34))}{A("y2", [120, 220], dur=4, begin=-k, calc="spline", extra="keyTimes=" + chr(34) + "0;1" + chr(34) + " keySplines=" + chr(34) + "0.6 0 0.9 0.5" + chr(34))}</line>'
    body = floor + disp(440, 70, "THANKS FOR PLAYING", 60, "url(#gold)", "middle", 'stroke="#000" stroke-width="6" paint-order="stroke"')
    body += mono(440, 104, "while (alive) { learn(); build(); improve(); }", 17, CYA, "middle", 1)
    body += f'<g>{blink(1.2)}{mono(440, 196, "CREDIT 01  ·  STILL LEARNING · STILL BUILDING · STILL GOING", 13, GOLD, "middle", 3)}</g>'
    S("footer.svg", svg(W, H, body, "Thanks for playing. Still learning, still building, still going.", c=22, glows=[(440, 60, 200, RED, .22)]))


# ═════════════════════════════ BUILD ═════════════════════════════
if __name__ == "__main__":
    hero()
    quote()
    for f, lab, col in [("btn-projects.svg", "PROJECTS", CYA), ("btn-arena.svg", "FIGHT ME", RED), ("btn-linkedin.svg", "LINKEDIN", BLU), ("btn-itch.svg", "ITCH.IO", PINK), ("btn-repos.svg", "ALL REPOS", PUR)]:
        button(f, lab, col)
    select_banner()
    web, ai, game = icons()
    select_tile(0, "select-web.svg", "PATH 01", "WEB DEV", "REACT · NODE · MONGODB", CYA, web)
    select_tile(1, "select-ai.svg", "PATH 02", "AI / ML", "PYTHON · DATA · SKLEARN", PUR, ai)
    select_tile(2, "select-game.svg", "PATH 03", "ARENA", "CHALLENGE ME TO A FIGHT", GOLD, game)
    for f, n, t, h, c in [("h-profile.svg", "01", "Player Profile", "fighter bio", CYA), ("h-moves.svg", "02", "Move List", "honest levels only", PUR),
                          ("h-stages.svg", "03", "Stage Select", "click a stage to see the source", PINK), ("h-ladder.svg", "04", "Arcade Ladder", "climbing toward the boss", GOLD),
                          ("h-training.svg", "05", "Training Mode", "ideas, not fake launches", LIME), ("h-log.svg", "06", "Battle Log", "auto-synced from GitHub", BLU),
                          ("h-arena.svg", "07", "Challenge Zain", "play a real round", RED), ("h-p2.svg", "08", "Player 2 Mode", "off the clock", PINK)]:
        header(f, n, t, h, c)
    profile(); movelist(); radar(); titanic(); ladder(); favourites(); continue_banner(); footer()
    for i, p in enumerate(PROJECTS):
        project(i, *p)
    for i, d in enumerate(IDEAS):
        idea(i, *d)
    s_icon, t_icon, g_icon = arena_icons()
    arena_button("btn-strike.svg", "STRIKE", "THROW", RED, s_icon)
    arena_button("btn-throw.svg", "THROW", "GUARD", GOLD, t_icon)
    arena_button("btn-guard.svg", "GUARD", "STRIKE", CYA, g_icon)
    # live graphics: placeholders (Actions redraw these with real data)
    stats.ROOT = __import__("pathlib").Path(HERE)
    if not (os.path.exists(os.path.join(OUT, "stats.svg")) and os.path.exists(os.path.join(OUT, "heatmap.svg"))):
        stats.write_all(None)
    sb = os.path.join(OUT, "scoreboard.svg")
    if not os.path.exists(sb):
        save(sb, fight.render_scoreboard(fight.DEFAULT))
    print("Generated", len(os.listdir(OUT)), "assets")
