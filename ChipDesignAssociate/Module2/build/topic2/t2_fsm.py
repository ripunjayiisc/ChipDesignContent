# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — finite state machines.

The three-block coding pattern, Moore against Mealy in structure and in
measured timing, the two lab state diagrams, and what state encoding costs.
"""
import _boot
from dsl import *


def _state(ax, x, y, r, name, col=NAVY, fc=WHITE, sub=None, size=8.6):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=col, lw=1.8, zorder=4))
    ax.text(x, y + (0.9 if sub else 0), name, ha="center", va="center",
            fontsize=size, color=col, fontweight="bold", zorder=5,
            family="monospace")
    if sub:
        ax.text(x, y - 2.0, sub, ha="center", va="center", fontsize=7.4,
                color=SLATE, zorder=5)


def _selfloop(ax, x, y, r, label, col=SLATE, h=3.4):
    """A rectangular self-loop above the state - predictable, never wanders."""
    top = y + r + h
    wire(ax, [(x - 2.4, y + r * 0.9), (x - 2.4, top), (x + 2.4, top)],
         color=col, lw=1.4)
    arrow(ax, x + 2.4, top, x + 2.4, y + r * 0.9, color=col, lw=1.4, ms=8)
    ax.text(x, top + 2.0, label, ha="center", va="center", fontsize=7.6,
            color=col, family="monospace", fontweight="bold")


def _backedge(ax, xa, xb, y, r, depth, label, col=SLATE, lx=None):
    """An edge from state at xa back to the state at xb, routed BELOW the row."""
    yy = y - r - depth
    wire(ax, [(xa, y - r), (xa, yy), (xb, yy)], color=col, lw=1.4)
    arrow(ax, xb, yy, xb, y - r, color=col, lw=1.4, ms=8)
    ax.text(lx if lx is not None else (xa + xb) / 2, yy - 2.2, label,
            ha="center", va="center", fontsize=7.6, color=col,
            family="monospace", fontweight="bold")


def fsm_pattern():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "How to write a state machine: the three-block pattern",
          12.5)
    ax.text(50, H - 7.0, "Every FSM in this lab, and in most RTL groups, is "
                         "written exactly like this.",
            fontsize=9, color=SLATE, ha="center")

    blocks = [("BLOCK 1", "state register", VIOLET,
               ["always @(posedge clk or negedge rst_n)",
                "    if (!rst_n) state <= S_IDLE;",
                "    else        state <= next_state;"],
               "sequential  ·  <=  ·  reset lives HERE and nowhere else"),
              ("BLOCK 2", "next-state logic", TEAL,
               ["always @(*) begin",
                "    next_state = state;      // the default",
                "    case (state) ... endcase",
                "end"],
               "combinational  ·  =  ·  the default assignment kills the latch"),
              ("BLOCK 3", "output logic", GREEN,
               ["always @(*) begin",
                "    out = 1'b0;              // defaults again",
                "    case (state) ... endcase",
                "end"],
               "combinational  ·  reads STATE only if the machine is Moore")]
    y = H - 11.0
    bh = 15.0
    for tag, nm, col, code, note in blocks:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.7)
        box(ax, 3, y - bh, 20, bh, fc=col, ec=col)
        ax.text(13, y - 4.6, tag, ha="center", va="center", fontsize=9.2,
                color=WHITE, fontweight="bold")
        ax.text(13, y - 8.6, nm, ha="center", va="center", fontsize=8.4,
                color=WHITE)
        for i, ln in enumerate(code):
            ax.text(25.5, y - 3.4 - i * 2.7, ln, ha="left", va="center",
                    fontsize=7.5, color=INK, family="monospace")
        ax.text(95, y - bh + 2.4, note, ha="right", va="center", fontsize=7.8,
                color=col, fontstyle="italic")
        y -= bh + 2.0

    box(ax, 3, 3.0, 94, 15.5, fc=LIGHT, ec=NAVY, lw=1.7)
    ax.text(50, 15.0, "Why three blocks and not one", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 10.0, "You can write a working FSM in a single clocked block. "
                      "Three blocks are still better, because each one has "
                      "exactly one\njob: block 1 is the only sequential logic, "
                      "so it is the only place a reset or a clock appears; "
                      "blocks 2 and 3 are pure\nfunctions of the state, so "
                      "they can be read, reviewed and changed without thinking "
                      "about time at all.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(50, 4.4, "make fsm   —   three machines written this way, "
                     "simulated and synthesised",
            fontsize=8.4, color=GREEN, ha="center", fontweight="bold",
            family="monospace")
    save(f, "fsm_pattern")


def moore_mealy():
    W, Hin = 11.5, 9.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Moore and Mealy: where the output comes from", 12.5)
    ax.text(50, H - 7.0, "One structural difference. Everything else follows "
                         "from it.", fontsize=9, color=SLATE, ha="center")

    def machine(x0, name, col, mealy):
        box(ax, x0, H - 36.0, 45, 25.0, fc=WHITE, ec=col, lw=1.8)
        ax.text(x0 + 22.5, H - 13.6, name, fontsize=10.2, color=col,
                ha="center", fontweight="bold")
        yb = H - 27.0
        label_box(ax, x0 + 4, yb, 11, 7.0, "next\nstate", fc=LIGHT, ec=TEAL,
                  tc=TEAL, size=7.6)
        label_box(ax, x0 + 18, yb, 9, 7.0, "REG", fc=WHITE, ec=VIOLET,
                  tc=VIOLET, size=8)
        label_box(ax, x0 + 30, yb, 11, 7.0, "output\nlogic", fc="#EEF7F1",
                  ec=GREEN, tc=GREEN, size=7.6)
        wire(ax, [(x0 + 15, yb + 3.5), (x0 + 18, yb + 3.5)], color=INK, lw=1.5)
        wire(ax, [(x0 + 27, yb + 3.5), (x0 + 30, yb + 3.5)], color=INK, lw=1.5)
        wire(ax, [(x0 + 41, yb + 3.5), (x0 + 43.5, yb + 3.5)], color=INK,
             lw=1.5)
        ax.text(x0 + 42.4, yb + 5.4, "out", fontsize=7.6, color=BODY,
                ha="center", va="center", family="monospace")
        # input
        wire(ax, [(x0 + 1.5, yb + 3.5), (x0 + 4, yb + 3.5)], color=INK, lw=1.5)
        ax.text(x0 + 2.6, yb + 1.5, "in", fontsize=7.6, color=BODY,
                ha="center", va="center", family="monospace")
        # state feedback
        wire(ax, [(x0 + 27.5, yb), (x0 + 27.5, yb - 4.5), (x0 + 9.5, yb - 4.5),
                  (x0 + 9.5, yb)], color=VIOLET, lw=1.4)
        ax.text(x0 + 18.5, yb - 6.0, "state", fontsize=7.2, color=VIOLET,
                ha="center")
        if mealy:
            wire(ax, [(x0 + 2.5, yb + 3.5), (x0 + 2.5, yb + 9.5),
                      (x0 + 35.5, yb + 9.5), (x0 + 35.5, yb + 7.0)],
                 color=RED, lw=1.8)
            ax.text(x0 + 19, yb + 11.0, "the input reaches the OUTPUT directly",
                    fontsize=7.6, color=RED, ha="center", fontweight="bold")
        else:
            ax.text(x0 + 22.5, yb + 11.0, "the output sees the STATE and "
                    "nothing else", fontsize=7.6, color=GREEN, ha="center",
                    fontweight="bold")

    machine(3, "MOORE", GREEN, False)
    machine(52, "MEALY", RED, True)

    rows = [["output depends on", "state only", "state AND input"],
            ["output appears", "one cycle after the input", "same cycle"],
            ["output glitches", "no - decoded from registers",
             "yes - inherits the input's glitches"],
            ["states needed", "usually one more", "usually one fewer"],
            ["measured here", "13 cells, 2 flops", "14 cells, 2 flops"],
            ["use it when", "the output drives other logic or leaves the block",
             "you cannot afford the cycle"]]
    table(ax, 3, H - 38.5, ["", "Moore", "Mealy"], rows, [24, 34, 36], 4.7,
          size=8.2, bold_col=[0], colcolors={1: GREEN, 2: RED})

    box(ax, 3, 3.0, 94, 9.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 8.6, "Both machines accept exactly the same language",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.8, "The lab proves it: one stream, one golden model, five "
                     "matches, zero mismatches. They differ in WHEN they say "
                     "so, not in WHAT they say.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "moore_mealy")


def moore_mealy_timing():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The one-cycle difference, measured", 12.5)
    ax.text(50, H - 7.0, "make fsm  —  one 17-bit stream into both detectors, "
                         "both checked against a golden model.",
            fontsize=8.8, color=SLATE, ha="center")

    din = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    mealy = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
    moore = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]

    x0, wdt, u = 12.0, 4.8, 4.6
    yd = H - 17.0
    wave(ax, x0, yd, wdt, din, u, color=NAVY, name="din")
    wave(ax, x0, yd - 9.0, wdt, mealy, u, color=RED, name="det (Mealy)")
    wave(ax, x0, yd - 18.0, wdt, moore, u, color=GREEN, name="det (Moore)")

    for i in range(17):
        ax.text(x0 + wdt * i + wdt / 2, yd + 5.4, str(i), fontsize=6.6,
                color=SLATE, ha="center")
    ax.text(x0 + wdt * 8.5, yd + 8.4, "cycle", fontsize=8, color=SLATE,
            ha="center", fontweight="bold")

    # link each Mealy detection to the Moore detection one cycle later
    for i, v in enumerate(mealy):
        if v and i + 1 < len(moore) and moore[i + 1]:
            xc = x0 + wdt * i + wdt / 2
            arrow(ax, xc, yd - 10.4, xc + wdt, yd - 13.8, color=AMBER, lw=1.4,
                  ms=8, rad=-0.3)

    ax.text(50, yd - 24.0, "each amber arrow is the SAME detection, one cycle "
                           "later", fontsize=8.2, color=AMBER, ha="center",
            fontweight="bold")

    box(ax, 3, 3.0, 94, 13.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 12.6, "5 matches in the stream  ·  0 mismatches against the "
                      "golden model  ·  Moore trails Mealy by exactly one "
                      "cycle, every time",
            fontsize=8.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.0, "The golden model is computed from the STREAM, not from "
                     "either machine - so a bug in one of them shows up as a "
                     "mismatch\nrather than as two machines confidently "
                     "agreeing on the wrong answer.",
            fontsize=8.3, color=BODY, ha="center")
    ax.text(50, 4.2, "That is the whole point of writing a reference model by "
                     "hand.", fontsize=8.3, color=GREEN, ha="center",
            fontweight="bold")
    save(f, "moore_mealy_timing")


def seq101_moore_states():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The '101' detector as a MOORE state diagram", 12.5)
    ax.text(50, H - 7.0, "Four states. The output is written INSIDE the state, "
                         "so it depends on nothing else.",
            fontsize=9, color=SLATE, ha="center")

    r, ym = 5.6, H - 26.0
    xs = [14, 38, 62, 86]
    names = [("S_IDLE", "det=0"), ("S_1", "det=0"), ("S_10", "det=0"),
             ("S_101", "det=1")]
    for i, (x, (nm, sub)) in enumerate(zip(xs, names)):
        _state(ax, x, ym, r, nm, col=GREEN if i == 3 else NAVY,
               fc="#EEF7F1" if i == 3 else WHITE, sub=sub, size=7.8)
    for i in range(3):
        arrow(ax, xs[i] + r, ym, xs[i + 1] - r, ym, color=SLATE, lw=1.6, ms=10)
        ax.text((xs[i] + xs[i + 1]) / 2, ym + 2.2, ["1", "0", "1"][i],
                fontsize=8.4, color=NAVY, ha="center", family="monospace",
                fontweight="bold")
    _selfloop(ax, xs[0], ym, r, "0")
    _selfloop(ax, xs[1], ym, r, "1")
    _backedge(ax, xs[2], xs[0], ym, r, 5.0, "0", lx=26)
    _backedge(ax, xs[3], xs[2], ym, r, 5.0, "0", lx=74)
    _backedge(ax, xs[3], xs[1], ym, r, 11.5, "1   (the overlapping match)",
              col=GREEN, lx=62)

    box(ax, 3, 3.0, 94, 12.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 11.4, "The fourth state exists only to say 'a match just "
                      "finished'", fontsize=9.2, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(50, 6.8, "S_101 has the same successors as S_1 would after a 1, "
                     "and as S_10 would after a 0 - it decides nothing new.\n"
                     "It is there so that det can be decoded from the state "
                     "register alone, which is the definition of Moore.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "seq101_moore_states")


def seq101_mealy_states():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The same detector as a MEALY state diagram", 12.5)
    ax.text(50, H - 7.0, "Three states. Each arrow is labelled input / output.",
            fontsize=9, color=SLATE, ha="center")

    r, ye = 5.6, H - 26.0
    xs2 = [22, 50, 78]
    for x, nm in zip(xs2, ["S_IDLE", "S_1", "S_10"]):
        _state(ax, x, ye, r, nm, col=NAVY, size=7.8)
    for i in range(2):
        arrow(ax, xs2[i] + r, ye, xs2[i + 1] - r, ye, color=SLATE, lw=1.6,
              ms=10)
        ax.text((xs2[i] + xs2[i + 1]) / 2, ye + 2.2, ["1/0", "0/0"][i],
                fontsize=8.4, color=NAVY, ha="center", family="monospace",
                fontweight="bold")
    _selfloop(ax, xs2[0], ye, r, "0/0")
    _selfloop(ax, xs2[1], ye, r, "1/0")
    _backedge(ax, xs2[2], xs2[1], ye, r, 5.0, "1 / 1   <- the detection",
              col=RED, lx=64)
    _backedge(ax, xs2[2], xs2[0], ye, r, 11.5, "0/0", lx=36)

    box(ax, 3, 3.0, 94, 12.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 11.9, "The detection lives on an arrow, not in a state",
            fontsize=9.2, color=RED, ha="center", fontweight="bold")
    ax.text(50, 7.4, "'1/1' means: with the machine in S_10 and a 1 arriving, "
                     "assert det NOW and go to S_1. One state fewer,\n"
                     "one cycle sooner - and an output that moves the instant "
                     "the input does, glitches included.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(50, 4.0, "Both diagrams describe the same language. Neither is "
                     "more correct than the other.",
            fontsize=8.4, color=NAVY, ha="center", fontweight="bold")
    save(f, "seq101_mealy_states")


def traffic_states():
    W, Hin = 11.5, 9.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "A Moore controller with a datapath timer", 12.5)
    ax.text(50, H - 7.0, "fsm/traffic.v  —  a two-road junction with a car "
                         "sensor on the minor road.",
            fontsize=9, color=SLATE, ha="center")

    cx, cy, R, r = 30.0, H - 30.0, 15.0, 6.4
    import math
    pts = []
    labels = [("S_MAIN\nGREEN", GREEN), ("S_MAIN\nYELLOW", AMBER),
              ("S_SIDE\nGREEN", GREEN), ("S_SIDE\nYELLOW", AMBER)]
    for i, (nm, col) in enumerate(labels):
        a = math.pi / 2 - i * math.pi / 2
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y))
        ax.add_patch(Circle((x, y), r, fc=WHITE, ec=col, lw=1.9, zorder=4))
        ax.text(x, y, nm, ha="center", va="center", fontsize=7.0, color=col,
                fontweight="bold", zorder=5, family="monospace")
    conds = ["car &&\ntimeout", "timeout", "timeout", "timeout"]
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        arrow(ax, x1 + (x2 - x1) * 0.33, y1 + (y2 - y1) * 0.33,
              x1 + (x2 - x1) * 0.67, y1 + (y2 - y1) * 0.67,
              color=SLATE, lw=1.7, ms=10)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + (mx - cx) * 0.30, my + (my - cy) * 0.30, conds[i],
                fontsize=7.0, color=NAVY, ha="center", va="center",
                family="monospace")

    rows = [["S_MAIN_GREEN", "GREEN", "RED", "6"],
            ["S_MAIN_YELLOW", "AMBER", "RED", "2"],
            ["S_SIDE_GREEN", "RED", "GREEN", "6"],
            ["S_SIDE_YELLOW", "RED", "AMBER", "2"]]
    table(ax, 52, H - 14.0, ["state", "MAIN", "SIDE", "cycles"], rows,
          [17, 11, 11, 9], 5.0, size=8.0, bold_col=[0])

    box(ax, 52, 26.0, 45, 17.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(74.5, 39.6, "two properties, checked EVERY cycle",
            fontsize=8.8, color=GREEN, ha="center", fontweight="bold")
    ax.text(74.5, 35.4, "P1   the two roads are never both green",
            fontsize=8.0, color=BODY, ha="center")
    ax.text(74.5, 32.0, "P2   a green never goes straight to red",
            fontsize=8.0, color=BODY, ha="center")
    ax.text(74.5, 28.2, "40 cycles checked, 0 violations",
            fontsize=8.6, color=GREEN, ha="center", fontweight="bold")

    box(ax, 3, 3.0, 94, 16.0, fc=LIGHT, ec=NAVY, lw=1.7)
    ax.text(50, 15.4, "Where the timer lives, and why it is not a state",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 10.2, "A green phase lasts six cycles. Six states would be "
                      "absurd, and six hundred would be impossible - so the "
                      "count lives in a\nDOWN-COUNTER, and the state machine "
                      "only ever asks it one question: are you at zero yet? "
                      "That is a datapath and a\ncontroller again, in the "
                      "smallest design in this topic.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(50, 4.4, "Measured: 75 cells, 10 flip-flops - 2 for the state, "
                     "8 for the timer.", fontsize=8.4, color=VIOLET,
            ha="center", fontweight="bold")
    save(f, "traffic_states")


def state_encoding():
    W, Hin = 11.5, 10.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "State encoding: the choice you make by typing "
                         "numbers", 12.5)
    ax.text(50, H - 7.0, "The same four states, two ways of numbering them. "
                         "Same behaviour, different hardware.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 11.0
    rows = [["S_IDLE", "2'b00", "4'b0001"],
            ["S_1", "2'b01", "4'b0010"],
            ["S_10", "2'b10", "4'b0100"],
            ["S_101", "2'b11", "4'b1000"]]
    table(ax, 6, y, ["state", "binary", "one-hot"], rows, [16, 14, 16], 5.0,
          size=8.6, bold_col=[0])

    rows2 = [["binary", "2", "13", "shortest register"],
             ["one-hot", "4", "30", "shortest decode path"]]
    table(ax, 54, y, ["encoding", "flops", "cells", "what it buys"], rows2,
          [12, 8, 8, 16], 5.0, size=8.2, bold_col=[0], colcolors={2: VIOLET})
    ax.text(76, y - 17.5, "measured by make fsm on this toolchain",
            fontsize=7.8, color=SLATE, ha="center", fontstyle="italic")

    y -= 27.0
    box(ax, 3, y - 18.0, 94, 18.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, y - 3.4, "Read the measurement before repeating the folklore",
            fontsize=9.6, color=RED, ha="center", fontweight="bold")
    ax.text(50, y - 9.0, "On this generic gate library one-hot is BIGGER: "
                         "four states need four flip-flops instead of two, "
                         "and the\nnext-state logic has to drive four bits "
                         "instead of two. 30 cells against 13.",
            fontsize=8.5, color=BODY, ha="center")
    ax.text(50, y - 15.4, "One-hot is still usually right on an FPGA. Both "
                          "statements are true; neither is a rule.",
            fontsize=8.5, color=NAVY, ha="center", fontweight="bold")

    y -= 22.0
    rows3 = [["binary", "fewest flip-flops", "ASIC, many states, area-critical"],
             ["one-hot", "one flop per state, decode is one wire",
              "FPGA, speed-critical, few states"],
             ["gray", "one bit changes per legal transition",
              "the state crosses a clock domain"]]
    table(ax, 3, y, ["encoding", "the property", "where it wins"], rows3,
          [16, 40, 38], 5.0, size=8.3, bold_col=[0])

    box(ax, 3, 3.0, 94, 10.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 10.0, "In Verilog the encoding is yours; in VHDL it is the "
                      "tool's unless you say otherwise",
            fontsize=8.8, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 5.6, "localparam S_IDLE = 2'd0 IS the encoding - you wrote the "
                     "bits. type state_t is (S_IDLE, ...) is a set of NAMES, "
                     "and the\nsynthesiser picks the bits unless an attribute "
                     "tells it otherwise.",
            fontsize=8.3, color=BODY, ha="center")
    save(f, "state_encoding")


for fn in (fsm_pattern, moore_mealy, moore_mealy_timing,
           seq101_moore_states, seq101_mealy_states, traffic_states,
           state_encoding):
    fn()
