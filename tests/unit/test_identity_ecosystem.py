"""V1.1 identity and GitHub-compatible Bento regression contracts."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import readme
from common import load_json, text_width
from render_ecosystem import product


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.current = []
        if tag == 'img' and self.current is not None:
            a = dict(attrs)
            if '/project-' in a.get('src', ''):
                self.current.append(a)

    def handle_endtag(self, tag):
        if tag == 'p' and self.current:
            self.rows.append(self.current)
            self.current = None


class RefinementTests(unittest.TestCase):
    def test_bento_has_two_featured_then_three_cards(self):
        parser = Rows()
        parser.feed(readme())
        self.assertEqual([[Path(a['src']).stem for a in row] for row in parser.rows],
                         [['project-ethan', 'project-vorcen'], ['project-gidace', 'project-inoryx', 'project-vaultify']])
        self.assertEqual([[a['width'] for a in row] for row in parser.rows], [['49%', '49%'], ['32%', '32%', '32%']])

    def test_retired_card_absent_company_preserved(self):
        self.assertNotIn('LK System', readme())
        self.assertNotIn('lk-system', readme())
        self.assertFalse(list((ROOT / 'generated').rglob('project-lk-system*.svg')))
        self.assertEqual(load_json('config/profile.json')['company'], {'prefix': 'Co-Founder at ', 'name': 'LK Technologies Brasil'})
        self.assertIn('LK Technologies Brasil', readme())

    def test_product_text_fits_all_responsive_variants(self):
        cfg = load_json('config/projects.json')
        for p in cfg['projects']:
            for theme in ('dark', 'light'):
                for mobile in (False, True):
                    svg = product(theme, p, featured=p['id'] in cfg['layout']['featured'], mobile=mobile)
                    tree = ET.fromstring(svg.render())
                    for text in tree.findall('.//{*}text'):
                        x, y, size = (float(text.get(key)) for key in ('x', 'y', 'font-size'))
                        width = text_width(''.join(text.itertext()), size, int(text.get('font-weight', '400')), spacing=float(text.get('letter-spacing', 0)))
                        self.assertLessEqual(x + width, svg.w - 7, (p['id'], theme, mobile, text.text))
                        self.assertLess(y, svg.h - 7)

    def test_photo_matches_fresh_public_provenance(self):
        provenance = load_json('docs/portrait-source.json')
        self.assertEqual(hashlib.sha256((ROOT / 'assets/portrait/source.jpg').read_bytes()).hexdigest(), provenance['sha256'])
        self.assertNotEqual(provenance['sha256'], provenance['previousSHA256'])
        self.assertEqual(provenance['resolution'], [460, 460])


if __name__ == '__main__':
    unittest.main()
