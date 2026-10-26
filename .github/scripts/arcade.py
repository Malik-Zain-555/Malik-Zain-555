"""arcade.py — shared look & feel for Zain's profile (palette, fonts, SVG shell, helpers).
Used by build_assets.py, fight.py and stats.py so every graphic matches."""
import html

INK, PANEL, EDGE = "#07060B", "#0E0B14", "#2B2040"
RED, ORG, GOLD, PUR, CYA = "#FF2E4D", "#FF8A1F", "#FFD23F", "#A855F7", "#22E5FF"
PINK, LIME, BLU = "#FF5FA2", "#A3E635", "#5AA9FF"
WHT, SOFT, DIM = "#F5F3FF", "#C9C3DE", "#8F88AD"
DISP = "Impact,Haettenschweiler,'Arial Narrow Bold','Franklin Gothic Heavy','Arial Black',sans-serif"
SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return html.escape(str(s), quote=False)


def poly(w, h, c=14):
    """Chamfered panel outline (top-left and bottom-right corners cut)."""
    return f"{c},0 {w},0 {w},{h - c} {w - c},{h} 0,{h} 0,{c}"


def svg(w, h, body, title, defs="", c=14, frame=True, glows=(), border=EDGE):
    P = poly(w, h, c)
    g = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity="{o}" filter="url(#blur)"/>'
        for x, y, r, col, o in glows
    )
    head = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF3B0"/><stop offset=".45" stop-color="{GOLD}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="hot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset=".55" stop-color="{ORG}"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<linearGradient id="cool" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PUR}"/><stop offset="1" stop-color="{CYA}"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.3" fill="#000" fill-opacity=".30"/></pattern>
<pattern id="haz" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="16" fill="{GOLD}"/><rect x="8" width="8" height="16" fill="{INK}"/></pattern>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="48"/></filter>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="card"><polygon points="{P}"/></clipPath>
{defs}
</defs>
"""
    if frame:
        inner = (
            f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{PANEL}"/>{g}{body}'
            f'<rect width="{w}" height="{h}" fill="url(#scan)" opacity=".55"/></g>'
            f'<polygon points="{P}" stroke="{border}" stroke-width="1.5"/>'
        )
    else:
        inner = f"<g>{body}</g>"
    return head + inner + "\n</svg>\n"


# ── animation helpers ──────────────────────────────────────────────────────
def A(attr, values, kt=None, dur=6, begin=0, calc=None, extra=""):
    v = ";".join(str(x) for x in values)
    k = f' keyTimes="{";".join(f"{t:.4f}" for t in kt)}"' if kt else ""
    c = f' calcMode="{calc}"' if calc else ""
    return f'<animate attributeName="{attr}" values="{v}"{k}{c} dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'


def AT(kind, values, kt=None, dur=6, begin=0, extra=""):
    v = ";".join(str(x) for x in values)
    k = f' keyTimes="{";".join(f"{t:.4f}" for t in kt)}"' if kt else ""
    return f'<animateTransform attributeName="transform" type="{kind}" values="{v}"{k} dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'


def window(t0, t1, T, f=0.12):
    """opacity values/keyTimes: invisible, fade in at t0, hold, fade out by t1, invisible."""
    return [0, 0, 1, 1, 0, 0], [0, t0 / T, (t0 + f) / T, (t1 - f) / T, t1 / T, 1]


def blink(dur=1.2):
    return A("opacity", [1, 1, 0, 0], [0, 0.5, 0.5, 1], dur=dur)


def sweep(w, h, color="url(#hot)", dur=6, delay=0):
    return (f'<rect x="-220" y="{h - 3}" width="220" height="3" fill="{color}" opacity=".9">'
            f'<animate attributeName="x" from="-220" to="{w}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></rect>')


# ── text helpers ───────────────────────────────────────────────────────────
def disp(x, y, t, size, fill="url(#gold)", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{DISP}" font-size="{size}" '
            f'font-style="italic" letter-spacing=".6" fill="{fill}" {extra}>{esc(t)}</text>')


def mono(x, y, t, size=13, fill=DIM, anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="{size}" '
            f'letter-spacing="{ls}" fill="{fill}" {extra}>{esc(t)}</text>')


def sans(x, y, t, size=15, fill=SOFT, anchor="start", weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SANS}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{esc(t)}</text>')


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


def fit(text, maxw, base, factor=0.7):
    """Font size that keeps DISP text inside maxw even if Impact is missing and a wider font is used."""
    return min(base, int(maxw / (len(text) * factor)))


def pulse(cx, cy, color, r=4, dur=2.0, delay=0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity=".4">'
            f'<animate attributeName="r" values="{r};{r * 3};{r}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".5;0;.5" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
