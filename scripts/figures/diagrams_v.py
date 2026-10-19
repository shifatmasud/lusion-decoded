# Generated explainer diagrams for handbook chapters 1-4 (PIL only).
import json, os
from PIL import Image, ImageDraw, ImageFont

OUT = 'img/v'
os.makedirs(OUT, exist_ok=True)
BG = (14, 16, 22); FG = (232, 234, 240); MUT = (140, 146, 160); GRID = (40, 44, 56)
C = {'blue': (77, 139, 255), 'teal': (40, 200, 170), 'amber': (255, 176, 59), 'pink': (255, 95, 140),
     'violet': (160, 110, 255), 'grey': (90, 96, 112), 'green': (110, 210, 90)}

def font(size, bold=False, mono=False):
    path = '/home/sprite/.fonts/JetBrainsMono.ttf' if mono else '/home/sprite/.fonts/Inter.ttf'
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name('Bold' if bold else ('Medium' if mono else 'Regular'))
    except Exception:
        pass
    return f

def canvas(w, h, title, sub=None):
    im = Image.new('RGB', (w, h), BG); d = ImageDraw.Draw(im)
    d.text((48, 36), title, font=font(34, True), fill=FG)
    if sub: d.text((48, 82), sub, font=font(19), fill=MUT)
    return im, d

def box(d, xy, fill, text=None, f=None, tc=BG, r=12, outline=None, center=True):
    d.rounded_rectangle(xy, r, fill=fill, outline=outline, width=2)
    if text:
        f = f or font(18, True)
        x0, y0, x1, y1 = xy
        lines = text.split('\n')
        lh = f.size + 6
        ty = (y0 + y1) / 2 - lh * len(lines) / 2 + 2
        for ln in lines:
            tw = d.textlength(ln, font=f)
            d.text(((x0 + x1) / 2 - tw / 2 if center else x0 + 14, ty), ln, font=f, fill=tc)
            ty += lh

def arrow(d, a, b, col=MUT, w=3):
    d.line([a, b], fill=col, width=w)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = 12
    p1 = (b[0] - L * math.cos(ang - 0.45), b[1] - L * math.sin(ang - 0.45))
    p2 = (b[0] - L * math.cos(ang + 0.45), b[1] - L * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=col)

def save(im, name):
    im.save(f'{OUT}/{name}', quality=90); print('saved', name, im.size)

# ---------- Ch1: bundle byte map ----------
def bundle_map():
    W, H = 1600, 700
    im, d = canvas(W, H, 'One 1,251,728-byte script: what sits where', 'hoisted.CUO_IjfL.js, measured byte offsets from parsing the shipped file (chapter 1)')
    total = 1251728
    segs = [(0, 532149, 'three.js r158 core', C['grey']), (532149, 565000, 'Engine base', C['blue']),
            (565000, 634675, 'Input, scroll, FBO, Stage3D, ScreenPaint', C['teal']), (634675, 704000, 'SplitType + Vimeo', C['violet']),
            (704000, 1106805, 'Pages, sections, scenes', C['amber']), (1106805, 1114000, 'day.js', C['violet']),
            (1114000, 1206033, 'Scroll + post stack + loaders', C['pink']), (1206033, 1230000, 'fflate + EXRLoader', C['violet']),
            (1230000, total, 'App, Preloader, UI, preRun/run', C['green'])]
    x0, x1, y0, y1 = 60, W - 60, 170, 290
    sx = lambda b: x0 + (x1 - x0) * b / total
    for a, b, label, col in segs:
        d.rectangle([sx(a), y0, sx(b) - 2, y1], fill=col)
    # tick marks
    for kb in range(0, 1300, 100):
        x = sx(kb * 1000)
        if x > x1: break
        d.line([x, y1 + 4, x, y1 + 14], fill=MUT, width=2)
        d.text((x - 14, y1 + 18), f'{kb}k', font=font(14, mono=True), fill=MUT)
    # legend with offsets
    ly = 360
    for i, (a, b, label, col) in enumerate(segs):
        cx = 60 + (i % 3) * 510; cy = ly + (i // 3) * 92
        d.rounded_rectangle([cx, cy, cx + 28, cy + 28], 6, fill=col)
        d.text((cx + 42, cy - 2), label, font=font(20, True), fill=FG)
        d.text((cx + 42, cy + 28), f'{a:,} to {b:,}  ({(b - a) / 1000:.0f} KB)', font=font(15, mono=True), fill=MUT)
    d.text((60, H - 50), 'Grey = three.js, purple = other libraries, colours = Lusion\'s own code. Segment boundaries between 565k and 704k are rounded.', font=font(16), fill=MUT)
    save(im, 'c1_bundle_map.png')

# ---------- Ch1: network waterfall (DevTools-style) ----------
def waterfall():
    rep = json.load(open('runtime/home_report.json'))
    res = [r for r in rep['perf']['res'] if r['st'] < 4200]
    res.sort(key=lambda r: r['st'])
    res = res[:26]
    W = 1600; rowh = 30; H = 200 + rowh * len(res) + 70
    im, d = canvas(W, H, 'Network waterfall: the first seconds of lusion.co', 'Resource timing from the headless probe (1440x900). Bars = start and duration, ms after navigation start.')
    cols = {'script': C['amber'], 'link': C['violet'], 'css': C['teal'], 'img': C['blue'], 'xmlhttprequest': C['pink'], 'fetch': C['grey'], 'video': C['green'], 'iframe': C['grey']}
    t0, t1 = 1400, 4300
    gx0, gx1 = 760, W - 60
    tx = lambda t: gx0 + (gx1 - gx0) * (t - t0) / (t1 - t0)
    top = 150
    d.text((60, top - 30), 'Resource', font=font(16, True), fill=MUT)
    d.text((560, top - 30), 'Type', font=font(16, True), fill=MUT)
    d.text((660, top - 30), 'Size', font=font(16, True), fill=MUT)
    for t in range(1500, 4301, 500):
        x = tx(t); d.line([x, top - 6, x, top + rowh * len(res)], fill=GRID, width=1)
        d.text((x - 20, top - 30), f'{t}ms', font=font(14, mono=True), fill=MUT)
    for i, r in enumerate(res):
        y = top + i * rowh
        if i % 2 == 0: d.rectangle([50, y, W - 50, y + rowh - 2], fill=(20, 23, 31))
        name = r['n'].split('?')[0].replace('https://', '')
        name = name if len(name) < 52 else '...' + name[-49:]
        d.text((60, y + 6), name, font=font(14, mono=True), fill=FG)
        d.text((560, y + 6), r['it'][:9], font=font(14, mono=True), fill=MUT)
        sz = r['dec']; d.text((660, y + 6), (f'{sz / 1000:.0f} KB' if sz else '-'), font=font(14, mono=True), fill=MUT)
        col = cols.get(r['it'], C['grey'])
        a = tx(r['st']); b = max(a + 4, tx(r['st'] + r['dur']))
        d.rounded_rectangle([a, y + 7, b, y + rowh - 9], 4, fill=col)
    ly = top + rowh * len(res) + 22
    x = 60
    for k, lab in [('script', 'JS bundle'), ('link', 'stylesheet'), ('css', 'fonts/icons from CSS'), ('xmlhttprequest', 'XHR (audio, Vimeo, meshes)'), ('img', 'textures/images')]:
        d.rounded_rectangle([x, ly, x + 22, ly + 18], 4, fill=cols[k]); d.text((x + 30, ly - 2), lab, font=font(16), fill=FG); x += d.textlength(lab, font=font(16)) + 80
    save(im, 'c1_network_waterfall.png')

# ---------- Ch2: boot timeline with preloader thumbnails ----------
def boot_timeline():
    W, H = 1600, 760
    im, d = canvas(W, H, 'Boot, step by step: from HTML to the first frame', 'Order is from the code (preRun module). Screens are real captures of the preloader and the loaded hero.')
    steps = [('HTML', '#preloader shown\n#canvas empty', C['grey']), ('preRun()', 'router + font loader\nAeonik:400', C['blue']),
             ('run()', 'initEngine + preInit\nstart rAF loop', C['teal']), ('ui.preload', 'assets + shader\nwarm-up = %', C['amber']),
             ('init()', 'pages build sections,\nStage3D, Ufx meshes', C['violet']), ('start()', 'scroll on, preloader\nfades, loop runs', C['green'])]
    n = len(steps); x0 = 60; bw = (W - 120 - (n - 1) * 24) / n; y = 150
    for i, (t, s, col) in enumerate(steps):
        bx = x0 + i * (bw + 24)
        box(d, [bx, y, bx + bw, y + 64], col, t, font(22, True))
        d.multiline_text((bx + 6, y + 78), s, font=font(17), fill=FG, spacing=6)
        if i < n - 1: arrow(d, (bx + bw + 2, y + 32), (bx + bw + 22, y + 32))
    thumbs = [('runtime/v/preloader_1200.png', '~1.2 s: preloader'), ('runtime/v/preloader_4000.png', '~4 s: still loading'), ('runtime/v/hero_both.png', 'after start(): hero')]
    tw = 460; th = int(tw * 900 / 1440); ty = 340
    for i, (p, cap) in enumerate(thumbs):
        if not os.path.exists(p): continue
        t = Image.open(p).convert('RGB').resize((tw, th))
        tx = 60 + i * (tw + 50)
        im.paste(t, (tx, ty)); d.rectangle([tx - 1, ty - 1, tx + tw, ty + th], outline=GRID, width=2)
        d.text((tx, ty + th + 12), cap, font=font(18, True), fill=FG)
    save(im, 'c2_boot_timeline.png')

# ---------- Ch2: one frame, update order ----------
def frame_order():
    W, H = 1600, 640
    im, d = canvas(W, H, 'Inside one frame: the fixed update order', 'loop() caps dt at 1/20 s (50 ms), runs Tween.autoUpdate(dt), then update(dt) calls these in order. Widths show order, not measured time.')
    calls = [('taskManager\n.update', C['grey']), ('properties\n.reset', C['grey']), ('app\n.preUpdate', C['blue']), ('input\n.update', C['teal']),
             ('scrollManager\n.update', C['teal']), ('pagesManager\n.update', C['amber']), ('ui\n.update', C['amber']), ('app.update\n(visuals + post)', C['pink']), ('input\n.postUpdate', C['teal'])]
    x = 60; y = 170; w = (W - 120) / len(calls)
    for i, (t, col) in enumerate(calls):
        box(d, [x + i * w + 3, y, x + (i + 1) * w - 3, y + 110], col, t, font(16, True))
        d.text((x + i * w + 8, y - 28), str(i + 1), font=font(18, True, mono=True), fill=MUT)
    notes = [(1, 'GPU warm-up: compile a shader or upload a texture, a slice per frame'),
             (4, 'raw wheel/touch/mouse -> smoothed deltas'),
             (5, 'virtual scroll eases; every ScrollDomRange gets 0..1 progress'),
             (6, 'active page + sections write into properties and Stage3D uniforms'),
             (8, 'Visuals copies the stage look into the post stack, then postprocessing.render(scene, camera)')]
    ny = 330
    for idx, txt in notes:
        cx = x + (idx - 0.5) * w
        d.line([cx, y + 112, cx, ny + 10], fill=GRID, width=2)
        d.ellipse([cx - 6, ny + 4, cx + 6, ny + 16], fill=MUT)
        d.text((80, ny), f'{idx}.', font=font(18, True, mono=True), fill=FG)
        d.text((130, ny), txt, font=font(18), fill=FG)
        ny += 50
    save(im, 'c2_frame_order.png')

# ---------- Ch2: DPR + pixel cap ----------
def pixel_cap():
    W, H = 1600, 720
    im, d = canvas(W, H, 'Why heavy shaders stay smooth: DPR and pixel caps', 'Settings: DPR = min(1.5, devicePixelRatio); MAX_PIXEL_COUNT = 2560 x 1440. FSR then upscales to the canvas (chapter 3).')
    s = 0.15; ox, oy = 80, 170
    rects = [(5120, 2880, '5K screen at DPR 2: 14.7 MP', C['grey']), (3840, 2160, '4K: 8.3 MP', C['violet']), (2560, 1440, 'Lusion cap: 3.7 MP rendered', C['teal'])]
    for w, h, lab, col in rects:
        d.rectangle([ox, oy, ox + w * s, oy + h * s], outline=col, width=4)
        d.text((ox + w * s - d.textlength(lab, font=font(18, True)) - 10, oy + h * s - 30), lab, font=font(18, True), fill=col)
    d.rectangle([ox, oy, ox + 2560 * s, oy + 1440 * s], fill=(30, 70, 66))
    d.text((ox + 14, oy + 14), 'drawn by the GPU', font=font(18, True), fill=FG)
    tx = ox + 5120 * s + 50
    for i, line in enumerate(['A 5K display at DPR 2 asks for 14.7', 'million pixels per pass. Lusion renders', 'at most 3.7 million, about 4x fewer,', 'then upscales and sharpens with FSR.', '', 'Every full-screen pass (bloom, grade,', 'distortion, SMAA) pays this cost, so', 'the cap multiplies across the chain.']):
        d.text((tx, oy + 10 + i * 34), line, font=font(20), fill=FG)
    save(im, 'c2_pixel_cap.png')

# ---------- Ch3: ping-pong ----------
def ping_pong():
    W, H = 1600, 760
    im, d = canvas(W, H, 'Ping-pong render targets: how passes hand off', 'Scene renders once into sceneRenderTarget, is copied into "from", then each pass reads "from", writes "to", and the two swap.')
    y = 190
    box(d, [60, y, 300, y + 90], C['grey'], 'scene + camera', font(20, True))
    arrow(d, (300, y + 45), (350, y + 45))
    box(d, [350, y, 610, y + 90], C['blue'], 'sceneRenderTarget', font(19, True))
    arrow(d, (610, y + 45), (660, y + 45))
    d.text((620, y - 30), 'fboHelper.copy', font=font(16, mono=True), fill=MUT)
    passes = [('Bloom 10', C['amber']), ('Final 30', C['pink']), ('PreUfx 50', C['violet']), ('Distort 75', C['teal']), ('PostUfx 100', C['violet']), ('SMAA 500', C['green']), ('FSR 2000', C['green'])]
    x = 660; py = y + 200
    box(d, [660, y, 900, y + 90], (60, 66, 82), 'from (read)', font(19, True), tc=FG)
    box(d, [660, y + 320, 900, y + 410], (60, 66, 82), 'to (write)', font(19, True), tc=FG)
    pw = 88; gap = 8; sx = 930
    for i, (t, col) in enumerate(passes):
        bx = sx + i * (pw + gap)
        box(d, [bx, py - 40, bx + pw, py + 40], col, t.replace(' ', '\n'), font(15, True))
        if i % 2 == 0:
            arrow(d, (bx + pw / 2, y + 90), (bx + pw / 2, py - 42), C['blue'], 2); arrow(d, (bx + pw / 2, py + 40), (bx + pw / 2, y + 318), C['pink'], 2)
        else:
            arrow(d, (bx + pw / 2, y + 320), (bx + pw / 2, py + 42), C['blue'], 2); arrow(d, (bx + pw / 2, py - 40), (bx + pw / 2, y + 92), C['pink'], 2)
    d.line([900, y + 45, sx + 7 * (pw + gap), y + 45], fill=GRID, width=2)
    d.line([900, y + 365, sx + 7 * (pw + gap), y + 365], fill=GRID, width=2)
    ex = sx + 7 * (pw + gap) + 10
    box(d, [ex, py - 40, ex + 130, py + 40], FG, 'Screen', font(20, True))
    arrow(d, (ex - 12, py), (ex - 2, py), FG)
    ny = y + 450
    for i, line in enumerate(['Blue arrows = read, pink arrows = write. After each pass the roles swap, so no pass reads and writes the same texture.',
                              'Only passes with enabled && needsRender() run; the last one in the sorted queue draws straight to the screen (toScreen = true).',
                              'Measured on the home page: 22 framebuffers created, about 14 to 16 draw calls per frame.']):
        d.text((60, ny + i * 36), line, font=font(19), fill=FG)
    save(im, 'c3_ping_pong.png')

# ---------- Ch4: coordinate mapping ----------
def dom_to_gl():
    W, H = 1600, 780
    im, d = canvas(W, H, 'From a DOM rect to a GPU quad (ufxVert chunk)', 'getBasePosition() scales a unit quad to u_domWH around u_domPivot; getScreenPosition() adds u_domXY and flips Y.')
    # left: DOM space
    lx, ly, lw, lh = 60, 170, 680, 480
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=GRID, width=2)
    d.text((lx, ly - 30), 'DOM / CSS pixels: origin top-left, Y grows down', font=font(18, True), fill=FG)
    arrow(d, (lx + 10, ly + 10), (lx + 140, ly + 10), C['amber']); d.text((lx + 146, ly), 'x', font=font(18, True), fill=C['amber'])
    arrow(d, (lx + 10, ly + 10), (lx + 10, ly + 140), C['amber']); d.text((lx + 18, ly + 140), 'y', font=font(18, True), fill=C['amber'])
    ex, ey, ew, eh = lx + 220, ly + 170, 300, 190
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(34, 52, 90), outline=C['blue'], width=3)
    d.text((ex + 14, ey + 14), '.project-item-main', font=font(17, mono=True), fill=FG)
    d.line([lx + 10, ey, ex, ey], fill=C['teal'], width=2); d.line([ex, ly + 10, ex, ey], fill=C['teal'], width=2)
    d.text((ex + 8, ly + 60), 'u_domXY = rect.left, rect.top', font=font(16, mono=True), fill=C['teal'])
    d.text((ex + 10, ey + eh + 10), 'u_domWH = width, height', font=font(16, mono=True), fill=C['teal'])
    pvx, pvy = ex + ew / 2, ey + eh / 2
    d.ellipse([pvx - 7, pvy - 7, pvx + 7, pvy + 7], fill=C['pink']); d.text((pvx + 12, pvy - 10), 'u_domPivot', font=font(16, mono=True), fill=C['pink'])
    d.rectangle([ex - 26, ey - 18, ex + ew + 26, ey + eh + 18], outline=C['violet'], width=2)
    d.text((ex - 26, ey + eh + 42), 'u_domPadding grows the quad (1000 px on one side for project items)', font=font(15), fill=C['violet'])
    # arrow middle
    arrow(d, (lx + lw + 20, ly + lh / 2), (lx + lw + 120, ly + lh / 2), FG, 4)
    d.text((lx + lw + 18, ly + lh / 2 + 14), '* (1,-1,1)', font=font(16, mono=True), fill=FG)
    # right: GL
    rx, ry, rw, rh = 880, 170, 660, 480
    d.rectangle([rx, ry, rx + rw, ry + rh], outline=GRID, width=2)
    d.text((rx, ry - 30), 'Ortho camera space: Y grows up', font=font(18, True), fill=FG)
    arrow(d, (rx + 10, ry + rh - 10), (rx + 140, ry + rh - 10), C['amber']); d.text((rx + 146, ry + rh - 22), 'x', font=font(18, True), fill=C['amber'])
    arrow(d, (rx + 10, ry + rh - 10), (rx + 10, ry + rh - 140), C['amber']); d.text((rx + 18, ry + rh - 160), 'y', font=font(18, True), fill=C['amber'])
    qx, qy = rx + 200, ry + 130
    d.polygon([(qx, qy + 30), (qx + 300, qy), (qx + 320, qy + 190), (qx + 20, qy + 220)], fill=(30, 80, 72), outline=C['teal'])
    d.text((qx + 40, qy + 90), 'quad, same rect,\nnow shader-driven', font=font(17, True), fill=FG)
    d.text((rx + 20, ry + rh + 14), 'u_quaternion + u_scale can rotate/scale it; padUv() keeps the texture aligned.', font=font(16), fill=MUT)
    d.text((60, H - 60), 'Scroll is virtual, so the rect comes from layout plus the engine\'s own scroll offset: no drift between text and pixels.', font=font(18), fill=FG)
    save(im, 'c4_dom_to_gl.png')

if __name__ == '__main__':
    bundle_map(); waterfall(); frame_order(); pixel_cap(); ping_pong(); dom_to_gl()
    if os.path.exists('runtime/v/preloader_4000.png'): boot_timeline()
