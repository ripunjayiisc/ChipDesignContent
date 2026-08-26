"""Topic 3A diagrams: Boolean algebra and logic gates."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsl import *
import numpy as np


def digital_abstraction():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 40.0
    title(ax, 50, H - 2.0, "The digital abstraction — a continuous voltage read as one of two symbols",
          13.5, NAVY)
    py, ph = 9.5, 22.0
    # ---- left: analog reality ----
    x0, w = 3, 36
    ax.add_patch(Rectangle((x0, py), w, ph, fc=LIGHT, ec=GRID, lw=1.2, zorder=1))
    t = np.linspace(0, 4 * np.pi, 500)
    v = 1.65 + 1.42 * np.sin(t) + 0.09 * np.sin(7 * t) + 0.05 * np.sin(19 * t)
    ax.plot(x0 + 1.5 + (w - 3) * t / t.max(), py + 1.5 + (ph - 3) * v / 3.3,
            color=AMBER, lw=1.7, zorder=4)
    title(ax, x0 + w / 2, py + ph + 2.6, "ANALOG REALITY", 11, AMBER)
    ax.text(x0 + w / 2, py - 2.8, "a real wire carries a noisy analog voltage",
            ha="center", va="center", fontsize=9.4, color=SLATE)

    arrow(ax, 40.5, py + ph / 2, 46.5, py + ph / 2, color=SLATE, lw=2.4, ms=13)
    ax.text(43.5, py + ph / 2 + 2.4, "interpret", ha="center", va="center",
            fontsize=9, color=SLATE, style="italic")

    # ---- right: banded voltage scale ----
    bx, bw = 49, 13
    bands = [(0.00, 0.26, GREEN,     "logic  0"),
             (0.26, 0.46, "#B9C4CF", "FORBIDDEN"),
             (0.46, 1.00, TEAL,      "logic  1")]
    for lo, hi, c, lab in bands:
        ax.add_patch(Rectangle((bx, py + ph * lo), bw, ph * (hi - lo), fc=c,
                               ec="white", lw=1.6, zorder=3))
        ax.text(bx + bw / 2, py + ph * (lo + hi) / 2, lab, ha="center", va="center",
                fontsize=10.5, color="white", fontweight="bold", zorder=5)
    title(ax, bx + bw / 2, py + ph + 2.6, "DIGITAL ABSTRACTION", 11, TEAL)
    ax.text(bx + bw / 2, py - 2.8, "we only ever say 0 or 1", ha="center", va="center",
            fontsize=9.4, color=SLATE)
    ax.text(bx - 1.6, py + ph, "V$_{DD}$", ha="right", va="center", fontsize=9, color=SLATE)
    ax.text(bx - 1.6, py, "0 V", ha="right", va="center", fontsize=9, color=SLATE)

    ann = [(0.13, "V$_{IL}$ = 0.8 V", "any input below this is read as 0", GREEN),
           (0.36, "noise margin", "the guard band — a healthy signal never rests here", SLATE),
           (0.72, "V$_{IH}$ = 2.0 V", "any input above this is read as 1", TEAL)]
    for pos, head, sub, c in ann:
        yy = py + ph * pos
        wire(ax, [(bx + bw, yy), (bx + bw + 2.4, yy)], color=c, lw=1.4)
        ax.text(bx + bw + 3.2, yy + 1.3, head, ha="left", va="center", fontsize=10,
                color=c, fontweight="bold")
        ax.text(bx + bw + 3.2, yy - 1.5, sub, ha="left", va="center", fontsize=8.8, color=BODY)
    ax.text(50, 2.6, "Why it matters:  the guard band makes digital logic RESTORATIVE — noise, ageing and temperature drift are "
            "discarded at every gate, so a signal can cross a whole chip without degrading.",
            ha="center", va="center", fontsize=9.4, color=BODY, style="italic")
    save(f, "digital_abstraction")


def number_systems():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                      # 43.08
    title(ax, 50, H - 2.0, "One number, four costumes — and how negative numbers are stored", 13.5, NAVY)

    bits = list("10110100")
    bw_, gap = 6.6, 0.9
    x0, yb, bh = 17, 28.5, 6.6
    for i, b in enumerate(bits):
        c = TEAL if b == "1" else "#C3CDD8"
        ax.add_patch(FancyBboxPatch((x0 + i * (bw_ + gap), yb), bw_, bh,
                     boxstyle="round,pad=0,rounding_size=1", fc=c, ec="white", lw=1.3, zorder=3))
        ax.text(x0 + i * (bw_ + gap) + bw_ / 2, yb + bh / 2, b, ha="center", va="center",
                fontsize=13, color="white", fontweight="bold", zorder=4)
        ax.text(x0 + i * (bw_ + gap) + bw_ / 2, yb + bh + 2.6, f"2$^{{{7-i}}}$",
                ha="center", va="center", fontsize=9.5, color=SLATE)
        ax.text(x0 + i * (bw_ + gap) + bw_ / 2, yb - 2.6, str(2 ** (7 - i)), ha="center",
                va="center", fontsize=8.6, color=NAVY if b == "1" else "#B4C0CC",
                fontweight="bold" if b == "1" else "normal")
    ax.text(x0 - 2.2, yb + bh / 2, "bits", ha="right", va="center", fontsize=10,
            color=NAVY, fontweight="bold")
    ax.text(x0 - 2.2, yb + bh + 2.6, "weight", ha="right", va="center", fontsize=9.5, color=SLATE)
    ax.text(x0 - 2.2, yb - 2.6, "value", ha="right", va="center", fontsize=9, color=SLATE)
    ax.text(79.5, yb + bh / 2 + 1.2, "=  180", ha="left", va="center",
            fontsize=13, color=AMBER, fontweight="bold")
    ax.text(79.5, yb + bh / 2 - 2.4, "128+32+16+4", ha="left", va="center",
            fontsize=8.6, color=SLATE)

    reps = [("BINARY", "1011 0100", "base 2 — what the wires carry", TEAL),
            ("HEX", "0xB4", "base 16 — one hex digit = 4 bits", AMBER),
            ("DECIMAL", "180", "base 10 — what humans read", GREEN),
            ("BCD", "0001 1000 0000", "each decimal digit in its own nibble", SLATE)]
    cw, cy, chh = 22.8, 12.0, 11.5
    for i, (nm, val, sub, c) in enumerate(reps):
        x = 2.4 + i * (cw + 1.4)
        box(ax, x, cy, cw, chh, fc=LIGHT, ec=c, lw=1.6)
        title(ax, x + cw / 2, cy + chh - 2.6, nm, 10.2, c)
        title(ax, x + cw / 2, cy + chh - 6.6, val, 11.5, NAVY)
        ax.text(x + cw / 2, cy + 2.0, sub, ha="center", va="center", fontsize=8.2, color=SLATE)

    ax.add_patch(FancyBboxPatch((2.4, 1.2), 95.2, 9.0, boxstyle="round,pad=0,rounding_size=1",
                                fc="#FFF6EC", ec=AMBER, lw=1.6, zorder=2))
    ax.text(4.6, 8.0, "TWO'S COMPLEMENT — how −5 is stored in 8 bits", ha="left", va="center",
            fontsize=10, color=AMBER, fontweight="bold", zorder=4)
    steps = [("start with +5", "0000 0101"), ("invert every bit", "1111 1010"),
             ("add 1", "1111 1011"), ("this IS −5", "1111 1011")]
    sx = 5.0
    for i, (lab, val) in enumerate(steps):
        ax.text(sx + i * 22.5, 4.8, val, ha="left", va="center", fontsize=10.5,
                color=NAVY if i in (0, 3) else BODY, fontweight="bold",
                family="DejaVu Sans Mono", zorder=4)
        ax.text(sx + i * 22.5, 2.4, lab, ha="left", va="center", fontsize=8.4,
                color=AMBER, fontweight="bold", zorder=4)
        if i < 3:
            arrow(ax, sx + i * 22.5 + 17.4, 4.8, sx + i * 22.5 + 20.6, 4.8,
                  color=AMBER, lw=1.6, ms=9, z=5)
    ax.text(95.4, 8.0, "MSB = sign bit  ·  n bits cover −2$^{n-1}$ … +2$^{n-1}$−1",
            ha="right", va="center", fontsize=9, color=BODY, style="italic", zorder=4)
    save(f, "number_systems")


GATE_SPEC = [
    ("AND",  "Y = A · B",   [0, 0, 0, 1], TEAL,   "output 1 only when ALL inputs are 1"),
    ("OR",   "Y = A + B",   [0, 1, 1, 1], TEAL,   "output 1 when ANY input is 1"),
    ("NOT",  "Y = A'",      None,          RED,    "inverts: 0→1, 1→0"),
    ("NAND", "Y = (A · B)'",[1, 1, 1, 0], AMBER,  "AND then invert — UNIVERSAL"),
    ("NOR",  "Y = (A + B)'",[1, 0, 0, 0], AMBER,  "OR then invert — UNIVERSAL"),
    ("XOR",  "Y = A ⊕ B",   [0, 1, 1, 0], GREEN,  "output 1 when inputs DIFFER"),
    ("XNOR", "Y = (A ⊕ B)'",[1, 0, 0, 1], GREEN,  "output 1 when inputs are EQUAL"),
]


def gate_gallery():
    f, ax = fig(13, 7.0)
    H = 100 * 7.0 / 13
    title(ax, 50, H - 2.0, "The seven logic gates — symbol, Boolean expression, truth table", 14, NAVY)
    notes = {
        "AND":  "output 1 only when\nALL inputs are 1",
        "OR":   "output 1 when\nANY input is 1",
        "NOT":  "inverts the input\n0 → 1,  1 → 0",
        "NAND": "AND then invert\nUNIVERSAL gate",
        "NOR":  "OR then invert\nUNIVERSAL gate",
        "XOR":  "output 1 when the\ninputs DIFFER",
        "XNOR": "output 1 when the\ninputs are EQUAL",
    }
    cw, ch = 12.7, 19.0
    y = H - 25.5
    for i, (nm, expr, tt, c, _n) in enumerate(GATE_SPEC):
        x = 1.4 + i * (cw + 1.5)
        box(ax, x, y, cw, ch, fc=WHITE, ec=c, lw=1.7)
        ax.add_patch(FancyBboxPatch((x, y + ch - 5.2), cw, 5.2,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, y + ch - 5.2), cw, 2.6, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, y + ch - 2.6, nm, ha="center", va="center", fontsize=11.5,
                color="white", fontweight="bold", zorder=6)
        gate(ax, nm, x + 3.3, y + 9.0, 5.6, 5.6, ec=c, stub=1.9,
             nin=1 if nm == "NOT" else 2)
        ax.text(x + cw / 2, y + 4.3, expr, ha="center", va="center", fontsize=9.4,
                color=NAVY, fontweight="bold")
        ax.text(x + cw / 2, y + 1.7, notes[nm], ha="center", va="center", fontsize=7.4,
                color=SLATE, linespacing=1.45)

    cap_y = y - 3.2
    title(ax, 50, cap_y, "Combined truth table — read one column to get that gate's behaviour",
          10.8, SLATE, "bold")
    idx = [0, 1, 3, 4, 5, 6]          # every gate except NOT (index 2)
    cols_lbl = ["A", "B"] + [GATE_SPEC[j][0] for j in idx]
    ab = [["0", "0"], ["0", "1"], ["1", "0"], ["1", "1"]]
    data = [ab[r] + [str(GATE_SPEC[j][2][r]) for j in idx] for r in range(4)]
    widths = [8, 8] + [11.0] * 6
    tw = sum(widths)
    table(ax, (100 - tw) / 2, cap_y - 2.6, cols_lbl, data, widths, 3.9,
          head_fc=NAVY, size=11, bold_col=[0, 1])
    ax.text(50, 1.2, "NOT is single-input:  A = 0 → Y = 1,   A = 1 → Y = 0        ·        "
            "'·' means AND,   '+' means OR,   an apostrophe (or overbar) means NOT",
            ha="center", va="center", fontsize=9.4, color=BODY, style="italic")
    save(f, "gate_gallery")


def universal_nand():
    W, Hin = 13, 5.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 41.54
    title(ax, 50, H - 2.0, "NAND is universal — every other gate can be built from NAND alone",
          13.5, NAVY)
    pw, gp = 22.8, 1.5
    py, ph = 8.0, 27.0
    heads = ["NOT  from  1 NAND", "AND  from  2 NANDs", "OR  from  3 NANDs", "XOR  from  4 NANDs"]
    exprs = ["Y = A'", "Y = A · B", "Y = A + B", "Y = A ⊕ B"]
    for i in range(4):
        px = 2.0 + i * (pw + gp)
        box(ax, px, py, pw, ph, fc=LIGHT, ec=AMBER, lw=1.6)
        ax.add_patch(FancyBboxPatch((px, py + ph - 5.0), pw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=AMBER, ec=AMBER, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((px, py + ph - 5.0), pw, 2.5, fc=AMBER, ec=AMBER, lw=0, zorder=4))
        ax.text(px + pw / 2, py + ph - 2.5, heads[i], ha="center", va="center",
                fontsize=10, color="white", fontweight="bold", zorder=6)
        ax.text(px + pw / 2, py + 2.4, exprs[i], ha="center", va="center", fontsize=10.5,
                color=NAVY, fontweight="bold")
        cy = py + 15.0

        if i == 0:
            ins, o = gate(ax, "NAND", px + 8.0, cy, 6.4, 6.4, ec=AMBER, stub=2.2)
            jx = px + 4.4
            wire(ax, [ins[0], (jx, ins[0][1]), (jx, ins[1][1]), ins[1]], color=INK)
            wire(ax, [(jx, cy), (px + 2.6, cy)], color=INK)
            dot(ax, jx, cy)
            ax.text(px + 2.0, cy, "A", ha="right", va="center", fontsize=10, color=NAVY, fontweight="bold")
            ax.text(o[0] + 0.7, o[1], "Y", ha="left", va="center", fontsize=10, color=NAVY, fontweight="bold")
            ax.text(px + pw / 2, cy - 7.6, "tie both inputs together", ha="center",
                    va="center", fontsize=8.2, color=SLATE, style="italic")

        elif i == 1:
            i1, o1 = gate(ax, "NAND", px + 4.6, cy, 5.2, 5.6, ec=AMBER, stub=1.8)
            i2, o2 = gate(ax, "NAND", px + 13.2, cy, 5.2, 5.6, ec=AMBER, stub=1.8)
            jx = i2[0][0] - 1.4
            wire(ax, [o1, (jx, o1[1])], color=INK)
            wire(ax, [(jx, i2[0][1]), i2[0]], color=INK)
            wire(ax, [(jx, i2[1][1]), i2[1]], color=INK)
            wire(ax, [(jx, i2[0][1]), (jx, i2[1][1])], color=INK)
            dot(ax, jx, cy)
            for p, lab in zip(i1, "AB"):
                wire(ax, [(px + 2.2, p[1]), p], color=INK)
                ax.text(px + 1.7, p[1], lab, ha="right", va="center", fontsize=9.6,
                        color=NAVY, fontweight="bold")
            ax.text(o2[0] + 0.6, o2[1], "Y", ha="left", va="center", fontsize=9.6,
                    color=NAVY, fontweight="bold")
            ax.text(px + pw / 2, cy - 7.6, "NAND, then invert the result", ha="center",
                    va="center", fontsize=8.2, color=SLATE, style="italic")

        elif i == 2:
            i1, o1 = gate(ax, "NAND", px + 5.8, cy + 4.6, 4.2, 4.4, ec=AMBER, stub=1.4)
            i2, o2 = gate(ax, "NAND", px + 5.8, cy - 4.6, 4.2, 4.4, ec=AMBER, stub=1.4)
            i3, o3 = gate(ax, "NAND", px + 14.6, cy, 5.0, 5.6, ec=AMBER, stub=1.5)
            for ii, lab in [(i1, "A"), (i2, "B")]:
                jx = ii[0][0] - 1.3
                wire(ax, [ii[0], (jx, ii[0][1]), (jx, ii[1][1]), ii[1]], color=INK)
                wire(ax, [(jx, (ii[0][1] + ii[1][1]) / 2), (px + 2.2, (ii[0][1] + ii[1][1]) / 2)], color=INK)
                dot(ax, jx, (ii[0][1] + ii[1][1]) / 2)
                ax.text(px + 1.7, (ii[0][1] + ii[1][1]) / 2, lab, ha="right", va="center",
                        fontsize=9.6, color=NAVY, fontweight="bold")
            vx = px + 13.0
            wire(ax, [o1, (vx, o1[1]), (vx, i3[0][1]), i3[0]], color=INK)
            wire(ax, [o2, (vx, o2[1]), (vx, i3[1][1]), i3[1]], color=INK)
            ax.text(o3[0] + 0.6, o3[1], "Y", ha="left", va="center", fontsize=9.6,
                    color=NAVY, fontweight="bold")
            ax.text(px + pw / 2, cy - 9.4, "invert both inputs, then NAND", ha="center",
                    va="center", fontsize=8.2, color=SLATE, style="italic")

        else:
            blocks = [(px + 3.2, cy + 4.4, "N1"), (px + 10.0, cy + 4.4, "N2"),
                      (px + 10.0, cy - 4.4, "N3"), (px + 16.4, cy, "N4")]
            for bxp, byp, nm in blocks:
                label_box(ax, bxp, byp - 2.2, 4.6, 4.4, nm, fc=WHITE, ec=AMBER,
                          tc=AMBER, size=8.6, lw=1.5, r=0.8)
            arrow(ax, px + 7.8, cy + 4.4, px + 9.9, cy + 4.4, color=SLATE, lw=1.3, ms=7)
            wire(ax, [(px + 7.8, cy + 4.4), (px + 8.8, cy + 4.4), (px + 8.8, cy - 4.4),
                      (px + 9.9, cy - 4.4)], color=SLATE, lw=1.3)
            arrow(ax, px + 8.8, cy - 4.4, px + 9.9, cy - 4.4, color=SLATE, lw=1.3, ms=7)
            wire(ax, [(px + 14.6, cy + 4.4), (px + 15.4, cy + 4.4), (px + 15.4, cy)], color=SLATE, lw=1.3)
            wire(ax, [(px + 14.6, cy - 4.4), (px + 15.4, cy - 4.4), (px + 15.4, cy)], color=SLATE, lw=1.3)
            arrow(ax, px + 15.4, cy, px + 16.3, cy, color=SLATE, lw=1.3, ms=7)
            ax.text(px + 2.6, cy + 4.4, "A\nB", ha="right", va="center", fontsize=8.4,
                    color=NAVY, fontweight="bold", linespacing=1.3)
            ax.text(px + 21.4, cy, "Y", ha="left", va="center", fontsize=9.6,
                    color=NAVY, fontweight="bold")
            ax.text(px + pw / 2, cy - 9.4, "A⊕B = A·(A·B)' + B·(A·B)'", ha="center",
                    va="center", fontsize=8.0, color=SLATE, style="italic")

    ax.text(50, 3.4, "Why industry cares:  a foundry only has to characterise, optimise and yield a SMALL set of primitive cells. "
            "NOR is universal too — the same proof runs by duality.",
            ha="center", va="center", fontsize=9.4, color=BODY, style="italic")
    save(f, "universal_nand")


def demorgan():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 35.38
    title(ax, 50, H - 2.0, "De Morgan's theorems — \"break the bar, change the operator\"", 13.5, NAVY)

    def row(cy, g1, g2, lhs, rhs, ident):
        ins, o = gate(ax, g1, 7, cy, 7.4, 7.4, ec=AMBER, stub=2.6)
        for p, lab in zip(ins, "AB"):
            ax.text(p[0] - 0.7, p[1], lab, ha="right", va="center", fontsize=10.5,
                    color=NAVY, fontweight="bold")
        ax.text(o[0] + 0.8, o[1], lhs, ha="left", va="center", fontsize=10,
                color=NAVY, fontweight="bold")
        ax.text(29.5, cy, "≡", ha="center", va="center", fontsize=24, color=RED, fontweight="bold")
        for dy, lab in [(3.0, "A"), (-3.0, "B")]:
            gate(ax, "NOT", 35, cy + dy, 4.4, 4.2, ec=RED, stub=1.9, nin=1)
            ax.text(32.6, cy + dy, lab, ha="right", va="center", fontsize=10.5,
                    color=NAVY, fontweight="bold")
        i2, o2 = gate(ax, g2, 47, cy, 7.4, 7.4, ec=TEAL, stub=2.6)
        for dy, p in [(3.0, i2[0]), (-3.0, i2[1])]:
            wire(ax, [(41.1, cy + dy), (43.6, cy + dy), (43.6, p[1]), p], color=INK)
        ax.text(o2[0] + 0.8, o2[1], rhs, ha="left", va="center", fontsize=10,
                color=NAVY, fontweight="bold")
        ax.add_patch(FancyBboxPatch((70, cy - 5.2), 28, 10.4,
                     boxstyle="round,pad=0,rounding_size=1.4", fc="#FFF6EC", ec=AMBER,
                     lw=1.8, zorder=2))
        ax.text(84, cy, ident, ha="center", va="center", fontsize=13,
                color=AMBER, fontweight="bold", zorder=4)

    row(H - 11.0, "NAND", "OR",  "(A · B)'", "A' + B'", "(A · B)'  =  A' + B'")
    row(H - 25.0, "NOR",  "AND", "(A + B)'", "A' · B'", "(A + B)'  =  A' · B'")

    ax.text(50, 3.0, "Read it as:  a bubble on the output can be pushed back to bubbles on every input, provided you swap AND ↔ OR.  "
            "This is why NAND/NOR logic is so flexible in real gate libraries.",
            ha="center", va="center", fontsize=9.4, color=BODY, style="italic")
    save(f, "demorgan")


def sop_pos():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 43.08
    title(ax, 50, H - 2.0, "Canonical forms — every truth table has two exact algebraic twins", 13.5, NAVY)
    rows = [["0", "0", "0", "0", "m$_0$ = A'B'C'", "M$_0$ = A + B + C"],
            ["0", "0", "1", "1", "m$_1$ = A'B'C",  "M$_1$"],
            ["0", "1", "0", "0", "m$_2$",          "M$_2$ = A + B' + C"],
            ["0", "1", "1", "1", "m$_3$ = A'BC",   "M$_3$"],
            ["1", "0", "0", "0", "m$_4$",          "M$_4$ = A' + B + C"],
            ["1", "0", "1", "1", "m$_5$ = AB'C",   "M$_5$"],
            ["1", "1", "0", "0", "m$_6$",          "M$_6$ = A' + B' + C"],
            ["1", "1", "1", "1", "m$_7$ = ABC",    "M$_7$"]]
    table(ax, 2.0, H - 5.6, ["A", "B", "C", "Y", "minterm  (Y = 1)", "maxterm  (Y = 0)"],
          rows, [5.2, 5.2, 5.2, 5.2, 15.6, 15.6], 3.55, size=9, head_fc=NAVY,
          bold_col=[3], colcolors={3: GREEN})

    cx, cwid = 56.5, 41.5
    box(ax, cx, H - 17.0, cwid, 13.0, fc="#E4F4EC", ec=GREEN, lw=1.8)
    title(ax, cx + cwid / 2, H - 6.6, "SUM OF PRODUCTS   (SOP)", 11, GREEN)
    ax.text(cx + cwid / 2, H - 10.2, "Y  =  Σm(1, 3, 5, 7)", ha="center", va="center",
            fontsize=12.5, color=NAVY, fontweight="bold")
    ax.text(cx + cwid / 2, H - 14.4, "= A'B'C + A'BC + AB'C + ABC\nOR together one product term per Y=1 row",
            ha="center", va="center", fontsize=8.8, color=BODY, linespacing=1.5)

    box(ax, cx, H - 31.5, cwid, 13.0, fc="#FFF6EC", ec=AMBER, lw=1.8)
    title(ax, cx + cwid / 2, H - 21.1, "PRODUCT OF SUMS   (POS)", 11, AMBER)
    ax.text(cx + cwid / 2, H - 24.7, "Y  =  ΠM(0, 2, 4, 6)", ha="center", va="center",
            fontsize=12.5, color=NAVY, fontweight="bold")
    ax.text(cx + cwid / 2, H - 28.9, "= (A+B+C)(A+B'+C)(A'+B+C)(A'+B'+C)\nAND together one sum term per Y=0 row",
            ha="center", va="center", fontsize=8.8, color=BODY, linespacing=1.5)

    box(ax, cx, 2.0, cwid, 8.6, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(cx + cwid / 2, 6.3, "Both describe the SAME function \u2014\nhere both reduce to just  Y = C.\n"
            "Canonical \u2260 minimal:  that is the job of K-maps.",
            ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="bold", linespacing=1.6)
    save(f, "sop_pos")


def _kmap(ax, ox, oy, cell, coltop, rowlab, vals, colhdr, rowhdr,
          groups=(), lab_size=9.5, val_size=11.5, mint=None):
    ncol, nrow = len(coltop), len(rowlab)
    for j in range(ncol):
        ax.text(ox + j * cell + cell / 2, oy + nrow * cell + 2.2, coltop[j],
                ha="center", va="center", fontsize=lab_size, color=SLATE, fontweight="bold")
    for i in range(nrow):
        ax.text(ox - 1.8, oy + (nrow - 1 - i) * cell + cell / 2, rowlab[i],
                ha="right", va="center", fontsize=lab_size, color=SLATE, fontweight="bold")
    ax.text(ox - 1.8, oy + nrow * cell + 2.2, rowhdr + " \\ " + colhdr, ha="right",
            va="center", fontsize=lab_size, color=NAVY, fontweight="bold")
    for i in range(nrow):
        for j in range(ncol):
            v = vals[i][j]
            fcc = "#E4F4EC" if v == "1" else (LIGHT if v == "0" else "#FFF0D6")
            ax.add_patch(Rectangle((ox + j * cell, oy + (nrow - 1 - i) * cell), cell, cell,
                                   fc=fcc, ec=GRID, lw=1.1, zorder=3))
            ax.text(ox + j * cell + cell / 2, oy + (nrow - 1 - i) * cell + cell / 2, v,
                    ha="center", va="center", fontsize=val_size,
                    color=GREEN if v == "1" else (AMBER if v == "X" else "#9AA8B6"),
                    fontweight="bold", zorder=4)
    for (i0, j0, ni, nj, col, inset) in groups:
        ax.add_patch(FancyBboxPatch((ox + j0 * cell + inset, oy + (nrow - i0 - ni) * cell + inset),
                     nj * cell - 2 * inset, ni * cell - 2 * inset,
                     boxstyle="round,pad=0,rounding_size=1.2", fc="none", ec=col,
                     lw=2.3, zorder=7))


def kmap_method():
    W, Hin = 13, 6.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 46.15
    title(ax, 50, H - 2.0, "Karnaugh maps — adjacency made visible by Gray-code ordering", 13.5, NAVY)
    c = 4.8
    base = 20.0
    _kmap(ax, 8, base, c, ["0", "1"], ["0", "1"],
          [["0", "1"], ["1", "1"]], "B", "A")
    title(ax, 8 + c, base - 3.0, "2 vars · 4 cells", 9.6, NAVY)

    _kmap(ax, 28, base, c, ["00", "01", "11", "10"], ["0", "1"],
          [["0", "1", "1", "0"], ["0", "1", "1", "0"]], "BC", "A",
          groups=[(0, 1, 2, 2, RED, 0.5)])
    title(ax, 28 + 2 * c, base - 3.0, "3 vars · 8 cells  ·  group of 4 → Y = B", 9.6, NAVY)

    _kmap(ax, 62, base, c, ["00", "01", "11", "10"], ["00", "01", "11", "10"],
          [["1", "0", "0", "1"], ["0", "0", "0", "0"],
           ["0", "1", "1", "0"], ["0", "1", "1", "0"]], "CD", "AB",
          groups=[(2, 1, 2, 2, RED, 0.5)])
    title(ax, 62 + 2 * c, base - 3.0, "4 vars · 16 cells  ·  edges wrap", 9.6, NAVY)

    ax.text(85.5, base + 16.0, "Why Gray code?", ha="left", va="center", fontsize=10,
            color=TEAL, fontweight="bold")
    ax.text(85.5, base + 6.5, "00 → 01 → 11 → 10\n\nOnly ONE bit changes\nbetween neighbours, so\ntwo touching cells always\ndiffer in exactly one\nvariable — which is\nexactly the condition for\nXY + XY' = X.",
            ha="left", va="center", fontsize=8.4, color=BODY, linespacing=1.55)

    ax.add_patch(FancyBboxPatch((2.5, 1.5), 95, 14.5, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=LIGHT, ec=TEAL, lw=1.6, zorder=2))
    title(ax, 5.5, 14.0, "The five rules of grouping", 10.5, TEAL, ha="left")
    rules = ["1.  Only ADJACENT cells may be grouped — Gray ordering guarantees neighbours differ in one variable.",
             "2.  Group sizes must be powers of two: 1, 2, 4, 8, 16.   3.  Make each group as LARGE as possible.",
             "4.  Use as FEW groups as possible — but every 1 must be covered at least once (overlap is allowed).",
             "5.  The map WRAPS: left edge touches right edge, top touches bottom, and the four corners are adjacent.",
             "Don't-cares (X) may be absorbed into a group when they make it bigger — but never grouped on their own."]
    for i, r in enumerate(rules):
        ax.text(5.5, 11.3 - i * 2.1, r, ha="left", va="center", fontsize=8.6,
                color=AMBER if i == 4 else NAVY, zorder=4,
                fontweight="bold" if i == 4 else "normal")
    save(f, "kmap_method")


def gate_cost():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 35.38
    title(ax, 50, H - 2.0, "Why minimisation still matters — one function, two very different costs",
          13.5, NAVY)
    py, ph = 6.0, 24.0
    panels = [(2.0, 27.0, "BEFORE — canonical SOP", "#FDECEF", RED,
               ["7 AND gates (4-input)", "1 OR gate (7-input)", "4 inverters",
                "28 literals", "≈ 12 gate-equivalents", "wide fan-in → slow"]),
              (35.0, 27.0, "AFTER — K-map minimised", "#E4F4EC", GREEN,
               ["2 AND gates (2-input)", "1 AND gate (3-input)", "1 OR gate (3-input)",
                "6 literals", "≈ 5 gate-equivalents", "narrow fan-in → fast"])]
    for x, pwid, nm, bg, c, items in panels:
        box(ax, x, py, pwid, ph, fc=bg, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x, py + ph - 5.0), pwid, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, py + ph - 5.0), pwid, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + pwid / 2, py + ph - 2.5, nm, ha="center", va="center", fontsize=10,
                color="white", fontweight="bold", zorder=6)
        for j, it in enumerate(items):
            yy = py + ph - 8.4 - j * 2.9
            ax.text(x + 2.2, yy, "·  " + it, ha="left", va="center", fontsize=8.8,
                    color=NAVY if j >= 3 else BODY, fontweight="bold" if j >= 3 else "normal")
    arrow(ax, 29.8, py + ph / 2, 34.2, py + ph / 2, color=SLATE, lw=2.6, ms=14)

    box(ax, 66.0, py, 32.0, ph, fc=LIGHT, ec=TEAL, lw=1.8)
    title(ax, 82, py + ph - 3.0, "What you actually save", 11, TEAL)
    sav = [("Area", "≈ 58 % fewer gate-equivalents"),
           ("Power", "fewer switching nodes → less dynamic power"),
           ("Delay", "narrow fan-in gates switch faster"),
           ("Yield", "smaller die → more good dice per wafer")]
    for j, (k, v) in enumerate(sav):
        yy = py + ph - 7.5 - j * 4.4
        ax.text(68.2, yy, k, ha="left", va="center", fontsize=9.6, color=GREEN, fontweight="bold")
        ax.text(68.2, yy - 2.1, v, ha="left", va="center", fontsize=8.2, color=BODY)
    ax.text(50, 2.6, "In practice a synthesis tool (Yosys, Design Compiler) runs Espresso/ABC-class algorithms for you — "
            "but you must be able to read the result and know when it is wrong.",
            ha="center", va="center", fontsize=9.2, color=BODY, style="italic")
    save(f, "gate_cost")


def kmap_worked():
    W, Hin = 13, 5.7
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 43.85
    title(ax, 50, H - 2.0, "Worked K-map:   F(A,B,C,D) = \u03a3m(0,1,2,5,8,9,10) + d(3,7)", 13.5, NAVY)
    c = 7.0
    ox, oy = 10.5, 4.5
    coltop = ["00", "01", "11", "10"]
    rowlab = ["00", "01", "11", "10"]
    gray = [0, 1, 3, 2]
    ones = {0, 1, 2, 5, 8, 9, 10}
    dc = {3, 7}
    for j in range(4):
        ax.text(ox + j * c + c / 2, oy + 4 * c + 2.6, coltop[j], ha="center",
                va="center", fontsize=10.5, color=SLATE, fontweight="bold")
    for i in range(4):
        ax.text(ox - 2.2, oy + (3 - i) * c + c / 2, rowlab[i], ha="right",
                va="center", fontsize=10.5, color=SLATE, fontweight="bold")
    ax.text(ox - 2.2, oy + 4 * c + 2.6, "AB \\ CD", ha="right", va="center",
            fontsize=10, color=NAVY, fontweight="bold")
    for i in range(4):
        for j in range(4):
            m = gray[i] * 4 + gray[j]
            v = "X" if m in dc else ("1" if m in ones else "0")
            fcc = "#E4F4EC" if v == "1" else (LIGHT if v == "0" else "#FFF0D6")
            ax.add_patch(Rectangle((ox + j * c, oy + (3 - i) * c), c, c,
                                   fc=fcc, ec=GRID, lw=1.2, zorder=3))
            ax.text(ox + j * c + c / 2, oy + (3 - i) * c + c / 2, v, ha="center",
                    va="center", fontsize=13,
                    color=GREEN if v == "1" else (AMBER if v == "X" else "#9AA8B6"),
                    fontweight="bold", zorder=4)
            ax.text(ox + j * c + 1.3, oy + (3 - i) * c + c - 1.3, "m%d" % m,
                    ha="left", va="center", fontsize=6.6, color="#9AA8B6", zorder=4)

    def grp(i0, j0, ni, nj, col, inset, lw=2.5):
        ax.add_patch(FancyBboxPatch((ox + j0 * c + inset, oy + (4 - i0 - ni) * c + inset),
                     nj * c - 2 * inset, ni * c - 2 * inset,
                     boxstyle="round,pad=0,rounding_size=1.4", fc="none", ec=col,
                     lw=lw, zorder=7))

    grp(0, 0, 1, 2, RED, 0.45)          # B'C' upper half (wraps)
    grp(3, 0, 1, 2, RED, 0.45)          # B'C' lower half
    for (ii, jj) in [(0, 0), (0, 3), (3, 0), (3, 3)]:
        grp(ii, jj, 1, 1, AMBER, 1.85, lw=2.2)     # B'D' four corners
    grp(0, 1, 2, 2, TEAL, 1.05)         # A'D

    lx, lwd = 46, 51
    box(ax, lx, 4.5, lwd, H - 10.5, fc=LIGHT, ec=TEAL, lw=1.6)
    title(ax, lx + 2.6, H - 8.4, "Reading the groups", 11.5, TEAL, ha="left")
    legend = [
        (RED,   "B' C'", "m0, m1, m8, m9 \u2014 wraps top \u2194 bottom edge"),
        (AMBER, "B' D'", "m0, m2, m8, m10 \u2014 the four corners"),
        (TEAL,  "A' D",  "m1, m3, m5, m7 \u2014 the X cells grow it to 4"),
    ]
    for i, (col, term, why) in enumerate(legend):
        yy = H - 12.2 - i * 5.0
        ax.add_patch(FancyBboxPatch((lx + 2.8, yy - 1.5), 3.2, 3.0,
                     boxstyle="round,pad=0,rounding_size=0.8", fc="none", ec=col,
                     lw=2.4, zorder=5))
        ax.text(lx + 7.4, yy + 0.55, term, ha="left", va="center", fontsize=10.5,
                color=NAVY, fontweight="bold")
        ax.text(lx + 7.4, yy - 2.2, why, ha="left", va="center", fontsize=8.6, color=BODY)
    ax.add_patch(FancyBboxPatch((lx + 2.8, 7.0), lwd - 5.6, 10.5,
                 boxstyle="round,pad=0,rounding_size=1.2",
                 fc="#E4F4EC", ec=GREEN, lw=1.8, zorder=5))
    ax.text(lx + lwd / 2, 14.0, "F  =  B'C'  +  B'D'  +  A'D", ha="center", va="center",
            fontsize=13, color=NAVY, fontweight="bold", zorder=7)
    ax.text(lx + lwd / 2, 9.6, "3 product terms \u00b7 6 literals\ncanonical SOP would need 7 terms / 28 literals",
            ha="center", va="center", fontsize=8.8, color=BODY, zorder=7, linespacing=1.5)
    ax.text(50, 1.4, "Every '1' must be covered at least once. m5 is covered ONLY by A'D, which makes A'D an essential prime implicant. "
            "The X cells were used to enlarge groups, never covered for their own sake.",
            ha="center", va="center", fontsize=8.8, color=SLATE, style="italic")
    save(f, "kmap_worked")


if __name__ == "__main__":
    digital_abstraction(); number_systems(); gate_gallery(); universal_nand()
    demorgan(); sop_pos(); kmap_method(); kmap_worked(); gate_cost()
