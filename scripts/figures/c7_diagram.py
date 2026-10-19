# Annotated concept diagram: how the mouse ray pushes balloons (constants from 023_HomeBalloonsPhysics.js).
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13, 6.5))
ax.set_aspect('equal'); ax.axis('off')
cam = np.array([-6.0, 0.4]); tgt = np.array([5.5, -0.9])
d = (tgt - cam) / np.linalg.norm(tgt - cam)
ax.add_patch(plt.Polygon([cam + [0, 0.35], cam + [0, -0.35], cam + [-0.6, 0]], color='#333'))
ax.text(cam[0] - 0.3, cam[1] + 0.6, 'camera', ha='center', fontsize=11)
ax.annotate('', xy=tgt, xytext=cam, arrowprops=dict(arrowstyle='->', color='#e4572e', lw=2.2))
ax.text(-3.6, 0.55, 'mouse ray: input.mouseXY unprojected\nthrough properties.camera', color='#e4572e', fontsize=10.5)
# influence band around the ray
n = np.array([-d[1], d[0]])
w = 0.55
band = [cam + n * w, tgt + n * w, tgt - n * w, cam - n * w]
ax.add_patch(plt.Polygon(band, color='#e4572e', alpha=0.08))
ax.text(4.2, -2.25, 'hit zone: distance to ray < radius + MOUSE_RADIUS (0.025)', fontsize=10, color='#b23a1a', ha='center')
balls = [((-1.2, 0.9), 0.75, False), ((0.4, -0.35), 0.8, True), ((2.0, 1.35), 0.6, False), ((1.6, -1.6), 0.55, False),
         ((3.3, -0.2), 0.65, True), ((-0.2, -2.1), 0.7, False), ((-2.4, -1.2), 0.5, False), ((0.9, 2.6), 0.5, False)]
for (x, y), r, hit in balls:
    p = np.array([x, y])
    ax.add_patch(Circle(p, r, color='#2e86ab' if not hit else '#f2a541', alpha=0.85, ec='#1b4f66' if not hit else '#a8641a', lw=1.5))
    g = -p / np.linalg.norm(p) * 0.45
    ax.add_patch(FancyArrowPatch(p + g * 0.2 / 0.45 * 0 + (-p / np.linalg.norm(p)) * r, p + (-p / np.linalg.norm(p)) * r + g, arrowstyle='->', color='#555', mutation_scale=12, lw=1))
    if hit:
        side = np.sign(np.dot(p - cam, n)) or 1
        push = n * side * 1.1 + d * 0.5
        ax.add_patch(FancyArrowPatch(p, p + push, arrowstyle='-|>', color='#b23a1a', mutation_scale=18, lw=2.2))
ax.plot(0, 0, marker='+', color='#111', ms=14, mew=2)
ax.text(0.15, 0.12, 'origin', fontsize=9)
ax.text(-6.4, -3.25, 'Grey arrows: "gravity" pulls every balloon toward the origin, GRAVITY_FACTOR = 40, weaker while touching (1 / (1 + frictionTot)).\n'
        'Red arrows: balloons in the hit zone are pushed sideways off the ray and pick up the pointer\'s velocity (MOUSE_PUSH_FORCE 0.12, MOUSE_INFLUENCE 0.1).\n'
        'Also each frame: every pair is tested (overlap split half and half, elastic bounce), a swirl around (1,1,1), then pos += vel*dt and vel *= 0.2^dt.',
        fontsize=10, va='top', color='#333')
ax.set_xlim(-7, 7); ax.set_ylim(-4.3, 3.4)
ax.set_title('How the pointer moves the hero balloons (side view, concept diagram)', fontsize=14, loc='left')
fig.tight_layout(); fig.savefig('img/c7_mouse_ray.png', dpi=110)
