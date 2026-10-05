# -*- coding: utf-8 -*-
"""fitcheck.py — report any Lecture 01 panel whose content leaves the axes.

dsl.save() writes with bbox_inches="tight", so content drawn outside the axes
is not clipped: the figure silently grows instead, which is what makes a card
look "cut off" when it is placed on a slide. This measures every artist's
bounding box in data coordinates and flags anything outside (0..100, 0..H).
"""
import sys
import _boot
import dsl
import matplotlib.pyplot as plt

TOL = 0.6          # units of slack; anti-aliasing and line width need a little
_flags = []
_real_save = dsl.save


def _checked_save(f, name):
    if name in SKIP:
        return _real_save(f, name)
    ax = f.axes[0]
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    r = f.canvas.get_renderer()
    inv = ax.transData.inverted()
    worst_v = None
    worst_h = None
    for art in ax.get_children():
        if not art.get_visible():
            continue
        try:
            bb = art.get_window_extent(renderer=r)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        (dx0, dy0) = inv.transform((bb.x0, bb.y0))
        (dx1, dy1) = inv.transform((bb.x1, bb.y1))
        txt = (getattr(art, "get_text", lambda: "")() or
               type(art).__name__)[:44]
        ov = max(y0 - dy0, dy1 - y1)
        oh = max(x0 - dx0, dx1 - x1)
        if ov > TOL and (worst_v is None or ov > worst_v[0]):
            worst_v = (ov, txt)
        if oh > 2.0 and (worst_h is None or oh > worst_h[0]):
            worst_h = (oh, txt)
    if worst_v or worst_h:
        _flags.append((name, worst_v, worst_h))
    return _real_save(f, name)


dsl.save = _checked_save
import l1_kit
l1_kit.save = _checked_save

SKIP = {"moore_plot"}
MODULES = sys.argv[1:] or ["l1_front", "l1_why", "l1_flow", "l1_steps", "l1_lab"]
for m in MODULES:
    try:
        mod = __import__(m)
    except ImportError:
        continue
    mod.save = _checked_save
    for fn in getattr(mod, "ORDER", []):
        getattr(mod, fn)()
    else:
        if not hasattr(mod, "ORDER"):
            for nm in dir(mod):
                o = getattr(mod, nm)
                if callable(o) and not nm.startswith("_") and o.__module__ == m:
                    try:
                        o()
                    except TypeError:
                        pass
    plt.close("all")

print()
nv = 0
for name, wv, wh in _flags:
    if wv:
        nv += 1
        print("VERTICAL   %-26s %6.2f units   %s" % (name, wv[0], wv[1]))
    if wh:
        print("  (wide)   %-26s %6.2f units   %s" % (name, wh[0], wh[1]))
print()
print("panels with VERTICAL overflow:", nv)
