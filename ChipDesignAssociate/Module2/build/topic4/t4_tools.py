# -*- coding: utf-8 -*-
"""Topic 4 diagrams: inference map, RTL flow, and the three toolchains."""
import _boot
from dsl import *
import numpy as np


def inference_map():
    W, Hin = 13, 5.8
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 44.62
    title(ax, 50, H - 2.0, "The inference map — what each RTL construct becomes in silicon",
          13.0, NAVY)
    rows = [("assign y = a & b;", "an AND gate", GREEN),
            ("assign y = s ? a : b;", "a 2:1 multiplexer", GREEN),
            ("assign y = a + b;", "an adder — the tool picks the structure", GREEN),
            ("assign y = a * b;", "a MULTIPLIER — large. Check you meant it.", AMBER),
            ("assign y = a / b;", "a DIVIDER — huge, or a synthesis error", RED),
            ("always @(*) with full assignment", "combinational gates", GREEN),
            ("always @(*) with a missing branch", "a transparent LATCH — a bug", RED),
            ("case (sel) … endcase", "a multiplexer, one input per branch", GREEN),
            ("if / else if / else if …", "a PRIORITY multiplexer chain — slower", AMBER),
            ("always @(posedge clk) q <= d;", "one D flip-flop per bit of q", GREEN),
            ("always @(posedge clk) if (en) q <= d;", "a flip-flop with a clock enable", GREEN),
            ("reg [7:0] mem [0:255];  with a clocked read",
             "a block RAM on FPGA, a memory macro on ASIC", GREEN),
            ("for (i=0; i<N; i=i+1)  with constant N",
             "N copies of the loop body, UNROLLED", GREEN),
            ("x <= y; in two different always blocks", "a multi-driver error", RED)]
    y = H - 6.0
    rh = 2.5
    ax.add_patch(Rectangle((3.0, y), 44.0, rh, fc=NAVY, ec=NAVY, zorder=3))
    ax.add_patch(Rectangle((47.0, y), 50.0, rh, fc=NAVY, ec=NAVY, zorder=3))
    ax.text(25.0, y + rh / 2, "you write", ha="center", va="center", fontsize=9.4,
            color="white", fontweight="bold", zorder=5)
    ax.text(72.0, y + rh / 2, "the tool builds", ha="center", va="center", fontsize=9.4,
            color="white", fontweight="bold", zorder=5)
    for i, (code, hw, c) in enumerate(rows):
        yy = y - (i + 1) * rh
        bg = WHITE if i % 2 == 0 else LIGHT
        ax.add_patch(Rectangle((3.0, yy), 44.0, rh, fc=bg, ec=GRID, lw=0.8, zorder=3))
        ax.add_patch(Rectangle((47.0, yy), 50.0, rh, fc=bg, ec=GRID, lw=0.8, zorder=3))
        ax.text(4.5, yy + rh / 2, code, ha="left", va="center", fontsize=7.8,
                color=BODY, family="DejaVu Sans Mono", zorder=5)
        ax.text(48.6, yy + rh / 2, hw, ha="left", va="center", fontsize=7.8,
                color=c, fontweight="bold" if c is not GREEN else "normal", zorder=5)
        ax.add_patch(Rectangle((45.2, yy + rh / 2 - 0.35), 1.6, 0.7, fc=c, ec=c, zorder=5))
    ax.text(50, 2.0, "Green = exactly what you meant.   Amber = check you meant it.   "
            "Red = a bug. There is no fourth category.",
            ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="bold")
    save(f, "inference_map")


def case_to_mux():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "case builds a MUX;  if/else-if builds a PRIORITY chain", 13.0, NAVY)
    # ---------------- case ----------------
    box(ax, 2.0, 11.0, 46.5, 22.0, fc="#E4F4EC", ec=GREEN, lw=1.8)
    ax.text(25.25, 31.3, "case  →  one balanced multiplexer", ha="center", va="center",
            fontsize=9.6, color=GREEN, fontweight="bold")
    for i, ln in enumerate(["case (sel)", "  2'd0: y = a;", "  2'd1: y = b;",
                            "  2'd2: y = c;", "  default: y = d;", "endcase"]):
        ax.text(5.0, 28.4 - i * 1.85, ln, ha="left", va="center", fontsize=8.0,
                color=BODY, family="DejaVu Sans Mono")
    tx, ty, tw_, th_ = 30.0, 14.6, 8.0, 12.0
    ax.add_patch(Polygon([(tx, ty + th_), (tx + tw_, ty + th_ - 2.6),
                          (tx + tw_, ty + 2.6), (tx, ty)], fc=WHITE, ec=GREEN, lw=1.8, zorder=3))
    for i, lab in enumerate("abcd"):
        yy = ty + th_ - 1.8 - i * 2.8
        wire(ax, [(tx - 2.6, yy), (tx, yy)], color=INK, lw=1.2)
        ax.text(tx - 3.2, yy, lab, ha="right", va="center", fontsize=8.0, color=NAVY,
                fontweight="bold")
    wire(ax, [(tx + tw_, ty + th_ / 2), (tx + tw_ + 3.0, ty + th_ / 2)], color=INK, lw=1.2)
    ax.text(tx + tw_ + 3.6, ty + th_ / 2, "y", ha="left", va="center", fontsize=9,
            color=GREEN, fontweight="bold")
    ax.text(25.25, 12.4, "ONE gate delay for every input — balanced", ha="center",
            va="center", fontsize=8.0, color=GREEN, fontweight="bold")

    # ---------------- if / else if ----------------
    box(ax, 51.5, 11.0, 46.5, 22.0, fc="#FFF6EC", ec=AMBER, lw=1.8)
    ax.text(74.75, 31.3, "if / else if  →  a priority CHAIN", ha="center", va="center",
            fontsize=9.6, color=AMBER, fontweight="bold")
    for i, ln in enumerate(["if      (p0) y = a;", "else if (p1) y = b;",
                            "else if (p2) y = c;", "else         y = d;"]):
        ax.text(54.0, 28.4 - i * 1.85, ln, ha="left", va="center", fontsize=8.0,
                color=BODY, family="DejaVu Sans Mono")
    for i in range(3):
        x = 57.0 + i * 9.0
        ax.add_patch(Polygon([(x, 20.4), (x + 5.0, 19.0), (x + 5.0, 14.8), (x, 13.4)],
                             fc=WHITE, ec=AMBER, lw=1.5, zorder=3))
        ax.text(x + 2.5, 16.9, "2:1", ha="center", va="center", fontsize=6.6,
                color=AMBER, fontweight="bold", zorder=5)
        if i < 2:
            arrow(ax, x + 5.0, 16.9, x + 8.8, 16.9, color=SLATE, lw=1.3, ms=8)
    arrow(ax, 84.0, 16.9, 88.0, 16.9, color=SLATE, lw=1.3, ms=8)
    ax.text(88.6, 16.9, "y", ha="left", va="center", fontsize=9, color=AMBER, fontweight="bold")
    ax.text(74.75, 12.4, "the LAST condition passes through 3 MUXes — slower",
            ha="center", va="center", fontsize=8.0, color=AMBER, fontweight="bold")

    box(ax, 2.0, 1.5, 96.0, 7.6, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(50, 7.3, "When does it matter?", ha="center", va="center", fontsize=9.4,
            color=TEAL, fontweight="bold")
    ax.text(50, 4.2, "Use  case  when the conditions are mutually exclusive — a decoder, an "
            "opcode, an FSM. Use  if/else if  when you genuinely WANT priority:\n"
            "an interrupt arbiter, a bus grant. Writing if/else-if for a mutually exclusive "
            "choice costs you delay for nothing.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.7)
    save(f, "case_to_mux")


def rtl_flow():
    W, Hin = 13, 4.4
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 33.85
    title(ax, 50, H - 2.0, "The RTL design loop — you will go round this many times per day",
          13.0, NAVY)
    steps = [("1", "SPECIFY", "what must it do?\nsketch the hardware", TEAL),
             ("2", "CODE", "write the RTL\nfollow the templates", TEAL),
             ("3", "LINT", "Verilator -Wall\ncatch width bugs early", AMBER),
             ("4", "SIMULATE", "self-checking testbench\ndoes it behave?", AMBER),
             ("5", "SYNTHESISE", "read the cell counts\nis it the hardware you meant?", GREEN),
             ("6", "REVIEW", "check the schematic\nand the warnings", GREEN)]
    bw, gap = 14.6, 2.0
    x0 = (100 - (6 * bw + 5 * gap)) / 2
    by, bh = 12.0, 15.0
    for i, (n, head, sub, c) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, by, bw, bh, fc=WHITE, ec=c, lw=1.8)
        ax.add_patch(Circle((x + bw / 2, by + bh - 2.8), 1.9, fc=c, ec=c, zorder=4))
        ax.text(x + bw / 2, by + bh - 2.8, n, ha="center", va="center", fontsize=9.6,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + bw / 2, by + bh - 7.2, head, ha="center", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold")
        ax.text(x + bw / 2, by + 3.0, sub, ha="center", va="center", fontsize=6.3,
                color=SLATE, linespacing=1.4)
        if i < 5:
            arrow(ax, x + bw + 0.3, by + bh / 2, x + bw + gap - 0.3, by + bh / 2,
                  color=SLATE, lw=1.8, ms=9)
    arrow(ax, x0 + 5 * (bw + gap) + bw / 2, by - 1.0, x0 + 1.4 * (bw + gap), by - 1.0,
          color=RED, lw=1.8, ms=10, rad=-0.10)
    ax.text(x0 + 3.3 * (bw + gap), by - 7.4, "anything wrong at ANY step sends you back to the code",
            ha="center", va="center", fontsize=8.4, color=RED, fontweight="bold")
    ax.text(50, 2.4, "Steps 3 and 5 are the ones beginners skip — and they are the two that "
            "tell you whether you wrote HARDWARE or just wrote code that compiles.",
            ha="center", va="center", fontsize=8.8, color=BODY, style="italic")
    save(f, "rtl_flow")


def toolchains():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 43.08
    title(ax, 50, H - 2.0, "Three toolchains — the syllabus tools, and a free one for home",
          13.0, NAVY)
    cols = [("VIVADO", TEAL, "#E8F5F7", "AMD / Xilinx  ·  free WebPACK edition",
             [("simulate", "built-in XSim"), ("synthesise", "yes, to real FPGA"),
              ("implement", "place & route, bitstream"), ("timing", "full STA"),
              ("schematic", "RTL and technology views"), ("size", "~50 GB"),
              ("in the syllabus", "YES — the specified tool")]),
            ("MODELSIM / QUESTA", AMBER, "#FFF6EC", "Siemens EDA  ·  free Intel Starter edition",
             [("simulate", "the industry reference"), ("synthesise", "no — simulation only"),
              ("implement", "no"), ("timing", "no"),
              ("schematic", "no, but excellent waveforms"), ("size", "~1–5 GB"),
              ("in the syllabus", "YES — the specified tool")]),
            ("OPEN-SOURCE", GREEN, "#E4F4EC", "Icarus + GTKWave + Yosys + Verilator",
             [("simulate", "Icarus Verilog, Verilator"), ("synthesise", "Yosys"),
              ("implement", "nextpnr, for some parts"), ("timing", "basic, via OpenSTA"),
              ("schematic", "Yosys  show  + graphviz"), ("size", "~200 MB"),
              ("in the syllabus", "no — but ideal for practice")])]
    cw = 31.4
    for i, (nm, c, bg, vendor, rows) in enumerate(cols):
        x = 2.0 + i * (cw + 1.5)
        box(ax, x, 4.0, cw, 33.0, fc=bg, ec=c, lw=1.9)
        ax.add_patch(FancyBboxPatch((x, 32.0), cw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 32.0), cw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, 34.5, nm, ha="center", va="center", fontsize=10.2,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + cw / 2, 30.0, vendor, ha="center", va="center", fontsize=7.2,
                color=c, fontweight="bold")
        for j, (k, v) in enumerate(rows):
            yy = 26.4 - j * 3.4
            ax.text(x + 1.8, yy + 0.7, k, ha="left", va="center", fontsize=7.2,
                    color=SLATE, fontweight="bold")
            ax.text(x + 1.8, yy - 0.7, v, ha="left", va="center", fontsize=7.6,
                    color=NAVY if j < 6 else c,
                    fontweight="bold" if j == 6 else "normal")
    ax.text(50, 2.2, "Learn the CONCEPTS on the free tools at home, then apply them on Vivado and "
            "ModelSim in the lab. The flow and the vocabulary are identical.",
            ha="center", va="center", fontsize=9.0, color=NAVY, fontweight="bold")
    save(f, "toolchains")


def vivado_flow():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 35.38
    title(ax, 50, H - 2.0, "The Vivado project flow — what each stage actually does", 13.0, NAVY)
    stages = [("Create\nProject", TEAL, "pick a part or board;\nadd design sources"),
              ("Add\nSources", TEAL, "RTL in Design Sources,\ntestbench in Simulation"),
              ("Run\nSimulation", AMBER, "XSim opens a waveform;\nbehavioural first"),
              ("Run\nSynthesis", GREEN, "RTL → gates.\nREAD THE WARNINGS."),
              ("Run\nImplementation", GREEN, "place & route\nfor the real device"),
              ("Generate\nBitstream", VIOLET, "the file you program\ninto the FPGA")]
    bw, gap = 14.6, 1.6
    x0 = (100 - (6 * bw + 5 * gap)) / 2
    by, bh = 14.0, 14.0
    for i, (nm, c, sub) in enumerate(stages):
        x = x0 + i * (bw + gap)
        box(ax, x, by, bw, bh, fc=LIGHT, ec=c, lw=1.8)
        ax.add_patch(Rectangle((x, by + bh - 1.2), bw, 1.2, fc=c, ec=c, zorder=4))
        ax.text(x + bw / 2, by + bh - 4.6, nm, ha="center", va="center", fontsize=8.8,
                color=NAVY, fontweight="bold", linespacing=1.3)
        ax.text(x + bw / 2, by + 3.4, sub, ha="center", va="center", fontsize=6.8,
                color=SLATE, linespacing=1.4)
        if i < 5:
            arrow(ax, x + bw + 0.2, by + bh / 2, x + bw + gap - 0.2, by + bh / 2,
                  color=SLATE, lw=1.7, ms=9)
    box(ax, 2.0, 2.0, 46.5, 10.0, fc="#E4F4EC", ec=GREEN, lw=1.6)
    ax.text(25.25, 10.2, "For this topic you only need the first four", ha="center",
            va="center", fontsize=9.0, color=GREEN, fontweight="bold")
    ax.text(25.25, 6.0, "Implementation and bitstream generation belong to\n"
            "Module 4 (FPGA Architecture and Programming). Stop after\n"
            "synthesis and read the report.",
            ha="center", va="center", fontsize=7.6, color=BODY, linespacing=1.6)
    box(ax, 51.5, 2.0, 46.5, 10.0, fc="#FFF6EC", ec=AMBER, lw=1.6)
    ax.text(74.75, 10.2, "The three reports you must learn to read", ha="center",
            va="center", fontsize=9.0, color=AMBER, fontweight="bold")
    ax.text(74.75, 6.0, "Messages  — every [Synth 8-xxx] warning matters.\n"
            "Utilization — LUTs, FFs, BRAM, DSP used.\n"
            "Schematic  — press F4 to see the inferred hardware.",
            ha="center", va="center", fontsize=7.6, color=BODY, linespacing=1.6)
    save(f, "vivado_flow")


def debug_ladder():
    W, Hin = 13, 6.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "Debugging RTL — work down this ladder, in this order", 13.0, NAVY)
    rungs = [("It does not COMPILE", RED,
              "Read the FIRST error only — later ones are usually cascade damage.\n"
              "Missing semicolon, missing endmodule, a reg driven by assign."),
             ("It compiles but the output is X", AMBER,
              "Find the FIRST signal that goes x and work backwards. Usual causes:\n"
              "no reset, an unconnected port, a multi-driver, or reading past the end of a vector."),
             ("It simulates but gives the WRONG answer", AMBER,
              "Add \\$display at the point of divergence. Compare against a reference model.\n"
              "Check blocking vs non-blocking, and check your width arithmetic."),
             ("It simulates right but SYNTHESISES wrong", TEAL,
              "You used something outside the synthesisable subset, or you inferred a latch.\n"
              "Read every synthesis warning. Compare the cell count with what you expected."),
             ("It synthesises but FAILS TIMING", GREEN,
              "That is Topic 6. For now: shorten the critical path, or pipeline it.")]
    y = H - 4.0
    for nm, c, txt in rungs:
        hgt = 5.8
        box(ax, 2.0, y - hgt, 96.0, hgt, fc=LIGHT, ec=c, lw=1.5)
        box(ax, 2.0, y - hgt, 30.0, hgt, fc=c, ec=c)
        ax.text(17.0, y - hgt / 2, nm, ha="center", va="center", fontsize=8.8,
                color="white", fontweight="bold")
        ax.text(33.5, y - hgt / 2, txt, ha="left", va="center", fontsize=7.8,
                color=BODY, linespacing=1.6)
        y -= hgt + 1.0
    box(ax, 2.0, 1.2, 96.0, 5.2, fc="#E4F4EC", ec=GREEN, lw=1.6)
    ax.text(50, 4.4, "The single most effective habit", ha="center", va="center",
            fontsize=9.4, color=GREEN, fontweight="bold")
    ax.text(50, 2.2, "Simulate after every few lines. A bug found in ten lines of new code takes "
            "a minute; the same bug found in three hundred takes an afternoon.",
            ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="bold")
    save(f, "debug_ladder")





def pipelining():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 36.92

    def ffbox(x, y, c):
        box(ax, x, y - 2.6, 4.2, 5.2, fc=WHITE, ec=c, lw=1.6, r=0.4)
        ax.add_patch(Polygon([(x, y - 1.2), (x + 1.2, y - 1.8), (x, y - 2.4)],
                             fc="none", ec=c, lw=1.1, zorder=6))

    def stage(x, wd, y, c, nm):
        box(ax, x, y - 2.6, wd, 5.2, fc=WHITE, ec=c, lw=1.5, r=0.5)
        ax.text(x + wd / 2, y, nm, ha="center", va="center", fontsize=8.0, color=NAVY)

    title(ax, 50, H - 2.0, "Pipelining — trade latency for throughput by inserting registers",
          13.0, NAVY)

    # ---------------- BEFORE ----------------
    y1 = 25.0
    box(ax, 2.0, y1 - 8.0, 96.0, 12.6, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(6.0, y1 + 3.0, "BEFORE — one long combinational path", ha="left", va="center",
            fontsize=9.4, color=RED, fontweight="bold")
    ffbox(8.0, y1 - 2.0, RED)
    arrow(ax, 4.4, y1 - 2.0, 7.8, y1 - 2.0, color=INK, lw=1.4, ms=8)
    xs = 16.0
    for nm, wd in [("multiply", 18.0), ("add", 14.0), ("saturate", 16.0)]:
        arrow(ax, xs - 3.6, y1 - 2.0, xs - 0.2, y1 - 2.0, color=INK, lw=1.4, ms=8)
        stage(xs, wd, y1 - 2.0, RED, nm)
        xs += wd + 3.6
    arrow(ax, xs - 3.6, y1 - 2.0, xs - 0.2, y1 - 2.0, color=INK, lw=1.4, ms=8)
    ffbox(xs, y1 - 2.0, RED)
    arrow(ax, xs + 4.4, y1 - 2.0, xs + 7.8, y1 - 2.0, color=INK, lw=1.4, ms=8)
    ax.text(50, y1 - 6.4, "T_clk ≥ t_cq + (multiply + add + saturate) + t_setup      →  "
            "one long path, a slow clock, 1-cycle latency",
            ha="center", va="center", fontsize=8.2, color=RED, fontweight="bold")

    # ---------------- AFTER ----------------
    y2 = 10.6
    box(ax, 2.0, y2 - 8.0, 96.0, 12.6, fc="#E4F4EC", ec=GREEN, lw=1.6)
    ax.text(6.0, y2 + 3.0, "AFTER — a register between every stage", ha="left", va="center",
            fontsize=9.4, color=GREEN, fontweight="bold")
    ffbox(8.0, y2 - 2.0, GREEN)
    arrow(ax, 4.4, y2 - 2.0, 7.8, y2 - 2.0, color=INK, lw=1.4, ms=8)
    xs = 15.4
    for nm, wd in [("multiply", 16.0), ("add", 13.0), ("saturate", 15.0)]:
        arrow(ax, xs - 3.0, y2 - 2.0, xs - 0.2, y2 - 2.0, color=INK, lw=1.4, ms=8)
        stage(xs, wd, y2 - 2.0, GREEN, nm)
        xs += wd
        arrow(ax, xs + 0.2, y2 - 2.0, xs + 1.4, y2 - 2.0, color=INK, lw=1.4, ms=8)
        ffbox(xs + 1.6, y2 - 2.0, GREEN)
        xs += 1.6 + 4.2 + 3.0
    arrow(ax, xs - 3.0, y2 - 2.0, xs - 0.4, y2 - 2.0, color=INK, lw=1.4, ms=8)
    ax.text(50, y2 - 6.4, "T_clk ≥ t_cq + (the LONGEST single stage) + t_setup      →  "
            "a much faster clock, 3-cycle latency, one result every cycle",
            ha="center", va="center", fontsize=8.2, color=GREEN, fontweight="bold")

    ax.text(50, 1.4, "Latency is how long ONE item takes. Throughput is how many finish per second. "
            "Pipelining makes latency worse and throughput much better.",
            ha="center", va="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "pipelining")


def memory_inference():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 36.92
    title(ax, 50, H - 2.0, "Inferring memory — write the pattern the tool recognises", 13.0, NAVY)
    panels = [("ROM — read only", TEAL, "#E8F5F7",
               ["always @(posedge clk)", "    case (addr)", "      4'd0: q <= 8'h3F;",
                "      4'd1: q <= 8'h06;", "      default: q <= 8'h00;", "    endcase"],
               "a look-up table, or\ninitialised block RAM"),
              ("Single-port RAM", GREEN, "#E4F4EC",
               ["reg [7:0] mem [0:255];", "always @(posedge clk) begin",
                "    if (we) mem[addr] <= din;", "    q <= mem[addr];", "end"],
               "ONE block RAM —\nthe registered read is\nwhat makes it inferable"),
              ("Register file", AMBER, "#FFF6EC",
               ["reg [31:0] rf [0:31];", "always @(posedge clk)",
                "    if (we) rf[wa] <= wd;", "assign rd0 = rf[ra0];",
                "assign rd1 = rf[ra1];"],
               "ASYNCHRONOUS reads →\nbuilt from flip-flops and\nMUXes, not block RAM")]
    cw = 31.4
    for i, (nm, c, bg, lines, note) in enumerate(panels):
        x = 2.0 + i * (cw + 1.5)
        box(ax, x, 5.0, cw, 24.5, fc=bg, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x, 24.5), cw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 24.5), cw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, 27.0, nm, ha="center", va="center", fontsize=9.8,
                color="white", fontweight="bold", zorder=6)
        for j, ln in enumerate(lines):
            ax.text(x + 1.6, 22.0 - j * 1.9, ln, ha="left", va="center", fontsize=7.2,
                    color=BODY, family="DejaVu Sans Mono")
        ax.text(x + cw / 2, 8.4, note, ha="center", va="center", fontsize=7.4,
                color=c, fontweight="bold", linespacing=1.6)
    box(ax, 2.0, 1.0, 96.0, 3.2, fc="#FDECEF", ec=RED, lw=1.5)
    ax.text(50, 2.6, "The difference that decides everything: a REGISTERED read infers block RAM; "
            "an ASYNCHRONOUS read infers flip-flops — far larger.",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold")
    save(f, "memory_inference")


if __name__ == "__main__":
    inference_map(); case_to_mux(); rtl_flow(); toolchains()
    vivado_flow(); debug_ladder(); pipelining(); memory_inference()
