# Filmstrips and annotated composites from real captures of lusion.co.
import sys
from PIL import Image, ImageDraw, ImageFont

def font(sz, bold=False):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()

def strip(paths, labels, title, out, cols=None, thumb_w=520, sub=None):
    ims = [Image.open(p).convert('RGB') for p in paths]
    cols = cols or len(ims)
    rows = (len(ims) + cols - 1) // cols
    th = int(thumb_w * ims[0].height / ims[0].width)
    pad, head, lab = 24, 70 if not sub else 100, 44
    W = pad + cols * (thumb_w + pad)
    H = head + rows * (th + lab + pad) + pad // 2
    canvas = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(canvas)
    d.text((pad, 20), title, fill='#111', font=font(28, True))
    if sub:
        d.text((pad, 60), sub, fill='#555', font=font(18))
    for i, (im, l) in enumerate(zip(ims, labels)):
        r, c = divmod(i, cols)
        x = pad + c * (thumb_w + pad); y = head + r * (th + lab + pad)
        canvas.paste(im.resize((thumb_w, th), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + thumb_w - 1, y + th - 1], outline='#ccc')
        d.ellipse([x + 8, y + 8, x + 40, y + 40], fill='#e4572e')
        d.text((x + 24, y + 24), str(i + 1), fill='white', font=font(18, True), anchor='mm')
        d.text((x, y + th + 10), l, fill='#222', font=font(18))
    canvas.save(out, quality=88)
    print(out, canvas.size)

if __name__ == '__main__':
    which = sys.argv[1]
    R = 'runtime/'
    if which == 'c5':
        strip([R + 'home_0_loaded.png', R + 'home_2_scroll.png', R + 'home_4_scroll.png', R + 'home_6_scroll.png', R + 'home_8_scroll.png', R + 'home_10_scroll.png'],
              ['Loaded, scroll 0', 'After 2 wheel ticks', 'After 4 ticks', 'After 6 ticks', 'After 8 ticks', 'After 10 ticks'],
              'Chapter 5: the virtual scroll on the live home page', 'img/c5_scroll_strip.jpg', cols=3, thumb_w=560,
              sub='Headless capture, 1440 x 900. Each tick: one wheel event, deltaY 650, which Input clamps to 200 px; then 1.2 s to settle. window.scrollY stayed 0 throughout.')
    if which == 'c6':
        strip([R + 'vis/tr_0.png', R + 'vis/tr_1.png', R + 'vis/tr_2.png', R + 'vis/tr_5.png'],
              ['Home, after hovering the About link', 'Hide: the old page pulls away', 'Covered: overlay with the logo mark', 'LOADING text while /about assets load'],
              'Chapter 6: a real page transition, home to /about', 'img/c6_transition_strip.jpg', cols=2, thumb_w=640,
              sub='Headless capture at 1280 x 800 with software WebGL, so each step is slower than on a real GPU. The URL had already changed to /about by frame 1.')
    if which == 'c7':
        strip([R + 'vis/t_trail1.png', R + 'vis/t_trail2.png'],
              ['Pointer sweeping left to right across the hero', 'Sweeping back right to left'],
              'Chapter 7: the live hero while the pointer moves', 'img/c7_hero_sweep.jpg', cols=2, thumb_w=720,
              sub='Headless capture, 1280 x 800, software WebGL: 31 mouse moves per sweep, screenshot at the end of each sweep.')
    if which == 'c9':
        strip([R + 'vis/load_0.png', R + 'vis/load_1.png', R + 'vis/load_3.png', R + 'vis/load_5.png', R + 'vis/load_6.png', R + 'vis/load_9.png'],
              ['First frame: counter starts', '+2 s: counter climbing', '+5 s: still loading', '+8 s: nearly done', '+9 s: counter at 100', 'Later: preloader gone, hero live'],
              'Chapter 9: the preloader on the live site', 'img/c9_preloader_strip.jpg', cols=3, thumb_w=560,
              sub='Headless capture, 1440 x 900, software WebGL, screenshots after DOMContentLoaded. Times are seconds after the first frame; software rendering makes the end slower than on a real GPU.')
