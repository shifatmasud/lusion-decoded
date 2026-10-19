#!/usr/bin/env python3
"""Draw numbered callouts on atlas screenshots from meta.json and write legend JSON.
usage: annotate.py <slug> <mode>"""
import json, re, sys, os
from PIL import Image, ImageDraw, ImageFont

slug, mode = sys.argv[1], sys.argv[2]
src = f'raw/{slug}/{mode}'
dst = f'img/{slug}/{mode}'
os.makedirs(dst, exist_ok=True)
meta = json.load(open(f'{src}/meta.json'))
if os.path.exists(f'{src}/meta_states.json'):
    have = {f['name'] for f in meta['frames']}
    meta['frames'] += [f for f in json.load(open(f'{src}/meta_states.json'))['frames'] if f['name'].startswith('state_') and f['name'] not in have]
FONT = os.path.expanduser('~/.fonts/Inter.ttf')
MONO = os.path.expanduser('~/.fonts/JetBrainsMono.ttf')
COLS = ['#ff2d55', '#00c2ff', '#ffb800', '#7cff00', '#b16cff', '#ff7a00']

def hexc(c):
    m = re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)', c or '')
    if not m:
        return c
    r, g, b = (int(float(x)) for x in m.groups()[:3])
    a = m.group(4)
    h = f'#{r:02x}{g:02x}{b:02x}'
    if a is not None and float(a) < 1:
        return 'transparent' if float(a) == 0 else f'{h} @{float(a):.2f}'
    return h

legend = {}
scale = 1.0 if mode == 'mobile' else 1.0
for fr in meta['frames']:
    p = f"{src}/{fr['name']}.png"
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert('RGB')
    W, H = im.size
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = ImageFont.truetype(FONT, 15 if mode == 'desktop' else 13)
    els = fr.get('els', [])
    if not fr['name'].startswith('state_menu'):
        els = [e for e in els if not (e['id'].startswith('header') or 'header-' in e['cls'] or e['id'] in ('ui', 'page-container', 'page-container-inner'))]
    rows = []
    for i, e in enumerate(els, 1):
        col = COLS[(i - 1) % len(COLS)]
        x, y, w, h = e['x'], e['y'], e['w'], e['h']
        x0, y0, x1, y1 = max(0, x), max(0, y), min(W - 1, x + w), min(H - 1, y + h)
        d.rectangle([x0, y0, x1, y1], outline=col, width=2)
        r = 12 if mode == 'desktop' else 10
        cx, cy = min(max(x0 + r + 2, r + 2), W - r - 2), min(max(y0 + r + 2, r + 2), H - r - 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline='white', width=2)
        t = str(i)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - (9 if mode == 'desktop' else 8)), t, fill='black', font=f)
        st = e['st']
        sel = (e['tag'] + ('#' + e['id'] if e['id'] else '') + ('.' + e['cls'].replace(' ', '.') if e['cls'] and not e['id'] else ''))
        rows.append({'n': i, 'sel': sel, 'text': e['text'], 'box': f"{x},{y} {w}x{h}", 'font': f"{st['ff']} {st['fs']}/{st['lh']} w{st['fw']} ls {st['ls']}" + (f" {st['tt']}" if st['tt'] != 'none' else ''), 'color': hexc(st['color']), 'bg': hexc(st['bg']), 'grid': st.get('gtc', 0), 'radius': st.get('br', '0px')})
    out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    # caption strip
    cap = ImageDraw.Draw(out)
    fm = ImageFont.truetype(MONO, 12)
    label = f"lusion.co{meta['path']}  |  {fr['name']}  |  {mode} {W}x{H}"
    tw = cap.textlength(label, font=fm)
    cap.rectangle([W - tw - 16, H - 22, W, H], fill='black')
    cap.text((W - tw - 8, H - 19), label, fill='white', font=fm)
    out.save(f"{dst}/{fr['name']}.jpg", quality=78)
    legend[fr['name']] = {'section': fr.get('section'), 'rows': rows, 'headerCls': fr.get('headerCls', '')}
# states without meta (loader, transition) are copied as-is with a caption
for fn in sorted(os.listdir(src)):
    if fn.endswith('.png') and fn[:-4] not in legend:
        im = Image.open(f'{src}/{fn}').convert('RGB')
        W, H = im.size
        cap = ImageDraw.Draw(im)
        fm = ImageFont.truetype(MONO, 12)
        label = f"lusion.co{meta['path']}  |  {fn[:-4]}  |  {mode} {W}x{H}"
        tw = cap.textlength(label, font=fm)
        cap.rectangle([W - tw - 16, H - 22, W, H], fill='black')
        cap.text((W - tw - 8, H - 19), label, fill='white', font=fm)
        im.save(f'{dst}/{fn[:-4]}.jpg', quality=78)
        legend.setdefault(fn[:-4], {'section': None, 'rows': []})
json.dump(legend, open(f'{dst}/legend.json', 'w'), indent=1)
print(slug, mode, len(legend), 'images')
