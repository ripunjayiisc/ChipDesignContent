# -*- coding: utf-8 -*-
"""Topic 4a diagrams: Verilog syntax, constructs and the language model."""
import _boot
from dsl import *
import numpy as np


def hdl_vs_software():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "Verilog is not a programming language — it DESCRIBES hardware", 13.5, NAVY)
    panels = [(2.0, "SOFTWARE  (C, Python)", RED, "#FDECEF",
               ["Statements run ONE AT A TIME, in order",
                "A variable is a location in memory",
                "A loop repeats over time",
                "'Faster' means fewer instructions",
                "Compiles to instructions for a CPU"]),
              (51.0, "HARDWARE  (Verilog RTL)", GREEN, "#E4F4EC",
               ["Every block runs ALL THE TIME, in parallel",
                "A signal is a wire or a flip-flop that EXISTS",
                "A loop UNROLLS into repeated hardware",
                "'Faster' means a shorter critical path",
                "Synthesises to gates on silicon"])]
    wd = 47.0
    for x0, nm, c, bg, items in panels:
        box(ax, x0, 9.5, wd, 26.0, fc=bg, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x0, 30.5), wd, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x0, 30.5), wd, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x0 + wd / 2, 33.0, nm, ha="center", va="center", fontsize=11,
                color="white", fontweight="bold", zorder=6)
        for j, it in enumerate(items):
            ax.text(x0 + 2.2, 27.6 - j * 3.6, "·  " + it, ha="left", va="center",
                    fontsize=9.2, color=BODY)
    ax.add_patch(FancyBboxPatch((2.0, 1.5), 96.0, 6.4, boxstyle="round,pad=0,rounding_size=1.0",
                 fc=LIGHT, ec=NAVY, lw=1.6, zorder=2))
    ax.text(50, 5.6, "The single most useful habit in this whole topic:", ha="center",
            va="center", fontsize=9.6, color=NAVY, fontweight="bold", zorder=4)
    ax.text(50, 3.0, "before you write a line of Verilog, SKETCH THE HARDWARE you want. "
            "Then write the code that describes that sketch.",
            ha="center", va="center", fontsize=9.6, color=NAVY, fontweight="bold", zorder=4)
    save(f, "hdl_vs_software")


def abstraction_levels():
    W, Hin = 13, 5.4
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 41.54
    title(ax, 50, H - 2.0, "Four levels of abstraction — all legal Verilog, only some synthesisable",
          13.0, NAVY)
    rows = [("BEHAVIOURAL", GREEN,
             "What it DOES, with no structure implied",
             "always @(*) y = a + b;",
             "highest"),
            ("DATAFLOW / RTL", TEAL,
             "How data moves between registers each clock",
             "assign y = sel ? a : b;",
             "the level you WRITE"),
            ("GATE / STRUCTURAL", AMBER,
             "Explicit primitives and instances, wired together",
             "and u1 (y, a, b);",
             "what synthesis OUTPUTS"),
            ("SWITCH", SLATE,
             "Individual transistors — nmos, pmos",
             "nmos n1 (out, in, ctrl);",
             "essentially never used")]
    y = H - 7.0
    hgt = 5.7
    for nm, c, what, ex, note in rows:
        box(ax, 2.0, y - hgt, 96.0, hgt, fc=LIGHT, ec=GRID, lw=1.2)
        box(ax, 2.0, y - hgt, 20.0, hgt, fc=c, ec=c)
        ax.text(12.0, y - hgt / 2 + 1.1, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold")
        ax.text(12.0, y - hgt / 2 - 1.7, note, ha="center", va="center", fontsize=7.6,
                color="white")
        ax.text(24.0, y - hgt / 2 + 1.3, what, ha="left", va="center", fontsize=9.6,
                color=NAVY, fontweight="bold")
        ax.text(24.0, y - hgt / 2 - 1.6, ex, ha="left", va="center", fontsize=9.0,
                color=BODY, family="DejaVu Sans Mono")
        y -= hgt + 1.0
    arrow(ax, 0.9, H - 7.5, 0.9, y + 1.0, color=SLATE, lw=1.8, ms=10)
    ax.add_patch(FancyBboxPatch((2.0, 1.0), 96.0, 5.8, boxstyle="round,pad=0,rounding_size=1.0",
                 fc="#E4F4EC", ec=GREEN, lw=1.6, zorder=2))
    ax.text(50, 5.0, "RTL is the sweet spot: abstract enough to be readable and portable, "
            "concrete enough that the hardware is predictable.",
            ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="bold", zorder=4)
    ax.text(50, 2.4, "Behavioural code that is not RTL-style simulates fine and may not synthesise "
            "at all. The synthesisable subset is a real and narrow boundary.",
            ha="center", va="center", fontsize=9.0, color=BODY, zorder=4)
    save(f, "abstraction_levels")


def module_anatomy():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 43.08
    title(ax, 50, H - 2.0, "Anatomy of a Verilog module — every design you write has this shape",
          13.0, NAVY)
    code = [
        ("module adder4 #(parameter W = 4) (", TEAL),
        ("    input  [W-1:0] a, b,", NAVY),
        ("    input          cin,", NAVY),
        ("    output [W-1:0] sum,", GREEN),
        ("    output         cout", GREEN),
        (");", TEAL),
        ("", BODY),
        ("    wire [W:0] tmp;", SLATE),
        ("", BODY),
        ("    assign tmp  = a + b + cin;", BODY),
        ("    assign sum  = tmp[W-1:0];", BODY),
        ("    assign cout = tmp[W];", BODY),
        ("", BODY),
        ("endmodule", TEAL),
    ]
    cx, cw = 24.0, 50.0
    ctop, lh = 36.4, 1.92
    cbot = ctop - len(code) * lh - 1.2
    box(ax, cx, cbot, cw, ctop - cbot + 1.2, fc=WHITE, ec=TEAL, lw=1.9, r=1.0)
    for i, (ln, c) in enumerate(code):
        ax.text(cx + 2.0, ctop - 1.0 - i * lh, ln, ha="left", va="center", fontsize=8.4,
                color=c, family="DejaVu Sans Mono",
                fontweight="bold" if c is TEAL else "normal")

    def brace(y1, y2, lab, sub, c):
        xb = cx + cw + 1.4
        wire(ax, [(xb, y1), (xb + 1.3, y1), (xb + 1.3, y2), (xb, y2)], color=c, lw=1.5)
        ym = (y1 + y2) / 2
        wire(ax, [(xb + 1.3, ym), (xb + 2.7, ym)], color=c, lw=1.5)
        ax.text(xb + 3.4, ym + 1.1, lab, ha="left", va="center", fontsize=8.6,
                color=c, fontweight="bold")
        ax.text(xb + 3.4, ym - 1.2, sub, ha="left", va="center", fontsize=7.2, color=SLATE)

    yt = ctop - 1.0
    brace(yt + 0.8, yt - 0.8, "name + parameters", "sized at instantiation", TEAL)
    brace(yt - lh + 0.8, yt - 4 * lh - 0.8, "port list", "the module's interface", NAVY)
    brace(yt - 7 * lh + 0.8, yt - 7 * lh - 0.8, "internal signals", "not visible outside", SLATE)
    brace(yt - 9 * lh + 0.8, yt - 11 * lh - 0.8, "the design body", "what it actually does", GREEN)

    ax.text(4.0, yt, "colour key", ha="left", va="center", fontsize=9.0,
            color=NAVY, fontweight="bold")
    for j, (c, lab) in enumerate([(TEAL, "structure"), (NAVY, "input ports"),
                                  (GREEN, "output ports"), (SLATE, "internal signal"),
                                  (BODY, "the logic itself")]):
        yy = yt - 3.2 - j * 3.0
        ax.add_patch(Rectangle((4.0, yy - 0.7), 2.2, 1.4, fc=c, ec=c, zorder=4))
        ax.text(7.2, yy, lab, ha="left", va="center", fontsize=8.4, color=BODY)

    ax.add_patch(FancyBboxPatch((2.0, 1.0), 96.0, 6.2, boxstyle="round,pad=0,rounding_size=1.0",
                 fc=LIGHT, ec=TEAL, lw=1.5, zorder=2))
    ax.text(50, 5.3, "A module is a BOX with a name and a set of ports. Everything you build in "
            "this topic is a box, or a box made of boxes.",
            ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="bold", zorder=4)
    ax.text(50, 2.6, "This is ANSI style, with ports declared in the header. The older non-ANSI "
            "style lists bare names there and declares them again below — expect it in legacy code.",
            ha="center", va="center", fontsize=8.2, color=BODY, zorder=4)
    save(f, "module_anatomy")


def four_value_logic():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "Verilog signals have FOUR values, not two", 13.5, NAVY)
    vals = [("0", "logic zero", "a real, driven\nlogic low", GREEN, "#E4F4EC"),
            ("1", "logic one", "a real, driven\nlogic high", TEAL, "#E8F5F7"),
            ("x", "unknown", "the simulator cannot\ntell — uninitialised, or\ntwo drivers fighting",
             RED, "#FDECEF"),
            ("z", "high impedance", "nothing is driving\nthis wire at all", AMBER, "#FFF6EC")]
    cw = 23.0
    for i, (v, nm, desc, c, bg) in enumerate(vals):
        x = 2.0 + i * (cw + 1.4)
        box(ax, x, 15.0, cw, 19.0, fc=bg, ec=c, lw=1.9)
        ax.add_patch(Circle((x + cw / 2, 30.0), 3.0, fc=c, ec=c, zorder=4))
        ax.text(x + cw / 2, 30.0, v, ha="center", va="center", fontsize=17,
                color="white", fontweight="bold", zorder=6, family="DejaVu Sans Mono")
        ax.text(x + cw / 2, 24.4, nm, ha="center", va="center", fontsize=10.5,
                color=c, fontweight="bold")
        ax.text(x + cw / 2, 19.6, desc, ha="center", va="center", fontsize=8.2,
                color=BODY, linespacing=1.5)
    box(ax, 2.0, 7.4, 47.0, 6.2, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(25.5, 11.6, "x is a SIMULATION value, not a hardware value", ha="center",
            va="center", fontsize=9.6, color=RED, fontweight="bold")
    ax.text(25.5, 9.0, "Real silicon always holds 0 or 1. An x means the simulator does not know "
            "which — and neither do you.", ha="center", va="center", fontsize=8.4, color=BODY)
    box(ax, 51.0, 7.4, 47.0, 6.2, fc="#FFF6EC", ec=AMBER, lw=1.6)
    ax.text(74.5, 11.6, "z is real, but only on a tri-state bus", ha="center",
            va="center", fontsize=9.6, color=AMBER, fontweight="bold")
    ax.text(74.5, 9.0, "Inside a modern chip you almost never use it.\n"
            "Off-chip pins and old shared buses do.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.5)
    ax.text(50, 3.4, "Chasing an x back to its source is the single most common debugging task in RTL. "
            "Start at the first signal that turns x and work backwards.",
            ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="bold")
    save(f, "four_value_logic")


def nets_vs_variables():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 40.0
    title(ax, 50, H - 2.0, "wire or reg? The rule is about HOW you assign, not what it becomes",
          13.0, NAVY)
    specs = [(2.0, "wire   (a NET)", TEAL, "#E8F5F7",
              ["Assigned by  assign", "Assigned by a module port connection",
               "Never assigned inside always/initial", "",
               "Models a physical connection", "The default type of an undeclared port"]),
             (51.0, "reg   (a VARIABLE)", AMBER, "#FFF6EC",
              ["Assigned inside  always  or  initial", "Assigned with  =  or  <=",
               "Never driven by  assign", "",
               "Holds its value between assignments", "— in the SIMULATOR. That is all it means."])]
    wd = 47.0
    for x0, nm, c, bg, items in specs:
        box(ax, x0, 12.0, wd, 24.0, fc=bg, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x0, 31.0), wd, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x0, 31.0), wd, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x0 + wd / 2, 33.5, nm, ha="center", va="center", fontsize=11,
                color="white", fontweight="bold", zorder=6, family="DejaVu Sans Mono")
        for j, it in enumerate(items):
            if not it:
                continue
            ax.text(x0 + 2.2, 28.2 - j * 2.9, ("·  " + it) if j != 3 else ("   " + it),
                    ha="left", va="center", fontsize=9.0, color=BODY)
    box(ax, 2.0, 1.2, 96.0, 9.4, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 8.4, "The misunderstanding that costs beginners the most time",
            ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
    ax.text(50, 5.6, "A  reg  is NOT a register.  It is a simulator variable. Whether it becomes a "
            "flip-flop depends ENTIRELY on how you assign it:",
            ha="center", va="center", fontsize=9.4, color=NAVY, fontweight="bold")
    ax.text(50, 2.8, "reg in always @(*)  →  combinational gates          "
            "reg in always @(posedge clk)  →  a flip-flop",
            ha="center", va="center", fontsize=8.6, color=BODY, family="DejaVu Sans Mono")
    save(f, "nets_vs_variables")


def literals():
    W, Hin = 13, 5.4
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 41.54
    title(ax, 50, H - 2.0, "Reading a Verilog number literal", 13.5, NAVY)
    parts = [("8", "SIZE\nin bits", TEAL, 16.0),
             ("'", "tick", SLATE, 6.0),
             ("h", "BASE\nb o d h", AMBER, 10.0),
             ("A5", "VALUE\nin that base", GREEN, 18.0)]
    x = 24.0
    for txt, lab, c, wdt in parts:
        box(ax, x, 30.0, wdt, 6.6, fc=c, ec=c, r=0.8)
        ax.text(x + wdt / 2, 33.3, txt, ha="center", va="center", fontsize=14,
                color="white", fontweight="bold", family="DejaVu Sans Mono")
        ax.text(x + wdt / 2, 27.4, lab, ha="center", va="center", fontsize=8.2,
                color=c, fontweight="bold", linespacing=1.4)
        x += wdt + 1.0
    ax.text(x + 2.0, 33.3, "=  1010 0101  =  165", ha="left", va="center", fontsize=11,
            color=NAVY, fontweight="bold")
    ax.text(22.0, 33.3, "8'hA5", ha="right", va="center", fontsize=12.5,
            color=NAVY, fontweight="bold", family="DejaVu Sans Mono")

    rows = [["4'b1010", "4 bits, binary", "10"],
            ["8'hFF", "8 bits, hex", "255"],
            ["8'd200", "8 bits, decimal", "200"],
            ["8'o17", "8 bits, octal", "15"],
            ["8'b1010_0101", "underscores are ignored — use them for readability", "165"],
            ["4'bx", "all four bits unknown", "xxxx"],
            ["4'b10z1", "bit 1 is high-impedance", "10z1"],
            ["42", "UNSIZED — 32 bits, signed. Avoid this.", "32'd42"],
            ["-8'd3", "the MINUS applies to the whole literal", "8'b1111_1101"]]
    table(ax, 8.0, 23.0, ["literal", "meaning", "value"], rows,
          [22.0, 40.0, 22.0], 1.95, size=8.4, head_fc=NAVY, bold_col=[0])
    ax.text(50, 1.9, "House rule: ALWAYS size your literals. An unsized 1 in a 64-bit expression is "
            "a 32-bit 1, and the top 32 bits silently become zero.",
            ha="center", va="center", fontsize=9.0, color=RED, fontweight="bold")
    save(f, "literals")


def vector_ops():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 40.0
    title(ax, 50, H - 2.0, "Vectors — slicing, concatenating and replicating", 13.0, NAVY)
    # the vector
    bits = list("11010110")
    bw, gap = 8.0, 1.0
    x0, yb, bh = 14.0, 26.4, 6.2
    for i, b in enumerate(bits):
        idx = 7 - i
        c = TEAL if b == "1" else "#C3CDD8"
        ax.add_patch(FancyBboxPatch((x0 + i * (bw + gap), yb), bw, bh,
                     boxstyle="round,pad=0,rounding_size=1", fc=c, ec="white", lw=1.3, zorder=3))
        ax.text(x0 + i * (bw + gap) + bw / 2, yb + bh / 2, b, ha="center", va="center",
                fontsize=13, color="white", fontweight="bold", zorder=4)
        ax.text(x0 + i * (bw + gap) + bw / 2, yb + bh + 2.4, "[%d]" % idx, ha="center",
                va="center", fontsize=8.6, color=SLATE, fontweight="bold")
    ax.text(x0 - 2.0, yb + bh / 2, "d", ha="right", va="center", fontsize=12,
            color=NAVY, fontweight="bold", family="DejaVu Sans Mono")
    ax.text(50, 23.6, "wire [7:0] d = 8'b1101_0110;", ha="center", va="center",
            fontsize=10.0, color=NAVY, fontweight="bold", family="DejaVu Sans Mono")

    ops = [("d[7]", "single bit — the MSB", "1'b1", TEAL),
           ("d[3:0]", "part-select — the low nibble", "4'b0110", TEAL),
           ("{d[3:0], d[7:4]}", "concatenation — swap the nibbles", "8'b0110_1101", GREEN),
           ("{4{d[7]}}", "replication — sign-extend by 4", "4'b1111", AMBER),
           ("{{4{d[7]}}, d[3:0]}", "replication INSIDE concatenation", "8'b1111_0110", AMBER),
           ("d[i +: 4]", "indexed part-select, 4 bits UP from i", "variable i is legal", VIOLET)]
    y = 20.2
    for nm, what, res, c in ops:
        ax.text(6.0, y, nm, ha="left", va="center", fontsize=9.6, color=c,
                fontweight="bold", family="DejaVu Sans Mono")
        ax.text(32.0, y, what, ha="left", va="center", fontsize=9.0, color=BODY)
        ax.text(72.0, y, res, ha="left", va="center", fontsize=9.2, color=NAVY,
                fontweight="bold", family="DejaVu Sans Mono")
        y -= 2.9
    box(ax, 2.0, 0.8, 96.0, 3.4, fc="#FDECEF", ec=RED, lw=1.5)
    ax.text(50, 2.5, "Keep every vector declared [MSB:0]. Mixing [7:0] and [0:7] in one design is "
            "legal, confusing, and a reliable source of reversed buses.",
            ha="center", va="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "vector_ops")


def operator_map():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "The Verilog operators you will actually use", 13.0, NAVY)
    left = [
        ("Arithmetic", TEAL, [("+  -  *", "add, subtract, multiply"),
                              ("/  %", "in RTL, only by a power of 2")]),
        ("Relational", TEAL, [("<  <=  >  >=", "comparison; the result is 1 bit")]),
        ("Equality", RED, [("==   !=", "gives x if either side has x or z"),
                           ("===  !==", "compares x and z literally"),
                           ("", "=== is TESTBENCH ONLY — it does not synthesise")]),
        ("Logical", AMBER, [("&&  ||  !", "whole vector as true/false; 1-bit result")]),
    ]
    right = [
        ("Bitwise", AMBER, [("&  |  ^  ~  ~^", "bit by bit; result is a vector")]),
        ("Reduction", GREEN, [("&a   |a   ^a", "collapse a whole vector to ONE bit"),
                              ("", "^a = parity,  |a = any bit set,  &a = all bits set")]),
        ("Shift", GREEN, [("<<   >>", "logical shift, zero fill"),
                          ("<<<  >>>", "arithmetic shift, sign fill")]),
        ("Conditional", VIOLET, [("? :", "the ternary MUX — used everywhere")]),
        ("Concatenation", VIOLET, [("{ }    {n{ }}", "join and replicate")]),
    ]
    for col, groups in enumerate((left, right)):
        x0 = 2.0 + col * 49.0
        wd = 47.0
        y = H - 5.6
        for nm, c, items in groups:
            n = len(items)
            hgt = 1.7 + 2.4 * n
            box(ax, x0, y - hgt, wd, hgt, fc=LIGHT, ec=GRID, lw=1.0)
            box(ax, x0, y - hgt, 14.0, hgt, fc=c, ec=c)
            ax.text(x0 + 7.0, y - hgt / 2, nm, ha="center", va="center", fontsize=9.0,
                    color="white", fontweight="bold")
            for j, (sym, desc) in enumerate(items):
                yy = y - 2.4 - j * 2.4
                if sym:
                    ax.text(x0 + 15.6, yy, sym, ha="left", va="center", fontsize=8.6,
                            color=NAVY, fontweight="bold", family="DejaVu Sans Mono")
                    ax.text(x0 + 27.0, yy, desc, ha="left", va="center", fontsize=7.8, color=BODY)
                else:
                    ax.text(x0 + 15.6, yy, desc, ha="left", va="center", fontsize=7.6, color=c,
                            fontweight="bold", style="italic")
            y -= hgt + 0.9
    ax.text(50, 1.6, "Precedence, tightest first:  ~ !   *  /  %   +  -   <<  >>   <  <=  >  >=   "
            "==  !=  ===  !==   &   ^   |   &&   ||   ?:      —  when in doubt, bracket it.",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold")
    save(f, "operator_map")


def width_rules():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "Width and sign rules — where silent bugs come from", 13.0, NAVY)
    box(ax, 2.0, 17.5, 96.0, 16.5, fc="#FDECEF", ec=RED, lw=1.8)
    ax.text(50, 32.4, "The context-determined width rule", ha="center", va="center",
            fontsize=10.5, color=RED, fontweight="bold")
    ax.text(50, 29.6, "Verilog first finds the WIDEST operand in the whole expression — the "
            "left-hand side included —\nthen extends every operand to that width BEFORE evaluating.",
            ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="bold", linespacing=1.6)
    lines = [("wire [3:0] a = 4'd9, b = 4'd8;", BODY, ""),
             ("wire [3:0] s4 = a + b;", RED, "17 truncates to 4'd1        WRONG"),
             ("wire [4:0] s5 = a + b;", GREEN, "5'd17                      correct"),
             ("wire [4:0] s6 = {1'b0, a} + b;", GREEN, "explicit — clearest of all")]
    for i, (code, c, note) in enumerate(lines):
        yy = 25.6 - i * 2.1
        ax.text(7.0, yy, code, ha="left", va="center", fontsize=9.0, color=c,
                family="DejaVu Sans Mono")
        if note:
            ax.text(46.0, yy, "// " + note, ha="left", va="center", fontsize=9.0,
                    color=c, family="DejaVu Sans Mono")
    cards = [("Signed arithmetic", AMBER, "#FFF6EC",
              ["A vector is UNSIGNED unless you declare it  signed.",
               "If ANY operand is unsigned, the WHOLE expression is",
               "unsigned — so one stray signal inverts your compare."]),
             ("Two habits that prevent all of it", GREEN, "#E4F4EC",
              ["1.  Make the result one bit wider than the widest operand.",
               "2.  Size every literal; never rely on an unsized constant.",
               "Then lint it — Verilator -Wall finds width bugs for free."])]
    for i, (nm, c, bg, ls) in enumerate(cards):
        x = 2.0 + i * 49.0
        box(ax, x, 2.5, 47.0, 13.0, fc=bg, ec=c, lw=1.7)
        ax.text(x + 23.5, 13.4, nm, ha="center", va="center", fontsize=10,
                color=c, fontweight="bold")
        for j, ln in enumerate(ls):
            ax.text(x + 1.8, 10.0 - j * 2.6, ln, ha="left", va="center", fontsize=8.2, color=BODY)
    save(f, "width_rules")


if __name__ == "__main__":
    hdl_vs_software(); abstraction_levels(); module_anatomy(); four_value_logic()
    nets_vs_variables(); literals(); vector_ops(); operator_map(); width_rules()
