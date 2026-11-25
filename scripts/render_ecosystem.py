"""Original, independent vector product cards; private entries never render."""
from __future__ import annotations
import math
import re
from common import LAYOUT, THEMES, Svg, load_json, num, wrap


def path(d, fill="none", stroke="url(#gold)", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1" {extra}/>'


def cube(x, y, s, svg):
    return (path(f'M{x} {y}l{s} {-s*.5} {s} {s*.5}-{s} {s*.5}z', 'url(#surface)')
            + path(f'M{x} {y}v{s}l{s} {s*.5} {s} {-s*.5}v{-s}M{x+s} {y+s*.5}v{s}', stroke=svg.c['gold'])
            + path(f'M{x+s} {y+s*1.5}l{-s} {-s*.5}v{-s}l{s} {s*.5}z',svg.c['goldDeep'],'none','opacity=".16"'))


def layers(svg):
    out = []
    for i in range(4):
        y = 79-i*15
        body = (path(f'M54 {y}l62-27 62 27-62 27z','url(#surface)',svg.c['gold'],f'opacity="{num(.42+i*.17)}"')
                + path(f'M54 {y}v5l62 27 62-27v-5',stroke=svg.c['borderStrong']))
        out.append(f'<g class="float" style="animation-delay:{num(-i*.6)}s">{body}</g>')
    return ''.join(out)


def neural(svg):
    cx,cy,r = 116,66,45
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sphere)" stroke="{svg.c["goldDeep"]}"/>']
    for rotation in (-58,-25,12,47):
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="16" fill="none" stroke="{svg.c["gold"]}" stroke-opacity=".45" transform="rotate({rotation} {cx} {cy})"/>')
    nodes = [(cx+r*math.cos(i*math.tau/13)*(.65 if i%3==0 else 1),cy+r*math.sin(i*math.tau/13)*(.65 if i%3==0 else .9)) for i in range(13)]
    for i,(x,y) in enumerate(nodes):
        nx,ny = nodes[(i+4)%len(nodes)]
        out.append(svg.line(x,y,nx,ny,'gold',.6,'opacity=".25"'))
        out.append(f'<circle class="node" cx="{num(x)}" cy="{num(y)}" r="2" fill="{svg.c["goldLight"]}" style="animation-delay:{num(-i*.23)}s"/>')
    return ''.join(out)


def financial(svg):
    out = [svg.line(27,y,205,y,'border',.7) for y in (38,62,86,110)]
    d = 'M28 100L48 92 65 97 82 73 102 79 121 58 138 63 156 43 176 49 201 25'
    out += [path(d+'V110H28z','url(#chart-area)','none'),path(d,stroke=svg.c['goldDeep'],extra='opacity=".65"'),path(d,extra='class="trace"'),f'<circle class="node" cx="201" cy="25" r="3" fill="{svg.c["goldLight"]}"/>']
    return ''.join(out)


def agents(svg):
    out = [path('M57 79L113 49 176 78M57 79L111 101 176 78',stroke=svg.c['goldDeep'],extra='stroke-dasharray="3 4"')]
    for i,(x,y,s) in enumerate(((39,64,18),(94,33,20),(157,64,18),(96,91,15))):
        out.append(f'<g class="float" style="animation-delay:{num(-i*.8)}s">{cube(x,y,s,svg)}</g>')
    return ''.join(out)


def knowledge(svg):
    nodes = [(116,66,8),(67,38,5),(163,29,4),(183,82,6),(139,110,4),(71,102,5),(40,68,3),(103,20,3)]
    edges = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(1,7),(2,3),(4,5),(5,6)]
    out = [svg.line(*nodes[a][:2],*nodes[b][:2],'gold',.9,'opacity=".45"') for a,b in edges]
    for i,(x,y,r) in enumerate(nodes):
        out.append(f'<circle cx="{x}" cy="{y}" r="{r+4}" fill="none" stroke="{svg.c["goldDeep"]}" stroke-opacity=".3"/>')
        out.append(f'<circle class="node" cx="{x}" cy="{y}" r="{r}" fill="url(#gold)" style="animation-delay:{num(-i*.4)}s"/>')
    return ''.join(out)


def vault(svg):
    out = [path('M75 32l19-12 67 11 0 79-18 13-68-12z','url(#surface)',svg.c['goldDeep']),
           path('M75 32l68 11 18-12M143 43v80',stroke=svg.c['gold']),svg.rect(82,41,54,62,4,'url(#surface)','gold'),
           svg.rect(86,45,46,54,2,'none','borderStrong'),f'<circle cx="109" cy="73" r="14" fill="url(#surface)" stroke="{svg.c["gold"]}"/>']
    spokes = []
    for i in range(5):
        a = i*math.tau/5
        spokes.append(svg.line(109+5*math.cos(a),73+5*math.sin(a),109+11*math.cos(a),73+11*math.sin(a),'goldLight',1.5))
    out.append('<g class="dial">'+''.join(spokes)+'</g>')
    out.append(f'<circle cx="109" cy="73" r="4" fill="url(#gold)"/>')
    out.append(svg.line(130,58,130,64,'gold',2))
    out.append(svg.line(130,83,130,89,'gold',2))
    return ''.join(out)


GRAPHICS = {'layers':layers,'neural':neural,'financial':financial,'agents':agents,'knowledge':knowledge,'vault':vault}


def product(theme, project):
    svg = Svg(232,222,theme,project['name'],project['description'])
    svg.add(svg.panel(0,0,232,222,9))
    svg.defs.append(f'<radialGradient id="sphere"><stop offset="0" stop-color="{svg.c["gold"]}" stop-opacity=".16"/><stop offset="1" stop-color="{svg.c["surface"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="chart-area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{svg.c["gold"]}" stop-opacity=".22"/><stop offset="1" stop-color="{svg.c["gold"]}" stop-opacity="0"/></linearGradient>')
    svg.css.append('.float{animation:float 5s ease-in-out infinite}@keyframes float{50%{transform:translateY(-4px)}}'
        '.node{animation:node 3.8s ease-in-out infinite}@keyframes node{50%{opacity:.45}}'
        '.trace{stroke-width:1.7;stroke-dasharray:280;animation:trace 2.8s ease both}@keyframes trace{from{stroke-dashoffset:280}to{stroke-dashoffset:0}}'
        '.dial{transform-origin:109px 73px;animation:dial 12s ease-in-out infinite}@keyframes dial{40%,70%{transform:rotate(72deg)}}')
    svg.add('<g aria-hidden="true">'+GRAPHICS[project['graphic']](svg)+'</g>')
    svg.add(svg.line(17,132,215,132,'border',.7))
    svg.add(svg.text(17,158,project['name'],19,weight=600,spacing=.3))
    for i,line in enumerate(wrap(project['description'],198,12)):
        svg.add(svg.text(17,180+i*16,line,12,fill='textSoft'))
    svg.add(svg.sheen(1,1,230,220,9,2.5))
    return svg


def header(theme, mobile=False):
    w = 360 if mobile else 720
    svg = Svg(w,26,theme,'Engineering Ecosystem',display_width=w if mobile else LAYOUT['displayWidth'])
    svg.section_header('03','ENGINEERING ECOSYSTEM','PRODUCTS & SYSTEMS')
    return svg


def render():
    projects = load_json('config/projects.json')['projects']
    for theme in THEMES:
        header(theme).save('ecosystem-header')
        header(theme,True).save('ecosystem-header-mobile')
        for p in projects:
            if p.get('public') is not True:
                continue
            if not re.fullmatch(r'[a-z][a-z0-9-]*',p['id']):
                raise ValueError('Invalid project id')
            product(theme,p).save('project-'+p['id'])


if __name__ == '__main__':
    render()