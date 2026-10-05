# -*- coding: utf-8 -*-
"""Lecture 01 diagrams — the practical component."""
import _boot
from dsl import *
from l1_kit import wrap, note, column_cards, rowcards, chars_for

CARDS = {
    "toolchain": (
        "Why these four, and why they are free",
        "Every tool here is open source and runs on Windows, macOS and Linux. "
        "Nothing in Lecture 01 needs a licence, a university server or a "
        "vendor account — which means you can do all of it on your own "
        "machine, tonight.", "GREEN"),
    "install_routes": (
        "If you are on Windows, use WSL",
        "Windows Subsystem for Linux gives you a real Ubuntu inside Windows, "
        "and every command in this lab then works unchanged. Install it once "
        "with  wsl --install  in an Administrator PowerShell, restart, and "
        "follow the Linux column.", "AMBER"),
    "lab_map": (
        "Every claim in this lecture is checked by one of these",
        "The theory section asserts that a CAD tool rewrites one hardware "
        "description as a more detailed one without changing what it does. "
        "Lab 2 proves exactly that, on your own machine, in about thirty "
        "seconds.", "NAVY"),
    "measured": (
        "These are measured numbers, not illustrations",
        "Every figure on this slide came out of Yosys 0.33 running on the "
        "counter in rtl/counter4.v. Run  make ladder  and you will get the "
        "same table. If your version of Yosys gives slightly different "
        "numbers, that is itself worth discussing — optimisation is not "
        "unique.", "TEAL"),
}


def toolchain():
    f, ax, H = panel(4.14)
    title(ax, 50, H - 3.5, "Four free programs, one for each thing the lecture "
          "says a CAD flow must do", size=FS_SUB, color=SLATE, weight="normal")

    column_cards(ax, 2.5, H - 7, 95.5, [
        ("ICARUS VERILOG\nthe simulator",
         "Compiles Verilog and runs it. This is how you check that a "
         "description behaves the way you meant. Command: iverilog, then vvp.",
         GREEN),
        ("GTKWAVE\nthe waveform viewer",
         "Draws the signals a simulation recorded, so you can look at a clock "
         "edge and see what happened. Reads the .vcd file the test bench "
         "writes.", TEAL),
        ("YOSYS\nthe synthesiser",
         "The CAD tool of the lecture's central slide: it reads your HDL and "
         "writes a more detailed HDL. This is what turns behaviour into "
         "gates.", VIOLET),
        ("GHDL\nthe VHDL simulator",
         "The same job as Icarus, for the other language — so you can compare "
         "the two on identical stimulus in Lab 5.", AMBER)], gap=1.8)
    save(f, "toolchain")


def install_routes():
    f, ax, H = panel(3.99)

    cols = [("LINUX  (Ubuntu / Debian)", GREEN,
             ["sudo apt update", "sudo apt install -y \\",
              "    iverilog gtkwave yosys ghdl"]),
            ("macOS  (Homebrew)", TEAL,
             ["brew install icarus-verilog", "brew install --cask gtkwave",
              "brew install yosys ghdl"]),
            ("WINDOWS  (via WSL)", VIOLET,
             ["wsl --install", "# then, inside Ubuntu:",
              "sudo apt install -y \\", "    iverilog gtkwave yosys ghdl"])]
    top = H - 1.5
    bh = 20.5
    w = 30.8
    gap = 1.55
    for i, (head, col, lines) in enumerate(cols):
        x = 2.5 + i * (w + gap)
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.2, w, 4.2, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.1, head, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        box(ax, x + 1.6, top - bh + 1.6, w - 3.2, bh - 7.4, fc="#11212F",
            ec="#11212F", lw=0)
        for j, ln in enumerate(lines):
            ax.text(x + 3.0, top - 7.6 - j * 3.0, ln, ha="left", va="center",
                    fontsize=7.4, color="#DCE6F0", family="DejaVu Sans Mono")
    save(f, "install_routes")


def verify_install():
    f, ax, H = panel(3.84)
    title(ax, 50, H - 3.5, "Run these four commands. Each must print a version "
          "number.", size=FS_SUB, color=SLATE, weight="normal")

    rows = [("iverilog -V", "Icarus Verilog version 12.0 (or later)", GREEN),
            ("yosys -V", "Yosys 0.33 (or later)", VIOLET),
            ("ghdl --version", "GHDL 4.1.0 (or later)", AMBER),
            ("gtkwave --version", "GTKWave Analyzer v3.3 (or later)", TEAL)]
    y = H - 7
    rh = 5.0
    for cmd, expect, col in rows:
        box(ax, 2.5, y - rh, 95.5, rh, fc=WHITE, ec=GRID, lw=1.1)
        box(ax, 2.5, y - rh, 1.3, rh, fc=col, ec=col, lw=0, r=0.4)
        box(ax, 5.5, y - rh + 0.9, 28.0, rh - 1.8, fc="#11212F", ec="#11212F",
            lw=0)
        ax.text(7.5, y - rh / 2, "$ " + cmd, ha="left", va="center",
                fontsize=FS_MONO - 0.5, color="#DCE6F0",
                family="DejaVu Sans Mono")
        ax.text(37.5, y - rh / 2, "→   " + expect, ha="left", va="center",
                fontsize=FS_SMALL, color=col)
        y -= rh + 0.8

    ax.text(50, y - 2.4, "If any of the four is missing, fix that before going "
            "on — every lab below needs all of them.", ha="center", va="center",
            fontsize=FS_SMALL, color=NAVY, fontweight="bold")
    save(f, "verify_install")


def lab_map():
    f, ax, H = panel(5.10)

    column_cards(ax, 2.5, H - 2, 95.5, [
        ("LAB 1\nmake sim",
         "Simulate the counter and look at its waveform. Proves you can run a "
         "description and see what it does — the \"simulation for "
         "verification\" step of the flow.", GREEN),
        ("LAB 2\nmake transform\nmake prove",
         "Watch Yosys read your Verilog and write more Verilog, twice. Then "
         "run the SAME test bench against the gate netlist and get the same "
         "waveform. The lecture's central claim, checked.", VIOLET),
        ("LAB 3\nmake ladder",
         "Count the cells at each level of the flow: 10 lines of source, then "
         "2 RTL cells, then 10 gate-level cells. The ladder, in numbers.",
         TEAL),
        ("LAB 4\nmake target",
         "Map the same design for an ASIC and for an FPGA, and compare. Six "
         "gates and four flip-flops, against four LUTs and four flip-flops.",
         AMBER),
        ("LAB 5\nmake langs",
         "Write the counter again in VHDL, simulate both, and diff the "
         "waveforms. They match from the end of reset onwards — and where "
         "they differ, the difference is instructive.", RED)],
        gap=1.6, head_h=9.0)
    save(f, "lab_map")


def measured():
    f, ax, H = panel(4.04)
    title(ax, 50, H - 3.5, "Yosys 0.33, on rtl/counter4.v — reproduce it with  "
          "make ladder", size=FS_SUB, color=SLATE, weight="normal")

    headers = ["Level of the flow", "Cells", "What they are"]
    rows = [["1 · Behavioural source", "—", "10 lines of Verilog — no cells yet"],
            ["2 · Data path (RTL)", "2", "1 adder, 1 four-bit register"],
            ["3 · Logic, for an ASIC", "10",
             "4 flip-flops + AND, NAND, NOT, XNOR, XOR ×2"],
            ["3 · Logic, for an FPGA", "8", "4 flip-flops + 4 look-up tables"]]
    colcol = [NAVY, TEAL, GREEN, AMBER]
    widths = [31.0, 12.0, 52.5]
    x0 = 2.5
    y = H - 7
    rh = 4.6
    cx = x0
    for wdt, h in zip(widths, headers):
        box(ax, cx, y - rh, wdt, rh, fc=NAVY, ec=NAVY, lw=0.8, r=0.0)
        ax.text(cx + wdt / 2, y - rh / 2, h, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        cx += wdt
    y -= rh
    for i, row in enumerate(rows):
        cx = x0
        for j, (wdt, cell) in enumerate(zip(widths, row)):
            box(ax, cx, y - rh, wdt, rh, fc=WHITE if i % 2 == 0 else LIGHT,
                ec=GRID, lw=0.8, r=0.0)
            ax.text(cx + wdt / 2, y - rh / 2, cell, ha="center", va="center",
                    fontsize=FS_SMALL - 0.5 if j != 1 else FS_BODY,
                    color=colcol[i] if j < 2 else BODY,
                    fontweight="bold" if j < 2 else "normal")
            cx += wdt
        y -= rh

    ax.text(50, y - 3.2, "Same circuit every time. Only the vocabulary changes "
            "— and the number of words needed to say it.", ha="center",
            va="center", fontsize=FS_SMALL, color=NAVY, fontweight="bold")
    save(f, "measured")


if __name__ == "__main__":
    toolchain()
    install_routes()
    verify_install()
    lab_map()
    measured()
