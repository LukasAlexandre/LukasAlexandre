"""Collection failure, data integrity, privacy and calendar regression checks."""
import copy
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from fetch_contributions import (CACHE, derive_metrics, parse_public_html, period_endpoints,
                                 read_cache, refresh, validate, write_cache)


def fixture(counts=(0, 2, 1, 0, 4, 3, 0)):
    start, end = period_endpoints(date(2026, 11, 25))
    counts = (0,) * ((end - start).days + 1 - len(counts)) + tuple(counts)
    return {"schemaVersion": 1, "login": "LukasAlexandre", "source": "https://github.com/users/LukasAlexandre/contributions",
            "period": {"from": start.isoformat(), "to": end.isoformat()},
            "updatedAt": "2026-11-25T05:00:00Z",
            "days": [{"date": (start + timedelta(days=i)).isoformat(), "count": n} for i, n in enumerate(counts)]}


class ContributionTests(unittest.TestCase):
    def test_metrics_and_yesterday_grace(self):
        actual = derive_metrics(fixture())
        self.assertEqual((actual["total"], actual["activeDays"], actual["currentStreak"], actual["longestStreak"]), (10, 4, 2, 2))

    def test_current_run_includes_today(self):
        self.assertEqual(derive_metrics(fixture((0, 1, 1)))["currentStreak"], 2)

    def test_complete_zero_calendar(self):
        metrics = derive_metrics(fixture((0,) * 7))
        self.assertEqual([metrics[k] for k in ("total", "activeDays", "currentStreak", "longestStreak")], [0, 0, 0, 0])

    def test_leap_year_window(self):
        start, end = period_endpoints(date(2024, 2, 29))
        self.assertEqual(start, date(2023, 3, 1))
        self.assertEqual((end - start).days + 1, 366)

    def test_strict_calendar_rejects_missing_duplicate_out_of_order(self):
        for mutation in (lambda p: p["days"].pop(), lambda p: p["days"].reverse(),
                         lambda p: p["days"].__setitem__(1, p["days"][0])):
            p = fixture()
            mutation(p)
            with self.assertRaises(ValueError):
                validate(p)

    def test_invalid_counts(self):
        for value in (-1, 0.5, True, "0", "<script/>", 10_000_001):
            p = fixture()
            p["days"][0]["count"] = value
            with self.assertRaises(ValueError):
                validate(p)

    def test_private_and_unexpected_fields_rejected(self):
        for mutation in (lambda p: p.update(token="secret"), lambda p: p["days"][0].update(repo="private"),
                         lambda p: p.update(source="https://evil.example/"), lambda p: p.update(login="x/<script>")):
            p = fixture()
            mutation(p)
            with self.assertRaises(ValueError):
                validate(p)

    def test_tooltip_count_parser(self):
        text = '<td id="a" data-date="2026-11-25"></td><tool-tip for="a">1,234 contributions on November 25th.</tool-tip>'
        self.assertEqual(parse_public_html(text, date(2026, 11, 25), date(2026, 11, 25)), [{"date": "2026-11-25", "count": 1234}])
        self.assertEqual(parse_public_html(text.replace("1,234", "No"), date(2026, 11, 25), date(2026, 11, 25))[0]["count"], 0)

    def test_missing_tooltip_never_becomes_zero(self):
        with self.assertRaises(ValueError):
            parse_public_html('<td id="a" data-date="2026-11-25"></td>', date(2026, 11, 25), date(2026, 11, 25))

    def test_duplicate_cell_rejected(self):
        with self.assertRaises(ValueError):
            parse_public_html('<td id="a" data-date="2026-11-25" data-count="1"></td>' * 2, date(2026, 11, 25), date(2026, 11, 25))

    def test_failure_preserves_cache_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cache.json"
            write_cache(fixture(), path)
            before = path.read_bytes()
            def offline(url):
                raise OSError("offline")
            result, fallback = refresh("LukasAlexandre", date(2026, 11, 25), path, offline)
            self.assertTrue(fallback)
            self.assertEqual(result, fixture())
            self.assertEqual(path.read_bytes(), before)
            _, fallback = refresh("LukasAlexandre", date(2026, 11, 25), path, lambda url: "<html>broken schema</html>")
            self.assertTrue(fallback)
            self.assertEqual(path.read_bytes(), before)

    def test_no_cache_failure_raises(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                refresh("LukasAlexandre", date(2026, 11, 25), Path(temp) / "absent", lambda url: "")

    def test_same_data_does_not_touch_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cache.json"
            p = fixture()
            self.assertTrue(write_cache(p, path))
            before = path.read_bytes()
            p["updatedAt"] = "2026-11-25T06:00:00Z"
            self.assertFalse(write_cache(p, path))
            self.assertEqual(path.read_bytes(), before)

    def test_atomic_write_failure_preserves_old_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cache.json"
            p = fixture()
            write_cache(p, path)
            before = path.read_bytes()
            p["days"][0]["count"] = 99
            with patch("fetch_contributions.os.replace", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    write_cache(p, path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(temp).glob("*.tmp")), [])

    def test_real_cache_integrity(self):
        payload = read_cache()
        self.assertEqual(payload["login"], "LukasAlexandre")
        start, end = period_endpoints(date.fromisoformat(payload["period"]["to"]))
        self.assertEqual(payload["period"]["from"], start.isoformat())
        self.assertEqual(len(payload["days"]), (end - start).days + 1)

    def test_refresh_combines_two_calendar_years(self):
        urls = []
        def yearly_response(url):
            urls.append(url)
            year = int(url.split("from=")[1][:4])
            d, end = date(year, 1, 1), date(year, 12, 31)
            cells = []
            while d <= end:
                cells.append(f'<td id="d-{d}" data-date="{d}" data-count="1"></td>')
                d += timedelta(days=1)
            return "".join(cells)
        with tempfile.TemporaryDirectory() as temp:
            payload, fallback = refresh("LukasAlexandre", date(2026, 11, 25), Path(temp) / "cache.json", yearly_response)
            self.assertFalse(fallback)
            self.assertEqual(len(urls), 2)
            self.assertEqual(len(payload["days"]), 365)
            self.assertEqual(derive_metrics(payload)["total"], 365)

    def test_empty_render_no_nonfinite_geometry(self):
        from render_activity import activity
        import xml.etree.ElementTree as ET
        for mobile in (False, True):
            text = activity("dark", fixture((0,) * 7), mobile).render()
            ET.fromstring(text)
            self.assertIn("No contributions in this period", text)
            self.assertNotIn('height="nan"', text)


if __name__ == "__main__":
    unittest.main()
