# -*- coding: utf-8 -*-
"""Topic 4c diagrams: writing RTL for real circuits, plus tooling."""
import _boot
from dsl import *
import numpy as np


def hierarchy():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 36.92
    title(ax, 50, H - 2.0, "Hierarchy — building a design out of instantiated modules", 13.0, NAVY)
    # top box
    box(ax, 8.0, 8.0, 46.0, 22.0, fc=LIGHT, ec=NAVY, lw=2.0)
    ax.text(31.0, 28.0, "module  cpu_top", ha="center", va="center", fontsize=10.5,
            color=NAVY, fontweight="bold", family="DejaVu Sans Mono")
    kids = [("u_alu", "alu", TEAL, 22.0), ("u_regfile", "regfile", GREEN, 16.6),
            ("u_ctrl", "controller", AMBER, 11.2)]
    for inst, mod, c, yy in kids:
        box(ax, 12.0, yy - 2.0, 38.0, 4.2, fc=WHITE, ec=c, lw=1.6, r=0.6)
        ax.text(14.0, yy, mod, ha="left", va="center", fontsize=9.0, color=c,
                fontweight="bold", family="DejaVu Sans Mono")
        ax.text(48.0, yy, inst, ha="right", va="center", fontsize=9.0, color=NAVY,
                family="DejaVu Sans Mono")
    ax.text(31.0, 6.0, "one MODULE can be instantiated many times;\n"
            "each INSTANCE has its own name", ha="center", va="center",
            fontsize=8.2, color=SLATE, linespacing=1.5, style="italic")

    box(ax, 58.0, 9.0, 40.0, 21.0, fc="#11212F", ec=TEAL, lw=1.8, r=0.8)
    lines = ["alu #(", "    .W (32)", ") u_alu (", "    .clk   (clk),",
             "    .a     (rs1_data),", "    .b     (rs2_data),", "    .op    (alu_op),",
             "    .result(alu_out)", ");"]
    for i, ln in enumerate(lines):
        ax.text(60.5, 27.6 - i * 2.05, ln, ha="left", va="center", fontsize=8.4,
                color="#DCE6F0", family="DejaVu Sans Mono")
    ax.text(78.0, 4.8, "NAMED port connection — always use this. Positional\n"
            "order is legal, and silently wrong the day someone adds a port.",
            ha="center", va="center", fontsize=7.8, color=SLATE, linespacing=1.5, style="italic")
    save(f, "hierarchy")


def parameters():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 35.38
    title(ax, 50, H - 2.0, "Parameters — write a module once, use it at every width", 13.0, NAVY)
    box(ax, 2.0, 12.0, 47.0, 19.0, fc="#11212F", ec=TEAL, lw=1.8, r=0.8)
    src = ["module counter #(", "    parameter W = 8", ")(", "    input             clk,",
           "    input             rst_n,", "    output reg [W-1:0] q", ");",
           "    always @(posedge clk or negedge rst_n)", "        if (!rst_n) q <= {W{1'b0}};",
           "        else        q <= q + 1'b1;", "endmodule"]
    for i, ln in enumerate(src):
        ax.text(4.2, 29.4 - i * 1.62, ln, ha="left", va="center", fontsize=7.6,
                color="#DCE6F0", family="DejaVu Sans Mono")
    ax.text(25.5, 10.2, "ONE source file", ha="center", va="center", fontsize=9.4,
            color=TEAL, fontweight="bold")

    uses = [("counter #(.W(4))  u_small (…);", "4 flip-flops", GREEN),
            ("counter #(.W(16)) u_medium(…);", "16 flip-flops", GREEN),
            ("counter #(.W(64)) u_big   (…);", "64 flip-flops", GREEN)]
    for i, (code, note, c) in enumerate(uses):
        yy = 27.0 - i * 5.4
        box(ax, 52.0, yy - 2.0, 46.0, 4.4, fc=LIGHT, ec=c, lw=1.5, r=0.6)
        ax.text(54.0, yy + 0.4, code, ha="left", va="center", fontsize=8.4,
                color=NAVY, family="DejaVu Sans Mono")
        ax.text(54.0, yy - 1.4, "→  " + note, ha="left", va="center", fontsize=7.8, color=c)
    ax.text(75.0, 10.2, "THREE different circuits", ha="center", va="center", fontsize=9.4,
            color=GREEN, fontweight="bold")

    box(ax, 2.0, 1.2, 96.0, 7.4, fc="#FFF6EC", ec=AMBER, lw=1.6)
    ax.text(50, 7.0, "parameter  vs  localparam  vs  `define", ha="center", va="center",
            fontsize=9.6, color=AMBER, fontweight="bold")
    ax.text(50, 4.4, "parameter — overridable at instantiation. Use for widths, depths, timing.",
            ha="center", va="center", fontsize=8.4, color=BODY)
    ax.text(50, 2.2, "localparam — NOT overridable. Use for state names and derived constants.        "
            "`define — global text substitution; use sparingly.",
            ha="center", va="center", fontsize=8.4, color=BODY)
    save(f, "parameters")


def generate_block():
    W, Hin = 13, 4.4
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 33.85
    title(ax, 50, H - 2.0, "generate — writing N copies of something without writing them out",
          13.0, NAVY)
    box(ax, 2.0, 10.0, 45.0, 19.0, fc="#11212F", ec=TEAL, lw=1.8, r=0.8)
    src = ["genvar i;", "generate", "  for (i = 0; i < W; i = i + 1) begin : bit_slice",
           "    full_adder u_fa (", "      .a   (a[i]),", "      .b   (b[i]),",
           "      .cin (c[i]),", "      .sum (sum[i]),", "      .cout(c[i+1])", "    );",
           "  end", "endgenerate"]
    for i, ln in enumerate(src):
        ax.text(4.2, 27.2 - i * 1.5, ln, ha="left", va="center", fontsize=7.4,
                color="#DCE6F0", family="DejaVu Sans Mono")

    arrow(ax, 48.0, 19.5, 54.0, 19.5, color=SLATE, lw=2.4, ms=13)
    ax.text(51.0, 21.8, "elaborates to", ha="center", va="center", fontsize=8.0,
            color=SLATE, style="italic")
    for i in range(4):
        x = 56.0 + i * 10.6
        box(ax, x, 16.0, 9.0, 7.0, fc=WHITE, ec=GREEN, lw=1.6, r=0.6)
        ax.text(x + 4.5, 20.4, "FA", ha="center", va="center", fontsize=9.0,
                color=GREEN, fontweight="bold")
        ax.text(x + 4.5, 17.8, "bit_slice[%d]" % i, ha="center", va="center", fontsize=6.4,
                color=SLATE)
        if i < 3:
            arrow(ax, x + 9.2, 19.5, x + 10.4, 19.5, color=RED, lw=1.4, ms=8)
    ax.text(77.0, 13.6, "four real, separate instances", ha="center", va="center",
            fontsize=8.6, color=GREEN, fontweight="bold")

    box(ax, 2.0, 1.5, 96.0, 6.8, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(50, 6.4, "generate is ELABORATION-time, not run-time", ha="center", va="center",
            fontsize=9.6, color=TEAL, fontweight="bold")
    ax.text(50, 3.6, "The loop runs once, while the tool is building the design. Nothing "
            "'iterates' in hardware.\nThe  : bit_slice  label is not optional decoration — it "
            "names the instances, and you need those names for timing reports and waveforms.",
            ha="center", va="center", fontsize=8.2, color=BODY, linespacing=1.7)
    save(f, "generate_block")


def synth_subset():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 40.0
    title(ax, 50, H - 2.0, "The synthesisable subset — what becomes hardware and what does not",
          13.0, NAVY)
    cols = [("SYNTHESISABLE", GREEN, "#E4F4EC",
             ["module / endmodule, ports", "wire, reg, parameter, localparam",
              "assign", "always @(*) and @(posedge clk)", "if / else, case / casez",
              "for loops with CONSTANT bounds", "function", "generate / genvar",
              "all operators except / and %", "  (unless by a power of two)"]),
            ("SIMULATION ONLY", RED, "#FDECEF",
             ["initial blocks", "#delays  ( #10 )", "wait, fork / join", "while, forever, repeat",
              "task with timing", "\\$display, \\$monitor, \\$finish", "\\$random, \\$readmemh",
              "real, time, event", "=== and !==", "force / release"])]
    cw = 47.0
    for i, (nm, c, bg, items) in enumerate(cols):
        x = 2.0 + i * (cw + 2.0)
        box(ax, x, 5.5, cw, 27.0, fc=bg, ec=c, lw=1.9)
        ax.add_patch(FancyBboxPatch((x, 27.5), cw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 27.5), cw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, 30.0, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=6)
        for j, it in enumerate(items):
            ax.text(x + 2.4, 25.0 - j * 2.1, ("·  " if not it.startswith("  ") else "   ") + it,
                    ha="left", va="center", fontsize=8.2, color=BODY)
    box(ax, 2.0, 1.0, 96.0, 3.4, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 2.7, "Simulation-only constructs are not bad — you need them in every testbench. "
            "They just must never appear in a design module.",
            ha="center", va="center", fontsize=9.0, color=NAVY, fontweight="bold")
    save(f, "synth_subset")


def testbench_anatomy():
    W, Hin = 13, 5.8
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 44.62
    title(ax, 50, H - 2.0, "Anatomy of a self-checking testbench", 13.0, NAVY)
    box(ax, 2.0, 35.3, 96.0, 6.2, fc="#E4F4EC", ec=GREEN, lw=1.6)
    ax.text(50, 39.6, "A testbench you have to READ A WAVEFORM to grade is a testbench that "
            "will not catch a regression.",
            ha="center", va="center", fontsize=9.2, color=NAVY, fontweight="bold")
    ax.text(50, 36.9, "Waveforms are for DIAGNOSING a failure; the PASS/FAIL message is for "
            "DETECTING one. You need both, and they do different jobs.",
            ha="center", va="center", fontsize=8.4, color=BODY, style="italic")

    dut_y = 14.0
    box(ax, 40.0, dut_y, 20.0, 10.0, fc=WHITE, ec=NAVY, lw=2.0)
    ax.text(50.0, dut_y + 6.6, "DUT", ha="center", va="center", fontsize=12,
            color=NAVY, fontweight="bold")
    ax.text(50.0, dut_y + 3.0, "the module\nyou are testing", ha="center", va="center",
            fontsize=7.8, color=SLATE, linespacing=1.4)

    blocks = [("CLOCK generator", TEAL, 8.0, 24.0, "always #5 clk = ~clk;"),
              ("RESET sequence", TEAL, 8.0, 13.0, "#12 rst_n = 1'b1;"),
              ("STIMULUS", AMBER, 8.0, 2.0, "drive the inputs"),
              ("REFERENCE model", GREEN, 70.0, 24.0, "what SHOULD happen"),
              ("CHECKER", GREEN, 70.0, 13.0, "if (got !== exp) errors++"),
              ("WAVEFORM dump", VIOLET, 70.0, 2.0, "\\$dumpfile / \\$dumpvars")]
    for nm, c, x, y, sub in blocks:
        box(ax, x, y, 22.0, 8.6, fc=LIGHT, ec=c, lw=1.7)
        ax.text(x + 11.0, y + 6.0, nm, ha="center", va="center", fontsize=8.8,
                color=c, fontweight="bold")
        ax.text(x + 11.0, y + 2.4, sub, ha="center", va="center", fontsize=6.8,
                color=BODY, family="DejaVu Sans Mono")
        if x < 40:
            arrow(ax, 30.4, y + 4.3, 39.4, dut_y + 5.0, color=c, lw=1.5, ms=9)
        else:
            arrow(ax, 60.6, dut_y + 5.0, 69.4, y + 4.3, color=c, lw=1.5, ms=9)
    save(f, "testbench_anatomy")


def uart_frame():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 35.38
    title(ax, 50, H - 2.0, "A real design target — the UART frame", 13.0, NAVY)
    x0, seg = 5.0, 8.4
    y = 20.0
    hgt = 6.0
    fields = [("idle", "1", SLATE), ("START", "0", RED), ("D0", "1", TEAL), ("D1", "0", TEAL),
              ("D2", "1", TEAL), ("D3", "1", TEAL), ("D4", "0", TEAL), ("D5", "1", TEAL),
              ("D6", "0", TEAL), ("D7", "0", TEAL), ("STOP", "1", GREEN)]
    for i, (nm, bit, c) in enumerate(fields):
        x = x0 + i * seg
        box(ax, x, y, seg - 0.6, hgt, fc=c, ec="white", lw=1.2, r=0.5)
        ax.text(x + (seg - 0.6) / 2, y + hgt / 2 + 0.9, nm, ha="center", va="center",
                fontsize=7.6, color="white", fontweight="bold")
        ax.text(x + (seg - 0.6) / 2, y + hgt / 2 - 1.8, bit, ha="center", va="center",
                fontsize=8.6, color="white", family="DejaVu Sans Mono")
    ax.text(50, 28.4, "one character = 10 bit-times, LSB first, no parity  (8N1)",
            ha="center", va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    arrow(ax, x0, 17.4, x0 + seg, 17.4, color=SLATE, lw=1.4, ms=8, style="<|-|>")
    ax.text(x0 + seg / 2, 15.4, "1 bit time", ha="center", va="center", fontsize=7.6,
            color=SLATE)
    ax.text(50, 12.6, "at 115 200 baud with a 50 MHz clock:   50 000 000 / 115 200  =  434 clocks "
            "per bit", ha="center", va="center", fontsize=9.2, color=AMBER, fontweight="bold")
    box(ax, 2.0, 1.5, 47.0, 8.6, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(25.5, 8.2, "Transmitter — an FSM plus a shift register", ha="center", va="center",
            fontsize=9.0, color=TEAL, fontweight="bold")
    ax.text(25.5, 4.6, "IDLE → START → DATA (×8) → STOP → IDLE,\n"
            "clocked by a baud-rate tick from a counter.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    box(ax, 51.0, 1.5, 47.0, 8.6, fc="#FFF6EC", ec=AMBER, lw=1.6)
    ax.text(74.5, 8.2, "Receiver — the same, plus one trick", ha="center", va="center",
            fontsize=9.0, color=AMBER, fontweight="bold")
    ax.text(74.5, 4.6, "Sample each bit in its MIDDLE, not at its edge —\n"
            "wait half a bit time after detecting the start bit.",
            ha="center", va="center", fontsize=8.0, color=BODY, linespacing=1.6)
    save(f, "uart_frame")


def fifo_structure():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 35.38
    title(ax, 50, H - 2.0, "A synchronous FIFO — the classic 'put it all together' design",
          13.0, NAVY)
    # memory array
    n = 8
    cw = 8.2
    x0, y = 22.0, 17.0
    used = {2: "0x41", 3: "0x42", 4: "0x43"}
    for i in range(n):
        x = x0 + i * cw
        filled = i in used
        box(ax, x, y, cw - 0.6, 7.0, fc="#E4F4EC" if filled else LIGHT,
            ec=GREEN if filled else GRID, lw=1.5, r=0.5)
        ax.text(x + (cw - 0.6) / 2, y + 4.6, str(i), ha="center", va="center",
                fontsize=7.0, color=SLATE)
        if filled:
            ax.text(x + (cw - 0.6) / 2, y + 2.2, used[i], ha="center", va="center",
                    fontsize=8.0, color=GREEN, fontweight="bold", family="DejaVu Sans Mono")
    ax.text(x0, y + 9.0, "mem  [7:0]", ha="left", va="center", fontsize=9.0,
            color=NAVY, fontweight="bold", family="DejaVu Sans Mono")
    # pointers
    for idx, lab, c in [(2, "rd_ptr", TEAL), (5, "wr_ptr", AMBER)]:
        px = x0 + idx * cw + (cw - 0.6) / 2
        arrow(ax, px, y - 4.2, px, y - 0.4, color=c, lw=2.0, ms=11)
        ax.text(px, y - 5.8, lab, ha="center", va="center", fontsize=8.4,
                color=c, fontweight="bold")
    arrow(ax, 6.0, y + 3.5, 20.0, y + 3.5, color=AMBER, lw=2.0, ms=11)
    ax.text(13.0, y + 5.6, "wr_data", ha="center", va="center", fontsize=8.4,
            color=AMBER, fontweight="bold")
    arrow(ax, x0 + n * cw, y + 3.5, x0 + n * cw + 8.0, y + 3.5, color=TEAL, lw=2.0, ms=11)
    ax.text(x0 + n * cw + 4.0, y + 5.6, "rd_data", ha="center", va="center", fontsize=8.4,
            color=TEAL, fontweight="bold")

    cards = [("full", RED, "wr_ptr + 1 == rd_ptr\n(one slot always wasted)\nor use an extra count bit"),
             ("empty", TEAL, "wr_ptr == rd_ptr"),
             ("the classic bug", AMBER, "full and empty look IDENTICAL\nwith plain pointers —\nthat is why you need the extra bit")]
    for i, (nm, c, txt) in enumerate(cards):
        x = 2.0 + i * 32.6
        box(ax, x, 1.5, 31.0, 8.4, fc=LIGHT, ec=c, lw=1.6)
        ax.text(x + 15.5, 8.4, nm, ha="center", va="center", fontsize=9.2,
                color=c, fontweight="bold")
        ax.text(x + 15.5, 4.6, txt, ha="center", va="center", fontsize=7.4,
                color=BODY, linespacing=1.6)
    save(f, "fifo_structure")


if __name__ == "__main__":
    hierarchy(); parameters(); generate_block(); synth_subset()
    testbench_anatomy(); uart_frame(); fifo_structure()
