"""Theme-adaptive assets for width/motion sources left intact by GitHub themed-picture."""
import base64
import xml.etree.ElementTree as ET
from common import ROOT, GENERATED

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def render():
    target = GENERATED / 'adaptive'
    target.mkdir(exist_ok=True)
    for dark in sorted((GENERATED / 'dark').glob('*.svg')):
        light = GENERATED / 'light' / dark.name
        root, other = ET.parse(dark).getroot(), ET.parse(light).getroot()
        nodes, peers = list(root.iter()), list(other.iter())
        if len(nodes) != len(peers):
            raise ValueError(f'Theme geometry differs: {dark.name}')
        overrides = []
        for node, peer in zip(nodes, peers):
            if node.tag != peer.tag or node.text != peer.text:
                raise ValueError(f'Theme structure differs: {dark.name}')
            for key in sorted(node.attrib.keys() | peer.attrib.keys()):
                if node.get(key) == peer.get(key):
                    continue
                if key not in {'fill', 'stroke', 'stop-color', 'stop-opacity', 'fill-opacity', 'stroke-opacity', 'opacity'}:
                    raise ValueError(f'Unsupported theme attribute {key}: {dark.name}')
                token = f'--lkr-{len(overrides)}'
                overrides.append(f'{token}:{peer.get(key)}')
                node.set(key, f'var({token},{node.get(key)})')
        style = ET.SubElement(root, f'{{{NS}}}style')
        style.text = '@media(prefers-color-scheme:light){:root{' + ';'.join(overrides) + '}}'
        (target / dark.name).write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8', newline='\n')
    # Raster bytes are embedded unchanged. Browser color-scheme inheritance selects
    # the theme independently of viewport and motion conditions in the outer picture.
    for mobile in (False, True):
        stem = 'project-ethan' + ('-mobile' if mobile else '')
        width, height = (174, 204) if mobile else (352, 238)
        variants = [('-webp', 'webp'), ('-gif', 'gif'), ('-static', 'png')] if mobile else [('-static', 'png')]
        for suffix, ext in variants:
            images = []
            for theme in ('dark', 'light'):
                source = stem + ('-static' if ext == 'png' else '') + '.' + ext
                encoded = base64.b64encode((GENERATED / theme / source).read_bytes()).decode('ascii')
                images.append(f'<image class="{theme}" width="{width}" height="{height}" href="data:image/{ext};base64,{encoded}"/>')
            svg = (f'<svg xmlns="{NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">'
                   '<title>ETHAN — original animation</title><desc>Original ETHAN render, adaptive theme.</desc>'
                   '<style>.light{display:none}@media(prefers-color-scheme:light){.dark{display:none}.light{display:inline}}</style>'
                   + ''.join(images) + '</svg>')
            (target / (stem + suffix + '.svg')).write_text(svg, encoding='utf-8', newline='\n')
