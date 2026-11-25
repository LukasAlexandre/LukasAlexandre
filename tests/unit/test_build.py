"""Cross-component publishing contracts checked against the generated README."""
import re
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import readme, validate_generated
from fetch_contributions import read_cache, derive_metrics
from render_activity import activity
from common import load_json
from unittest.mock import patch


class BuildTests(unittest.TestCase):
    def test_all_picture_sources_exist(self):
        sources = re.findall(r'(?:src|srcset)="\./([^\"]+)"', readme())
        self.assertGreater(len(sources), 40)
        for source in sources:
            self.assertTrue((ROOT / source).is_file(), source)
        validate_generated()

    def test_only_explicitly_public_projects_are_exposed(self):
        original = load_json
        def configured(path):
            if path == 'config/projects.json':
                return {'projects': [{'id': 'private-secret-project', 'name': 'Internal', 'public': False}, {'id': 'default-hidden', 'name': 'Internal'}]}
            return original(path)
        with patch('build.load_json', side_effect=configured):
            markup = readme()
        self.assertNotIn('private-secret', markup)
        self.assertNotIn('default-hidden', markup)

    def test_empty_calendar_render_remains_legible(self):
        payload = read_cache()
        payload['days'] = [dict(d, count=0) for d in payload['days']]
        self.assertEqual(derive_metrics(payload)['total'], 0)
        for theme in ('dark', 'light'):
            for mobile in (False, True):
                text = activity(theme, payload, mobile).render()
                tree = ET.fromstring(text)
                self.assertIn('No contributions in this period', text)
                numeric = {'x', 'y', 'width', 'height', 'cx', 'cy', 'r', 'rx', 'ry', 'viewBox', 'd', 'transform'}
                for node in tree.iter():
                    for key, value in node.attrib.items():
                        if key in numeric:
                            self.assertIsNone(re.search(r'(?<![A-Za-z])(?:nan|inf)(?![A-Za-z])', value, re.I), (key, value))

    def test_readme_has_no_active_external_runtime(self):
        text = readme()
        for forbidden in ('<script', '<iframe', '<style', 'style=', 'javascript:', 'vercel.app/api'):
            self.assertNotIn(forbidden, text)
        self.assertIn('prefers-color-scheme: light', text)
        self.assertIn('max-width: 600px', text)


if __name__ == '__main__':
    unittest.main()
