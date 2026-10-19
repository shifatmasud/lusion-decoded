# Pass-by-pass view of one captured frame of lusion.co (headless, software WebGL, 1280x800).
from PIL import Image, ImageDraw
from strips import font
V = 'runtime/vis/'

def enh(im, gain, center):
    return Image.eval(im, lambda v: max(0, min(255, int((v - center) * gain + center if center else v * gain))))

panels = [
    ('pass_00.jpg', 'Draw 1 of 34 | ScreenPaint | 320x200', 'pointer velocity field (contrast x8)', lambda im: enh(im, 8, 127)),
    ('pass_03.jpg', 'Draw 5 | copy of the 3D scene | 1280x800', 'the balloons, rendered off-screen', None),
    ('pass_05.jpg', 'Draws 7-24 | blur pyramid | 640 to 80 px', 'two runs of H+V blur per level (320x200 shown)', None),
    ('pass_07.jpg', 'Draw 27 | frame background (frameBgFrag)', 'rounded-corner mask: u_domWH, u_globalRadius', None),
    ('pass_08.jpg', 'Draw 29 | ScreenPaintDistortion (order 75)', 'reads the paint field; rgbShift, blue noise', None),
    ('pass_09.jpg', 'Draw 32 | SMAA 1: edge detection', 'edges found in the frame (contrast x4)', lambda im: enh(im, 4, 0)),
    ('pass_10.jpg', 'Draw 33 | SMAA 2: blend weights', 'per-pixel weights from area/search LUTs (x30)', lambda im: enh(im, 30, 0)),
    ('pass_11.jpg', 'Draw 34 | SMAA 3: resolve to screen', 'the only draw into the default framebuffer', None),
]
tw, th, pad, head, lab = 520, 325, 24, 110, 62
cols = 4
W = pad + cols * (tw + pad); H = head + 2 * (th + lab + pad)
c = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(c)
d.text((pad, 18), 'Chapter 8: one real frame of lusion.co, pass by pass', fill='#111', font=font(28, True))
d.text((pad, 58), 'Captured by hooking WebGL drawArrays and reading each full-screen pass back (first occurrence of each program and size). 34 full-screen draws in this frame.', fill='#555', font=font(17))
d.text((pad, 82), 'Hero section, mouse still. No bloom or colour-grading program ran in this frame.', fill='#555', font=font(17))
for i, (f, t1, t2, fx) in enumerate(panels):
    r, k = divmod(i, cols)
    x = pad + k * (tw + pad); y = head + r * (th + lab + pad)
    im = Image.open(V + f).convert('RGB')
    if fx: im = fx(im)
    im = im.resize((tw, th), Image.NEAREST if im.width < 400 else Image.LANCZOS)
    c.paste(im, (x, y)); d.rectangle([x, y, x + tw - 1, y + th - 1], outline='#bbb')
    d.ellipse([x + 8, y + 8, x + 40, y + 40], fill='#e4572e')
    d.text((x + 24, y + 24), str(i + 1), fill='white', font=font(18, True), anchor='mm')
    d.text((x, y + th + 8), t1, fill='#111', font=font(17, True))
    d.text((x, y + th + 32), t2, fill='#444', font=font(16))
    if k < cols - 1:
        d.polygon([(x + tw + 6, y + th // 2 - 8), (x + tw + 18, y + th // 2), (x + tw + 6, y + th // 2 + 8)], fill='#e4572e')
c.save('img/c8_passes.jpg', quality=88)
print(c.size)
