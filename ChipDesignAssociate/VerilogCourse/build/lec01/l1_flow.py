# -*- coding: utf-8 -*-
"""Lecture 01 diagrams — the design flow, CAD tools, and the ladder."""
import _boot
from dsl import *
from l1_kit import wrap, note, column_cards, rowcards, ladder, chars_for



# The prose that used to sit in a box at the foot of each panel. It belongs on
# the slide as real text at 12pt, not inside a PNG that gets scaled down.
CARDS = {
    "design_flow_steps": (
        "Why it had to be standardized",
        "Dozens of engineers, several companies and a fabrication plant all "
        "work on one chip. A standard flow gives each step a defined input, a "
        "defined output and a defined check — so the work can be divided up, "
        "and a mistake is caught at the step that made it rather than three "
        "steps later.", "NAVY"),
    "cad_transform": (
        "The idea to hold on to",
        "At every one of these steps, both the input and the output are "
        "hardware descriptions. Nothing is ever \"compiled into a program\" — "
        "the design simply gets described in progressively more concrete "
        "terms, until the last description is a set of shapes a factory can "
        "print.", "TEAL"),
    "hdl_family": (
        "\"Designs are created typically using HDLs, which get transformed "
        "from one level of abstraction to the next as the design flow "
        "progresses.\"",
        "Both Verilog and VHDL can describe the same hardware, and a synthesis "
        "tool will produce the same gates from either. The choice is a matter "
        "of house style, existing code and local convention — not of what the "
        "silicon can do. In Lab 5 you will write the same counter in both and "
        "compare the waveforms.", "NAVY"),
    "ladder_example": (
        "The point of the exercise",
        "All five describe exactly the same counter. A designer writes the "
        "first one; tools produce the other four. In Lab 3 you will run that "
        "descent yourself and count what comes out at each level.", "NAVY"),
    "abstraction_what_changes": (
        "Read the last column",
        "The number of things to keep track of grows by roughly a factor of "
        "ten at every level. That growth is exactly why a designer works at "
        "the top of the table and lets tools handle the bottom.", "TEAL"),
}

def design_flow_steps():
    f, ax, H = panel(4.04)
    title(ax, 50, H - 3.5, "\"Step by step, starting from a given specification, "
          "down to the actual hardware circuit.\"", size=FS_SUB, color=SLATE,
          weight="normal")

    steps = [("SPECIFICATION", "what it must do", "English, numbers, timing "
              "budgets", TEAL),
             ("SYNTHESIS", "turn it into gates", "one HDL description becomes a "
              "more detailed one", VIOLET),
             ("SIMULATION", "check it works", "apply stimulus, watch the "
              "outputs", GREEN),
             ("LAYOUT", "place it on silicon", "polygons on each fabrication "
              "layer", AMBER),
             ("TESTABILITY", "check the chip you built", "patterns that find "
              "manufacturing faults", RED),
             ("… AND MANY MORE", "the lecturer's own phrase", "floorplanning, "
              "timing closure, sign-off", SLATE)]
    x = 2.5
    w = 15.1
    gap = 1.3
    top = H - 7
    bh = 19.0
    for i, (head, what, detail, col) in enumerate(steps):
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.0, w, 4.0, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.0, head, ha="center", va="center",
                fontsize=8.6, color=WHITE, fontweight="bold")
        wrap(ax, x + w / 2, top - 6.6, w - 2.4, what, FS_SMALL - 1.5,
             color=col, ha="center", weight="bold")
        wrap(ax, x + w / 2, top - 11.4, w - 2.4, detail, FS_SMALL - 2.0,
             ha="center")
        if i < len(steps) - 1:
            arrow(ax, x + w + 0.2, top - bh / 2, x + w + gap - 0.2,
                  top - bh / 2, color=SLATE, lw=1.6, ms=9)
        x += w + gap

    save(f, "design_flow_steps")


def cad_transform():
    f, ax, H = panel(4.54)
    title(ax, 50, H - 3.5, "\"A CAD tool transforms its HDL input into an HDL "
          "output that contains more detailed information about the hardware.\"",
          size=FS_SUB, color=SLATE, weight="normal")

    # the single transformation, drawn once
    top = H - 7.5
    bh = 11.0
    box(ax, 4.0, top - bh, 24.0, bh, fc=LIGHT, ec=TEAL, lw=2.0)
    ax.text(16.0, top - 3.6, "HDL IN", ha="center", va="center",
            fontsize=FS_BODY, color=TEAL, fontweight="bold")
    wrap(ax, 16.0, top - 7.2, 21.0, "a description of the design at one level "
         "of detail", FS_SMALL - 1.0, ha="center")

    box(ax, 36.0, top - bh, 24.0, bh, fc=NAVY, ec=NAVY, lw=2.0)
    ax.text(48.0, top - 3.6, "CAD TOOL", ha="center", va="center",
            fontsize=FS_BODY, color=WHITE, fontweight="bold")
    wrap(ax, 48.0, top - 7.2, 21.0, "synthesis, mapping, placement, routing",
         FS_SMALL - 1.0, color=PALE if False else "#C9D6E3", ha="center")

    box(ax, 68.0, top - bh, 28.0, bh, fc=LIGHT, ec=GREEN, lw=2.0)
    ax.text(82.0, top - 3.6, "HDL OUT", ha="center", va="center",
            fontsize=FS_BODY, color=GREEN, fontweight="bold")
    wrap(ax, 82.0, top - 7.2, 25.0, "the same design, described in MORE detail",
         FS_SMALL - 1.0, ha="center")

    arrow(ax, 28.6, top - bh / 2, 35.4, top - bh / 2, color=SLATE, lw=2.2, ms=12)
    arrow(ax, 60.6, top - bh / 2, 67.4, top - bh / 2, color=SLATE, lw=2.2, ms=12)

    # the four transformations the lecture names
    y = top - bh - 4.0
    ax.text(50, y, "And the tool is applied again and again, one level at a time",
            ha="center", va="center", fontsize=FS_BODY, color=NAVY,
            fontweight="bold")
    y -= 4.2
    pairs = [("Behavioral", "Register transfer", VIOLET),
             ("Register transfer", "Gate", TEAL),
             ("Gate", "Transistor", AMBER),
             ("Transistor", "Layout", RED)]
    x = 3.0
    w = 23.0
    gap = 1.8
    ph = 7.4
    for a, b, col in pairs:
        box(ax, x, y - ph, w, ph, fc=WHITE, ec=col, lw=1.6)
        ax.text(x + w / 2, y - 2.6, a, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=BODY)
        ax.text(x + w / 2, y - 4.6, "↓", ha="center", va="center",
                fontsize=FS_SMALL, color=col, fontweight="bold")
        ax.text(x + w / 2, y - 6.4, b, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=col, fontweight="bold")
        x += w + gap

    save(f, "cad_transform")


def hdl_family():
    f, ax, H = panel(3.60)

    y = column_cards(ax, 2.5, H - 1.5, 95.5, [
        ("VERILOG", "C-like syntax, terse, and the language of this course. "
         "Dominant in industry in the Americas and much of Asia. "
         "Standardised as IEEE 1364.", TEAL),
        ("VHDL", "Ada-like syntax, verbose and strongly typed. Strong in "
         "Europe, aerospace and defence. Standardised as IEEE 1076.", VIOLET),
        ("SystemVerilog", "A large superset of Verilog, adding features aimed "
         "mostly at verification: classes, constrained random stimulus, "
         "assertions. IEEE 1800.", GREEN),
        ("SystemC", "A C++ class library rather than a separate language, used "
         "for modelling whole systems before the hardware is written.", SLATE)])

    save(f, "hdl_family")


def flow_ladder():
    f, ax, H = panel(5.24)
    title(ax, 50, H - 3.5, "The lecture's own diagram — each box is a "
          "description, each arrow is a CAD tool", size=FS_SUB, color=SLATE,
          weight="normal")

    top = H - 6
    ax.add_patch(Polygon([(10.0, top), (32.0, top), (35.5, top - 1.8),
                          (32.0, top - 3.6), (10.0, top - 3.6),
                          (6.5, top - 1.8)], fc="#FFF7EC", ec=AMBER, lw=2.0,
                         zorder=3))
    ax.text(21.0, top - 1.8, "DESIGN IDEA", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=AMBER, fontweight="bold", zorder=4)

    # each box carries its own right-hand annotation on a second line, which
    # keeps the ladder narrow enough to sit beside the notes
    steps = [("Behavioral Design", "flow graph, pseudo code", VIOLET),
             ("Data Path Design", "bus / register structure", TEAL),
             ("Logic Design", "gate / flip-flop netlist", GREEN),
             ("Physical Design", "transistor layout", AMBER),
             ("Manufacturing", "masks, one per layer", RED)]
    sh, gp = 4.6, 1.1
    y = top - 5.0
    for i, (lab, ann, col) in enumerate(steps):
        box(ax, 6.5, y - sh, 29.0, sh, fc=WHITE, ec=col, lw=1.8)
        box(ax, 6.5, y - sh, 1.2, sh, fc=col, ec=col, lw=0, r=0.4)
        ax.text(21.0, y - 1.7, lab, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=NAVY, fontweight="bold")
        ax.text(21.0, y - 3.4, ann, ha="center", va="center",
                fontsize=FS_SMALL - 2.0, color=col)
        if i < len(steps) - 1:
            arrow(ax, 21.0, y - sh - 0.1, y * 0 + 21.0, y - sh - gp + 0.1,
                  color=SLATE, lw=1.7, ms=9)
        y -= sh + gp
    y += gp

    ax.add_patch(Polygon([(10.0, y - 1.0), (32.0, y - 1.0), (35.5, y - 2.8),
                          (32.0, y - 4.6), (10.0, y - 4.6), (6.5, y - 2.8)],
                         fc="#FDECEF", ec=RED, lw=2.0, zorder=3))
    ax.text(21.0, y - 2.8, "CHIP / BOARD", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=RED, fontweight="bold", zorder=4)

    # the reading of the diagram, as a list rather than as cards: four stacked
    # cards would not fit beside a ladder this tall, and the ladder is the point
    notes = [("Each box is a DESCRIPTION", NAVY,
              "Not a stage of manufacture — a document that says what the "
              "circuit is, in a different vocabulary each time."),
             ("Each arrow is a TOOL", TEAL,
              "A program reads the description above it and writes the one "
              "below, adding detail that was not there before."),
             ("Detail only ever increases", VIOLET,
              "You never climb back up. Each level fixes decisions that the "
              "level above deliberately left open."),
             ("This course lives at the top two", GREEN,
              "Behavioral and data path — exactly where Verilog is written. "
              "The rest is done for you by tools.")]
    nx = 42.0
    ny = top + 0.5
    for head, col, body in notes:
        box(ax, nx, ny - 7.6, 1.2, 7.6, fc=col, ec=col, lw=0, r=0.4)
        ax.text(nx + 3.2, ny - 1.6, head, ha="left", va="center",
                fontsize=FS_SMALL, color=col, fontweight="bold")
        wrap(ax, nx + 3.2, ny - 4.6, 52.0, body, FS_SMALL - 1.5, lh=2.5)
        ny -= 9.4

    save(f, "flow_ladder")


def ladder_example():
    f, ax, H = panel(4.54)
    title(ax, 50, H - 3.5, "A 4-bit counter — the same hardware, described five "
          "ways", size=FS_SUB, color=SLATE, weight="normal")

    column_cards(ax, 2.5, H - 6.5, 95.5, [
        ("1 · BEHAVIORAL",
         "\"On every rising clock edge, unless reset is asserted, the output "
         "becomes one more than it was.\"  A sentence — or a few lines of "
         "Verilog.", VIOLET),
        ("2 · DATA PATH (RTL)",
         "A 4-bit register, a 4-bit incrementer, and a multiplexer choosing "
         "between the incremented value and zero. Named blocks, wired "
         "together.", TEAL),
        ("3 · LOGIC",
         "Four D flip-flops and about a dozen gates — AND, XOR, inverters — "
         "taken from a standard cell library and connected.", GREEN),
        ("4 · PHYSICAL",
         "Each cell becomes a rectangle of silicon at a fixed position, and "
         "every connection becomes a metal track on a specific layer.", AMBER),
        ("5 · MANUFACTURE",
         "A set of masks: one layer of polygons per fabrication step, sent to "
         "the foundry.", RED)], gap=1.6)
    save(f, "ladder_example")


def abstraction_what_changes():
    f, ax, H = panel(3.49)

    headers = ["Level", "A component is…", "A connection is…",
               "Typical count for a small design"]
    rows = [["Behavioral", "a statement", "a variable name", "tens of lines"],
            ["Data path (RTL)", "register, adder, mux", "a named bus or wire",
             "tens of blocks"],
            ["Logic", "gate or flip-flop", "a net", "hundreds of cells"],
            ["Physical", "a placed cell", "a metal track", "thousands of shapes"],
            ["Manufacturing", "a polygon", "a layer", "millions of shapes"]]
    cols = [(TEAL, "Behavioral"), (VIOLET, "Data path (RTL)"), (GREEN, "Logic"),
            (AMBER, "Physical"), (RED, "Manufacturing")]
    widths = [19.0, 24.0, 22.0, 30.5]
    x0 = 2.5
    y = H - 2.5
    rh = 4.4
    # header
    cx = x0
    for wdt, h in zip(widths, headers):
        box(ax, cx, y - rh, wdt, rh, fc=NAVY, ec=NAVY, lw=0.8, r=0.0)
        ax.text(cx + wdt / 2, y - rh / 2, h, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=WHITE, fontweight="bold")
        cx += wdt
    y -= rh
    for i, row in enumerate(rows):
        cx = x0
        for j, (wdt, cell) in enumerate(zip(widths, row)):
            box(ax, cx, y - rh, wdt, rh, fc=WHITE if i % 2 == 0 else LIGHT,
                ec=GRID, lw=0.8, r=0.0)
            ax.text(cx + wdt / 2, y - rh / 2, cell, ha="center", va="center",
                    fontsize=FS_SMALL - 0.5,
                    color=cols[i][0] if j == 0 else BODY,
                    fontweight="bold" if j == 0 else "normal")
            cx += wdt
        y -= rh

    save(f, "abstraction_what_changes")


if __name__ == "__main__":
    design_flow_steps()
    cad_transform()
    hdl_family()
    flow_ladder()
    ladder_example()
    abstraction_what_changes()
