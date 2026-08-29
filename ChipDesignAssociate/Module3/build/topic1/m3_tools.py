# -*- coding: utf-8 -*-
"""Module 3 Topic 1 diagrams — tools, installation, and the lab programme."""
import _boot
from dsl import *


def tool_landscape():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "Which tool answers which question", 13)

    rows = [["tools/hazard.py", "you write it", "which covers have hazards",
             "this lab"],
            ["Icarus Verilog", "free", "does it actually glitch, and when", "this lab"],
            ["GTKWave", "free", "look at the glitch", "this lab"],
            ["Yosys", "free", "what does synthesis build", "this lab"],
            ["sta/sta.py", "you write it", "setup, hold, slack, Fmax", "Module 2 T6"],
            ["Vivado", "free WebPACK", "all of the above, on a real device",
             "syllabus tool"],
            ["ModelSim / Questa", "free starter", "gate-level simulation with SDF",
             "syllabus tool"],
            ["PrimeTime / Tempus", "commercial", "ASIC sign-off timing", "industry"]]
    table(ax, 3, H - 9.0, ["tool", "licence", "the question it answers", "used in"],
          rows, [24, 18, 34, 18], 4.8, size=8.2, bold_col=[0])

    box(ax, 3, 3.0, 94, 14.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.0, "The pairing that matters in this topic", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 9.2, "A static analyser for setup and hold, and a delay-annotated "
                     "simulator for hazards. Neither one\nsubstitutes for the other, "
                     "and a flow with only one of them has a blind spot.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.4, "Everything except the last three rows runs on free software you "
                     "can install in one command.",
            fontsize=8.4, color=GREEN, ha="center", fontstyle="italic")
    save(f, "tool_landscape")


def install_required():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Install this, and the whole lab runs", 13, color=GREEN)
    ax.text(50, H - 7.2, "One apt line. No licence, no account, no download manager.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 11.0
    bh = 35.0
    box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=GREEN, lw=1.7)
    box(ax, 3, y - 5.5, 94, 5.5, fc=GREEN, ec=GREEN)
    ax.text(6, y - 2.75, "REQUIRED", ha="left", va="center", fontsize=9.2,
            color=WHITE, fontweight="bold")
    ax.text(94, y - 2.75, "Debian / Ubuntu / WSL2", ha="right", va="center",
            fontsize=8.2, color=WHITE, fontstyle="italic")
    lines = [("sudo apt update", 1),
             ("sudo apt install yosys iverilog gtkwave python3 python3-matplotlib", 1),
             ("Yosys        synthesis - and what it does to your hazard fix", 0),
             ("Icarus       gate-level simulation WITH DELAYS - this is the one", 0),
             ("             that shows you a glitch; nothing else in the flow can", 0),
             ("GTKWave      to look at the VCD when the counter says something odd", 0),
             ("Python 3     runs tools/hazard.py and sta/sta.py", 0)]
    yy = y - 9.5
    for ln, mono in lines:
        ax.text(7, yy, ln, ha="left", va="center", fontsize=8.0,
                color=NAVY if mono else BODY,
                family="monospace" if mono else "sans-serif",
                fontweight="bold" if mono else "normal")
        yy -= 3.9

    box(ax, 3, 3.0, 94, 10.5, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 10.0, "yosys -V  &&  iverilog -V  &&  python3 tools/hazard.py --selftest",
            fontsize=8.6, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 5.6, "The self-test cross-checks the hazard rule against a timing "
                     "simulation on 400 random functions.\nIf it prints PASSED, "
                     "everything in this topic will run.",
            fontsize=8.3, color=GREEN, ha="center", fontstyle="italic")
    save(f, "install_required")


def install_vendor():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "The vendor tools the syllabus names", 12.5)
    ax.text(50, H - 7.2, "Needed for the last lab only. Everything before it runs "
                         "without them.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["1", "Create a free AMD/Xilinx account",
             "the download will not start without one"],
            ["2", "Download the Unified Installer (web installer, ~200 MB)",
             "not the 40 GB full archive"],
            ["3", "Choose Vivado ML Edition, then Vivado ML Standard",
             "Standard is free; no licence file"],
            ["4", "Deselect every device family except Zynq-7000",
             "cuts 40 GB to about 8 GB"],
            ["5", "Verify with  vivado -version", "then it runs headless"],
            ["6", "The ZynQ7000 board and JTAG cable are optional here",
             "this is a synthesise-and-report flow"]]
    table(ax, 3, H - 10.5, ["", "what to do", "watch out for"],
          rows, [7, 52, 35], 5.0, size=8.2, bold_col=[0])

    box(ax, 3, 3.0, 94, 13.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 13.0, "You do not need the board to do the timing work", fontsize=9.4,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 8.2, "Vivado will target a Zynq-7000 it has never been connected to and "
                     "give you a real timing report\nfor it. The board and the JTAG "
                     "cable matter when you want to run the design, not analyse it.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "install_vendor")


def lab_flow():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "The lab flow: one circuit, two toolchains", 12.5)

    yb = H - 20.0
    label_box(ax, 38, yb, 24, 10.0, "your circuit", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.4, lw=2.0)

    label_box(ax, 6, yb - 20.0, 30, 10.0, "iverilog + delays", fc="#F2F0FA",
              ec=VIOLET, tc=VIOLET, size=9.0, lw=1.8)
    label_box(ax, 64, yb - 20.0, 30, 10.0, "yosys + sta.py", fc=LIGHT, ec=TEAL,
              tc=TEAL, size=9.0, lw=1.8)
    arrow(ax, 44, yb, 26, yb - 10.0, color=VIOLET, lw=1.8)
    arrow(ax, 56, yb, 74, yb - 10.0, color=TEAL, lw=1.8)

    ax.text(21, yb - 24.0, "does it glitch?", fontsize=8.8, color=VIOLET,
            ha="center", fontweight="bold")
    ax.text(79, yb - 24.0, "does it meet timing?", fontsize=8.8, color=TEAL,
            ha="center", fontweight="bold")

    ax.text(50, yb - 30.0, "make analyse   make glitch   make capture   make synth   "
                           "make fmax   make setup   make hold",
            fontsize=8.4, color=NAVY, ha="center", family="monospace",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.6, "Nothing in this chain is a black box", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 9.6, "You write the hazard analyser, you write the Liberty file, you "
                     "wrote the timing engine in Module 2.\nThen you open Vivado and "
                     "recognise everything in it.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.6, "That is the point of building the tools before using one.",
            fontsize=8.5, color=TEAL, ha="center", fontstyle="italic")
    save(f, "lab_flow")


def vivado_zynq():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "The same analysis on a Zynq-7000", 13)

    steps = [("1", "read_verilog rtl/pipe_bal.v", "load the design", TEAL),
             ("2", "read_xdc vivado/zynq.xdc", "the same create_clock you wrote, "
              "plus pin constraints SDC has no concept of", VIOLET),
             ("3", "synth_design -top pipe_bal -part xc7z020clg400-1",
              "synthesise for the real device", NAVY),
             ("4", "report_timing_summary", "WNS, TNS, and the worst path", GREEN),
             ("5", "opt_design ; place_design ; route_design",
              "and report again - setup gets worse, hold appears", AMBER)]
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

    box(ax, 3, 3.0, 94, 14.5, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 14.0, "vivado -mode batch -source vivado/zynq_sta.tcl", fontsize=8.8,
            color=GREEN, ha="center", family="monospace", fontweight="bold")
    ax.text(50, 9.2, "The absolute numbers will not match your engine - a Zynq LUT is "
                     "not cda_edu.lib. What should\nmatch is the shape of the report, "
                     "which path is critical, and the direction of every change\n"
                     "you make to the constraints.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "vivado_zynq")


def lab_map():
    W, Hin = 11.5, 9.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 78.3
    title(ax, 50, H - 3, "The practical component - 12 hours, seven parts", 12.5)
    ax.text(50, H - 7.2, "Module 3 practical: 35 hours across three subtopics. "
                         "This is subtopic 1's share.",
            fontsize=8.8, color=SLATE, ha="center")

    parts = [("A", "Hazards on paper", "K-maps, adjacency, the consensus term", 2,
              TEAL),
             ("B", "Build the analyser", "tools/hazard.py, and its self-test", 2, TEAL),
             ("C", "Gate-level glitches", "the detector; static, then dynamic", 2, NAVY),
             ("D", "Does it matter?", "one signal as data, as clock, as reset", 1,
              VIOLET),
             ("E", "Synthesis", "watch the optimiser delete your fix", 1, AMBER),
             ("F", "Setup, hold, Fmax", "the pipeline, the skew, the period", 2, GREEN),
             ("G", "Vivado on Zynq-7000", "the same design in an industrial tool", 2,
              RED)]
    y = H - 11.0
    rh = 5.8
    for n, hd, sub, hrs, col in parts:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((7.5, y - rh / 2), 2.2, fc=col, ec=col, zorder=5))
        ax.text(7.5, y - rh / 2, n, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(12, y - rh / 2, hd, ha="left", va="center", fontsize=8.8, color=col,
                fontweight="bold")
        ax.text(42, y - rh / 2, sub, ha="left", va="center", fontsize=8.0, color=BODY)
        ax.text(94, y - rh / 2, "%d h" % hrs, ha="right", va="center", fontsize=8.6,
                color=NAVY, fontweight="bold")
        y -= rh + 1.2

    box(ax, 3, 3.0, 94, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.6, "58 graded exercises, every one with a worked solution",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 9.6, "Parts A-C build the understanding and the tool. Parts D-E connect "
                     "it to real design decisions.\nParts F-G are the timing half, and "
                     "part G proves the ideas transfer.",
            fontsize=8.5, color=BODY, ha="center")
    ax.text(50, 4.6, "Nothing is quoted in this topic that you cannot reproduce with "
                     "make.",
            fontsize=8.4, color=GREEN, ha="center", fontstyle="italic")
    save(f, "lab_map")


def assessment():
    W, Hin = 11.5, 7.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 67.8
    title(ax, 50, H - 3, "How the 58 exercises are weighted", 13)

    rows = [["A · hazards on paper", "10", "15%", "correct adjacency reasoning"],
            ["B · the analyser", "8", "15%", "self-test passes, and you can explain it"],
            ["C · gate-level glitches", "12", "20%", "prediction before measurement"],
            ["D · does it matter", "6", "10%", "the right rule, not the slogan"],
            ["E · synthesis", "6", "10%", "what survived, and why"],
            ["F · setup, hold, Fmax", "11", "20%", "hand arithmetic matches the tool"],
            ["G · industrial tools", "5", "10%", "the comparison write-up"]]
    table(ax, 3, H - 9.0, ["part", "exercises", "weight", "assessed on"],
          rows, [30, 16, 14, 34], 4.8, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 13.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 13.0, "The rule that runs through every part", fontsize=9.4, color=RED,
            ha="center", fontweight="bold")
    ax.text(50, 8.2, "A fix you cannot explain is not a fix. Marks go to the reasoning, "
                     "not to a clean report - because\nin this field it is trivially "
                     "easy to produce a clean report on a broken design.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "assessment")


for fn in (tool_landscape, install_required, install_vendor, lab_flow, vivado_zynq,
           lab_map, assessment):
    fn()
