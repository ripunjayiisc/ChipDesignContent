# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — the physical picture underneath RTL.

These come FIRST in the deck. RTL is an abstraction, and an abstraction is
only learnable once you have seen the thing it abstracts: what is physically
on the chip, what a signal physically is, what a register physically does,
and what physically happens in the gap between two clock edges.
"""
import _boot
from dsl import *


def chip_physical():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "What is actually on the chip", FS_TITLE)
    ax.text(50, H - 10.0, "Before any abstraction: these are the physical "
                          "objects everything else is built from.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    top = H - 15.0
    bh = 22.0
    items = [("TRANSISTOR", "~20 nm", "a switch: a voltage\non its gate lets\n"
              "current flow, or not", NAVY),
             ("GATE", "4-10 transistors", "a Boolean function\nbuilt from those\n"
              "switches", TEAL),
             ("FLIP-FLOP", "~20 transistors", "remembers ONE bit,\nand changes it "
              "only\nat the clock edge", VIOLET),
             ("BLOCK", "thousands", "a counter, a filter,\na CPU - what you\n"
              "are asked to build", GREEN)]
    x = 3
    for nm, scale, what, col in items:
        box(ax, x, top - bh, 21, bh, fc=WHITE, ec=col, lw=2.0)
        box(ax, x, top - 6.0, 21, 6.0, fc=col, ec=col)
        ax.text(x + 10.5, top - 3.0, nm, ha="center", va="center",
                fontsize=FS_SMALL, color=WHITE, fontweight="bold")
        ax.text(x + 10.5, top - 9.2, scale, ha="center", va="center",
                fontsize=FS_SMALL - 1, color=col, fontstyle="italic")
        ax.text(x + 10.5, top - 15.5, what, ha="center", va="center",
                fontsize=FS_SMALL - 1, color=BODY)
        if x > 3:
            arrow(ax, x - 3.4, top - bh / 2 - 1, x - 0.7, top - bh / 2 - 1,
                  color=SLATE, lw=2.0, ms=11)
        x += 24.4

    ax.text(50, 8.0, "Every design in this course is ultimately a pattern of "
                     "these four things.",
            fontsize=FS_HEAD, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 3.5, "RTL is a way of TALKING about that pattern without "
                     "drawing it. It does not replace it.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "chip_physical")


def signal_voltage():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "A signal is a voltage on a wire", FS_TITLE)
    ax.text(50, H - 10.0, "0 and 1 are not numbers travelling down the wire. "
                          "They are ranges of voltage.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    # ---- left: the voltage bands ---------------------------------------
    x0, y0, w, h = 8, 11.0, 28, 25.0
    box(ax, x0, y0, w, h, fc=WHITE, ec=SLATE, lw=1.6)
    bands = [(0.70, 0.30, "#EEF7F1", GREEN, "logic 1", "VDD"),
             (0.38, 0.32, "#FDECEF", RED, "forbidden", ""),
             (0.00, 0.38, "#F4F8FB", TEAL, "logic 0", "0 V")]
    for frac, fh, fill, col, lab, volt in bands:
        yy = y0 + frac * h
        box(ax, x0, yy, w, fh * h, fc=fill, ec=col, lw=1.4, r=0.3)
        ax.text(x0 + w / 2, yy + fh * h / 2, lab, ha="center", va="center",
                fontsize=FS_BODY, color=col, fontweight="bold")
    ax.text(x0 - 1.2, y0 + h, "VDD", ha="right", va="center",
            fontsize=FS_SMALL, color=NAVY, fontweight="bold")
    ax.text(x0 - 1.2, y0, "0 V", ha="right", va="center", fontsize=FS_SMALL,
            color=NAVY, fontweight="bold")
    ax.text(x0 + w / 2, y0 - 3.4, "what the wire actually carries",
            ha="center", fontsize=FS_SMALL, color=SLATE, fontweight="bold")

    # ---- right: a real edge --------------------------------------------
    bx, by = 48, 17.0
    lo, hi = by, by + 14.0
    wire(ax, [(bx, lo), (bx + 9, lo), (bx + 16, hi), (bx + 28, hi),
              (bx + 35, lo), (bx + 44, lo)], color=TEAL, lw=2.6)
    for xx in (bx + 9, bx + 16, bx + 28, bx + 35):
        wire(ax, [(xx, lo - 3.0), (xx, hi + 1.0)], color=GRID, lw=1.0, ls=":")
    ax.annotate("", xy=(bx + 9, lo - 2.0), xytext=(bx + 16, lo - 2.0),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.8))
    ax.text(bx + 12.5, lo - 5.0, "rise time", ha="center", fontsize=FS_SMALL,
            color=AMBER, fontweight="bold")
    ax.annotate("", xy=(bx + 28, lo - 2.0), xytext=(bx + 35, lo - 2.0),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.8))
    ax.text(bx + 31.5, lo - 5.0, "fall time", ha="center", fontsize=FS_SMALL,
            color=AMBER, fontweight="bold")
    ax.text(bx + 22, hi + 3.0, "a real signal, not a square wave",
            ha="center", fontsize=FS_BODY, color=NAVY, fontweight="bold")

    ax.text(50, 3.5, "Changing a wire from 0 to 1 means charging it, and that "
                     "takes real time.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "signal_voltage")


def register_physical():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "What a register physically does", FS_TITLE)
    ax.text(50, H - 10.0, "Not storage in the software sense - a door that the "
                          "clock edge opens for an instant.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    label_box(ax, 4, 15.0, 16, 13.0, "D        Q", fc=WHITE, ec=VIOLET,
              tc=NAVY, size=FS_HEAD, lw=2.2)
    wire(ax, [(4, 19.0), (7, 21.5), (4, 24.0)], color=VIOLET, lw=1.8)
    ax.text(2.5, 21.5, "clk", ha="right", va="center", fontsize=FS_SMALL,
            color=VIOLET, fontweight="bold")

    # --- one explicit timing picture, so every edge lines up -------------
    x0, P, n = 27.0, 10.0, 7
    hi, lo = 3.4, 0.0

    def trace(y, pts, col, name):
        wire(ax, [(x, y + (hi if v else lo)) for x, v in pts], color=col,
             lw=2.2)
        ax.text(x0 - 2.5, y + hi / 2, name, ha="right", va="center",
                fontsize=FS_SMALL, color=NAVY, fontweight="bold")

    # clock: low half, high half, rising edge at x0 + P/2 + k*P
    cpts = []
    for k in range(n):
        a = x0 + k * P
        cpts += [(a, 0), (a + P / 2, 0), (a + P / 2, 1), (a + P, 1)]
    trace(31.0, cpts, NAVY, "clk")

    edges = [x0 + P / 2 + k * P for k in range(n)]
    d_val = [1, 0, 1, 1, 0, 0, 1]        # value of D during cycle k
    # D changes shortly AFTER each edge, so it is stable across the next one
    dpts = [(x0, d_val[0])]
    for k in range(n - 1):
        ch = edges[k] + 2.0
        dpts += [(ch, d_val[k]), (ch, d_val[k + 1])]
    dpts += [(x0 + n * P, d_val[-1])]
    trace(22.5, dpts, TEAL, "D")

    # Q takes the value D held just before the edge, and holds it
    qpts = [(x0, 0)]
    for k in range(n):
        e = edges[k] + 0.8                      # clk-to-Q
        prev = d_val[k - 1] if k else 0
        qpts += [(e, prev), (e, d_val[k])]
    qpts += [(x0 + n * P, d_val[-1])]
    trace(14.0, qpts, GREEN, "Q")

    for e in edges[:4]:
        wire(ax, [(e, 12.0), (e, 34.8)], color=RED, lw=1.2, ls=":")
    ax.text(edges[1] + 6, 36.4, "D is captured at every rising edge",
            ha="center", fontsize=FS_SMALL, color=RED, fontweight="bold")

    ax.text(50, 7.5, "D wanders all cycle. Q takes D's value at the edge, then "
                     "holds it flat until the next one.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 3.0, "That is what makes a design analysable: between edges, "
                     "nothing you can see changes.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "register_physical")


def clock_cycle_anatomy():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "What happens between two clock edges", FS_TITLE)
    ax.text(50, H - 10.0, "This is the picture to keep in your head for the "
                          "rest of the course.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    xa, xb = 14.0, 88.0
    ytop = H - 15.0

    # the two edges
    for xx, lab in ((xa, "clock edge"), (xb, "next clock edge")):
        wire(ax, [(xx, 8.0), (xx, ytop)], color=NAVY, lw=2.4)
        ax.text(xx, ytop + 2.6, lab, ha="center", fontsize=FS_SMALL,
                color=NAVY, fontweight="bold")
    ax.annotate("", xy=(xa, ytop - 2.5), xytext=(xb, ytop - 2.5),
                arrowprops=dict(arrowstyle="<->", color=NAVY, lw=2.0))
    ax.text((xa + xb) / 2, ytop - 5.6, "ONE CLOCK PERIOD", ha="center",
            fontsize=FS_BODY, color=NAVY, fontweight="bold")

    yb = 15.0
    # phase 1: clock-to-Q
    x1 = xa + 9.0
    box(ax, xa, yb, x1 - xa, 7.0, fc="#F6F2FC", ec=VIOLET, lw=1.6)
    ax.text((xa + x1) / 2, yb + 3.5, "clk→Q", ha="center", va="center",
            fontsize=FS_SMALL, color=VIOLET, fontweight="bold")

    # phase 2: settling, with glitches
    x2 = xa + 44.0
    box(ax, x1, yb, x2 - x1, 7.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    gx = [x1 + 1 + i * 2.6 for i in range(15)]
    gy = [yb + 5.4 if i % 2 else yb + 1.6 for i in range(15)]
    wire(ax, list(zip(gx, gy)), color=AMBER, lw=1.4)
    ax.text((x1 + x2) / 2, yb - 3.0, "the logic settles\n(and glitches while "
            "it does)", ha="center", va="top", fontsize=FS_SMALL, color=AMBER,
            fontweight="bold")

    # phase 3: stable
    x3 = xb - 12.0
    box(ax, x2, yb, x3 - x2, 7.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    wire(ax, [(x2, yb + 5.4), (x3, yb + 5.4)], color=GREEN, lw=2.2)
    ax.text((x2 + x3) / 2, yb - 3.0, "stable, and correct",
            ha="center", va="top", fontsize=FS_SMALL, color=GREEN,
            fontweight="bold")
    wire(ax, [(x2, yb + 1.6), (x2 + 1.2, yb + 5.4)], color=GREEN, lw=2.2)

    # phase 4: setup window
    box(ax, x3, yb, xb - x3, 7.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text((x3 + xb) / 2, yb + 3.5, "setup", ha="center", va="center",
            fontsize=FS_SMALL, color=RED, fontweight="bold")
    ax.text((x3 + xb) / 2, yb + 10.5, "already\nstable", ha="center",
            va="center", fontsize=FS_SMALL, color=RED, fontweight="bold")

    ax.text(6.0, yb + 3.5, "data", ha="right", va="center", fontsize=FS_BODY,
            color=NAVY, fontweight="bold")

    ax.text(50, 4.0, "RTL says WHAT the value must be at the next edge. It "
                     "never says how long the settling takes.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "clock_cycle_anatomy")


def abstraction_stack():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The ladder of abstraction, and where RTL sits",
          FS_TITLE)

    ax.text(30, H - 10.0, "what you SAY at this level", ha="left",
            fontsize=FS_SMALL, color=SLATE, fontweight="bold")
    ax.text(96, H - 10.0, "what you leave out", ha="right", fontsize=FS_SMALL,
            color=SLATE, fontweight="bold")

    levels = [("ALGORITHM", "what the system computes", "all timing", GREEN),
              ("RTL", "which registers exist, and what transfers in",
               "gates, wiring, delays", NAVY),
              ("GATE", "every gate and every wire", "transistor sizes", VIOLET),
              ("TRANSISTOR", "every switch, and its width", "geometry", TEAL),
              ("LAYOUT", "the actual shapes on the silicon", "nothing", SLATE)]
    y = H - 13.0
    rh = 4.6
    for nm, says, omits, col in levels:
        hl = (nm == "RTL")
        box(ax, 6, y - rh, 91, rh, fc="#F4F8FB" if hl else WHITE, ec=col,
            lw=2.6 if hl else 1.4)
        box(ax, 6, y - rh, 22, rh, fc=col, ec=col)
        ax.text(17, y - rh / 2, nm, ha="center", va="center",
                fontsize=FS_BODY if hl else FS_SMALL, color=WHITE,
                fontweight="bold")
        ax.text(30, y - rh / 2, says, ha="left", va="center",
                fontsize=FS_SMALL, color=BODY)
        ax.text(96, y - rh / 2, omits, ha="right", va="center",
                fontsize=FS_SMALL - 1, color=SLATE, fontstyle="italic")
        if hl:
            ax.text(3.5, y - rh / 2, "▶", ha="center", va="center",
                    fontsize=FS_HEAD, color=NAVY, fontweight="bold")
        y -= rh + 0.7

    ax.text(50, 6.0, "Above RTL you cannot say WHEN things happen. Below it "
                     "you cannot say anything else.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 2.0, "Each rung down adds detail you must supply, and takes "
                     "away a decision the tool was making for you.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "abstraction_stack")


def designer_view():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The designer's side of the bargain", FS_TITLE)
    ax.text(50, H - 10.0, "RTL is a contract: you decide these, the tool "
                          "decides those.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    top = H - 14.0
    bh = 26.0

    box(ax, 3, top - bh, 46, bh, fc="#F4F8FB", ec=NAVY, lw=2.2)
    box(ax, 3, top - 6.0, 46, 6.0, fc=NAVY, ec=NAVY)
    ax.text(26, top - 3.0, "YOU DECIDE", ha="center", va="center",
            fontsize=FS_HEAD, color=WHITE, fontweight="bold")
    for i, it in enumerate(["which registers exist, and where",
                            "how many cycles an operation takes",
                            "what happens on each cycle",
                            "the interface, and the reset policy",
                            "how the design is partitioned"]):
        ax.text(6, top - 10.5 - i * 3.4, "▪", fontsize=FS_SMALL, color=NAVY,
                ha="left")
        ax.text(9, top - 10.5 - i * 3.4, it, fontsize=FS_SMALL, color=BODY,
                ha="left")

    box(ax, 51, top - bh, 46, bh, fc="#EEF7F1", ec=GREEN, lw=2.2)
    box(ax, 51, top - 6.0, 46, 6.0, fc=GREEN, ec=GREEN)
    ax.text(74, top - 3.0, "THE TOOL DECIDES", ha="center", va="center",
            fontsize=FS_HEAD, color=WHITE, fontweight="bold")
    for i, it in enumerate(["which gates to use, and how many",
                            "how big to make each one",
                            "how they are wired together",
                            "where buffers are needed",
                            "where everything is placed"]):
        ax.text(54, top - 10.5 - i * 3.4, "▪", fontsize=FS_SMALL, color=GREEN,
                ha="left")
        ax.text(57, top - 10.5 - i * 3.4, it, fontsize=FS_SMALL, color=BODY,
                ha="left")

    ax.text(50, 3.5, "Give away too much and you cannot meet timing. Give away "
                     "too little and you are drawing gates by hand.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "designer_view")


for fn in (chip_physical, signal_voltage, register_physical,
           clock_cycle_anatomy, abstraction_stack, designer_view):
    fn()
