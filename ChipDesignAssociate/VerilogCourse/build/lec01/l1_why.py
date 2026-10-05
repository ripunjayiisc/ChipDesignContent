# -*- coding: utf-8 -*-
"""Lecture 01 diagrams — objectives, and the problem the design flow solves."""
import _boot
from dsl import *
import matplotlib.pyplot as plt
import numpy as np


def _wrap(ax, x, y, w_chars, text, size, color=BODY, lh=2.9, ha="left",
          weight="normal", style="normal"):
    import textwrap
    lines = textwrap.wrap(text, w_chars)
    for i, ln in enumerate(lines):
        ax.text(x, y - i * lh, ln, ha=ha, va="center", fontsize=size,
                color=color, fontweight=weight, fontstyle=style)
    return y - (len(lines) - 1) * lh


def _note(ax, x, y_top, w, head, text, col=NAVY, fill=LIGHT, chars=104,
          size=None, lh=2.8, head_size=None):
    """A footer card that sizes itself to the wrapped text it holds."""
    import textwrap
    size = FS_SMALL if size is None else size
    head_size = FS_BODY if head_size is None else head_size
    lines = textwrap.wrap(text, chars)
    h = (2.6 if head else 0.0) + 2.6 + lh * len(lines) + 1.4
    box(ax, x, y_top - h, w, h, fc=fill, ec=col, lw=1.6)
    yy = y_top - 3.0
    if head:
        ax.text(x + 2.6, yy, head, ha="left", va="center", fontsize=head_size,
                color=col, fontweight="bold")
        yy -= 3.4
    for i, ln in enumerate(lines):
        ax.text(x + 2.6, yy - i * lh, ln, ha="left", va="center", fontsize=size,
                color=BODY)
    return y_top - h


def objectives():
    f, ax, H = panel(5.24)
    title(ax, 50, H - 3.5, "Hardware Modeling Using Verilog — the lecturer's own "
          "six objectives, with what each one will mean in practice",
          size=FS_SUB, color=SLATE, weight="normal")

    items = [("1", "Learn about the Verilog hardware description language.",
              "Syntax, data types, operators, and the module as the unit of design.",
              TEAL),
             ("2", "Understand the difference between behavioral and structural "
              "design styles.",
              "Say WHAT the circuit does, or name WHICH PARTS it is built "
              "from. This distinction runs through the course.", VIOLET),
             ("3", "Learn to write test benches and analyze simulation results.",
              "A design you cannot test is a design you cannot trust. Weeks 5 "
              "onwards are built on this.", GREEN),
             ("4", "Learn to model combinational and sequential circuits.",
              "Logic with no memory, and logic with memory. Almost every real "
              "block is a mixture of the two.", AMBER),
             ("5", "Distinguish between good and bad coding practices.",
              "Verilog will let you write something that simulates correctly "
              "and synthesises into the wrong hardware.", RED),
             ("6", "Case studies with some complex designs.",
              "Week 8 builds a pipelined processor — datapath and control path "
              "— entirely in Verilog.", NAVY)]
    y = H - 7
    h = 5.5
    gap = 0.55
    for n, head, detail, col in items:
        box(ax, 2.0, y - h, 96.0, h, fc=WHITE, ec=GRID, lw=1.1)
        box(ax, 2.0, y - h, 5.6, h, fc=col, ec=col, lw=1.0)
        ax.text(4.8, y - h / 2, n, ha="center", va="center", fontsize=FS_HEAD,
                color=WHITE, fontweight="bold")
        ax.text(9.5, y - h / 2 + 1.35, head, ha="left", va="center",
                fontsize=FS_SMALL, color=NAVY, fontweight="bold")
        ax.text(9.5, y - h / 2 - 1.45, detail, ha="left", va="center",
                fontsize=FS_SMALL - 1.0, color=BODY)
        y -= h + gap
    save(f, "objectives")


def hdl_not_program():
    f, ax, H = panel(5.14)
    title(ax, 50, H - 3.5, "Both are text you type. What the text MEANS is "
          "completely different — and this is the single most common beginner "
          "error.", size=FS_SUB, color=SLATE, weight="normal")

    top = H - 7.5
    bh = 26.5
    panes = [(2.0, RED, "#FDF2F4", "C  —  A PROGRAM",
              ["a = 1;", "b = 2;", "c = 3;"],
              "These happen ONE AFTER ANOTHER.",
              "The order of the lines is the order of events. Swap two of "
              "them and you change what the program does."),
             (51.5, GREEN, "#EEF7F1", "VERILOG  —  A DESCRIPTION",
              ["assign a = 1;", "assign b = 2;", "assign c = 3;"],
              "These are all true AT THE SAME TIME.",
              "Each line describes a piece of wire that exists permanently. "
              "Swap two of them and nothing changes at all.")]
    for x, col, fill, head, code, punch, body in panes:
        w = 46.5
        box(ax, x, top - bh, w, bh, fc=fill, ec=col, lw=1.8)
        box(ax, x, top - 4.2, w, 4.2, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.1, head, ha="center", va="center",
                fontsize=FS_BODY, color=WHITE, fontweight="bold")
        yy = top - 7.8
        for ln in code:
            ax.text(x + 3.5, yy, ln, ha="left", va="center", fontsize=FS_MONO,
                    color=INK, family="DejaVu Sans Mono")
            yy -= 3.1
        ax.text(x + 3.5, yy - 1.4, punch, ha="left", va="center",
                fontsize=FS_SMALL - 0.5, color=col, fontweight="bold")
        _wrap(ax, x + 3.5, yy - 5.0, 55, body, FS_SMALL - 1.0, lh=2.7)

    box(ax, 2.0, 1.6, 96.0, 8.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 7.4, "In the Verilog pane there is no \"first\" and no \"next\" "
            "— only what is connected to what.", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=BODY)
    ax.text(50, 5.0, "You are not writing instructions for a machine to follow.",
            ha="center", va="center", fontsize=FS_SMALL, color=BODY)
    ax.text(50, 2.8, "You are writing a description of a machine that will be "
            "built.", ha="center", va="center", fontsize=FS_BODY, color=NAVY,
            fontweight="bold")
    save(f, "hdl_not_program")


def design_complexity():
    f, ax, H = panel(4.10)

    chain = [("Fabrication\ntechnology\nimproves", TEAL),
             ("More transistors\nfit on\none chip", TEAL),
             ("Designs grow\nbigger and\nmore complex", AMBER),
             ("Manual design\nbecomes\nimpossible", RED),
             ("CAD tools\nbecome\nessential", VIOLET),
             ("CAD tools need\na language:\nan HDL", GREEN)]
    x = 2.2
    w = 14.6
    gap = 1.6
    top = H - 2.5
    bh = 13.5
    for i, (txt, col) in enumerate(chain):
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=2.0)
        box(ax, x, top - 1.6, w, 1.6, fc=col, ec=col, lw=0)
        ax.text(x + w / 2, top - bh / 2 - 0.6, txt, ha="center", va="center",
                fontsize=9.0, color=BODY, linespacing=1.7)
        if i < len(chain) - 1:
            arrow(ax, x + w + 0.25, top - bh / 2, x + w + gap - 0.25,
                  top - bh / 2, color=SLATE, lw=1.8, ms=10)
        x += w + gap

    y = top - bh - 3.4
    box(ax, 2.2, y - 13.4, 95.6, 13.4, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(5.0, y - 2.4, "And the requirements conflict with each other",
            ha="left", va="center", fontsize=FS_BODY, color=AMBER,
            fontweight="bold")
    _wrap(ax, 5.0, y - 5.6, 102,
          "Smaller area, higher speed, lower energy — you cannot have all "
          "three. Push on one and at least one of the others gets worse. "
          "That is why the design flow is not a recipe to follow but a series "
          "of engineering choices to make.", FS_SMALL, lh=2.8)
    save(f, "design_complexity")


def scale_compare():
    f, ax, H = panel(4.64)
    title(ax, 50, H - 3.5, "The two chips the lecturer puts side by side — and "
          "the factor between them", size=FS_SUB, color=SLATE, weight="normal")

    cards = [("FIRST COMMERCIAL\nPLANAR IC", "Fairchild Micrologic\nflip-flop, 1961",
              "about 4", "transistors", TEAL),
             ("A MODERN\nPROCESSOR", "Intel Core i7 (Nehalem)\nquad-core, 2008",
              "731 000 000", "transistors", NAVY),
             ("TODAY, FOR\nCOMPARISON", "Apple M1 Ultra,\n2022",
              "114 000 000 000", "transistors", VIOLET)]
    x = 2.5
    w = 30.3
    gap = 2.3
    top = H - 7
    bh = 17.5
    for head, sub, num, unit, col in cards:
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=2.0)
        box(ax, x, top - 5.4, w, 5.4, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.7, head, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=WHITE, fontweight="bold",
                linespacing=1.5)
        ax.text(x + w / 2, top - 8.2, sub, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=SLATE, linespacing=1.5)
        ax.text(x + w / 2, top - 12.6, num, ha="center", va="center",
                fontsize=FS_TITLE - 1.0, color=col, fontweight="bold")
        ax.text(x + w / 2, top - 15.6, unit, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=BODY)
        x += w + gap

    y = top - bh - 3.2
    box(ax, 2.5, y - 12.6, 95.5, 12.6, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(5.0, y - 2.2, "What that factor actually means for a designer",
            ha="left", va="center", fontsize=FS_BODY, color=NAVY,
            fontweight="bold")
    _wrap(ax, 5.0, y - 5.0, 102,
          "From 4 devices to 731 million is a factor of about 180 million. If "
          "you could place and wire one transistor per second, by hand, without "
          "ever sleeping, the Nehalem alone would take you about 23 years.",
          FS_SMALL, lh=2.8)
    save(f, "scale_compare")


# ---- real, widely published transistor counts --------------------------------
MOORE = [(1971, 2.3e3,   "Intel 4004", 1),
         (1978, 2.9e4,   "Intel 8086", 1),
         (1982, 1.34e5,  "80286", 1),
         (1985, 2.75e5,  "80386", 1),
         (1989, 1.18e6,  "80486", 1),
         (1993, 3.1e6,   "Pentium", 1),
         (1997, 7.5e6,   "Pentium II", 1),
         (2000, 4.2e7,   "Pentium 4", 1),
         (2006, 2.91e8,  "Core 2 Duo", 1),
         (2008, 7.31e8,  "Core i7 (Nehalem)", 1),
         (2012, 1.4e9,   "Ivy Bridge", 1),
         (2015, 5.56e9,  "Xeon Haswell-E5", 1),
         (2017, 1.92e10, "AMD Epyc", 0),
         (2019, 3.954e10, "Epyc Rome", 0),
         (2022, 1.14e11, "Apple M1 Ultra", 0)]


def moore_plot():
    f, ax = plt.subplots(figsize=(PW, 5.0))
    xs = [m[0] for m in MOORE]
    ys = [m[1] for m in MOORE]
    intel = [m[3] for m in MOORE]

    # the doubling-every-two-years reference line, anchored on the 4004
    ref_x = np.array([1970, 2023])
    ref_y = 2.3e3 * 2 ** ((ref_x - 1971) / 2.0)
    ax.plot(ref_x, ref_y, "--", color=SLATE, lw=1.6,
            label="doubling every 2 years (reference)")

    for (x, y, name, is_intel) in MOORE:
        ax.plot([x], [y], "o", ms=9,
                color=NAVY if is_intel else RED, zorder=5)
    ax.set_yscale("log")
    ax.set_xlim(1968, 2026)
    ax.set_ylim(1e3, 3e11)
    ax.set_xlabel("Year of introduction", fontsize=FS_BODY, color=BODY)
    ax.set_ylabel("Transistors per chip (log scale)", fontsize=FS_BODY,
                  color=BODY)
    ax.tick_params(labelsize=FS_SMALL - 0.5, colors=BODY)
    ax.grid(True, which="major", color=GRID, lw=0.9)
    ax.grid(True, which="minor", color="#EDF1F5", lw=0.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(GRID)

    ann = {"Intel 4004": (10, -4), "Pentium": (-20, 18),
           "Core i7 (Nehalem)": (-122, -4), "Apple M1 Ultra": (-104, 10),
           "Xeon Haswell-E5": (-116, 14)}
    for (x, y, name, is_intel) in MOORE:
        if name in ann:
            dx, dy = ann[name]
            ax.annotate(name, (x, y), textcoords="offset points",
                        xytext=(dx, dy), fontsize=FS_SMALL - 1.0,
                        color=NAVY if is_intel else RED, fontweight="bold")
    ax.plot([], [], "o", color=NAVY, ms=9, label="Intel processors")
    ax.plot([], [], "o", color=RED, ms=9, label="other manufacturers")
    ax.legend(loc="upper left", fontsize=FS_SMALL - 0.5, frameon=False)
    ax.set_title("Moore's Law — Measured, Not Predicted",
                 fontsize=FS_TITLE, color=NAVY, fontweight="bold", pad=14)
    save(f, "moore_plot")


def moore_economics():
    f, ax, H = panel(5.00)

    cols = [("WHAT MOORE ACTUALLY SAID",
             "In 1965 Gordon Moore looked at four data points and saw "
             "components per chip doubling every year. In 1975 he revised it to "
             "every two years. It was a note on what the industry had been "
             "doing.", TEAL),
            ("WHY IT KEPT COMING TRUE",
             "Because it became a target. Equipment makers, materials suppliers "
             "and chip companies all planned around it, so the investment "
             "arrived on schedule. A self-fulfilling forecast.", VIOLET),
            ("WHY IT IS SLOWING",
             "Transistors are now a few tens of atoms across. Leakage, heat and "
             "the cost of each new fab rise faster than the gain. The answer "
             "has shifted to chiplets, 3-D stacking and accelerators.", AMBER)]
    x = 2.5
    w = 31.0
    gap = 1.75
    top = H - 1.5
    bh = 25.0
    for head, body, col in cols:
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.4, w, 4.4, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.2, head, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        _wrap(ax, x + 1.9, top - 6.6, 33, body, FS_SMALL - 1.0, lh=2.8)
        x += w + gap

    y = top - bh - 2.8
    box(ax, 2.5, y - 12.6, 95.5, 12.6, fc=LIGHT, ec=NAVY, lw=1.6)
    _wrap(ax, 5.0, y - 3.6, 104,
          "For this course the point is simply this: the number of things on a "
          "chip grew far faster than any human's ability to place them. "
          "Everything that follows — the flow, the tools, the language — exists "
          "to close that gap.", FS_SMALL, color=NAVY, lh=2.8)
    save(f, "moore_economics")


def tech_ladder():
    f, ax, H = panel(4.90)

    stages = [("PLANAR CMOS", "down to ~22 nm",
               "The gate sits flat on top of the channel. Simple, and the "
               "workhorse of the industry for forty years.", TEAL),
              ("FinFET", "22 nm → 5 nm",
               "The channel is raised into a fin, so the gate wraps it on "
               "three sides. Far better control of leakage.", VIOLET),
              ("GATE-ALL-AROUND", "3 nm → 2 nm, now",
               "Stacked nanosheets with the gate wrapped completely around "
               "them. In volume production today.", GREEN),
              ("QUANTUM?", "not yet — and not\na replacement",
               "A different kind of machine for a different kind of problem, "
               "not a smaller version of this one.", SLATE)]
    x = 2.5
    w = 23.0
    gap = 1.6
    top = H - 1.6
    bh = 22.0
    for i, (head, node, body, col) in enumerate(stages):
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.2, w, 4.2, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.1, head, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        ax.text(x + w / 2, top - 7.4, node, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=col, fontweight="bold",
                linespacing=1.6)
        _wrap(ax, x + w / 2, top - 12.0, 32, body, FS_SMALL - 1.5, ha="center",
              lh=2.6)
        if i < len(stages) - 1:
            arrow(ax, x + w + 0.25, top - bh / 2, x + w + gap - 0.25,
                  top - bh / 2, color=SLATE, lw=1.8, ms=10)
        x += w + gap

    _note(ax, 2.5, top - bh - 2.8, 95.5,
          "A note on the numbers in the original slide",
          "The lecture says \"CMOS up to 22 nm, FinFET 14 nm\" — correct when "
          "it was recorded. Those node names are now marketing labels rather "
          "than measurements: no feature on a \"3 nm\" chip is 3 nm across. "
          "What has not changed at all is the design flow.",
          col=AMBER, fill="#FFF7EC", chars=104)
    save(f, "tech_ladder")


def feature_size():
    f, ax, H = panel(5.14)
    title(ax, 50, H - 3.5, "A sense of scale, so the node numbers mean something "
          "physical", size=FS_SUB, color=SLATE, weight="normal")

    rows = [("A human hair", "about 70 000 nm wide", 42.0, SLATE),
            ("A red blood cell", "about 7 000 nm across", 30.0, SLATE),
            ("Visible light", "400 – 700 nm wavelength", 19.5, AMBER),
            ("A 22 nm transistor gate", "the lecture's \"state of the art\"",
             9.0, TEAL),
            ("A silicon atom", "about 0.2 nm across", 2.6, RED)]
    y = H - 6.6
    rh = 4.0
    for name, val, barlen, col in rows:
        ax.text(2.5, y - rh / 2, name, ha="left", va="center",
                fontsize=FS_SMALL, color=NAVY, fontweight="bold")
        ax.text(28.5, y - rh / 2, val, ha="left", va="center",
                fontsize=FS_SMALL - 0.5, color=BODY)
        box(ax, 54.0, y - rh / 2 - 1.1, barlen, 2.2, fc=col, ec=col, lw=0, r=0.5)
        y -= rh
    ax.text(54.0, y - 0.6, "(bar lengths are illustrative — the real range spans "
            "five orders of magnitude)", ha="left", va="center",
            fontsize=FS_SMALL - 1.8, color=SLATE, fontstyle="italic")

    _note(ax, 2.5, y - 4.4, 95.5,
          "So a 22 nm gate is roughly 100 silicon atoms across",
          "At that size a handful of stray atoms changes a transistor's "
          "behaviour. That is why fabrication is statistical, why every chip is "
          "tested individually, and why the flow verifies at every level.",
          col=NAVY, chars=104)
    save(f, "feature_size")


def tradeoff_triangle():
    f, ax, H = panel(4.60)
    title(ax, 50, H - 3.5, "\"Often these requirements are conflicting. If you "
          "try to optimize one you may make the other one worse.\"",
          size=FS_SUB, color=SLATE, weight="normal")

    cx, cy, r = 23.0, (H - 13.0) / 2.0 + 1.0, 9.5
    pts = [(cx, cy + r), (cx - r * 0.95, cy - r * 0.58),
           (cx + r * 0.95, cy - r * 0.58)]
    labels = [("AREA", "how much silicon it costs", TEAL),
              ("SPEED", "how fast the clock\ncan run", VIOLET),
              ("POWER", "how much energy\neach result costs", AMBER)]
    ax.add_patch(Polygon(pts, fc="#F4F8FB", ec=NAVY, lw=2.0, zorder=2))
    for (px, py), (lab, sub, col) in zip(pts, labels):
        ax.add_patch(Circle((px, py), 3.9, fc=col, ec=WHITE, lw=2.0, zorder=5))
        ax.text(px, py, lab, ha="center", va="center", fontsize=FS_SMALL - 1.0,
                color=WHITE, fontweight="bold", zorder=6)
        if py > cy:
            ax.text(px, py + 5.8, sub, ha="center", va="center",
                    fontsize=FS_SMALL - 1.5, color=col, zorder=6)
        else:
            ax.text(px, py - 6.8, sub, ha="center", va="center",
                    fontsize=FS_SMALL - 1.5, color=col, linespacing=1.6,
                    zorder=6)

    rows = [("Want less AREA?", "Share one adder between several operations — "
             "so the job now takes more clock cycles. Speed falls.", TEAL),
            ("Want more SPEED?", "Add pipeline registers, or duplicate logic so "
             "it runs in parallel. Area rises, and so does switching power.",
             VIOLET),
            ("Want less POWER?", "Lower the supply voltage, or gate the clock. "
             "Gates get slower, and the control logic gets bigger.", AMBER)]
    x0 = 46.0
    y = H - 9.0
    rh = 9.0
    for head, body, col in rows:
        box(ax, x0, y - rh, 52.0, rh, fc=WHITE, ec=col, lw=1.5)
        box(ax, x0, y - rh, 1.3, rh, fc=col, ec=col, lw=0, r=0.4)
        ax.text(x0 + 3.4, y - 2.4, head, ha="left", va="center",
                fontsize=FS_SMALL, color=col, fontweight="bold")
        _wrap(ax, x0 + 3.4, y - 5.2, 56, body, FS_SMALL - 1.0, lh=2.7)
        y -= rh + 1.0
    save(f, "tradeoff_triangle")


def manual_impossible():
    f, ax, H = panel(4.50)

    steps = [("731 000 000", "transistors in the\nNehalem die", NAVY),
             ("÷ 1 per second", "an impossibly fast\nhuman designer", SLATE),
             ("= 23 years", "of continuous work,\nwithout sleeping", RED),
             ("and then", "one specification change\nand you start again",
              AMBER)]
    x = 2.5
    w = 23.0
    gap = 1.6
    top = H - 2
    bh = 14.0
    for i, (big, sub, col) in enumerate(steps):
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        ax.text(x + w / 2, top - 5.2, big, ha="center", va="center",
                fontsize=FS_TITLE - 2.0, color=col, fontweight="bold")
        ax.text(x + w / 2, top - 10.2, sub, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=BODY, linespacing=1.6)
        if i < len(steps) - 1:
            arrow(ax, x + w + 0.25, top - bh / 2, x + w + gap - 0.25,
                  top - bh / 2, color=SLATE, lw=1.8, ms=10)
        x += w + gap

    y = _note(ax, 2.5, top - bh - 3.0, 95.5, "So the job changed",
              "A VLSI designer does not place transistors. A designer writes a "
              "DESCRIPTION of what the circuit must do, and a program turns "
              "that description into transistors.", col=TEAL, chars=104)
    ax.text(5.1, y - 3.2, "That program is a CAD tool. The description is "
            "written in a hardware description language.", ha="left",
            va="center", fontsize=FS_SMALL, color=NAVY, fontweight="bold")
    ax.text(5.1, y - 6.2, "That is the whole reason this course exists.",
            ha="left", va="center", fontsize=FS_SMALL, color=NAVY,
            fontweight="bold")
    save(f, "manual_impossible")


if __name__ == "__main__":
    objectives()
    hdl_not_program()
    design_complexity()
    scale_compare()
    moore_plot()
    moore_economics()
    tech_ladder()
    feature_size()
    tradeoff_triangle()
    manual_impossible()
