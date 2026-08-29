# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — finite state machines.

Drawn to the shared readability budget in dsl.py: wide, short, and large
enough to read from the back of a room.
"""
import _boot
from dsl import *


def _state(ax, x, y, r, name, col=NAVY, fc=WHITE, sub=None, size=FS_SMALL):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=col, lw=2.0, zorder=4))
    ax.text(x, y + (1.0 if sub else 0), name, ha="center", va="center",
            fontsize=size, color=col, fontweight="bold", zorder=5,
            family="monospace")
    if sub:
        ax.text(x, y - 2.2, sub, ha="center", va="center", fontsize=FS_SMALL - 1,
                color=SLATE, zorder=5)


def _selfloop(ax, x, y, r, label, col=SLATE, h=3.2):
    top = y + r + h
    wire(ax, [(x - 2.6, y + r * 0.9), (x - 2.6, top), (x + 2.6, top)],
         color=col, lw=1.6)
    arrow(ax, x + 2.6, top, x + 2.6, y + r * 0.9, color=col, lw=1.6, ms=9)
    ax.text(x, top + 2.4, label, ha="center", va="center", fontsize=FS_SMALL,
            color=col, family="monospace", fontweight="bold")


def _backedge(ax, xa, xb, y, r, depth, label, col=SLATE, lx=None):
    yy = y - r - depth
    wire(ax, [(xa, y - r), (xa, yy), (xb, yy)], color=col, lw=1.6)
    arrow(ax, xb, yy, xb, y - r, color=col, lw=1.6, ms=9)
    ax.text(lx if lx is not None else (xa + xb) / 2, yy - 2.6, label,
            ha="center", va="center", fontsize=FS_SMALL, color=col,
            family="monospace", fontweight="bold")


def fsm_pattern():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "How to write a state machine: the three-block "
                           "pattern", FS_TITLE)

    blocks = [("BLOCK 1", "state register", VIOLET,
               ["always @(posedge clk or negedge rst_n)",
                "    if (!rst_n) state <= S_IDLE;",
                "    else        state <= next_state;"],
               "sequential  ·  <=  ·  reset lives HERE"),
              ("BLOCK 2", "next-state logic", TEAL,
               ["always @(*) begin",
                "    next_state = state;    // the default",
                "    case (state) ... endcase   end"],
               "combinational  ·  =  ·  no latch"),
              ("BLOCK 3", "output logic", GREEN,
               ["always @(*) begin",
                "    out = 1'b0;            // defaults",
                "    case (state) ... endcase   end"],
               "state only => MOORE")]
    y = H - 9.5
    bh = 11.0
    for tag, nm, col, code, note in blocks:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, 3, y - bh, 21, bh, fc=col, ec=col)
        ax.text(13.5, y - 4.0, tag, ha="center", va="center", fontsize=FS_HEAD,
                color=WHITE, fontweight="bold")
        ax.text(13.5, y - 7.6, nm, ha="center", va="center", fontsize=FS_SMALL,
                color=WHITE)
        for i, ln in enumerate(code):
            ax.text(26, y - 2.6 - i * 2.9, ln, ha="left", va="center",
                    fontsize=9.6, color=INK, family="monospace")
        ax.text(95, y - bh + 2.0, note, ha="right", va="center",
                fontsize=FS_SMALL, color=col, fontstyle="italic")
        y -= bh + 1.9
    save(f, "fsm_pattern")


def moore_mealy():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Moore and Mealy: where the output comes from",
          FS_TITLE)
    ax.text(50, H - 10.0, "One structural difference - whether the output logic "
                          "can see the input. Everything else follows.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    def machine(x0, name, col, mealy):
        box(ax, x0, 4.0, 46, H - 18.0, fc=WHITE, ec=col, lw=2.0)
        ax.text(x0 + 23, H - 18.5, name, fontsize=FS_HEAD + 2, color=col,
                ha="center", fontweight="bold")
        yb = 13.0
        label_box(ax, x0 + 3, yb, 12, 9.0, "next\nstate", fc=LIGHT, ec=TEAL,
                  tc=TEAL, size=FS_SMALL)
        label_box(ax, x0 + 18, yb, 10, 9.0, "REG", fc=WHITE, ec=VIOLET,
                  tc=VIOLET, size=FS_SMALL)
        label_box(ax, x0 + 31, yb, 12, 9.0, "output\nlogic", fc="#EEF7F1",
                  ec=GREEN, tc=GREEN, size=FS_SMALL)
        wire(ax, [(x0 + 15, yb + 4.5), (x0 + 18, yb + 4.5)], color=INK, lw=1.6)
        wire(ax, [(x0 + 28, yb + 4.5), (x0 + 31, yb + 4.5)], color=INK, lw=1.6)
        wire(ax, [(x0 + 43, yb + 4.5), (x0 + 45, yb + 4.5)], color=INK, lw=1.6)
        wire(ax, [(x0 + 1, yb + 4.5), (x0 + 3, yb + 4.5)], color=INK, lw=1.6)
        ax.text(x0 + 3.2, yb + 6.8, "in", fontsize=FS_SMALL, color=BODY,
                ha="center", family="monospace")
        ax.text(x0 + 42.6, yb + 6.8, "out", fontsize=FS_SMALL, color=BODY,
                ha="center", family="monospace")
        wire(ax, [(x0 + 28.5, yb), (x0 + 28.5, yb - 4.5), (x0 + 9, yb - 4.5),
                  (x0 + 9, yb)], color=VIOLET, lw=1.6)
        ax.text(x0 + 19, yb - 6.6, "state", fontsize=FS_SMALL, color=VIOLET,
                ha="center")
        if mealy:
            wire(ax, [(x0 + 2, yb + 4.5), (x0 + 2, yb + 13.0),
                      (x0 + 37, yb + 13.0), (x0 + 37, yb + 9.0)],
                 color=RED, lw=2.0)
            ax.text(x0 + 23, yb + 15.0, "the input reaches the OUTPUT directly",
                    fontsize=FS_SMALL, color=RED, ha="center",
                    fontweight="bold")
        else:
            ax.text(x0 + 23, yb + 15.0, "the output sees the STATE, and nothing "
                    "else", fontsize=FS_SMALL, color=GREEN, ha="center",
                    fontweight="bold")

    machine(3, "MOORE", GREEN, False)
    machine(51, "MEALY", RED, True)
    save(f, "moore_mealy")


def moore_mealy_table():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Choosing between Moore and Mealy", FS_TITLE)

    rows = [["output depends on", "state only", "state AND input"],
            ["output appears", "one cycle after the input", "the same cycle"],
            ["output glitches", "no - decoded from registers",
             "yes - inherits the input's"],
            ["states needed", "usually one more", "usually one fewer"],
            ["measured here", "13 cells, 2 flip-flops", "14 cells, 2 flip-flops"],
            ["use it when", "the output leaves the block",
             "you cannot afford the cycle"]]
    table(ax, 3, H - 9.0, ["", "MOORE", "MEALY"], rows, [24, 35, 35], 4.8,
          size=FS_TABLE, bold_col=[0], colcolors={1: GREEN, 2: RED})

    ax.text(50, 3.0, "Both accept exactly the same language. They differ in WHEN "
                     "they say so, not in WHAT they say.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "moore_mealy_table")


def moore_mealy_timing():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The one-cycle difference, measured", FS_TITLE)
    ax.text(50, H - 10.0, "One stream into both detectors, both checked against "
                          "a golden model.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    din = [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    mealy = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1]
    moore = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]

    x0, wdt, u = 15.0, 4.9, 5.2
    yd = H - 19.5
    wave(ax, x0, yd, wdt, din, u, color=NAVY, name="din",
         name_size=FS_SMALL, label_dx=2.0)
    wave(ax, x0, yd - 10.0, wdt, mealy, u, color=RED, name="det (Mealy)",
         name_size=FS_SMALL, label_dx=2.0)
    wave(ax, x0, yd - 20.0, wdt, moore, u, color=GREEN, name="det (Moore)",
         name_size=FS_SMALL, label_dx=2.0)

    for i in range(17):
        ax.text(x0 + wdt * i + wdt / 2, yd + 5.4, str(i), fontsize=FS_SMALL - 1,
                color=SLATE, ha="center")

    for i, v in enumerate(mealy):
        if v and i + 1 < len(moore) and moore[i + 1]:
            xc = x0 + wdt * i + wdt / 2
            arrow(ax, xc, yd - 11.6, xc + wdt, yd - 15.4, color=AMBER, lw=1.6,
                  ms=9, rad=-0.3)

    ax.text(50, 2.5, "5 matches  ·  0 mismatches  ·  Moore trails Mealy by "
                     "exactly one cycle, every time",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "moore_mealy_timing")


def seq101_moore_states():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The '101' detector as a MOORE state diagram",
          FS_TITLE)

    r, ym = 5.4, H - 20.0
    xs = [14, 38, 62, 86]
    names = [("S_IDLE", "det=0"), ("S_1", "det=0"), ("S_10", "det=0"),
             ("S_101", "det=1")]
    for i, (x, (nm, sub)) in enumerate(zip(xs, names)):
        _state(ax, x, ym, r, nm, col=GREEN if i == 3 else NAVY,
               fc="#EEF7F1" if i == 3 else WHITE, sub=sub)
    for i in range(3):
        arrow(ax, xs[i] + r, ym, xs[i + 1] - r, ym, color=SLATE, lw=1.8, ms=11)
        ax.text((xs[i] + xs[i + 1]) / 2, ym + 2.6, ["1", "0", "1"][i],
                fontsize=FS_BODY, color=NAVY, ha="center", family="monospace",
                fontweight="bold")
    _selfloop(ax, xs[0], ym, r, "0")
    _selfloop(ax, xs[1], ym, r, "1")
    _backedge(ax, xs[2], xs[0], ym, r, 4.5, "0", lx=26)
    _backedge(ax, xs[3], xs[2], ym, r, 4.5, "0", lx=74)
    _backedge(ax, xs[3], xs[1], ym, r, 10.5, "1   (the overlapping match)",
              col=GREEN, lx=62)

    ax.text(50, 2.5, "The fourth state exists only to say 'a match just "
                     "finished'.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "seq101_moore_states")


def seq101_mealy_states():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The same detector as a MEALY state diagram",
          FS_TITLE)
    ax.text(50, H - 10.0, "Three states. Each arrow is labelled input / output.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    r, ye = 5.4, H - 22.0
    xs2 = [22, 50, 78]
    for x, nm in zip(xs2, ["S_IDLE", "S_1", "S_10"]):
        _state(ax, x, ye, r, nm, col=NAVY)
    for i in range(2):
        arrow(ax, xs2[i] + r, ye, xs2[i + 1] - r, ye, color=SLATE, lw=1.8,
              ms=11)
        ax.text((xs2[i] + xs2[i + 1]) / 2, ye + 2.6, ["1/0", "0/0"][i],
                fontsize=FS_BODY, color=NAVY, ha="center", family="monospace",
                fontweight="bold")
    _selfloop(ax, xs2[0], ye, r, "0/0")
    _selfloop(ax, xs2[1], ye, r, "1/0")
    _backedge(ax, xs2[2], xs2[1], ye, r, 4.5, "1 / 1   <- the detection",
              col=RED, lx=64)
    _backedge(ax, xs2[2], xs2[0], ye, r, 10.5, "0/0", lx=36)

    ax.text(50, 2.5, "The detection lives on an arrow, not in a state.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "seq101_mealy_states")


def traffic_states():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "A Moore controller with a datapath timer", FS_TITLE)

    import math
    cx, cy, R, r = 26.0, 20.0, 13.0, 6.2
    labels = [("S_MAIN\nGREEN", GREEN), ("S_MAIN\nYELLOW", AMBER),
              ("S_SIDE\nGREEN", GREEN), ("S_SIDE\nYELLOW", AMBER)]
    pts = []
    for i, (nm, col) in enumerate(labels):
        a = math.pi / 2 - i * math.pi / 2
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y))
        ax.add_patch(Circle((x, y), r, fc=WHITE, ec=col, lw=2.2, zorder=4))
        ax.text(x, y, nm, ha="center", va="center", fontsize=FS_SMALL - 1.5,
                color=col, fontweight="bold", zorder=5, family="monospace")
    conds = ["car &&\ntimeout", "timeout", "timeout", "timeout"]
    for i in range(4):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % 4]
        arrow(ax, x1 + (x2 - x1) * 0.34, y1 + (y2 - y1) * 0.34,
              x1 + (x2 - x1) * 0.66, y1 + (y2 - y1) * 0.66,
              color=SLATE, lw=2.0, ms=12)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + (mx - cx) * 0.34, my + (my - cy) * 0.34, conds[i],
                fontsize=FS_SMALL - 1, color=NAVY, ha="center", va="center",
                family="monospace")

    rows = [["S_MAIN_GREEN", "GREEN", "RED", "6"],
            ["S_MAIN_YELLOW", "AMBER", "RED", "2"],
            ["S_SIDE_GREEN", "RED", "GREEN", "6"],
            ["S_SIDE_YELLOW", "RED", "AMBER", "2"]]
    table(ax, 52, H - 11.0, ["state", "MAIN", "SIDE", "cycles"], rows,
          [18, 10, 10, 9], 4.6, size=FS_TABLE - 0.5, bold_col=[0])

    ax.text(75.5, 11.5, "40 cycles checked, 0 property violations",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    ax.text(75.5, 7.0, "75 cells, 10 flip-flops - 2 for the state,",
            fontsize=FS_SMALL, color=VIOLET, ha="center")
    ax.text(75.5, 3.5, "8 for the timer that counts out each phase",
            fontsize=FS_SMALL, color=VIOLET, ha="center")
    save(f, "traffic_states")


def state_encoding():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "State encoding: the choice you make by typing "
                           "numbers", FS_TITLE)

    rows = [["S_IDLE", "2'b00", "4'b0001"],
            ["S_1", "2'b01", "4'b0010"],
            ["S_10", "2'b10", "4'b0100"],
            ["S_101", "2'b11", "4'b1000"]]
    table(ax, 4, H - 10.0, ["state", "binary", "one-hot"], rows,
          [15, 14, 16], 5.0, size=FS_TABLE, bold_col=[0])

    rows2 = [["binary", "2", "13"], ["one-hot", "4", "30"]]
    table(ax, 55, H - 10.0, ["encoding", "flip-flops", "cells"], rows2,
          [14, 14, 13], 5.0, size=FS_TABLE, bold_col=[0],
          colcolors={2: VIOLET})
    ax.text(75.5, H - 27.0, "measured by  make fsm", fontsize=FS_SMALL,
            color=SLATE, ha="center", fontstyle="italic", family="monospace")

    ax.text(50, 8.0, "On this generic gate library one-hot came out BIGGER, "
                     "not smaller.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    ax.text(50, 3.5, "Four states need four flip-flops instead of two, and the "
                     "next-state logic drives four bits instead of two.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "state_encoding")


def state_encoding_choice():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Which encoding, and when", FS_TITLE)

    rows = [["binary", "fewest flip-flops",
             "ASIC, many states, area-critical"],
            ["one-hot", "one flip-flop per state; every decode is one wire",
             "FPGA, speed-critical, few states"],
            ["gray", "one bit changes per legal transition",
             "the state vector crosses a clock domain"]]
    table(ax, 3, H - 9.5, ["encoding", "the property", "where it wins"], rows,
          [16, 43, 35], 6.4, size=FS_TABLE, bold_col=[0])

    ax.text(50, 10.0, "In Verilog the encoding is yours. In VHDL it is the "
                      "tool's, unless you say otherwise.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 5.0, "localparam S_IDLE = 2'd0        you wrote the bits",
            fontsize=FS_SMALL - 1, color=BODY, ha="center", family="monospace")
    ax.text(50, 1.8, "type state_t is (S_IDLE, ...)   the tool picks the bits",
            fontsize=FS_SMALL - 1, color=BODY, ha="center", family="monospace")
    save(f, "state_encoding_choice")


for fn in (fsm_pattern, moore_mealy, moore_mealy_table, moore_mealy_timing,
           seq101_moore_states, seq101_mealy_states, traffic_states,
           state_encoding, state_encoding_choice):
    fn()
