# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — tools, installation and the lab programme."""
import _boot
from dsl import *


def tool_landscape():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 81.7
    title(ax, 50, H - 3, "The tools, and what each one is for", 13)

    rows = [["Icarus Verilog", "free", "simulate Verilog", "this lab"],
            ["GHDL", "free", "simulate VHDL", "this lab"],
            ["GTKWave", "free", "look at the waveforms", "this lab"],
            ["Yosys", "free", "synthesise, and prove equivalence", "this lab"],
            ["Verilator", "free", "fast simulation, and a good linter", "recommended"],
            ["rtl_lint.py", "you write it", "the seven coding rules", "this lab"],
            ["Vivado", "free WebPACK", "synthesis and implementation, Xilinx",
             "syllabus tool"],
            ["ModelSim / Questa", "free starter", "simulation, both languages",
             "syllabus tool"],
            ["Design Compiler", "commercial", "ASIC synthesis", "industry"]]
    table(ax, 3, H - 9.0, ["tool", "licence", "what it does", "used in"],
          rows, [24, 18, 36, 16], 4.8, size=8.2, bold_col=[0])

    box(ax, 3, 3.0, 94, 16.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 15.6, "Everything in this topic runs on the free rows", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 10.6, "Yosys is the interesting one: it is the only free tool here "
                      "that will both synthesise your RTL\nand PROVE that the netlist "
                      "it produced is equivalent to what you wrote.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.0, "Vivado and ModelSim are named by the syllabus and are covered "
                     "in the deck; they were not\nused to produce any number in these "
                     "materials.",
            fontsize=8.4, color=SLATE, ha="center", fontstyle="italic")
    save(f, "tool_landscape")


def install_required():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Install this, and the whole lab runs", 13, color=GREEN)
    ax.text(50, H - 7.2, "Two apt lines. No licence, no account, no download manager.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 11.5
    bh = 34.0
    box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=GREEN, lw=1.7)
    box(ax, 3, y - 5.5, 94, 5.5, fc=GREEN, ec=GREEN)
    ax.text(6, y - 2.75, "REQUIRED", ha="left", va="center", fontsize=9.2,
            color=WHITE, fontweight="bold")
    ax.text(94, y - 2.75, "Debian / Ubuntu / WSL2", ha="right", va="center",
            fontsize=8.2, color=WHITE, fontstyle="italic")
    lines = [("sudo apt update", 1),
             ("sudo apt install yosys iverilog gtkwave python3", 1),
             ("sudo apt install ghdl          # only for the VHDL comparison", 1),
             ("Icarus    simulates Verilog - and the transistor level too", 0),
             ("GHDL      simulates VHDL, so 'Verilog or VHDL' can be shown", 0),
             ("Yosys     synthesises, and proves equivalence with a SAT solver", 0),
             ("GTKWave   for when the transcript is not enough", 0)]
    yy = y - 9.5
    for ln, mono in lines:
        ax.text(7, yy, ln, ha="left", va="center", fontsize=8.0,
                color=NAVY if mono else BODY,
                family="monospace" if mono else "sans-serif",
                fontweight="bold" if mono else "normal")
        yy -= 3.7

    box(ax, 3, 3.0, 94, 11.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 10.4, "yosys -V  &&  iverilog -V  &&  ghdl --version",
            fontsize=8.8, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 5.8, "Three version strings and every target in the lab Makefile "
                     "will run.\nWithout ghdl, everything except  make langs  still "
                     "works.",
            fontsize=8.3, color=GREEN, ha="center", fontstyle="italic")
    save(f, "install_required")


def install_vendor():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "The vendor tools the syllabus names", 12.5)

    rows = [["1", "Create a free AMD/Xilinx account",
             "the download will not start without one"],
            ["2", "Download the Unified Installer (~200 MB web installer)",
             "not the 40 GB full archive"],
            ["3", "Choose Vivado ML Edition, then ML Standard",
             "Standard is free; no licence file needed"],
            ["4", "Deselect every device family but the one you use",
             "cuts 40 GB to about 8 GB"],
            ["5", "ModelSim: Intel FPGA Starter Edition is free",
             "simulates both Verilog and VHDL"],
            ["6", "Verify:  vivado -version   and   vsim -version",
             "both then run headless"]]
    table(ax, 3, H - 9.0, ["", "what to do", "watch out for"],
          rows, [7, 52, 35], 5.2, size=8.2, bold_col=[0])

    box(ax, 3, 3.0, 94, 17.0, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 16.6, "What these add, and what they do not", fontsize=9.4,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 11.6, "They add a real device library, real timing numbers, and a "
                      "flow you will meet at work. They do not\nadd anything to the "
                      "CONCEPTS in this topic - RTL is RTL, and the free toolchain "
                      "shows all of it.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.4, "Learn the ideas on the free tools, where the whole flow takes "
                     "seconds. Then run the same design\nthrough Vivado and recognise "
                     "every stage.",
            fontsize=8.5, color=NAVY, ha="center")
    save(f, "install_vendor")


def lab_flow():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "What the lab does with your RTL", 13)

    yb = H - 18.0
    label_box(ax, 38, yb, 24, 10.0, "your RTL", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.4, lw=2.0)

    outs = [(6, "rtl_lint.py", "the rules", TEAL),
            (28, "iverilog", "does it work?", VIOLET),
            (50, "yosys", "what gets built", GREEN),
            (72, "yosys sat", "is it still the same?", AMBER)]
    for x, tool, q, col in outs:
        label_box(ax, x, yb - 20.0, 22, 9.0, tool, fc=LIGHT, ec=col, tc=col,
                  size=8.8, lw=1.6)
        ax.text(x + 11, yb - 23.6, q, fontsize=8.0, color=col, ha="center")
        arrow(ax, 50, yb, x + 11, yb - 11.0, color=col, lw=1.4, ms=7)

    ax.text(50, yb - 29.0, "make lint   make ladder   make subset   make prove   "
                           "make flow",
            fontsize=8.6, color=NAVY, ha="center", family="monospace",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.6, "Four different questions about one piece of code", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 9.6, "Does it follow the rules? Does it do what the spec says? What "
                     "will actually be built from it?\nAnd is that thing still the "
                     "design you wrote?",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.6, "A methodology is exactly the discipline of asking all four, "
                     "every time.",
            fontsize=8.5, color=TEAL, ha="center", fontstyle="italic")
    save(f, "lab_flow")


def lab_map():
    W, Hin = 11.5, 10.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 88.7
    title(ax, 50, H - 3, "The practical component - 14 hours, nine parts", 12.5)
    ax.text(50, H - 7.2, "Module 2 practical: RTL Design and Implementation Labs "
                         "(40 h). This is Topic 2's share.",
            fontsize=8.8, color=SLATE, ha="center")

    parts = [("A", "What RTL means", "registers, transfers, and the clock edge", 1,
              TEAL),
             ("B", "The abstraction ladder", "one adder, four levels, all simulated",
              2, TEAL),
             ("C", "Proof, not just testing", "equivalence checking, and a bug it "
              "catches", 2, NAVY),
             ("D", "The synthesisable subset", "eleven constructs, measured", 2,
              VIOLET),
             ("E", "Simulation vs silicon", "the sensitivity-list mismatch", 1,
              VIOLET),
             ("F", "The coding rules", "build the linter, then check the linter", 2,
              AMBER),
             ("G", "Two languages", "the same counter in Verilog and VHDL", 1, AMBER),
             ("H", "The flow, end to end", "spec to formal proof, seven stages", 2,
              GREEN),
             ("I", "Vendor tools", "the same design in Vivado", 1, RED)]
    y = H - 11.0
    rh = 5.6
    for n, hd, sub, hrs, col in parts:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((7.5, y - rh / 2), 2.2, fc=col, ec=col, zorder=5))
        ax.text(7.5, y - rh / 2, n, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(12, y - rh / 2, hd, ha="left", va="center", fontsize=8.8, color=col,
                fontweight="bold")
        ax.text(42, y - rh / 2, sub, ha="left", va="center", fontsize=8.0,
                color=BODY)
        ax.text(94, y - rh / 2, "%d h" % hrs, ha="right", va="center", fontsize=8.6,
                color=NAVY, fontweight="bold")
        y -= rh + 1.2

    box(ax, 3, 3.0, 94, 14.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.6, "60 graded exercises, every one with a worked solution",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.6, "Parts A-C build the mental model. D-F are the methodology, made "
                     "mechanical. G-I connect it\nto other languages and to the tools "
                     "you will meet at work.",
            fontsize=8.5, color=BODY, ha="center")
    ax.text(50, 4.4, "Every number in this deck came from a target in that lab.",
            fontsize=8.4, color=GREEN, ha="center", fontstyle="italic")
    save(f, "lab_map")


def assessment():
    W, Hin = 11.5, 7.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 67.8
    title(ax, 50, H - 3, "How the 60 exercises are weighted", 13)

    rows = [["A · what RTL means", "6", "10%", "can you read a transfer as hardware"],
            ["B · the ladder", "9", "15%", "same circuit, four notations"],
            ["C · proof", "7", "12%", "why exhaustive testing stops working"],
            ["D · the subset", "10", "18%", "prediction before measurement"],
            ["E · sim vs silicon", "5", "10%", "explaining the mismatch precisely"],
            ["F · coding rules", "10", "17%", "the rule, and the reason for it"],
            ["G · two languages", "5", "8%", "reading VHDL without panic"],
            ["H · the flow", "8", "10%", "evidence at every stage"]]
    table(ax, 3, H - 9.0, ["part", "exercises", "weight", "assessed on"],
          rows, [28, 16, 14, 36], 4.8, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 15.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 14.6, "The rule that runs through every part", fontsize=9.4,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 9.6, "Predict, then measure. An exercise where you ran the command and "
                     "wrote down the answer earns\nvery little; one where you wrote "
                     "the prediction first and then explained the difference earns "
                     "it all.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.4, "Being wrong and knowing why is the whole point of a lab.",
            fontsize=8.5, color=NAVY, ha="center", fontstyle="italic")
    save(f, "assessment")


def vivado_flow():
    W, Hin = 11.5, 8.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 76.5
    title(ax, 50, H - 3, "The same flow in Vivado and ModelSim", 12.5)

    steps = [("1", "vlog counter.v ; vsim -c tb_counter", "ModelSim: compile and "
              "simulate - the same job as iverilog + vvp", VIOLET),
             ("2", "read_verilog rtl/counter.v", "Vivado: read the design", TEAL),
             ("3", "synth_design -top counter -part xc7a35t", "synthesise for a real "
              "device", NAVY),
             ("4", "report_utilization", "how many LUTs and flip-flops - the same "
              "question as 'cells'", GREEN),
             ("5", "write_verilog -mode funcsim net.v",
              "the netlist, for gate-level simulation", AMBER)]
    y = H - 9.0
    rh = 8.4
    for n, cmd, sub, col in steps:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((8.5, y - rh / 2), 2.5, fc=col, ec=col, zorder=5))
        ax.text(8.5, y - rh / 2, n, ha="center", va="center", fontsize=9.2,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(13.5, y - 3.0, cmd, ha="left", fontsize=8.2, color=NAVY,
                family="monospace", fontweight="bold")
        ax.text(13.5, y - 6.3, sub, ha="left", fontsize=7.9, color=BODY)
        y -= rh + 1.3

    box(ax, 3, 3.0, 94, 15.0, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 14.6, "Stated plainly: these commands were not run here", fontsize=9.4,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 9.6, "Vivado and ModelSim are not installed in the environment these "
                     "materials were built in. Every\nnumber quoted in this deck came "
                     "from the free toolchain, and is reproducible with make.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.4, "The commands above are from the vendor documentation. Run them "
                     "and record what you get.",
            fontsize=8.5, color=NAVY, ha="center", fontstyle="italic")
    save(f, "vivado_flow")


for fn in (tool_landscape, install_required, install_vendor, lab_flow, lab_map,
           assessment, vivado_flow):
    fn()
