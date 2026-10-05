# -*- coding: utf-8 -*-
"""Lecture 01 diagrams — course map, outcomes, and the source-slide map."""
import _boot
from dsl import *


def course_map():
    f, ax, H = panel(3.95)
    title(ax, 50, H - 3.5, "Prof. Indranil Sengupta · Dept. of Computer Science and "
          "Engineering · IIT Kharagpur (NPTEL)", size=FS_SUB, color=SLATE,
          weight="normal")

    weeks = [("Week 1", "Introduction\nDesign representation\nVerilog basics", 5),
             ("Week 2", "Language features\nOperators\nModeling examples", 6),
             ("Week 3", "Description styles\nProcedural\nassignment", 4),
             ("Week 4", "Blocking and\nnon-blocking\nUser-defined primitives", 5),
             ("Week 5", "Test benches\nFinite state\nmachines", 4),
             ("Week 6", "Synthesizable\nVerilog · Recommended\npractices", 5),
             ("Week 7", "Memory · Register\nbanks · Pipelining\nSwitch level", 7),
             ("Week 8", "Pipelined\nprocessor — a full\ncase study", 5)]
    x = 2.0
    w = 11.6
    gap = 0.5
    top = H - 8.0
    bh = 17.5
    for i, (wk, txt, n) in enumerate(weeks):
        fc = "#E8F4F7" if i == 0 else WHITE
        ec = TEAL if i == 0 else GRID
        lw = 2.2 if i == 0 else 1.2
        box(ax, x, top - bh, w, bh, fc=fc, ec=ec, lw=lw)
        box(ax, x, top - 4.2, w, 4.2, fc=TEAL if i == 0 else NAVY,
            ec=TEAL if i == 0 else NAVY, lw=1.0)
        ax.text(x + w / 2, top - 2.1, wk, ha="center", va="center",
                fontsize=FS_BODY, color=WHITE, fontweight="bold")
        ax.text(x + w / 2, top - 10.2, txt, ha="center", va="center",
                fontsize=7.0, color=BODY, linespacing=1.8)
        ax.text(x + w / 2, top - bh + 1.9, "%d lectures" % n, ha="center",
                va="center", fontsize=7.4, color=SLATE, fontstyle="italic")
        x += w + gap

    # the marker for Lecture 01
    y0 = top - bh
    arrow(ax, 7.8, y0 - 3.4, 7.8, y0 - 0.5, color=AMBER, lw=2.4, ms=13)
    ax.text(7.8, y0 - 5.6, "YOU ARE HERE", ha="center", va="center",
            fontsize=FS_SMALL - 1.0, color=AMBER, fontweight="bold")
    ax.text(16.5, y0 - 5.6, "Lecture 01 · Introduction — the VLSI design flow, and "
            "why a hardware description language is the thing that makes it possible",
            ha="left", va="center", fontsize=FS_SMALL - 0.5, color=BODY)
    save(f, "course_map")


def terminal_outcomes():
    f, ax, H = panel(4.54)
    title(ax, 50, H - 3.5, "Chip Design Associate · Module 2 · NOS NIE/ELE/N0102 — "
          "Verilog RTL Coding for Synthesis", size=FS_SUB, color=SLATE,
          weight="normal")

    rows = [("TO-1", "Explain the design cycle of a VLSI circuit — from a design "
             "idea down to a fabricated chip or a programmed FPGA.",
             GREEN, "Fully served. This lecture IS the design cycle."),
            ("TO-2", "Describe Verilog syntax, the levels of abstraction in Verilog "
             "programming, and testbench simulation.",
             TEAL, "Levels of abstraction: served. Syntax and testbenches: opened."),
            ("TO-3", "Design and develop IPs using Verilog.",
             SLATE, "Groundwork only — the vocabulary every later lecture uses."),
            ("TO-4", "Emulate, debug and characterise reusable IPs.",
             SLATE, "Groundwork only — introduces simulation and verification.")]
    y = H - 7
    h = 6.6
    for code, txt, col, note in rows:
        box(ax, 2.0, y - h, 96.0, h, fc=WHITE, ec=GRID, lw=1.2)
        box(ax, 2.0, y - h, 8.5, h, fc=col, ec=col, lw=1.0)
        ax.text(6.25, y - h / 2, code, ha="center", va="center",
                fontsize=FS_BODY, color=WHITE, fontweight="bold")
        ax.text(11.8, y - h / 2 + 1.5, txt, ha="left", va="center",
                fontsize=FS_SMALL, color=BODY)
        ax.text(11.8, y - h / 2 - 1.9, note, ha="left", va="center",
                fontsize=FS_SMALL - 0.8, color=col, fontstyle="italic",
                fontweight="bold")
        y -= h + 0.8
    save(f, "terminal_outcomes")


def learning_outcomes():
    f, ax, H = panel(5.44)
    title(ax, 50, H - 3.5, "Each one is assessed by something you produce or run, "
          "not by something you recite.", size=FS_SUB, color=SLATE, weight="normal")

    items = [("1", "Name the five levels of the VLSI design flow in order, and say "
              "what each level's description is made of."),
             ("2", "Explain what a CAD tool actually does: it reads an HDL "
              "description and writes a more detailed HDL description."),
             ("3", "Distinguish a behavioural description from a structural one, "
              "and give an example of each for the same circuit."),
             ("4", "Define a netlist as a directed graph, and read one at the "
              "functional, gate and transistor level."),
             ("5", "State Moore's Law, and explain why it is an economic "
              "observation rather than a law of physics."),
             ("6", "Install and verify a complete open-source Verilog toolchain: "
              "Icarus Verilog, GTKWave, Yosys and Verilator."),
             ("7", "Run a synthesis tool on a small design and read the cell count "
              "it reports at each level of the flow."),
             ("8", "Explain the ASIC / FPGA trade-off in terms of speed, "
              "flexibility and cost.")]
    y = H - 6.6
    h = 4.0
    gap = 0.5
    for i, (n, txt) in enumerate(items):
        col = GREEN if i < 5 else AMBER
        box(ax, 2.0, y - h, 96.0, h, fc=LIGHT if i % 2 == 0 else WHITE,
            ec=GRID, lw=1.0)
        ax.add_patch(Circle((5.6, y - h / 2), 1.7, fc=col, ec=col, zorder=4))
        ax.text(5.6, y - h / 2, n, ha="center", va="center", fontsize=FS_SMALL,
                color=WHITE, fontweight="bold", zorder=5)
        ax.text(9.5, y - h / 2, txt, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        y -= h + gap
    ax.text(50, 2.0, "Outcomes 1–5 are theory.   Outcomes 6–8 are the practical "
            "component, and are assessed at the keyboard.",
            ha="center", va="center", fontsize=FS_SMALL - 0.5, color=SLATE,
            fontstyle="italic")
    save(f, "learning_outcomes")


def source_map():
    f, ax, H = panel(5.04)
    title(ax, 50, H - 3.5, "Every slide of Lecture 01 is kept, in the lecturer's own "
          "order. The right-hand column is what has been added around it.",
          size=FS_SUB, color=SLATE, weight="normal")

    rows = [("00:58", "Main Objectives of the Course",
             "What an HDL is and is not; a concurrency example"),
            ("03:06", "VLSI Design Process",
             "The complexity arithmetic; the area/speed/power triangle"),
            ("07:25", "First planar IC vs. a modern processor",
             "The actual transistor counts, and what they mean"),
            ("08:23", "Moore's Law",
             "Real data to 2022; why it is economics, not physics"),
            ("11:30", "CMOS · FinFET · Quantum?",
             "What a 'nanometre' means; where the node numbers stand now"),
            ("13:19", "VLSI Design Flow",
             "Each step named, with its input and its output"),
            ("14:40", "Need to use CAD tools",
             "The central idea: a CAD tool is an HDL→HDL transformer"),
            ("17:16", "Two Competing HDLs",
             "The same counter written in Verilog and in VHDL"),
            ("18:23", "Simplistic View of Design Flow",
             "One circuit carried down all five levels"),
            ("19:39", "Behavioral design",
             "The four ways of specifying behaviour, each illustrated"),
            ("20:54", "Data path design",
             "RTL components; what 'register transfer' means"),
            ("21:20", "Netlist as a graph (whiteboard)",
             "The graph drawn properly, at three levels of abstraction"),
            ("22:46", "Logic design",
             "What a standard cell library actually contains"),
            ("24:27", "Physical design and Manufacturing",
             "The layers; and the ASIC / FPGA trade-off"),
            ("25:52", "Other Steps in the Design Flow",
             "Simulation, formal verification, DFT — and where each returns")]

    y = H - 6.2
    rh = 2.25
    box(ax, 2.0, y - rh, 96.0, rh, fc=NAVY, ec=NAVY, lw=1.0)
    for cx, lbl, ha in ((7.0, "SLIDE TIME", "center"),
                        (13.0, "ORIGINAL SLIDE TITLE", "left"),
                        (52.0, "WHAT THIS SESSION ADDS", "left")):
        ax.text(cx, y - rh / 2, lbl, ha=ha, va="center", fontsize=FS_SMALL - 1.0,
                color=WHITE, fontweight="bold")
    y -= rh
    for i, (t, orig, add) in enumerate(rows):
        box(ax, 2.0, y - rh, 96.0, rh, fc=WHITE if i % 2 == 0 else LIGHT,
            ec=GRID, lw=0.8)
        ax.text(7.0, y - rh / 2, t, ha="center", va="center",
                fontsize=FS_SMALL - 1.5, color=AMBER, fontweight="bold")
        ax.text(13.0, y - rh / 2, orig, ha="left", va="center",
                fontsize=FS_SMALL - 1.0, color=NAVY, fontweight="bold")
        ax.text(52.0, y - rh / 2, add, ha="left", va="center",
                fontsize=FS_SMALL - 1.0, color=BODY)
        y -= rh
    save(f, "source_map")


if __name__ == "__main__":
    course_map()
    terminal_outcomes()
    learning_outcomes()
    source_map()
