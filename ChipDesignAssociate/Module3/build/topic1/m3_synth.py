# -*- coding: utf-8 -*-
"""Module 3 Topic 1 diagrams — timing constraints for synthesis, and what
synthesis does with them."""
import _boot
from dsl import *


def constraints_drive_synthesis():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Constraints are the input to synthesis, not a report setting",
          12)
    ax.text(50, H - 7.2, "The same RTL becomes a different circuit depending on what "
                         "you asked for.",
            fontsize=9, color=SLATE, ha="center")

    yb = H - 14.0
    label_box(ax, 6, yb - 9.0, 18, 9.0, "your RTL", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.2, lw=1.8)
    label_box(ax, 41, yb - 9.0, 18, 9.0, "synthesis", fc=LIGHT, ec=TEAL, tc=TEAL,
              size=9.2, lw=1.8)
    label_box(ax, 76, yb - 9.0, 18, 9.0, "netlist", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.2, lw=1.8)
    arrow(ax, 24, yb - 4.5, 41, yb - 4.5, color=SLATE, lw=1.8)
    arrow(ax, 59, yb - 4.5, 76, yb - 4.5, color=SLATE, lw=1.8)
    label_box(ax, 41, yb - 24.0, 18, 8.0, "your SDC", fc="#FFF7EC", ec=AMBER,
              tc=AMBER, size=9.2, lw=1.8)
    arrow(ax, 50, yb - 16.0, 50, yb - 9.0, color=AMBER, lw=2.0)
    ax.text(62, yb - 20.0, "the objective the optimiser is\nactually trying to meet",
            fontsize=8.2, color=AMBER, ha="left", va="center", fontstyle="italic")

    rows = [["no constraint at all", "optimise for area", "small and slow"],
            ["a loose period", "stop as soon as it fits", "small, just fast enough"],
            ["a tight period", "spend area on the critical path", "large and fast"],
            ["an impossible period", "try everything, still fail",
             "large, slow AND late"]]
    table(ax, 6, 29.0, ["what you write", "what the tool does", "what you get"],
          rows, [30, 34, 24], 4.6, size=8.4, bold_col=[0])

    ax.text(50, 4.2, "Row four is real, and it is expensive.", fontsize=9.2,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 1.2, "Ask for a period the technology cannot deliver and the tool "
                     "burns area and runtime chasing it.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "constraints_drive_synthesis")


def sdc_minimum():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 73.0
    title(ax, 50, H - 3, "The minimum honest constraint set, in order", 12.5)

    steps = [("1", "create_clock", "Every clock, including generated ones. Without "
              "this there is\nno target and nothing is checked.", TEAL),
             ("2", "set_clock_uncertainty", "Jitter, plus the clock-tree skew that "
              "does not exist yet.\nTaking it out makes the report prettier and the "
              "chip no faster.", VIOLET),
             ("3", "set_input_delay / set_output_delay", "Every port, against the "
              "clock that samples it. Omit these and\nevery boundary path is "
              "UNCONSTRAINED - unchecked, not passed.", NAVY),
             ("4", "exceptions, each with a reason", "set_false_path and "
              "set_multicycle_path. Only write one you can\njustify in a sentence "
              "on the line above it.", AMBER),
             ("5", "check for holes", "Report unconstrained endpoints. It must be "
              "zero. A clean report\non a half-constrained design is worse than a "
              "failing one.", GREEN)]
    y = H - 9.5
    rh = 8.8
    for n, hd, sub, col in steps:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((9.5, y - rh / 2), 2.6, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - rh / 2, n, ha="center", va="center", fontsize=9.4,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(15, y - 3.0, hd, ha="left", fontsize=9.0, color=col,
                fontweight="bold", family="monospace")
        ax.text(15, y - 6.4, sub, ha="left", va="center", fontsize=7.9, color=BODY)
        y -= rh + 1.4

    box(ax, 4, 2.5, 92, 8.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 7.6, "Module 2 Topic 6 develops each of these in full.", fontsize=9.0,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.0, "This topic assumes them and moves on to what synthesis then does "
                     "with your circuit.",
            fontsize=8.4, color=SLATE, ha="center", fontstyle="italic")
    save(f, "sdc_minimum")


def synth_deletes_fix():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "Synthesis deletes your hazard fix. Every time.", 12.5,
          color=RED)
    ax.text(50, H - 7.4, "The consensus term is REDUNDANT by construction. "
                         "Removing redundancy is what an optimiser is for.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["f = a&~b | b&c", "1", "$_MUX_", "the hazard is still in there"],
            ["f = a&~b | b&c | a&c", "1", "$_MUX_", "identical netlist - term gone"]]
    table(ax, 4, H - 11.5, ["what you wrote in RTL", "cells", "gate", "result"],
          rows, [32, 12, 18, 30], 5.6, size=8.6, bold_col=[0],
          colcolors={2: VIOLET})

    box(ax, 4, 24.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 35.6, "And look at what it built instead", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 30.4, "A single multiplexer. A B' + B C is exactly B ? C : A, and the "
                      "optimiser saw that before it saw\nanything else. Whether THAT "
                      "cell glitches is decided by its internals, in a library you\n"
                      "did not write.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 4, 3.0, 92, 18.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 18.0, "So how do you keep a hazard-free circuit?", fontsize=9.6,
            color=AMBER, ha="center", fontweight="bold")
    for i, ln in enumerate([
            "Protect it structurally: a dont_touch / keep attribute on the net or "
            "the cell.",
            "Or instantiate a library cell directly, so there is nothing to optimise.",
            "Or put it in a module the tool is told not to flatten.",
            "And then re-run the glitch detector on the NETLIST, not on the RTL."]):
        ax.text(8, 13.6 - i * 3.3, "•", fontsize=9, color=AMBER, ha="left",
                fontweight="bold")
        ax.text(11, 13.6 - i * 3.3, ln, fontsize=8.4, color=BODY, ha="left")
    save(f, "synth_deletes_fix")


def where_hazards_matter():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "One glitchy signal, three consumers - the measurement", 12.5)

    rows = [["as DATA into a normally-clocked flop", "correct",
             "sampled long after it settled"],
            ["as a CLOCK", "4 spurious edges", "every glitch is an edge"],
            ["as an ASYNCHRONOUS RESET", "flag cleared", "no clock referees it"]]
    table(ax, 4, H - 10.0, ["how the signal was used", "what happened", "why"],
          rows, [38, 24, 30], 5.6, size=8.6, bold_col=[0],
          colcolors={1: RED})

    box(ax, 4, 22.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 33.6, "The glitch was placed 80 ns before any clock edge", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 28.4, "That is the friendliest possible case for \"synchronous design "
                      "tolerates glitches\". It is true for\nthe first row and false "
                      "for the other two - and the signal is the same signal.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 4, 3.0, 92, 16.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 16.0, "So the rule is not \"glitches do not matter\"", fontsize=9.6,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 11.6, "It is: a glitch is harmless ONLY where a clock edge samples it "
                      "after it has settled.",
            fontsize=8.8, color=BODY, ha="center", fontweight="bold")
    ax.text(50, 6.4, "Anywhere edge-sensitive - a derived clock, a latch enable, an "
                     "asynchronous reset or set, a\nhandshake into another clock "
                     "domain - hazards are still yours to remove.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "where_hazards_matter")


def synth_to_sta():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "Circuit synthesis and timing analysis: one loop", 12.5)

    import math
    cx, cy, r = 50.0, H - 24.0, 14.0
    nodes = [("RTL", 90, NAVY), ("constraints", 18, AMBER), ("synthesis", -54, TEAL),
             ("netlist", -126, VIOLET), ("timing report", 162, GREEN)]
    pts = []
    for nm, ang, col in nodes:
        a = math.radians(ang)
        pts.append((cx + r * math.cos(a) * 2.0, cy + r * math.sin(a), nm, col))
    for x, y, nm, col in pts:
        box(ax, x - 11, y - 4.6, 22, 9.2, fc=WHITE, ec=col, lw=1.7)
        ax.text(x, y, nm, ha="center", va="center", fontsize=8.6, color=col,
                fontweight="bold")
    for i in range(len(pts)):
        x1, y1, _, _ = pts[i]
        x2, y2, _, _ = pts[(i + 1) % len(pts)]
        dx, dy = x2 - x1, y2 - y1
        dd = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / dd, dy / dd
        arrow(ax, x1 + ux * 13.0, y1 + uy * 6.0, x2 - ux * 13.0, y2 - uy * 6.0,
              color=SLATE, lw=1.5, ms=8)

    box(ax, 4, 3.0, 92, 15.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 14.6, "You go round this loop until three things are true at once",
            fontsize=9.4, color=GREEN, ha="center", fontweight="bold")
    for i, ln in enumerate(["setup slack >= 0 at the slow corner",
                            "hold slack >= 0 at the fast corner",
                            "zero unconstrained endpoints"]):
        ax.text(12, 10.6 - i * 3.2, "✓", fontsize=9, color=GREEN, ha="left",
                fontweight="bold")
        ax.text(16, 10.6 - i * 3.2, ln, fontsize=8.5, color=BODY, ha="left")
    save(f, "synth_to_sta")


def area_speed():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Everything in this topic is a trade", 13)

    items = [("hazard-free cover", "+ area, + power", "no glitches on that output",
              GREEN),
             ("pipelining", "+ registers, + latency", "a faster clock", TEAL),
             ("hold buffers", "+ area, + power", "the design works at all", VIOLET),
             ("tighter constraints", "+ area, + runtime", "a faster chip, up to a point",
              AMBER),
             ("looser constraints", "- area", "a slower chip you can actually build",
              SLATE)]
    y = H - 9.0
    rh = 6.4
    for nm, cost, gain, col in items:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.3)
        ax.text(8, y - rh / 2, nm, fontsize=8.8, color=col, ha="left", va="center",
                fontweight="bold")
        ax.text(40, y - rh / 2, cost, fontsize=8.4, color=RED, ha="left", va="center")
        ax.text(64, y - rh / 2, gain, fontsize=8.4, color=BODY, ha="left",
                va="center")
        y -= rh + 1.2

    ax.text(40, H - 6.0, "you pay", fontsize=8.2, color=RED, ha="left",
            fontweight="bold")
    ax.text(64, H - 6.0, "you get", fontsize=8.2, color=NAVY, ha="left",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 8.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 8.0, "There is no free row in that table, and a design that pays "
                     "nothing gets nothing.",
            fontsize=9.0, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.6, "The engineering is in deciding which of these you need, "
                     "on which nets, and defending the choice.",
            fontsize=8.4, color=SLATE, ha="center", fontstyle="italic")
    save(f, "area_speed")


for fn in (constraints_drive_synthesis, sdc_minimum, synth_deletes_fix,
           where_hazards_matter, synth_to_sta, area_speed):
    fn()
