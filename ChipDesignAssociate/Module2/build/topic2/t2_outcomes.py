# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — terminal outcomes, learning outcomes, syllabus."""
import _boot
from dsl import *


def terminal_outcomes():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 81.7
    title(ax, 50, H - 3, "Module 2 terminal outcomes", 13)
    ax.text(50, H - 7.4, "NOS NIE/ELE/N0102 · Verilog RTL coding for Synthesis · "
                         "25 h theory + 35 h practical",
            fontsize=8.8, color=SLATE, ha="center")

    outs = [("1", "Understand the design cycle of VLSI",
             "where RTL sits in the flow, and what happens either side of it",
             TEAL, "Topic 1 and 2"),
            ("2", "Understand Verilog syntax, LEVELS OF ABSTRACTION, and testbench "
             "simulation",
             "the abstraction ladder is this subtopic's central idea", VIOLET,
             "Topic 2, 4, 5"),
            ("3", "Design and develop IPs for VLSI using Verilog",
             "which begins with knowing what is synthesisable and what is not",
             NAVY, "Topic 2, 4"),
            ("4", "Emulate, debug and characterise reusable IPs",
             "reuse is a property you design in, not one you add later", GREEN,
             "Topic 2, 5, 6")]
    y = H - 12.0
    bh = 11.5
    for n, hd, sub, col, where in outs:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.7)
        ax.add_patch(Circle((9.5, y - bh / 2), 3.2, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - bh / 2, n, ha="center", va="center", fontsize=10.5,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(16, y - 4.2, hd, ha="left", fontsize=9.2, color=col,
                fontweight="bold")
        ax.text(16, y - 8.0, sub, ha="left", fontsize=8.2, color=BODY)
        ax.text(94, y - bh / 2, where, ha="right", va="center", fontsize=7.8,
                color=SLATE, fontstyle="italic")
        y -= bh + 2.0

    box(ax, 3, 3.0, 94, 14.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 13.6, "Outcome 2 names this subtopic explicitly", fontsize=9.4,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 8.6, "\"Level of abstraction in Verilog programming\" is the phrase in "
                     "the NOS. This session takes one\ncircuit down all four levels, "
                     "simulates them together, and proves they are the same.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.4, "That is the deliverable this subtopic exists to produce.",
            fontsize=8.4, color=NAVY, ha="center", fontstyle="italic")
    save(f, "terminal_outcomes")


def learning_outcomes():
    W, Hin = 11.5, 7.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 67.8
    title(ax, 50, H - 3, "Key learning outcomes for this subtopic", 13)

    y = H - 9.0
    box(ax, 3, y - 26.0, 45.5, 26.0, fc=LIGHT, ec=TEAL, lw=1.8)
    box(ax, 3, y - 5.5, 45.5, 5.5, fc=TEAL, ec=TEAL)
    ax.text(25.75, y - 2.75, "THEORY", ha="center", va="center", fontsize=9.6,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "Explain what register transfer level\nmeans, and the timing model it "
            "implies",
            "Describe the levels of abstraction in an\nHDL and choose between them",
            "Explain how timing constraints and the\nsynthesisable subset shape "
            "the RTL you\nwrite",
            "Compare Verilog and VHDL"]):
        ax.text(6, y - 9.5 - i * 4.8, "▪", fontsize=8.4, color=TEAL, ha="left")
        ax.text(9, y - 9.5 - i * 4.8, ln, fontsize=7.8, color=BODY, ha="left",
                va="top")

    box(ax, 51.5, y - 26.0, 45.5, 26.0, fc="#EEF7F1", ec=GREEN, lw=1.8)
    box(ax, 51.5, y - 5.5, 45.5, 5.5, fc=GREEN, ec=GREEN)
    ax.text(74.25, y - 2.75, "PRACTICAL", ha="center", va="center", fontsize=9.6,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "Write RTL code for basic digital circuits",
            "Validate RTL designs through simulation\nusing testbenches",
            "Apply a coding standard and check it\nmechanically",
            "Synthesise a design and read what the\ntool built"]):
        ax.text(54.5, y - 9.5 - i * 4.8, "▪", fontsize=8.4, color=GREEN, ha="left")
        ax.text(57.5, y - 9.5 - i * 4.8, ln, fontsize=7.8, color=BODY, ha="left",
                va="top")

    y -= 29.0
    box(ax, 3, y - 22.0, 94, 22.0, fc=WHITE, ec=NAVY, lw=1.6)
    ax.text(50, y - 4.4, "Every one of them is assessed by something you run",
            fontsize=9.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, y - 13.0, "what RTL means        ->  make transfer, make ladder\n"
                          "levels of abstraction ->  make ladder, make prove\n"
                          "the coding standard   ->  make lint, make lintcheck\n"
                          "synthesis             ->  make subset, make flow\n"
                          "Verilog or VHDL       ->  make langs",
            fontsize=8.2, color=BODY, ha="center", family="monospace")
    save(f, "learning_outcomes")


def syllabus_map():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "Every syllabus phrase, and where it is covered", 12.5)

    rows = [["Basics of register transfer level (RTL) design", "Theory 1", "5-16"],
            ["Overview of RTL design process and methodology", "Theory 2", "17-38"],
            ["Introduction to hardware description languages\n(HDLs) such as "
             "Verilog or VHDL", "Theory 3", "39-54"],
            ["Practical: RTL Design and Implementation Labs", "Labs A-I", "55-70"]]
    table(ax, 4, H - 9.0, ["syllabus phrase", "section", "slides"],
          rows, [56, 20, 16], 7.0, size=8.6, bold_col=[1])

    box(ax, 4, 3.0, 92, 21.0, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 20.6, "The syllabus gives this subtopic 4 notional hours",
            fontsize=9.6, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 15.4, "Four hours is enough to define the terms. It is not enough to "
                      "make anyone believe them, and\nnothing in this subtopic is "
                      "believed until it has been seen to happen.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 9.4, "So the theory is developed to the depth the ideas need, and "
                     "every claim is attached to a lab target\nthat produces it. "
                     "Deliver it in four hours by lecturing from the summary slides; "
                     "deliver it properly\nby running the lab alongside.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "syllabus_map")


def topic_structure():
    W, Hin = 11.5, 8.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 76.5
    title(ax, 50, H - 3, "How this session runs", 13)

    parts = [("THEORY 1", "What RTL is", "registers, transfers, and four levels of "
              "abstraction", TEAL),
             ("THEORY 2", "The methodology", "the flow, the subset, the rules, and "
              "why each exists", VIOLET),
             ("THEORY 3", "HDLs", "what an HDL is, and Verilog against VHDL", NAVY),
             ("PRACTICAL", "Labs A-I", "14 hours, 60 exercises, all measured", GREEN)]
    y = H - 9.5
    rh = 8.6
    for nm, hd, sub, col in parts:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.4)
        box(ax, 4, y - rh, 22, rh, fc=col, ec=col)
        ax.text(15, y - rh / 2, nm, ha="center", va="center", fontsize=9.0,
                color=WHITE, fontweight="bold")
        ax.text(29, y - rh / 2 + 1.6, hd, ha="left", va="center", fontsize=9.4,
                color=col, fontweight="bold")
        ax.text(29, y - rh / 2 - 2.2, sub, ha="left", va="center", fontsize=8.2,
                color=BODY)
        y -= rh + 1.6

    box(ax, 4, 3.0, 92, 19.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 18.6, "One sentence to open with", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 13.0, "RTL is not a language and it is not a tool. It is a way of "
                      "thinking about hardware in which you\nsay which registers "
                      "exist and what transfers into them - and leave everything "
                      "else to the tool.",
            fontsize=8.8, color=BODY, ha="center")
    ax.text(50, 6.0, "Everything else in this session is a consequence of that "
                     "sentence: what you may write, what you\nmay not, why the rules "
                     "exist, and what the tool does with it.",
            fontsize=8.6, color=TEAL, ha="center")
    save(f, "topic_structure")


def what_you_can_do():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "By the end of this subtopic you can", 13, color=GREEN)

    items = ["Read an always block and say which registers it creates, and which "
             "logic sits between them.",
             "Write the same function at four levels of abstraction, and say what "
             "each level costs you.",
             "Choose the right level - and defend the choice with a cell count.",
             "Prove two descriptions are the same circuit, instead of hoping.",
             "Say which Verilog constructs synthesise, which do not, and which are "
             "traps.",
             "Recognise an inferred latch before the tool builds one.",
             "Explain why an incomplete sensitivity list is worse than an error.",
             "Apply the seven coding rules, and say why each one exists.",
             "Read a VHDL design without needing it translated.",
             "Take a design from spec to formal proof and show your evidence at "
             "each stage."]
    y = H - 10.0
    for it in items:
        ax.text(6, y, "✓", fontsize=9.4, color=GREEN, ha="left", fontweight="bold")
        ax.text(10, y, it, fontsize=8.8, color=BODY, ha="left", va="center")
        y -= 4.4

    box(ax, 4, 3.0, 92, 12.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 11.6, "And one habit to carry into every design you ever write",
            fontsize=9.4, color=RED, ha="center", fontweight="bold")
    ax.text(50, 6.6, "Before you write a line of RTL, know what you expect the tool "
                     "to build. Then check whether it did.\nEvery bug in this topic "
                     "lives in the gap between those two things.",
            fontsize=8.7, color=BODY, ha="center")
    save(f, "what_you_can_do")


for fn in (terminal_outcomes, learning_outcomes, syllabus_map, topic_structure,
           what_you_can_do):
    fn()
