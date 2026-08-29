# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — what RTL is, and the abstraction ladder."""
import _boot
from dsl import *


# ------------------------------------------------------ what RTL means
def rtl_definition():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Register Transfer Level: the name is the definition",
          FS_TITLE)
    yb = H - 26.0
    label_box(ax, 6, yb, 18, 11.0, "REGISTER", fc=WHITE, ec=NAVY, tc=NAVY,
              size=FS_HEAD, lw=2.2)
    box(ax, 33, yb + 1.0, 30, 9.0, fc=LIGHT, ec=TEAL, lw=2.0)
    ax.text(48, yb + 5.5, "combinational logic", ha="center", va="center",
            fontsize=FS_BODY, color=TEAL, fontweight="bold")
    label_box(ax, 72, yb, 18, 11.0, "REGISTER", fc=WHITE, ec=NAVY, tc=NAVY,
              size=FS_HEAD, lw=2.2)
    arrow(ax, 24, yb + 5.5, 33, yb + 5.5, color=SLATE, lw=2.2, ms=12)
    arrow(ax, 63, yb + 5.5, 72, yb + 5.5, color=SLATE, lw=2.2, ms=12)

    ax.text(15, yb + 15.0, "1. WHICH REGISTERS EXIST", fontsize=FS_BODY,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(81, yb + 16.5, "2. WHAT TRANSFERS INTO EACH,", fontsize=FS_BODY,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(81, yb + 13.2, "ON EACH CLOCK EDGE", fontsize=FS_BODY,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(48, yb - 3.2, "you never say how long this takes, or what gates it "
                          "uses",
            fontsize=FS_SMALL, color=TEAL, ha="center", fontstyle="italic")

    ax.text(50, 8.5, "always @(posedge clk)   y <= x + 1;", fontsize=13,
            color=NAVY, ha="center", family="monospace", fontweight="bold")
    ax.text(50, 3.5, "x, through an adder, into y - and everything else is the "
                     "tool's problem.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "rtl_definition")


def rtl_transfer_trace():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Watch one value transfer, one register per edge",
          FS_TITLE)
    ax.text(50, H - 10.0, "A single 5 is applied on cycle 0 and never again.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    rows = [["0", "5", "5", "1", "0", "0"],
            ["1", "0", "0", "6", "2", "0"],
            ["2", "0", "0", "1", "12", "2"],
            ["3", "0", "0", "1", "2", "14"],
            ["4", "0", "0", "1", "2", "16"]]
    table(ax, 17, H - 13.5, ["cycle", "din", "x", "y", "z", "acc"], rows,
          [11, 11, 11, 11, 11, 11], 4.0, size=FS_TABLE, bold_col=[0],
          colcolors={2: TEAL, 3: TEAL, 4: TEAL, 5: GREEN})

    ax.text(50, 7.5, "5 -> x      6 -> y      12 -> z      -> acc",
            fontsize=13, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 2.5, "One edge each. Nothing moved in between - that is the "
                     "entire timing model of RTL.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "rtl_transfer_trace")


def nonblocking():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Why clocked blocks use <= and combinational blocks "
                           "use =", FS_TITLE)

    y = H - 10.0
    bh = 24.0
    box(ax, 3, y - bh, 46, bh, fc=LIGHT, ec=NAVY, lw=2.0)
    ax.text(26, y - 4.6, "<=  non-blocking", fontsize=FS_HEAD + 1, color=NAVY,
            ha="center", fontweight="bold", family="monospace")
    ax.text(26, y - 9.0, "in CLOCKED blocks", fontsize=FS_SMALL, color=SLATE,
            ha="center")
    for i, ln in enumerate(["every right-hand side is read first,",
                            "using the OLD values, then every",
                            "left-hand side updates at the",
                            "same instant"]):
        ax.text(26, y - 13.5 - i * 3.2, ln, fontsize=FS_SMALL, color=BODY,
                ha="center")

    box(ax, 51, y - bh, 46, bh, fc="#F4F8FB", ec=TEAL, lw=2.0)
    ax.text(74, y - 4.6, "=  blocking", fontsize=FS_HEAD + 1, color=TEAL,
            ha="center", fontweight="bold", family="monospace")
    ax.text(74, y - 9.0, "in COMBINATIONAL blocks", fontsize=FS_SMALL,
            color=SLATE, ha="center")
    for i, ln in enumerate(["each statement completes before",
                            "the next one starts, exactly the",
                            "way software statements run",
                            ""]):
        ax.text(74, y - 13.5 - i * 3.2, ln, fontsize=FS_SMALL, color=BODY,
                ha="center")

    ax.text(50, 8.5, "a <= b;  b <= a;   swaps them.        "
                     "a = b;  b = a;   does not.",
            fontsize=FS_BODY, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 3.5, "Neither is an error. Both are caught by rules L001 and "
                     "L002 of the linter in this lab.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "nonblocking")


# -------------------------------------------------- the abstraction ladder
def ladder():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Four levels of abstraction, one circuit", FS_TITLE)
    ax.text(50, H - 10.0, "Higher up you say WHAT. Lower down you say HOW. The "
                          "circuit is the same.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    levels = [("BEHAVIOURAL", "{cout,sum} = a + b + cin;",
               "you describe the function", GREEN),
              ("DATAFLOW", "assign sum = a ^ b ^ cin;",
               "you describe the Boolean form", TEAL),
              ("GATE", "xor x1 (s1, a, b);",
               "you name every gate and wire", VIOLET),
              ("SWITCH", "pmos p1 (y, vdd, a);",
               "you place individual transistors", AMBER)]
    y = H - 14.0
    rh = 6.6
    for nm, code, what, col in levels:
        box(ax, 5, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.6)
        box(ax, 5, y - rh, 23, rh, fc=col, ec=col)
        ax.text(16.5, y - rh / 2, nm, ha="center", va="center", fontsize=FS_BODY,
                color=WHITE, fontweight="bold")
        ax.text(31, y - rh / 2, code, ha="left", va="center", fontsize=FS_MONO,
                color=NAVY, family="monospace", fontweight="bold")
        ax.text(63, y - rh / 2, what, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        y -= rh + 1.2

    arrow(ax, 2.2, H - 14.0, 2.2, y + 1.2, color=SLATE, lw=2.0, ms=11)
    ax.text(1.0, (H - 14.0 + y) / 2, "more detail", fontsize=FS_SMALL,
            color=SLATE, ha="center", va="center", rotation=90)

    ax.text(50, 1.8, "All four simulated together on all 8 input patterns. "
                     "Zero mismatches.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "ladder")


def ladder_synthesis():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "And what a synthesiser makes of each level",
          FS_TITLE)

    rows = [["behavioural", "OK", "5", "NAND x3, XOR x2"],
            ["dataflow", "OK", "6", "AND x2, OR x2, XNOR, ORNOT"],
            ["gate", "OK", "6", "identical netlist to dataflow"],
            ["switch", "REFUSED", "-", "transistors are not synthesisable"]]
    table(ax, 6, H - 10.0, ["written at", "synthesis", "cells", "what came out"],
          rows, [22, 18, 12, 36], 5.2, size=FS_TABLE, bold_col=[0, 2],
          colcolors={2: NAVY})

    ax.text(50, 9.5, "The BEHAVIOURAL description produced the SMALLEST "
                     "circuit - five cells against six.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 5.8, "Dataflow and gate produced the IDENTICAL netlist: writing "
                     "the Boolean form already fixes the structure.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    ax.text(50, 1.8, "So write at the highest level that expresses your intent.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "ladder_synthesis")


def proof_vs_test():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Simulation shows. Proof settles.", FS_TITLE)

    y = H - 10.0
    bh = 22.0
    box(ax, 3, y - bh, 46, bh, fc=LIGHT, ec=TEAL, lw=2.0)
    ax.text(26, y - 4.6, "EXHAUSTIVE SIMULATION", fontsize=FS_HEAD, color=TEAL,
            ha="center", fontweight="bold")
    ax.text(26, y - 11.0, "8 patterns, 3 inputs.\nEvery possible case, so this\n"
                          "really is complete.", fontsize=FS_SMALL, color=BODY,
            ha="center")
    ax.text(26, y - 19.0, "but 2^30 patterns is not",
            fontsize=FS_SMALL, color=RED, ha="center", fontstyle="italic")

    box(ax, 51, y - bh, 46, bh, fc="#EEF7F1", ec=GREEN, lw=2.0)
    ax.text(74, y - 4.6, "EQUIVALENCE CHECKING", fontsize=FS_HEAD, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(74, y - 11.0, "Both designs, same inputs,\noutputs compared, and an\n"
                          "assertion that they agree.", fontsize=FS_SMALL,
            color=BODY, ha="center")
    ax.text(74, y - 19.0, "A solver cannot break it",
            fontsize=FS_SMALL, color=GREEN, ha="center", fontstyle="italic")

    ax.text(50, 11.5, "behav vs dataflow   EQUIVALENT   (94 SAT variables)",
            fontsize=FS_MONO, color=BODY, ha="center", family="monospace")
    ax.text(50, 7.8, "behav vs broken     NOT EQUIVALENT",
            fontsize=FS_MONO, color=RED, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 3.0, "A checker that cannot fail is not evidence of anything.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "proof_vs_test")


for fn in (rtl_definition, rtl_transfer_trace, nonblocking, ladder,
           ladder_synthesis, proof_vs_test):
    fn()
