"""Monochrome vector icons on a 24x24 grid.

Brand marks come from assets/icons (Simple Icons, CC0). Everything else is drawn here.
"""
from __future__ import annotations

import re
from functools import lru_cache

from common import ROOT, num

# name -> markup; "S" is replaced by the stroke colour, "F" by the fill colour.
_STROKE = 'fill="none" stroke="S" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
AUTHORED = {
    "code": f'<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14" {_STROKE}/>',
    "calendar": f'<path d="M4 6h16v14H4zM4 10h16M8 3v5M16 3v5M8 13.5h2M14 13.5h2M8 16.5h2M14 16.5h2" {_STROKE}/>',
    "bolt": f'<path d="M13 2L5 13.5h6L10 22l9-12h-6z" {_STROKE}/>',
    "trophy": f'<path d="M7 4h10v5a5 5 0 01-10 0zM7 6H4v1a3.5 3.5 0 003.5 3.5M17 6h3v1a3.5 3.5 0 01-3.5 3.5M12 14v4M8 21h8M9.5 18h5" {_STROKE}/>',
    "layers": f'<path d="M12 3l9 4.5-9 4.5-9-4.5zM3 12l9 4.5 9-4.5M3 16.5L12 21l9-4.5" {_STROKE}/>',
    "server": f'<path d="M4 4h16v7H4zM4 13h16v7H4zM7.5 7.5h.1M7.5 16.5h.1M12 7.5h5M12 16.5h5" {_STROKE}/>',
    "database": f'<path d="M4 6c0-1.700 3.600-3 8-3s8 1.300 8 3-3.600 3-8 3-8-1.300-8-3zM4 6v12c0 1.700 3.600 3 8 3s8-1.300 8-3V6M4 12c0 1.700 3.600 3 8 3s8-1.300 8-3" {_STROKE}/>',
    "brain": f'<path d="M12 4.5a3 3 0 00-5.500 1.700A3.400 3.400 0 004 9.500a3.300 3.300 0 00.600 4.900A3.300 3.300 0 007.800 19 2.800 2.800 0 0012 19.500a2.800 2.800 0 004.200-.500 3.300 3.300 0 003.200-4.600 3.300 3.300 0 00.600-4.900 3.400 3.400 0 00-2.500-3.300A3 3 0 0012 4.500zM12 4.500v15M12 9.500L9 8M12 14l-3.500 1M12 11.500l3.500-1.500M12 16l3-.5" {_STROKE}/>',
    "infinity": f'<path d="M12 12c-2-2.700-3.500-4-5.500-4a4 4 0 000 8c2 0 3.500-1.300 5.500-4zm0 0c2 2.700 3.500 4 5.500 4a4 4 0 000-8c-2 0-3.500 1.300-5.500 4z" {_STROKE}/>',
    "globe": f'<path d="M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c-5 5-5 13 0 18M12 3c5 5 5 13 0 18" {_STROKE}/>',
    "external": f'<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5" {_STROKE}/>',
    "csharp": (
        f'<path d="M12 2l8.700 5v10L12 22l-8.700-5V7z" fill="F"/>'
        '<path d="M11.600 9.200a3.500 3.500 0 10.1 5.600M14 9.500l-.7 5M16.300 9.500l-.7 5M12.700 11h4.600M12.400 13.100H17" '
        'fill="none" stroke="K" stroke-width="1.3" stroke-linecap="round"/>'
    ),
}


@lru_cache(maxsize=None)
def _brand_path(name: str) -> str | None:
    path = ROOT / "assets/icons" / f"{name}.svg"
    if not path.exists():
        return None
    found = re.search(r'<path d="([MmLlHhVvCcSsQqTtAaZz0-9 .,eE+-]+)"', path.read_text(encoding="utf-8"))
    if not found:
        raise ValueError(f"unexpected icon markup in {path.name}")
    return found.group(1)


def icon(name: str, x: float, y: float, size: float, colour: str, knockout: str = "#000") -> str:
    brand = _brand_path(name)
    if brand:
        inner = f'<path d="{brand}" fill="{colour}"/>'
    else:
        inner = AUTHORED[name].replace('"S"', f'"{colour}"').replace('"F"', f'"{colour}"').replace('"K"', f'"{knockout}"')
    return f'<g transform="translate({num(x)} {num(y)}) scale({num(size / 24)})" aria-hidden="true">{inner}</g>'
