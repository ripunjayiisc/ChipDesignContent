# -*- coding: utf-8 -*-
"""Topic 5 diagrams — tools, regression and verification maturity."""
import _boot
from dsl import *


def tool_matrix():
    W, Hin = 11.5, 5.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 47.0
    title(ax, 50, H - 3.2, "The verification jobs, and the tool that does each one", 12.5)

    cols = ["job", "open-source", "Vivado", "ModelSim / Questa"]
    rows = [["static checks (lint)", "verilator --lint-only -Wall", "report_methodology", "vlog warnings"],
            ["simulate Verilog", "iverilog + vvp", "xvlog / xelab / xsim", "vlog / vsim"],
            ["simulate SystemVerilog", "verilator --binary --timing", "xvlog -sv", "vlog -sv"],
            ["concurrent assertions", "verilator --assert (subset)", "full SVA", "full SVA"],
            ["waveforms", "GTKWave (.vcd)", "built-in wave window", "wave window (.wlf)"],
            ["code coverage", "verilator --coverage", "-cover, report_coverage", "vlog -cover bcesx"],
            ["functional coverage", "by hand (see Lab V4)", "SV covergroups", "SV covergroups"],
            ["regression", "shell / Makefile", "TCL batch", "TCL .do batch"]]
    cw = [26, 26, 22, 24]
    table(ax, 50 - sum(cw) / 2, H - 8.0, cols, rows, cw, 3.4, size=8.0, bold_col=0)
    ax.text(50, 2.4, "Everything in Topic5_Lab was run with the open-source column. "
                     "The vendor scripts are working templates, not captured runs.",
            ha="center", fontsize=8.6, color=RED, fontweight="bold")
    save(f, "tool_matrix")


def regression_loop():
    W, Hin = 12.0, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 38.3
    title(ax, 50, H - 3, "A regression is what turns random stimulus into evidence", 12.5)

    steps = [("COMMIT", "somebody changes\nthe RTL", NAVY),
             ("LINT", "one second", GREEN),
             ("LABS V1-V4", "every directed and\nrandom test", TEAL),
             ("SEEDS x PROFILES", "12 runs, each one\nreproducible", VIOLET),
             ("COVERAGE MERGE", "what did the whole\nregression reach?", AMBER),
             ("VERDICT", "green, or a seed\nto reproduce", RED)]
    bw, gap = 14.0, 2.6
    x0 = 50 - (6 * bw + 5 * gap) / 2
    ytop = H - 9.5
    for i, (name, sub, col) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 13.0, bw, 13.0, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, ytop - 4.3, bw, 4.3, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.15, name, ha="center", va="center", fontsize=7.6,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ytop - 8.8, sub, ha="center", va="center", fontsize=7.8,
                color=BODY)
        if i < 5:
            arrow(ax, x + bw, ytop - 6.5, x + bw + gap, ytop - 6.5, color=SLATE, lw=1.6)

    xa = x0 + 5 * (bw + gap) + bw / 2
    xb = x0 + bw / 2
    wire(ax, [(xa, ytop - 13.0), (xa, 11.0), (xb, 11.0), (xb, ytop - 13.0)],
         color=RED, lw=1.7)
    arrow(ax, xb, 12.0, xb, ytop - 13.0, color=RED, lw=1.7)
    ax.text(50, 9.0, "a failing seed goes straight back to the designer, with the exact "
                     "command that reproduces it",
            ha="center", fontsize=8.6, color=RED, fontweight="bold")
    ax.text(50, 4.6, "Run it on every commit. A regression that is run \"when we remember\" "
                     "is a regression that has already stopped working.",
            ha="center", fontsize=8.6, color=BODY, fontstyle="italic")
    save(f, "regression_loop")


def ver_maturity():
    W, Hin = 11.5, 5.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 47.0
    title(ax, 50, H - 3, "The verification maturity ladder — where is your testbench?", 12.5)

    levels = [("0", "prints values; a human reads the transcript", RED,
               "not a testbench at all"),
              ("1", "hard-coded expected values, PASS / FAIL printed", AMBER,
               "V1  —  catches 0 of 5 bugs"),
              ("2", "a reference model checked every cycle, plus the corners", TEAL,
               "V2  —  catches 4 of 5"),
              ("3", "constrained-random, seeded, run as a regression", GREEN,
               "V3  —  catches 5 of 5"),
              ("4", "functional coverage, merged, with a closure verdict", GREEN,
               "V4  —  tells you when to STOP"),
              ("5", "layered environment, plus assertions bound to the DUT", VIOLET,
               "V6  —  reports at the cycle the rule broke")]
    ytop = H - 8.0
    rh = 5.6
    for i, (n, txt, col, note) in enumerate(levels):
        y = ytop - (i + 1) * rh
        cy = y + (rh - 1.0) / 2
        box(ax, 11, y, 50, rh - 1.0, fc=col, ec=col, r=0.5)
        ax.add_patch(Circle((7.0, cy), 2.4, fc=col, ec=col, zorder=5))
        ax.text(7.0, cy, n, ha="center", va="center", fontsize=8.8, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(12.8, cy, txt, ha="left", va="center", fontsize=7.9, color=WHITE,
                fontweight="bold")
        ax.text(63.5, cy, note, ha="left", va="center", fontsize=8.0, color=col,
                fontweight="bold")
    ax.text(50, 3.2, "Level 3 is the minimum for anything that will be manufactured.",
            ha="center", fontsize=8.8, color=NAVY, fontweight="bold")
    ax.text(50, 0.6, "Levels 4 and 5 are what a professional verification team is measured on.",
            ha="center", fontsize=8.6, color=BODY)
    save(f, "ver_maturity")


def install_map():
    W, Hin = 11.5, 5.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 45.2
    title(ax, 50, H - 3, "What to install, and what each one is for", 12.5)

    items = [("iverilog", "compile + simulate\nVerilog-2005", "sudo apt install iverilog", TEAL),
             ("verilator", "lint, and run\nSystemVerilog + SVA", "sudo apt install verilator", VIOLET),
             ("gtkwave", "view .vcd\nwaveforms", "sudo apt install gtkwave", GREEN),
             ("make", "drive the whole\nregression", "usually already there", SLATE)]
    bw, gap = 21.0, 4.0
    x0 = 50 - (4 * bw + 3 * gap) / 2
    ytop = H - 8.5
    for i, (name, body, cmd, col) in enumerate(items):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 18.0, bw, 18.0, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, ytop - 4.4, bw, 4.4, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.2, name, ha="center", va="center", fontsize=9.2,
                color=WHITE, fontweight="bold", family="monospace")
        ax.text(x + bw / 2, ytop - 8.6, body, ha="center", va="center", fontsize=8.0,
                color=BODY)
        ax.text(x + bw / 2, ytop - 14.8, cmd, ha="center", va="center", fontsize=7.0,
                color=SLATE, family="monospace")

    box(ax, 4, 3.5, 92, 12.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.1, "One line installs the whole open-source verification flow",
            fontsize=9.6, color=NAVY, fontweight="bold", ha="center")
    ax.text(50, 9.2, "sudo apt update && sudo apt install -y iverilog gtkwave verilator yosys graphviz",
            fontsize=9.0, color=GREEN, ha="center", family="monospace")
    ax.text(50, 5.8, "Windows: run the same line inside WSL2, or use the OSS CAD Suite.   "
                     "macOS: brew install icarus-verilog verilator gtkwave",
            fontsize=8.2, color=BODY, ha="center")
    save(f, "install_map")


if __name__ == "__main__":
    tool_matrix(); regression_loop(); ver_maturity(); install_map()
