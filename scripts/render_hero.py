"""Section 01: ASCII portrait, identity block and the typed code window."""
from __future__ import annotations

from common import LAYOUT, MOTION, ROOT, THEMES, Svg, esc, load_json, num, text_width
from icons import icon

# Glyph -> tone class. ':' is reserved for the removed background.
TONES = {":": "pb", ".": "p1", "-": "p1", "=": "p2", "+": "p2", "*": "p3", "#": "p4", "%": "p4", "@": "p4"}
# The portrait window stays graphite in both themes: light glyphs need a dark ground.
PORTRAIT_INK = {"pb": "#454A53", "p1": "#6B707A", "p2": "#9A9EA6", "p3": "#C9CBD0", "p4": "#F4F4F5"}
KEYWORDS = ("const",)


def portrait_lines() -> list[str]:
    path = ROOT / load_json("config/profile.json")["portrait"]["output"]
    return path.read_text(encoding="utf-8").splitlines()


def portrait(svg: Svg, x: float, y: float, w: float, h: float) -> None:
    lines = portrait_lines()
    cols, rows = len(lines[0]), len(lines)
    pad = 5
    cfg = load_json("config/profile.json")["portrait"]
    left, top, right, bottom = cfg["crop"]
    aspect = (right - left) / (bottom - top)
    grid_w = min(w - pad * 2, (h - pad * 2) * aspect)
    grid_h = grid_w / aspect
    grid_x, grid_y = x + (w - grid_w) / 2, y + (h - grid_h) / 2
    cell_w, cell_h = grid_w / cols, grid_h / rows
    size = cell_h * 1.08
    step = MOTION["portraitRow"]

    svg.add(svg.rect(x, y, w, h, 12, "#07080A", "border"))
    svg.defs.append(f'<clipPath id="pc">{svg.rect(x, y, w, h, 12, "#000")}</clipPath>')
    svg.css.append("".join(f".{k}{{fill:{v}}}" for k, v in PORTRAIT_INK.items()))
    svg.css.append(
        ".row{animation:wipe .5s steps(28) both}"
        "@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}"
        f".cur{{opacity:0;animation:scan {num(rows * step + .5)}s steps({rows}) both}}"
        f"@keyframes scan{{0%{{opacity:1;transform:translateY(0)}}99%{{opacity:1}}100%{{opacity:0;transform:translateY({num(rows * cell_h)}px)}}}}"
    )
    out = ['<g clip-path="url(#pc)" aria-hidden="true">']
    for r, line in enumerate(lines):
        spans, run, current = [], "", None
        for ch in line:
            tone = TONES.get(ch, current or "p1")  # spaces join the current run
            if tone != current and run:
                spans.append((current, run))
                run = ""
            current, run = tone, run + ch
        spans.append((current, run))
        svg.use_font(line, 700, "mono")
        body = "".join(f'<tspan class="{tone}">{esc(chunk)}</tspan>' for tone, chunk in spans)
        out.append(
            f'<text class="mono row" xml:space="preserve" x="{num(grid_x)}" y="{num(grid_y + (r + .82) * cell_h)}" '
            f'font-size="{num(size)}" font-weight="700" textLength="{num(cols * cell_w)}" lengthAdjust="spacingAndGlyphs" '
            f'style="animation-delay:{num(r * step)}s;white-space:pre">{body}</text>'
        )
    out.append(svg.rect(grid_x + grid_w - 8, grid_y, 5, cell_h * 1.6, 0, "goldLight", extra='class="cur"'))
    out.append("</g>")
    svg.add("".join(out))


def badges(svg: Svg, brand: dict, x: float, y: float, right: float, size: float) -> None:
    mark, label = brand["mark"], brand["label"]
    mark_w = text_width(mark, size, 700, "mono", .4)
    label_w = text_width(f"/ {label}", size, 400, "mono", .4)
    w = mark_w + label_w + 20
    svg.add(svg.group(
        svg.rect(x, y, w, 19, 5, "url(#surface)", "gold", 'stroke-opacity="0.6"')
        + svg.text(x + 8, y + 12.6, mark, size, weight=700, family="mono", fill="goldLight", spacing=.4)
        + svg.text(x + 12 + mark_w, y + 12.6, f"/ {label}", size, family="mono", fill="textSoft", spacing=.4),
        delay=.15,
    ))
    status = brand["status"]
    pill = text_width(status, size, 400, "mono", .4) + 29
    px = right - pill
    svg.css.append(".pulse{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{50%{opacity:.35}}")
    svg.add(svg.group(
        svg.rect(px, y, pill, 19, 5, "url(#surface)", "gold", 'stroke-opacity="0.6"')
        + f'<circle class="pulse" cx="{num(px + 11)}" cy="{num(y + 9.5)}" r="3.4" fill="{svg.c["gold"]}"/>'
        + svg.text(px + 20, y + 12.6, status, size, family="mono", fill="goldLight", spacing=.4),
        delay=.25,
    ))


def token_spans(svg: Svg, line: str) -> str:
    """Colour keywords and string literals; everything stays escaped."""
    parts, i = [], 0
    while i < len(line):
        if line[i] == '"':
            end = line.index('"', i + 1) + 1
            parts.append((svg.c["goldLight"], line[i:end], 400))
        else:
            end = line.find('"', i)
            end = len(line) if end < 0 else end
            chunk = line[i:end]
            keyword = next((k for k in KEYWORDS if chunk.startswith(k)), "")
            if keyword:
                parts.append((svg.c["text"], keyword, 700))
                chunk = chunk[len(keyword):]
            if chunk:
                parts.append((svg.c["textSoft"], chunk, 400))
        i = end
    out = []
    for colour, chunk, weight in parts:
        svg.use_font(chunk, weight, "mono")
        out.append(f'<tspan fill="{colour}" font-weight="{weight}">{esc(chunk)}</tspan>')
    return "".join(out)


def code_window(svg: Svg, code: list[str], x: float, y: float, w: float, h: float, size: float, wave: bool) -> None:
    svg.add(svg.rect(x, y, w, h, 7, "#07080A" if svg.theme == "dark" else "#FFFFFF", "border"))
    svg.add(svg.rect(x + .5, y + .5, w - 1, 19, 7, "surface"))
    svg.add(svg.line(x, y + 19.5, x + w, y + 19.5))
    for i, colour in enumerate(("gold", "gold", "secondary")):
        svg.add(f'<circle cx="{num(x + 13 + i * 12)}" cy="{num(y + 10)}" r="3.2" fill="none" stroke="{svg.c[colour]}" stroke-width="1.3"/>')

    if wave:
        # Brushed-gold swell: a fan of offset curves.
        svg.defs.append(
            f'<linearGradient id="wg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{svg.c["gold"]}" stop-opacity="0"/>'
            f'<stop offset="0.75" stop-color="{svg.c["goldLight"]}" stop-opacity="0.9"/>'
            f'<stop offset="1" stop-color="{svg.c["gold"]}" stop-opacity="0.35"/></linearGradient>'
        )
        right, base = x + w - 1, y + h - 38
        paths = "".join(
            f'<path d="M{num(right - 150 + i * 2)} {num(base - i * .6)}C{num(right - 88)} {num(base - 4 + i * 2.1)} '
            f'{num(right - 62)} {num(base - 48 - i * 1.4)} {num(right)} {num(y + 28 + i * 4.4)}" '
            f'opacity="{num(1 - i * .11)}" pathLength="1" class="draw" style="animation-delay:{num(1.4 + i * .09)}s"/>'
            for i in range(8)
        )
        svg.css.append(".draw{stroke-dasharray:1;animation:draw 1.8s ease-out both}@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}")
        svg.add(f'<g fill="none" stroke="url(#wg)" stroke-width="0.8" aria-hidden="true">{paths}</g>')

    pitch = min((h - 30) / len(code), size * 1.45)
    svg.css.append(".type{animation:type both}@keyframes type{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}")
    start = 1.1
    for i, line in enumerate(code):
        ly = y + 33 + i * pitch
        svg.add(svg.text(x + 24, ly, str(i + 1), size * .85, family="mono", fill="secondary", anchor="end"))
        chars = max(len(line.strip()), 2)
        duration = chars * MOTION["typeChar"]
        indent = len(line) - len(line.lstrip(" "))
        cx = x + 50 + indent * text_width(" ", size, 400, "mono")
        svg.add(
            f'<text class="mono type" xml:space="preserve" x="{num(cx)}" y="{num(ly)}" font-size="{num(size)}" '
            f'style="animation-duration:{num(duration)}s;animation-delay:{num(start)}s;animation-timing-function:steps({chars})">'
            f"{token_spans(svg, line.strip())}</text>"
        )
        start += duration + .05
    last = code[-1].strip()
    cursor_x = x + 52 + text_width(last, size, 400, "mono")
    svg.css.append(".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    svg.add(f'<g class="fade" style="animation-delay:{num(start)}s">'
            + svg.rect(cursor_x, y + 33 + (len(code) - 1) * pitch - size * .85, size * .55, size, 0, "gold", extra='class="blink"')
            + "</g>")


def desktop(theme: str, profile: dict) -> Svg:
    top = LAYOUT["sectionHeader"]
    svg = Svg(720, top + 332, theme, f"{profile['name']} — {profile['role']}",
              f"{profile['name']}. {profile['role']}. {', '.join(profile['focusLine'])}. "
              f"{profile['company']['prefix']}{profile['company']['name']}. ASCII portrait and code snippet.",
              display_width=LAYOUT["displayWidth"])
    svg.section_header("01", "IDENTITY", "LKR — ENGINEERING INTELLIGENCE")
    svg.add(svg.panel(0, top, 719, 331, 10))
    portrait(svg, 14, top + 10, 243, 311)

    badges(svg, profile["brand"], 285, top + 18, 701, 7.4)
    svg.add(svg.group(svg.text(284, top + 77, profile["name"], 30, weight=700, spacing=-.2), delay=.35))
    svg.add(svg.group(svg.text(285, top + 100, profile["role"], 11.6, weight=700, fill="gold", spacing=2.5), delay=.45))
    svg.add(svg.group(svg.text(285, top + 121.5, "  ·  ".join(profile["focusLine"]), 11.6, fill="text"), delay=.55))
    company = profile["company"]
    svg.add(svg.group(
        icon("layers", 284, top + 132, 19, svg.c["gold"])
        + svg.text(318, top + 146, company["prefix"] + company["name"], 11.6, fill="textSoft"),
        delay=.65,
    ))
    code_window(svg, profile["code"], 285, top + 163, 417, 153, 8.6, wave=True)
    svg.add(svg.sheen(1, top + 1, 717, 329, 10, 3))
    return svg


def mobile(theme: str, profile: dict) -> Svg:
    top = LAYOUT["sectionHeader"]
    portrait_w, portrait_h = 332, 425
    y = top + 14 + portrait_h
    height = y + 346
    svg = Svg(360, height, theme, f"{profile['name']} — {profile['role']}",
              f"{profile['name']}. {profile['role']}. ASCII portrait and code snippet.")
    svg.section_header("01", "IDENTITY", "LKR")
    svg.add(svg.panel(0, top, 360, height - top, 10))
    portrait(svg, 14, top + 14, portrait_w, portrait_h)
    badges(svg, profile["brand"], 14, y + 14, 346, 6.6)
    svg.add(svg.group(svg.text(14, y + 68, profile["name"], 27, weight=700, spacing=-.3), delay=.35))
    svg.add(svg.group(svg.text(14, y + 91, profile["role"], 11, weight=700, fill="gold", spacing=1.6), delay=.45))
    focus = profile["focusLine"]
    svg.add(svg.group(
        svg.text(14, y + 112, "  ·  ".join(focus[:2]), 11.5)
        + svg.text(14, y + 128, "  ·  ".join(focus[2:]), 11.5),
        delay=.55,
    ))
    company = profile["company"]
    svg.add(svg.group(
        icon("layers", 13, y + 139, 18, svg.c["gold"])
        + svg.text(40, y + 152, company["prefix"] + company["name"], 11.5, fill="textSoft"),
        delay=.65,
    ))
    code_window(svg, profile["code"], 14, y + 170, 332, 162, 8.8, wave=False)
    return svg


def render() -> None:
    profile = load_json("config/profile.json")
    for theme in THEMES:
        desktop(theme, profile).save("hero")
        mobile(theme, profile).save("hero-mobile")


if __name__ == "__main__":
    render()
