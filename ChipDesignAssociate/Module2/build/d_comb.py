"""Topic 3B diagrams: combinational logic design."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsl import *
import numpy as np


def comb_vs_seq():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0,
          "The two families of digital logic — the only structural difference is the feedback path",
          13.0, NAVY)
    specs = [
        (2.0, "COMBINATIONAL", TEAL, "#E8F5F7",
         ["Output = f(present inputs) only", "No memory, no clock, no feedback",
          "Same inputs always give the same output", "Analysed with truth tables and K-maps",
          "Adders · MUXes · decoders · comparators · ALUs"]),
        (51.0, "SEQUENTIAL", AMBER, "#FFF6EC",
         ["Output = f(present inputs, present STATE)", "Has memory — it remembers past inputs",
          "Same inputs can give different outputs", "Analysed with state tables and state diagrams",
          "Registers · counters · shift registers · FSMs"]),
    ]
    wd = 47.0
    for k, (x0, nm, c, bg, items) in enumerate(specs):
        box(ax, x0, 3.5, wd, 34.0, fc=bg, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x0, 32.5), wd, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x0, 32.5), wd, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x0 + wd / 2, 35.0, nm, ha="center", va="center", fontsize=11.5,
                color="white", fontweight="bold", zorder=6)

        gy = 26.0
        label_box(ax, x0 + 16.0, gy - 4.0, 15.0, 8.0, "combinational\nlogic\n(gates only)",
                  fc=WHITE, ec=c, tc=NAVY, size=8.4, lw=1.8)
        arrow(ax, x0 + 6.0, gy, x0 + 15.6, gy, color=SLATE, lw=2.0, ms=11)
        arrow(ax, x0 + 31.2, gy, x0 + 40.5, gy, color=SLATE, lw=2.0, ms=11)
        ax.text(x0 + 10.5, gy + 2.4, "inputs", ha="center", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold")
        ax.text(x0 + 36.0, gy + 2.4, "outputs", ha="center", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold")

        if k == 1:
            ry = 18.0
            label_box(ax, x0 + 16.0, ry - 2.6, 15.0, 5.2, "state register",
                      fc=WHITE, ec=RED, tc=RED, size=8.6, lw=1.8)
            # clock triangle on the register
            ax.add_patch(Polygon([(x0 + 16.0, ry - 1.4), (x0 + 17.5, ry - 2.0),
                                  (x0 + 16.0, ry - 2.6)], fc="none", ec=RED, lw=1.4, zorder=6))
            ax.text(x0 + 14.9, ry - 2.0, "clk", ha="right", va="center", fontsize=7.6,
                    color=RED, fontweight="bold")
            # next state: tap the logic output, run down and into the register
            tx = x0 + 34.5
            dot(ax, tx, gy, color=RED)
            wire(ax, [(tx, gy), (tx, ry), (x0 + 31.6, ry)], color=RED, lw=1.8)
            arrow(ax, x0 + 32.4, ry, x0 + 31.1, ry, color=RED, lw=1.8, ms=10)
            ax.text(tx + 0.9, (gy + ry) / 2, "next\nstate", ha="left", va="center",
                    fontsize=7.6, color=RED, fontweight="bold", linespacing=1.3)
            # present state: register output back into the logic
            bx = x0 + 12.6
            wire(ax, [(x0 + 16.0, ry), (bx, ry), (bx, gy - 2.4)], color=RED, lw=1.8)
            arrow(ax, bx, gy - 2.4, x0 + 15.7, gy - 2.4, color=RED, lw=1.8, ms=10)
            ax.text(bx - 0.7, (gy + ry) / 2, "present\nstate", ha="right", va="center",
                    fontsize=7.6, color=RED, fontweight="bold", linespacing=1.3)
            ax.text(x0 + wd / 2, 13.9, "the red loop is the memory", ha="center", va="center",
                    fontsize=9.0, color=RED, fontweight="bold")
        else:
            ax.text(x0 + wd / 2, 19.0, "no path returns to the input", ha="center",
                    va="center", fontsize=9.0, color=TEAL, fontweight="bold")
            ax.text(x0 + wd / 2, 15.8, "output settles a fixed delay after the input changes",
                    ha="center", va="center", fontsize=8.2, color=SLATE, style="italic")

        for j, it in enumerate(items):
            ax.text(x0 + 2.0, 12.4 - j * 1.88, "·  " + it, ha="left", va="center",
                    fontsize=8.4, color=BODY)
    save(f, "comb_vs_seq")


def comb_design_flow():
    W, Hin = 13, 4.4
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 33.85
    title(ax, 50, H - 2.0, "The seven-step procedure for designing any combinational circuit",
          13.0, NAVY)
    steps = [("1", "State the\nproblem", "in plain words", TEAL),
             ("2", "Name inputs\n& outputs", "and their widths", TEAL),
             ("3", "Build the\ntruth table", "every input combo", TEAL),
             ("4", "Write the\nBoolean form", "canonical SOP/POS", AMBER),
             ("5", "Minimise", "K-map or Q\u2013M", AMBER),
             ("6", "Draw the\ngate circuit", "map to real cells", GREEN),
             ("7", "Verify", "simulate all cases", GREEN)]
    bw, gap = 12.6, 1.9
    x0 = (100 - (7 * bw + 6 * gap)) / 2
    by, bh = 12.5, 13.5
    for i, (n, head, sub, c) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, by, bw, bh, fc=WHITE, ec=c, lw=1.8)
        ax.add_patch(Circle((x + bw / 2, by + bh - 2.6), 1.75, fc=c, ec=c, zorder=4))
        ax.text(x + bw / 2, by + bh - 2.6, n, ha="center", va="center", fontsize=9.5,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + bw / 2, by + bh - 7.4, head, ha="center", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold", linespacing=1.4)
        ax.text(x + bw / 2, by + 2.2, sub, ha="center", va="center", fontsize=6.8,
                color=SLATE, linespacing=1.3)
        if i < 6:
            arrow(ax, x + bw + 0.25, by + bh / 2, x + bw + gap - 0.25, by + bh / 2,
                  color=SLATE, lw=1.8, ms=9)
    # iteration arrow
    arrow(ax, x0 + 6 * (bw + gap) + bw / 2, by - 1.2, x0 + 3.5 * (bw + gap), by - 1.2,
          color=RED, lw=1.8, ms=10, rad=-0.16)
    ax.text(x0 + 4.9 * (bw + gap), by - 6.0, "if verification fails, go back and fix the table or the minimisation",
            ha="center", va="center", fontsize=8.6, color=RED, fontweight="bold")
    ax.add_patch(FancyBboxPatch((x0, 26.6), 7 * bw + 6 * gap, 3.4,
                 boxstyle="round,pad=0,rounding_size=0.9", fc=LIGHT, ec=TEAL, lw=1.4, zorder=2))
    ax.text(50, 28.3, "Steps 1–3 are SPECIFICATION  ·  steps 4–5 are OPTIMISATION  ·  steps 6–7 are IMPLEMENTATION & SIGN-OFF",
            ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="bold", zorder=4)
    ax.text(50, 2.4, "In an RTL flow you write steps 1–2 as a Verilog module header and step 3–6 as one always/assign block — "
            "the synthesiser performs steps 4–6 for you. Step 7 never goes away.",
            ha="center", va="center", fontsize=9.0, color=BODY, style="italic")
    save(f, "comb_design_flow")


def adders():
    W, Hin = 13, 5.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 44.62
    title(ax, 50, H - 2.0, "Half adder and full adder — the atoms of every arithmetic unit", 13.0, NAVY)

    # ---------------- HALF ADDER ----------------
    box(ax, 2.0, 3.5, 46.0, 36.0, fc="#E8F5F7", ec=TEAL, lw=1.8)
    ax.add_patch(FancyBboxPatch((2.0, 34.5), 46.0, 5.0, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=TEAL, ec=TEAL, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((2.0, 34.5), 46.0, 2.5, fc=TEAL, ec=TEAL, lw=0, zorder=4))
    ax.text(25.0, 37.0, "HALF ADDER — adds two bits", ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=6)
    xi, ys, yc = 14.0, 27.5, 21.0
    i1, o1 = gate(ax, "XOR", xi, ys, 6.6, 6.0, ec=GREEN, stub=2.2, fc=WHITE)
    i2, o2 = gate(ax, "AND", xi, yc, 6.6, 6.0, ec=AMBER, stub=2.2, fc=WHITE)
    ax.text(5.4, 30.6, "A", ha="right", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    ax.text(5.4, 17.8, "B", ha="right", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    wire(ax, [(6.0, 30.6), (8.2, 30.6), (8.2, i1[0][1])], color=INK)
    wire(ax, [(8.2, i1[0][1]), i1[0]], color=INK)
    wire(ax, [(8.2, i1[0][1]), (8.2, i2[0][1]), i2[0]], color=INK)
    dot(ax, 8.2, i1[0][1]); dot(ax, 8.2, i2[0][1])
    wire(ax, [(6.0, 17.8), (10.2, 17.8), (10.2, i2[1][1])], color=INK)
    wire(ax, [(10.2, i2[1][1]), i2[1]], color=INK)
    wire(ax, [(10.2, i2[1][1]), (10.2, i1[1][1]), i1[1]], color=INK)
    dot(ax, 10.2, i1[1][1]); dot(ax, 10.2, i2[1][1])
    ax.text(o1[0] + 0.8, o1[1], "S  =  A ⊕ B", ha="left", va="center", fontsize=10,
            color=GREEN, fontweight="bold")
    ax.text(o2[0] + 0.8, o2[1], "C  =  A · B", ha="left", va="center", fontsize=10,
            color=AMBER, fontweight="bold")
    table(ax, 4.5, 16.5, ["A", "B", "S", "C"],
          [["0", "0", "0", "0"], ["0", "1", "1", "0"], ["1", "0", "1", "0"], ["1", "1", "0", "1"]],
          [5.5, 5.5, 5.5, 5.5], 2.4, size=8.6, head_fc=NAVY, bold_col=[2, 3])
    ax.add_patch(FancyBboxPatch((28.5, 5.0), 18.0, 10.5, boxstyle="round,pad=0,rounding_size=1.0",
                 fc=WHITE, ec=TEAL, lw=1.4, zorder=2))
    ax.text(37.5, 13.4, "Limitation", ha="center", va="center", fontsize=9.0,
            color=TEAL, fontweight="bold", zorder=4)
    ax.text(37.5, 9.0, "It has no carry INPUT,\nso it can only be used\nfor the least-significant\nbit of an adder.",
            ha="center", va="center", fontsize=8.0, color=BODY, zorder=4, linespacing=1.5)

    # ---------------- FULL ADDER ----------------
    box(ax, 52.0, 3.5, 46.0, 36.0, fc="#FFF6EC", ec=AMBER, lw=1.8)
    ax.add_patch(FancyBboxPatch((52.0, 34.5), 46.0, 5.0, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=AMBER, ec=AMBER, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((52.0, 34.5), 46.0, 2.5, fc=AMBER, ec=AMBER, lw=0, zorder=4))
    ax.text(75.0, 37.0, "FULL ADDER — adds three bits", ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=6)
    for lab, yA, c in [("A", 31.4, NAVY), ("B", 28.4, NAVY), ("C$_{in}$", 25.4, RED)]:
        ax.text(56.4, yA, lab, ha="right", va="center", fontsize=10, color=c, fontweight="bold")
        wire(ax, [(57.0, yA), (59.0, yA)], color=INK)
    label_box(ax, 59.0, 23.5, 13.0, 10.0, "FULL\nADDER", fc=WHITE, ec=AMBER, tc=NAVY,
              size=10, lw=2.0)
    wire(ax, [(72.0, 30.2), (74.4, 30.2)], color=INK)
    wire(ax, [(72.0, 26.8), (74.4, 26.8)], color=INK)
    ax.text(75.0, 30.2, "S", ha="left", va="center", fontsize=10.5, color=GREEN, fontweight="bold")
    ax.text(75.0, 26.8, "C$_{out}$", ha="left", va="center", fontsize=10.5, color=RED, fontweight="bold")
    ax.text(75.0, 21.4, "S = A ⊕ B ⊕ C$_{in}$          C$_{out}$ = AB + C$_{in}$(A ⊕ B)",
            ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="bold")
    fa = []
    for a in range(2):
        for b in range(2):
            for ci in range(2):
                fa.append([str(a), str(b), str(ci), str(a ^ b ^ ci),
                           "1" if (a + b + ci) >= 2 else "0"])
    table(ax, 54.0, 19.3, ["A", "B", "C$_{in}$", "S", "C$_{out}$"], fa,
          [5.5, 5.5, 6.5, 5.5, 6.5], 1.68, size=7.8, head_fc=NAVY, bold_col=[3, 4])
    ax.add_patch(FancyBboxPatch((85.5, 5.6), 11.5, 13.7, boxstyle="round,pad=0,rounding_size=1.0",
                 fc=WHITE, ec=AMBER, lw=1.4, zorder=2))
    ax.text(91.25, 17.4, "Built from", ha="center", va="center", fontsize=8.2,
            color=AMBER, fontweight="bold", zorder=4)
    ax.text(91.25, 12.4, "2 half adders\n+\n1 OR gate",
            ha="center", va="center", fontsize=7.8, color=NAVY, fontweight="bold",
            zorder=4, linespacing=1.6)
    ax.text(91.25, 7.8, "this is the cell\nthat tiles into\nan n-bit adder",
            ha="center", va="center", fontsize=7.0, color=BODY, zorder=4, linespacing=1.4)
    save(f, "adders")


def ripple_adder():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 36.92
    title(ax, 50, H - 2.0, "4-bit ripple-carry adder — correct, compact, and slow by construction",
          13.0, NAVY)
    bw, bh = 15.0, 10.0
    gapx = 5.0
    x0 = 8.0
    cy = 17.0
    for i in range(4):
        x = x0 + (3 - i) * (bw + gapx)
        label_box(ax, x, cy, bw, bh, "FA%d" % i, fc=WHITE, ec=AMBER, tc=NAVY, size=10.5, lw=1.9)
        ax.text(x + bw / 2, cy + bh + 4.4, "A$_%d$   B$_%d$" % (i, i), ha="center", va="center",
                fontsize=9.6, color=NAVY, fontweight="bold")
        wire(ax, [(x + bw * 0.30, cy + bh + 3.0), (x + bw * 0.30, cy + bh)], color=INK)
        wire(ax, [(x + bw * 0.70, cy + bh + 3.0), (x + bw * 0.70, cy + bh)], color=INK)
        wire(ax, [(x + bw / 2, cy), (x + bw / 2, cy - 3.2)], color=INK)
        ax.text(x + bw / 2, cy - 4.8, "S$_%d$" % i, ha="center", va="center", fontsize=10,
                color=GREEN, fontweight="bold")
        if i < 3:
            arrow(ax, x - 0.3, cy + bh / 2, x - gapx + 0.3, cy + bh / 2, color=RED, lw=2.0, ms=10)
            ax.text(x - gapx / 2, cy + bh / 2 + 2.2, "C$_%d$" % (i + 1), ha="center",
                    va="center", fontsize=8.8, color=RED, fontweight="bold")
    # carry in / carry out
    xr = x0 + 3 * (bw + gapx)
    wire(ax, [(xr + bw + 3.6, cy + bh / 2), (xr + bw, cy + bh / 2)], color=RED, lw=2.0)
    arrow(ax, xr + bw + 1.2, cy + bh / 2, xr + bw - 0.2, cy + bh / 2, color=RED, lw=2.0, ms=10)
    ax.text(xr + bw + 4.2, cy + bh / 2, "C$_{in}$ = 0", ha="left", va="center", fontsize=9.2,
            color=RED, fontweight="bold")
    arrow(ax, x0, cy + bh / 2, x0 - 4.4, cy + bh / 2, color=RED, lw=2.0, ms=10)
    ax.text(x0 - 5.0, cy + bh / 2, "C$_{out}$", ha="right", va="center", fontsize=9.6,
            color=RED, fontweight="bold")

    ax.add_patch(FancyBboxPatch((3.0, 2.0), 60.0, 8.0, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#FDECEF", ec=RED, lw=1.7, zorder=2))
    ax.text(5.5, 8.0, "The problem: the carry must RIPPLE", ha="left", va="center",
            fontsize=10, color=RED, fontweight="bold", zorder=4)
    ax.text(5.5, 4.4, "FA3 cannot produce a correct sum until C$_3$ is valid, which needs C$_2$, which needs C$_1$…\n"
            "Worst-case delay grows LINEARLY with the number of bits:   t$_{RCA}$ ≈ n × t$_{carry}$",
            ha="left", va="center", fontsize=8.6, color=BODY, zorder=4, linespacing=1.6)
    ax.add_patch(FancyBboxPatch((66.0, 2.0), 31.0, 8.0, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#E4F4EC", ec=GREEN, lw=1.7, zorder=2))
    ax.text(81.5, 8.0, "The fix: carry-lookahead", ha="center", va="center", fontsize=10,
            color=GREEN, fontweight="bold", zorder=4)
    ax.text(81.5, 4.4, "Compute  G$_i$ = A$_i$B$_i$,  P$_i$ = A$_i$ ⊕ B$_i$  for all bits\n"
            "at once → delay grows as log n, at the cost of area.",
            ha="center", va="center", fontsize=8.2, color=BODY, zorder=4, linespacing=1.6)
    save(f, "ripple_adder")


def mux_demux():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 40.0
    title(ax, 50, H - 2.0, "Multiplexer and de-multiplexer — the data-routing pair", 13.0, NAVY)
    ty, th_, tw_ = 13.5, 15.0, 10.0

    # ---- 4:1 MUX ----
    box(ax, 2.0, 3.0, 45.0, 31.5, fc="#E8F5F7", ec=TEAL, lw=1.8)
    ax.text(24.5, 32.4, "4-to-1 MULTIPLEXER  —  many in, one out", ha="center", va="center",
            fontsize=10.5, color=TEAL, fontweight="bold")
    tx = 13.0
    ax.add_patch(Polygon([(tx, ty + th_), (tx + tw_, ty + th_ - 3.4),
                          (tx + tw_, ty + 3.4), (tx, ty)], fc=WHITE, ec=TEAL, lw=2.0, zorder=3))
    for i in range(4):
        yy = 26.6 - i * 3.6
        wire(ax, [(tx - 4.0, yy), (tx, yy)], color=INK)
        ax.text(tx - 4.6, yy, "I$_%d$" % i, ha="right", va="center", fontsize=9.4,
                color=NAVY, fontweight="bold")
        ax.text(tx + 1.4, yy, "%d" % i, ha="left", va="center", fontsize=7.4, color=SLATE, zorder=5)
    wire(ax, [(tx + tw_, ty + th_ / 2), (tx + tw_ + 4.0, ty + th_ / 2)], color=INK)
    ax.text(tx + tw_ + 4.6, ty + th_ / 2, "Y", ha="left", va="center", fontsize=10.5,
            color=GREEN, fontweight="bold")
    wire(ax, [(tx + tw_ / 2, ty), (tx + tw_ / 2, ty - 3.0)], color=AMBER, lw=1.8)
    ax.text(tx + tw_ / 2, ty - 4.6, "S$_1$ S$_0$   (select)", ha="center", va="center",
            fontsize=9.2, color=AMBER, fontweight="bold")
    table(ax, 31.0, 29.5, ["S$_1$", "S$_0$", "Y"],
          [["0", "0", "I$_0$"], ["0", "1", "I$_1$"], ["1", "0", "I$_2$"], ["1", "1", "I$_3$"]],
          [4.2, 4.2, 5.4], 2.6, size=8.4, head_fc=NAVY, bold_col=[2], colcolors={2: GREEN})
    ax.text(37.9, 13.4, "Y = S$_1$'S$_0$'I$_0$ + S$_1$'S$_0$I$_1$\n      + S$_1$S$_0$'I$_2$ + S$_1$S$_0$I$_3$",
            ha="center", va="center", fontsize=7.4, color=BODY, linespacing=1.7)
    ax.text(24.5, 5.6, "n select lines choose one of 2$^n$ inputs", ha="center", va="center",
            fontsize=9.0, color=NAVY, fontweight="bold")

    # ---- 1:4 DEMUX ----
    box(ax, 53.0, 3.0, 45.0, 31.5, fc="#FFF6EC", ec=AMBER, lw=1.8)
    ax.text(75.5, 32.4, "1-to-4 DE-MULTIPLEXER  —  one in, many out", ha="center", va="center",
            fontsize=10.5, color=AMBER, fontweight="bold")
    tx2 = 68.0
    ax.add_patch(Polygon([(tx2 + tw_, ty + th_), (tx2, ty + th_ - 3.4),
                          (tx2, ty + 3.4), (tx2 + tw_, ty)], fc=WHITE, ec=AMBER, lw=2.0, zorder=3))
    wire(ax, [(tx2 - 4.0, ty + th_ / 2), (tx2, ty + th_ / 2)], color=INK)
    ax.text(tx2 - 4.6, ty + th_ / 2, "D", ha="right", va="center", fontsize=10.5,
            color=NAVY, fontweight="bold")
    for i in range(4):
        yy = 26.6 - i * 3.6
        wire(ax, [(tx2 + tw_, yy), (tx2 + tw_ + 4.0, yy)], color=INK)
        ax.text(tx2 + tw_ + 4.6, yy, "Y$_%d$" % i, ha="left", va="center", fontsize=9.4,
                color=GREEN, fontweight="bold")
    wire(ax, [(tx2 + tw_ / 2, ty), (tx2 + tw_ / 2, ty - 3.0)], color=AMBER, lw=1.8)
    ax.text(tx2 + tw_ / 2, ty - 4.6, "S$_1$ S$_0$   (select)", ha="center", va="center",
            fontsize=9.2, color=AMBER, fontweight="bold")
    ax.text(75.5, 6.8, "The selected output receives D; every other output is driven to 0.",
            ha="center", va="center", fontsize=8.2, color=BODY)
    ax.text(75.5, 4.2, "A decoder is simply a de-multiplexer with D tied to 1",
            ha="center", va="center", fontsize=9.0, color=NAVY, fontweight="bold")
    save(f, "mux_demux")


def decoder_encoder():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Decoders and encoders — converting between binary codes and one-hot lines",
          13.0, NAVY)
    # ---------------- decoder ----------------
    box(ax, 2.0, 3.0, 45.0, 34.5, fc="#E8F5F7", ec=TEAL, lw=1.8)
    ax.text(24.5, 35.6, "2-to-4 DECODER  ·  binary code → one-hot", ha="center", va="center",
            fontsize=10.5, color=TEAL, fontweight="bold")
    label_box(ax, 15.0, 22.0, 13.0, 12.0, "2:4\nDEC", fc=WHITE, ec=TEAL, tc=NAVY, size=10, lw=2.0)
    for i, lab in enumerate(["A$_1$", "A$_0$"]):
        yy = 30.5 - i * 4.6
        wire(ax, [(10.0, yy), (15.0, yy)], color=INK)
        ax.text(9.4, yy, lab, ha="right", va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    for i in range(4):
        yy = 31.6 - i * 3.0
        wire(ax, [(28.0, yy), (31.6, yy)], color=INK)
        ax.text(32.2, yy, "D$_%d$" % i, ha="left", va="center", fontsize=9.4,
                color=GREEN, fontweight="bold")
    table(ax, 5.0, 19.5, ["A$_1$", "A$_0$", "D$_3$ D$_2$ D$_1$ D$_0$"],
          [["0", "0", "0  0  0  1"], ["0", "1", "0  0  1  0"],
           ["1", "0", "0  1  0  0"], ["1", "1", "1  0  0  0"]],
          [7.0, 7.0, 15.0], 2.5, size=8.4, head_fc=NAVY, bold_col=[2], colcolors={2: GREEN})
    ax.text(24.5, 5.0, "Exactly ONE output is high at a time — this is how a CPU turns an address\n"
            "into a memory chip-select, and an opcode into a control line.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.5)

    # ---------------- priority encoder ----------------
    box(ax, 53.0, 3.0, 45.0, 34.5, fc="#FFF6EC", ec=AMBER, lw=1.8)
    ax.text(75.5, 35.6, "4-to-2 PRIORITY ENCODER  ·  one-hot → binary code", ha="center",
            va="center", fontsize=10.5, color=AMBER, fontweight="bold")
    label_box(ax, 66.0, 22.0, 13.0, 12.0, "4:2\nPRIORITY\nENCODER", fc=WHITE, ec=AMBER,
              tc=NAVY, size=8.0, lw=2.0)
    for i in range(4):
        yy = 31.6 - i * 3.0
        wire(ax, [(61.4, yy), (66.0, yy)], color=INK)
        ax.text(60.8, yy, "I$_%d$" % i, ha="right", va="center", fontsize=9.2,
                color=NAVY, fontweight="bold")
    for i, (lab, c) in enumerate([("Y$_1$", GREEN), ("Y$_0$", GREEN), ("V", RED)]):
        yy = 31.0 - i * 4.0
        wire(ax, [(79.0, yy), (82.4, yy)], color=INK)
        ax.text(83.0, yy, lab, ha="left", va="center", fontsize=9.4, color=c, fontweight="bold")
    table(ax, 56.0, 19.5, ["I$_3$ I$_2$ I$_1$ I$_0$", "Y$_1$", "Y$_0$", "V"],
          [["0  0  0  0", "x", "x", "0"], ["0  0  0  1", "0", "0", "1"],
           ["0  0  1  x", "0", "1", "1"], ["0  1  x  x", "1", "0", "1"],
           ["1  x  x  x", "1", "1", "1"]],
          [14.0, 6.0, 6.0, 6.0], 2.2, size=8.0, head_fc=NAVY, bold_col=[1, 2])
    ax.text(75.5, 4.3, "'Priority' resolves several simultaneous 1s — the highest index wins.\n"
            "V (valid) distinguishes 'input 0 active' from 'no input active'.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.5)
    save(f, "decoder_encoder")


def comparator_parity():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 36.92
    title(ax, 50, H - 2.0, "Two more standard blocks you will meet in every datapath", 13.0, NAVY)
    # comparator
    box(ax, 2.0, 3.0, 45.0, 30.0, fc="#E8F5F7", ec=TEAL, lw=1.8)
    ax.text(24.5, 30.6, "MAGNITUDE COMPARATOR", ha="center", va="center", fontsize=10.5,
            color=TEAL, fontweight="bold")
    label_box(ax, 15.0, 12.5, 14.0, 13.0, "n-bit\nCOMP", fc=WHITE, ec=TEAL, tc=NAVY, size=10, lw=2.0)
    for i, lab in enumerate(["A", "B"]):
        yy = 22.0 - i * 4.4
        wire(ax, [(10.0, yy), (15.0, yy)], color=INK)
        ax.text(9.4, yy, lab, ha="right", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
    for i, (lab, c) in enumerate([("A > B", GREEN), ("A = B", AMBER), ("A < B", RED)]):
        yy = 23.0 - i * 4.0
        wire(ax, [(29.0, yy), (32.0, yy)], color=INK)
        ax.text(32.6, yy, lab, ha="left", va="center", fontsize=9.4, color=c, fontweight="bold")
    ax.text(24.5, 8.6, "1-bit equality:   A = B  ⇔  (A ⊕ B)' = 1", ha="center", va="center",
            fontsize=9.0, color=NAVY, fontweight="bold")
    ax.text(24.5, 5.6, "n-bit equality ANDs together n XNOR outputs. Magnitude compare works\n"
            "MSB-first: the first differing bit decides the result.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.5)

    # parity
    box(ax, 53.0, 3.0, 45.0, 30.0, fc="#FFF6EC", ec=AMBER, lw=1.8)
    ax.text(75.5, 30.6, "PARITY GENERATOR / CHECKER", ha="center", va="center", fontsize=10.5,
            color=AMBER, fontweight="bold")
    i1, o1 = gate(ax, "XOR", 64.0, 24.0, 6.0, 5.4, ec=GREEN, stub=2.0, fc=WHITE)
    i2, o2 = gate(ax, "XOR", 64.0, 16.0, 6.0, 5.4, ec=GREEN, stub=2.0, fc=WHITE)
    i3, o3 = gate(ax, "XOR", 76.0, 20.0, 6.0, 5.4, ec=GREEN, stub=2.0, fc=WHITE)
    for p, lab in zip(i1 + i2, ["D$_0$", "D$_1$", "D$_2$", "D$_3$"]):
        ax.text(p[0] - 0.6, p[1], lab, ha="right", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold")
    wire(ax, [o1, (o1[0] + 1.2, o1[1]), (o1[0] + 1.2, i3[0][1]), i3[0]], color=INK)
    wire(ax, [o2, (o2[0] + 1.2, o2[1]), (o2[0] + 1.2, i3[1][1]), i3[1]], color=INK)
    ax.text(o3[0] + 0.8, o3[1], "P", ha="left", va="center", fontsize=10.5,
            color=GREEN, fontweight="bold")
    ax.text(75.5, 10.2, "P = D$_0$ ⊕ D$_1$ ⊕ D$_2$ ⊕ D$_3$   (EVEN parity)", ha="center",
            va="center", fontsize=9.0, color=NAVY, fontweight="bold")
    ax.text(75.5, 6.4, "XOR of all bits = 1 when the number of 1s is odd. Send P alongside the data;\n"
            "the receiver re-computes it. A mismatch means at least one bit flipped in transit.",
            ha="center", va="center", fontsize=7.8, color=BODY, linespacing=1.5)
    save(f, "comparator_parity")


def alu_block():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 35.38
    title(ax, 50, H - 2.0, "An ALU is just combinational blocks sharing one multiplexer", 13.0, NAVY)
    # functional units
    units = [("ADDER / SUBTRACTOR", GREEN, 27.0), ("AND  unit", TEAL, 21.4),
             ("OR  unit", TEAL, 15.8), ("SHIFTER", AMBER, 10.2)]
    for nm, c, yy in units:
        label_box(ax, 22.0, yy - 2.2, 20.0, 4.4, nm, fc=WHITE, ec=c, tc=NAVY, size=8.4, lw=1.6)
        wire(ax, [(42.0, yy), (52.0, yy)], color=SLATE, lw=1.5)
        arrow(ax, 50.0, yy, 52.2, yy, color=SLATE, lw=1.5, ms=8)
    # A / B buses
    for lab, yy in [("A  [n-1:0]", 30.0), ("B  [n-1:0]", 6.6)]:
        ax.text(4.0, yy, lab, ha="left", va="center", fontsize=9.4, color=NAVY, fontweight="bold")
    wire(ax, [(15.0, 30.0), (15.0, 6.6)], color=INK, lw=1.8)
    wire(ax, [(12.6, 30.0), (15.0, 30.0)], color=INK, lw=1.8)
    wire(ax, [(12.6, 6.6), (15.0, 6.6)], color=INK, lw=1.8)
    for nm, c, yy in units:
        wire(ax, [(15.0, yy), (22.0, yy)], color=INK, lw=1.4)
        dot(ax, 15.0, yy)
    # MUX
    ax.add_patch(Polygon([(52.5, 30.5), (58.5, 27.0), (58.5, 9.0), (52.5, 5.5)],
                         fc=WHITE, ec=NAVY, lw=2.0, zorder=3))
    ax.text(55.5, 18.0, "M\nU\nX", ha="center", va="center", fontsize=9.5, color=NAVY,
            fontweight="bold", zorder=5, linespacing=1.4)
    wire(ax, [(58.5, 18.0), (71.0, 18.0)], color=INK, lw=1.8)
    ax.text(64.5, 19.8, "Result", ha="center", va="center", fontsize=10.5,
            color=GREEN, fontweight="bold")
    wire(ax, [(55.5, 5.5), (55.5, 2.6)], color=AMBER, lw=1.8)
    ax.text(55.5, 1.2, "opcode  (function select)", ha="center", va="center", fontsize=8.6,
            color=AMBER, fontweight="bold")
    # flags
    box(ax, 76.0, 12.0, 22.0, 18.5, fc=LIGHT, ec=RED, lw=1.7)
    ax.text(87.0, 28.4, "STATUS FLAGS", ha="center", va="center", fontsize=9.6,
            color=RED, fontweight="bold")
    for j, (fl, mean) in enumerate([("Z", "result is zero"), ("N", "result is negative"),
                                    ("C", "carry / borrow out"), ("V", "signed overflow")]):
        ax.text(78.2, 25.0 - j * 3.4, fl, ha="left", va="center", fontsize=9.4,
                color=RED, fontweight="bold")
        ax.text(81.4, 25.0 - j * 3.4, mean, ha="left", va="center", fontsize=8.0, color=BODY)
    arrow(ax, 71.0, 18.0, 75.6, 18.0, color=SLATE, lw=1.5, ms=9)
    dot(ax, 71.0, 18.0)
    ax.text(87.0, 8.6, "Every unit computes in parallel;\nthe opcode simply picks which\nanswer leaves the block.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.5)
    save(f, "alu_block")


def hazards():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Glitches and hazards — when correct logic still produces a wrong pulse",
          13.0, NAVY)
    # ---------- timing panel ----------
    box(ax, 2.0, 10.0, 52.0, 28.0, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(28.0, 36.8, "F = AB' + BC     with A = C = 1 and B falling 1 → 0", ha="center",
            va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    u, x0, ww = 5.2, 15.0, 4.3
    gx = x0 + 4 * ww
    ax.add_patch(Rectangle((gx, 14.0), ww, 20.0, fc=RED, alpha=0.10, ec="none", zorder=1))
    wave(ax, x0, 30.6, ww, [1, 1, 1, 1, 0, 0, 0, 0], u, color=NAVY, name="B", name_size=9.4)
    wave(ax, x0, 25.6, ww, [1, 1, 1, 1, 0, 0, 0, 0], u, color=TEAL, name="BC", name_size=9.4)
    wave(ax, x0, 20.6, ww, [0, 0, 0, 0, 0, 1, 1, 1], u, color=AMBER, name="AB'", name_size=9.4)
    wave(ax, x0, 15.0, ww, [1, 1, 1, 1, 0, 1, 1, 1], u, color=RED, name="F", name_size=9.4)
    ax.text(gx + ww / 2, 34.6, "GLITCH", ha="center", va="center", fontsize=8.6,
            color=RED, fontweight="bold")
    ax.text(28.0, 12.0, "BC falls one gate-delay BEFORE AB' rises — for that window neither term holds F high.",
            ha="center", va="center", fontsize=8.2, color=BODY)
    ax.add_patch(FancyBboxPatch((2.0, 2.0), 52.0, 6.6, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#FDECEF", ec=RED, lw=1.5, zorder=2))
    ax.text(28.0, 5.3, "Glitches burn power, and they BREAK asynchronous logic — a glitch on a clock\n"
            "or reset line is fatal. This is a major reason industry designs synchronously.",
            ha="center", va="center", fontsize=8.2, color=BODY, zorder=4, linespacing=1.6)

    # ---------- taxonomy ----------
    box(ax, 57.0, 22.0, 41.0, 16.0, fc=LIGHT, ec=TEAL, lw=1.7)
    ax.text(59.2, 35.8, "Three kinds of hazard", ha="left", va="center", fontsize=10,
            color=TEAL, fontweight="bold")
    for j, (nm, d) in enumerate([("Static-1", "should stay 1, but dips to 0"),
                                 ("Static-0", "should stay 0, but spikes to 1"),
                                 ("Dynamic", "one transition that bounces 0→1→0→1")]):
        yy = 32.6 - j * 3.4
        ax.text(59.2, yy, nm, ha="left", va="center", fontsize=9.2, color=NAVY, fontweight="bold")
        ax.text(69.4, yy, d, ha="left", va="center", fontsize=8.0, color=BODY)
    ax.text(59.2, 24.0, "Root cause: two paths to the same output with unequal delay.",
            ha="left", va="center", fontsize=8.2, color=SLATE, style="italic")

    # ---------- fixes ----------
    box(ax, 57.0, 2.0, 41.0, 19.0, fc="#E4F4EC", ec=GREEN, lw=1.7)
    ax.text(77.5, 19.2, "Two ways to deal with it", ha="center", va="center", fontsize=10,
            color=GREEN, fontweight="bold")
    ax.text(59.2, 15.6, "1.   Add a redundant (consensus) term", ha="left", va="center",
            fontsize=9.2, color=NAVY, fontweight="bold")
    ax.text(59.2, 12.0, "F = AB' + BC + AC.  The extra AC group bridges the two\n"
            "K-map groups, so F is held high through the transition.\n"
            "It costs area and is logically redundant — but necessary.",
            ha="left", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    ax.text(59.2, 7.8, "2.   Or simply clock it", ha="left", va="center",
            fontsize=9.2, color=NAVY, fontweight="bold")
    ax.text(59.2, 4.8, "In a synchronous design the glitch settles long before the\n"
            "next clock edge, so no register ever samples it.",
            ha="left", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    save(f, "hazards")


def delay_fanout():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 35.38
    title(ax, 50, H - 2.0, "What actually limits speed — propagation delay, fan-in and fan-out",
          13.0, NAVY)
    # prop delay
    box(ax, 2.0, 3.0, 44.0, 28.5, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(24.0, 29.4, "PROPAGATION DELAY of one gate", ha="center", va="center",
            fontsize=10, color=NAVY, fontweight="bold")
    u, x0, ww = 5.0, 12.0, 3.6
    wave(ax, x0, 21.0, ww, [0, 0, 1, 1, 1, 1, 1, 1], u, color=NAVY, name="in", name_size=9.4)
    wave(ax, x0, 13.0, ww, [0, 0, 0, 1, 1, 1, 1, 1], u, color=TEAL, name="out", name_size=9.4)
    ax.plot([x0 + 2 * ww, x0 + 2 * ww], [12.2, 24.6], color=RED, lw=1.1, ls=(0, (3, 3)), zorder=5)
    ax.plot([x0 + 3 * ww, x0 + 3 * ww], [12.2, 24.6], color=RED, lw=1.1, ls=(0, (3, 3)), zorder=5)
    arrow(ax, x0 + 2 * ww, 25.4, x0 + 3 * ww, 25.4, color=RED, lw=1.5, ms=8, style="<|-|>")
    ax.text(x0 + 2.5 * ww, 27.0, "t$_{pd}$", ha="center", va="center", fontsize=10,
            color=RED, fontweight="bold")
    ax.text(24.0, 9.0, "t$_{pd}$ is measured at the 50 % points. It depends on the cell,\n"
            "the supply voltage, the temperature and — critically — the LOAD.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.5)
    ax.text(24.0, 5.0, "Path delay = the sum of t$_{pd}$ along the slowest route",
            ha="center", va="center", fontsize=9.0, color=NAVY, fontweight="bold")

    # fan-out
    box(ax, 49.0, 3.0, 49.0, 28.5, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(73.5, 29.4, "FAN-OUT — every extra load slows the driver", ha="center",
            va="center", fontsize=10, color=NAVY, fontweight="bold")
    _, od = gate(ax, "NOT", 55.0, 20.0, 5.4, 5.4, ec=TEAL, stub=2.0, nin=1, fc=WHITE)
    ax.text(52.6, 20.0, "A", ha="right", va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    hub = od[0] + 2.0
    wire(ax, [od, (hub, 20.0)], color=INK)
    for i in range(4):
        yy = 26.9 - i * 4.6
        wire(ax, [(hub, 20.0), (hub, yy), (hub + 3.0, yy)], color=INK)
        gate(ax, "BUF", hub + 3.0, yy, 4.2, 3.4, ec=SLATE, stub=1.3, nin=1, fc=WHITE)
    dot(ax, hub, 20.0)
    ax.text(hub + 12.0, 20.0, "4 loads", ha="left", va="center", fontsize=9.2,
            color=SLATE, fontweight="bold")
    ax.add_patch(FancyBboxPatch((80.0, 12.0), 16.5, 16.0, boxstyle="round,pad=0,rounding_size=1.0",
                 fc=LIGHT, ec=AMBER, lw=1.5, zorder=2))
    ax.text(88.2, 26.2, "rule of thumb", ha="center", va="center", fontsize=8.6,
            color=AMBER, fontweight="bold", zorder=4)
    ax.text(88.2, 20.0, "t$_{pd}$  ≈\n\nt$_{intrinsic}$ + k · C$_{load}$",
            ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="bold",
            zorder=4, linespacing=1.5)
    ax.text(88.2, 14.4, "double the loads,\nroughly double the\nload-dependent part",
            ha="center", va="center", fontsize=7.4, color=BODY, zorder=4, linespacing=1.4)
    ax.text(73.5, 8.4, "FAN-IN is the other half: a 6-input AND is slower than a tree of 2-input ANDs.\n"
            "Synthesis tools fix both automatically — by BUFFERING (adding repeaters) and by RESTRUCTURING logic.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    save(f, "delay_fanout")


if __name__ == "__main__":
    comb_vs_seq(); comb_design_flow(); adders(); ripple_adder()
    mux_demux(); decoder_encoder(); comparator_parity(); alu_block()
    hazards(); delay_fanout()
