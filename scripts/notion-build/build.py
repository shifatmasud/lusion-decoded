#!/usr/bin/env python3
"""Build composites + Markdown for chapter 15. usage: build.py composites|md"""
import json, os, re, sys, glob, html as H
from html.parser import HTMLParser
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from content import PAGES, EXTRA, GLOBALS, CH, URL
from facts import facts
BASE = '/home/sprite/lusion/handbook/ch15'
os.chdir(BASE)
os.makedirs('notion', exist_ok=True)
MONO = os.path.expanduser('~/.fonts/JetBrainsMono.ttf')
HTMLF = {'home': 'home', 'about': 'about', 'projects': 'projects', 'project_oryzo_ai': 'projects_oryzo_ai', 'playground': 'playground'}

def frames(slug, mode, sec):
    return sorted(glob.glob(f'img/{slug}/{mode}/[0-9][0-9]_{sec}_*.jpg'))

def stack(paths, out, width=1200, horizontal=False, label=None):
    ims = [Image.open(p) for p in paths]
    if not ims:
        return None
    if horizontal:
        h = 640
        ims = [im.resize((int(im.width * h / im.height), h)) for im in ims]
        W = sum(i.width for i in ims) + 12 * (len(ims) - 1)
        canvas = Image.new('RGB', (W, h), 'white'); x = 0
        for im in ims:
            canvas.paste(im, (x, 0)); x += im.width + 12
    else:
        ims = [im.resize((width, int(im.height * width / im.width))) for im in ims]
        Ht = sum(i.height for i in ims) + 8 * (len(ims) - 1)
        canvas = Image.new('RGB', (width, Ht), 'white'); y = 0
        for im in ims:
            canvas.paste(im, (0, y)); y += im.height + 8
    canvas.save(out, quality=80)
    return out

def grid(paths, out, cols=3, cw=480):
    ims = [Image.open(p) for p in paths]
    ims = [im.resize((cw, int(im.height * cw / im.width))) for im in ims]
    ch = max(i.height for i in ims)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new('RGB', (cols * cw + (cols - 1) * 10, rows * ch + (rows - 1) * 10), 'white')
    for k, im in enumerate(ims):
        canvas.paste(im, ((k % cols) * (cw + 10), (k // cols) * (ch + 10)))
    canvas.save(out, quality=80)
    return out

def composites():
    made = []
    for P in PAGES + [dict(slug='playground', sections=[])]:
        slug = P['slug']
        for S in P.get('sections', []) + EXTRA:
            fr = frames(slug, 'desktop', S['id'])
            hv = glob.glob(f"img/{slug}/desktop/state_hover_{S['id']}.jpg")
            if S['id'] in ('about-hero',):
                fr = [f'img/{slug}/desktop/00_loaded.jpg']
            if S in EXTRA and slug != 'home':
                continue  # shared sections documented once, on home
            if fr or hv:
                made.append(stack(fr + hv, f"notion/{slug}__{S['id']}.jpg"))
        mob = sorted(glob.glob(f'img/{slug}/mobile/*.jpg'))
        mob = [m for m in mob if 'state_' not in m or 'menu' in m]
        for i in range(0, len(mob), 6):
            made.append(stack(mob[i:i + 6], f'notion/{slug}__mobile_{i // 6}.jpg', horizontal=True))
        if slug == 'playground':
            d = sorted(glob.glob('img/playground/desktop/*.jpg'))
            if d:
                made.append(stack(d[:3], 'notion/playground__desktop.jpg'))
    st = [p for p in ['img/home/desktop/state_loader_900.jpg', 'img/home/desktop/state_loader_2200.jpg', 'img/home/desktop/state_loader_3800.jpg', 'img/home/desktop/00_loaded.jpg', 'img/home/desktop/state_cursor_trail.jpg', 'img/home/desktop/state_menu_open.jpg'] if os.path.exists(p)]
    if st:
        made.append(grid(st, 'notion/globals__states.jpg', cols=2, cw=720))
    tr = sorted(glob.glob('img/*/desktop/state_transition_*.jpg'))
    if tr:
        made.append(grid(tr, 'notion/globals__transitions.jpg', cols=3, cw=480))
    gal = sorted(glob.glob('img/gal_*/desktop/00_loaded.jpg'))
    if gal:
        made.append(grid(gal, 'notion/gallery__heroes.jpg', cols=3, cw=480))
    gal2 = sorted(glob.glob('img/gal_*/desktop/01_below.jpg'))
    if gal2:
        made.append(grid(gal2, 'notion/gallery__below.jpg', cols=3, cw=480))
    print('\n'.join(m for m in made if m))

# ---------- markdown ----------
class Outline(HTMLParser):
    VOID = {'meta', 'link', 'img', 'br', 'input', 'source', 'path', 'use', 'circle', 'rect', 'line', 'polyline', 'polygon', 'hr', 'stop', 'ellipse'}
    def __init__(s, target, depth):
        super().__init__(); s.t = target; s.maxd = depth; s.d = 0; s.start = None; s.lines = []; s.done = False
    def handle_starttag(s, t, a):
        if t in s.VOID or s.done:
            return
        a = dict(a); s.d += 1
        if a.get('id') == s.t and s.start is None:
            s.start = s.d
        if s.start is not None and s.d - s.start <= s.maxd and t not in ('svg', 'g', 'defs', 'clippath', 'lineargradient'):
            lbl = t + ('#' + a['id'] if a.get('id') else '') + ('.' + '.'.join(a['class'].split()[:3]) if a.get('class') else '')
            if s.lines and s.lines[-1][1] == lbl and s.lines[-1][0] == s.d - s.start:
                s.lines[-1][2] += 1
            else:
                s.lines.append([s.d - s.start, lbl, 1])
    def handle_endtag(s, t):
        if t in s.VOID or s.done:
            return
        if s.start is not None and s.d == s.start:
            s.done = True
        s.d -= 1

def outline(slug, sid, depth=3, cap=40):
    f = HTMLF.get(slug, 'home')
    if sid in ('end-section', 'footer-section', 'scroll-nav-section', 'home-goal'):
        f = 'home'
    try:
        o = Outline(sid, depth); o.feed(open(f'/home/sprite/lusion/html/{f}.html').read())
    except Exception:
        return ''
    ls = ['  ' * d + l + (f'  ×{n}' if n > 1 else '') for d, l, n in o.lines[:cap]]
    if len(o.lines) > cap:
        ls.append(f'  … {len(o.lines) - cap} more nodes')
    return '\n'.join(ls)

def css(prefixes, limit=16):
    import subprocess
    out = subprocess.run(['python3', 'cssq.py'] + prefixes, capture_output=True, text=True).stdout.splitlines()
    base = [l for l in out if not l.startswith('@')]
    mob = [l for l in out if l.startswith('@media (max-width: 812px)') or l.startswith('@media (max-width: 560px)')]
    pick = base[:limit] + mob[:max(4, limit // 2)]
    more = len(out) - len(pick)
    txt = '\n'.join(l if len(l) < 300 else l[:297] + '…' for l in pick)
    return txt, more

def esc(s):
    return H.escape(str(s or ''), quote=False).replace('|', '/')

def legend_table(slug, sid):
    leg = {}
    p = f'img/{slug}/desktop/legend.json'
    if os.path.exists(p):
        leg = json.load(open(p))
    names = [os.path.basename(f)[:-4] for f in frames(slug, 'desktop', sid)] + ([f'state_hover_{sid}'] if f'state_hover_{sid}' in leg else [])
    if sid == 'about-hero':
        names = ['00_loaded']
    rows = []
    for nm in names:
        for r in leg.get(nm, {}).get('rows', []):
            rows.append((nm, r))
    if not rows:
        return ''
    t = ['<table header-row="true">', '<tr><td>Frame</td><td>#</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / background</td><td>Box x,y w×h</td></tr>']
    for nm, r in rows:
        t.append(f"<tr><td>{esc(nm)}</td><td>{r['n']}</td><td>`{esc(r['sel'])[:80]}`</td><td>{esc(r['text'])[:60]}</td><td>{esc(r['font'])}</td><td>{esc(r['color'])} / {esc(r['bg'])}</td><td>{esc(r['box'])}</td></tr>")
    t.append('</table>')
    return '\n'.join(t)

def chlinks(chs):
    return ', '.join(f'[{CH[c]}]({URL[c]})' if c in URL else CH[c] for c in chs)

def img(path, cap):
    return f'[[IMG:{path}|{cap}]]' if os.path.exists(path) else f'*(Screenshot not captured: {path})*'

def section_md(slug, S, num):
    o = [f"## {num}. {S['name']}  `#{S['id']}`", '']
    o.append(img(f"notion/{slug}__{S['id']}.jpg", f"{S['name']}: desktop 1440×900, numbered callouts match the table below"))
    o.append('')
    o.append('**Build spec**')
    o.append(S['spec']); o.append('')
    o.append(f"**Mobile (390 wide):** {S['mobile']}"); o.append('')
    o.append(f"**Driven by:** {', '.join('`' + m + '`' for m in S['modules'])}. Read more: {chlinks(S['ch'])}."); o.append('')
    lt = legend_table(slug, S['id'])
    if lt:
        o.append('**Callouts: measured in the live page at capture time**'); o.append(lt); o.append('')
    o.append('**Driver facts (pulled from the module source)**')
    for m in S['modules'][:3]:
        try:
            F = facts(m)
        except FileNotFoundError:
            continue
        bits = []
        for k in ('DOM hooks', 'SplitType', 'Easings', 'WebGL objects', 'Uniforms', 'Classes toggled', 'Motion samples'):
            if k in F:
                v = '; '.join(F[k])
                bits.append(f"{k}: `{v[:260]}`")
        o.append(f"- `{m}`: " + ' · '.join(bits))
    o.append('')
    c, more = css(S['css'])
    if c:
        o.append('**Exact CSS (desktop rules, then the 812px and 560px overrides)**')
        o.append('```css\n' + c + '\n```')
        if more > 0:
            o.append(f'*{more} more rules match these selectors in the shipped stylesheet (see lusion_pretty.css).*')
        o.append('')
    ol = outline(slug, S['id'])
    if ol:
        o.append('**DOM outline (from the served HTML, 3 levels)**')
        o.append('```\n' + ol + '\n```'); o.append('')
    return '\n'.join(o)

def page_md(P):
    slug = P['slug']
    o = [f"# 15.{P['n']} {P['title']}", '']
    o.append(f'<callout icon="🗺️" color="blue_bg">\n\t{P["summary"]}\n</callout>'); o.append('')
    secs = P['sections'] + (EXTRA if slug == 'home' else [])
    o.append('**Sections in scroll order:** ' + ' → '.join(f"`#{s['id']}`" for s in secs) + ('' if slug == 'home' else ' → shared tail (`#end-section`, `#footer-section`, `#scroll-nav-section`; documented on the Home page)'))
    o.append('')
    o.append(img(f'img/{slug}/desktop/00_loaded.jpg', 'First screen after the preloader, desktop 1440×900'))
    o.append('')
    for i, S in enumerate(secs, 1):
        o.append(section_md(slug, S, i))
    mob = sorted(glob.glob(f'notion/{slug}__mobile_*.jpg'))
    o.append('## Mobile strip (390×844)'); o.append('')
    for m in mob:
        o.append(img(m, 'Mobile key sections in scroll order (left to right)')); o.append('')
    if not mob:
        o.append('*(Mobile captures not available for this page in this run.)*')
    return '\n'.join(o)


def gallery_md(n):
    rows = []
    for p in sorted(glob.glob('raw/gal_*/desktop/meta.json')):
        m = json.load(open(p)); els = m['frames'][0].get('els', [])
        g = lambda i: next((e for e in els if e['id'] == i), None)
        t, d = g('project-details-title'), g('project-details-desc')
        side = [e['text'] for e in els if 'side-list' in (e['id'] + e['cls']) and e['text']][:1]
        rows.append(f"<tr><td>[{esc(t['text'] if t else m['slug'][4:])}](https://lusion.co{m['path']})</td><td>`{m['path']}`</td><td>{esc(t['st']['fs']) if t else ''} {esc(t['st']['fw']) if t else ''}</td><td>{esc(hexc(t['st']['color'])) if t else ''}</td><td>{esc(d['text'][:90]) if d else ''}</td><td>{esc(side[0][:60]) if side else ''}</td></tr>")
    o = [f'# 15.{n} Project pages gallery (the other 18)', '',
         '<callout icon="🖼️" color="blue_bg">\n\tEvery project page uses the same `ProjectPage` template documented in 15.4. This page shows the first screen of each, plus one screen below it, so an agent can check the per-project data (title, description, meta list, media and colour variables) against the template. The values in the table were measured in the live page.\n</callout>', '',
         img('notion/gallery__heroes.jpg', 'First screen of each project page, desktop 1440×900, alphabetical by slug'), '',
         img('notion/gallery__below.jpg', 'One screen further down on each project page: media items start'), '',
         '## Per-project data (measured)', '',
         '<table header-row="true">', '<tr><td>Project</td><td>Route</td><td>Title size / weight</td><td>Title colour</td><td>Description (start)</td><td>Side list (first item)</td></tr>'] + rows + ['</table>', '',
         '## What changes per project and what stays fixed', '',
         '- **Changes:** the title, description, meta (client, year, services), the media list (images, videos, text panels from `ProjectDetailsData`), the `--project-details-*` colour variables, whether there\'s a launch link (`has-cta`), and the next-project target.',
         '- **Fixed:** the layout grid, type scale, title-centred intro (`ease.expoInOut`), media fade-in (`ease.expoOut`), the back button in the header, and the next-project swap at the bottom.',
         '- **To check a rebuild:** render each route from data alone and compare it with the two thumbnails here. The title wrap, the description length and where the first media item sits should match.']
    return '\n'.join(o)

def hexc(c):
    m = re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)', c or '')
    return '#%02x%02x%02x' % tuple(int(float(x)) for x in m.groups()) if m else c

if __name__ == '__main__':
    if sys.argv[1] == 'composites':
        composites()
    else:
        for n, P in enumerate(PAGES, 1):
            P['n'] = n
            if sys.argv[2:] and P['slug'] not in sys.argv[2:]:
                continue
            md = page_md(P)
            open(f"15_{n}_{P['slug']}.md", 'w').write(md)
            print(P['slug'], len(md), 'chars', len(re.findall(r'\[\[IMG:', md)), 'images')
        if not sys.argv[2:] or 'gallery' in sys.argv[2:]:
            md = gallery_md(len(PAGES) + 1)
            open(f'15_{len(PAGES)+1}_gallery.md', 'w').write(md); print('gallery', len(md))
