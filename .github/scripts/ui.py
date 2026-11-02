"""Shared design helpers for the Malik Zain profile README.

Palette, fonts and tiny SVG/SMIL helpers. Fonts (Unbounded + Hanken Grotesk, both SIL OFL) are
subsetted to the glyphs each SVG really uses and embedded as base64, because GitHub renders README
images in <img> mode where external fonts never load.
"""
import base64
import io
import os
import re
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "fonts"))

# palette, straight from the portfolio's :root block
CB, CB2, TG, TG2 = "#2b3cff", "#aab2ff", "#ff6a2b", "#ffb48f"
MT, LC, YE, PK = "#8ef0c8", "#cdbbff", "#ffe27a", "#ffb3d1"
INK, SN, WHITE = "#0c0c16", "#f4f4ef", "#ffffff"

FILES = {"d": "unbounded-latin-800-normal.woff2", "f4": "hanken-grotesk-latin-400-normal.woff2", "f6": "hanken-grotesk-latin-600-normal.woff2"}
FAM = {"d": ("Unbounded", 800), "f4": ("Hanken Grotesk", 400), "f6": ("Hanken Grotesk", 600)}
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

_F = {}


def _font(key):
    if key not in _F:
        f = TTFont(os.path.join(FONT_DIR, FILES[key]))
        _F[key] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _F[key]


def adv(key, text):
    cm, hm, upm = _font(key)
    sp = cm.get(32)
    return sum(hm[cm.get(ord(c), sp)][0] for c in text) / upm


def tw(key, text, size, ls=0.0):
    """Rendered width of a string in px."""
    return adv(key, text) * size + ls * len(text)


def wrap(key, text, size, maxw, ls=0.0):
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if cur and tw(key, t, size, ls) > maxw:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def typo(s):
    """Typographic punctuation for text people read."""
    s = re.sub(r'(^|[\s(\[])"', lambda m: m.group(1) + "\u201c", s)
    s = s.replace('"', "\u201d")
    return s.replace("'", "\u2019")


# ───────────────────────── SMIL helpers ─────────────────────────
def anim(attr, values, dur, key_times=None, begin="0s", repeat="indefinite", discrete=False, freeze=False, spline=None):
    v = ";".join(str(x) for x in values)
    kt = f' keyTimes="{";".join(f"{k:.4f}" for k in key_times)}"' if key_times else ""
    cm = ' calcMode="discrete"' if discrete else (f' calcMode="spline" keySplines="{";".join([spline] * (len(values) - 1))}"' if spline else "")
    rp = "" if repeat is None else f' repeatCount="{repeat}"'
    fz = ' fill="freeze"' if freeze else ""
    return f'<animate attributeName="{attr}" values="{v}"{kt}{cm} dur="{dur}s" begin="{begin}"{rp}{fz}/>'


def anim_t(kind, values, dur, key_times=None, begin="0s", repeat="indefinite", freeze=False, spline=None):
    v = ";".join(values)
    kt = f' keyTimes="{";".join(f"{k:.4f}" for k in key_times)}"' if key_times else ""
    cm = f' calcMode="spline" keySplines="{";".join([spline] * (len(values) - 1))}"' if spline else ""
    rp = "" if repeat is None else f' repeatCount="{repeat}"'
    fz = ' fill="freeze"' if freeze else ""
    return f'<animateTransform attributeName="transform" type="{kind}" values="{v}"{kt}{cm} dur="{dur}s" begin="{begin}"{rp}{fz} additive="sum"/>'


def window(n_states, i, dur, on=1, off=0):
    """opacity (or any value) that is `on` during state i of n and `off` otherwise (discrete)."""
    return anim("opacity", [on if k == i else off for k in range(n_states)], dur, [k / n_states for k in range(n_states)], discrete=True)


def track(pts, T):
    """pts = [(seconds, value), ...] -> (values, keyTimes) for a looping animation of length T."""
    pts = sorted(pts, key=lambda p: p[0])
    return [v for _, v in pts], [t / T for t, _ in pts]


def smooth(vals, e=0.04):
    """Hold each of n values for 1/n of the loop, easing to the next during the last fraction e. Returns (values, keyTimes)."""
    n = len(vals)
    pts = [(0.0, vals[0])]
    for i in range(n):
        pts.append(((i + 1) / n - e, vals[i]))
        pts.append(((i + 1) / n, vals[(i + 1) % n]))
    return [v for _, v in pts], [t for t, _ in pts]


# ───────────────────────── SVG document ─────────────────────────
class Doc:
    def __init__(self, W, H, title, desc="", natural=True):
        self.W, self.H, self.title, self.desc, self.natural = W, H, title, desc, natural
        self.body, self.defs = [], []
        self.chars = {"d": set(" "), "f4": set(" "), "f6": set(" ")}
        self._id = 0

    def uid(self, p="i"):
        self._id += 1
        return f"{p}{self._id}"

    def add(self, s):
        self.body.append(s)

    def rec(self, f, t):
        for c in t:
            self.chars[f].add(c)

    # text: f in d | f4 | f6.  size in px, ls (letter spacing) in px
    def text(self, x, y, t, f="f4", size=18, fill=INK, anchor="start", op=None, ls=None, extra="", fix=True, raw=None):
        if fix and raw is None:
            t = typo(t)
        plain = re.sub(r"<[^>]+>", "", raw) if raw is not None else t
        plain = plain.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if f != "m":
            self.rec(f, plain)
        cls = {"d": "d", "f4": "f", "f6": "f b", "m": "m"}[f]
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        o = "" if op is None else f' fill-opacity="{op}"'
        l = f' letter-spacing="{ls:.2f}"' if ls else ""
        inner = raw if raw is not None else escape(t)
        return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" fill="{fill}"{o}{a}{l} {extra}>{inner}</text>'

    def T(self, *a, **k):
        self.add(self.text(*a, **k))

    def lines(self, x, y, ls_, f, size, fill, lh, anchor="start", op=None, ls=None, extra=""):
        """Emit several lines; returns y after the block."""
        for i, l in enumerate(ls_):
            self.T(x, y + i * lh, l, f, size, fill, anchor, op, ls, extra)
        return y + len(ls_) * lh

    def _fontcss(self):
        css = ""
        for key, chars in self.chars.items():
            txt = "".join(sorted(chars))
            f = TTFont(os.path.join(FONT_DIR, FILES[key]))
            cm = f.getBestCmap()
            miss = [c for c in txt if ord(c) not in cm]
            if miss:
                print(f"  ! {self.title[:30]}: glyphs missing in {key}: {miss}")
            o = subset.Options()
            o.flavor = "woff2"
            o.layout_features = ["kern", "liga", "calt"]
            o.notdef_outline = False
            s = subset.Subsetter(o)
            s.populate(text=txt)
            s.subset(f)
            buf = io.BytesIO()
            f.flavor = "woff2"
            f.save(buf)
            fam, wt = FAM[key]
            css += f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff2;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff2')}}"
        css += ".d{font-family:'Unbounded','Arial Black','Helvetica Neue',Arial,sans-serif;font-weight:800}"
        css += ".f{font-family:'Hanken Grotesk','Helvetica Neue',Arial,system-ui,sans-serif;font-weight:400}.b{font-weight:600}"
        css += f".m{{font-family:{MONO}}}"
        return css

    def render(self):
        wh = f' width="{self.W}" height="{self.H}"' if self.natural else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"{wh} viewBox="0 0 {self.W} {self.H}" role="img" aria-label="{escape(self.title, {chr(34): "&quot;"})}">'
            f"<title>{escape(self.title)}</title>"
            + (f"<desc>{escape(self.desc)}</desc>" if self.desc else "")
            + f"<defs><style>{self._fontcss()}</style>{''.join(self.defs)}</defs>"
            + "".join(self.body)
            + "</svg>"
        )

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        s = self.render()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(s)
        print(f"  {os.path.relpath(path)}  {len(s) / 1024:.1f} KB")


def tile(doc, fill, rx=44, stroke=None, W=None, H=None, rx_bottom=None):
    """Full-bleed rounded tile background."""
    W = W or doc.W
    H = H or doc.H
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    doc.add(f'<rect x="{1 if stroke else 0}" y="{1 if stroke else 0}" width="{W - (2 if stroke else 0)}" height="{H - (2 if stroke else 0)}" rx="{rx}" fill="{fill}"{st}/>')


def arrow(x, y, color, size=9, w=2.4):
    """A small → drawn as a path (no glyph needed). x,y = centre of shaft start."""
    return (f'<path d="M{x} {y}H{x + size * 1.7:.1f}M{x + size * 1.7 - size * .75:.1f} {y - size * .75:.1f}L{x + size * 1.7:.1f} {y}L{x + size * 1.7 - size * .75:.1f} {y + size * .75:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def section_header(d, title, sub, x, y, fg=INK, w=800, tsize=60, sub_w=760):
    """Section title (Unbounded) + sub paragraph. Returns the y just below the block (last baseline + one line)."""
    ls = -0.04 * tsize
    lh = tsize * 1.04
    lines = wrap("d", title, tsize, w, ls)
    d.lines(x, y + tsize, lines, "d", tsize, fg, lh, ls=ls)
    last = y + tsize + (len(lines) - 1) * lh
    return d.lines(x, last + 46, wrap("f4", typo(sub), 22, sub_w), "f4", 22, fg, 33, op=0.82)
