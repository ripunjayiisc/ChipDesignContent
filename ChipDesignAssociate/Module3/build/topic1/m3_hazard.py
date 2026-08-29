# -*- coding: utf-8 -*-
"""Module 3 Topic 1 diagrams — races and hazards in combinational circuits."""
import _boot
from dsl import *


# ------------------------------------------------------- what a hazard is
def hazard_idea():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "A hazard is a wrong value on the way to the right one", 12.5)
    ax.text(50, H - 7.2, "The truth table says the output should not move. "
                         "For a few hundred picoseconds, it does.",
            fontsize=9, color=SLATE, ha="center")

    ax.text(6, 50.0, "what the truth table promises", fontsize=9.2, color=GREEN,
            ha="left", fontweight="bold")
    wave(ax, 24, 44.0, 9.0, [1] * 6, 5.0, color=GREEN, lw=2.2)
    ax.text(80, 45.5, "F stays 1", fontsize=8.6, color=GREEN, ha="left",
            va="center")

    ax.text(6, 37.0, "what the gates actually do", fontsize=9.2, color=RED,
            ha="left", fontweight="bold")
    wave(ax, 24, 31.0, 4.5, [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], 5.0,
         color=RED, lw=2.2)
    arrow(ax, 78, 32.5, 42, 32.5, color=RED, lw=1.4, ms=7)
    ax.text(80, 32.5, "the glitch", fontsize=8.6, color=RED, ha="left",
            va="center", fontweight="bold")

    box(ax, 4, 14.5, 92, 13.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 24.6, "Why it happens: two paths, one output", fontsize=9.6,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 19.0, "One input feeds the output by two different routes with "
                      "different delays. When that input changes, one\nroute has "
                      "already reacted and the other has not. The output is briefly "
                      "computing from two\ninconsistent versions of the same signal.",
            fontsize=8.7, color=BODY, ha="center")

    box(ax, 4, 2.5, 92, 10.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 9.6, "This is not a slow path, and static timing analysis cannot see it",
            fontsize=9.4, color=RED, ha="center", fontweight="bold")
    ax.text(50, 5.0, "STA measures how long each path is, and every path here meets "
                     "timing. A hazard is about the\nDIFFERENCE between two paths, "
                     "so only a simulation with delays will show it.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "hazard_idea")


# ------------------------------------------------------ the three kinds
def hazard_kinds():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 53.9
    title(ax, 50, H - 3, "Three kinds of hazard", 13)

    yb = H - 10.0
    bh = 26.0
    kinds = [("STATIC-1", "F should stay 1", [1, 1, 0, 1, 1], RED,
              "a dip to 0", "two-level AND-OR"),
             ("STATIC-0", "F should stay 0", [0, 0, 1, 0, 0], AMBER,
              "a spike to 1", "two-level OR-AND"),
             ("DYNAMIC", "F should change once", [1, 0, 1, 0, 0], VIOLET,
              "it changes 3 times", "3+ levels only")]
    bw = 29.0
    x0 = 50 - (3 * bw + 2 * 3.5) / 2
    for i, (nm, want, seq, col, got, where) in enumerate(kinds):
        x = x0 + i * (bw + 3.5)
        box(ax, x, yb - bh, bw, bh, fc=WHITE, ec=col, lw=1.7)
        box(ax, x, yb - 6.0, bw, 6.0, fc=col, ec=col)
        ax.text(x + bw / 2, yb - 3.0, nm, ha="center", va="center", fontsize=10,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, yb - 9.2, want, ha="center", fontsize=8.4, color=BODY)
        wave(ax, x + 4, yb - 18.0, 4.2, seq, 4.6, color=col, lw=2.0)
        ax.text(x + bw / 2, yb - 21.0, got, ha="center", fontsize=8.6, color=col,
                fontweight="bold")
        ax.text(x + bw / 2, yb - 24.0, where, ha="center", fontsize=8.0, color=SLATE,
                fontstyle="italic")

    box(ax, 4, 3.0, 92, 13.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.0, "And one that no circuit change can remove", fontsize=9.6,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.0, "A FUNCTION hazard happens when two or more inputs change at "
                     "once and the function itself demands\na glitch. It belongs to the "
                     "truth table, not to your gates - so no implementation avoids it.\n"
                     "The only remedy is to not change those inputs together.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "hazard_kinds")


# ------------------------------------------------ the worked circuit
def hazard_race():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "The race, in time:  F = A B' + B C  with A = 1, C = 1", 12.5)
    ax.text(50, H - 7.4, "B falls. Watch the two product terms hand over - and miss.",
            fontsize=9, color=SLATE, ha="center")

    x0, wpix, n = 26.0, 4.6, 14
    sigs = [("B", [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], NAVY,
             "the input, falling"),
            ("B C", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], VIOLET,
             "switches OFF quickly - one AND delay"),
            ("A B'", [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], TEAL,
             "switches ON late - inverter, THEN an AND"),
            ("F", [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1], RED,
             "nothing is holding it up in between")]
    y = H - 15.0
    for nm, seq, col, note in sigs:
        wave(ax, x0, y, wpix, seq, 5.2, color=col, lw=2.2, name=nm, name_size=9.5)
        ax.text(x0 + n * wpix + 2.0, y + 1.6, note, fontsize=8.0, color=col,
                ha="left", va="center")
        y -= 9.0

    # the danger window
    xa, xb = x0 + 5 * wpix, x0 + 7 * wpix
    ax.add_patch(Rectangle((xa, y + 5.0), xb - xa, H - 15.0 - y - 1.0,
                           fc="#FDECEF", ec="none", zorder=1))
    ax.plot([xa, xa], [y + 5.0, H - 11.5], color=RED, lw=1.0, ls="--", zorder=6)
    ax.plot([xb, xb], [y + 5.0, H - 11.5], color=RED, lw=1.0, ls="--", zorder=6)
    ax.text((xa + xb) / 2, H - 10.5, "both terms 0", fontsize=8.2, color=RED,
            ha="center", fontweight="bold")

    box(ax, 4, 3.0, 92, 15.5, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 15.0, "The rule this gives you", fontsize=9.6, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(50, 9.6, "Take two input patterns one variable apart that both give F = 1. "
                     "If NO single product term covers\nboth of them, then one term "
                     "must switch off while another switches on - and whether the\n"
                     "output dips is decided by delays you do not control.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 4.6, "That is a static-1 logic hazard, and tools/hazard.py finds them "
                     "by exactly this test.",
            fontsize=8.5, color=TEAL, ha="center", fontstyle="italic")
    save(f, "hazard_race")


# ------------------------------------------------------------ the K-map
def hazard_kmap():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "The same thing on a K-map: adjacent 1s in different loops",
          12.5)

    # K-map for F = A B' + B C, rows A, cols BC
    cols = ["00", "01", "11", "10"]
    vals = {(0, "00"): 0, (0, "01"): 0, (0, "11"): 1, (0, "10"): 0,
            (1, "00"): 1, (1, "01"): 1, (1, "11"): 1, (1, "10"): 0}
    x0, y0 = 22.0, H - 14.0
    cw, ch = 11.0, 8.0
    ax.text(x0 - 4, y0 + 3.0, "A", fontsize=9.5, color=NAVY, ha="center",
            fontweight="bold")
    ax.text(x0 + 2 * cw, y0 + 5.5, "B C", fontsize=9.5, color=NAVY, ha="center",
            fontweight="bold")
    for j, c in enumerate(cols):
        ax.text(x0 + j * cw + cw / 2, y0 + 2.0, c, fontsize=8.8, color=SLATE,
                ha="center")
    for i in (0, 1):
        ax.text(x0 - 4, y0 - i * ch - ch / 2, str(i), fontsize=8.8, color=SLATE,
                ha="center", va="center")
        for j, c in enumerate(cols):
            v = vals[(i, c)]
            box(ax, x0 + j * cw, y0 - (i + 1) * ch, cw, ch, fc=WHITE, ec=GRID,
                lw=1.0, r=0.2)
            ax.text(x0 + j * cw + cw / 2, y0 - i * ch - ch / 2, str(v),
                    fontsize=11, color=NAVY if v else "#C9D2DA", ha="center",
                    va="center", fontweight="bold")

    # loop A B'  -> A=1, B=0 : cells (1,"00") and (1,"01")
    box(ax, x0 - 1.2, y0 - 2 * ch - 1.2, 2 * cw + 2.4, ch + 2.4, fc="none",
        ec=TEAL, lw=2.2, r=1.4)
    ax.text(x0 + cw - 2, y0 - 2 * ch - 4.6, "A B'", fontsize=9, color=TEAL,
            ha="center", fontweight="bold")
    # loop B C -> B=1,C=1 : cells (0,"11") and (1,"11")
    box(ax, x0 + 2 * cw - 1.2, y0 - 2 * ch - 1.2, cw + 2.4, 2 * ch + 2.4,
        fc="none", ec=VIOLET, lw=2.2, r=1.4)
    ax.text(x0 + 2 * cw + cw / 2 + 7.5, y0 - ch, "B C", fontsize=9, color=VIOLET,
            ha="left", va="center", fontweight="bold")

    # the gap
    ax.add_patch(Circle((x0 + 1.5 * cw, y0 - 1.5 * ch), 5.2, fc="none", ec=RED,
                        lw=2.4, ls="--", zorder=6))
    ax.text(x0 + 1.5 * cw, y0 - 2 * ch - 8.0, "these two 1s are adjacent\n"
                                              "but no single loop holds both",
            fontsize=8.4, color=RED, ha="center", fontweight="bold")

    box(ax, 4, 3.0, 92, 15.5, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 15.0, "The fix is a third loop that bridges the gap", fontsize=9.6,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 10.0, "Draw a loop around those two cells: A = 1, C = 1, B either way. "
                      "That is the term A C.",
            fontsize=8.8, color=BODY, ha="center")
    ax.text(50, 5.4, "It covers no new 1s, so it changes nothing in the truth table. "
                     "It is REDUNDANT - and that is\nexactly why a minimiser deletes it "
                     "and why you have to ask for it deliberately.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "hazard_kmap")


# ------------------------------------------------------- the consensus fix
def consensus_fix():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "The consensus term: one extra gate, no logic change", 12.5)

    # the same timeline, with the third term added
    x0, wpix, n = 26.0, 4.6, 14
    sigs = [("B C", [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], VIOLET, ""),
            ("A B'", [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], TEAL, ""),
            ("A C", [1] * 14, GREEN, "the new term - 1 throughout, whatever B does"),
            ("F", [1] * 14, RED, "never dips")]
    y = H - 13.0
    for nm, seq, col, note in sigs:
        wave(ax, x0, y, wpix, seq, 5.2, color=col, lw=2.2, name=nm, name_size=9.5)
        if note:
            ax.text(x0 + n * wpix + 2.0, y + 1.6, note, fontsize=8.0, color=col,
                    ha="left", va="center")
        y -= 8.0

    box(ax, 4, 16.0, 44, 14.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(26, 27.2, "why it works", fontsize=9.2, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(26, 21.4, "With A = 1 and C = 1 the term A C is 1\nwhatever B is doing. "
                      "It holds F up right\nthrough the transition, so there is no\n"
                      "handover to lose.",
            fontsize=8.3, color=BODY, ha="center")

    box(ax, 52, 16.0, 44, 14.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(74, 27.2, "what it costs", fontsize=9.2, color=AMBER, ha="center",
            fontweight="bold")
    ax.text(74, 21.4, "One AND gate and one more input on\nthe OR - and a term a "
                      "logic minimiser\nwill delete the moment you stop\nprotecting "
                      "it.",
            fontsize=8.3, color=BODY, ha="center")

    box(ax, 4, 2.5, 92, 11.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 10.1, "Measured in the lab", fontsize=9.4, color=NAVY, ha="center",
            fontweight="bold")
    ax.text(50, 6.1, "hz_static1: 1 glitch over 24 transitions.   hz_static1_fix: 0.",
            fontsize=8.8, color=BODY, ha="center", family="monospace")
    ax.text(50, 3.4, "Both truth tables 10111000 - the function did not change.",
            fontsize=8.5, color=GREEN, ha="center")
    save(f, "consensus_fix")


# ------------------------------------------------------- the detector
def glitch_detector():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Finding glitches by counting, not by squinting", 12.5)
    ax.text(50, H - 7.2, "A waveform viewer does not scale and does not go in a "
                         "regression. Counting does.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 13.0
    steps = [("1", "Settle at the starting input pattern, record F", TEAL),
             ("2", "Arm a counter on every change of F", VIOLET),
             ("3", "Change ONE input, wait, record F again", NAVY),
             ("4", "Expected changes: 0 if F ended where it started, else 1", GREEN),
             ("5", "More than expected = a glitch. Name it and count it.", RED)]
    rh = 6.6
    for n, t, col in steps:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((9.5, y - rh / 2), 2.3, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - rh / 2, n, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(15, y - rh / 2, t, ha="left", va="center", fontsize=9.0, color=BODY)
        y -= rh + 1.2

    box(ax, 4, 3.0, 92, 14.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.6, "It also records the settled truth table", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.6, "So a \"fix\" that quietly changes the function cannot pass as a "
                     "fix. In the lab every design in a\nfamily prints the same "
                     "signature - 10111000 before the fix and after it.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.2, "24 transitions examined per design. Three inputs, eight states, "
                     "three single-variable moves from each.",
            fontsize=8.3, color=SLATE, ha="center", fontstyle="italic")
    save(f, "glitch_detector")


# -------------------------------------------------- the measured results
def hazard_results():
    W, Hin = 11.5, 7.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 67.8
    title(ax, 50, H - 3, "Six designs, one detector, and a surprise in row five", 12.5)

    rows = [["hz_static1", "A B' + B C", "10111000", "1 glitch (static)"],
            ["hz_static1_fix", "+ A C", "10111000", "CLEAN"],
            ["hz_none", "A B + A C", "11100000", "CLEAN"],
            ["hz_dynamic", "(A B'+B C) XOR B", "01110100", "5 glitches"],
            ["hz_dynamic_fix", "+ A C inside", "01110100", "4 glitches"],
            ["hz_flat_fix", "A B' + B C' + A C'", "01110100", "CLEAN"]]
    table(ax, 4, H - 9.0, ["design", "cover", "truth table", "detector"],
          rows, [24, 28, 20, 20], 4.8, size=8.4, bold_col=[0],
          colcolors={2: SLATE})

    box(ax, 4, 3.0, 92, 21.0, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 20.6, "Row five is the one to stop on", fontsize=9.6, color=AMBER,
            ha="center", fontweight="bold")
    ax.text(50, 15.0, "Adding the consensus term removed the DYNAMIC hazard and left "
                      "four static ones. Those have a\ndifferent cause: with A=0, C=1 "
                      "the inner expression collapses to a DELAYED COPY of B, so the\n"
                      "circuit computes B XOR B-delayed and spikes on every edge.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 7.4, "That is reconvergent fanout. No redundant product term repairs it, "
                     "because the cover is not what\nis wrong - the structure is. "
                     "Row six flattens it and re-covers: clean.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 3.9, "\"Add the consensus term\" cures a two-level logic hazard, "
                     "and only that.",
            fontsize=8.8, color=RED, ha="center", fontweight="bold")
    save(f, "hazard_results")


for fn in (hazard_idea, hazard_kinds, hazard_race, hazard_kmap, consensus_fix,
           glitch_detector, hazard_results):
    fn()
