"""Shared design system and SVG builder used by every renderer.

Every SVG is self-contained (fonts embedded, no external references, no script) because
GitHub displays README images through <img>, where only inline CSS animation runs.
"""
from __future__ import annotations

import base64
import io
import json
import re
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
THEMES = ("dark", "light")


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


TOKENS = load_json("config/design-tokens.json")
LAYOUT = TOKENS["layout"]
MOTION = TOKENS["motion"]
RADIUS = TOKENS["radius"]

FONT_FILES = {
    ("sans", w): f"assets/fonts/inter-latin-{w}-normal.woff2" for w in (400, 500, 600, 700)
} | {("mono", w): f"assets/fonts/jetbrains-mono-latin-{w}-normal.woff2" for w in (400, 700)}

_INVALID_XML = re.compile("[^\t\n\r\x20-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]")


def esc(value) -> str:
    """Escape text and attribute values; characters XML cannot carry are dropped."""
    text = _INVALID_XML.sub("", str(value))
    for raw, safe in (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;"), ("'", "&#39;")):
        text = text.replace(raw, safe)
    return text


def safe_url(url: str | None) -> str | None:
    """Only absolute https links ever reach the README."""
    if url and re.fullmatch(r"https://[A-Za-z0-9.-]+(?::\d+)?(?:/[A-Za-z0-9._~/%?#=&+-]*)?", url):
        return url
    return None


def num(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".") or "0"


@lru_cache(maxsize=None)
def _metrics(family: str, weight: int):
    font = TTFont(ROOT / FONT_FILES[(family, weight)])
    return font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm


def text_width(value: str, size: float, weight: int = 400, family: str = "sans", spacing: float = 0) -> float:
    cmap, hmtx, upm = _metrics(family, weight)
    fallback = hmtx[cmap[ord("n")]][0]
    units = sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else fallback for c in value)
    return units * size / upm + spacing * len(value)


def wrap(value: str, max_width: float, size: float, weight: int = 400) -> list[str]:
    lines, current = [], ""
    for word in value.split():
        candidate = f"{current} {word}".strip()
        if current and text_width(candidate, size, weight) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    return lines + [current] if current else lines


@lru_cache(maxsize=None)
def _font_face(family: str, weight: int, chars: str) -> str:
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "tnum"]
    options.name_IDs = []
    options.notdef_outline = True
    font = TTFont(ROOT / FONT_FILES[(family, weight)], recalcTimestamp=False)
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=chars)
    subsetter.subset(font)
    buffer = io.BytesIO()
    font.flavor = "woff2"
    font.save(buffer)
    data = base64.b64encode(buffer.getvalue()).decode("ascii")
    name = TOKENS["type"][family]
    return f"@font-face{{font-family:'{name}';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}"


class Svg:
    def __init__(self, width: float, height: float, theme: str, title: str, desc: str = "",
                 display_width: float | None = None):
        self.w, self.h, self.theme = width, height, theme
        self.c = TOKENS["themes"][theme]
        self.title, self.desc = title, desc or title
        self.display_width = display_width or width
        self.body: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = []
        self._chars: dict[tuple[str, int], set[str]] = {}
        self._standard_defs()

    # -- primitives ---------------------------------------------------------
    def add(self, markup: str) -> None:
        self.body.append(markup)

    def use_font(self, value: str, weight: int, family: str) -> None:
        self._chars.setdefault((family, weight), set()).update(_INVALID_XML.sub("", value))

    def text(self, x: float, y: float, value: str, size: float, *, weight: int = 400,
             family: str = "sans", fill: str = "text", spacing: float = 0, anchor: str = "start",
             extra: str = "") -> str:
        self.use_font(value, weight, family)
        colour = self.c.get(fill, fill)
        attrs = f' letter-spacing="{num(spacing)}"' if spacing else ""
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        return (f'<text class="{family}" x="{num(x)}" y="{num(y)}" font-size="{num(size)}" '
                f'font-weight="{weight}" fill="{colour}"{attrs}{" " + extra if extra else ""}>{esc(value)}</text>')

    def rect(self, x, y, w, h, r=0, fill="none", stroke=None, extra="") -> str:
        s = f' stroke="{self.c.get(stroke, stroke)}"' if stroke else ""
        return (f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{num(r)}" '
                f'fill="{self.c.get(fill, fill)}"{s}{" " + extra if extra else ""}/>')

    def line(self, x1, y1, x2, y2, stroke="border", width=1, extra="") -> str:
        return (f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" '
                f'stroke="{self.c.get(stroke, stroke)}" stroke-width="{num(width)}"{" " + extra if extra else ""}/>')

    def panel(self, x, y, w, h, r=None) -> str:
        """Liquid-glass surface: graphite fill, top reflection, hairline lit from above."""
        r = RADIUS["card"] if r is None else r
        return (
            self.rect(x + .5, y + .5, w - 1, h - 1, r, "url(#surface)")
            + self.rect(x + .5, y + .5, w - 1, h - 1, r, "url(#gloss)")
            + self.rect(x + .5, y + .5, w - 1, h - 1, r, "none", "url(#edge)")
        )

    def section_header(self, number: str, title: str, aside: str) -> None:
        """'01 / IDENTITY ------ ASIDE' strip drawn at the top of a full-width section."""
        size = 9.5 if self.w >= 600 else 11
        self.add(self.text(1, 14, number, size, weight=700, spacing=.6))
        x = 1 + text_width(number, size, 700, spacing=.6) + 6
        self.add(self.text(x, 14, "/", size, weight=400, fill="secondary"))
        x += 14
        self.add(self.text(x, 14, title, size, weight=700, spacing=.5))
        start = x + text_width(title, size, 700, spacing=.5) + 9
        aside_size = 7.6 if self.w >= 600 else 8
        spacing = 1.2 if self.w >= 600 else .4
        aside_w = text_width(aside, aside_size, 400, "mono", spacing)
        if start + aside_w + 20 < self.w:
            self.add(self.text(self.w - 6, 14, aside, aside_size, family="mono", fill="secondary",
                               spacing=spacing, anchor="end"))
            end = self.w - 6 - aside_w - 9
        else:
            end = self.w - 2
        if end > start:
            self.add(self.rect(start, 10.5, end - start, 1, 0, "url(#rule)"))

    # -- shared defs & motion ----------------------------------------------
    def _standard_defs(self) -> None:
        c = self.c
        gloss, opacity = c["gloss"], float(c["glossOpacity"])
        self.defs.append(
            f'<linearGradient id="surface" x1="0" y1="0" x2="0.35" y2="1">'
            f'<stop offset="0" stop-color="{c["surfaceHigh"]}"/><stop offset="0.55" stop-color="{c["surface"]}"/>'
            f'<stop offset="1" stop-color="{c["background"]}"/></linearGradient>'
            f'<linearGradient id="gloss" x1="0" y1="0" x2="0.25" y2="1">'
            f'<stop offset="0" stop-color="{gloss}" stop-opacity="{num(opacity)}"/>'
            f'<stop offset="0.42" stop-color="{gloss}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c["borderStrong"]}"/><stop offset="1" stop-color="{c["border"]}"/></linearGradient>'
            f'<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c["goldLight"]}"/><stop offset="1" stop-color="{c["gold"]}"/></linearGradient>'
            f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{c["border"]}" stop-opacity="0.35"/>'
            f'<stop offset="0.5" stop-color="{c["borderStrong"]}"/>'
            f'<stop offset="1" stop-color="{c["border"]}" stop-opacity="0.5"/></linearGradient>'
        )
        e, d = MOTION["easing"], MOTION["enter"]
        self.css.append(
            f".rise{{animation:rise {d}s {e} both}}.fade{{animation:fade {d}s ease both}}"
            "@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}"
            "@keyframes fade{from{opacity:0}to{opacity:1}}"
        )

    @staticmethod
    def group(content: str, cls: str = "rise", delay: float = 0) -> str:
        return f'<g class="{cls}" style="animation-delay:{num(delay)}s">{content}</g>'

    def sheen(self, x, y, w, h, r, delay: float = 2.0) -> str:
        """Slow metallic reflection that crosses a surface once per period."""
        key = f"s{len(self.defs)}"
        band = w * .28
        self.defs.append(
            f'<clipPath id="{key}">{self.rect(x, y, w, h, r, "#000")}</clipPath>'
            f'<linearGradient id="{key}g" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{self.c["goldLight"]}" stop-opacity="0"/>'
            f'<stop offset="0.5" stop-color="{self.c["goldLight"]}" stop-opacity="0.07"/>'
            f'<stop offset="1" stop-color="{self.c["goldLight"]}" stop-opacity="0"/></linearGradient>'
        )
        self.css.append(
            f".{key}m{{opacity:0;animation:{key}k {MOTION['sheenPeriod']}s ease-in-out {num(delay)}s infinite}}"
            f"@keyframes {key}k{{0%{{opacity:1;transform:translateX(0)}}32%{{opacity:1;transform:translateX({num(w + band * 2)}px)}}"
            f"33%,100%{{opacity:0;transform:translateX({num(w + band * 2)}px)}}}}"
        )
        return (f'<g clip-path="url(#{key})"><g class="{key}m">'
                f'<path d="M{num(x - band)} {num(y)}h{num(band)}l{num(-band * .35)} {num(h)}h{num(-band)}z" fill="url(#{key}g)"/></g></g>')

    def render(self) -> str:
        faces = "".join(
            _font_face(family, weight, "".join(sorted(chars)))
            for (family, weight), chars in sorted(self._chars.items())
        )
        types = TOKENS["type"]
        base = (f".sans{{font-family:'{types['sans']}',{types['sansFallback']}}}"
                f".mono{{font-family:'{types['mono']}',{types['monoFallback']}}}"
                "text{text-rendering:geometricPrecision}")
        reduced = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        scale = self.display_width / self.w
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{num(self.display_width)}" '
            f'height="{num(self.h * scale)}" viewBox="0 0 {num(self.w)} {num(self.h)}" role="img" '
            f'aria-labelledby="t d"><title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>'
            f"<style>{faces}{base}{''.join(self.css)}{reduced}</style>"
            f"<defs>{''.join(self.defs)}</defs>{''.join(self.body)}</svg>\n"
        )

    def save(self, name: str) -> Path:
        path = GENERATED / self.theme / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        markup = self.render()
        path.write_text(markup, encoding="utf-8", newline="\n")
        # Some browsers do not propagate reduced-motion into SVG image documents.
        # README <picture> can reliably select this unconditional static variant.
        static = markup.replace('</style>', '*{animation:none!important}</style>', 1)
        path.with_name(f'{name}-static.svg').write_text(static, encoding='utf-8', newline='\n')
        return path
