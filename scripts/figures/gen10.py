# Chapter 10 screenshot composites (live captures + annotations) as HTML for render.mjs
import json, os, glob, sys
sys.path.insert(0, '/home/sprite/lusion/vis')
R = '/home/sprite/lusion/vis/raw'
OUT = '/home/sprite/lusion/vis/html'
from PIL import Image
CSS = open('/home/sprite/lusion/vis/gen_vis.py').read().split('CSS = """')[1].split('"""')[0]
FOOT = '<div class=foot>Live capture of lusion.co (headless Chrome, October 2026) with annotations added for this handbook</div>'
def page(name, body, extra=''):
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset=utf-8><style>{CSS}{extra}</style></head><body>{body}</body></html>')
l = json.load(open(R + '/log10.json'))
cols = l['gridCols']
# 1. grid overlay
first, w = cols[0]
gap = cols[1][0] - (cols[0][0] + cols[0][1])
sc = 1500 / 1440
ann = f'''<div style="position:relative;height:64px;width:1500px">
<div class=br style="left:0;width:{first*sc}px"><span>--base-padding-x<br><b>max(5vw, 40px) = {first}px</b></span></div>
<div class=br style="left:{first*sc}px;width:{w*sc}px;border-color:#ff2878"><span style="color:#ff2878">--grid-space<br><b>{w}px</b></span></div>
<div class=br style="left:{(first+w)*sc}px;width:{gap*sc}px;border-color:#c1ff00"><span style="color:#c1ff00;left:0;transform:none;white-space:nowrap">&nbsp;--grid-gap 2vw \u2248 28.8px</span></div></div>'''
page('10_grid', f'''<h1>The 12-column rhythm, measured on the live site <small>A 12-column overlay built from Lusion's own tokens (<span class=m>--base-padding-x</span>, <span class=m>--grid-gap</span>) and laid over the home page at 1440 × 900. Each column is <span class=m>--grid-space = (100% − 11 × gap) / 12</span>.</small></h1>
<div style="margin-top:26px">{ann}<img src="file://{R}/d_grid.png" style="width:1500px;border-radius:10px;display:block"></div>{FOOT}''',
'.br{position:absolute;bottom:6px;height:14px;border:2px solid #9aa0b8;border-top:none}.br span{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);font-size:13px;text-align:center;line-height:1.25;color:#c9cde0;white-space:nowrap}')
# 2. desktop vs mobile
m = json.load(open(R + '/log10b.json')).get('mobile', {}) if os.path.exists(R + '/log10b.json') else {}
if os.path.exists(R + '/m_hero.png'):
    page('10_breakpoint', f'''<h1>One breakpoint, two layouts: 812px <small>Left: desktop at 1440px. Right: a 390px phone, below <span class=m>(max-width: 812px)</span>. The same rule flips <span class=m>properties.useMobileLayout</span> in JavaScript, so CSS and WebGL switch together.</small></h1>
<div style="display:flex;gap:30px;margin-top:28px;align-items:flex-start">
<div style="flex:1"><div class=lab style="margin-bottom:8px">Desktop · 1440 × 900</div><img src="file://{R}/d_s00.png" style="width:100%;border-radius:10px">
<table class=t><tr><td>--base-padding-x</td><td>max(5vw, 40px) → 72px</td></tr><tr><td>--grid-gap</td><td>2vw → 28.8px</td></tr><tr><td>--global-border-radius</td><td>20px</td></tr></table></div>
<div style="width:330px"><div class=lab style="margin-bottom:8px">Phone · 390 × 844</div><img src="file://{R}/m_hero.png" style="width:100%;border-radius:18px;border:6px solid #262b3d">
<table class=t><tr><td>--base-padding-x</td><td>15px (25px between 401 and 812px)</td></tr><tr><td>--grid-gap</td><td>4vw → 15.6px</td></tr><tr><td>--global-border-radius</td><td>15px</td></tr></table></div></div>
<div style="margin-top:16px;color:#9aa0b8">Only the tokens change at the breakpoint; components keep the same CSS and resize because they are built from the tokens. 812px is used in 129 media queries.</div>{FOOT}''',
'.t{margin-top:12px;border-collapse:collapse;width:100%;font-size:14px}.t td{padding:5px 8px;border-bottom:1px solid #262b3d}.t td:first-child{font-family:DejaVu Sans Mono,monospace;color:#c1ff00}')
# 3. header states on /about
if os.path.exists(R + '/log10b.json'):
    ab = json.load(open(R + '/log10b.json'))['about']
    shots = [f for f in sorted(glob.glob(R + '/a_*.png')) if not f.endswith('a_00.png')]
    rows = ''
    for f in shots:
        i = int(os.path.basename(f)[2:4])
        s = next(x for x in ab if x['i'] == i)
        bg = [c for c in s['html'].split() if c.endswith('-bg')]
        rows += f'''<div class=card style="display:flex;gap:24px;align-items:center;margin-top:16px"><div style="width:250px"><div class=m style="font-size:20px;color:#c1ff00">{bg[0] if bg else 'no class: default'}</div><div style="color:#9aa0b8;font-size:14px;margin-top:4px">scroll step {i}<br>header text: <span class=m>{s['header']}</span></div></div>
<div class=crop><img src="file://{f}"></div></div>'''
    page('10_header', f'''<h1>The header recolours itself as you scroll <small>Live captures of lusion.co/about. The page script works out which background is behind the header and toggles one class on <span class=m>&lt;html&gt;</span>; CSS does the rest. Each row is the top of the screen at the scroll step where the class changed. On this run the order was black, then blue, then white (with <span class=m>is-footer-in</span>).</small></h1>{rows}{FOOT}''',
    '.crop{flex:1;height:170px;overflow:hidden;border-radius:10px}.crop img{width:1240px;display:block}')
print('ok')
