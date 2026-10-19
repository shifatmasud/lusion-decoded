# Screenshot composites for chapters 1, 3, 4.
import json
from PIL import Image, ImageDraw
from diagrams_v import font, canvas, save, C, FG, MUT, GRID

def triptych(prefix, title, sub, labels, name, rects=None):
    tw = 760; th = int(tw * 900 / 1440); gap = 30
    W = 60 * 2 + tw * 3 + gap * 2; H = 160 + th + 120
    im, d = canvas(W, H, title, sub)
    for i, (suffix, lab, note) in enumerate(labels):
        src = Image.open(f'runtime/v/{prefix}_{suffix}.png').convert('RGB')
        if rects and suffix == 'both':
            dd = ImageDraw.Draw(src)
            for r in rects:
                dd.rectangle([r['x'], r['y'], r['x'] + r['w'], r['y'] + r['h']], outline=C['pink'], width=5)
                dd.rectangle([r['x'], r['y'] - 34, r['x'] + 300, r['y']], fill=C['pink'])
                dd.text((r['x'] + 8, r['y'] - 31), r['sel'] + ' -> UfxMesh', font=font(22, True, mono=True), fill=(14, 16, 22))
        t = src.resize((tw, th))
        x = 60 + i * (tw + gap); y = 150
        im.paste(t, (x, y)); d.rectangle([x - 1, y - 1, x + tw, y + th], outline=GRID, width=2)
        d.text((x, y + th + 14), lab, font=font(22, True), fill=FG)
        d.text((x, y + th + 48), note, font=font(17), fill=MUT)
    save(im, name)

triptych('hero', 'Two layers, one page: the live home hero', 'Captured from lusion.co at 1440x900. Left: #canvas hidden. Middle: #page-container and #header hidden. Right: both, as you see it.',
         [('dom', 'HTML layer only', 'Real text, links and layout; almost no pixels'), ('gl', 'WebGL #canvas only', 'Every 3D and image pixel comes from one canvas'), ('both', 'Composite (what you see)', 'Fixed canvas behind, fixed HTML on top')],
         'c1_live_layers.png')

rects = [r for r in json.load(open('runtime/v/rects.json')) if r['y'] < 900]
triptych('proj', 'Ufx on the live site: project cards are drawn by WebGL', 'Home page, featured projects. The .project-item-main elements hold the layout; their thumbnails are UfxMesh quads in the canvas.',
         [('dom', 'Canvas hidden', 'The cards keep their size but show no images'), ('gl', 'HTML hidden', 'The thumbnails are still there: they live on the GPU'), ('both', 'Composite + DOM rects (pink)', 'Each pink rect is the refDom a UfxMesh copies')],
         'c4_live_ufx_cards.png', rects)

# Ch3: canvas-only output crop
src = Image.open('runtime/v/hero_gl.png').convert('RGB')
im, d = canvas(1600, 1160, 'The output of the post chain', 'Home hero with the HTML layer hidden: everything here passed through Bloom, Final grade, distortion, SMAA and FSR before reaching the screen.')
im.paste(src.resize((1480, 925)), (60, 150)); d.rectangle([59, 149, 1540, 1075], outline=GRID, width=2)
d.text((60, 1092), 'Captured headless with SwiftShader, so colours and bloom can differ slightly from a real GPU.', font=font(17), fill=MUT)
save(im, 'c3_post_output.png')
