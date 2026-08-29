# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — how a real RTL block is put together.

Combinational against sequential, the synchronous discipline, datapath and
controller, the running example, and three measured results from the lab.
"""
import _boot
from dsl import *


def comb_vs_seq():
    W, Hin = 11.5, 9.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The only two kinds of digital logic there are", 12.5)
    ax.text(50, H - 7.0, "Every RTL block you will ever write is some "
                         "arrangement of these two.",
            fontsize=9, color=SLATE, ha="center")

    # ---- combinational -----------------------------------------------
    box(ax, 3, H - 34.0, 45, 23.0, fc=LIGHT, ec=TEAL, lw=1.8)
    ax.text(25.5, H - 13.5, "COMBINATIONAL", fontsize=10.4, color=TEAL,
            ha="center", fontweight="bold")
    ins, outp = gate(ax, "AND", 14, H - 22.5, 9, 7, ec=TEAL)
    ins2, out2 = gate(ax, "OR", 30, H - 22.5, 9, 7, ec=TEAL)
    wire(ax, [(outp[0], outp[1]), (30, H - 22.5)], color=TEAL, lw=1.6)
    for p in ins:
        wire(ax, [(p[0] - 5, p[1]), p], color=TEAL, lw=1.4)
    wire(ax, [(ins2[1][0] - 5, ins2[1][1]), ins2[1]], color=TEAL, lw=1.4)
    wire(ax, [out2, (out2[0] + 5, out2[1])], color=TEAL, lw=1.6)
    ax.text(25.5, H - 30.5, "output = f(inputs RIGHT NOW)", fontsize=8.6,
            color=NAVY, ha="center", family="monospace")
    ax.text(25.5, H - 33.0, "no clock, no memory, no history",
            fontsize=8.3, color=BODY, ha="center")

    # ---- sequential ---------------------------------------------------
    box(ax, 52, H - 34.0, 45, 23.0, fc="#F6F2FC", ec=VIOLET, lw=1.8)
    ax.text(74.5, H - 13.5, "SEQUENTIAL", fontsize=10.4, color=VIOLET,
            ha="center", fontweight="bold")
    label_box(ax, 68, H - 26.0, 14, 9.0, "D    Q", fc=WHITE, ec=VIOLET,
              tc=NAVY, size=9)
    wire(ax, [(60, H - 21.5), (68, H - 21.5)], color=VIOLET, lw=1.6)
    wire(ax, [(82, H - 21.5), (90, H - 21.5)], color=VIOLET, lw=1.6)
    wire(ax, [(70, H - 26.0), (72, H - 24.0), (70, H - 22.0)], color=VIOLET,
         lw=1.4)
    ax.text(66.5, H - 27.6, "clk", fontsize=8, color=VIOLET, ha="center")
    ax.text(74.5, H - 30.5, "output = f(inputs AND past inputs)",
            fontsize=8.6, color=NAVY, ha="center", family="monospace")
    ax.text(74.5, H - 33.0, "state changes only on the clock edge",
            fontsize=8.3, color=BODY, ha="center")

    rows = [["what it is", "logic gates", "flip-flops (and the logic feeding them)"],
            ["Verilog", "always @* ... =", "always @(posedge clk) ... <="],
            ["what it remembers", "nothing", "one value per flip-flop"],
            ["what can go wrong",
             "an inferred latch, a glitch", "a setup or hold violation"],
            ["where it is checked", "simulation, lint", "simulation, lint, STA"]]
    table(ax, 3, H - 36.5, ["", "combinational", "sequential"], rows,
          [22, 30, 42], 4.7, size=8.3, bold_col=[0])

    box(ax, 3, 3.0, 94, 8.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 7.6, "The whole of RTL design is deciding what goes in the "
                     "registers and what happens between them",
            fontsize=9.0, color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 4.4, "That is not a slogan - it is literally what the letters "
                     "R, T and L stand for.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "comb_vs_seq")


def sync_design():
    W, Hin = 11.5, 9.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The synchronous discipline: one clock, one edge, "
                         "everything", 12.5)
    ax.text(50, H - 7.0, "Almost every rule in this topic is a consequence of "
                         "this one decision.",
            fontsize=9, color=SLATE, ha="center")

    yb = H - 30.0
    # three registers with clouds between them
    xs = [10, 40, 70]
    for i, x in enumerate(xs):
        label_box(ax, x, yb, 12, 10.0, "REG", fc=WHITE, ec=VIOLET, tc=VIOLET,
                  size=9.4)
        wire(ax, [(x + 2, yb), (x + 4, yb + 2), (x + 2, yb + 4)], color=VIOLET,
             lw=1.4)
    for i in range(2):
        x0 = xs[i] + 12
        x1 = xs[i + 1]
        box(ax, x0 + 3, yb + 1.5, x1 - x0 - 6, 7.0, fc=LIGHT, ec=TEAL, lw=1.4)
        ax.text((x0 + x1) / 2, yb + 5.0, "logic", fontsize=8.4, color=TEAL,
                ha="center", fontweight="bold")
        wire(ax, [(x0, yb + 5), (x0 + 3, yb + 5)], color=INK, lw=1.4)
        wire(ax, [(x1 - 3, yb + 5), (x1, yb + 5)], color=INK, lw=1.4)
    wire(ax, [(4, yb + 5), (10, yb + 5)], color=INK, lw=1.4)
    wire(ax, [(82, yb + 5), (92, yb + 5)], color=INK, lw=1.4)

    # the clock spine
    wire(ax, [(6, yb - 7.0), (92, yb - 7.0)], color=NAVY, lw=2.4)
    for x in xs:
        wire(ax, [(x + 2, yb - 7.0), (x + 2, yb)], color=NAVY, lw=1.8)
        dot(ax, x + 2, yb - 7.0, color=NAVY, s=14)
    ax.text(6, yb - 9.6, "clk  —  ONE clock, reaching every register",
            fontsize=8.8, color=NAVY, ha="left", fontweight="bold")

    rows = [["one clock edge", "every register samples at the same instant",
             "so 'now' means the same thing everywhere"],
            ["one reset policy", "sync or async, active high or low - pick one",
             "so nobody has to look it up per module"],
            ["no logic on the clock", "no gated clocks, no ripple clocks",
             "so STA has one thing to analyse"],
            ["no latches", "assign every output on every path",
             "so timing is edge-to-edge, not level-dependent"],
            ["registered outputs", "a block's outputs come out of flops",
             "so a slow path never crosses two blocks"]]
    table(ax, 3, yb - 12.0, ["the rule", "what it means", "why"], rows,
          [22, 38, 34], 4.8, size=8.3, bold_col=[0])

    box(ax, 3, 3.0, 94, 11.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, 10.6, "You are allowed to break these rules. You are not "
                      "allowed to break them by accident.",
            fontsize=9.0, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 6.0, "Clock gating and multiple clock domains are real "
                     "techniques - deliberate, reviewed and constrained.\n"
                     "That is a different thing from a design that drifted "
                     "out of the discipline without anyone deciding.",
            fontsize=8.3, color=BODY, ha="center")
    save(f, "sync_design")


def datapath_controller():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Datapath and controller: the shape of almost every "
                         "block", 12.5)
    ax.text(50, H - 7.0, "A UART, a cache, a GPU. Different sizes, same two "
                         "halves.", fontsize=9, color=SLATE, ha="center")

    yt = H - 12.0
    # controller
    box(ax, 6, yt - 17.0, 30, 17.0, fc="#F6F2FC", ec=VIOLET, lw=1.9)
    ax.text(21, yt - 3.4, "CONTROLLER", fontsize=10.2, color=VIOLET,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["a finite state machine", "narrow  ·  all decisions",
                            "measured: 10 cells, 2 flops"]):
        ax.text(21, yt - 7.4 - i * 3.3, ln, fontsize=8.3,
                color=BODY if i < 2 else VIOLET, ha="center",
                fontweight="normal" if i < 2 else "bold")

    # datapath
    box(ax, 64, yt - 17.0, 30, 17.0, fc=LIGHT, ec=TEAL, lw=1.9)
    ax.text(79, yt - 3.4, "DATAPATH", fontsize=10.2, color=TEAL,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["registers, adders, muxes", "wide  ·  no decisions",
                            "measured: 145 cells, 24 flops"]):
        ax.text(79, yt - 7.4 - i * 3.3, ln, fontsize=8.3,
                color=BODY if i < 2 else TEAL, ha="center",
                fontweight="normal" if i < 2 else "bold")

    # the two bundles
    arrow(ax, 36, yt - 5.5, 64, 5.5 + yt - 11.0, color=VIOLET, lw=2.4, ms=13)
    ax.text(50, yt - 3.8, "CONTROL", fontsize=8.8, color=VIOLET, ha="center",
            fontweight="bold")
    ax.text(50, yt - 6.6, "acc_clr  acc_en  cnt_ld  cnt_dec", fontsize=7.8,
            color=SLATE, ha="center", family="monospace")

    arrow(ax, 64, yt - 14.0, 36, yt - 14.0, color=TEAL, lw=2.4, ms=13)
    ax.text(50, yt - 11.8, "STATUS", fontsize=8.8, color=TEAL, ha="center",
            fontweight="bold")
    ax.text(50, yt - 16.2, "cnt_done", fontsize=7.8, color=SLATE, ha="center",
            family="monospace")

    ax.text(50, yt - 21.0, "Two thin bundles of wires. That is the entire "
                           "interface between the two halves.",
            fontsize=8.8, color=NAVY, ha="center", fontweight="bold")

    rows = [["you re-time the datapath", "the state machine does not change"],
            ["you re-specify the sequence", "no adder is touched"],
            ["you widen the data", "the controller is width-independent"],
            ["you review the design", "one half is 10 cells and can be read"]]
    table(ax, 12, yt - 24.0, ["when...", "...this is why it is cheap"], rows,
          [38, 38], 4.8, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 8.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 7.6, "make dpctrl   —   the accumulator, its FSM, and every "
                     "control signal printed per cycle",
            fontsize=8.8, color=GREEN, ha="center", fontweight="bold",
            family="monospace")
    ax.text(50, 4.4, "The controller is 6% of the cells and 100% of the "
                     "behaviour. That ratio is the reason for the split.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "datapath_controller")


def running_example():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The running example: a 4-bit counter", 12.5)
    ax.text(50, H - 7.0, "One design, carried through the coding, the "
                         "testbench, the flow and the reuse lab.",
            fontsize=9, color=SLATE, ha="center")

    # block symbol
    yb = H - 27.0
    box(ax, 8, yb, 26, 16.0, fc=LIGHT, ec=NAVY, lw=1.9)
    ax.text(21, yb + 13.0, "counter4", fontsize=10.2, color=NAVY, ha="center",
            fontweight="bold", family="monospace")
    for i, p in enumerate(["clk", "rst_n", "en"]):
        yy = yb + 9.5 - i * 3.2
        wire(ax, [(2, yy), (8, yy)], color=INK, lw=1.5)
        ax.text(1.5, yy, p, fontsize=8.2, color=BODY, ha="right", va="center",
                family="monospace")
    for i, p in enumerate(["count[3:0]", "tc"]):
        yy = yb + 8.5 - i * 4.0
        wire(ax, [(34, yy), (40, yy)], color=INK, lw=1.5)
        ax.text(40.6, yy, p, fontsize=8.2, color=BODY, ha="left", va="center",
                family="monospace")

    code = ["always @(posedge clk or negedge rst_n) begin",
            "    if (!rst_n)  count <= 4'd0;",
            "    else if (en) count <= count + 4'd1;",
            "end",
            "assign tc = en & (count == 4'd15);"]
    box(ax, 54, yb - 1.0, 43, 17.0, fc="#FBFCFE", ec=SLATE, lw=1.3)
    for i, ln in enumerate(code):
        ax.text(56, yb + 13.0 - i * 3.0, ln, fontsize=7.6, color=INK,
                ha="left", va="center", family="monospace")

    # waveform
    u = 5.0
    x0, yw = 14.0, 17.0
    n = 8
    clk_wave(ax, x0, yw + 12.0, 9.0, n, u, name="clk")
    wave(ax, x0, yw + 6.0, 9.0, [1] * n, u, color=GREEN, name="en")
    seq = [0, 0, 0, 1, 0, 0, 0, 0]
    wave(ax, x0, yw, 9.0, seq, u, color=AMBER, name="tc")
    for i, v in enumerate(["12", "13", "14", "15", "0", "1", "2", "3"]):
        ax.text(x0 + 9.0 * i + 4.5, yw - 4.2, v, fontsize=8.0, color=NAVY,
                ha="center", family="monospace")
    ax.text(x0 - 1.5, yw - 4.2, "count", fontsize=9, color=NAVY, ha="right",
            fontweight="bold")
    ax.text(x0 + 9.0 * 3 + 4.5, yw + 18.5, "tc is high for exactly one cycle, "
            "while count == 15", fontsize=8.2, color=AMBER, ha="center",
            fontweight="bold")

    box(ax, 3, 3.0, 94, 8.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 7.6, "The same design comes back three times", fontsize=9.0,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.4, "Lab 3 runs it through the whole front end  ·  Lab 4 turns "
                     "its controller into an FSM  ·  Lab 7 parameterises it and "
                     "instantiates it twice",
            fontsize=8.2, color=BODY, ha="center")
    save(f, "running_example")


def mux_styles():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "One function, three coding styles - and three "
                         "netlists", 12.5)
    ax.text(50, H - 7.0, "A 4:1 multiplexer. All 64 patterns simulated; every "
                         "pair proved equivalent by SAT.",
            fontsize=9, color=SLATE, ha="center")

    cols = [("mux4_assign", TEAL,
             ["assign y =", "  sel[1] ? (sel[0]?d[3]:d[2])", "        : (sel[0]?d[1]:d[0]);"],
             "3"),
            ("mux4_if", VIOLET,
             ["if      (sel==2'b00) y = d[0];", "else if (sel==2'b01) y = d[1];",
              "else ...  else       y = d[3];"], "6"),
            ("mux4_case", AMBER,
             ["case (sel)", "  2'b00: y = d[0];  ...", "  default: y = 1'b0;",
              "endcase"], "10")]
    x = 3
    for nm, col, lines, cells in cols:
        box(ax, x, H - 36.0, 30.6, 25.0, fc=WHITE, ec=col, lw=1.7)
        box(ax, x, H - 16.0, 30.6, 5.0, fc=col, ec=col)
        ax.text(x + 15.3, H - 13.5, nm, fontsize=9.4, color=WHITE,
                ha="center", va="center", fontweight="bold",
                family="monospace")
        for i, ln in enumerate(lines):
            ax.text(x + 1.2, H - 19.0 - i * 2.7, ln, fontsize=6.9, color=INK,
                    ha="left", va="center", family="monospace")
        ax.text(x + 15.3, H - 33.0, cells + " cells", fontsize=12.5, color=col,
                ha="center", va="center", fontweight="bold")
        x += 32.7

    box(ax, 3, 15.5, 94, 18.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 30.8, "EQUIVALENT is not the same as IDENTICAL", fontsize=10.2,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 25.5, "The SAT proof says all three compute the same Boolean "
                      "function. It says nothing at all about area or timing,\n"
                      "and on Yosys 0.33 the three netlists are 3, 6 and 10 "
                      "cells.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 18.8, "The conditional expression uses sel[1] and sel[0] "
                      "STRAIGHT as mux selects. The other two build equality\n"
                      "comparators and ask the tool to re-derive that those "
                      "comparisons are the select bits. It does not, quite.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 3, 3.0, 94, 10.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 9.6, "So which do you write?", fontsize=9.4, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(50, 5.4, "Whichever reads best - and then MEASURE, on your own "
                     "tool, if the block is on a critical path.\nFolklore "
                     "about what optimisers do is the least reliable knowledge "
                     "in this field.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "mux_styles")


def blocking_measured():
    W, Hin = 11.5, 9.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Blocking in a clocked block: what it actually builds",
          12.5)
    ax.text(50, H - 7.0, "The same three lines. One character different on "
                         "each. make pitfalls",
            fontsize=9, color=SLATE, ha="center")

    pairs = [("shift_nb   —   correct", GREEN,
              ["always @(posedge clk) begin", "    q[0] <= din;",
               "    q[1] <= q[0];", "    q[2] <= q[1];", "end"],
              "3 flip-flops", "a 3-stage delay line"),
             ("shift_bl   —   not a shift register", RED,
              ["always @(posedge clk) begin", "    q[0] = din;",
               "    q[1] = q[0];", "    q[2] = q[1];", "end"],
              "1 flip-flop", "din reaches q[2] in ONE cycle")]
    x = 3
    for nm, col, lines, ff, what in pairs:
        box(ax, x, H - 40.0, 46, 29.0, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, H - 16.5, 46, 5.5, fc=col, ec=col)
        ax.text(x + 23, H - 13.7, nm, fontsize=9.4, color=WHITE, ha="center",
                va="center", fontweight="bold")
        for i, ln in enumerate(lines):
            ax.text(x + 2.5, H - 20.0 - i * 2.9, ln, fontsize=7.8, color=INK,
                    ha="left", va="center", family="monospace")
        ax.text(x + 23, H - 35.6, ff, fontsize=11.5, color=col, ha="center",
                fontweight="bold")
        ax.text(x + 23, H - 38.6, what, fontsize=8.3, color=BODY, ha="center")
        x += 48

    rows = [["2", "0", "100", "000", "1"],
            ["4", "1", "001", "111", "0"],
            ["6", "0", "110", "000", "1"]]
    table(ax, 16, H - 42.0, ["cycle", "din", "q_nb", "q_bl", "expected q[2]"],
          rows, [12, 12, 16, 16, 22], 4.6, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 13.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 13.0, "non-blocking: 0 wrong cycles      ·      blocking: 6 "
                      "wrong cycles out of 10 checked",
            fontsize=9.4, color=RED, ha="center", fontweight="bold")
    ax.text(50, 7.6, "It compiled. It simulated. It synthesised. No tool "
                     "issued a single warning, because nothing illegal was "
                     "written -\nthe code simply describes a different circuit "
                     "from the one the author had in mind.",
            fontsize=8.5, color=BODY, ha="center")
    ax.text(50, 4.0, "This is what a methodology rule is FOR. Rule L001 in the "
                     "lab linter catches it in about a millisecond.",
            fontsize=8.4, color=NAVY, ha="center", fontweight="bold")
    save(f, "blocking_measured")


def hierarchy_generate():
    W, Hin = 11.5, 8.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "From module to IP: parameters, hierarchy, generate",
          12.5)
    ax.text(50, H - 7.0, "Reusable means ONE file that covers a family of "
                         "widths and depths.",
            fontsize=9, color=SLATE, ha="center")

    # the source
    box(ax, 3, H - 32.0, 42, 21.0, fc="#FBFCFE", ec=SLATE, lw=1.4)
    src = ["genvar k;", "generate", "  for (k=0; k<N; k=k+1) begin : stage",
           "    preg #(.W(W)) u_reg (", "      .d(tap[k]), .q(tap[k+1]));",
           "  end", "endgenerate"]
    for i, ln in enumerate(src):
        ax.text(5, H - 14.0 - i * 2.7, ln, fontsize=7.6, color=INK, ha="left",
                va="center", family="monospace")
    ax.text(24, H - 34.6, "what you write", fontsize=8.6, color=SLATE,
            ha="center", fontweight="bold")

    arrow(ax, 46, H - 21.0, 53, H - 21.0, color=NAVY, lw=2.4, ms=13)
    ax.text(49.5, H - 18.2, "elaborate", fontsize=7.6, color=NAVY,
            ha="center", fontweight="bold")

    # elaborated chain
    for i in range(4):
        x = 55 + i * 10.5
        label_box(ax, x, H - 25.0, 8.5, 8.0, "preg", fc=WHITE, ec=VIOLET,
                  tc=VIOLET, size=8)
        if i:
            wire(ax, [(x - 2, H - 21.0), (x, H - 21.0)], color=INK, lw=1.4)
    wire(ax, [(52, H - 21.0), (55, H - 21.0)], color=INK, lw=1.4)
    wire(ax, [(95.5, H - 21.0), (97, H - 21.0)], color=INK, lw=1.4)
    ax.text(76, H - 34.6, "what gets built  (N = 4)", fontsize=8.6, color=SLATE,
            ha="center", fontweight="bold")
    ax.text(76, H - 30.0, "no loop survives into hardware", fontsize=8.0,
            color=VIOLET, ha="center", fontstyle="italic")

    rows = [["1", "8", "8"], ["2", "16", "16"], ["4", "32", "32"],
            ["8", "64", "64"]]
    table(ax, 22, H - 37.0, ["N", "cells", "flip-flops"], rows,
          [18, 19, 19], 4.6, size=8.6, bold_col=[0], colcolors={2: VIOLET})

    box(ax, 3, 3.0, 94, 11.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 10.6, "Eight flip-flops per stage, exactly N stages, measured "
                      "at four depths",
            fontsize=9.2, color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 6.0, "parameter, hierarchy and generate are all instructions "
                     "to the ELABORATOR. None of them exists in the netlist;\n"
                     "they are gone before synthesis sees its first gate.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "hierarchy_generate")


def numerical_example():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "A worked numerical example", 12.5)
    ax.text(50, H - 7.0, "The counter and the accumulator, with the arithmetic "
                         "written out.",
            fontsize=9, color=SLATE, ha="center")

    box(ax, 3, H - 34.0, 45.5, 23.0, fc=LIGHT, ec=NAVY, lw=1.7)
    ax.text(25.7, H - 13.6, "counter4 at 100 MHz", fontsize=9.8, color=NAVY,
            ha="center", fontweight="bold")
    lines = [("clock period", "1 / 100 MHz = 10 ns"),
             ("states before it wraps", "2^4 = 16"),
             ("time for one full cycle", "16 x 10 ns = 160 ns"),
             ("tc pulse rate", "1 / 160 ns = 6.25 MHz"),
             ("tc pulse width", "10 ns - exactly one clock")]
    for i, (a, b) in enumerate(lines):
        ax.text(5.5, H - 17.8 - i * 3.1, a, fontsize=8.2, color=BODY,
                ha="left", va="center")
        ax.text(46, H - 17.8 - i * 3.1, b, fontsize=8.2, color=NAVY,
                ha="right", va="center", family="monospace",
                fontweight="bold")

    box(ax, 51.5, H - 34.0, 45.5, 23.0, fc="#F6F2FC", ec=VIOLET, lw=1.7)
    ax.text(74.2, H - 13.6, "accum_top, N = 6 samples", fontsize=9.8,
            color=VIOLET, ha="center", fontweight="bold")
    lines = [("cycle 0", "start seen, sum cleared, cnt <- 6"),
             ("cycles 1..6", "one sample added per clock"),
             ("cycle 7", "cnt reached 0, machine moves on"),
             ("cycle 8", "done pulses, sum is valid"),
             ("total latency", "N + 3 = 9 clocks")]
    for i, (a, b) in enumerate(lines):
        ax.text(54, H - 17.8 - i * 3.1, a, fontsize=8.2, color=BODY,
                ha="left", va="center", family="monospace")
        ax.text(94.5, H - 17.8 - i * 3.1, b, fontsize=7.8, color=VIOLET,
                ha="right", va="center")

    box(ax, 3, 15.0, 94, 18.5, fc=WHITE, ec=TEAL, lw=1.7)
    ax.text(50, 30.8, "Why the latency formula is worth deriving rather than "
                      "measuring",
            fontsize=9.4, color=TEAL, ha="center", fontweight="bold")
    ax.text(50, 25.0, "One cycle to accept the request, N to accumulate, one "
                      "to notice the counter hit zero, one to flag it.\n"
                      "That is N + 3, and it holds for every N - so a "
                      "testbench that only ever tries N = 6 has told you almost "
                      "nothing.",
            fontsize=8.5, color=BODY, ha="center")
    ax.text(50, 17.6, "The measured run agrees: sum = 157 for samples "
                      "10+20+30+40+50+7, done at cycle 8.",
            fontsize=8.5, color=NAVY, ha="center", fontweight="bold")

    box(ax, 3, 3.0, 94, 11.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, 10.6, "Throughput, not latency, is what usually matters",
            fontsize=9.2, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 6.0, "This design accepts one sample per clock while it is "
                     "running: 100 M samples/s at 100 MHz.\nThe three extra "
                     "cycles are paid once per batch, not once per sample.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "numerical_example")


for fn in (comb_vs_seq, sync_design, datapath_controller, running_example,
           mux_styles, blocking_measured, hierarchy_generate,
           numerical_example):
    fn()
