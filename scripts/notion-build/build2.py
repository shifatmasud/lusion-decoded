#!/usr/bin/env python3
"""Compact builder for 15.1 Home and 15.2 About. usage: build2.py composites|md"""
import json, os, sys, glob, re
sys.path.insert(0, '/home/sprite/lusion/handbook/ch15')
import build as B
from build import frames, css, outline, esc, chlinks, img
from content import PAGES, EXTRA, URL
URL.setdefault(4, 'https://app.notion.com/p/3fd48559569d816eb890f8d968ec1fae'); URL.setdefault('4', 'https://app.notion.com/p/3fd48559569d816eb890f8d968ec1fae')
from facts import facts
from PIL import Image, ImageDraw, ImageFont

SH = sorted(os.path.basename(p) for p in glob.glob('/home/sprite/lusion/shaders_by_owner/*.glsl'))
FONT = ImageFont.truetype(B.MONO, 22) if os.path.exists(B.MONO) else ImageFont.load_default()
MEAS = '/home/sprite/lusion/handbook/ch15/notion2'
os.makedirs(MEAS, exist_ok=True)

def secs(slug):
    P = [p for p in PAGES if p['slug'] == slug][0]
    return P, P['sections'] + (EXTRA if slug == 'home' else [])

def visible(slug, mode, path, sid):
    if sid == 'scroll-nav-section':
        return mode == 'mobile' and False
    p = f'raw/{slug}/{mode}/meta.json'
    if not os.path.exists(p):
        return True
    vh = 900 if mode == 'desktop' else 844
    nm = os.path.basename(path)[:-4]
    for f in json.load(open(p))['frames']:
        if f['name'] == nm:
            for x in f.get('sections', []):
                if x['id'] == sid:
                    return x['top'] < vh - 120 and x['top'] + x['h'] > 120
    return True

def inview(slug, mode, sid, n=2):
    p = f'raw/{slug}/{mode}/meta.json'
    if not os.path.exists(p):
        return []
    vh = 900 if mode == 'desktop' else 844
    best = []
    for f in json.load(open(p))['frames']:
        for x in f.get('sections', []):
            if x['id'] == sid:
                ov = min(vh, x['top'] + x['h']) - max(0, x['top'])
                if ov > 300:
                    best.append((ov, f['name']))
    best.sort(reverse=True)
    return [q for q in (f'img/{slug}/{mode}/{nm}.jpg' for _, nm in best[:n]) if os.path.exists(q)]

FORCE = {('home', 'footer-section'): ['img/home/desktop/16_scroll-nav-section_0.jpg'],
         ('home', 'scroll-nav-section'): [], ('about', 'footer-section'): None}

def dframes(slug, sid):
    if FORCE.get((slug, sid)) is not None:
        return [p for p in FORCE[(slug, sid)] if os.path.exists(p)]
    fr = [p for p in frames(slug, 'desktop', sid) if visible(slug, 'desktop', p, sid)] or inview(slug, 'desktop', sid)
    if sid == 'about-hero':
        fr = [f'img/{slug}/desktop/00_loaded.jpg'] + fr[:1]
    hv = glob.glob(f'img/{slug}/desktop/state_hover_{sid}.jpg')
    return [p for p in fr + hv if os.path.exists(p)]

def mframes(slug, sid):
    fr = [p for p in frames(slug, 'mobile', sid) if visible(slug, 'mobile', p, sid)] or inview(slug, 'mobile', sid)
    if sid == 'about-hero' or (sid == 'home-hero' and not fr):
        fr = [f'img/{slug}/mobile/00_loaded.jpg'] + fr
    if sid == 'home-hero':
        fr += glob.glob(f'img/{slug}/mobile/state_menu_open.jpg')
    return [p for p in fr if os.path.exists(p)][:4]

def label(canvas, y, text):
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, y, canvas.width, y + 40], fill=(17, 17, 17))
    d.text((14, y + 8), text, fill=(255, 255, 255), font=FONT)

def composite(slug, sid):
    D = [Image.open(p).convert('RGB') for p in dframes(slug, sid)]
    M = [Image.open(p).convert('RGB') for p in mframes(slug, sid)]
    if not D and not M:
        return None
    W = 1200
    D = [im.resize((W, int(im.height * W / im.width))) for im in D]
    mh = 600
    M = [im.resize((int(im.width * mh / im.height), mh)) for im in M]
    H = 40 + sum(i.height + 8 for i in D) + ((40 + mh + 8) if M else 0)
    c = Image.new('RGB', (W, H), 'white')
    y = 0
    label(c, y, f'#{sid}  DESKTOP 1440x900  ({len(D)} frame{"s" if len(D) != 1 else ""}, numbered callouts = table)'); y += 40
    for im in D:
        c.paste(im, (0, y)); y += im.height + 8
    if M:
        label(c, y, f'MOBILE 390x844  (left to right in scroll order)'); y += 40
        x = 0
        for im in M:
            if x + im.width > W:
                break
            c.paste(im, (x, y)); x += im.width + 12
    out = f'{MEAS}/{slug}__{sid}.jpg'
    c.save(out, quality=82)
    return out

def shaders(mods):
    out = []
    for m in mods:
        cls = re.sub(r'^\d+_', '', m)
        roots = {cls, cls.replace('Section', '')}
        for s in SH:
            own = s.split('__')[0]
            if own in roots and s not in out:
                out.append(s)
    return out

def legend(slug, sid, cap=7):
    p = f'img/{slug}/desktop/legend.json'
    if not os.path.exists(p):
        return ''
    leg = json.load(open(p))
    names = [os.path.basename(f)[:-4] for f in dframes(slug, sid)]
    rows, seen = [], set()
    for nm in names:
        for r in leg.get(nm, {}).get('rows', []):
            rows.append((nm, r))
    stem = sid.replace('-section', '').replace('home-', 'home-').split('-')[0] if sid.startswith(('footer', 'end', 'scroll')) else sid
    own = [x for x in rows if stem in x[1]['sel'] or (sid == 'home-featured' and 'project-item' in x[1]['sel'])]
    rows = own or rows
    if not rows:
        return ''
    t = ['<table header-row="true">', '<tr><td>Frame · #</td><td>Element</td><td>Text</td><td>Type (computed)</td><td>Colour / bg</td><td>Box x,y w×h</td></tr>']
    for nm, r in rows[:cap]:
        fr = nm.split('_')[0] if nm[0].isdigit() else nm.replace('state_', '').split('_')[0]
        t.append(f"<tr><td>{esc(fr)} · {r['n']}</td><td>`{esc(r['sel'])[:60]}`</td><td>{esc(r['text'])[:40]}</td><td>{esc(r['font'])[:60]}</td><td>{esc(r['color'])} / {esc(r['bg'])}</td><td>{esc(r['box'])}</td></tr>")
    t.append('</table>')
    if len(rows) > cap:
        t.append(f'*{len(rows) - cap} more callouts are in the image and in img/{slug}/desktop/legend.json.*')
    return '\n'.join(t)

UP = {}
TOKENS = '''--color-blue: #1a2ffb;  --color-dark-blue: #071bdf;  --header-color: #0016ec;
--color-black: #000000; --color-white: #fff;  --color-off-white: #f0f1fa;  --color-dark-white: #e4e6ef;
--color-grey-blue: #2b2e3a; --color-green: #c1ff00; --color-red: #ff4c41; --color-purple: #8832f7;
--grid-gap: 2vw;            /* 4vw at max-width 812px */
--grid-space: calc((100% - 11 * var(--grid-gap)) / 12);   /* 12 columns; 6 on mobile */
--base-padding-x: max(5vw, 40px);        /* 25px <=812px, 15px <=400px, max(6vw,60px) at >=21:9 */
--base-padding-y: clamp(30px, 4vw, 50px); /* 25px <=812px, 15px <=400px */
--global-border-radius: 20px;             /* 10px at <=812px */
--header-size: clamp(1rem, 1vw, 2rem);  --cross-size: clamp(0.875rem, 1vw, 2rem);'''

def section_md(slug, S, num):
    o = [f"## {num}. {S['name']}  `#{S['id']}`", '']
    p = f'{MEAS}/{slug}__{S["id"]}.jpg'
    if S['id'] == 'scroll-nav-section' and slug == 'home':
        o.append('*No screenshot: in the headless capture this bar stays below the last reachable scroll position (its top measured at 924px in a 900px viewport at maximum scroll), so it never entered the frame. The spec below comes from the CSS and module source.*')
    else:
        o.append(f'[[IMG:{p}|{S["name"]}: desktop frames with numbered callouts, mobile row underneath]]' if os.path.exists(p) else '*(Screenshot not captured in this run.)*')
    o.append('')
    o.append('**Rebuild spec**'); o.append(S['spec']); o.append('')
    o.append(f"**Mobile (390 wide):** {S['mobile']}"); o.append('')
    sh = shaders(S['modules'])
    o.append(f"**Driven by:** {', '.join('`' + m + '`' for m in S['modules'])}." + (f" Shaders: {', '.join('`' + s + '`' for s in sh[:10])}{' …' if len(sh) > 10 else ''}." if sh else ' No section-specific shader files (HTML + shared Ufx/post passes).') + f" Handbook: {chlinks(S['ch'])}.")
    o.append('')
    lt = legend(slug, S['id'])
    if lt:
        o.append('**Callouts (measured on the live page at capture time)**'); o.append(lt); o.append('')
    bits_all = []
    for m in S['modules'][:2]:
        try:
            F = facts(m)
        except Exception:
            continue
        bits = [f"{k}: `{'; '.join(F[k])[:160]}`" for k in ('DOM hooks', 'Easings', 'Uniforms', 'Classes toggled') if k in F]
        if bits:
            bits_all.append(f"- `{m}`: " + ' · '.join(bits))
    if bits_all:
        o.append('**Driver facts (from the module source)**'); o += bits_all; o.append('')
    c, more = css(S["css"], limit=7)
    if c:
        o.append('**Exact CSS (desktop rules, then 812px / 560px overrides)**')
        o.append('```css\n' + c + '\n```')
        if more > 0:
            o.append(f'*{more} more matching rules in lusion_pretty.css.*')
        o.append('')
    ol = outline(slug, S['id'], depth=2, cap=10)
    if ol:
        o.append('**DOM outline (served HTML, 2 levels)**'); o.append('```\n' + ol + '\n```'); o.append('')
    return '\n'.join(o)

def page_md(slug):
    P, ss = secs(slug)
    o = [f'<callout icon="🗺️" color="blue_bg">\n\t{P["summary"]}\n</callout>', '']
    o.append('**Sections in scroll order:** ' + ' → '.join(f"`#{s['id']}`" for s in ss) + ('' if slug == 'home' else ' → shared tail (`#end-section`, `#footer-section`, `#scroll-nav-section`, documented on 15.1 Home)'))
    o.append('')
    o.append('**How to read this page:** each section has one image (desktop 1440×900 frames on top, mobile 390×844 row below). Numbers in the image match the callout table. Values in code blocks and tables are exact (from the shipped CSS, module source or measured computed styles); anything written as *inferred* is a reading, not a measured value. Screenshots come from a headless browser with software WebGL, so glow and colour can look flatter than on a real GPU.')
    o.append('')
    o.append('**Tokens every section below uses (exact, from `:root` in the shipped CSS)**')
    o.append('```css\n' + TOKENS + '\n```')
    o.append('Fonts: Aeonik 400 / 500 / 400 italic (body and display), IBMPlexMono 400 / 500 and LusionMono 400 (labels, counters, crosses), all `font-display: block` from `/assets/fonts/`. Background state is a class on `<html>`: `is-black-bg`, `is-blue-bg` or `is-white-bg`; under the first two the header text and scroll bar turn white.')
    o.append('')
    for i, S in enumerate(ss, 1):
        o.append(section_md(slug, S, i))
    return '\n'.join(o)

if __name__ == '__main__':
    what = sys.argv[1]
    slugs = sys.argv[2:] or ['home', 'about']
    for slug in slugs:
        if what == 'composites':
            for S in secs(slug)[1]:
                print(composite(slug, S['id']))
        else:
            md = page_md(slug)
            open(f'15_{dict(home=1,about=2)[slug]}_{slug}.src.md', 'w').write(md)
            print(slug, len(md), md.count('[[IMG:'))
