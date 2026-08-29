# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — tools, installation and the lab programme."""
import _boot
from dsl import *


def tool_landscape():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "The tools, and what each one is for", FS_TITLE)

    rows = [["Icarus Verilog", "free", "simulate Verilog", "this lab"],
            ["GHDL", "free", "simulate VHDL", "this lab"],
            ["GTKWave", "free", "look at the waveforms", "this lab"],
            ["Yosys", "free", "synthesise, and prove equivalence", "this lab"],
            ["Verilator", "free", "fast simulation, a good linter", "recommended"],
            ["rtl_lint.py", "you write it", "the seven coding rules", "this lab"],
            ["Vivado", "free WebPACK", "synthesis for Xilinx parts",
             "syllabus tool"],
            ["ModelSim / Questa", "free starter", "simulation, both languages",
             "syllabus tool"],
            ["Design Compiler", "commercial", "ASIC synthesis", "industry"]]
    table(ax, 3, H - 10.0, ["tool", "licence", "what it does", "used in"],
          rows, [24, 18, 36, 16], 3.9, size=FS_TABLE, bold_col=[0])

    ax.text(50, 5.5, "Yosys is the interesting one: the only free tool here "
                     "that both synthesises your RTL",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 2.0, "and PROVES the netlist it produced is equivalent to what "
                     "you wrote.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "tool_landscape")


def install_required():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Install this, and the whole lab runs", FS_TITLE,
          color=GREEN)

    y = H - 10.0
    bh = 20.0
    box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=GREEN, lw=2.0)
    box(ax, 3, y - 6.0, 94, 6.0, fc=GREEN, ec=GREEN)
    ax.text(6, y - 3.0, "REQUIRED", ha="left", va="center", fontsize=FS_HEAD,
            color=WHITE, fontweight="bold")
    ax.text(94, y - 3.0, "Debian / Ubuntu / WSL2", ha="right", va="center",
            fontsize=FS_SMALL, color=WHITE, fontstyle="italic")
    lines = ["sudo apt update",
             "sudo apt install yosys iverilog gtkwave python3",
             "sudo apt install ghdl        # only for the VHDL comparison"]
    yy = y - 10.0
    for ln in lines:
        ax.text(7, yy, ln, ha="left", va="center", fontsize=FS_MONO, color=NAVY,
                family="monospace", fontweight="bold")
        yy -= 4.0

    box(ax, 3, y - bh - 12.5, 94, 10.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, y - bh - 5.0, "yosys -V  &&  iverilog -V  &&  ghdl --version",
            fontsize=FS_BODY, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, y - bh - 9.5, "Three version strings, and every target in the "
                              "lab Makefile will run.",
            fontsize=FS_SMALL, color=BODY, ha="center")

    ax.text(50, 3.0, "Without ghdl, everything except  make langs  still works.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "install_required")


def install_vendor():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The vendor tools the syllabus names", FS_TITLE)

    rows = [["1", "Create a free AMD/Xilinx account",
             "no account, no download"],
            ["2", "Download the Unified Installer (~200 MB)",
             "not the 40 GB full archive"],
            ["3", "Choose Vivado ML Edition, then ML Standard",
             "Standard is free; no licence file"],
            ["4", "Deselect every device family but yours",
             "cuts 40 GB to about 8 GB"],
            ["5", "ModelSim: Intel FPGA Starter Edition is free",
             "simulates both languages"],
            ["6", "Verify:  vivado -version,  vsim -version",
             "both then run headless"]]
    table(ax, 3, H - 9.5, ["", "what to do", "watch out for"], rows,
          [7, 52, 35], 4.3, size=FS_TABLE, bold_col=[0])

    ax.text(50, 7.0, "They add a real device library, real timing numbers, and "
                     "a flow you will meet at work.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 2.8, "They add nothing to the CONCEPTS in this topic. Learn "
                     "those on the free tools, where the flow takes seconds.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "install_vendor")


def lab_flow():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Four questions about one piece of code", FS_TITLE)

    yb = H - 17.0
    label_box(ax, 38, yb, 24, 9.0, "your RTL", fc=WHITE, ec=NAVY, tc=NAVY,
              size=FS_HEAD, lw=2.2)

    outs = [(4, "rtl_lint.py", "does it follow\nthe rules?", TEAL),
            (28, "iverilog", "does it do what\nthe spec says?", VIOLET),
            (52, "yosys", "what will actually\nbe built?", GREEN),
            (76, "yosys sat", "is that still the\ndesign you wrote?", AMBER)]
    for x, tool, q, col in outs:
        label_box(ax, x, yb - 15.0, 20, 8.0, tool, fc=LIGHT, ec=col, tc=col,
                  size=FS_SMALL, lw=1.8)
        ax.text(x + 10, yb - 20.5, q, fontsize=FS_SMALL, color=col,
                ha="center", va="top")
        arrow(ax, 50, yb, x + 10, yb - 7.0, color=col, lw=1.6, ms=9)

    ax.text(50, 3.0, "A methodology is the discipline of asking all four, every "
                     "time.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "lab_flow")


def lab_map():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "The practical component - 26 hours, fourteen parts",
          FS_TITLE)

    parts = [("A", "What RTL means", 1, TEAL),
             ("B", "The abstraction ladder", 2, TEAL),
             ("C", "Proof, not just testing", 2, NAVY),
             ("D", "The synthesisable subset", 2, NAVY),
             ("E", "Simulation against silicon", 1, VIOLET),
             ("F", "The coding rules", 2, VIOLET),
             ("G", "Coding style", 1, VIOLET),
             ("H", "The two pitfalls", 2, RED),
             ("I", "State machines", 3, AMBER),
             ("J", "A controller with a timer", 2, AMBER),
             ("K", "Datapath and controller", 2, AMBER),
             ("L", "From module to IP", 2, GREEN),
             ("M", "Two languages", 2, GREEN),
             ("N", "The flow, and the vendor tools", 2, GREEN)]
    rh = 4.6
    for k, (n, hd, hrs, col) in enumerate(parts):
        cx = 3 if k < 7 else 51
        y = H - 10.0 - (k % 7) * (rh + 1.0)
        box(ax, cx, y - rh, 46, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((cx + 3.6, y - rh / 2), 1.9, fc=col, ec=col,
                            zorder=5))
        ax.text(cx + 3.6, y - rh / 2, n, ha="center", va="center",
                fontsize=FS_SMALL, color=WHITE, fontweight="bold", zorder=6)
        ax.text(cx + 8, y - rh / 2, hd, ha="left", va="center",
                fontsize=FS_SMALL, color=col, fontweight="bold")
        ax.text(cx + 44, y - rh / 2, "%d h" % hrs, ha="right", va="center",
                fontsize=FS_SMALL, color=NAVY, fontweight="bold")

    ax.text(50, 5.0, "103 graded exercises, every one with a worked solution",
            fontsize=FS_HEAD, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 1.5, "Every number in this deck came from a target in that lab.",
            fontsize=FS_SMALL, color=GREEN, ha="center", fontstyle="italic")
    save(f, "lab_map")


def assessment():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "How the 103 exercises are weighted", FS_TITLE)

    left = [["A · what RTL means", "6", "5%"],
            ["B · the ladder", "9", "8%"],
            ["C · proof", "7", "7%"],
            ["D · the subset", "10", "9%"],
            ["E · sim vs silicon", "5", "5%"],
            ["F · coding rules", "10", "9%"],
            ["G · coding style", "5", "5%"]]
    right = [["H · the two pitfalls", "7", "7%"],
             ["I · state machines", "12", "13%"],
             ["J · controller + timer", "6", "6%"],
             ["K · datapath/controller", "7", "8%"],
             ["L · module to IP", "6", "6%"],
             ["M · two languages", "5", "5%"],
             ["N · the flow", "8", "7%"]]
    table(ax, 3, H - 10.0, ["part", "exercises", "weight"], left,
          [24, 13, 11], 4.7, size=FS_TABLE, bold_col=[0])
    table(ax, 51, H - 10.0, ["part", "exercises", "weight"], right,
          [24, 13, 11], 4.7, size=FS_TABLE, bold_col=[0])

    ax.text(50, 5.5, "Predict, then measure.", fontsize=FS_HEAD, color=RED,
            ha="center", fontweight="bold")
    ax.text(50, 1.8, "An exercise where you ran the command and copied the "
                     "answer earns very little; one where you predicted first "
                     "earns it all.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "assessment")


def vivado_flow():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The same flow in Vivado and ModelSim", FS_TITLE)

    steps = [("1", "vlog counter.v ; vsim -c tb_counter",
              "ModelSim - the same job as iverilog + vvp", VIOLET),
             ("2", "read_verilog rtl/counter.v", "Vivado: read the design", TEAL),
             ("3", "synth_design -top counter -part xc7a35t",
              "synthesise for a real device", NAVY),
             ("4", "report_utilization",
              "LUTs and flip-flops - the same question as 'cells'", GREEN),
             ("5", "write_verilog -mode funcsim net.v",
              "the netlist, for gate-level simulation", AMBER)]
    y = H - 9.0
    rh = 5.8
    for n, cmd, sub, col in steps:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((8.0, y - rh / 2), 2.2, fc=col, ec=col, zorder=5))
        ax.text(8.0, y - rh / 2, n, ha="center", va="center", fontsize=FS_SMALL,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(13, y - 2.4, cmd, ha="left", fontsize=FS_MONO, color=NAVY,
                family="monospace", fontweight="bold")
        ax.text(13, y - 4.6, sub, ha="left", fontsize=FS_SMALL, color=BODY)
        y -= rh + 1.0

    ax.text(50, 3.0, "Stated plainly: these commands were NOT run here. Every "
                     "number in this deck came from the free toolchain.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    save(f, "vivado_flow")


for fn in (tool_landscape, install_required, install_vendor, lab_flow, lab_map,
           assessment, vivado_flow):
    fn()
