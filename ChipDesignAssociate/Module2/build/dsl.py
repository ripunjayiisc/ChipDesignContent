"""Shared drawing helpers + house palette for Module 2 Topic 3 diagrams."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Rectangle, Circle, Polygon,
                                FancyArrowPatch, Arc, Wedge)
from matplotlib.path import Path
import matplotlib.patches as mpatches
import os

# ----- house palette (extracted from Module 2 Topic 1 deck) -----
NAVY   = "#0E2A47"
TEAL   = "#1B9AAA"
ORANGE = "#E8A55C"
AMBER  = "#C77514"
GREEN  = "#2A9D5C"
SLATE  = "#5A6B7B"
BODY   = "#33414F"
INK    = "#1A2332"
RED    = "#D6224A"
VIOLET = "#7A4FBF"
LIGHT  = "#F4F8FB"
GRID   = "#D8DEE5"
WHITE  = "#FFFFFF"

OUT = os.environ.get("CDA_IMG_DIR",
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"))
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["savefig.facecolor"] = "white"


def fig(w, h):
    f, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.axis("off")
    ax.set_aspect("equal")
    return f, ax


def save(f, name):
    p = os.path.join(OUT, name + ".png")
    f.savefig(p, dpi=200, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(f)
    print("  wrote", name)
    return p


def title(ax, x, y, s, size=13, color=NAVY, weight="bold", ha="center", style="normal"):
    ax.text(x, y, s, ha=ha, va="center", fontsize=size, color=color,
            fontweight=weight, fontstyle=style)


def box(ax, x, y, w, h, fc=WHITE, ec=TEAL, lw=1.6, r=1.2, z=2):
    b = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(b)
    return b


def label_box(ax, x, y, w, h, text, fc=WHITE, ec=TEAL, tc=NAVY, size=10,
              lw=1.6, weight="bold", r=1.2, z=2):
    box(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, r=r, z=z)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=size, color=tc, fontweight=weight, zorder=z + 1)


def arrow(ax, x1, y1, x2, y2, color=SLATE, lw=2.0, ms=9, style="-|>", z=3,
          rad=0.0, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=ms, color=color, lw=lw, zorder=z,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def wire(ax, pts, color=INK, lw=1.6, z=3, ls="-"):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_capstyle="round", ls=ls)


def dot(ax, x, y, color=INK, s=16, z=5):
    ax.plot([x], [y], "o", color=color, ms=s / 3.0, zorder=z)


# --------------------------------------------------------------------------
# Logic-gate primitives.  (x, y) is the centre-left of the gate body;
# `w` is body width, `h` body height.  Returns (input_pts, output_pt).
# --------------------------------------------------------------------------
def _bubble(ax, x, y, r, ec):
    ax.add_patch(Circle((x + r, y), r, fc=WHITE, ec=ec, lw=1.7, zorder=4))
    return x + 2 * r


def gate(ax, kind, x, y, w=8.0, h=8.0, ec=NAVY, label=None, lsize=9,
         nin=2, stub=3.0, fc=WHITE):
    """Draw an IEEE distinctive-shape gate. Returns (inputs, output)."""
    kind = kind.upper()
    hb = h / 2.0
    br = h * 0.09          # bubble radius
    inv = kind in ("NOT", "NAND", "NOR", "XNOR")
    base = {"NAND": "AND", "NOR": "OR", "XNOR": "XOR", "NOT": "BUF"}.get(kind, kind)

    if base == "AND":
        body = w * 0.55
        ax.add_patch(Rectangle((x, y - hb), body, h, fc=fc, ec="none", zorder=3))
        ax.add_patch(Wedge((x + body, y), hb, -90, 90, fc=fc, ec="none", zorder=3))
        wire(ax, [(x + body, y - hb), (x, y - hb), (x, y + hb), (x + body, y + hb)],
             color=ec, lw=1.8, z=4)
        ax.add_patch(Arc((x + body, y), h, h, theta1=-90, theta2=90,
                         ec=ec, lw=1.8, zorder=4))
        tipx = x + body + hb
    elif base in ("OR", "XOR"):
        import numpy as np
        ts = np.linspace(-1, 1, 60)
        # back curve
        def backx(t, off=0.0):
            return x + off + w * 0.16 * (1 - t ** 2) * -1 + w * 0.16
        bx = [x + w * 0.18 * (1 - t ** 2) for t in ts]
        by = [y + hb * t for t in ts]
        # front: two arcs meeting at tip
        top = [(x + w * 0.16 * (t ** 2), y + hb * t) for t in ts]
        fx, fy = [], []
        for t in ts:
            fx.append(x + w * (0.18 + 0.82 * (1 - abs(t) ** 2.3)))
            fy.append(y + hb * t)
        ax.fill(bx + fx[::-1], by + fy[::-1], color=fc, zorder=3, ec="none")
        wire(ax, list(zip(bx, by)), color=ec, lw=1.8, z=4)
        wire(ax, list(zip(fx, fy)), color=ec, lw=1.8, z=4)
        if base == "XOR":
            bx2 = [x - w * 0.11 + w * 0.18 * (1 - t ** 2) for t in ts]
            wire(ax, list(zip(bx2, by)), color=ec, lw=1.8, z=4)
        tipx = x + w
    else:  # BUF / NOT triangle
        tipx = x + w * 0.72
        ax.add_patch(Polygon([(x, y - hb), (x, y + hb), (tipx, y)],
                             fc=fc, ec=ec, lw=1.8, zorder=4))

    outx = _bubble(ax, tipx, y, br, ec) if inv else tipx

    # input stubs
    ins = []
    if base == "BUF":
        offs = [0.0]
    elif nin == 2:
        offs = [hb * 0.5, -hb * 0.5]
    elif nin == 3:
        offs = [hb * 0.62, 0.0, -hb * 0.62]
    else:
        offs = [hb * (1 - 2 * i / (nin - 1)) * 0.72 for i in range(nin)]
    for o in offs:
        sx = x - (w * 0.11 if base == "XOR" else 0)
        # for OR/XOR the body curves in; start the stub a little inside
        adj = 0
        if base in ("OR", "XOR"):
            adj = w * 0.18 * (1 - (o / hb) ** 2)
        wire(ax, [(x - stub, y + o), (sx + adj, y + o)], color=ec, lw=1.6, z=4)
        ins.append((x - stub, y + o))

    wire(ax, [(outx, y), (outx + stub, y)], color=ec, lw=1.6, z=4)
    if label:
        ax.text(x + w * 0.42, y, label, ha="center", va="center",
                fontsize=lsize, color=ec, fontweight="bold", zorder=6)
    return ins, (outx + stub, y)


def table(ax, x, y, cols, rows, cw, rh, head_fc=NAVY, head_tc=WHITE,
          fc=WHITE, alt=LIGHT, ec=GRID, size=9, tc=BODY, bold_col=None,
          colcolors=None):
    """Draw a simple grid table with header row. (x,y) = top-left."""
    n = len(cols)
    widths = cw if isinstance(cw, (list, tuple)) else [cw] * n
    # header
    cx = x
    for i, c in enumerate(cols):
        ax.add_patch(Rectangle((cx, y - rh), widths[i], rh, fc=head_fc,
                               ec=head_fc, lw=0.8, zorder=3))
        ax.text(cx + widths[i] / 2, y - rh / 2, str(c), ha="center", va="center",
                fontsize=size, color=head_tc, fontweight="bold", zorder=4)
        cx += widths[i]
    # body
    yy = y - rh
    for r, row in enumerate(rows):
        cx = x
        bg = fc if r % 2 == 0 else alt
        for i, cell in enumerate(row):
            ax.add_patch(Rectangle((cx, yy - rh), widths[i], rh, fc=bg,
                                   ec=ec, lw=0.8, zorder=3))
            col = tc
            wt = "normal"
            if colcolors and colcolors.get(i):
                col = colcolors[i]
            if bold_col is not None and i in (bold_col if isinstance(bold_col, (list, tuple)) else [bold_col]):
                wt = "bold"
                col = NAVY if not (colcolors and colcolors.get(i)) else col
            ax.text(cx + widths[i] / 2, yy - rh / 2, str(cell), ha="center",
                    va="center", fontsize=size, color=col, fontweight=wt, zorder=4)
            cx += widths[i]
        yy -= rh
    return yy


def wave(ax, x0, y, width, seq, unit, color=TEAL, lw=2.0, name=None,
         name_size=9, label_dx=1.5, z=4):
    """Draw a digital waveform. seq = list of 0/1 (one per unit)."""
    hi = y + unit * 0.62
    lo = y
    pts = []
    px = x0
    prev = seq[0]
    pts.append((px, hi if prev else lo))
    for v in seq:
        if v != prev:
            pts.append((px, hi if v else lo))
        pts.append((px + width, hi if v else lo))
        prev = v
        px += width
    wire(ax, pts, color=color, lw=lw, z=z)
    if name:
        ax.text(x0 - label_dx, y + unit * 0.31, name, ha="right", va="center",
                fontsize=name_size, color=NAVY, fontweight="bold")
    return hi, lo


def clk_wave(ax, x0, y, period, n, unit, color=NAVY, name="clk", lw=2.0):
    seq = []
    for _ in range(n):
        seq += [0, 1]
    return wave(ax, x0, y, period / 2.0, seq, unit, color=color, name=name, lw=lw)
