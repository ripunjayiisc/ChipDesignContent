# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — how a real RTL block is put together.

Every panel here is drawn to the shared readability budget in dsl.py: wide and
short, so it fills the slide's width and its text lands at the size it is set.
Prose that used to live in a box at the bottom of these panels is now a card on
the slide instead.
"""
import _boot
from dsl import *


def comb_vs_seq():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The only two kinds of digital logic there are",
          FS_TITLE)
    ax.text(50, H - 10.0, "Every RTL block you will ever write is some "
                          "arrangement of these two.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    top = H - 14.0
    bh = 27.0

    # ---- combinational -------------------------------------------------
    box(ax, 3, top - bh, 46, bh, fc=LIGHT, ec=TEAL, lw=2.0)
    ax.text(26, top - 4.6, "COMBINATIONAL", fontsize=FS_HEAD + 1, color=TEAL,
            ha="center", fontweight="bold")
    ins, outp = gate(ax, "AND", 12, top - 13.0, 10, 8, ec=TEAL)
    ins2, out2 = gate(ax, "OR", 29, top - 13.0, 10, 8, ec=TEAL)
    wire(ax, [outp, (29, top - 13.0)], color=TEAL, lw=1.8)
    for pt in ins:
        wire(ax, [(pt[0] - 5, pt[1]), pt], color=TEAL, lw=1.6)
    wire(ax, [(ins2[1][0] - 5, ins2[1][1]), ins2[1]], color=TEAL, lw=1.6)
    wire(ax, [out2, (out2[0] + 5, out2[1])], color=TEAL, lw=1.8)
    ax.text(26, top - 21.0, "output = f(inputs RIGHT NOW)", fontsize=FS_BODY,
            color=NAVY, ha="center", family="monospace")
    ax.text(26, top - 25.0, "no clock  ·  no memory  ·  no history",
            fontsize=FS_BODY, color=BODY, ha="center")

    # ---- sequential ----------------------------------------------------
    box(ax, 51, top - bh, 46, bh, fc="#F6F2FC", ec=VIOLET, lw=2.0)
    ax.text(74, top - 4.6, "SEQUENTIAL", fontsize=FS_HEAD + 1, color=VIOLET,
            ha="center", fontweight="bold")
    label_box(ax, 68, top - 17.5, 15, 10.0, "D      Q", fc=WHITE, ec=VIOLET,
              tc=NAVY, size=FS_BODY)
    wire(ax, [(59, top - 12.5), (68, top - 12.5)], color=VIOLET, lw=1.8)
    wire(ax, [(83, top - 12.5), (92, top - 12.5)], color=VIOLET, lw=1.8)
    wire(ax, [(68, top - 15.5), (71, top - 12.5), (68, top - 9.5)],
         color=VIOLET, lw=1.6)
    ax.text(66.5, top - 16.6, "clk", fontsize=FS_SMALL, color=VIOLET,
            ha="right", va="center")
    ax.text(74, top - 21.0, "output = f(inputs AND the past)", fontsize=FS_BODY,
            color=NAVY, ha="center", family="monospace")
    ax.text(74, top - 25.0, "state changes only on the clock edge",
            fontsize=FS_BODY, color=BODY, ha="center")

    ax.text(50, 4.0, "There is no third kind.", fontsize=FS_HEAD, color=GREEN,
            ha="center", fontweight="bold")
    save(f, "comb_vs_seq")


def comb_vs_seq_table():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Combinational and sequential, side by side",
          FS_TITLE)

    rows = [["what it is", "logic gates", "flip-flops, and the logic feeding them"],
            ["how you write it", "always @* ... =", "always @(posedge clk) ... <="],
            ["what it remembers", "nothing", "one value per flip-flop"],
            ["what goes wrong", "an inferred latch, a glitch",
             "a setup or a hold violation"],
            ["what checks it", "simulation, lint", "simulation, lint, and STA"]]
    table(ax, 3, H - 10.0, ["", "COMBINATIONAL", "SEQUENTIAL"], rows,
          [24, 33, 37], 5.4, size=FS_TABLE, bold_col=[0],
          colcolors={1: TEAL, 2: VIOLET})

    ax.text(50, 4.5, "The whole of RTL design is deciding what goes in the "
                     "registers,\nand what happens between them.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "comb_vs_seq_table")


def sync_design():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The synchronous discipline: one clock, one edge, "
                           "everything", FS_TITLE)

    yb = H - 26.0
    xs = [12, 42, 72]
    for x in xs:
        label_box(ax, x, yb, 14, 12.0, "REG", fc=WHITE, ec=VIOLET, tc=VIOLET,
                  size=FS_HEAD)
        wire(ax, [(x, yb + 3.0), (x + 3, yb + 6.0), (x, yb + 9.0)],
             color=VIOLET, lw=1.6)
    for i in range(2):
        x0, x1 = xs[i] + 14, xs[i + 1]
        box(ax, x0 + 3, yb + 2.0, x1 - x0 - 6, 8.0, fc=LIGHT, ec=TEAL, lw=1.6)
        ax.text((x0 + x1) / 2, yb + 6.0, "logic", fontsize=FS_BODY, color=TEAL,
                ha="center", va="center", fontweight="bold")
        wire(ax, [(x0, yb + 6), (x0 + 3, yb + 6)], color=INK, lw=1.6)
        wire(ax, [(x1 - 3, yb + 6), (x1, yb + 6)], color=INK, lw=1.6)
    wire(ax, [(5, yb + 6), (12, yb + 6)], color=INK, lw=1.6)
    wire(ax, [(86, yb + 6), (95, yb + 6)], color=INK, lw=1.6)

    wire(ax, [(8, yb - 8.0), (95, yb - 8.0)], color=NAVY, lw=2.8)
    for x in xs:
        wire(ax, [(x + 3, yb - 8.0), (x + 3, yb)], color=NAVY, lw=2.0)
        dot(ax, x + 3, yb - 8.0, color=NAVY, s=16)
    ax.text(8, yb - 12.5, "clk", fontsize=FS_HEAD, color=NAVY, ha="left",
            fontweight="bold")
    ax.text(16, yb - 12.5, "one clock, reaching every register, and every "
                           "register sampling at the same instant",
            fontsize=FS_BODY, color=BODY, ha="left")

    ax.text(50, 4.0, "You are allowed to break this. You are not allowed to "
                     "break it by accident.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    save(f, "sync_design")


def datapath_controller():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Datapath and controller: the shape of almost every "
                           "block", FS_TITLE)

    top = H - 11.0
    bh = 21.0

    box(ax, 3, top - bh, 33, bh, fc="#F6F2FC", ec=VIOLET, lw=2.2)
    ax.text(19.5, top - 4.6, "CONTROLLER", fontsize=FS_HEAD + 1, color=VIOLET,
            ha="center", fontweight="bold")
    ax.text(19.5, top - 10.0, "a finite state machine", fontsize=FS_BODY,
            color=BODY, ha="center")
    ax.text(19.5, top - 14.0, "narrow  ·  all the decisions", fontsize=FS_BODY,
            color=BODY, ha="center")
    ax.text(19.5, top - 18.4, "10 cells,  2 flip-flops", fontsize=FS_BODY,
            color=VIOLET, ha="center", fontweight="bold")

    box(ax, 64, top - bh, 33, bh, fc=LIGHT, ec=TEAL, lw=2.2)
    ax.text(80.5, top - 4.6, "DATAPATH", fontsize=FS_HEAD + 1, color=TEAL,
            ha="center", fontweight="bold")
    ax.text(80.5, top - 10.0, "registers, adders, muxes", fontsize=FS_BODY,
            color=BODY, ha="center")
    ax.text(80.5, top - 14.0, "wide  ·  no decisions", fontsize=FS_BODY,
            color=BODY, ha="center")
    ax.text(80.5, top - 18.4, "145 cells,  24 flip-flops", fontsize=FS_BODY,
            color=TEAL, ha="center", fontweight="bold")

    arrow(ax, 36, top - 7.0, 64, top - 7.0, color=VIOLET, lw=2.6, ms=15)
    ax.text(50, top - 4.0, "CONTROL", fontsize=FS_BODY, color=VIOLET,
            ha="center", fontweight="bold")
    ax.text(50, top - 10.2, "acc_clr  acc_en", fontsize=FS_MONO, color=SLATE,
            ha="center", family="monospace")
    ax.text(50, top - 13.4, "cnt_ld  cnt_dec", fontsize=FS_MONO, color=SLATE,
            ha="center", family="monospace")

    arrow(ax, 64, top - 17.0, 36, top - 17.0, color=TEAL, lw=2.6, ms=15)
    ax.text(50, top - 20.2, "STATUS   cnt_done", fontsize=FS_MONO, color=TEAL,
            ha="center", family="monospace", fontweight="bold")

    ax.text(50, 4.0, "Six per cent of the cells, one hundred per cent of the "
                     "behaviour.",
            fontsize=FS_HEAD, color=NAVY, ha="center", fontweight="bold")
    save(f, "datapath_controller")


def running_example():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The running example: a 4-bit counter", FS_TITLE)

    yb = H - 26.0
    box(ax, 9, yb, 26, 16.0, fc=LIGHT, ec=NAVY, lw=2.0)
    ax.text(22, yb + 12.6, "counter4", fontsize=FS_HEAD + 1, color=NAVY,
            ha="center", fontweight="bold", family="monospace")
    for i, p in enumerate(["clk", "rst_n", "en"]):
        yy = yb + 9.0 - i * 3.2
        wire(ax, [(3.5, yy), (9, yy)], color=INK, lw=1.6)
        ax.text(3.0, yy, p, fontsize=FS_SMALL, color=BODY, ha="right",
                va="center", family="monospace")
    for i, p in enumerate(["count[3:0]", "tc"]):
        yy = yb + 8.0 - i * 4.0
        wire(ax, [(35, yy), (40, yy)], color=INK, lw=1.6)
        ax.text(40.6, yy, p, fontsize=FS_SMALL, color=BODY, ha="left",
                va="center", family="monospace")

    code = ["always @(posedge clk or negedge rst_n)",
            "    if (!rst_n)  count <= 4'd0;",
            "    else if (en) count <= count + 4'd1;",
            "",
            "assign tc = en & (count == 4'd15);"]
    box(ax, 56, yb - 1.5, 41, 19.0, fc="#FBFCFE", ec=SLATE, lw=1.6)
    for i, ln in enumerate(code):
        ax.text(58, yb + 13.5 - i * 3.4, ln, fontsize=9.6, color=INK,
                ha="left", va="center", family="monospace")

    u = 5.6
    x0, yw = 20.0, 9.5
    wave(ax, x0, yw, 8.0, [0, 0, 0, 1, 0, 0, 0, 0], u, color=AMBER, name="tc",
         name_size=FS_SMALL, label_dx=2.0)
    for i, v in enumerate(["12", "13", "14", "15", "0", "1", "2", "3"]):
        ax.text(x0 + 8.0 * i + 4.0, yw - 3.6, v, fontsize=FS_SMALL, color=NAVY,
                ha="center", family="monospace")
    ax.text(x0 - 2.0, yw - 3.6, "count", fontsize=FS_SMALL, color=NAVY,
            ha="right", fontweight="bold")
    ax.text(50, 2.0, "tc is high for exactly one cycle, while count == 15",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    save(f, "running_example")


def mux_styles():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "One function, three coding styles - and three "
                           "netlists", FS_TITLE)
    ax.text(50, H - 10.0, "A 4:1 multiplexer. All 64 patterns simulated; every "
                          "pair proved equivalent by SAT.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    cols = [("mux4_assign", TEAL,
             ["assign y =", "  sel[1] ? (sel[0]?d[3]:d[2])",
              "          : (sel[0]?d[1]:d[0]);"], "3"),
            ("mux4_if", VIOLET,
             ["if      (sel==2'b00) y = d[0];",
              "else if (sel==2'b01) y = d[1];",
              "else ...        else y = d[3];"], "6"),
            ("mux4_case", AMBER,
             ["case (sel)", "  2'b00: y = d[0];   ...",
              "  default: y = 1'b0;"], "10")]
    top = H - 13.5
    bh = 26.0
    x = 3
    for nm, col, lines, cells in cols:
        box(ax, x, top - bh, 30.6, bh, fc=WHITE, ec=col, lw=2.0)
        box(ax, x, top - 5.6, 30.6, 5.6, fc=col, ec=col)
        ax.text(x + 15.3, top - 2.8, nm, fontsize=FS_HEAD, color=WHITE,
                ha="center", va="center", fontweight="bold",
                family="monospace")
        for i, ln in enumerate(lines):
            ax.text(x + 1.4, top - 9.4 - i * 3.4, ln, fontsize=9.4, color=INK,
                    ha="left", va="center", family="monospace")
        ax.text(x + 15.3, top - 23.0, cells + " cells", fontsize=20,
                color=col, ha="center", va="center", fontweight="bold")
        x += 32.7

    ax.text(50, 4.0, "EQUIVALENT is not the same as IDENTICAL.", fontsize=FS_HEAD,
            color=RED, ha="center", fontweight="bold")
    save(f, "mux_styles")


def blocking_measured():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Blocking in a clocked block: what it actually "
                           "builds", FS_TITLE)

    pairs = [("shift_nb   —   correct", GREEN,
              ["always @(posedge clk) begin", "    q[0] <= din;",
               "    q[1] <= q[0];", "    q[2] <= q[1];", "end"],
              "3 flip-flops"),
             ("shift_bl   —   not a shift register", RED,
              ["always @(posedge clk) begin", "    q[0] = din;",
               "    q[1] = q[0];", "    q[2] = q[1];", "end"],
              "1 flip-flop")]
    top = H - 9.0
    bh = 30.0
    x = 3
    for nm, col, lines, ff in pairs:
        box(ax, x, top - bh, 46, bh, fc=WHITE, ec=col, lw=2.0)
        box(ax, x, top - 5.6, 46, 5.6, fc=col, ec=col)
        ax.text(x + 23, top - 2.8, nm, fontsize=FS_HEAD, color=WHITE,
                ha="center", va="center", fontweight="bold")
        for i, ln in enumerate(lines):
            ax.text(x + 3, top - 9.8 - i * 3.2, ln, fontsize=FS_MONO, color=INK,
                    ha="left", va="center", family="monospace")
        ax.text(x + 23, top - 27.0, ff, fontsize=17, color=col, ha="center",
                fontweight="bold")
        x += 48

    ax.text(50, 4.0, "0 wrong cycles against 6.    Nothing illegal was written, "
                     "so nothing warned.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "blocking_measured")


def hierarchy_generate():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "From module to IP: parameters, hierarchy, generate",
          FS_TITLE)

    top = H - 9.5
    box(ax, 3, top - 16.5, 40, 16.5, fc="#FBFCFE", ec=SLATE, lw=1.6)
    src = ["genvar k;", "generate", "  for (k=0; k<N; k=k+1) begin : stage",
           "    preg #(.W(W)) u_reg (", "      .d(tap[k]), .q(tap[k+1]));",
           "  end", "endgenerate"]
    for i, ln in enumerate(src):
        ax.text(4.8, top - 2.4 - i * 2.1, ln, fontsize=8.8, color=INK, ha="left",
                va="center", family="monospace")
    ax.text(23, top - 18.8, "what you write", fontsize=FS_BODY, color=SLATE,
            ha="center", fontweight="bold")

    arrow(ax, 44.5, top - 9.0, 49.5, top - 9.0, color=NAVY, lw=2.6, ms=15)
    ax.text(45, top - 5.2, "elaborate", fontsize=FS_SMALL, color=NAVY,
            ha="center", fontweight="bold")

    for i in range(4):
        x = 52 + i * 10.8
        label_box(ax, x, top - 13.0, 8.6, 8.0, "preg", fc=WHITE, ec=VIOLET,
                  tc=VIOLET, size=FS_SMALL)
        if i:
            wire(ax, [(x - 2.2, top - 9.0), (x, top - 9.0)], color=INK, lw=1.6)
    wire(ax, [(49.5, top - 9.0), (52, top - 9.0)], color=INK, lw=1.6)
    wire(ax, [(93, top - 9.0), (96, top - 9.0)], color=INK, lw=1.6)
    ax.text(73, top - 18.8, "what gets built   (N = 4)", fontsize=FS_BODY,
            color=SLATE, ha="center", fontweight="bold")

    # the measurement, laid on its side so it stays one band high
    rows = [["cells", "8", "16", "32", "64"],
            ["flip-flops", "8", "16", "32", "64"]]
    table(ax, 18, top - 21.5, ["N", "1", "2", "4", "8"], rows,
          [20, 11, 11, 11, 11], 4.2, size=FS_TABLE, bold_col=[0])

    ax.text(50, 2.2, "Eight flip-flops per stage, exactly N stages, and no loop "
                     "anywhere in the netlist.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "hierarchy_generate")


def numerical_example():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "A worked numerical example", FS_TITLE)

    top = H - 10.0
    bh = 29.0

    box(ax, 3, top - bh, 46, bh, fc=LIGHT, ec=NAVY, lw=2.0)
    ax.text(26, top - 4.4, "counter4 at 100 MHz", fontsize=FS_HEAD, color=NAVY,
            ha="center", fontweight="bold")
    lines = [("clock period", "10 ns"),
             ("states before it wraps", "2^4 = 16"),
             ("one full cycle", "160 ns"),
             ("tc pulse rate", "6.25 MHz"),
             ("tc pulse width", "10 ns")]
    for i, (a, b) in enumerate(lines):
        ax.text(5.5, top - 9.5 - i * 4.0, a, fontsize=FS_BODY, color=BODY,
                ha="left", va="center")
        ax.text(46.5, top - 9.5 - i * 4.0, b, fontsize=FS_BODY, color=NAVY,
                ha="right", va="center", family="monospace", fontweight="bold")

    box(ax, 51, top - bh, 46, bh, fc="#F6F2FC", ec=VIOLET, lw=2.0)
    ax.text(74, top - 4.4, "accum_top, N = 6 samples", fontsize=FS_HEAD,
            color=VIOLET, ha="center", fontweight="bold")
    lines = [("cycle 0", "start seen, cnt <- 6"),
             ("cycles 1..6", "one sample added per clock"),
             ("cycle 7", "counter reached zero"),
             ("cycle 8", "done pulses, sum valid"),
             ("total latency", "N + 3 = 9 clocks")]
    for i, (a, b) in enumerate(lines):
        ax.text(53.5, top - 9.5 - i * 4.0, a, fontsize=FS_BODY, color=BODY,
                ha="left", va="center", family="monospace")
        ax.text(94.5, top - 9.5 - i * 4.0, b, fontsize=FS_SMALL, color=VIOLET,
                ha="right", va="center")

    ax.text(50, 3.5, "Derive the formula, then measure it. Measured: sum = 157, "
                     "done at cycle 8.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "numerical_example")


for fn in (comb_vs_seq, comb_vs_seq_table, sync_design, datapath_controller,
           running_example, mux_styles, blocking_measured, hierarchy_generate,
           numerical_example):
    fn()
