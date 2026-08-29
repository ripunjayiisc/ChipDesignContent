# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — terminal outcomes, learning outcomes, syllabus."""
import _boot
from dsl import *


def terminal_outcomes():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Module 2 terminal outcomes", FS_TITLE)
    ax.text(50, H - 10.0, "NOS NIE/ELE/N0102  ·  Verilog RTL Coding for Synthesis "
                          "·  25 h theory + 35 h practical",
            fontsize=FS_SUB, color=SLATE, ha="center")

    outs = [("1", "Understand the design cycle of VLSI", TEAL, "Topics 1, 2"),
            ("2", "Understand Verilog syntax and LEVELS OF ABSTRACTION",
             VIOLET, "Topics 2, 4, 5"),
            ("3", "Design and develop IPs for VLSI using Verilog", NAVY,
             "Topics 2, 4"),
            ("4", "Emulate, debug and characterise reusable IPs", GREEN,
             "Topics 2, 5, 6")]
    y = H - 12.5
    bh = 6.4
    for n, hd, col, where in outs:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.8)
        ax.add_patch(Circle((9.5, y - bh / 2), 2.5, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - bh / 2, n, ha="center", va="center", fontsize=FS_BODY,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(15, y - bh / 2, hd, ha="left", va="center", fontsize=FS_BODY,
                color=col, fontweight="bold")
        ax.text(95, y - bh / 2, where, ha="right", va="center",
                fontsize=FS_SMALL, color=SLATE, fontstyle="italic")
        y -= bh + 1.3

    ax.text(50, 3.5, "Outcome 2 names this subtopic explicitly: "
                     "\"level of abstraction in Verilog programming\".",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "terminal_outcomes")


def learning_outcomes():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Key learning outcomes for this subtopic", FS_TITLE)

    y = H - 10.0
    bh = 29.0
    box(ax, 3, y - bh, 46, bh, fc=LIGHT, ec=TEAL, lw=2.0)
    box(ax, 3, y - 6.0, 46, 6.0, fc=TEAL, ec=TEAL)
    ax.text(26, y - 3.0, "THEORY", ha="center", va="center", fontsize=FS_HEAD,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "What register transfer level means,\nand the timing model it implies",
            "The levels of abstraction in an HDL,\nand how to choose between them",
            "How the synthesisable subset and the\ncoding rules shape what you write",
            "Verilog against VHDL"]):
        ax.text(6, y - 9.8 - i * 5.4, "▪", fontsize=FS_BODY, color=TEAL,
                ha="left")
        ax.text(9.5, y - 9.8 - i * 5.4, ln, fontsize=FS_SMALL, color=BODY,
                ha="left", va="top")

    box(ax, 51, y - bh, 46, bh, fc="#EEF7F1", ec=GREEN, lw=2.0)
    box(ax, 51, y - 6.0, 46, 6.0, fc=GREEN, ec=GREEN)
    ax.text(74, y - 3.0, "PRACTICAL", ha="center", va="center", fontsize=FS_HEAD,
            color=WHITE, fontweight="bold")
    for i, ln in enumerate([
            "Write RTL for basic digital circuits",
            "Validate a design by simulation,\nwith a testbench that checks itself",
            "Apply a coding standard, and check it\nmechanically rather than by eye",
            "Synthesise, and read what was built"]):
        ax.text(54, y - 9.8 - i * 5.4, "▪", fontsize=FS_BODY, color=GREEN,
                ha="left")
        ax.text(57.5, y - 9.8 - i * 5.4, ln, fontsize=FS_SMALL, color=BODY,
                ha="left", va="top")

    ax.text(50, 4.0, "Every one of them is assessed by a command you run.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "learning_outcomes")


def outcomes_commands():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Each outcome, and the command that assesses it",
          FS_TITLE)

    rows = [["what RTL means", "make transfer,  make ladder"],
            ["levels of abstraction", "make ladder,  make prove"],
            ["coding style and what it costs", "make mux,  make pitfalls"],
            ["the coding standard", "make lint,  make lintcheck"],
            ["state machines and structure", "make fsm,  make dpctrl,  make reuse"],
            ["synthesis, and reading the result", "make subset,  make flow"],
            ["Verilog or VHDL", "make langs"]]
    table(ax, 8, H - 9.5, ["the outcome", "the command"], rows, [40, 44], 4.2,
          size=FS_TABLE, bold_col=[0])

    ax.text(50, 3.0, "Nothing in this topic is assessed by recitation.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "outcomes_commands")


def syllabus_map():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Every syllabus phrase, and where it is covered",
          FS_TITLE)

    rows = [["Basics of register transfer level (RTL) design", "Theory 1",
             "6-25"],
            ["Overview of RTL design process and methodology", "Theory 2",
             "26-41"],
            ["   ... and the patterns that process produces", "Theory 3",
             "42-59"],
            ["Introduction to HDLs such as Verilog or VHDL", "Theory 4",
             "60-75"],
            ["Practical: RTL Design and Implementation Labs", "Labs A-N",
             "76-92"]]
    table(ax, 4, H - 9.5, ["syllabus phrase", "section", "slides"], rows,
          [56, 20, 16], 4.6, size=FS_TABLE, bold_col=[1])

    ax.text(50, 8.5, "The syllabus gives this subtopic 4 notional hours.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 3.5, "Enough to define the terms; not enough to make anyone "
                     "believe them. Lecture from the summary slides to fit four "
                     "hours;\ndeliver it properly by running the lab alongside.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "syllabus_map")


def topic_structure():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "How this session runs", FS_TITLE)

    parts = [("THEORY 1", "What RTL is",
              "the two kinds of logic, the discipline, abstraction", TEAL),
             ("THEORY 2", "The methodology",
              "the flow, the subset, the rules, and coding style", VIOLET),
             ("THEORY 3", "The patterns",
              "datapath and controller, state machines, parameters", AMBER),
             ("THEORY 4", "HDLs", "what an HDL is, and Verilog against VHDL",
              NAVY),
             ("PRACTICAL", "Labs A-N", "26 hours, 103 exercises, all measured",
              GREEN)]
    y = H - 9.0
    bh = 5.6
    for nm, hd, sub, col in parts:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.6)
        box(ax, 3, y - bh, 20, bh, fc=col, ec=col)
        ax.text(13, y - bh / 2, nm, ha="center", va="center", fontsize=FS_SMALL,
                color=WHITE, fontweight="bold")
        ax.text(25, y - bh / 2, hd, ha="left", va="center", fontsize=FS_BODY,
                color=col, fontweight="bold")
        ax.text(48, y - bh / 2, sub, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        y -= bh + 1.1

    ax.text(50, 3.0, "RTL is not a language and it is not a tool. It is a way "
                     "of thinking about hardware.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "topic_structure")


def what_you_can_do():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "By the end of this subtopic you can", FS_TITLE,
          color=GREEN)

    items = ["Read an always block and say which registers it creates.",
             "Tell combinational logic from sequential, and code each correctly.",
             "Write the same function at four levels of abstraction, and say "
             "what each level costs you.",
             "Prove two descriptions are the same circuit, instead of hoping.",
             "Say which Verilog constructs synthesise, which do not, and which "
             "are traps.",
             "Recognise an inferred latch before the tool builds one.",
             "Explain why an incomplete sensitivity list is worse than an error.",
             "Apply the seven coding rules, and say why each one exists.",
             "Split a block into a datapath and a controller.",
             "Write a state machine in the three-block form, in either style.",
             "Parameterise a design so one file covers a family of widths.",
             "Read a VHDL design without needing it translated.",
             "Take a design from spec to formal proof, showing evidence at each "
             "stage."]
    y = H - 11.0
    for it in items:
        ax.text(5, y, "✓", fontsize=FS_BODY, color=GREEN, ha="left",
                va="center", fontweight="bold")
        ax.text(9, y, it, fontsize=FS_BODY, color=BODY, ha="left", va="center")
        y -= 3.1

    ax.text(50, 3.0, "And one habit: before you write RTL, know what you expect "
                     "the tool to build. Then check whether it did.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "what_you_can_do")


for fn in (terminal_outcomes, learning_outcomes, outcomes_commands,
           syllabus_map, topic_structure, what_you_can_do):
    fn()
