"""Validated anonymous public GitHub day counts and last-known-good cache."""
from __future__ import annotations
import argparse
import calendar
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/contributions.json"
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")


def period_endpoints(end: date) -> tuple[date, date]:
    """Inclusive trailing year, leap-safe, anniversary + one day through end."""
    anniversary = end.replace(year=end.year - 1, day=min(end.day, calendar.monthrange(end.year - 1, end.month)[1]))
    return anniversary + timedelta(days=1), end


class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells, self.tips = {}, {}
        self.tip_id, self.tip_parts = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("td", "rect") and "data-date" in a:
            identity = a.get("id")
            if not identity or identity in self.cells:
                raise ValueError("duplicate or unidentified contribution cell")
            self.cells[identity] = {"date": a["data-date"], "count": a.get("data-count")}
        if tag == "tool-tip":
            self.tip_id, self.tip_parts = a.get("for"), []

    def handle_data(self, text):
        if self.tip_id:
            self.tip_parts.append(text)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tip_id:
            if self.tip_id in self.tips:
                raise ValueError("duplicate contribution tooltip")
            self.tips[self.tip_id] = " ".join("".join(self.tip_parts).split())
            self.tip_id, self.tip_parts = None, []


def parse_public_html(html: str, start: date, end: date) -> list[dict]:
    p = ContributionParser()
    p.feed(html)
    result = []
    for identity, cell in p.cells.items():
        day = date.fromisoformat(cell["date"])
        if not start <= day <= end:
            continue
        raw_count = cell["count"]
        if raw_count is None:
            match = re.match(r"^(No|[0-9][0-9,]*) contributions? on .+\.$", p.tips.get(identity, ""))
            if not match:
                raise ValueError(f"missing/invalid count for {day}")
            raw_count = "0" if match[1] == "No" else match[1].replace(",", "")
        if not re.fullmatch(r"[0-9]+", raw_count):
            raise ValueError("invalid contribution count")
        result.append({"date": day.isoformat(), "count": int(raw_count)})
    return sorted(result, key=lambda row: row["date"])


def validate(payload: dict) -> dict:
    if not isinstance(payload, dict) or payload.get("schemaVersion") != 1:
        raise ValueError("invalid cache schema")
    if set(payload) != {"schemaVersion", "login", "source", "period", "updatedAt", "days"}:
        raise ValueError("unexpected cache fields")
    if not isinstance(payload.get("login"), str) or not LOGIN.fullmatch(payload["login"]):
        raise ValueError("invalid GitHub login")
    if not isinstance(payload.get("period"), dict) or set(payload["period"]) != {"from", "to"}:
        raise ValueError("invalid period fields")
    start, end = date.fromisoformat(payload["period"]["from"]), date.fromisoformat(payload["period"]["to"])
    if (start, end) != period_endpoints(end):
        raise ValueError("invalid period")
    stamp = datetime.fromisoformat(payload["updatedAt"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or stamp.date() < end:
        raise ValueError("invalid update timestamp")
    if payload.get("source") != f"https://github.com/users/{payload['login']}/contributions":
        raise ValueError("untrusted data source")
    rows = payload.get("days")
    if not isinstance(rows, list) or len(rows) != (end - start).days + 1:
        raise ValueError("incomplete contribution calendar")
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"date", "count"}:
            raise ValueError("unexpected day fields")
        if row["date"] != (start + timedelta(days=i)).isoformat():
            raise ValueError("duplicate, missing or unordered date")
        if type(row["count"]) is not int or not 0 <= row["count"] <= 10_000_000:
            raise ValueError("invalid daily count")
    return payload


def derive_metrics(payload: dict) -> dict:
    validate(payload)
    days = payload["days"]
    longest = run = 0
    monthly = {}
    for row in days:
        run = run + 1 if row["count"] else 0
        longest = max(longest, run)
        key = row["date"][:7]
        monthly[key] = monthly.get(key, 0) + row["count"]
    tail = days[:-1] if days and not days[-1]["count"] else days
    current = 0
    for row in reversed(tail):
        if not row["count"]:
            break
        current += 1
    return {"total": sum(d["count"] for d in days), "activeDays": sum(d["count"] > 0 for d in days),
            "currentStreak": current, "longestStreak": longest, "monthly": monthly}


def read_cache(path: Path = CACHE) -> dict:
    return validate(json.loads(path.read_text(encoding="utf-8")))


def write_cache(payload: dict, path: Path = CACHE) -> bool:
    validate(payload)
    if path.exists():
        try:
            previous = read_cache(path)
            if all(previous[k] == payload[k] for k in ("login", "source", "period", "days")):
                return False
        except (ValueError, KeyError, TypeError):
            pass
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=".contributions-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return True


def download(url: str) -> str:
    req = Request(url, headers={"User-Agent": "LKR-profile-art/1.0", "Accept": "text/html", "Accept-Language": "en-US,en;q=0.9"})
    with urlopen(req, timeout=30) as response:
        raw = response.read(4_000_001)
        if len(raw) > 4_000_000:
            raise ValueError("oversized contribution response")
        return raw.decode("utf-8")


def refresh(login: str, end: date | None = None, cache_path: Path = CACHE, fetcher=download) -> tuple[dict, bool]:
    if not LOGIN.fullmatch(login):
        raise ValueError("invalid GitHub login")
    start, end = period_endpoints(end or datetime.now(timezone.utc).date())
    source = f"https://github.com/users/{login}/contributions"
    try:
        # GitHub serves a calendar YEAR when a historical `to` is supplied,
        # rather than respecting arbitrary rolling `from`/`to` boundaries.
        # Request each intersecting year separately, then validate the exact window.
        days = []
        for year in range(start.year, end.year + 1):
            html = fetcher(f"{source}?from={year}-01-01&to={year}-12-31")
            days.extend(parse_public_html(html, max(start, date(year, 1, 1)), min(end, date(year, 12, 31))))
        payload = {"schemaVersion": 1, "login": login, "source": source,
                   "period": {"from": start.isoformat(), "to": end.isoformat()},
                   "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                   "days": days}
        validate(payload)
        write_cache(payload, cache_path)
        return read_cache(cache_path), False
    except (OSError, ValueError, KeyError, TypeError) as exc:
        cached = read_cache(cache_path)
        if cached["login"] != login:
            raise ValueError("cache belongs to another user") from exc
        return cached, True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--login", default="LukasAlexandre")
    p.add_argument("--end", type=date.fromisoformat)
    p.add_argument("--cache", type=Path, default=CACHE)
    args = p.parse_args()
    payload, fallback = refresh(args.login, args.end, args.cache)
    print(json.dumps({"fallback": fallback, "period": payload["period"], "updatedAt": payload["updatedAt"], **derive_metrics(payload)}))


if __name__ == "__main__":
    main()
