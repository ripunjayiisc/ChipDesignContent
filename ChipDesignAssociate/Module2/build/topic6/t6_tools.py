# -*- coding: utf-8 -*-
"""Topic 6 diagrams — tools, installation and the lab flow."""
import _boot
from dsl import *


# ------------------------------------------------------------ the landscape
def tool_landscape():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Timing tools - what exists, and what you will use", 12.5)

    rows = [["Vivado (Xilinx/AMD)", "FPGA", "free WebPACK edition", "report_timing_summary"],
            ["Quartus Prime (Intel)", "FPGA", "free Lite edition", "TimeQuest / Timing Analyzer"],
            ["PrimeTime (Synopsys)", "ASIC sign-off", "commercial", "the industry reference"],
            ["Tempus (Cadence)", "ASIC sign-off", "commercial", "the other reference"],
            ["OpenSTA", "ASIC / academic", "open source", "reads real .lib and .sdc"],
            ["OpenROAD / OpenLane", "full ASIC flow", "open source", "OpenSTA inside it"],
            ["sta.py (this course)", "teaching", "you write it", "200 lines, no black box"]]
    table(ax, 3, H - 9.0, ["tool", "used for", "licence", "the timing command"],
          rows, [26, 20, 22, 26], 4.8, size=8.0, bold_col=0)

    box(ax, 3, 3.0, 94, 15.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 15.0, "They all do the same arithmetic", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 10.4, "Arrival, required, slack. The differences are the delay models, "
                      "the report formats and the price.\nLearn to read one report and you "
                      "can read all of them.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.0, "The syllabus names Vivado and ModelSim, so both are covered here - "
                     "but every exercise also runs\nwith no licence at all, on the "
                     "open-source flow.",
            fontsize=8.5, color=TEAL, ha="center", fontstyle="italic")
    save(f, "tool_landscape")


# --------------------------------------------------------------- install map
def _tier(ax, y, hd, sub, lines, col, bh):
    box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.7)
    box(ax, 3, y - 5.5, 94, 5.5, fc=col, ec=col)
    ax.text(6, y - 2.75, hd, ha="left", va="center", fontsize=9.2, color=WHITE,
            fontweight="bold")
    ax.text(94, y - 2.75, sub, ha="right", va="center", fontsize=8.2, color=WHITE,
            fontstyle="italic")
    yy = y - 9.0
    for ln, mono in lines:
        ax.text(7, yy, ln, ha="left", va="center", fontsize=8.0,
                color=NAVY if mono else BODY,
                family="monospace" if mono else "sans-serif",
                fontweight="bold" if mono else "normal")
        yy -= 3.9
    return y - bh


def install_required():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Install this, and every exercise in the topic runs", 12.5)
    ax.text(50, H - 7.2, "One apt line. No licence, no account, no download manager.",
            fontsize=9, color=SLATE, ha="center")

    _tier(ax, H - 11.0, "TIER 1 - required", "Debian / Ubuntu / WSL2",
          [("sudo apt update", 1),
           ("sudo apt install yosys iverilog gtkwave python3 python3-matplotlib", 1),
           ("Yosys        synthesis, and the JSON netlist that sta.py reads", 0),
           ("Icarus       simulation, to prove the optimised netlist still works", 0),
           ("GTKWave      waveform viewer, for the hold-violation exercise", 0),
           ("Python 3     runs sta.py - the timing engine you build in part C", 0),
           ("matplotlib   draws the Fmax curves in the closure exercise", 0)],
          GREEN, 35.0)

    box(ax, 3, 3.0, 94, 10.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 9.4, "yosys -V   &&   iverilog -V   &&   python3 -c \"import matplotlib\"",
            fontsize=8.8, color=NAVY, ha="center", family="monospace", fontweight="bold")
    ax.text(50, 5.2, "Three version strings and you are ready. On Windows, install WSL2 "
                     "first and run the same line inside it.",
            fontsize=8.3, color=GREEN, ha="center", fontstyle="italic")
    save(f, "install_required")


def install_optional():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "Two optional tiers - for the last exercises only", 12.5)

    y = _tier(ax, H - 8.0, "TIER 2 - recommended",
              "a real STA tool that reads real Liberty and SDC",
              [("git clone https://github.com/parallaxsw/OpenSTA", 1),
               ("cd OpenSTA && mkdir build && cd build && cmake .. && make -j4", 1),
               ("sudo make install", 1),
               ("OpenSTA      the same command set as PrimeTime, no licence at all", 0)],
              TEAL, 23.0)

    _tier(ax, y - 3.0, "TIER 3 - vendor",
          "what the syllabus names; large, slow, licence-gated",
          [("Vivado ML Edition (WebPACK)        free, about 40 GB, Linux or Windows", 0),
           ("ModelSim / Questa Intel Starter    free, simulation only", 0),
           ("Register for a free account, then run the web installer and select "
            "only your device family.", 0)],
          VIOLET, 20.0)

    ax.text(50, 6.0, "Exercises G1-G5 use these. Everything before them - "
                     "57 of the 62 exercises - runs on tier 1 alone.",
            fontsize=8.8, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 2.5, "Nothing in this course is gated behind a licence you cannot get.",
            fontsize=8.3, color=GREEN, ha="center", fontstyle="italic")
    save(f, "install_optional")


# ------------------------------------------------------------- the lab flow
def lab_flow():
    W, Hin = 11.5, 6.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 57.4
    title(ax, 50, H - 3, "The lab flow - RTL in, slack out", 13)

    yb = H - 20.0
    stages = [("your.v", "RTL", NAVY), ("yosys", "synthesis", TEAL),
              ("design.json", "netlist", VIOLET), ("sta.py", "timing", GREEN),
              ("report", "slack", RED)]
    bw, gap = 15.0, 5.0
    x0 = 50 - (5 * bw + 4 * gap) / 2
    for i, (nm, sub, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        box(ax, x, yb, bw, 11.0, fc=WHITE, ec=col, lw=1.8)
        ax.text(x + bw / 2, yb + 7.0, nm, ha="center", va="center", fontsize=8.8, color=col,
                fontweight="bold", family="monospace")
        ax.text(x + bw / 2, yb + 3.2, sub, ha="center", va="center", fontsize=8.0,
                color=SLATE)
        if i:
            arrow(ax, x - gap, yb + 5.5, x, yb + 5.5, color=SLATE, lw=1.8, ms=8)

    for i, (x_off, lab) in enumerate([(1, "your .lib"), (3, "your .sdc")]):
        x = x0 + x_off * (bw + gap) + bw / 2
        label_box(ax, x - 9, yb - 13.0, 18, 7.0, lab, fc=LIGHT, ec=AMBER, tc=AMBER,
                  size=8.4, lw=1.5)
        arrow(ax, x, yb - 6.0, x, yb, color=AMBER, lw=1.6, ms=8)

    ax.text(50, yb - 17.5, "make sweep     make hold     make mcp     make closure",
            fontsize=9.4, color=NAVY, ha="center", family="monospace", fontweight="bold")

    box(ax, 4, 3.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.4, "Nothing in this chain is a black box", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 9.6, "You write the Liberty file, so you know every delay number. "
                     "You write sta.py, so you know\nexactly how the slack was computed. "
                     "Then you open Vivado and recognise everything in it.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.8, "That is the point of building the tool before using one.", fontsize=8.6,
            color=TEAL, ha="center", fontstyle="italic")
    save(f, "lab_flow")


# ------------------------------------------------------------- vivado flow
def vivado_flow():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "The same four steps in Vivado", 13)

    steps = [("1", "read_verilog rtl/add32.v", "load the design", TEAL),
             ("2", "read_xdc constraints/vivado.xdc", "load the constraints - the "
              "same create_clock you wrote", VIOLET),
             ("3", "synth_design -top add32 -part xc7a35tcpg236-1", "synthesise for "
              "a real device", NAVY),
             ("4", "report_timing_summary -file post_synth_timing.rpt", "the report - "
              "WNS, TNS, and the worst path", GREEN),
             ("5", "opt_design ; place_design ; route_design", "and again after layout, "
              "when skew is real", AMBER)]
    y = H - 9.0
    rh = 8.2
    for n, cmd, sub, col in steps:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((8.5, y - rh / 2), 2.5, fc=col, ec=col, zorder=5))
        ax.text(8.5, y - rh / 2, n, ha="center", va="center", fontsize=9.2, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(13.5, y - 3.0, cmd, ha="left", fontsize=8.4, color=NAVY, family="monospace",
                fontweight="bold")
        ax.text(13.5, y - 6.2, sub, ha="left", fontsize=8.0, color=BODY)
        y -= rh + 1.3

    box(ax, 3, 3.0, 94, 12.5, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 12.0, "Run it headless:   vivado -mode batch -source vivado_timing.tcl",
            fontsize=8.8, color=GREEN, ha="center", family="monospace", fontweight="bold")
    ax.text(50, 7.4, "The script is in the lab. Every line above is the industrial "
                     "equivalent of one line in your\nMakefile - the concepts do not "
                     "change, only the command names.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "vivado_flow")


# -------------------------------------------------------------- sdc vs xdc
def sdc_vs_xdc():
    W, Hin = 11.5, 5.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 50.4
    title(ax, 50, H - 3, "SDC and XDC - the same language, two names", 12.5)

    rows = [["create_clock", "yes", "yes", "identical"],
            ["set_input_delay", "yes", "yes", "identical"],
            ["set_output_delay", "yes", "yes", "identical"],
            ["set_false_path", "yes", "yes", "identical"],
            ["set_multicycle_path", "yes", "yes", "identical"],
            ["set_clock_uncertainty", "yes", "yes", "Vivado also derives its own"],
            ["set_property PACKAGE_PIN", "no", "yes", "XDC extension - pin placement"],
            ["set_load / set_driving_cell", "yes", "partly", "ASIC-oriented"]]
    table(ax, 3, H - 8.5, ["command", "SDC", "XDC", "note"], rows, [32, 12, 12, 38], 3.9,
          size=7.9, bold_col=0)

    ax.text(50, 4.0, "XDC = SDC + Xilinx physical constraints in one file. "
                     "The timing half is standard SDC.",
            fontsize=9, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 1.2, "Write the timing constraints once and they travel between tools "
                     "almost unchanged.",
            fontsize=8.3, color=TEAL, ha="center", fontstyle="italic")
    save(f, "sdc_vs_xdc")


# ------------------------------------------------------------- the exercises
def lab_map():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "The practical component - 25 hours, seven parts", 12.5)
    ax.text(50, H - 7.2, "Syllabus practicals: Timing Analysis and Closure Labs (10 h) "
                         "+ Design Synthesis and Optimisation Labs (15 h)",
            fontsize=8.6, color=SLATE, ha="center")

    parts = [("A", "Build the delay model", "write cda_edu.lib, read it with liberty.py", 2,
              TEAL),
             ("B", "Build the timing graph", "netlist to nodes and arcs; check it by hand", 3,
              TEAL),
             ("C", "Arrival, required, slack", "finish sta.py; verify against arithmetic", 4,
              NAVY),
             ("D", "Constraints", "write SDC; watch the report change", 4, VIOLET),
             ("E", "Setup closure", "Fmax sweep, mapping options, pipelining", 5, GREEN),
             ("F", "Hold and exceptions", "skew, hold fixes, multicycle paths", 4, AMBER),
             ("G", "Vivado / OpenSTA", "the same design in an industrial tool", 3, RED)]
    y = H - 11.0
    rh = 5.6
    for n, hd, sub, hrs, col in parts:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((7.5, y - rh / 2), 2.1, fc=col, ec=col, zorder=5))
        ax.text(7.5, y - rh / 2, n, ha="center", va="center", fontsize=8.6, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(12, y - rh / 2, hd, ha="left", va="center", fontsize=8.8, color=col,
                fontweight="bold")
        ax.text(42, y - rh / 2, sub, ha="left", va="center", fontsize=8.0, color=BODY)
        ax.text(94, y - rh / 2, "%d h" % hrs, ha="right", va="center", fontsize=8.6,
                color=NAVY, fontweight="bold")
        y -= rh + 1.1

    box(ax, 3, 3.0, 94, 13.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.0, "62 graded exercises, every one with a worked solution", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.4, "Parts A-C build the tool. Parts D-F use it on real violations. "
                     "Part G proves the ideas transfer.\nNothing is quoted in this course "
                     "that you cannot reproduce with make.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "lab_map")


for fn in (tool_landscape, install_required, install_optional, lab_flow,
           vivado_flow, sdc_vs_xdc, lab_map):
    fn()
