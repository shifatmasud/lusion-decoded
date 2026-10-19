# Generates HTML sources for the chapter 10-13 diagrams; render.mjs turns them into PNGs.
import json, re, os, html, collections
B = '/home/sprite/lusion'
OUT = B + '/vis/html'
os.makedirs(OUT, exist_ok=True)
E = html.escape

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1600px;background:#0d0f17;color:#e9ebf5;font:16px/1.4 'DejaVu Sans',Arial,sans-serif;padding:48px}
h1{font-size:34px;font-weight:700;letter-spacing:-.5px}
h1 small{display:block;font-size:17px;font-weight:400;color:#9aa0b8;margin-top:6px}
.k{color:#c1ff00}.b{color:#6f7dff}.m{font-family:'DejaVu Sans Mono',monospace}
.card{background:#161a26;border:1px solid #262b3d;border-radius:16px;padding:20px}
.lab{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:#8b91aa}
.foot{margin-top:28px;color:#6d7390;font-size:13px}
"""
def page(name, body, extra=''):
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset=utf-8><style>{CSS}{extra}</style></head><body>{body}</body></html>')

FOOT = '<div class=foot>Lusion.co Decoded handbook · diagram drawn from the study files, not Lusion artwork</div>'

# ---------- 10: rolling letters ----------
frames = [('0%', 0, 'translateZ(0): start, original letter showing'), ('33%', 1, 'translate3d(0, 1.5em, 0): move done in the first third'), ('to (100%)', 1, 'still 1.5em: the hold is the built-in rest')]
cells = ''
for pct, up, txt in frames:
    off = -1 if up else 0
    cells += f'''<div class=card style="flex:1"><div class=lab>keyframe {pct}</div>
<div class=stage><div class=win></div><div class=wrap style="transform:translateY({off*96}px)"><div class=ch>L</div><div class=ch clone>L</div></div></div>
<div style="margin-top:14px;color:#b9bed3" class=m>{E(txt)}</div></div>'''
page('10_rolling', f'''<h1>Rolling letters: one window, two copies <small>SplitType splits the word; each character is cloned into a <span class=m>.char-wrapper</span>. The word box clips to one line, so moving the wrapper swaps which copy you see.</small></h1>
<div style="display:flex;gap:24px;margin-top:32px">{cells}</div>
<div class=card style="margin-top:24px;display:flex;gap:40px;align-items:center">
<div><div class=lab>DOM after the split</div><pre class=m style="margin-top:10px;color:#c9cde0;font-size:15px">&lt;div class="home-reel-video-title-word"&gt;   <span class=k>overflow:hidden; height:.8em</span>
  &lt;div class="char-wrapper"&gt;               <span class=k>inline-block, moves</span>
    &lt;div&gt;L&lt;/div&gt;   <span class=b>original</span>
    &lt;div&gt;L&lt;/div&gt;   <span class=b>clone (cloneNode)</span>
  &lt;/div&gt; ...one wrapper per letter
&lt;/div&gt;</pre></div>
<div style="flex:1;color:#b9bed3">Only <span class=m>transform</span> changes, so the browser can run it on the compositor. The swap shown here follows 10.6: the clone slides in as the wrapper moves. That direction is inferred; the exact per-section animation code was not traced.</div></div>{FOOT}''',
'''.stage{position:relative;height:260px;margin-top:14px;display:flex;justify-content:center;align-items:center;background:#0d0f17;border-radius:12px;overflow:hidden}
.win{position:absolute;left:50%;top:50%;width:120px;height:96px;transform:translate(-50%,-50%);border:3px dashed #c1ff00;border-radius:8px;z-index:3;box-shadow:0 0 0 999px rgba(13,15,23,.72)}
.wrap{display:flex;flex-direction:column;align-items:center;transition:none;transform-origin:center}
.ch{font:700 84px/96px 'DejaVu Sans';height:96px;color:#fff}.ch[clone]{color:#6f7dff}''')

# ---------- 11: architecture poster ----------
layers = [
 ('6', 'Render pipeline', 'Postprocessing \u00b7 PostEffect subclasses \u00b7 FboHelper', 'Turn the stage into the final image; passes sorted by a number', 'Bloom 10 \u2192 Final 30 \u2192 PreUfx 50 \u2192 ScreenPaintDistortion 75 \u2192 PostUfx 100 \u2192 Smaa 500 \u2192 Fsr 2000'),
 ('5', '3D', 'Visuals \u00b7 Stage3D \u00b7 HomeBalloons \u00b7 GoalTunnels \u00b7 AboutHero', 'Scenes that mirror what the DOM says is on screen; one active stage per frame', ''),
 ('4', 'DOM', 'PageManager \u00b7 Page \u00b7 *Section \u00b7 Header \u00b7 UI', 'Real HTML pages and sections; layout lives in CSS, JS toggles classes and transforms', ''),
 ('3', 'Services', 'Input \u00b7 ScrollPane / ScrollManager \u00b7 QuickLoader \u00b7 TaskManager \u00b7 RouteManager \u00b7 Audios', 'Singletons ticked by the loop', ''),
 ('2', 'Shared state', 'Properties (+ sharedUniforms)', 'One place for every value systems share; nobody owns it', ''),
 ('1', 'Core utilities', 'MathUtils \u00b7 Ease \u00b7 Tween \u00b7 SecondOrderDynamics \u00b7 Simple1DNoise', 'Pure maths and motion: no DOM, no WebGL, no state', ''),
 ('0', 'Platform', 'Settings \u00b7 Browser \u00b7 Support', 'Know the device before anything runs; read-only after boot', ''),
]
rows = ''
for i, (n, name, cls, own, extra) in enumerate(layers):
    hue = 232 - i * 12
    ex = ('<div class=m style="color:#fff;font-size:13px;margin-top:6px;background:#0d0f17;padding:5px 8px;border-radius:6px;display:inline-block">' + extra + '</div>') if extra else ''
    rows += f'''<div class=layer style="background:linear-gradient(90deg,hsl({hue},80%,{30+i*2}%),#161a26 70%)"><div class=ln>{n}</div><div style="flex:1"><div style="font-size:21px;font-weight:700">{name}</div><div style="color:#c9cde0;margin-top:2px">{own}</div><div class=m style="color:#c1ff00;font-size:13.5px;margin-top:6px">{cls}</div>{ex}</div></div>'''
loop = ['rAF', 'dt = min(1/20, elapsed)', 'Tween.autoUpdate', 'taskManager.update', 'properties.reset', 'app.preUpdate', 'input.update', 'scrollManager.update', 'pagesManager.update', 'ui.update', 'app.update', 'input.postUpdate']
loopc = ''.join(f'<div class=step><span class=sn>{i}</span>{E(s)}</div>' for i, s in enumerate(loop))
page('11_poster', f'''<h1>Lusion.co on one page <small>One clock, one state bag, one lifecycle contract (preInit, init, start, resize, update), one render queue. Layers 0 to 6 as in 11.1; each builds on the ones below.</small></h1>
<div style="display:grid;grid-template-columns:1fr 430px;gap:28px;margin-top:30px">
<div><div class=lab style="margin-bottom:10px">The seven layers</div>{rows}</div>
<div style="display:flex;flex-direction:column;gap:20px">
<div class=card style="border-color:#c1ff00"><div class=lab>Shared state</div><div style="font-size:22px;font-weight:700;margin:6px 0" class=k>properties (blackboard)</div>
<div style="color:#c9cde0">Pages, sections and the active Stage3D <b>write</b> look values such as <span class=m>bloomAmount</span>, <span class=m>saturation</span>, <span class=m>vignetteFrom</span>. <span class=m>App.update</span> copies them into the effects every frame, and shared uniforms like <span class=m>u_time</span> reach every material. Scenes never talk to effects directly.</div></div>
<div class=card><div class=lab>Every frame, in this order</div><div style="margin-top:10px">{loopc}</div></div>
<div class=card><div class=lab>Boot</div><div style="display:flex;gap:8px;margin-top:10px" class=m><div class=pill>run()</div>→<div class=pill>init()</div>→<div class=pill>start()</div></div><div style="color:#9aa0b8;margin-top:8px;font-size:14px">The loop starts inside run(), before loading ends. The preloader calls init at files 100% and start at GPU tasks 100%.</div></div>
</div></div>
<div class=card style="margin-top:28px;display:flex;gap:28px;align-items:center"><div class=lab style="width:170px">Conceptual model</div>
<div style="flex:1;display:flex;gap:18px;align-items:center"><div class=doc><b>HTML document</b><br><span style="color:#9aa0b8">real text, links, layout · moved by the virtual scroller · recoloured by CSS classes</span></div>
<div class=m style="color:#c1ff00;text-align:center">scroll is the<br>shared timeline</div>
<div class=doc style="border-color:#6f7dff"><b>GPU document</b><br><span style="color:#9aa0b8">3D scenes + textured copies of HTML (Ufx) · one canvas behind and on top</span></div></div></div>{FOOT}''',
'''.layer{display:flex;gap:18px;align-items:center;border:1px solid #2c3247;border-radius:14px;padding:14px 18px;margin-bottom:10px}
.ln{font:700 34px 'DejaVu Sans Mono';width:44px;color:#fff;opacity:.9}
.step{font:14.5px 'DejaVu Sans Mono';padding:5px 8px;border-left:3px solid #6f7dff;margin:4px 0;background:#10131d;border-radius:4px}
.sn{display:inline-block;width:26px;color:#8b91aa}
.pill{background:#1f2540;border:1px solid #6f7dff;border-radius:999px;padding:6px 14px}
.doc{flex:1;border:2px solid #c1ff00;border-radius:12px;padding:16px;background:#10131d}''')

# ---------- 11: pixel budget ----------
sc = 0.16
def box(w, h, col, label):
    return f'<div style="width:{w*sc}px;height:{h*sc}px;border:3px solid {col};border-radius:6px;display:flex;align-items:flex-end;padding:8px;color:{col};font-weight:700">{label}</div>'
import math
W4, H4 = 3840, 2160
MAX = 2560*1440
a = W4 / H4; n = math.sqrt(MAX / a); r = math.ceil(n * a); n = math.ceil(n)
page('11_pixels', f'''<h1>The pixel budget <small>DPR is capped at 1.5, then the drawing size is scaled down to at most 2560 × 1440 = 3,686,400 pixels, keeping the aspect ratio.</small></h1>
<div style="display:flex;gap:40px;margin-top:34px;align-items:flex-end">
<div class=card style="flex:1"><div class=lab>4K monitor, DPR 1</div><div style="margin-top:14px;position:relative">{box(W4,H4,'#ff4c41','3840 × 2160 = 8,294,400 px requested')}
<div style="position:absolute;left:0;bottom:0">{box(r,n,'#c1ff00',f'{r} × {n} ≈ {r*n:,} px drawn')}</div></div></div>
<div class=card style="width:520px"><div class=lab>The rule (141_preRun.js)</div><pre class=m style="margin-top:10px;font-size:14px;color:#c9cde0;white-space:pre-wrap">if (r * n &gt; MAX_PIXEL_COUNT) {{
  a = r / n;            // aspect
  n = sqrt(MAX / a);    // new height
  r = ceil(n * a);      // new width
}}</pre><div style="margin-top:14px;color:#b9bed3">About <b class=k>{r*n/(W4*H4)*100:.0f}%</b> of the pixels, so a big monitor costs roughly what a 1440p laptop does. The optional FSR upscaler (last pass) can render smaller still and sharpen back up.</div></div></div>{FOOT}''')

# ---------- 12: minified vs pretty ----------
mini = open(B + '/vis/min_snip.txt').read().strip()
pretty = open(B + '/js/hoisted.pretty.js').read().split('\n')[43039:43062]
page('12_pretty', f'''<h1>Step 2: the same bytes, before and after pretty-print <small>The main loop of Lusion's bundle (/_astro/hoisted.CUO_IjfL.js). Locals are minified to <span class=m>o, e</span>, but <span class=k>class, method and property names survive</span>, which is what makes a teardown possible.</small></h1>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:30px">
<div class=card><div class=lab>As shipped: one line, 1,251,728 bytes</div><div class=m style="margin-top:12px;font-size:14px;color:#c9cde0;word-break:break-all;line-height:1.55">{E(mini)}</div></div>
<div class=card><div class=lab>After prettier --parser babel (DevTools {{}} does the same)</div><pre class=m style="margin-top:12px;font-size:14px;color:#c9cde0;line-height:1.5">{E(chr(10).join(pretty))}</pre></div></div>{FOOT}''')

# ---------- 12: bundle byte map ----------
idx = [l.strip().split('\t') for l in open(B + '/modules/INDEX.tsv')]
TOTAL = 1251728
segs = ''
for name, s, ln in idx:
    s, ln = int(s), int(ln)
    lib = name.startswith('00_') or '_lib_' in name
    col = '#ff4c41' if name.startswith('00_') else ('#f5a524' if lib else '#1a2ffb')
    segs += f'<div title="{name}" style="position:absolute;left:{s/TOTAL*100}%;width:{max(ln/TOTAL*100,0.05)}%;top:0;bottom:0;background:{col};border-right:1px solid #0d0f17"></div>'
libs = [(n, int(s), int(l)) for n, s, l in idx if '_lib_' in n]
librows = ''.join(f'<tr><td class=m>{n.split("_lib_")[1]}</td><td class=m style="text-align:right">{s:,}</td><td class=m style="text-align:right">{l:,}</td></tr>' for n, s, l in libs)
ticks = ''.join(f'<div style="position:absolute;left:{v/TOTAL*100}%;top:0;transform:translateX(-50%);color:#8b91aa;font-size:13px" class=m>{v//1000}k</div>' for v in [0, 250000, 500000, 750000, 1000000, 1250000])
page('12_bytemap', f'''<h1>Step 3: where the libraries end <small>Every byte of the 1,251,728-byte bundle, coloured by what owns it. The split script cut it into 141 numbered files.</small></h1>
<div class=card style="margin-top:30px"><div style="position:relative;height:90px;border-radius:8px;overflow:hidden;background:#222">{segs}</div>
<div style="position:relative;height:22px;margin-top:6px">{ticks}</div>
<div style="display:flex;gap:30px;margin-top:14px"><div><span class=sw style="background:#ff4c41"></span>three.js r158 core: bytes 0 to 532,149 (about 43%)</div><div><span class=sw style="background:#1a2ffb"></span>Lusion's own classes</div><div><span class=sw style="background:#f5a524"></span>small bundled libraries</div></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:24px"><div class=card><div class=lab>Bundled libraries found by marker search</div><table style="width:100%;margin-top:10px;border-collapse:collapse"><tr style="color:#8b91aa"><td>library</td><td style="text-align:right">starts at byte</td><td style="text-align:right">bytes</td></tr>{librows}</table></div>
<div class=card><div class=lab>How to read it</div><div style="margin-top:10px;color:#c9cde0">Skip the red block: it is three.js, documented elsewhere. The blue stripes are what you study. Bundle order is roughly dependency order, so files 001 to 141 read the site bottom-up: maths and settings first, scenes and pages later, <span class=m>preRun</span> last.</div></div></div>{FOOT}''',
'.sw{display:inline-block;width:16px;height:16px;border-radius:4px;vertical-align:-2px;margin-right:8px}td{padding:4px 0;border-bottom:1px solid #262b3d}')

# ---------- 12: probe dashboard ----------
rep = json.load(open(B + '/runtime/home_report.json'))
resp = rep['responses']
cnt = collections.Counter(x['type'] for x in resp)
byt = collections.Counter()
for x in resp: byt[x['type']] += x['len']
tot = sum(byt.values())
typ = sorted(cnt, key=lambda k: -byt[k])
colors = {'media': '#ff4c41', 'image': '#c1ff00', 'xhr': '#6f7dff', 'fetch': '#f5a524', 'script': '#8832f7', 'font': '#00d1c1', 'stylesheet': '#ff8ad8', 'document': '#ffffff', 'ping': '#666'}
bars = ''.join(f'<div style="display:flex;align-items:center;gap:12px;margin:7px 0"><div class=m style="width:100px">{t}</div><div style="flex:1;background:#10131d;border-radius:4px;height:22px"><div style="width:{max(byt[t]/tot*100,0.4)}%;height:100%;background:{colors.get(t,"#888")};border-radius:4px"></div></div><div class=m style="width:210px;text-align:right;color:#c9cde0">{byt[t]/1e6:.2f} MB · {cnt[t]} req</div></div>' for t in typ)
dots = ''
maxt = max(x['t'] for x in resp)
for i, x in enumerate(sorted(resp, key=lambda x: x['t'])):
    dots += f'<div style="position:absolute;left:{x["t"]/maxt*100}%;top:{(i%14)*9}px;width:8px;height:8px;border-radius:50%;background:{colors.get(x["type"],"#888")}"></div>'
g = rep['gl']
dpf = g['dpfTail']
spark = ''.join(f'<div style="flex:1;height:{v*6}px;background:#6f7dff;border-radius:2px 2px 0 0"></div>' for v in dpf)
stats = [('48', 'shader programs linked', 'during one headless run'), ('84', 'textures created', 'createTexture calls'), ('22', 'framebuffers', 'off-screen render targets'), ('14–16', 'draw calls per frame', 'steady state, last 60 frames'), (str(len(resp)), 'network responses', f'{tot/1e6:.1f} MB in {maxt/1000:.0f} s'), ('1', 'WebGL2 context', 'antialias off, alpha off')]
st = ''.join(f'<div class=card><div style="font:700 44px DejaVu Sans;color:#c1ff00">{a}</div><div style="font-weight:700;margin-top:2px">{b}</div><div style="color:#8b91aa;font-size:14px">{c}</div></div>' for a, b, c in stats)
page('12_probe', f'''<h1>Step 7: what the runtime probe saw <small>Puppeteer opened lusion.co at 1440 × 900 with WebGL wrapped before the page created its context, then scrolled. Numbers from runtime/home_report.json.</small></h1>
<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:28px">{st}</div>
<div style="display:grid;grid-template-columns:1.2fr 1fr;gap:24px;margin-top:24px">
<div class=card><div class=lab>Bytes by request type (the Network tab, summed)</div><div style="margin-top:10px">{bars}</div><div style="color:#8b91aa;font-size:14px;margin-top:8px">The showreel video (reel/desktop.mp4) is most of the weight. 89 of the 126 requests, about 25 MB, go to lusion.dev, a separate asset host.</div></div>
<div style="display:flex;flex-direction:column;gap:24px"><div class=card><div class=lab>Draw calls per frame (last 60 frames)</div><div style="display:flex;align-items:flex-end;gap:2px;height:110px;margin-top:12px;border-bottom:1px solid #2c3247">{spark}</div><div style="color:#8b91aa;font-size:14px;margin-top:8px">16 for 45 frames, then 14 for the last 15. The whole home page is a handful of passes, not hundreds of meshes.</div></div>
<div class=card><div class=lab>Requests over time (0 to {maxt/1000:.0f} s)</div><div style="position:relative;height:130px;margin-top:12px">{dots}</div></div></div></div>{FOOT}''')

# ---------- 13: class family map ----------
lay = json.load(open(B + '/vis/layers13.json'))
laycols = ['#00d1c1', '#ff4c41', '#6f7dff', '#f5a524', '#c1ff00', '#ff8ad8', '#8832f7']
cols = ''
for (title, rows), c in zip(lay, laycols):
    m = sum(x[4] for x in rows)
    chips = ''
    for cname, parent, mod, stt, mc in sorted(rows, key=lambda x: -x[4]):
        fs = 12 + min(mc, 30) * 0.32
        conf = stt == 'Confirmed'
        par = f'<span style="opacity:.7"> ← {parent}</span>' if parent else ''
        chips += f'<span class=chip style="font-size:{fs:.1f}px;border-color:{c};{"background:"+c+"33" if conf else ""}">{cname}{par} <span style="opacity:.6">{mc}</span></span>'
    short = title.split(' (')[0]
    cols += f'<div class=card style="border-top:5px solid {c}"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font-size:20px;font-weight:700">{short}</div><div class=m style="color:{c}">{len(rows)} classes · {m} methods</div></div><div style="margin-top:12px;line-height:2.1">{chips}</div></div>'
kids = collections.defaultdict(list)
for _t, rows in lay:
    for cname, parent, mod, stt, mc in rows:
        if parent: kids[parent].append(cname)
bases = [(p, ', '.join(sorted(k))) for p, k in sorted(kids.items(), key=lambda x: -len(x[1])) if len(k) >= 2]
br = ''.join(f'<div style="margin:6px 0"><span class=m style="color:#c1ff00">{a}</span> <span style="color:#8b91aa">→</span> {b}</div>' for a, b in bases)
page('13_family', f'''<h1>Class family map <small>Lusion's own classes from chapter 13.4, one card per layer. Chip size = number of methods (number after the name). <span style="background:#ffffff22;padding:1px 6px;border-radius:4px">Filled</span> = purpose confirmed by reading code, outlined = inferred from the name. ← shows the parent class.</small></h1>
<div class=card style="margin-top:24px;border-color:#c1ff00"><div class=lab>Parent classes with two or more children (from the extends column)</div><div style="margin-top:8px;font-size:15.5px">{br}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px">{cols}</div>{FOOT}''',
'.chip{display:inline-block;border:1.5px solid;border-radius:999px;padding:1px 10px;margin:0 6px 4px 0;white-space:nowrap;color:#eef}')
print('ok', os.listdir(OUT))
