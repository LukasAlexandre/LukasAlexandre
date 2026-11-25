"""Checks important image-context constraints rather than string snapshots."""
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from common import Svg, esc, safe_url, TOKENS, text_width
from render_hero import desktop, mobile, portrait_lines
from common import load_json


def luminance(colour):
    rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in rgb]
    return sum(x * k for x, k in zip(rgb, (.2126, .7152, .0722)))


class SvgTests(unittest.TestCase):
    def test_escape_xml_and_unicode(self):
        payload = '<script onload="alert(1)">&\x00\ud800 日本語 é'
        svg = Svg(100, 50, 'dark', payload)
        svg.add(svg.text(0, 20, payload, 12))
        doc = ET.fromstring(svg.render())
        self.assertEqual(len(doc.findall('.//{*}script')), 0)
        self.assertIn('日本語', ''.join(doc.itertext()))

    def test_url_protocol_injection(self):
        for value in ('javascript:alert(1)', '//evil.test', 'https://ok.test/" onload="bad', 'http://ok.test', 'https://user:pass@test.com'):
            self.assertIsNone(safe_url(value))
        self.assertEqual(safe_url('https://github.com/LukasAlexandre'), 'https://github.com/LukasAlexandre')

    def test_deterministic_fonts(self):
        def render():
            s = Svg(100, 50, 'light', 'Identity')
            s.add(s.text(5, 25, 'Lukas Alexandre', 14))
            return s.render()
        self.assertEqual(render(), render())

    def test_portrait_is_real_character_grid(self):
        lines = portrait_lines()
        self.assertGreater(len(lines), 60)
        self.assertEqual({len(x) for x in lines}, {112})
        self.assertGreater(len(set(''.join(lines))), 5)
        for variant in (desktop, mobile):
            svg = variant('dark', load_json('config/profile.json')).render()
            tree = ET.fromstring(svg)
            self.assertFalse(tree.findall('.//{*}image'))
            self.assertIn('prefers-reduced-motion', svg)

    def test_palette_text_contrast(self):
        for theme, c in TOKENS['themes'].items():
            for fg in ('text', 'textSoft', 'secondary', 'gold'):
                for bg in ('background', 'surface', 'surfaceHigh'):
                    a, b = sorted((luminance(c[fg]), luminance(c[bg])))
                    self.assertGreaterEqual((b + .05) / (a + .05), 4.5, (theme, fg, bg))


if __name__ == '__main__':
    unittest.main()
