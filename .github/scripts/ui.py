"""ui.py — shared design system for Zain's profile ("Workbench"): palette, type, SVG shell, helpers."""
import html

BG, SURF, SURF2, LINE = "#0B0C0F", "#111317", "#171A20", "#272B33"
TX, SOFT, MUT = "#F3F0EA", "#BDB9B0", "#80848E"
OR, MINT, AMB, SKY, VIO, ROSE = "#FF6B3D", "#4ADE9C", "#F5C451", "#7AB7FF", "#B39DFF", "#FF7A90"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Times New Roman',serif"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return html.escape(str(s), quote=False)


def svg(w, h, body, title, defs="", r=18, frame=True, border=LINE, fill=SURF, grid=False):
    shell = ""
    if frame:
        g = f'<rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#fade)"/>' if grid else ""
        shell = f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{fill}"/>{g}{body}</g><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r}" stroke="{border}"/>'
    else:
        shell = f"<g>{body}</g>"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
<linearGradient id="og" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{OR}"/><stop offset="1" stop-color="#FFB24D"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#fff" stroke-opacity=".05"/></pattern>
<radialGradient id="fg" cx=".7" cy=".4" r=".8"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="{w}" height="{h}" fill="url(#fg)"/></mask>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="card"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
{defs}
</defs>
{shell}
</svg>
"""


# ── animation helpers ──
def A(attr, values, kt=None, dur=6, begin=0, calc=None, extra=""):
    v = ";".join(str(x) for x in values)
    k = f' keyTimes="{";".join(f"{t:.4f}" for t in kt)}"' if kt else ""
    c = f' calcMode="{calc}"' if calc else ""
    return f'<animate attributeName="{attr}" values="{v}"{k}{c} dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'


def AT(kind, values, kt=None, dur=6, begin=0, extra=""):
    v = ";".join(str(x) for x in values)
    k = f' keyTimes="{";".join(f"{t:.4f}" for t in kt)}"' if kt else ""
    return f'<animateTransform attributeName="transform" type="{kind}" values="{v}"{k} dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'


def window(t0, t1, T, f=0.2):
    return [0, 0, 1, 1, 0, 0], [0, t0 / T, (t0 + f) / T, (t1 - f) / T, t1 / T, 1]


def blink(dur=1.2):
    return A("opacity", [1, 1, 0, 0], [0, 0.5, 0.5, 1], dur=dur)


def pulse(cx, cy, color, r=4, dur=2.0, delay=0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity=".4"><animate attributeName="r" values="{r};{r * 3};{r}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".5;0;.5" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def tick(w, y, color=OR, dur=6, delay=0):
    """thin light travelling along a hairline"""
    return (f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{LINE}"/><rect x="-120" y="{y - 1}" width="120" height="2" fill="{color}">'
            f'<animate attributeName="x" from="-120" to="{w}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></rect>')


# ── text helpers ──
def serif(x, y, t, size, fill=TX, anchor="start", italic=False, weight=400, extra=""):
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SERIF}" font-size="{size}" font-weight="{weight}"{st} fill="{fill}" {extra}>{esc(t)}</text>'


def sans(x, y, t, size=15, fill=SOFT, anchor="start", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{esc(t)}</text>'


def mono(x, y, t, size=12, fill=MUT, anchor="start", ls=0, extra=""):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" {extra}>{esc(t)}</text>'


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


def fit(text, maxw, base, factor=0.56):
    """largest font size <= base so that text fits maxw (conservative for fallback fonts)"""
    return min(base, int(maxw / (max(1, len(text)) * factor)))


def chip(x, y, t, col, fs=11, h=22, fill=True):
    w = round(len(t) * fs * 0.64 + 18)
    f = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{col if fill else "none"}" fill-opacity="{.12 if fill else 0}" stroke="{col}" stroke-opacity=".55"/>'
    return f + mono(x + w / 2, y + h / 2 + fs * .35, t, fs, col, "middle"), w


def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
