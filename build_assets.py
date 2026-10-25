#!/usr/bin/env python3
"""
Zain Ali — profile README asset generator.
Run:  python3 build_assets.py   ->  writes animated SVGs into ./assets
Edit the DATA blocks (projects, skills, ratings...) and re-run to regenerate.
All SVGs are self-contained (no external fonts/images) so GitHub renders them.
"""
import html
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

# ── palette ────────────────────────────────────────────────────────────────
PANEL, BORDER = "#0B0D1A", "#1B1F3B"
TEXT, SOFT, MUTED = "#E6E8F5", "#AEB4D6", "#8B91B5"
CY, VI, PK, AM, LM, BL = "#22D3EE", "#8B5CF6", "#F472B6", "#FBBF24", "#A3E635", "#60A5FA"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Inter','SF Pro Display',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"


def esc(s):
    return html.escape(s, quote=False)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def wrap_text(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = f"{cur} {w}".strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def svg(w, h, body, title, defs="", rx=24, frame=True, glows=(), dots=True):
    """Common card shell: dark glass panel, dot grid, soft glows, hairline border."""
    glow_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" fill-opacity="{o}" filter="url(#blur)"/>'
        for (x, y, r, c, o) in glows
    )
    if frame:
        dots_svg = f'<rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#fade)"/>' if dots else ""
        shell_open = f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{PANEL}"/>{dots_svg}{glow_svg}'
    else:
        shell_open = "<g>"
    border = (
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" stroke="{BORDER}"/>' if frame else ""
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
<linearGradient id="aur" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}"/><stop offset=".5" stop-color="{VI}"/><stop offset="1" stop-color="{PK}"/></linearGradient>
<clipPath id="card"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".09"/></pattern>
<radialGradient id="fadeg" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="{w}" height="{h}" fill="url(#fadeg)"/></mask>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{defs}
</defs>
{shell_open}
{body}
</g>
{border}
</svg>
"""


def scanline(w, h, color="url(#aur)", dur=6, delay=0):
    """A thin light that sweeps along the bottom edge."""
    return (
        f'<rect x="-240" y="{h - 3}" width="240" height="3" fill="{color}" opacity=".9">'
        f'<animate attributeName="x" from="-240" to="{w}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></rect>'
    )


def tspans(runs):
    return "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in runs)


def typed(uid, x, y, runs, fs, keytimes, width, cursor_color=CY, family=MONO, dur=14, weight=400, cw=0.61):
    """Typewriter line: a clip rect grows (SMIL) while a cursor block follows it."""
    kt = ";".join(f"{k:.4f}" for k in keytimes)
    vals = ";".join(str(v) for v in [0, 0, width, width, 0, 0][: len(keytimes)])
    xs = ";".join(str(v) for v in [x, x, x + width, x + width, x, x][: len(keytimes)])
    a1, b, c = keytimes[1], keytimes[2], keytimes[3]
    ok = f"0;{a1:.4f};{min(b + 0.015, c):.4f};1"
    return f"""<clipPath id="c{uid}"><rect x="{x - 2}" y="{y - fs}" width="0" height="{fs * 1.5:.0f}"><animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></rect></clipPath>
<text x="{x}" y="{y}" font-family="{family}" font-size="{fs}" font-weight="{weight}" clip-path="url(#c{uid})" xml:space="preserve">{tspans(runs)}</text>
<rect x="{x}" y="{y - fs + 2}" width="{fs * 0.5:.1f}" height="{fs * 1.1:.1f}" fill="{cursor_color}" opacity="0"><animate attributeName="x" values="{xs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="{ok}" dur="{dur}s" repeatCount="indefinite"/></rect>"""


def pulse_dot(cx, cy, color, r=5, dur=2.2, delay=0):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity=".35">'
        f'<animate attributeName="r" values="{r};{r * 3};{r}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".45;0;.45" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    )


# ══════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════
def hero():
    W, H = 1200, 440
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.randint(20, W - 20)}" cy="{rnd.randint(16, H - 16)}" r="{rnd.choice([1, 1, 1.4, 1.8])}" fill="#fff" opacity=".6">'
        f'<animate attributeName="opacity" values=".1;.9;.1" dur="{rnd.uniform(2.5, 6):.1f}s" begin="{rnd.uniform(0, 4):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(26)
    )
    blobs = f"""
<g filter="url(#blur)">
  <circle cx="230" cy="110" r="190" fill="{CY}" fill-opacity=".30"><animateTransform attributeName="transform" type="translate" values="0 0;70 40;0 0" dur="14s" repeatCount="indefinite"/></circle>
  <circle cx="1010" cy="360" r="210" fill="{VI}" fill-opacity=".38"><animateTransform attributeName="transform" type="translate" values="0 0;-80 -40;0 0" dur="17s" repeatCount="indefinite"/></circle>
  <circle cx="640" cy="40" r="150" fill="{PK}" fill-opacity=".22"><animateTransform attributeName="transform" type="translate" values="0 0;-60 60;0 0" dur="19s" repeatCount="indefinite"/></circle>
</g>"""
    orbit = (
        f'<g transform="translate(965 212)"><circle r="196" stroke="#fff" stroke-opacity=".07" stroke-dasharray="3 9"/>'
        f'<circle r="150" stroke="{CY}" stroke-opacity=".12" stroke-dasharray="1 14"/>'
        f'<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="60s" repeatCount="indefinite" additive="sum"/></g>'
    )
    # prompt lines (typewriter cycle)
    lines = [
        "BSCS student & developer in progress",
        "JavaScript → full-stack web development",
        "Python → data science & machine learning",
        "Turning real problems into useful products",
    ]
    T, slot, fs = 16.0, 4.0, 24
    prompt = ""
    for i, ln in enumerate(lines):
        a = i * slot
        kt = [0, (a + 0.15) / T, (a + 1.9) / T, (a + slot - 0.5) / T, (a + slot - 0.1) / T, 1]
        wdt = round(len(ln) * fs * 0.6 + 6)
        prompt += typed(f"h{i}", 92, 296, [(ln, TEXT)], fs, kt, wdt, dur=T, weight=500)
    code = f"""
<g>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -10;0 0" dur="7s" repeatCount="indefinite"/>
  <rect x="800" y="70" width="340" height="282" rx="20" fill="#0F1226" fill-opacity=".72" stroke="#fff" stroke-opacity=".13"/>
  <circle cx="826" cy="96" r="5.5" fill="#FB7185"/><circle cx="846" cy="96" r="5.5" fill="{AM}"/><circle cx="866" cy="96" r="5.5" fill="{LM}"/>
  <text x="1112" y="100" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">zain.ts</text>
  <line x1="800" y1="116" x2="1140" y2="116" stroke="#fff" stroke-opacity=".08"/>
  <text font-family="{MONO}" font-size="16" xml:space="preserve">
    <tspan x="826" y="152" fill="{PK}">const </tspan><tspan fill="{CY}">zain </tspan><tspan fill="{MUTED}">= {{</tspan>
    <tspan x="826" y="182" fill="{TEXT}">  main: </tspan><tspan fill="{LM}">"Full-Stack Web"</tspan><tspan fill="{MUTED}">,</tspan>
    <tspan x="826" y="212" fill="{TEXT}">  next: </tspan><tspan fill="{LM}">"AI / ML"</tspan><tspan fill="{MUTED}">,</tspan>
    <tspan x="826" y="242" fill="{TEXT}">  mood: </tspan><tspan fill="{LM}">"keep going"</tspan><tspan fill="{MUTED}">,</tspan>
    <tspan x="826" y="272" fill="{MUTED}">}};</tspan>
    <tspan x="826" y="318" fill="{AM}">build</tspan><tspan fill="{TEXT}">(</tspan><tspan fill="{CY}">zain</tspan><tspan fill="{TEXT}">);</tspan>
  </text>
  <rect x="948" y="304" width="9" height="19" fill="{CY}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>
</g>"""
    body = f"""
{blobs}
{orbit}
{stars}
<g>
  <rect x="60" y="54" width="338" height="36" rx="18" fill="{CY}" fill-opacity=".08" stroke="{CY}" stroke-opacity=".38"/>
  {pulse_dot(84, 72, "#34D399")}
  <text x="102" y="77" font-family="{MONO}" font-size="12.5" letter-spacing="1.6" fill="#A5F3FC">LEARNING IN PUBLIC · BSCS · PK</text>
</g>
<defs>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="{CY}"/><stop offset=".45" stop-color="{VI}"/><stop offset=".8" stop-color="{PK}"/><stop offset="1" stop-color="{CY}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.6 0;0.6 0;-0.6 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<text x="56" y="214" font-family="{SANS}" font-size="116" font-weight="800" letter-spacing="-3" fill="url(#name)">Zain Ali</text>
<text x="60" y="296" font-family="{MONO}" font-size="24" font-weight="700" fill="{CY}">&gt;</text>
{prompt}
<text x="60" y="352" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{MUTED}">CODE  •  CREATE  •  KEEP GOING</text>
<text x="60" y="402" font-family="{MONO}" font-size="13" fill="{MUTED}" fill-opacity=".85">Riphah International University · Pakistan</text>
{code}
<rect x="0" y="{H - 4}" width="{W}" height="4" fill="url(#aur)"/>
"""
    save("hero.svg", svg(W, H, body, "Zain Ali — BSCS student and developer in progress", rx=28, dots=True))


# ══════════════════════════════════════════════════════════════════════════
# SECTION HEADERS
# ══════════════════════════════════════════════════════════════════════════
def section_header(file, num, title, hint, accent=CY):
    W, H = 1200, 92
    body = f"""
<rect x="0" y="0" width="7" height="{H}" fill="url(#aur)"/>
<text x="38" y="36" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{accent}">// {num}</text>
<text x="36" y="72" font-family="{SANS}" font-size="34" font-weight="800" letter-spacing="-.5" fill="{TEXT}">{esc(title)}</text>
<text x="{W - 36}" y="58" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(hint)}</text>
{scanline(W, H, dur=5)}
"""
    save(file, svg(W, H, body, f"{title} — section header", rx=22, glows=[(1100, 20, 120, accent, 0.18)]))


# ══════════════════════════════════════════════════════════════════════════
# BUTTONS
# ══════════════════════════════════════════════════════════════════════════
def button(file, label, accent):
    W, H = 220, 56
    body = f"""
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="28" fill="{accent}" fill-opacity=".10" stroke="{accent}" stroke-opacity=".65" stroke-width="1.5"/>
<defs><linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<rect x="-90" y="0" width="70" height="{H}" fill="url(#shine)" transform="skewX(-20)"><animate attributeName="x" values="-90;{W + 40};{W + 40}" keyTimes="0;.45;1" dur="4.5s" repeatCount="indefinite"/></rect>
<circle cx="34" cy="{H / 2}" r="5" fill="{accent}" filter="url(#glow)"/>
<text x="54" y="{H / 2 + 5.5}" font-family="{SANS}" font-size="15.5" font-weight="700" letter-spacing="1.2" fill="{TEXT}">{esc(label)}</text>
<text x="{W - 30}" y="{H / 2 + 6}" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="700" fill="{accent}">→</text>
"""
    save(file, svg(W, H, body, label, rx=28, frame=False))


# ══════════════════════════════════════════════════════════════════════════
# QUOTE
# ══════════════════════════════════════════════════════════════════════════
def quote():
    W, H = 1200, 176
    body = f"""
<text x="34" y="150" font-family="{SANS}" font-size="170" font-weight="800" fill="url(#aur)" opacity=".95">“</text>
<text x="610" y="78" text-anchor="middle" font-family="{SANS}" font-size="36" font-weight="800" letter-spacing="-.5" fill="{TEXT}">Never stop because life is not end yet.</text>
<text x="610" y="122" text-anchor="middle" font-family="{SANS}" font-size="16.5" fill="{SOFT}">I don't need to know everything today. I need to keep learning,</text>
<text x="610" y="146" text-anchor="middle" font-family="{SANS}" font-size="16.5" fill="{SOFT}">build honestly, and get a little better with every project.</text>
{scanline(W, H, dur=7)}
"""
    save("quote.svg", svg(W, H, body, "Never stop because life is not end yet", rx=26, glows=[(180, 90, 160, VI, 0.25), (1050, 100, 160, CY, 0.18)]))


# ══════════════════════════════════════════════════════════════════════════
# ABOUT: terminal + status
# ══════════════════════════════════════════════════════════════════════════
def terminal():
    W, H, T, fs = 720, 360, 18.0, 15
    cmd = lambda t: [("$ ", CY), (t, TEXT)]
    out = lambda t, c=SOFT: [(t, c)]
    script = [
        (cmd("whoami"), 0.8, 1.6),
        (out("zain ali · bscs student · developer in progress", LM), 2.0, 3.4),
        (cmd("cat mission.txt"), 4.0, 5.2),
        (out("build useful things for the web, understand them deeply,"), 5.6, 7.2),
        (out("then grow into AI/ML along the way."), 7.3, 8.5),
        (cmd("cat stack.json"), 9.0, 10.2),
        (out('{ "main": ["JavaScript", "React", "Node", "MongoDB"],', "#C4B5FD"), 10.5, 12.0),
        (out('  "learning": ["Python", "scikit-learn"] }', "#C4B5FD"), 12.1, 13.2),
        (cmd("echo $MOTTO"), 13.7, 14.8),
        (out("Never stop because life is not end yet.", AM), 15.1, 16.8),
    ]
    body = f"""
<rect x="0" y="0" width="{W}" height="46" fill="#fff" fill-opacity=".03"/>
<line x1="0" y1="46" x2="{W}" y2="46" stroke="#fff" stroke-opacity=".08"/>
<circle cx="28" cy="23" r="6" fill="#FB7185"/><circle cx="50" cy="23" r="6" fill="{AM}"/><circle cx="72" cy="23" r="6" fill="{LM}"/>
<text x="{W / 2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{MUTED}">zain@riphah: ~/about</text>
"""
    y = 84
    for i, (runs, s, e) in enumerate(script):
        n = sum(len(t) for t, _ in runs)
        kt = [0, s / T, e / T, 0.965, 0.995, 1]
        body += typed(f"t{i}", 32, y, runs, fs, kt, round(n * fs * 0.61 + 6), dur=T)
        y += 27 if i not in (0, 2, 4, 5, 7, 8) else 27
    save("terminal.svg", svg(W, H, body, "Terminal: whoami — Zain Ali, BSCS student", rx=24, glows=[(660, 40, 150, VI, 0.20)]))


def status():
    W, H = 480, 360
    rows = [
        ("LEARNING", ["React · Node/Express · MongoDB", "Python · pandas · scikit-learn"], CY),
        ("PRACTISING", ["Auth flows: bcrypt, JWT, role middleware", "and clean REST APIs"], VI),
        ("AIMING FOR", ["A problem-first FYP and a shipped", "full-stack project"], PK),
        ("PLAYING", ["Tekken (Kazuya main) · Clash games"], AM),
    ]
    body = f'<text x="32" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{CY}">STATUS · RIGHT NOW</text>'
    body += f'<line x1="32" y1="62" x2="{W - 32}" y2="62" stroke="#fff" stroke-opacity=".08"/>'
    y = 100
    for i, (lab, vals, col) in enumerate(rows):
        body += pulse_dot(40, y - 4, col, r=4.5, delay=i * 0.5)
        body += f'<text x="62" y="{y}" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{col}">{lab}</text>'
        for j, v in enumerate(vals):
            body += f'<text x="62" y="{y + 24 + j * 21}" font-family="{SANS}" font-size="15" fill="{TEXT}">{esc(v)}</text>'
        y += 70
    body += scanline(W, H, dur=6, delay=1)
    save("status.svg", svg(W, H, body, "Status right now: learning, practising, aiming for, playing", rx=24, glows=[(430, 330, 140, PK, 0.16)]))


# ══════════════════════════════════════════════════════════════════════════
# STACK marquee
# ══════════════════════════════════════════════════════════════════════════
LEVEL = {"c": CY, "s": VI, "e": AM}
ROW_WEB = [
    ("HTML", "c"), ("CSS", "c"), ("Tailwind CSS", "c"), ("JavaScript", "c"), ("React", "c"),
    ("Node.js", "s"), ("Express", "s"), ("MongoDB", "s"), ("MySQL", "s"), ("EJS", "s"),
    ("REST APIs", "s"), ("JWT", "s"), ("bcrypt", "s"), ("Git", "s"), ("GitHub", "s"),
]
ROW_DATA = [
    ("Python", "s"), ("NumPy", "s"), ("pandas", "s"), ("Matplotlib", "s"), ("scikit-learn", "s"),
    ("Logistic Regression", "s"), ("Random Forest", "s"), ("Java", "s"), ("Docker", "e"), ("Linux", "e"),
    ("Figma", "e"), ("Flutter", "e"), ("Dart", "e"), ("Unity", "e"), ("C#", "e"),
]


def chip_row(items, y):
    x, parts, h = 0, [], 48
    for label, lv in items:
        w = round(len(label) * 9.7 + 62)
        col = LEVEL[lv]
        parts.append(
            f'<g transform="translate({x} {y})"><rect width="{w}" height="{h}" rx="24" fill="#fff" fill-opacity=".04" stroke="{col}" stroke-opacity=".55"/>'
            f'<circle cx="26" cy="{h / 2}" r="5" fill="{col}"/>'
            f'<text x="42" y="{h / 2 + 5.5}" font-family="{SANS}" font-size="16" font-weight="600" fill="{TEXT}">{esc(label)}</text></g>'
        )
        x += w + 16
    return "".join(parts), x


def stack():
    W, H = 1200, 262
    r1, w1 = chip_row(ROW_WEB, 34)
    r2, w2 = chip_row(ROW_DATA, 106)
    d1, d2 = w1 / 55, w2 / 45
    body = f"""
<defs>
  <linearGradient id="fl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>
  <linearGradient id="fr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>
</defs>
<g><animateTransform attributeName="transform" type="translate" from="0 0" to="-{w1} 0" dur="{d1:.1f}s" repeatCount="indefinite"/>
  <g>{r1}</g><g transform="translate({w1} 0)">{r1}</g></g>
<g><animateTransform attributeName="transform" type="translate" from="-{w2} 0" to="0 0" dur="{d2:.1f}s" repeatCount="indefinite"/>
  <g>{r2}</g><g transform="translate({w2} 0)">{r2}</g></g>
<rect x="0" y="0" width="130" height="{H}" fill="url(#fl)"/><rect x="{W - 130}" y="0" width="130" height="{H}" fill="url(#fr)"/>
<line x1="40" y1="178" x2="{W - 40}" y2="178" stroke="#fff" stroke-opacity=".08"/>
<g font-family="{MONO}" font-size="13" fill="{SOFT}">
  <circle cx="330" cy="218" r="5" fill="{CY}"/><text x="346" y="223">comfortable building with</text>
  <circle cx="598" cy="218" r="5" fill="{VI}"/><text x="614" y="223">actively levelling up</text>
  <circle cx="812" cy="218" r="5" fill="{AM}"/><text x="828" y="223">exploring</text>
</g>
"""
    save("stack.svg", svg(W, H, body, "Tech stack: web development, data and ML, tools", rx=26, glows=[(600, 260, 200, VI, 0.13)]))


def meters():
    W, H = 720, 340
    rows = [
        ("Curiosity", 10, CY, False), ("Frontend", 7, CY, False), ("JavaScript", 6, VI, False),
        ("Consistency", 6, VI, True), ("Backend", 5, VI, True), ("Python & ML", 4, PK, True), ("Kazuya combos", 5, AM, False),
    ]
    body = f'<text x="36" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{CY}">CHARACTER SHEET</text>'
    body += f'<text x="{W - 36}" y="44" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">self-assessed · still levelling up</text>'
    body += f'<line x1="36" y1="62" x2="{W - 36}" y2="62" stroke="#fff" stroke-opacity=".08"/>'
    y, bx, bw = 98, 196, 400
    for i, (lab, v, col, rising) in enumerate(rows):
        tgt = round(bw * v / 10)
        body += f'<text x="36" y="{y + 5}" font-family="{SANS}" font-size="15.5" font-weight="600" fill="{TEXT}">{esc(lab)}</text>'
        body += f'<rect x="{bx}" y="{y - 6}" width="{bw}" height="12" rx="6" fill="#fff" fill-opacity=".07"/>'
        body += (
            f'<rect x="{bx}" y="{y - 6}" width="0" height="12" rx="6" fill="{col}" filter="url(#glow)">'
            f'<animate attributeName="width" values="0;{tgt};{tgt};0" keyTimes="0;.22;.9;1" dur="9s" begin="{i * 0.12}s" repeatCount="indefinite"/></rect>'
        )
        body += f'<text x="{W - 36}" y="{y + 5}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{SOFT}">{v}/10{" ▲" if rising else ""}</text>'
        y += 34
    save("meters.svg", svg(W, H, body, "Character sheet: self-assessed skill levels", rx=24, glows=[(80, 330, 150, CY, 0.12)]))


def titanic():
    W, H = 480, 340
    r, c = 72, 2 * 3.14159265 * 72
    off = c * (1 - 0.799)
    body = f"""
<defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CY}"/><stop offset=".55" stop-color="{VI}"/><stop offset="1" stop-color="{PK}"/></linearGradient></defs>
<text x="32" y="44" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{PK}">ML CHECKPOINT · TITANIC</text>
<line x1="32" y1="62" x2="{W - 32}" y2="62" stroke="#fff" stroke-opacity=".08"/>
<g transform="rotate(-90 240 150)">
  <circle cx="240" cy="150" r="{r}" stroke="#fff" stroke-opacity=".08" stroke-width="14"/>
  <circle cx="240" cy="150" r="{r}" stroke="url(#rg)" stroke-width="14" stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}" filter="url(#glow)">
    <animate attributeName="stroke-dashoffset" values="{c:.1f};{off:.1f};{off:.1f};{c:.1f}" keyTimes="0;.25;.9;1" dur="9s" repeatCount="indefinite"/>
  </circle>
</g>
<text x="240" y="162" text-anchor="middle" font-family="{SANS}" font-size="40" font-weight="800" fill="{TEXT}">79.9%</text>
<text x="240" y="186" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{MUTED}">TEST ACCURACY</text>
<text x="240" y="260" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{TEXT}">Logistic Regression + feature standardisation</text>
<text x="240" y="284" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{SOFT}">Held-out test split · a learning checkpoint,</text>
<text x="240" y="303" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{SOFT}">not a claim of production ML experience.</text>
"""
    save("titanic.svg", svg(W, H, body, "Titanic experiment: about 79.9 percent accuracy with logistic regression", rx=24, glows=[(240, 150, 130, VI, 0.20)]))


# ══════════════════════════════════════════════════════════════════════════
# PROJECT CARDS
# ══════════════════════════════════════════════════════════════════════════
PROJECTS = [
    ("zylo", "Zylo", "FULL-STACK SOCIAL PLATFORM",
     "Server-rendered social application focused on connecting routes, views, authentication, and persistent data.",
     ["Node.js", "Express", "EJS", "MySQL"], CY),
    ("lms", "Library Management System", "DESKTOP APP · DATABASE PRACTICE",
     "JavaFX and MySQL project exploring records, member workflows, and database integration.",
     ["Java", "JavaFX", "MySQL"], AM),
    ("ochi", "Ochi Website Clone", "FRONTEND & MOTION EXPERIMENT",
     "A recreation inspired by Ochi.design to practise composition, animation, and polished landing-page interactions.",
     ["React", "GSAP", "Framer Motion"], VI),
    ("grid", "Grid Scroll Animation", "SCROLL INTERACTION EXPERIMENT",
     "An animated grid exploring scroll-driven movement and more expressive browsing experiences.",
     ["JavaScript", "GSAP", "Lenis"], PK),
    ("twogood", "Two Good Website Clone", "WEBSITE RECREATION",
     "Frontend practice with animated sections, scroll interactions, and page composition.",
     ["HTML", "CSS", "JavaScript", "GSAP"], LM),
    ("bubble", "Bubble Game", "BROWSER MINI-GAME",
     "A small JavaScript game and a reminder that learning can be visual, interactive, and fun.",
     ["JavaScript", "HTML", "CSS"], BL),
]


def project_card(i, key, title, kind, desc, tags, col):
    W, H = 580, 280
    per = 2 * (W + H) - 8 * 22
    lines = wrap_text(desc, 54)
    body = f"""
<text x="36" y="50" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{MUTED}"><tspan fill="{col}" font-weight="700">0{i + 1}</tspan>  /  {esc(kind)}</text>
<text x="{W - 36}" y="50" text-anchor="end" font-family="{MONO}" font-size="12.5" letter-spacing="1.5" fill="{TEXT}" fill-opacity=".8">VIEW SOURCE ↗</text>
<text x="36" y="102" font-family="{SANS}" font-size="31" font-weight="800" letter-spacing="-.6" fill="{TEXT}">{esc(title)}</text>
"""
    for j, ln in enumerate(lines[:3]):
        body += f'<text x="36" y="{140 + j * 23}" font-family="{SANS}" font-size="15" fill="{SOFT}">{esc(ln)}</text>'
    x = 36
    for t in tags:
        w = round(len(t) * 7.6 + 26)
        body += (
            f'<rect x="{x}" y="{H - 62}" width="{w}" height="28" rx="14" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".40"/>'
            f'<text x="{x + w / 2}" y="{H - 43.5}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{col}">{esc(t)}</text>'
        )
        x += w + 10
    body += (
        f'<rect x="1.2" y="1.2" width="{W - 2.4}" height="{H - 2.4}" rx="23" stroke="{col}" stroke-width="2.4" stroke-linecap="round" '
        f'stroke-dasharray="150 {per}" filter="url(#glow)"><animate attributeName="stroke-dashoffset" from="0" to="-{per + 150}" dur="7s" begin="-{i * 1.3}s" repeatCount="indefinite"/></rect>'
    )
    save(f"project-{key}.svg", svg(W, H, body, f"{title}: {kind.title()}", rx=24, glows=[(W - 40, 20, 130, col, 0.16)]))


# ══════════════════════════════════════════════════════════════════════════
# ROADMAP
# ══════════════════════════════════════════════════════════════════════════
def roadmap():
    W, H = 1200, 392
    top = "M 80 118 H 790 C 900 118 920 196 1000 196"
    bot = "M 80 286 H 700 C 860 286 890 196 1000 196"
    node = lambda x, y, st: {
        "done": f'<circle cx="{x}" cy="{y}" r="11" fill="{CY}" filter="url(#glow)"/><path d="M{x - 4.5} {y} l3.2 3.4 l6-6.6" stroke="#06101A" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
        "now": pulse_dot(x, y, VI, r=10, dur=2.6),
        "next": f'<circle cx="{x}" cy="{y}" r="10" fill="{PANEL}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="3 3"/>',
    }[st]
    web = [(80, "HTML · CSS · JS", "done", "comfortable"), (310, "React", "now", "levelling up"),
           (540, "Node + Express", "now", "levelling up"), (770, "MongoDB + Auth", "now", "levelling up")]
    ai = [(80, "Python + pandas", "now", "levelling up"), (390, "scikit-learn", "now", "levelling up"),
          (700, "NLP + AI features", "next", "up next")]
    body = f"""
<text x="36" y="46" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{CY}">WEB TRACK</text>
<text x="36" y="214" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{PK}">AI / ML TRACK</text>
<path d="{top}" stroke="#fff" stroke-opacity=".12" stroke-width="2.5"/>
<path d="{bot}" stroke="#fff" stroke-opacity=".12" stroke-width="2.5" stroke-dasharray="1 0"/>
<path d="{top}" stroke="{CY}" stroke-opacity=".55" stroke-width="2.5" stroke-dasharray="120 900"><animate attributeName="stroke-dashoffset" from="0" to="-1020" dur="6s" repeatCount="indefinite"/></path>
<path d="{bot}" stroke="{PK}" stroke-opacity=".55" stroke-width="2.5" stroke-dasharray="120 900"><animate attributeName="stroke-dashoffset" from="0" to="-1020" dur="6s" begin="-3s" repeatCount="indefinite"/></path>
<circle r="5.5" fill="{CY}" filter="url(#glow)"><animateMotion dur="7s" repeatCount="indefinite" path="{top}"/></circle>
<circle r="5.5" fill="{PK}" filter="url(#glow)"><animateMotion dur="7s" begin="-3.5s" repeatCount="indefinite" path="{bot}"/></circle>
"""
    for x, lab, st, sub in web:
        body += node(x, 118, st)
        body += f'<text x="{x}" y="86" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">{esc(lab)}</text>'
        body += f'<text x="{x}" y="152" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{sub}</text>'
    for x, lab, st, sub in ai:
        body += node(x, 286, st)
        body += f'<text x="{x}" y="254" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">{esc(lab)}</text>'
        body += f'<text x="{x}" y="320" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{sub}</text>'
    body += f"""
<g transform="translate(1046 196)">
  <circle r="40" stroke="{AM}" stroke-opacity=".55" stroke-dasharray="4 7"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>
  <circle r="22" fill="{AM}" fill-opacity=".18"/>
  <circle r="12" fill="{AM}" filter="url(#glow)"><animate attributeName="r" values="12;14.5;12" dur="2.4s" repeatCount="indefinite"/></circle>
</g>
<text x="1046" y="266" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{AM}">SHIP A REAL</text>
<text x="1046" y="286" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="{AM}">PRODUCT</text>
<g font-family="{MONO}" font-size="12.5" fill="{SOFT}">
  <circle cx="420" cy="366" r="5" fill="{CY}"/><text x="434" y="370">comfortable</text>
  <circle cx="568" cy="366" r="5" fill="{VI}"/><text x="582" y="370">levelling up now</text>
  <circle cx="742" cy="366" r="5" fill="{PANEL}" stroke="{MUTED}" stroke-dasharray="2 2"/><text x="756" y="370">up next</text>
</g>
"""
    save("roadmap.svg", svg(W, H, body, "Roadmap: web and AI tracks converging on shipping a real product", rx=26,
                            glows=[(1046, 196, 170, AM, 0.14), (200, 90, 150, CY, 0.10)]))


# ══════════════════════════════════════════════════════════════════════════
# WORKSHOP
# ══════════════════════════════════════════════════════════════════════════
IDEAS = [
    ("inventory", "Inventory OS", "Offline-first inventory & POS for small shops: stock, barcodes, expiry alerts, receipts, and staff roles. Built to stay dependable without internet.", CY),
    ("habit", "Habit & Dev Tools", "Habit tracking, daily planning, and a developer task tracker. Made to cut friction, not to add more organising.", PK),
    ("fyp", "Problem-First FYP", "A BSCS final-year product that solves a real student or workflow problem. Users first, tech second, and AI only when it adds real capability.", AM),
]


def idea(i, key, title, desc, col):
    W, H = 400, 268
    body = f"""
<rect x="32" y="30" width="112" height="26" rx="13" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>
{pulse_dot(50, 43, col, r=3.5, delay=i * .7)}
<text x="62" y="48" font-family="{MONO}" font-size="11.5" letter-spacing="2" fill="{col}">CONCEPT</text>
<text x="32" y="102" font-family="{SANS}" font-size="26" font-weight="800" letter-spacing="-.4" fill="{TEXT}">{esc(title)}</text>
"""
    for j, ln in enumerate(wrap_text(desc, 40)[:5]):
        body += f'<text x="32" y="{136 + j * 22}" font-family="{SANS}" font-size="14.5" fill="{SOFT}">{esc(ln)}</text>'
    body += f'<text x="32" y="{H - 24}" font-family="{MONO}" font-size="11.5" letter-spacing="1.5" fill="{MUTED}">NOT A LAUNCH · AN IDEA TO BUILD</text>'
    body += scanline(W, H, color=col, dur=5 + i, delay=i)
    save(f"idea-{key}.svg", svg(W, H, body, f"Concept: {title}", rx=24, glows=[(W - 30, 10, 110, col, 0.16)]))


# ══════════════════════════════════════════════════════════════════════════
# OUTSIDE THE EDITOR
# ══════════════════════════════════════════════════════════════════════════
def tile_icon(kind, col):
    base = f'<rect width="52" height="52" rx="15" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
    g = {
        "fight": f'<path d="M15 15 L37 37 M37 15 L15 37" stroke="{col}" stroke-width="4" stroke-linecap="round"/>',
        "game": f'<rect x="21" y="11" width="10" height="30" rx="3" fill="{col}"/><rect x="11" y="21" width="30" height="10" rx="3" fill="{col}"/>',
        "movie": f'<path d="M20 14 L39 26 L20 38 Z" fill="{col}" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>',
        "curious": f'<circle cx="23" cy="23" r="9.5" stroke="{col}" stroke-width="4"/><path d="M30.5 30.5 L39 39" stroke="{col}" stroke-width="4" stroke-linecap="round"/>',
    }[kind]
    return f'<g transform="translate(26 26)" filter="url(#glow)">{base}{g}</g>'


def outside():
    tiles = [
        ("fight", "Fighting-game arc", "Tekken is movement, timing, and execution. Kazuya is my main.", CY),
        ("game", "Gaming", "Free Fire, Clash of Clans, Clash Royale, and whatever's next.", VI),
        ("movie", "Anime & movies", "High-energy action, darker stories, and films with emotional damage.", PK),
        ("curious", "Curiosity mode", "I like knowing how tools work under the hood, not just which button to press.", AM),
    ]
    W, H, tw, gap = 1200, 214, 282, 24
    body = ""
    for i, (ic, t, d, col) in enumerate(tiles):
        x = i * (tw + gap)
        body += f"""
<g transform="translate({x} 0)">
  <rect x=".5" y=".5" width="{tw - 1}" height="{H - 1}" rx="22" fill="{PANEL}" stroke="{BORDER}"/>
  <circle cx="{tw - 20}" cy="14" r="70" fill="{col}" fill-opacity=".14" filter="url(#blur)"/>
  {tile_icon(ic, col)}
  <text x="26" y="116" font-family="{SANS}" font-size="19" font-weight="800" fill="{TEXT}">{esc(t)}</text>"""
        for j, ln in enumerate(wrap_text(d, 31)[:3]):
            body += f'<text x="26" y="{142 + j * 20}" font-family="{SANS}" font-size="14" fill="{SOFT}">{esc(ln)}</text>'
        body += f'<rect x="26" y="{H - 20}" width="40" height="3" rx="1.5" fill="{col}"/></g>'
    save("outside.svg", svg(W, H, body, "Outside the editor: Tekken, gaming, anime and movies, curiosity", frame=False))


# ══════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════
def footer():
    W, H = 1200, 230
    wave = lambda y, a, b: (
        f"M0 {y} C 200 {y - a}, 400 {y + a}, 600 {y} S 1000 {y - b}, 1200 {y} V{H} H0 Z",
        f"M0 {y} C 200 {y + a}, 400 {y - a}, 600 {y} S 1000 {y + b}, 1200 {y} V{H} H0 Z",
    )
    layers = [(160, 26, 20, CY, .13, 9), (178, 22, 28, VI, .17, 12), (198, 18, 16, PK, .20, 15)]
    body = ""
    for y, a, b, col, op, dur in layers:
        d1, d2 = wave(y, a, b)
        body += f'<path d="{d1}" fill="{col}" fill-opacity="{op}"><animate attributeName="d" values="{d1};{d2};{d1}" dur="{dur}s" repeatCount="indefinite"/></path>'
    body += f"""
<text x="600" y="62" text-anchor="middle" font-family="{MONO}" font-size="24" font-weight="700" fill="{CY}">while (alive) {{ learn(); build(); improve(); }}</text>
<text x="600" y="98" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{SOFT}">Thanks for stopping by. Pick a repo, explore the code, and let's keep building.</text>
<text x="600" y="128" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{PK}">STILL LEARNING · STILL BUILDING · STILL GOING</text>
"""
    save("footer.svg", svg(W, H, body, "Footer: still learning, still building, still going", rx=26, glows=[(600, 40, 220, VI, 0.20)]))


if __name__ == "__main__":
    hero()
    quote()
    for f, label, col in [
        ("btn-projects.svg", "MY PROJECTS", CY), ("btn-repos.svg", "ALL REPOS", VI),
        ("btn-linkedin.svg", "LINKEDIN", BL), ("btn-itch.svg", "ITCH.IO", PK),
    ]:
        button(f, label, col)
    for f, n, t, h, c in [
        ("h-about.svg", "01", "About", "whoami --verbose", CY),
        ("h-stack.svg", "02", "Stack & Skills", "honest levels, always", VI),
        ("h-projects.svg", "03", "Selected Builds", "click a card → source", PK),
        ("h-roadmap.svg", "04", "Roadmap", "two tracks, one goal", AM),
        ("h-workshop.svg", "05", "The Workshop", "ideas, not fake launches", LM),
        ("h-stats.svg", "06", "Control Room", "live from GitHub", BL),
        ("h-outside.svg", "07", "Outside the Editor", "player two mode", PK),
        ("h-connect.svg", "08", "Connect & Build", "say hello", CY),
    ]:
        section_header(f, n, t, h, c)
    terminal()
    status()
    stack()
    meters()
    titanic()
    for i, p in enumerate(PROJECTS):
        project_card(i, *p)
    roadmap()
    for i, d in enumerate(IDEAS):
        idea(i, *d)
    outside()
    footer()
    print("Generated", len(os.listdir(OUT)), "assets in", OUT)
