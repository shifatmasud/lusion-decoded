# Charts for chapters 5 and 9, computed from the quoted Lusion code and the runtime probe report.
import json, math, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = 'img/'
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'axes.facecolor': '#fafafa'})

# ---------- Chapter 5: motion curves ----------
fig, ax = plt.subplots(1, 3, figsize=(16, 4.8))
# (a) wheel ease: frame-rate independent exponential ease, k = 12
for fps, c in [(30, '#e4572e'), (60, '#2e86ab'), (144, '#76b041')]:
    dt = 1 / fps; s = 0.0; t = 0.0; T = [0]; S = [0]
    while t < 0.6:
        s += (650 - s) * (1 - math.exp(-12 * dt)); t += dt; T.append(t); S.append(s)
    ax[0].plot(T, S, color=c, lw=2, label=f'{fps} fps', drawstyle='steps-post' if fps == 30 else 'default')
# naive lerp(0.1) per frame for contrast
for fps, c in [(30, '#e4572e'), (144, '#76b041')]:
    s = 0.0; T = [0]; S = [0]; t = 0
    while t < 0.6:
        s += (650 - s) * 0.1; t += 1 / fps; T.append(t); S.append(s)
    ax[0].plot(T, S, color=c, lw=1.2, ls='--')
ax[0].set_title('Wheel: 1 - exp(-12 dt) ease (solid)\nvs naive lerp 0.1 per frame (dashed)')
ax[0].set_xlabel('seconds after one wheel tick'); ax[0].set_ylabel('scrollPixel (target 650)')
ax[0].legend(frameon=False)
# (b) fling after finger release, speed-dependent friction 2.1 -> 1.9
view = 900
for v0, c in [(1500, '#2e86ab'), (6000, '#e4572e'), (12000, '#76b041')]:
    dt = 1 / 60; v = v0; x = 0; t = 0; T = [0]; X = [0]
    while t < 2.5:
        k = 2.1 + (1.9 - 2.1) * min(1, max(0, abs(v / view / 5)))
        v += -k * v * dt; x += v * dt; t += dt; T.append(t); X.append(x)
    ax[1].plot(T, X, color=c, lw=2, label=f'release at {v0} px/s')
ax[1].set_title('Drag release: velocity decays with friction\nmix(2.1, 1.9, |v| / viewSize / 5)')
ax[1].set_xlabel('seconds after release'); ax[1].set_ylabel('distance travelled (px)')
ax[1].legend(frameon=False)
# (c) SecondOrderDynamics step responses
def sod(f, z, r, dur=2.0, dt=1 / 120):
    w = 2 * math.pi * f; k1 = z / (math.pi * f); k2 = 1 / (w * w); k3 = r * z / w
    y = 0; yv = 0; xp = 0; T = []; Y = []; t = 0
    while t < dur:
        x = 1.0 if t > 0.1 else 0.0
        xd = (x - xp) / dt; xp = x
        k2s = max(k2, dt * dt / 2 + dt * k1 / 2, dt * k1)
        y += dt * yv; yv += dt * (x + k3 * xd - y - k1 * yv) / k2s
        T.append(t); Y.append(y); t += dt
    return T, Y
for (f, z, r), c, lab in [((1, 2.2, 0.7), '#2e86ab', 'f=1, z=2.2, r=0.7 (ProjectItem zoom)'),
                          ((2, 0.4, 2), '#e4572e', 'f=2, z=0.4, r=2 (overshoot)'),
                          ((2, 1, -1), '#76b041', 'f=2, z=1, r=-1 (anticipation)')]:
    T, Y = sod(f, z, r); ax[2].plot(T, Y, color=c, lw=2, label=lab)
ax[2].axhline(1, color='#999', lw=0.8, ls=':')
ax[2].set_title('SecondOrderDynamics: same target step,\nthree (f, z, r) settings')
ax[2].set_xlabel('seconds'); ax[2].set_ylabel('value (target jumps 0 to 1)')
ax[2].legend(frameon=False, fontsize=9)
fig.tight_layout(); fig.savefig(OUT + 'c5_motion_curves.png', dpi=110); plt.close(fig)

# ---------- Chapter 9: network assets ----------
rep = json.load(open('runtime/home_report.json'))
res = rep['perf']['res']
def kind(n):
    u = n.split('?')[0].lower()
    for ext, k in [('.buf', 'mesh (.buf)'), ('.ktx2', 'texture'), ('.webp', 'texture'), ('.png', 'texture'), ('.jpg', 'texture'), ('.exr', 'HDR'), ('.hdr', 'HDR'),
                   ('.woff', 'font'), ('.ttf', 'font'), ('.otf', 'font'), ('.js', 'script'), ('.css', 'css'), ('.mp4', 'video'), ('.webm', 'video'), ('.json', 'json'), ('.ogg', 'audio')]:
        if u.endswith(ext) or ext + '2' in u and ext == '.woff':
            return k
    if 'lusion.co' in u and (u.endswith('/') or '.' not in u.rsplit('/', 1)[-1]):
        return 'html'
    return 'other'
agg = collections.defaultdict(lambda: [0, 0])
lens = {}
for x in rep['responses']:
    lens[x['url']] = max(lens.get(x['url'], 0), x['len'])
own = [r for r in res if 'lusion.co' in r['n'] or 'lusion.dev' in r['n']]
seen = set()
for r in own:
    if r['n'] in seen: continue
    seen.add(r['n']); k = kind(r['n']); agg[k][0] += 1; agg[k][1] += max(lens.get(r['n'], 0), r['dec'])
colors = {'mesh (.buf)': '#e4572e', 'texture': '#2e86ab', 'HDR': '#7b2cbf', 'font': '#76b041', 'script': '#f2a541', 'css': '#999999', 'html': '#555555', 'video': '#d62828', 'json': '#00a6a6', 'audio': '#b5838d', 'other': '#cccccc'}
fig, ax = plt.subplots(1, 2, figsize=(16, 6.2), gridspec_kw={'width_ratios': [1, 2]})
ks = sorted(agg, key=lambda k: -agg[k][1])
ax[0].barh([f'{k} ({agg[k][0]})' for k in ks][::-1], [agg[k][1] / 1024 for k in ks][::-1], color=[colors.get(k, '#ccc') for k in ks][::-1])
ax[0].set_xlabel('KB (Content-Length, or decoded size when known)'); ax[0].set_title('Files from lusion.co + lusion.dev on first load,\nby type (count in brackets)')
# waterfall
own_sorted = sorted(own, key=lambda r: r['st'])
for i, r in enumerate(own_sorted):
    ax[1].barh(i, max(r['dur'], 8), left=r['st'], color=colors.get(kind(r['n']), '#ccc'), height=0.8)
ax[1].invert_yaxis(); ax[1].set_yticks([])
ax[1].set_xlabel('ms since navigation start'); ax[1].set_title(f'Waterfall: {len(own_sorted)} requests to lusion.co / lusion.dev, home page (one bar each)')
from matplotlib.patches import Patch
ax[1].legend(handles=[Patch(color=colors[k], label=k) for k in ks], frameon=False, loc='lower right')
fig.tight_layout(); fig.savefig(OUT + 'c9_network.png', dpi=110); plt.close(fig)
print({k: (v[0], round(v[1] / 1024)) for k, v in agg.items()}, len(res), len(own))
print(sorted([(kind(r['n']), r['n'].split('/')[-1][:40], max(lens.get(r['n'],0), r['dec'])) for r in own], key=lambda x: -x[2])[:12])
