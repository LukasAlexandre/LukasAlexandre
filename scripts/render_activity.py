"""Development activity, rendered from validated anonymous GitHub day counts."""
from __future__ import annotations
from datetime import date, timedelta
import math

from common import LAYOUT, MOTION, THEMES, Svg, esc, num
from fetch_contributions import derive_metrics, read_cache
from icons import icon

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def heat_level(count: int, maximum: int) -> int:
    return 0 if not count else min(4, max(1, math.ceil(count * 4 / max(maximum, 1))))


def stats(svg: Svg, metrics: dict, mobile: bool):
    items = (("total", "Total Contributions", "code"), ("activeDays", "Active Days", "calendar"),
             ("currentStreak", "Current Streak", "bolt"), ("longestStreak", "Longest Streak", "trophy"))
    columns, gap = (2 if mobile else 4), 8
    width = (svg.w - gap * (columns - 1)) / columns
    for i, (key, label, glyph) in enumerate(items):
        x, y = (i % columns) * (width + gap), 26 + (i // columns) * 84
        content = svg.panel(x, y, width, 76)
        content += icon(glyph, x + width - 32, y + 17, 17, svg.c["gold"])
        content += svg.text(x + 15, y + 37, f"{metrics[key]:,}", 26, weight=600, fill="text")
        content += svg.text(x + 15, y + 59, label, 9.2, fill="textSoft")
        svg.add(svg.group(content, delay=i * MOTION["stagger"]))


def heatmap(svg: Svg, days: list[dict], x: float, y: float, width: float, mobile=False):
    start = date.fromisoformat(days[0]["date"])
    first_sunday = start - timedelta(days=(start.weekday() + 1) % 7)
    final = date.fromisoformat(days[-1]["date"])
    columns = ((final - first_sunday).days // 7) + 1
    labels, usable = 28, width - 30
    pitch = min(12.3 if not mobile else 10.5, usable / columns)
    cell = pitch - (2.8 if not mobile else 2.2)
    max_count = max(row["count"] for row in days)
    font_size = 8 if not mobile else 8.5
    for weekday, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        svg.add(svg.text(x, y + 19 + weekday * pitch + cell * .8, label, font_size, fill="secondary"))
    seen_months = set()
    for row in days:
        day = date.fromisoformat(row["date"])
        column, weekday = divmod((day - first_sunday).days, 7)
        key = row["date"][:7]
        if key not in seen_months:
            # A partial first week can be too close to the next month label.
            if column > 1 or day.day <= 23:
                svg.add(svg.text(x + labels + column * pitch, y + 8, MONTHS[day.month - 1], font_size, fill="secondary"))
            seen_months.add(key)
        level = heat_level(row["count"], max_count)
        rect = svg.rect(x + labels + column * pitch, y + 19 + weekday * pitch, cell, cell, 1.7, f"heat{level}")
        # Accessible per-day text, safe because only validated ISO date and int enter.
        tip = f'{row["date"]}: {row["count"]} contributions'
        svg.add(f'<g class="cell" style="animation-delay:{num(column * .025 + weekday * .015)}s"><title>{esc(tip)}</title>{rect}</g>')
    return 19 + 7 * pitch


def legend(svg: Svg, x, y):
    svg.add(svg.text(x, y + 7, "Less", 7.5, fill="secondary"))
    for i in range(5):
        svg.add(svg.rect(x + 27 + i * 11, y, 8, 8, 1.4, f"heat{i}"))
    svg.add(svg.text(x + 87, y + 7, "More", 7.5, fill="secondary"))


def monthly(svg: Svg, totals: dict, x, y, width, height, mobile=False):
    maximum = max(totals.values(), default=0)
    # A zero calendar is legitimate and displays an explicit empty state.
    top_value = max(1, math.ceil(maximum / 50) * 50)
    left, bottom = x + 31, y + height - 29
    plot_h, plot_w = height - 49, width - 43
    for fraction in (0, .5, 1):
        gy = bottom - plot_h * fraction
        svg.add(svg.line(left, gy, left + plot_w, gy, extra='stroke-dasharray="2 4"'))
        svg.add(svg.text(left - 7, gy + 3, str(round(top_value * fraction)), 7.5, family="mono", fill="secondary", anchor="end"))
    pitch = plot_w / max(len(totals), 1)
    for i, (key, count) in enumerate(totals.items()):
        bx = left + i * pitch + pitch * .22
        bw = pitch * .55
        bar_h = count / top_value * plot_h
        bar = svg.rect(bx, bottom - bar_h, bw, bar_h, 2, "url(#gold)") if count else ""
        title = f"{key}: {count} contributions"
        svg.add(f'<g class="bar" style="transform-origin:{num(bx)}px {num(bottom)}px;animation-delay:{num(.3 + i * .045)}s"><title>{esc(title)}</title>{bar}</g>')
        if count:
            svg.add(svg.text(bx + bw / 2, bottom - bar_h - 5, str(count), 6.7 if mobile else 7.5, fill="textSoft", anchor="middle"))
        # Two-line year labels distinguish the two partial November bins.
        mon = MONTHS[int(key[5:]) - 1]
        svg.add(svg.text(bx + bw / 2, bottom + 13, mon, 7 if mobile else 8, fill="secondary", anchor="middle"))
        if i in (0, len(totals) - 1) or key.endswith("-01"):
            svg.add(svg.text(bx + bw / 2, bottom + 24, key[2:4], 7, family="mono", fill="secondary", anchor="middle"))
    if maximum == 0:
        svg.add(svg.text(left + plot_w / 2, y + 34, "No contributions in this period", 11, fill="secondary", anchor="middle"))


def activity(theme: str, payload: dict, mobile=False) -> Svg:
    metrics = derive_metrics(payload)
    width, height = (360, 690) if mobile else (720, 458)
    svg = Svg(width, height, theme, "Development Activity — Lukas Alexandre Rosa",
              f"{metrics['total']} contributions across {metrics['activeDays']} active days. "
              f"Current streak {metrics['currentStreak']} days; longest streak {metrics['longestStreak']} days. "
              f"Period {payload['period']['from']} through {payload['period']['to']}. "
              f"Public GitHub day counts. Last changed {payload['updatedAt']}.",
              display_width=width if mobile else LAYOUT["displayWidth"])
    svg.section_header("02", "DEVELOPMENT ACTIVITY", "CONSISTENCY / CRAFT / PROGRESS")
    svg.css.append(".cell{animation:fade .6s ease both}.bar{animation:grow 1s cubic-bezier(.2,.7,.2,1) both}@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}")
    stats(svg, metrics, mobile)
    top, ph = (197, 267) if mobile else (113, 160)
    svg.add(svg.panel(0, top, width, ph))
    svg.add(svg.text(16, top + 23, "CONTRIBUTION HEATMAP", 9.3, weight=600, spacing=1, fill="text"))
    if mobile:
        days = payload["days"]
        # Two contiguous half-year bands keep cells legible in an image at 360px.
        midpoint = len(days) // 2
        for i, chunk in enumerate((days[:midpoint], days[midpoint:])):
            heatmap(svg, chunk, 13, top + 36 + i * 98, width - 26, True)
        legend(svg, width - 125, top + ph - 18)
        svg.add(svg.text(16, top + ph - 10, "Two chronological bands", 7.5, fill="secondary"))
    else:
        heatmap(svg, payload["days"], 16, top + 34, width - 32)
        legend(svg, width - 125, top + ph - 17)
    chart_y, chart_h = (476, 179) if mobile else (285, 140)
    svg.add(svg.panel(0, chart_y, width, chart_h))
    svg.add(svg.text(16, chart_y + 22, "MONTHLY ACTIVITY", 9.3, weight=600, spacing=1))
    svg.add(svg.text(width - 16, chart_y + 22, "EDGE MONTHS PARTIAL", 6.8, family="mono", fill="secondary", anchor="end"))
    monthly(svg, metrics["monthly"], 10, chart_y + 26, width - 20, chart_h - 30, mobile)
    footer = chart_y + chart_h + 15
    period = payload["period"]
    svg.add(svg.text(1, footer, f"{period['from']} — {period['to']}", 7.3, family="mono", fill="secondary"))
    svg.add(svg.text(width - 1, footer, "PUBLIC GITHUB DATA", 7.3, family="mono", fill="secondary", anchor="end"))
    svg.add(svg.text(1, footer + 13, f"Updated {payload['updatedAt'].replace('T', ' ').replace('Z', ' UTC')}", 7.2, family="mono", fill="secondary"))
    return svg


def render():
    payload = read_cache()
    for theme in THEMES:
        activity(theme, payload).save("activity")
        activity(theme, payload, mobile=True).save("activity-mobile")


if __name__ == "__main__":
    render()
