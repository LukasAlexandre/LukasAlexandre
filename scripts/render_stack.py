"""Technology taxonomy with monochrome vectors and no proficiency claims."""
from __future__ import annotations
from common import LAYOUT, THEMES, Svg
from icons import icon

GROUPS = [
    ('LANGUAGES',[('typescript','TypeScript'),('javascript','JavaScript'),('python','Python'),('csharp','C#')]),
    ('FRONTEND',[('react','React'),('html5','HTML'),('css3','CSS')]),
    ('BACKEND',[('nodedotjs','Node.js'),('fastapi','FastAPI')]),
    ('DATABASES',[('mysql','MySQL'),('postgresql','PostgreSQL')]),
    ('AI',[('brain','Artificial Intelligence')]),
    ('INFRASTRUCTURE & DEVOPS',[('git','Git'),('github','GitHub'),('docker','Docker')]),
]


def stack(theme, mobile=False):
    w = 360 if mobile else 720
    cols = 2 if mobile else 3
    gap,pad = 10,14
    cell = (w-(cols-1)*gap)/cols
    rowh = 153 if mobile else 138
    rows = (len(GROUPS)+cols-1)//cols
    svg = Svg(w,26+rows*rowh+(rows-1)*gap,theme,'Technology Stack',
        'Languages: TypeScript, JavaScript, Python, C#. Frontend: React, HTML, CSS. Backend: Node.js, FastAPI. '
        'Databases: MySQL, PostgreSQL. AI: Artificial Intelligence. Infrastructure and DevOps: Git, GitHub, Docker. Git Logo by Jason Long and HTML5/CSS3 identity by W3C, CC-BY-3.0 (https://creativecommons.org/licenses/by/3.0/), adapted to monochrome via Simple Icons.',
        display_width=w if mobile else LAYOUT['displayWidth'])
    svg.section_header('04','TECHNOLOGY STACK','ENGINEERING TOOLKIT')
    for i,(label,items) in enumerate(GROUPS):
        x,y = (i%cols)*(cell+gap),26+(i//cols)*(rowh+gap)
        svg.add(svg.panel(x,y,cell,rowh,8))
        if mobile and len(label)>20:
            svg.add(svg.text(x+pad,y+21,'INFRASTRUCTURE',8.4,weight=600,spacing=.6,fill='gold'))
            svg.add(svg.text(x+pad,y+33,'& DEVOPS',8.4,weight=600,spacing=.6,fill='gold'))
        else:
            svg.add(svg.text(x+pad,y+23,label,8.4,weight=600,spacing=.6,fill='gold'))
        if mobile:
            for j,(name,title) in enumerate(items):
                yy = y+42+j*25
                svg.add(icon(name,x+pad,yy,16,svg.c['textSoft'],svg.c['surface']))
                if len(title)>18:
                    svg.add(svg.text(x+pad+23,yy+6,'Artificial',11,fill='textSoft'))
                    svg.add(svg.text(x+pad+23,yy+20,'Intelligence',11,fill='textSoft'))
                else:
                    svg.add(svg.text(x+pad+23,yy+12,title,11,fill='textSoft'))
        else:
            for j,(name,title) in enumerate(items):
                xx = x+pad+(j%2)*107 if len(title)<18 else x+pad
                yy = y+47+(j//2)*40
                svg.add(icon(name,xx,yy,19,svg.c['textSoft'],svg.c['surface']))
                svg.add(svg.text(xx+25,yy+14,title,10.3,fill='textSoft'))
    return svg


def render():
    for theme in THEMES:
        stack(theme).save('stack')
        stack(theme,True).save('stack-mobile')


if __name__ == '__main__':
    render()