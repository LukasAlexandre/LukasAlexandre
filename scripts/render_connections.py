"""Independent connection images; links belong to README HTML, outside SVG."""
from __future__ import annotations
from common import LAYOUT, THEMES, Svg, load_json
from icons import icon


def connection_mark(svg,name):
    # Text monograms below are original geometry, not downloaded brand assets.
    if name in ('linkedin','lk'):
        return (svg.rect(14,15,26,26,6,'none','gold')
                + svg.text(27,33,'in' if name=='linkedin' else 'LK',14 if name=='linkedin' else 10.5,
                           weight=700,fill='goldLight',anchor='middle'))
    return icon(name,15,16,24,svg.c['goldLight'])


def connection(theme,item):
    svg = Svg(232,91,theme,item['title'],item['subtitle'])
    svg.add(svg.panel(0,0,232,91,8))
    svg.add(connection_mark(svg,item['icon']))
    svg.add(svg.text(49,32,item['title'],12 if len(item['title'])>16 else 14,weight=600))
    svg.add(svg.text(14,67,item['subtitle'],11,fill='textSoft'))
    return svg


def header(theme,mobile=False):
    w = 360 if mobile else 720
    svg = Svg(w,26,theme,'Professional Connections',display_width=w if mobile else LAYOUT['displayWidth'])
    svg.section_header('05','PROFESSIONAL CONNECTIONS','LET’S CONNECT')
    return svg


def footer(theme,mobile=False):
    w = 360 if mobile else 720
    svg = Svg(w,64,theme,'LKR — Engineering Intelligence',display_width=w if mobile else LAYOUT['displayWidth'])
    svg.add(svg.rect(0,9,w,1,0,'url(#rule)'))
    svg.add(svg.text(w/2,35,'LKR — ENGINEERING INTELLIGENCE',8.2 if mobile else 9,
        family='mono',spacing=1.4 if mobile else 2.7,fill='gold',anchor='middle'))
    svg.add(svg.text(w/2,52,'Engineering intelligent systems.',9,fill='secondary',anchor='middle'))
    return svg


def render():
    profile = load_json('config/profile.json')
    for theme in THEMES:
        header(theme).save('connections-header')
        header(theme,True).save('connections-header-mobile')
        footer(theme).save('footer')
        footer(theme,True).save('footer-mobile')
        for item in profile['connections']:
            connection(theme,item).save('connection-'+item['id'])


if __name__ == '__main__':
    render()