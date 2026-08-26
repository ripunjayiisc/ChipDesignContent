# -*- coding: utf-8 -*-
"""Topic 5 diagrams — testbench construction."""
import _boot
from dsl import *


# ---------------------------------------------------------------- anatomy
def tb_anatomy():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 53.9
    title(ax, 50, H - 3, "The six parts of every testbench", 13)

    box(ax, 3, 3.0, 94, 44.0, fc=LIGHT, ec=GRID)
    ax.text(50, 44.5, "module tb_fifo;      // a module with NO PORTS - nothing outside drives it",
            fontsize=9.2, color=SLATE, ha="center", family="monospace")

    dutx, dutw, duty, duth = 39.5, 21, 22.0, 12.0
    label_box(ax, dutx, duty, dutw, duth, "DEVICE\nUNDER TEST", fc=WHITE, ec=NAVY,
              tc=NAVY, size=10, lw=2.2)

    items = [
        (1, "CLOCK & RESET",   6.0, 33.0, 27, 8.5, TEAL,   "always #(CLK/2) clk = ~clk;"),
        (4, "CHECKS",         67.0, 33.0, 27, 8.5, VIOLET, "one task, one error counter"),
        (2, "STIMULUS",        6.0, 22.0, 27, 9.0, TEAL,   "tasks that drive the pins"),
        (5, "WAVEFORM DUMP",  67.0, 22.0, 27, 9.0, AMBER,  "\\$dumpfile / \\$dumpvars"),
        (3, "REFERENCE MODEL", 6.0, 11.0, 27, 9.0, GREEN,  "computes what SHOULD happen"),
        (6, "VERDICT & STOP", 67.0, 11.0, 27, 9.0, RED,    "PASS / FAIL, then \\$finish"),
    ]
    for n, name, x, y, w, h, col, sub in items:
        box(ax, x, y, w, h, fc=WHITE, ec=col, lw=1.7)
        ax.add_patch(Circle((x + 2.9, y + h - 2.6), 2.0, fc=col, ec=col, zorder=5))
        ax.text(x + 2.9, y + h - 2.6, str(n), ha="center", va="center", fontsize=8,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(x + w / 2 + 2.4, y + h - 2.6, name, ha="center", va="center",
                fontsize=9, color=col, fontweight="bold")
        ax.text(x + w / 2, y + 2.9, sub, ha="center", va="center", fontsize=7.9,
                color=BODY, family="monospace")

    arrow(ax, 33, 28.0, dutx, 28.0, color=TEAL, lw=2.0)
    ax.text(36.2, 30.2, "drive", fontsize=8, color=TEAL, ha="center")
    arrow(ax, dutx + dutw, 28.0, 67, 28.0, color=VIOLET, lw=2.0)
    ax.text(64.2, 30.2, "observe", fontsize=8, color=VIOLET, ha="center")

    wire(ax, [(19.5, 11.0), (19.5, 7.5), (80.5, 7.5)], color=GREEN, lw=1.6, ls="--")
    arrow(ax, 80.5, 8.5, 80.5, 11.0, color=GREEN, lw=1.6, ls="--")
    ax.text(50, 5.0, "the model sees the same stimulus; its answer is what the checks compare against",
            fontsize=8.2, color=GREEN, ha="center", fontstyle="italic")
    save(f, "tb_anatomy")


# ----------------------------------------------------------------- layers
def tb_layers():
    W, Hin = 12.0, 5.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 43.3
    title(ax, 50, H - 3, "A layered testbench — each part replaceable on its own", 13)

    blocks = [("GENERATOR", "decides WHAT\nto test", VIOLET),
              ("DRIVER", "knows the pin-level\nprotocol", TEAL),
              ("DUT", "", NAVY),
              ("MONITOR", "watches the pins,\ndrives nothing", AMBER),
              ("SCOREBOARD", "the only place that\nknows 'correct'", GREEN)]
    bw, gap = 16.0, 4.0
    x0 = 50 - (5 * bw + 4 * gap) / 2
    y = 16.5                               # bottom of the block row
    for i, (name, sub, col) in enumerate(blocks):
        x = x0 + i * (bw + gap)
        if name == "DUT":
            box(ax, x, y - 1.5, bw, 15.5, fc=WHITE, ec=NAVY, lw=2.4)
            ax.text(x + bw / 2, y + 8.0, "DUT", ha="center", va="center", fontsize=12,
                    color=NAVY, fontweight="bold")
            ax.text(x + bw / 2, y + 3.4, "the only\nreal hardware", ha="center",
                    va="center", fontsize=8, color=SLATE, fontstyle="italic")
        else:
            box(ax, x, y, bw, 12.5, fc=WHITE, ec=col, lw=1.9)
            box(ax, x, y + 8.4, bw, 4.1, fc=col, ec=col)
            ax.text(x + bw / 2, y + 10.45, name, ha="center", va="center", fontsize=8.8,
                    color=WHITE, fontweight="bold")
            ax.text(x + bw / 2, y + 4.0, sub, ha="center", va="center", fontsize=8.2,
                    color=BODY)
        if i < 4:
            arrow(ax, x + bw, y + 6.2, x + bw + gap, y + 6.2, color=SLATE, lw=1.9)

    # assertions band, ABOVE the blocks and below the title
    xd = x0 + 2 * (bw + gap)
    label_box(ax, 22, H - 11.0, 56, 5.4, "ASSERTIONS  —  bound to the DUT, checked every cycle",
              fc="#F2EDFA", ec=VIOLET, tc=VIOLET, size=8.8)
    arrow(ax, xd + bw / 2, H - 11.0, xd + bw / 2, y + 14.0, color=VIOLET, lw=1.8)

    # reference model, BELOW the blocks
    xg = x0
    xs = x0 + 4 * (bw + gap)
    label_box(ax, 40, 5.5, 20, 6.0, "REFERENCE MODEL", fc="#EEF7F1", ec=GREEN,
              tc=GREEN, size=8.6)
    wire(ax, [(xg + bw / 2, y), (xg + bw / 2, 8.5), (40, 8.5)], color=GREEN, lw=1.7, ls="--")
    arrow(ax, 38, 8.5, 40, 8.5, color=GREEN, lw=1.7, ls="--")
    wire(ax, [(60, 8.5), (xs + bw / 2, 8.5), (xs + bw / 2, y)], color=GREEN, lw=1.7, ls="--")
    arrow(ax, xs + bw / 2, y - 2.0, xs + bw / 2, y, color=GREEN, lw=1.7, ls="--")
    ax.text(50, 2.4, "the same stimulus goes to the model; the scoreboard compares the two",
            ha="center", fontsize=8.3, color=GREEN, fontstyle="italic")
    save(f, "tb_layers")


# ----------------------------------------------------- stimulus timing
def stimulus_timing():
    W, Hin = 11.5, 5.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 45.2
    title(ax, 50, H - 3, "When to drive and when to sample — the commonest testbench bug", 12.5)

    for x0, col, fcol, head in [(3, RED, "#FDECEF", "WRONG — driven ON the clock edge"),
                                (52, GREEN, "#EEF7F1", "RIGHT — driven just AFTER the edge")]:
        box(ax, x0, 17.0, 45, 21.0, fc=fcol, ec=col, lw=1.7)
        ax.text(x0 + 22.5, 35.0, head, fontsize=9.4, color=col, fontweight="bold",
                ha="center")

    clk_wave(ax, 14, 28.5, 10.0, 3, 4.2, color=NAVY, name="clk")
    wave(ax, 14, 22.0, 5.0, [0, 0, 1, 1, 1, 0], 4.2, color=RED, name="wr_en")
    for k in range(3):
        xx = 14 + 5.0 + k * 10.0
        ax.plot([xx, xx], [22.0, 31.2], color=RED, lw=0.9, ls=":", zorder=1)
    ax.plot([24.0], [24.6], "o", ms=8, color=RED, zorder=6)
    ax.text(25.5, 19.2, "the input changes at the same instant as the edge: a race",
            fontsize=8.2, color=RED, ha="center")

    clk_wave(ax, 63, 28.5, 10.0, 3, 4.2, color=NAVY, name="clk")
    wave(ax, 63, 22.0, 5.0, [0, 0, 0, 1, 1, 0], 4.2, color=GREEN, name="wr_en")
    ax.text(74.5, 19.2, "the input settles long before the next edge: no ambiguity",
            fontsize=8.2, color=GREEN, ha="center")

    box(ax, 3, 3.5, 94, 12.0, fc=WHITE, ec=NAVY, lw=1.6)
    ax.text(50, 13.1, "The rule, and the code that implements it", fontsize=9.8,
            color=NAVY, fontweight="bold", ha="center")
    ax.text(50, 9.3, "@(posedge clk);  #1;  wr_en = 1'b1;                 // DRIVE a moment AFTER the edge",
            fontsize=8.8, color=GREEN, ha="center", family="monospace")
    ax.text(50, 5.8, "@(posedge clk);  #1;  check(rd_data, expected);      // SAMPLE after the NEXT edge",
            fontsize=8.8, color=GREEN, ha="center", family="monospace")
    save(f, "stimulus_timing")


# --------------------------------------------------------- reference model
def refmodel():
    W, Hin = 11.0, 5.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 49.1
    title(ax, 50, H - 3, "A reference model is a SECOND implementation of the specification", 12.5)

    ytop = H - 9.0
    label_box(ax, 4, ytop - 17.5, 18, 7.0, "STIMULUS", fc=WHITE, ec=VIOLET,
              tc=VIOLET, size=9.5)
    label_box(ax, 31, ytop - 11.0, 27, 11.0, "DEVICE UNDER TEST\n(the RTL)", fc=WHITE,
              ec=NAVY, tc=NAVY, size=9.5, lw=2.0)
    label_box(ax, 31, ytop - 24.0, 27, 11.0, "REFERENCE MODEL\n(the specification)",
              fc="#EEF7F1", ec=GREEN, tc=GREEN, size=9.5, lw=2.0)
    label_box(ax, 70, ytop - 17.5, 26, 11.0, "COMPARE", fc=WHITE, ec=AMBER, tc=AMBER,
              size=10, lw=2.0)

    wire(ax, [(22, ytop - 14.0), (27, ytop - 14.0), (27, ytop - 5.5), (31, ytop - 5.5)],
         color=VIOLET, lw=1.8)
    arrow(ax, 29, ytop - 5.5, 31, ytop - 5.5, color=VIOLET, lw=1.8)
    wire(ax, [(27, ytop - 14.0), (27, ytop - 18.5), (31, ytop - 18.5)], color=VIOLET, lw=1.8)
    arrow(ax, 29, ytop - 18.5, 31, ytop - 18.5, color=VIOLET, lw=1.8)

    wire(ax, [(58, ytop - 5.5), (66, ytop - 5.5), (66, ytop - 9.5), (70, ytop - 9.5)],
         color=NAVY, lw=1.8)
    arrow(ax, 68, ytop - 9.5, 70, ytop - 9.5, color=NAVY, lw=1.8)
    wire(ax, [(58, ytop - 18.5), (66, ytop - 18.5), (66, ytop - 14.5), (70, ytop - 14.5)],
         color=GREEN, lw=1.8)
    arrow(ax, 68, ytop - 14.5, 70, ytop - 14.5, color=GREEN, lw=1.8)

    bb = dict(boxstyle="round,pad=0.22", fc=WHITE, ec="none")
    ax.text(63.0, ytop - 5.5, "what it DID", fontsize=8.0, color=NAVY, ha="center",
            va="center", bbox=bb, zorder=6)
    ax.text(63.0, ytop - 18.5, "what it SHOULD have done", fontsize=8.0, color=GREEN,
            ha="center", va="center", bbox=bb, zorder=6)

    box(ax, 4, 3.5, 92, 11.5, fc=LIGHT, ec=AMBER, lw=1.5)
    ax.text(50, 12.2, "Two rules that make a model worth having", fontsize=9.6,
            color=AMBER, fontweight="bold", ha="center")
    ax.text(50, 8.4, "1.  Write it from the SPECIFICATION, never by reading the RTL — "
                     "a model derived from the design agrees with the design's bugs.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.2, "2.  It never looks inside the DUT — only at the same inputs, and its own state.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "refmodel")


# ------------------------------------------------------- model order bug
def model_order_bug():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 53.9
    title(ax, 50, H - 3, "A real bug in a reference model, found while writing this lab", 12.5)
    ax.text(50, H - 7.2, "Read and write asserted together, on an EMPTY FIFO.",
            fontsize=9.2, color=SLATE, ha="center")

    ptop = H - 10.5
    box(ax, 3, 3.5, 45, ptop - 3.5, fc="#FDECEF", ec=RED, lw=1.8)
    ax.text(25.5, ptop - 3.6, "THE MODEL, WRITTEN WRONG", fontsize=9.4, color=RED,
            fontweight="bold", ha="center")
    y = ptop - 8.4
    for ln in ["if (do_w && !mfull())  push(d);",
               "if (do_r && !mempty()) pop();"]:
        ax.text(6, y, ln, fontsize=8.4, color=INK, ha="left", family="monospace")
        y -= 3.6
    y -= 1.6
    for a, b in [("start", "model empty, 0 words"),
                 ("push", "model now holds 1 word"),
                 ("test mempty()", "FALSE — it just pushed"),
                 ("pop", "the word goes straight back out"),
                 ("result", "model says 0.  Hardware says 1.")]:
        ax.text(6, y, a, fontsize=8.0, color=RED, ha="left", fontweight="bold")
        ax.text(22, y, b, fontsize=8.0, color=BODY, ha="left")
        y -= 3.9

    box(ax, 52, 3.5, 45, ptop - 3.5, fc="#EEF7F1", ec=GREEN, lw=1.8)
    ax.text(74.5, ptop - 3.6, "THE MODEL, WRITTEN RIGHT", fontsize=9.4, color=GREEN,
            fontweight="bold", ha="center")
    y = ptop - 8.4
    for ln in ["was_full  = mfull();      // sample FIRST",
               "was_empty = mempty();",
               "if (do_w && !was_full)  push(d);",
               "if (do_r && !was_empty) pop();"]:
        ax.text(55, y, ln, fontsize=8.1, color=INK, ha="left", family="monospace")
        y -= 3.6
    y -= 2.2
    ax.text(55, y, "The hardware decides BOTH from the state that", fontsize=8.4,
            color=BODY, ha="left")
    ax.text(55, y - 3.4, "existed BEFORE the clock edge. So must the model.",
            fontsize=8.4, color=BODY, ha="left")
    ax.text(55, y - 8.6, "Symptom before the fix: the CORRECT FIFO failed,",
            fontsize=8.3, color=RED, ha="left", fontweight="bold")
    ax.text(55, y - 11.9, "and the BROKEN one passed.", fontsize=8.3, color=RED,
            ha="left", fontweight="bold")
    save(f, "model_order_bug")


# ------------------------------------------------------------ random weights
def random_weights():
    W, Hin = 11.5, 5.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 48.7
    title(ax, 50, H - 3, "The constraints ARE the test — weighting changes what you reach", 12.5)

    profs = [("write-heavy", 90, 10, RED, "sits at FULL",
              "never reaches empty:\n3 of 12 bins MISS", 0.86, 0.22),
             ("read-heavy", 10, 90, AMBER, "sits at EMPTY",
              "never reaches full:\n4 of 12 bins MISS", 0.14, 0.22),
             ("balanced", 50, 50, GREEN, "roams the whole range",
              "all 12 bins HIT\nin a single run", 0.50, 0.80)]
    bw = 29.0
    x0 = 50 - (3 * bw + 2 * 3.5) / 2
    ptop, pbot = H - 8.0, 6.5
    for i, (name, w, r, col, mid, note, frac, span) in enumerate(profs):
        x = x0 + i * (bw + 3.5)
        box(ax, x, pbot, bw, ptop - pbot, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, ptop - 5.5, bw, 5.5, fc=col, ec=col)
        ax.text(x + bw / 2, ptop - 2.75, name, ha="center", va="center", fontsize=9.8,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ptop - 9.0, "+WR=%d   +RD=%d" % (w, r), ha="center",
                fontsize=8.6, color=NAVY, family="monospace")

        sx, sy, sw = x + 3.5, ptop - 17.5, bw - 7
        box(ax, sx, sy, sw, 4.2, fc=LIGHT, ec=GRID)
        ax.text(sx, sy - 2.8, "empty", fontsize=7.6, color=SLATE, ha="left")
        ax.text(sx + sw, sy - 2.8, "full", fontsize=7.6, color=SLATE, ha="right")
        bwid = sw * span
        bx = max(sx, min(sx + frac * sw - bwid / 2, sx + sw - bwid))
        box(ax, bx, sy + 0.5, bwid, 3.2, fc=col, ec=col, r=0.4)

        ax.text(x + bw / 2, sy - 7.2, "where the occupancy lives:", fontsize=8.2,
                color=SLATE, ha="center")
        ax.text(x + bw / 2, sy - 10.8, mid, fontsize=9.2, color=col, ha="center",
                fontweight="bold")
        ax.text(x + bw / 2, sy - 16.4, note, fontsize=8.4, color=BODY, ha="center")

    ax.text(50, 3.0, "Verified in Topic5_Lab: no single profile closes coverage. "
                     "Merged across all three, it does.",
            ha="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "random_weights")


# --------------------------------------------------------------- seeds
def seed_repro():
    W, Hin = 11.0, 3.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The seed is what makes a random failure debuggable", 12.5)

    label_box(ax, 5, H - 15, 17, 7.0, "+SEED=42", fc=WHITE, ec=VIOLET, tc=VIOLET,
              size=10)
    arrow(ax, 22, H - 11.5, 30, H - 11.5, color=SLATE, lw=1.8)
    label_box(ax, 30, H - 17, 24, 11.0, "the SAME\nsequence of\ntransactions", fc=LIGHT,
              ec=SLATE, tc=NAVY, size=9)
    arrow(ax, 54, H - 11.5, 62, H - 11.5, color=SLATE, lw=1.8)
    label_box(ax, 62, H - 17, 33, 11.0, "the SAME failure,\nat the SAME cycle,\nevery time",
              fc="#EEF7F1", ec=GREEN, tc=GREEN, size=9)

    box(ax, 5, 4.0, 90, 11.0, fc=WHITE, ec=AMBER, lw=1.6)
    ax.text(50, 12.4, "So the regression prints the seed on EVERY line, pass or fail",
            fontsize=9.5, color=AMBER, fontweight="bold", ha="center")
    ax.text(50, 8.6, "FAIL - V3 random on fifo_b5 : seed=1  342 errors, first at cycle 1",
            fontsize=8.8, color=RED, ha="center", family="monospace")
    ax.text(50, 5.6, "vvp build/regress.vvp +SEED=1 +WR=55 +RD=45      <- reproduces it exactly",
            fontsize=8.8, color=GREEN, ha="center", family="monospace")
    save(f, "seed_repro")


# ------------------------------------------------------------ coverage bins
def cov_bins():
    W, Hin = 11.5, 5.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "A coverage model, and the report it produces", 12.5)
    ax.text(50, H - 7.2, "Twelve bins, written before the stimulus. Real output from "
                         "Topic5_Lab, three stimulus profiles.",
            fontsize=8.8, color=SLATE, ha="center")

    bins = ["write accepted", "read accepted", "read+write same cycle", "idle cycle",
            "read+write while EMPTY", "read+write while FULL", "reached FULL",
            "reached EMPTY", "pointers wrapped", "write attempted while full",
            "read attempted while empty", "full -> empty -> full"]
    # HIT/MISS per profile: writeheavy, readheavy, balanced
    wh = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0]
    rh = [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0]
    ba = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    x0 = 6
    colw = [40, 13, 13, 13, 13]
    heads = ["coverage bin", "write-\nheavy", "read-\nheavy", "balanced", "MERGED"]
    y = H - 11
    cx = x0
    for i, hh in enumerate(heads):
        ax.add_patch(Rectangle((cx, y - 6.0), colw[i], 6.0, fc=NAVY, ec=NAVY, lw=0.8, zorder=3))
        ax.text(cx + colw[i] / 2, y - 3.0, hh, ha="center", va="center", fontsize=8.0,
                color=WHITE, fontweight="bold", zorder=4)
        cx += colw[i]
    yy = y - 6.0
    for j, b in enumerate(bins):
        cx = x0
        bg = WHITE if j % 2 == 0 else LIGHT
        ax.add_patch(Rectangle((cx, yy - 3.6), colw[0], 3.6, fc=bg, ec=GRID, lw=0.6, zorder=3))
        ax.text(cx + 1.5, yy - 1.8, b, ha="left", va="center", fontsize=7.8, color=BODY, zorder=4)
        cx += colw[0]
        for k, arr in enumerate([wh, rh, ba, None]):
            v = 1 if arr is None else arr[j]
            ax.add_patch(Rectangle((cx, yy - 3.6), colw[k + 1], 3.6,
                                   fc="#EEF7F1" if v else "#FDECEF", ec=GRID, lw=0.6, zorder=3))
            ax.text(cx + colw[k + 1] / 2, yy - 1.8, "HIT" if v else "MISS", ha="center",
                    va="center", fontsize=7.6, color=GREEN if v else RED,
                    fontweight="bold", zorder=4)
            cx += colw[k + 1]
        yy -= 3.6
    cx = x0
    tots = ["totals", "9/12", "8/12", "12/12", "12/12"]
    for i, t in enumerate(tots):
        ax.add_patch(Rectangle((cx, yy - 4.4), colw[i], 4.4, fc=NAVY, ec=NAVY, lw=0.8, zorder=3))
        ax.text(cx + colw[i] / 2, yy - 2.2, t, ha="center", va="center", fontsize=8.2,
                color=WHITE, fontweight="bold", zorder=4)
        cx += colw[i]
    ax.text(50, yy - 8.0,
            "No single profile closes coverage. Merged across the regression, it does — "
            "and that is how coverage is really closed.",
            ha="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "cov_bins")


# --------------------------------------------------------- assertion anatomy
def assertion_anatomy():
    W, Hin = 11.5, 4.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Anatomy of a concurrent assertion", 13)

    code = "a_step_up: assert property (@(posedge clk) disable iff (!rst_n)  wr_accepted |=> count == \\$past(count)+1);"
    box(ax, 3, H - 16, 94, 6.5, fc=INK, ec=VIOLET, lw=1.6)
    ax.text(50, H - 12.75, code, fontsize=8.2, color="#DCE6F0", ha="center",
            family="monospace")

    parts = [("a_step_up:", "a NAME — it appears in the failure message", 9, VIOLET),
             ("assert property", "check this on every clock. cover property just RECORDS it.", 27, TEAL),
             ("@(posedge clk)", "the sampling clock — assertions are synchronous", 43, NAVY),
             ("disable iff (!rst_n)", "switched off during reset, where nothing is guaranteed", 58, AMBER),
             ("|=>", "implication with ONE cycle of delay.  |-> means same cycle.", 76, GREEN),
             ("\\$past(count)", "the value one clock ago — how you express 'changed by'", 90, RED)]
    ytop = H - 16
    for i, (frag, expl, xf, col) in enumerate(parts):
        yr = ytop - 4.5 - i * 4.6
        ax.plot([xf, xf], [ytop, yr + 1.6], color=col, lw=1.0, ls=":")
        ax.plot([xf], [ytop], "o", ms=3, color=col)
        ax.text(5, yr, frag, fontsize=8.6, color=col, ha="left", fontweight="bold",
                family="monospace")
        ax.text(28, yr, expl, fontsize=8.4, color=BODY, ha="left")
    save(f, "assertion_anatomy")


# ------------------------------------------------- assertions vs scoreboard
def assert_vs_scoreboard():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Assertions and scoreboards catch different things", 12.5)
    ax.text(50, H - 7.4, "Real output from ./scripts/assert.sh in Topic5_Lab.",
            fontsize=8.8, color=SLATE, ha="center")

    cols = ["broken design", "what is wrong", "caught by", "when"]
    rows = [["fifo_b1", "full flag is one entry late", "ASSERTION  a_full_iff_depth", "205 ns"],
            ["fifo_b2", "read not guarded when empty", "ASSERTION  a_count_range", "425 ns"],
            ["fifo_b3", "count drifts on simultaneous r+w", "ASSERTION  a_step_both", "545 ns"],
            ["fifo_b4", "write address wrong after a wrap", "SCOREBOARD only", "456 ns"],
            ["fifo_b5", "write dropped on r+w while empty", "ASSERTION  a_step_up", "465 ns"]]
    cw = [17, 33, 32, 12]
    x0 = 50 - sum(cw) / 2
    y = H - 11
    cx = x0
    for i, c in enumerate(cols):
        ax.add_patch(Rectangle((cx, y - 5.0), cw[i], 5.0, fc=NAVY, ec=NAVY, lw=0.8, zorder=3))
        ax.text(cx + cw[i] / 2, y - 2.5, c, ha="center", va="center", fontsize=8.4,
                color=WHITE, fontweight="bold", zorder=4)
        cx += cw[i]
    yy = y - 5.0
    for r, row in enumerate(rows):
        cx = x0
        sb = "SCOREBOARD" in row[2]
        for i, cell in enumerate(row):
            bg = "#FFF7EC" if sb else (WHITE if r % 2 == 0 else LIGHT)
            ax.add_patch(Rectangle((cx, yy - 5.0), cw[i], 5.0, fc=bg, ec=GRID, lw=0.7, zorder=3))
            tc = BODY
            wt = "normal"
            if i == 0:
                tc, wt = NAVY, "bold"
            if i == 2:
                tc, wt = (AMBER, "bold") if sb else (VIOLET, "bold")
            ax.text(cx + cw[i] / 2, yy - 2.5, cell, ha="center", va="center",
                    fontsize=8.0, color=tc, fontweight=wt, zorder=4,
                    family="monospace" if i == 0 else "sans-serif")
            cx += cw[i]
        yy -= 5.0

    box(ax, x0, yy - 12.5, sum(cw), 10.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, yy - 4.4, "Why b4 slips past every assertion", fontsize=9.4,
            color=AMBER, fontweight="bold", ha="center")
    ax.text(50, yy - 8.4, "The assertions in sva/fifo_sva.sv describe the CONTROL interface — "
                          "count, full, empty. fifo_b4 keeps all of those perfectly correct\n"
                          "and corrupts the DATA. No property is violated, so nothing fires. "
                          "The scoreboard, which compares every word, catches it.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "assert_vs_scoreboard")


if __name__ == "__main__":
    tb_anatomy(); tb_layers(); stimulus_timing(); refmodel(); model_order_bug()
    random_weights(); seed_repro(); cov_bins(); assertion_anatomy()
    assert_vs_scoreboard()
