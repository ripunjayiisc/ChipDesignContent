"""Topic 3C diagrams: sequential logic, flip-flops, registers, state machines."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsl import *
import numpy as np


def ff_symbol(ax, x, y, w, h, ins, outs, ec=TEAL, fc=WHITE, title_txt=None,
              clk_idx=None, lw=1.9, size=9.4, outside=False):
    """Draw a rectangular flip-flop/register symbol.
    ins/outs are lists of (label, colour). clk_idx marks which input gets the edge triangle."""
    box(ax, x, y, w, h, fc=fc, ec=ec, lw=lw, r=0.9)
    n = len(ins)
    ipts = []
    for i, (lab, c) in enumerate(ins):
        yy = y + h * (n - i) / (n + 1)
        wire(ax, [(x - 3.2, yy), (x, yy)], color=INK)
        if clk_idx is not None and i == clk_idx:
            ax.add_patch(Polygon([(x, yy + 1.05), (x + 1.7, yy), (x, yy - 1.05)],
                                 fc="none", ec=ec, lw=1.3, zorder=6))
            ax.text(x + 2.4, yy, lab, ha="left", va="center", fontsize=size - 1.0,
                    color=c, fontweight="bold", zorder=6)
        else:
            ax.text(x + 1.4, yy, lab, ha="left", va="center", fontsize=size,
                    color=c, fontweight="bold", zorder=6)
        if outside:
            ax.text(x - 3.8, yy, lab, ha="right", va="center", fontsize=size,
                    color=c, fontweight="bold")
        ipts.append((x - 3.2, yy))
    m = len(outs)
    opts = []
    for i, (lab, c) in enumerate(outs):
        yy = y + h * (m - i) / (m + 1)
        wire(ax, [(x + w, yy), (x + w + 3.2, yy)], color=INK)
        ax.text(x + w - 1.4, yy, lab, ha="right", va="center", fontsize=size,
                color=c, fontweight="bold", zorder=6)
        if outside:
            ax.text(x + w + 3.8, yy, lab, ha="left", va="center", fontsize=size,
                    color=c, fontweight="bold")
        opts.append((x + w + 3.2, yy))
    if title_txt:
        ax.text(x + w / 2, y + h + 1.9, title_txt, ha="center", va="center",
                fontsize=size + 0.4, color=ec, fontweight="bold")
    return ipts, opts


def clock_anatomy():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 40.0
    title(ax, 50, H - 2.0, "The clock — the single heartbeat every synchronous design marches to",
          13.0, NAVY)
    x0, per, u = 14.0, 12.4, 11.0
    ybase = 18.0
    seq = []
    for _ in range(6):
        seq += [0, 1]
    hi, lo = wave(ax, x0, ybase, per / 2, seq, u, color=NAVY, name="clk", lw=2.4, name_size=11)
    # ---- period ----
    for k in (1, 2):
        ax.plot([x0 + k * per, x0 + k * per], [ybase - 3.6, lo + 0.8], color=RED,
                lw=1.0, ls=(0, (3, 3)), zorder=2)
    arrow(ax, x0 + per, ybase - 2.6, x0 + 2 * per, ybase - 2.6, color=RED, lw=1.5,
          ms=9, style="<|-|>")
    ax.text(x0 + 1.5 * per, ybase - 4.6, "period  T", ha="center", va="center",
            fontsize=10, color=RED, fontweight="bold")
    # ---- high time ----
    for k in (4.5, 5.0):
        ax.plot([x0 + k * per / 2 * 2 / 2, x0 + k * per], [hi, hi + 4.2], color=AMBER,
                lw=0.0, zorder=2)
    xa, xb = x0 + 4.5 * per / 1.0 / 2 * 1.0, 0
    xa = x0 + 4.5 * (per / 2) * 1.0
    xa = x0 + 9 * (per / 2)          # start of a HIGH half-period
    xb = xa + per / 2
    for xx in (xa, xb):
        ax.plot([xx, xx], [hi, hi + 4.4], color=AMBER, lw=1.0, ls=(0, (3, 3)), zorder=2)
    arrow(ax, xa, hi + 3.4, xb, hi + 3.4, color=AMBER, lw=1.5, ms=9, style="<|-|>")
    ax.text((xa + xb) / 2, hi + 5.6, "t$_{high}$", ha="center", va="center",
            fontsize=9.6, color=AMBER, fontweight="bold")
    # ---- edges ----
    for k, (xx, lab, c, ly) in enumerate([(x0 + per / 2, "rising edge  (posedge)", GREEN, 34.6),
                                          (x0 + per, "falling edge  (negedge)", SLATE, 31.4)]):
        ax.add_patch(Circle((xx, (hi + lo) / 2), 1.1, fc="none", ec=c, lw=2.0, zorder=6))
        ax.plot([xx, xx + 5.0], [(hi + lo) / 2 + 1.1, ly - 0.9], color=c, lw=1.1, zorder=5)
        ax.text(xx + 5.6, ly, lab, ha="left", va="center", fontsize=9.0, color=c,
                fontweight="bold")
    cards = [("Period  T", "seconds per cycle", TEAL),
             ("Frequency  f = 1/T", "T = 2 ns  →  f = 500 MHz", TEAL),
             ("Duty cycle", "t$_{high}$ / T — usually 50 %", AMBER),
             ("Edge", "the instant a flip-flop samples", GREEN)]
    cwd = 23.0
    for i, (k, v, c) in enumerate(cards):
        x = 2.0 + i * (cwd + 1.4)
        box(ax, x, 2.5, cwd, 8.0, fc=LIGHT, ec=c, lw=1.5)
        ax.text(x + cwd / 2, 8.1, k, ha="center", va="center", fontsize=9.2,
                color=c, fontweight="bold")
        ax.text(x + cwd / 2, 4.8, v, ha="center", va="center", fontsize=7.8, color=BODY)
    save(f, "clock_anatomy")


def sr_latch():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 38.46
    title(ax, 50, H - 2.0, "The SR latch — the smallest circuit that can remember one bit", 13.0, NAVY)
    # cross-coupled NOR
    box(ax, 2.0, 3.0, 46.0, 30.0, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(25.0, 30.8, "Cross-coupled NOR gates", ha="center", va="center", fontsize=10.2,
            color=NAVY, fontweight="bold")
    i1, o1 = gate(ax, "NOR", 18.0, 23.0, 7.0, 6.4, ec=TEAL, stub=2.4, fc=WHITE)
    i2, o2 = gate(ax, "NOR", 18.0, 12.0, 7.0, 6.4, ec=TEAL, stub=2.4, fc=WHITE)
    ax.text(i1[0][0] - 0.7, i1[0][1], "R", ha="right", va="center", fontsize=10.5,
            color=RED, fontweight="bold")
    ax.text(i2[1][0] - 0.7, i2[1][1], "S", ha="right", va="center", fontsize=10.5,
            color=GREEN, fontweight="bold")
    ax.text(o1[0] + 0.8, o1[1], "Q", ha="left", va="center", fontsize=11, color=NAVY, fontweight="bold")
    ax.text(o2[0] + 0.8, o2[1], "Q'", ha="left", va="center", fontsize=11, color=NAVY, fontweight="bold")
    # cross-coupling
    ax.plot([o1[0] - 1.0], [o1[1]], "o", color=AMBER, ms=4, zorder=8)
    wire(ax, [(o1[0] - 1.0, o1[1]), (o1[0] - 1.0, 17.8), (13.0, 17.8), (13.0, i2[0][1]), i2[0]],
         color=AMBER, lw=1.6)
    ax.plot([o2[0] - 1.0], [o2[1]], "o", color=AMBER, ms=4, zorder=8)
    wire(ax, [(o2[0] - 1.0, o2[1]), (o2[0] - 1.0, 17.2), (14.6, 17.2), (14.6, i1[1][1]), i1[1]],
         color=AMBER, lw=1.6)
    ax.text(25.0, 6.4, "Each gate's output feeds the OTHER gate's input.\n"
            "That loop is the memory: remove it and you have plain combinational logic.",
            ha="center", va="center", fontsize=8.4, color=BODY, linespacing=1.6)

    # table
    box(ax, 51.0, 3.0, 47.0, 30.0, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(74.5, 30.8, "Behaviour", ha="center", va="center", fontsize=10.2,
            color=TEAL, fontweight="bold")
    table(ax, 54.0, 28.0, ["S", "R", "Q$_{next}$", "meaning"],
          [["0", "0", "Q", "HOLD — remembers"],
           ["0", "1", "0", "RESET to 0"],
           ["1", "0", "1", "SET to 1"],
           ["1", "1", "—", "FORBIDDEN"]],
          [7.0, 7.0, 10.0, 18.0], 3.0, size=9.0, head_fc=NAVY, bold_col=[2])
    ax.add_patch(FancyBboxPatch((54.0, 4.0), 42.0, 8.4, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#FDECEF", ec=RED, lw=1.6, zorder=3))
    ax.text(75.0, 10.2, "Why S = R = 1 is forbidden", ha="center", va="center",
            fontsize=9.4, color=RED, fontweight="bold", zorder=5)
    ax.text(75.0, 6.4, "Both outputs are forced to 0, so Q and Q' are no longer complements.\n"
            "Worse, releasing both together leaves the final state UNPREDICTABLE — a race.",
            ha="center", va="center", fontsize=7.8, color=BODY, zorder=5, linespacing=1.6)
    save(f, "sr_latch")


def latch_vs_ff():
    W, Hin = 13, 5.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 44.62
    title(ax, 50, H - 2.0, "Latch vs flip-flop — level-sensitive versus edge-triggered", 13.0, NAVY)
    x0, ww, u = 18.0, 4.6, 8.4
    n = 16
    clk = [0, 0, 1, 1] * 4                     # quarter-period resolution
    dsq = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1]
    # shade the clock-HIGH phases
    for k in range(4):
        xs = x0 + (4 * k + 2) * ww
        ax.add_patch(Rectangle((xs, 8.5), 2 * ww, 29.0, fc=TEAL, alpha=0.10, ec="none", zorder=1))
    wave(ax, x0, 31.5, ww, clk, u, color=NAVY, name="clk", name_size=10, label_dx=2.0)
    wave(ax, x0, 24.0, ww, dsq, u, color=AMBER, name="D", name_size=10, label_dx=2.0)
    lat, q = [], 0
    for i in range(n):
        if clk[i] == 1:
            q = dsq[i]
        lat.append(q)
    wave(ax, x0, 16.5, ww, lat, u, color=TEAL, name="Q  (D latch)", name_size=9.4, label_dx=2.0)
    ffo, q = [], 0
    for i in range(n):
        if clk[i] == 1 and (i == 0 or clk[i - 1] == 0):
            q = dsq[i]
        ffo.append(q)
    wave(ax, x0, 9.0, ww, ffo, u, color=GREEN, name="Q  (D flip-flop)", name_size=9.4, label_dx=2.0)
    for k in range(4):
        xs = x0 + (4 * k + 2) * ww
        ax.add_patch(Polygon([(xs - 1.0, 6.6), (xs + 1.0, 6.6), (xs, 8.2)],
                             fc=GREEN, ec="none", zorder=6))
    ax.text(x0 + 10.5 * ww, 40.0, "shaded = clock HIGH (a latch is transparent here)",
            ha="center", va="center", fontsize=8.0, color=TEAL, fontweight="bold")
    ax.text(x0 + n * ww / 2, 4.6, "▲  the only instants a flip-flop looks at D",
            ha="center", va="center", fontsize=8.8, color=GREEN, fontweight="bold")
    # call out the two places they differ
    for k in (3, 11):
        xs = x0 + k * ww
        ax.add_patch(FancyBboxPatch((xs - 0.5, 15.6), ww + 1.0, 6.6,
                     boxstyle="round,pad=0,rounding_size=0.8", fc="none", ec=RED,
                     lw=1.8, zorder=8))
    ax.text(x0 + 3.5 * ww, 40.0, "red boxes = D changes mid-pulse", ha="center", va="center",
            fontsize=7.6, color=RED, fontweight="bold", zorder=9)
    box(ax, 2.0, 0.6, 96.0, 3.2, fc=LIGHT, ec=TEAL, lw=1.4)
    ax.text(50, 2.2, "A latch is a door held open while clk is high — the output can change many times per cycle.    "
            "A flip-flop is a turnstile — exactly one change per clock edge.    "
            "In the red boxes D changes mid-pulse: the latch follows it, the flip-flop does not.",
            ha="center", va="center", fontsize=7.8, color=NAVY, fontweight="bold")
    save(f, "latch_vs_ff")


def master_slave():
    W, Hin = 13, 4.4
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 33.85
    title(ax, 50, H - 2.0, "How edge-triggering is actually built — the master–slave D flip-flop",
          13.0, NAVY)
    cy = 18.0
    label_box(ax, 20.0, cy - 5.0, 17.0, 10.0, "MASTER\nD latch", fc=WHITE, ec=TEAL, tc=NAVY,
              size=9.4, lw=1.9)
    label_box(ax, 50.0, cy - 5.0, 17.0, 10.0, "SLAVE\nD latch", fc=WHITE, ec=GREEN, tc=NAVY,
              size=9.4, lw=1.9)
    wire(ax, [(12.0, cy), (20.0, cy)], color=INK, lw=1.7)
    ax.text(11.4, cy, "D", ha="right", va="center", fontsize=11, color=AMBER, fontweight="bold")
    arrow(ax, 37.0, cy, 49.6, cy, color=SLATE, lw=1.7, ms=10)
    ax.text(43.3, cy + 2.2, "Q$_M$", ha="center", va="center", fontsize=9.4,
            color=SLATE, fontweight="bold")
    wire(ax, [(67.0, cy), (74.0, cy)], color=INK, lw=1.7)
    ax.text(74.6, cy, "Q", ha="left", va="center", fontsize=11, color=GREEN, fontweight="bold")
    # clock distribution
    wire(ax, [(8.0, 6.0), (58.5, 6.0)], color=RED, lw=1.7)
    ax.text(7.4, 6.0, "clk", ha="right", va="center", fontsize=10, color=RED, fontweight="bold")
    wire(ax, [(24.0, 6.0), (24.0, 10.4)], color=RED, lw=1.7)
    dot(ax, 24.0, 6.0, color=RED)
    _, invo = gate(ax, "NOT", 25.5, 10.4, 5.0, 3.8, ec=RED, stub=1.5, nin=1, fc=WHITE)
    wire(ax, [invo, (invo[0] + 1.4, invo[1]), (invo[0] + 1.4, cy - 5.0)], color=RED, lw=1.7)
    wire(ax, [(58.5, 6.0), (58.5, cy - 5.0)], color=RED, lw=1.7)
    ax.text(invo[0] + 2.1, 11.6, "clk'", ha="left", va="center", fontsize=8.6,
            color=RED, fontweight="bold")
    ax.text(59.3, 11.6, "clk", ha="left", va="center", fontsize=8.6, color=RED, fontweight="bold")
    ax.add_patch(FancyBboxPatch((2.0, 23.0), 45.0, 6.8, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#E8F5F7", ec=TEAL, lw=1.5, zorder=2))
    ax.text(24.5, 27.6, "While clk = 0", ha="center", va="center", fontsize=9.4,
            color=TEAL, fontweight="bold", zorder=4)
    ax.text(24.5, 24.8, "master is transparent and tracks D; slave holds the old Q.",
            ha="center", va="center", fontsize=8.2, color=BODY, zorder=4)
    ax.add_patch(FancyBboxPatch((51.0, 23.0), 47.0, 6.8, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#E4F4EC", ec=GREEN, lw=1.5, zorder=2))
    ax.text(74.5, 27.6, "When clk goes 0 → 1", ha="center", va="center", fontsize=9.4,
            color=GREEN, fontweight="bold", zorder=4)
    ax.text(74.5, 24.8, "master freezes, slave opens and copies it. ONE change per edge.",
            ha="center", va="center", fontsize=8.2, color=BODY, zorder=4)
    ax.text(50, 2.6, "Because the two latches are never transparent at the same time, data can never race through both "
            "in one clock phase — that is precisely what makes the flip-flop edge-triggered.",
            ha="center", va="center", fontsize=8.8, color=BODY, style="italic")
    save(f, "master_slave")


def ff_family():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "The flip-flop family — four behaviours, one clocked structure", 13.0, NAVY)
    specs = [
        ("D  flip-flop", TEAL, [("D", NAVY), ("clk", RED)],
         "Q$_{next}$ = D",
         [["0", "0"], ["1", "1"]], ["D", "Q$_{next}$"],
         "The workhorse. Everything\nsynthesisable maps to this."),
        ("T  flip-flop", GREEN, [("T", NAVY), ("clk", RED)],
         "Q$_{next}$ = T ⊕ Q",
         [["0", "Q"], ["1", "Q'"]], ["T", "Q$_{next}$"],
         "Toggle on every edge when\nT=1 — the basis of counters."),
        ("JK  flip-flop", AMBER, [("J", NAVY), ("K", NAVY), ("clk", RED)],
         "Q$_{next}$ = JQ' + K'Q",
         [["0", "0", "Q"], ["0", "1", "0"], ["1", "0", "1"], ["1", "1", "Q'"]],
         ["J", "K", "Q$_{next}$"],
         "Like SR but J=K=1 toggles\ninstead of being illegal."),
        ("SR  flip-flop", SLATE, [("S", NAVY), ("R", NAVY), ("clk", RED)],
         "Q$_{next}$ = S + R'Q",
         [["0", "0", "Q"], ["0", "1", "0"], ["1", "0", "1"], ["1", "1", "—"]],
         ["S", "R", "Q$_{next}$"],
         "Clocked SR latch. S=R=1\nremains forbidden."),
    ]
    pw = 23.4
    for i, (nm, c, ins, eq, rows, hdr, note) in enumerate(specs):
        x = 1.6 + i * (pw + 1.5)
        box(ax, x, 3.0, pw, 35.0, fc=WHITE, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x, 33.0), pw, 5.0, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 33.0), pw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + pw / 2, 35.5, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=6)
        ff_symbol(ax, x + 7.4, 22.0, 8.6, 9.0, ins, [("Q", NAVY)], ec=c,
                  clk_idx=len(ins) - 1, size=8.4)
        ax.text(x + pw / 2, 19.4, eq, ha="center", va="center", fontsize=9.4,
                color=NAVY, fontweight="bold")
        wds = [6.0] * (len(hdr) - 1) + [8.4]
        tw_ = sum(wds)
        table(ax, x + (pw - tw_) / 2, 17.8, hdr, rows, wds, 2.15, size=8.2,
              head_fc=NAVY, bold_col=[len(hdr) - 1])
        ax.text(x + pw / 2, 4.9, note, ha="center", va="center", fontsize=7.4,
                color=BODY, linespacing=1.5)
    save(f, "ff_family")


def ff_timing():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 36.92
    title(ax, 50, H - 2.0, "The three timing parameters that decide whether a flip-flop works",
          13.0, NAVY)
    x0, ww, u = 14.0, 4.5, 9.0
    n = 12
    clk = [0, 0, 1, 1] * 3                     # rising edges at index 2, 6, 10
    edge = x0 + 6 * ww                         # the edge we annotate
    setw, holdw = 6.0, 3.0
    ax.add_patch(Rectangle((edge - setw, 14.0), setw, 8.6, fc=RED, alpha=0.13, ec="none", zorder=1))
    ax.add_patch(Rectangle((edge, 14.0), holdw, 8.6, fc=TEAL, alpha=0.16, ec="none", zorder=1))
    ax.plot([edge, edge], [5.0, 32.0], color=SLATE, lw=1.0, ls=(0, (3, 3)), zorder=2)
    wave(ax, x0, 24.0, ww, clk, u, color=NAVY, name="clk", name_size=10, label_dx=2.0)
    dsq = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    wave(ax, x0, 14.5, ww, dsq, u, color=AMBER, name="D", name_size=10, label_dx=2.0)
    qsq = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    wave(ax, x0, 5.5, ww, qsq, u, color=GREEN, name="Q", name_size=10, label_dx=2.0)
    hi = 24.0 + 0.62 * u
    arrow(ax, edge - setw, hi + 1.6, edge, hi + 1.6, color=RED, lw=1.4, ms=8, style="<|-|>")
    ax.text(edge - setw / 2, hi + 3.2, "t$_{setup}$", ha="center", va="center", fontsize=9.4,
            color=RED, fontweight="bold")
    arrow(ax, edge, hi + 1.6, edge + holdw, hi + 1.6, color=TEAL, lw=1.4, ms=8, style="<|-|>")
    ax.text(edge + holdw + 1.4, hi + 3.2, "t$_{hold}$", ha="left", va="center", fontsize=9.4,
            color=TEAL, fontweight="bold")
    ax.plot([edge + holdw / 2, edge + holdw + 1.1], [hi + 2.4, hi + 3.0],
            color=TEAL, lw=1.0, zorder=5)
    arrow(ax, edge, 12.2, x0 + 7 * ww, 12.2, color=GREEN, lw=1.4, ms=8, style="<|-|>")
    ax.text((edge + x0 + 7 * ww) / 2, 10.4, "t$_{cq}$", ha="center", va="center", fontsize=9.4,
            color=GREEN, fontweight="bold")
    box(ax, 72.0, 12.0, 26.0, 20.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(85.0, 29.6, "If you violate them", ha="center", va="center", fontsize=9.6,
            color=RED, fontweight="bold")
    ax.text(85.0, 21.0, "The flip-flop can go\nMETASTABLE — its output\nhovers between 0 and 1\n"
            "for an unbounded time,\nthen settles to either\nvalue at random.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.7)
    defs = [("t$_{setup}$", "D stable this long BEFORE the edge", RED),
            ("t$_{hold}$", "D stable this long AFTER the edge", TEAL),
            ("t$_{cq}$", "edge → Q valid (clock-to-Q delay)", GREEN)]
    for j, (k, v, c) in enumerate(defs):
        x = 2.0 + j * 32.6
        box(ax, x, 0.8, 31.0, 3.6, fc=LIGHT, ec=c, lw=1.4)
        ax.text(x + 2.0, 2.6, k, ha="left", va="center", fontsize=9.2, color=c, fontweight="bold")
        ax.text(x + 8.4, 2.6, v, ha="left", va="center", fontsize=7.4, color=BODY)
    save(f, "ff_timing")


def metastability():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 36.92
    title(ax, 50, H - 2.0, "Metastability and the two-flop synchroniser", 13.0, NAVY)
    # left: metastable waveform
    box(ax, 2.0, 10.0, 44.0, 23.0, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(24.0, 31.2, "What a metastable output looks like", ha="center", va="center",
            fontsize=9.8, color=NAVY, fontweight="bold")
    xs, xe = 8.0, 43.0
    lo, hia = 14.0, 26.0
    wire(ax, [(xs, lo), (16.0, lo)], color=SLATE, lw=2.0)
    t = np.linspace(0, 1, 220)
    yy = lo + (hia - lo) * (0.5 + 0.5 * np.tanh((t - 0.55) * 3.0) * 0.15)
    ax.plot(16.0 + t * 14.0, lo + (hia - lo) * (0.5 + 0.06 * np.sin(t * 26) * np.exp(-t * 2)),
            color=RED, lw=2.0, zorder=4)
    wire(ax, [(16.0, lo), (16.0, (lo + hia) / 2)], color=RED, lw=2.0)
    t2 = np.linspace(0, 1, 120)
    ax.plot(30.0 + t2 * 7.0, (lo + hia) / 2 + (hia - (lo + hia) / 2) * (1 / (1 + np.exp(-(t2 - 0.45) * 12))),
            color=RED, lw=2.0, zorder=4)
    wire(ax, [(37.0, hia), (xe, hia)], color=RED, lw=2.0)
    ax.plot([xs, xe], [hia, hia], color=GRID, lw=0.9, ls=(0, (4, 4)), zorder=2)
    ax.plot([xs, xe], [lo, lo], color=GRID, lw=0.9, ls=(0, (4, 4)), zorder=2)
    ax.text(xs - 0.6, hia, "1", ha="right", va="center", fontsize=9, color=SLATE, fontweight="bold")
    ax.text(xs - 0.6, lo, "0", ha="right", va="center", fontsize=9, color=SLATE, fontweight="bold")
    ax.text(23.0, 21.4, "hovers here", ha="center", va="center", fontsize=8.6,
            color=RED, fontweight="bold")
    ax.text(24.0, 11.6, "The resolution time is a random variable — it has NO upper bound.",
            ha="center", va="center", fontsize=8.0, color=BODY)

    # right: 2-FF synchroniser
    box(ax, 49.0, 10.0, 49.0, 23.0, fc=LIGHT, ec=GREEN, lw=1.6)
    ax.text(73.5, 31.2, "The fix: a two-flop synchroniser", ha="center", va="center",
            fontsize=9.8, color=GREEN, fontweight="bold")
    cy = 21.0
    for k, (xx, c) in enumerate([(60.0, AMBER), (76.0, GREEN)]):
        ff_symbol(ax, xx, cy - 4.0, 8.0, 8.0, [("D", NAVY), ("clk", RED)], [("Q", NAVY)],
                  ec=c, clk_idx=1, size=7.8)
    ax.text(54.5, cy + 1.4, "async\nin", ha="center", va="center", fontsize=8.2,
            color=RED, fontweight="bold", linespacing=1.3)
    ax.text(92.0, cy + 1.4, "safe", ha="center", va="center", fontsize=8.6,
            color=GREEN, fontweight="bold")
    ax.text(73.5, 13.0, "FF1 may go metastable; it is given a full clock period to settle\n"
            "before FF2 samples it. Two stages cut the failure rate to ~1 in 10⁹ years.",
            ha="center", va="center", fontsize=7.8, color=BODY, linespacing=1.6)
    box(ax, 2.0, 2.0, 96.0, 6.4, fc="#FDECEF", ec=RED, lw=1.5)
    ax.text(50, 5.4, "Rule you must never break:  every signal entering your clock domain from OUTSIDE it — another clock",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold")
    ax.text(50, 3.2, "domain, a button, a sensor, an off-chip pin — must pass through a synchroniser first.",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold")
    save(f, "metastability")


def fmax_path():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 35.38
    title(ax, 50, H - 2.0, "The timing path — where the maximum clock frequency comes from",
          13.0, NAVY)
    cy = 21.0
    ff_symbol(ax, 10.0, cy - 5.0, 9.0, 10.0, [("D", NAVY), ("clk", RED)], [("Q", NAVY)],
              ec=TEAL, clk_idx=1, size=8.6)
    label_box(ax, 36.0, cy - 4.0, 22.0, 8.0, "combinational logic", fc=WHITE, ec=AMBER,
              tc=NAVY, size=9.4, lw=1.9)
    ff_symbol(ax, 68.0, cy - 5.0, 9.0, 10.0, [("D", NAVY), ("clk", RED)], [("Q", NAVY)],
              ec=TEAL, clk_idx=1, size=8.6)
    ax.text(14.5, 13.6, "launch FF", ha="center", va="center", fontsize=9.2,
            color=TEAL, fontweight="bold")
    ax.text(72.5, 13.6, "capture FF", ha="center", va="center", fontsize=9.2,
            color=TEAL, fontweight="bold")
    arrow(ax, 22.6, cy, 35.6, cy, color=SLATE, lw=1.9, ms=11)
    arrow(ax, 58.4, cy, 64.4, cy, color=SLATE, lw=1.9, ms=11)
    wire(ax, [(6.0, 7.0), (76.0, 7.0)], color=RED, lw=1.8)
    ax.text(5.4, 7.0, "clk", ha="right", va="center", fontsize=10, color=RED, fontweight="bold")
    for xx in (14.5, 72.5):
        wire(ax, [(xx, 7.0), (xx, cy - 5.0)], color=RED, lw=1.5)
        dot(ax, xx, 7.0, color=RED)
    segs = [(14.5, 22.6, "t$_{cq}$  =  60 ps", GREEN),
            (22.6, 64.4, "t$_{logic}$  =  240 ps", AMBER),
            (64.4, 72.5, "t$_{setup}$  =  50 ps", RED)]
    for a_, b_, lab, c in segs:
        arrow(ax, a_, cy + 7.6, b_, cy + 7.6, color=c, lw=1.5, ms=9, style="<|-|>")
        ax.text((a_ + b_) / 2, cy + 9.6, lab, ha="center", va="center", fontsize=9.0,
                color=c, fontweight="bold")
    box(ax, 80.0, 12.0, 18.0, 17.0, fc="#FDECEF", ec=RED, lw=1.5)
    ax.text(89.0, 26.8, "Hold check", ha="center", va="center", fontsize=9.0,
            color=RED, fontweight="bold")
    ax.text(89.0, 22.6, "t$_{cq}$ + t$_{logic,min}$\n≥  t$_{hold}$",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold",
            linespacing=1.7)
    ax.text(89.0, 16.4, "Hold is a RACE,\nnot a speed limit —\nit cannot be fixed\nby slowing the clock.",
            ha="center", va="center", fontsize=7.2, color=BODY, linespacing=1.6)
    box(ax, 2.0, 1.0, 96.0, 4.4, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 3.2, "T$_{clk}$  ≥  t$_{cq}$ + t$_{logic}$ + t$_{setup}$        "
            "here:  60 + 240 + 50 = 350 ps        f$_{max}$ = 1 / 350 ps  ≈  2.86 GHz",
            ha="center", va="center", fontsize=10.0, color=NAVY, fontweight="bold")
    save(f, "fmax_path")


def clock_skew():
    W, Hin = 13, 4.2
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 32.31
    title(ax, 50, H - 2.0, "Clock skew and jitter — two ways the heartbeat goes wrong", 13.0, NAVY)
    x0, ww, u = 14.0, 4.6, 7.6
    clk = [0, 1] * 4
    wave(ax, x0, 20.0, ww, clk, u, color=NAVY, name="clk @ FF1", name_size=8.6, label_dx=2.0)
    wave(ax, x0 + 2.4, 13.0, ww, clk, u, color=AMBER, name="clk @ FF2", name_size=8.6, label_dx=4.4)
    for k in range(1, 4):
        xe = x0 + (2 * k - 1) * ww
        ax.plot([xe, xe], [12.4, 25.4], color=RED, lw=1.0, ls=(0, (3, 3)), zorder=2)
        ax.plot([xe + 2.4, xe + 2.4], [12.4, 25.4], color=RED, lw=1.0, ls=(0, (3, 3)), zorder=2)
    xe = x0 + ww
    arrow(ax, xe, 26.6, xe + 2.4, 26.6, color=RED, lw=1.5, ms=9, style="<|-|>")
    ax.text(xe + 1.2, 28.4, "skew", ha="center", va="center", fontsize=9.2,
            color=RED, fontweight="bold")
    ax.text(30.0, 9.4, "SKEW — the same clock edge reaches different flip-flops at\n"
            "different times. Systematic, caused by unequal clock-tree wire\n"
            "lengths, and fixed by clock-tree synthesis (CTS).",
            ha="center", va="center", fontsize=7.8, color=BODY, linespacing=1.6)
    box(ax, 60.0, 3.5, 38.0, 24.5, fc=LIGHT, ec=AMBER, lw=1.6)
    ax.text(79.0, 25.8, "JITTER", ha="center", va="center", fontsize=10,
            color=AMBER, fontweight="bold")
    ax.text(79.0, 20.6, "The edge of the SAME clock line arrives\nearly or late from cycle to cycle — random,\n"
            "caused by supply noise and the PLL.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    ax.text(79.0, 14.4, "Both eat into your timing budget:", ha="center", va="center",
            fontsize=8.8, color=NAVY, fontweight="bold")
    ax.text(79.0, 9.0, "T$_{clk}$  ≥  t$_{cq}$ + t$_{logic}$ + t$_{setup}$\n              + t$_{skew}$ + t$_{jitter}$",
            ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="bold", linespacing=1.8)
    ax.text(79.0, 5.2, "Useful skew: a deliberately late capture clock\nbuys the path extra time.",
            ha="center", va="center", fontsize=7.0, color=SLATE, style="italic", linespacing=1.5)
    save(f, "clock_skew")


if __name__ == "__main__":
    clock_anatomy(); sr_latch(); latch_vs_ff(); master_slave()
    ff_family(); ff_timing(); metastability(); fmax_path(); clock_skew()
