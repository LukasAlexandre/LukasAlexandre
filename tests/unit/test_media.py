"""Publishing contracts for the pre-rendered public original animation."""
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from build import readme
from common import load_json


def gif_info(data):
    if data[:6] not in (b'GIF89a', b'GIF87a'):
        raise ValueError('Not GIF')
    width, height = struct.unpack_from('<HH', data, 6)
    at = 13 + (3 * 2 ** ((data[10] & 7) + 1) if data[10] & 128 else 0)
    frames = duration = 0
    def skip_blocks(at):
        while data[at]:
            at += 1 + data[at]
        return at + 1
    while data[at] != 0x3b:
        block = data[at]
        at += 1
        if block == 0x21:
            label = data[at]
            at += 1
            if label == 0xf9:
                duration += struct.unpack_from('<H', data, at + 2)[0] * 10
            at = skip_blocks(at)
        elif block == 0x2c:
            packed = data[at + 8]
            at += 9
            if packed & 128:
                at += 3 * 2 ** ((packed & 7) + 1)
            at += 1  # LZW minimum code size
            at = skip_blocks(at)
            frames += 1
        else:
            raise ValueError('Unknown GIF block')
    return width, height, frames, duration


class MediaTests(unittest.TestCase):
    def test_original_animation_with_compatible_fallbacks(self):
        for theme in ('dark', 'light'):
            for mobile in (False, True):
                stem = ROOT / 'generated' / theme / ('project-ethan' + ('-mobile' if mobile else ''))
                width, height, frames, duration = gif_info(stem.with_suffix('.gif').read_bytes())
                self.assertEqual((width, height), (174, 204) if mobile else (352, 238))
                self.assertGreaterEqual(frames, 100)
                self.assertEqual(duration, 6000)
                self.assertLess(stem.with_suffix('.gif').stat().st_size, 3_000_000)
                png = stem.with_name(stem.name + '-static.png').read_bytes()
                self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack_from('>II', png, 16), (width, height))
                webp = stem.with_suffix('.webp').read_bytes()
                self.assertEqual(webp[:4], b'RIFF')
                self.assertEqual(webp[8:12], b'WEBP')
                self.assertIn(b'ANIM', webp)
                self.assertLess(len(webp), stem.with_suffix('.gif').stat().st_size)

    def test_no_ascii_runtime_or_private_source_is_published(self):
        self.assertNotIn('ASCII', readme())
        self.assertNotIn('portrait', load_json('config/profile.json'))
        for removed in ('scripts/generate_ascii.py', 'assets/portrait/portrait.txt', 'requirements-portrait.txt'):
            self.assertFalse((ROOT / removed).exists())
        self.assertTrue((ROOT / 'assets/portrait/source.jpg').exists())
        for private_source_pattern in ('*.ts', '*.glsl', '*.js', '.env*'):
            self.assertFalse(list((ROOT / 'generated').rglob(private_source_pattern)))
        self.assertFalse(list((ROOT / 'generated/dark').glob('project-ethan*.svg')))
        self.assertFalse(list((ROOT / 'generated/light').glob('project-ethan*.svg')))
        self.assertIn('type="image/webp"', readme())
        self.assertIn('project-ethan.gif', readme())
        self.assertIn('adaptive/project-ethan-static.svg', readme())


if __name__ == '__main__':
    unittest.main()
