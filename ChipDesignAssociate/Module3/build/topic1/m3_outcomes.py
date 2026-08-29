# -*- coding: utf-8 -*-
"""Module 3 Topic 1 diagrams — terminal outcomes, learning outcomes, and how
the subtopic maps onto the NOS."""
import _boot
from dsl import *


def terminal_outcomes():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Module 3 terminal outcomes", 13)
    ax.text(50, H - 7.4, "NOS NIE/ELE/N0103 · Static Timing Analysis of VLSI Circuits "
                         "· 25 h theory + 35 h practical",
            fontsize=8.8, color=SLATE, ha="center")

    outs = [("1", "Understand static timing analysis",
             "what a timing path is, how arrival, required and slack are computed,\n"
             "and how to read any timing report", TEAL),
            ("2", "Understand ECO fixes and timing closure",
             "how to diagnose a violation, choose a fix, and drive a design to a\n"
             "state where every check passes at every corner", VIOLET)]
    y = H - 12.0
    bh = 14.0
    for n, hd, sub, col in outs:
        box(ax, 4, y - bh, 92, bh, fc=WHITE, ec=col, lw=1.8)
        ax.add_patch(Circle((11, y - bh / 2), 3.6, fc=col, ec=col, zorder=5))
        ax.text(11, y - bh / 2, n, ha="center", va="center", fontsize=11,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(18, y - 4.6, hd, ha="left", fontsize=10.2, color=col,
                fontweight="bold")
        ax.text(18, y - 9.6, sub, ha="left", va="center", fontsize=8.4, color=BODY)
        y -= bh + 2.5

    box(ax, 4, 3.0, 92, 18.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 17.6, "Where this subtopic sits", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 12.4, "Subtopic 1 · Overview of VLSI STA        builds outcome 1, "
                      "and the vocabulary outcome 2 needs\n"
                      "Subtopic 2 · Timing performance          pipelining, retiming, "
                      "skew, block and chip level\n"
                      "Subtopic 3 · STA using EDA tools         post-synthesis and "
                      "post-route, ECO flow, sign-off",
            fontsize=8.4, color=BODY, ha="center", family="monospace")
    ax.text(50, 5.0, "This deck is subtopic 1. It ends where the ECO flow begins.",
            fontsize=8.6, color=TEAL, ha="center", fontstyle="italic")
    save(f, "terminal_outcomes")


def learning_outcomes():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Key learning outcomes for this subtopic", 13)

    y = H - 9.0
    box(ax, 3, y - 26.0, 45.5, 26.0, fc=LIGHT, ec=TEAL, lw=1.8)
    box(ax, 3, y - 5.5, 45.5, 5.5, fc=TEAL, ec=TEAL)
    ax.text(25.75, y - 2.75, "THEORY", ha="center", va="center", fontsize=9.6,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "Describe the key components of STA:\ntiming paths, constraints, reports",
            "Analyse timing issues in combinational\ncircuits, including races and "
            "hazards",
            "Discuss how timing constraints influence\nsynthesis and optimisation",
            "Evaluate maximum frequency of operation"]):
        ax.text(6, y - 9.5 - i * 4.6, "▪", fontsize=8.4, color=TEAL, ha="left")
        ax.text(9, y - 9.5 - i * 4.6, ln, fontsize=7.9, color=BODY, ha="left",
                va="top")

    box(ax, 51.5, y - 26.0, 45.5, 26.0, fc="#EEF7F1", ec=GREEN, lw=1.8)
    box(ax, 51.5, y - 5.5, 45.5, 5.5, fc=GREEN, ec=GREEN)
    ax.text(74.25, y - 2.75, "PRACTICAL", ha="center", va="center", fontsize=9.6,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "Conduct STA using industry-standard tools\nto analyse timing paths",
            "Identify and resolve setup and hold\nviolations through exercises",
            "Implement timing constraints in EDA tools\nand analyse their impact "
            "during synthesis",
            "Evaluate the effect of clock skew"]):
        ax.text(54.5, y - 9.5 - i * 4.6, "▪", fontsize=8.4, color=GREEN, ha="left")
        ax.text(57.5, y - 9.5 - i * 4.6, ln, fontsize=7.9, color=BODY, ha="left",
                va="top")

    y -= 29.0
    box(ax, 3, y - 20.0, 94, 20.0, fc=WHITE, ec=NAVY, lw=1.6)
    ax.text(50, y - 4.4, "Every one of them is assessed by something you run",
            fontsize=9.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, y - 12.5, "races and hazards      ->  make analyse, make glitch, "
                          "make capture\n"
                          "constraints and synthesis ->  make synth, make setup\n"
                          "setup and hold          ->  make hold, and the Fmax sweep\n"
                          "industry-standard tools ->  vivado/zynq_sta.tcl on a "
                          "Zynq-7000",
            fontsize=8.2, color=BODY, ha="center", family="monospace")
    save(f, "learning_outcomes")


def syllabus_map():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 73.0
    title(ax, 50, H - 3, "Every syllabus phrase, and where it is covered", 12.5)

    rows = [["Introduction to timing analysis", "Theory 1", "5-12"],
            ["Combinational circuit timing - races and hazards", "Theory 2", "13-32"],
            ["Sequential circuit timing - setup and hold timing", "Theory 3", "33-44"],
            ["Maximum frequency of operation", "Theory 3", "45-50"],
            ["Practical examples of setup and hold violations\nand their solution",
             "Theory 3 + Labs F", "51-58"],
            ["Timing constraints for synthesis", "Theory 4", "59-66"],
            ["Circuit synthesis and timing analysis", "Theory 4", "67-72"]]
    table(ax, 4, H - 9.0, ["syllabus phrase", "section", "slides"],
          rows, [56, 22, 14], 5.4, size=8.4, bold_col=[1])

    box(ax, 4, 3.0, 92, 14.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 14.0, "On the overlap with Module 2 Topic 6", fontsize=9.4,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 9.2, "Setup, hold and constraints were taught there from the RTL "
                     "designer's point of view. Here they are\nrevisited at gate level "
                     "and treated as the second half of a bigger question. The genuinely "
                     "new\nmaterial in this subtopic is races and hazards - and it is "
                     "given the most room.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "syllabus_map")


def topic_structure():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "How this session runs", 13)

    parts = [("THEORY 1", "What timing analysis is", "why a truth table is not enough",
              TEAL),
             ("THEORY 2", "Races and hazards", "the new material - most of the session",
              RED),
             ("THEORY 3", "Setup, hold, Fmax", "the sequential half, at gate level",
              NAVY),
             ("THEORY 4", "Constraints and synthesis", "what the tool does with it all",
              VIOLET),
             ("PRACTICAL", "Labs A-G", "12 hours, 58 exercises, all measured", GREEN)]
    y = H - 9.0
    rh = 7.4
    for nm, hd, sub, col in parts:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.4)
        box(ax, 4, y - rh, 20, rh, fc=col, ec=col)
        ax.text(14, y - rh / 2, nm, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold")
        ax.text(27, y - rh / 2 + 1.4, hd, ha="left", va="center", fontsize=9.2,
                color=col, fontweight="bold")
        ax.text(27, y - rh / 2 - 2.0, sub, ha="left", va="center", fontsize=8.0,
                color=BODY)
        y -= rh + 1.4

    box(ax, 4, 3.0, 92, 11.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 10.6, "One sentence to open with", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 5.8, "A circuit can compute exactly the right answer and still be "
                     "wrong, because it passed through a\nwrong answer on the way - "
                     "and no truth table and no static analysis will tell you.",
            fontsize=8.7, color=RED, ha="center", fontweight="bold")
    save(f, "topic_structure")


def what_you_can_do():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "By the end of this subtopic you can", 13, color=GREEN)

    items = ["Look at a two-level cover and say whether it has a static hazard, "
             "and which transition.",
             "Prescribe the redundant term that removes it, and prove the function "
             "did not change.",
             "Build a testbench that detects glitches by counting, not by looking.",
             "Say where a glitch is harmless and where it is fatal - and defend the "
             "distinction.",
             "Explain why static timing analysis cannot see any of this.",
             "Compute maximum frequency of operation from the four terms of a path.",
             "Diagnose a setup violation, size it against the period, and pick the "
             "right fix.",
             "Recognise a hold violation and explain why the clock frequency is "
             "irrelevant to it.",
             "Write a constraint set that makes synthesis optimise for what you "
             "actually want."]
    y = H - 9.5
    for it in items:
        ax.text(6, y, "✓", fontsize=9.6, color=GREEN, ha="left", fontweight="bold")
        ax.text(10, y, it, fontsize=9.0, color=BODY, ha="left", va="center")
        y -= 4.4

    box(ax, 4, 3.0, 92, 9.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 8.6, "And one thing to carry into every design you ever do", fontsize=9.2,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 4.4, "\"It simulates correctly\" and \"it meets timing\" are two "
                     "different claims, and neither implies the other.",
            fontsize=8.7, color=BODY, ha="center")
    save(f, "what_you_can_do")


for fn in (terminal_outcomes, learning_outcomes, syllabus_map, topic_structure,
           what_you_can_do):
    fn()
