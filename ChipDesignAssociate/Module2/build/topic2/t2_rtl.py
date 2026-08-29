# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — what RTL is, and the abstraction ladder."""
import _boot
from dsl import *


# ------------------------------------------------------ what RTL means
def rtl_definition():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Register Transfer Level: the name is the definition", 12.5)
    ax.text(50, H - 7.4, "An RTL description says two things, and nothing else.",
            fontsize=9, color=SLATE, ha="center")

    yb = H - 26.0
    label_box(ax, 6, yb, 17, 11.0, "REGISTER", fc=WHITE, ec=NAVY, tc=NAVY, size=9.4,
              lw=2.0)
    box(ax, 32, yb + 1.0, 30, 9.0, fc=LIGHT, ec=TEAL, lw=1.8)
    ax.text(47, yb + 5.5, "combinational logic", ha="center", va="center",
            fontsize=9.0, color=TEAL, fontweight="bold")
    label_box(ax, 71, yb, 17, 11.0, "REGISTER", fc=WHITE, ec=NAVY, tc=NAVY, size=9.4,
              lw=2.0)
    arrow(ax, 23, yb + 5.5, 32, yb + 5.5, color=SLATE, lw=2.0)
    arrow(ax, 62, yb + 5.5, 71, yb + 5.5, color=SLATE, lw=2.0)

    ax.text(14.5, yb + 14.5, "1. WHICH REGISTERS EXIST", fontsize=8.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(47, yb - 3.6, "you never say how long this takes,\n"
                          "or what gates it uses",
            fontsize=8.2, color=TEAL, ha="center", fontstyle="italic")
    ax.text(79.5, yb + 14.5, "2. WHAT TRANSFERS INTO EACH,\nON EACH CLOCK EDGE",
            fontsize=8.6, color=NAVY, ha="center", fontweight="bold")

    box(ax, 4, 17.0, 92, 15.0, fc="#F4F8FB", ec=NAVY, lw=1.6)
    ax.text(50, 29.0, "always @(posedge clk) begin", fontsize=9.4, color=NAVY,
            ha="center", family="monospace")
    ax.text(50, 25.0, "    y <= x + 1;        // x, through an adder, into y",
            fontsize=9.4, color=TEAL, ha="center", family="monospace")
    ax.text(50, 21.0, "end", fontsize=9.4, color=NAVY, ha="center",
            family="monospace")

    box(ax, 4, 3.0, 92, 11.5, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 11.0, "Everything else is the tool's problem", fontsize=9.6,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 6.2, "How many gates, which gates, how they are wired, how fast they "
                     "are - none of that is in\nthe description. You state the "
                     "transfers; synthesis works out the circuit.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "rtl_definition")


def rtl_transfer_trace():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Watch one value transfer, one register per edge", 12.5)
    ax.text(50, H - 7.4, "A single 5 is applied on cycle 0 and never again.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["0", "5", "5", "1", "0", "0"],
            ["1", "0", "0", "6", "2", "0"],
            ["2", "0", "0", "1", "12", "2"],
            ["3", "0", "0", "1", "2", "14"],
            ["4", "0", "0", "1", "2", "16"]]
    table(ax, 14, H - 11.0, ["cycle", "din", "x", "y", "z", "acc"],
          rows, [12, 12, 12, 12, 12, 12], 5.0, size=9.4, bold_col=[0],
          colcolors={2: TEAL, 3: TEAL, 4: TEAL, 5: GREEN})

    ax.text(50, 20.5, "5  ->  x        6  ->  y        12  ->  z        ->  acc",
            fontsize=9.6, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 17.0, "one edge        one edge         one edge",
            fontsize=8.2, color=SLATE, ha="center", family="monospace")

    box(ax, 4, 3.0, 92, 11.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 10.6, "Nothing moved between edges", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 5.8, "The logic settles during the cycle and the registers all update "
                     "together at the edge. That is the\nentire timing model of RTL, "
                     "and it is why RTL is easy to reason about.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "rtl_transfer_trace")


def nonblocking():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Why clocked blocks use <= and combinational blocks use =",
          12.5)

    y = H - 10.0
    box(ax, 4, y - 20.0, 44, 20.0, fc=LIGHT, ec=NAVY, lw=1.7)
    ax.text(26, y - 4.0, "<=  non-blocking", fontsize=10, color=NAVY, ha="center",
            fontweight="bold", family="monospace")
    ax.text(26, y - 8.0, "in CLOCKED blocks", fontsize=8.6, color=SLATE, ha="center")
    for i, ln in enumerate(["every right-hand side is read first,",
                            "using the OLD values,",
                            "then every left-hand side updates",
                            "at the same instant"]):
        ax.text(26, y - 11.6 - i * 2.6, ln, fontsize=8.2, color=BODY, ha="center")

    box(ax, 52, y - 20.0, 44, 20.0, fc="#F4F8FB", ec=TEAL, lw=1.7)
    ax.text(74, y - 4.0, "=  blocking", fontsize=10, color=TEAL, ha="center",
            fontweight="bold", family="monospace")
    ax.text(74, y - 8.0, "in COMBINATIONAL blocks", fontsize=8.6, color=SLATE,
            ha="center")
    for i, ln in enumerate(["each statement completes before",
                            "the next one starts,",
                            "exactly the way software",
                            "statements run"]):
        ax.text(74, y - 11.6 - i * 2.6, ln, fontsize=8.2, color=BODY, ha="center")

    ax.text(50, 32.5, "a <= b;   b <= a;      swaps them.      "
                      "a = b;   b = a;      does not.",
            fontsize=9.2, color=NAVY, ha="center", family="monospace",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 25.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 24.6, "Get it backwards and the code still compiles", fontsize=9.6,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 19.6, "Blocking assignments in a clocked block make two blocks see "
                      "each other's half-updated values,\nand which one wins depends "
                      "on the order the simulator happens to run them in.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 13.0, "Non-blocking in a combinational block makes it behave like a "
                      "register in simulation while\nsynthesis builds plain logic - "
                      "so the simulation and the silicon disagree.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 6.4, "Neither one is an error. Both are caught by rules L001 and L002 "
                     "of the linter in this lab.",
            fontsize=8.6, color=RED, ha="center", fontweight="bold")
    save(f, "nonblocking")


# -------------------------------------------------- the abstraction ladder
def ladder():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "Four levels of abstraction, one circuit", 13)
    ax.text(50, H - 7.4, "Higher up you say WHAT. Lower down you say HOW. "
                         "The circuit is the same.",
            fontsize=9, color=SLATE, ha="center")

    levels = [("BEHAVIOURAL", "{cout,sum} = a + b + cin;",
               "you describe the function", GREEN, "written here"),
              ("DATAFLOW", "assign sum = a ^ b ^ cin;",
               "you describe the Boolean form", TEAL, ""),
              ("GATE", "xor x1 (s1, a, b);",
               "you name every gate and wire", VIOLET, "synthesis writes here"),
              ("SWITCH", "pmos p1 (y, vdd, a);",
               "you place individual transistors", AMBER,
               "the foundry writes here")]
    y = H - 12.0
    rh = 9.6
    for i, (nm, code, what, col, who) in enumerate(levels):
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.6)
        box(ax, 4, y - rh, 22, rh, fc=col, ec=col)
        ax.text(15, y - rh / 2, nm, ha="center", va="center", fontsize=9.4,
                color=WHITE, fontweight="bold")
        ax.text(28, y - 3.2, code, ha="left", fontsize=8.6, color=NAVY,
                family="monospace", fontweight="bold")
        ax.text(28, y - 6.8, what, ha="left", fontsize=8.2, color=BODY)
        if who:
            ax.text(94, y - rh / 2, who, ha="right", va="center", fontsize=8.0,
                    color=col, fontstyle="italic")
        y -= rh + 1.2

    arrow(ax, 1.5, H - 12.0, 1.5, y + 1.2, color=SLATE, lw=1.8)
    ax.text(0.6, (H - 12.0 + y) / 2, "more detail", fontsize=8.0, color=SLATE,
            ha="center", va="center", rotation=90)

    box(ax, 4, 3.0, 92, 12.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 11.6, "All four were simulated together on all 8 input patterns. "
                      "Zero mismatches.", fontsize=9.4, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(50, 6.6, "The level of abstraction changed WHAT WAS WRITTEN, not WHAT IT "
                     "DOES. That is the single\nmost useful idea in this topic.",
            fontsize=8.7, color=BODY, ha="center")
    save(f, "ladder")


def ladder_synthesis():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "And what a synthesiser makes of each level", 12.5)

    rows = [["behavioural", "OK", "5", "NAND x3, XOR x2"],
            ["dataflow", "OK", "6", "AND x2, OR x2, XNOR, ORNOT"],
            ["gate", "OK", "6", "identical netlist to dataflow"],
            ["switch", "REFUSED", "-", "transistors are not synthesisable"]]
    table(ax, 6, H - 10.0, ["written at", "synthesis", "cells", "what came out"],
          rows, [22, 18, 12, 36], 5.4, size=8.8, bold_col=[0, 2],
          colcolors={2: NAVY})

    box(ax, 4, 20.0, 92, 15.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 32.0, "Two results worth stopping on", fontsize=9.6, color=AMBER,
            ha="center", fontweight="bold")
    ax.text(50, 27.0, "The BEHAVIOURAL description produced the SMALLEST circuit - "
                      "five cells against six.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 22.6, "And dataflow and gate produced the IDENTICAL netlist: once you "
                      "write the Boolean expression\nyou have already chosen the "
                      "structure, and naming the gates adds nothing but typing.",
            fontsize=8.7, color=BODY, ha="center")

    box(ax, 4, 3.0, 92, 14.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 13.6, "The rule this gives you", fontsize=9.6, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(50, 8.4, "Write at the highest level that expresses your intent. Every "
                     "level you descend takes a decision\naway from the tool and "
                     "gives it to you - whether or not you wanted it.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 4.0, "The tool is better than you are at choosing gates. It is not "
                     "better than you are at choosing architecture.",
            fontsize=8.4, color=TEAL, ha="center", fontstyle="italic")
    save(f, "ladder_synthesis")


def proof_vs_test():
    W, Hin = 11.5, 7.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 67.8
    title(ax, 50, H - 3, "Simulation shows. Proof settles.", 13)

    y = H - 10.0
    box(ax, 4, y - 21.0, 44, 21.0, fc=LIGHT, ec=TEAL, lw=1.7)
    ax.text(26, y - 4.2, "EXHAUSTIVE SIMULATION", fontsize=9.4, color=TEAL,
            ha="center", fontweight="bold")
    ax.text(26, y - 9.0, "8 patterns, 3 inputs.\nEvery possible case, so this\n"
                         "really is complete.", fontsize=8.4, color=BODY,
            ha="center")
    ax.text(26, y - 17.0, "but 2^30 patterns is not,\nand real designs are bigger",
            fontsize=8.2, color=RED, ha="center", fontstyle="italic")

    box(ax, 52, y - 21.0, 44, 21.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(74, y - 4.2, "EQUIVALENCE CHECKING", fontsize=9.4, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(74, y - 9.0, "Build a miter: both designs,\nsame inputs, outputs compared,\n"
                         "assert they always agree.", fontsize=8.4, color=BODY,
            ha="center")
    ax.text(74, y - 17.0, "A solver then tries to break it\nand cannot. No enumeration "
                          "at all.", fontsize=8.2, color=GREEN, ha="center",
            fontstyle="italic")

    box(ax, 4, 16.0, 92, 15.5, fc="#F4F8FB", ec=NAVY, lw=1.6)
    ax.text(50, 28.0, "proved in the lab", fontsize=9.2, color=NAVY, ha="center",
            fontweight="bold")
    ax.text(50, 23.4, "behav vs dataflow   EQUIVALENT  (94 SAT variables)",
            fontsize=8.6, color=BODY, ha="center", family="monospace")
    ax.text(50, 20.4, "behav vs gate       EQUIVALENT  (94 SAT variables)",
            fontsize=8.6, color=BODY, ha="center", family="monospace")
    ax.text(50, 17.4, "behav vs broken     NOT EQUIVALENT",
            fontsize=8.6, color=RED, ha="center", family="monospace",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 11.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 10.6, "That last line is the important one", fontsize=9.4, color=RED,
            ha="center", fontweight="bold")
    ax.text(50, 5.8, "fa_broken has one carry term missing, so it is wrong for one "
                     "input pattern in eight. A checker\nthat cannot fail is not "
                     "evidence of anything - you have to watch it catch a real bug.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "proof_vs_test")


for fn in (rtl_definition, rtl_transfer_trace, nonblocking, ladder,
           ladder_synthesis, proof_vs_test):
    fn()
