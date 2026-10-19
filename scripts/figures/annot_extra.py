# Numbered callouts for frames captured by capd_wheel.mjs / capm_drag.mjs (boxes from their logged rects or computed from CSS/JS)
from PIL import Image, ImageDraw, ImageFont
import os
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PINK = (255, 46, 136)

def annot(src, dst, boxes, scale_to=None):
    im = Image.open(src).convert('RGB')
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(F, 18 if im.width > 600 else 13)
    for n, (x, y, w, h, dashed) in enumerate(boxes, 1):
        y0, y1 = max(0, y), min(im.height - 1, y + h)
        if y1 <= y0:
            continue
        if dashed:
            for xx in range(x, x + w, 14):
                d.line([(xx, y0), (min(xx + 7, x + w), y0)], fill=PINK, width=3)
                d.line([(xx, y1), (min(xx + 7, x + w), y1)], fill=PINK, width=3)
            for yy in range(y0, y1, 14):
                d.line([(x, yy), (x, min(yy + 7, y1))], fill=PINK, width=3)
                d.line([(x + w, yy), (x + w, min(yy + 7, y1))], fill=PINK, width=3)
        else:
            d.rectangle([x, y0, x + w, y1], outline=PINK, width=3)
        r = 15 if im.width > 600 else 11
        cx, cy = x + r + 4, y0 + r + 4
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PINK, outline='white', width=2)
        t = str(n)
        tw = d.textlength(t, font=font)
        d.text((cx - tw / 2, cy - (10 if r == 15 else 7)), t, fill='white', font=font)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, quality=86)

R = 'raw/p15_oryzo'
O = 'img/p15_oryzo/extra'
# desktop 1440x900: rail wrapper measured top 145 h 638; overscroll/preview zone = last 25% of viewport (overScrollSize = vw*0.25, code)
for f in ['01', '03']:
    annot(f'{R}/desktop_wheel/{f}.png', f'{O}/desktop_rail_{f}.jpg', [(0, 145, 1440, 638, False)])
annot(f'{R}/desktop_wheel/04.png', f'{O}/desktop_rail_04.jpg', [(0, 145, 1080, 638, False), (1080, 8, 352, 884, True)])
annot(f'{R}/desktop_wheel/06.png', f'{O}/desktop_next_06.jpg', [(72, 260, 544, 380, False), (0, 145, 1440, 638, True)])
# mobile 390x844: rects logged by capm_drag.mjs (meta, first media item); x = base-padding-x 15px
mob = {'00': [(15, 15, 360, 970, False)], '01': [(15, -449, 360, 970, False), (15, 645, 360, 207, False)],
       '02': [(15, 181, 360, 207, False)], '05': [(15, -1212 + 1600, 360, 0, False)]}
annot(f'{R}/mobile_drag/01.png', f'{O}/mobile_drag_01.jpg', mob['01'])
annot(f'{R}/mobile_drag/02.png', f'{O}/mobile_drag_02.jpg', mob['02'])
annot(f'{R}/mobile_drag/04.png', f'{O}/mobile_drag_04.jpg', [])
print('ok')
