# -*- coding: utf-8 -*-
"""Topic 6 diagrams — constraints: telling the tool what you meant."""
import _boot
from dsl import *


# ------------------------------------------------------- why constrain at all
def why_constrain():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 53.9
    title(ax, 50, H - 3, "A tool with no constraints is not being careful - it is being blind", 12)
    ax.text(50, H - 7.2, "Synthesis and place-and-route optimise for the goal you give them. "
                         "No goal, no optimisation.",
            fontsize=9, color=SLATE, ha="center")

    ytop = H - 11.5
    bh = 21.0
    box(ax, 4, ytop - bh, 44, bh, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(26, ytop - 4.0, "WITHOUT constraints", fontsize=10.5, color=RED, ha="center",
            fontweight="bold")
    for i, ln in enumerate(["the tool assumes an infinitely fast clock",
                            "every path is \"good enough\" - none is worked on",
                            "the report says MET because nothing was checked",
                            "the chip fails on the bench, not on the screen"]):
        ax.text(7.5, ytop - 8.8 - i * 3.4, "-  " + ln, fontsize=8.6, color=BODY, ha="left")

    box(ax, 52, ytop - bh, 44, bh, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(74, ytop - 4.0, "WITH constraints", fontsize=10.5, color=GREEN, ha="center",
            fontweight="bold")
    for i, ln in enumerate(["the tool knows the target period",
                            "it spends effort on the paths that fail",
                            "the report is a real prediction of silicon",
                            "\"MET\" means something you can trust"]):
        ax.text(55.5, ytop - 8.8 - i * 3.4, "-  " + ln, fontsize=8.6, color=BODY, ha="left")

    box(ax, 4, 3.0, 92, 12.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 12.0, "The constraint file is a specification, not a settings file", fontsize=10,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 8.0, "It says how fast the clock runs, when data arrives from outside, when it "
                     "must leave,\nand which paths are not real. Everything the timing report "
                     "says is downstream of it.",
            fontsize=8.8, color=BODY, ha="center")
    save(f, "why_constrain")


# ----------------------------------------------------------------- the SDC map
def sdc_map():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Four questions - and the constraint that answers each", 12.5)

    ytop = H - 9.0
    items = [("1", "How fast does\nthe clock run?", "create_clock -period 10 \\\n"
              "    -name clk [get_ports clk]", TEAL),
             ("2", "When does data\narrive from outside?", "set_input_delay 3.0 \\\n"
              "    -clock clk [get_ports din*]", NAVY),
             ("3", "When must data\nleave the chip?", "set_output_delay 2.5 \\\n"
              "    -clock clk [get_ports dout*]", VIOLET),
             ("4", "Which paths are\nnot real?", "set_false_path / \\\n"
              "    set_multicycle_path", AMBER)]
    rh = 9.5
    y = ytop
    for n, q, code, col in items:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.5)
        ax.add_patch(Circle((10, y - rh / 2), 3.0, fc=col, ec=col, zorder=5))
        ax.text(10, y - rh / 2, n, ha="center", va="center", fontsize=10, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(16.5, y - rh / 2, q, ha="left", va="center", fontsize=9.2, color=col,
                fontweight="bold")
        ax.text(47, y - rh / 2, code, ha="left", va="center", fontsize=8.4, color=BODY,
                family="monospace")
        y -= rh + 1.8

    ax.text(50, 5.4, "Every timing report you will ever read is an answer to these four questions.",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 2.0, "SDC is the vendor-neutral name (Synopsys Design Constraints). "
                     "Xilinx calls its version XDC - the timing commands are the same.",
            fontsize=8.4, color=SLATE, ha="center", fontstyle="italic")
    save(f, "sdc_map")


# --------------------------------------------------------------- create_clock
def create_clock_anatomy():
    W, Hin = 11.5, 6.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 52.2
    title(ax, 50, H - 3, "create_clock - the one constraint you cannot leave out", 12.5)

    ax.text(50, H - 9.0, "create_clock  -name sys_clk  -period 10.0  "
                         "-waveform {0 5}  [get_ports clk]",
            fontsize=10.5, color=NAVY, ha="center", family="monospace", fontweight="bold")

    parts = [("-name", "what the report calls it", 15.0, TEAL),
             ("-period", "10.0 ns  =  100 MHz", 34.0, RED),
             ("-waveform", "rise at 0, fall at 5\n(the duty cycle)", 56.0, VIOLET),
             ("[get_ports clk]", "the pin it enters on", 80.0, GREEN)]
    for nm, sub, x, col in parts:
        ax.plot([x, x], [H - 11.5, H - 15.0], color=col, lw=1.2)
        ax.text(x, H - 17.6, nm, fontsize=8.6, color=col, ha="center", fontweight="bold",
                family="monospace")
        ax.text(x, H - 21.2, sub, fontsize=8.2, color=BODY, ha="center")

    ctop = 15.5
    clk_wave(ax, 14, ctop, 26.0, 3, 5.5, color=NAVY, name="sys_clk")
    for k, x in enumerate([14, 40, 66, 92]):
        ax.plot([x, x], [ctop - 3.0, ctop + 6.0], color=GRID, lw=1.0, ls=":")
    arrow(ax, 14, ctop - 4.5, 40, ctop - 4.5, color=RED, lw=1.8, style="<|-|>")
    ax.text(27, ctop - 7.6, "period = 10.0 ns", fontsize=9, color=RED, ha="center",
            fontweight="bold")
    arrow(ax, 27, ctop + 8.0, 40, ctop + 8.0, color=VIOLET, lw=1.6, style="<|-|>")
    ax.text(33.5, ctop + 9.6, "high for 5.0 ns", fontsize=8.2, color=VIOLET, ha="center")

    ax.text(50, 3.0, "Get the period wrong and every number in the report is wrong "
                     "by the same amount.",
            fontsize=9, color=NAVY, ha="center", fontweight="bold")
    save(f, "create_clock_anatomy")


# ------------------------------------------------------------------ I/O delay
def io_delay():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "Input and output delay - the part of the path outside your chip", 12)
    ax.text(50, H - 7.2, "Your first flop is not the start of the path. The path started in "
                         "another chip.",
            fontsize=9, color=SLATE, ha="center")

    ymid = H - 22.6
    label_box(ax, 3, ymid, 17, 10.0, "UPSTREAM\nchip", fc="#F2F0FA", ec=VIOLET, tc=VIOLET,
              size=8.8, lw=1.6)
    box(ax, 27, ymid - 5.0, 46, 18.0, fc=LIGHT, ec=NAVY, lw=2.0)
    ax.text(50, ymid + 10.4, "YOUR CHIP", fontsize=9.4, color=NAVY, ha="center",
            fontweight="bold")
    label_box(ax, 30, ymid + 1.0, 14, 8.0, "first\nflop", fc=WHITE, ec=TEAL, tc=TEAL, size=8.4)
    label_box(ax, 56, ymid + 1.0, 14, 8.0, "last\nflop", fc=WHITE, ec=TEAL, tc=TEAL, size=8.4)
    arrow(ax, 44, ymid + 5.0, 56, ymid + 5.0, color=SLATE, lw=1.8)
    label_box(ax, 80, ymid, 17, 10.0, "DOWNSTREAM\nchip", fc="#F2F0FA", ec=VIOLET, tc=VIOLET,
              size=8.8, lw=1.6)

    arrow(ax, 20, ymid + 5.0, 30, ymid + 5.0, color=RED, lw=2.0)
    ax.text(23.5, ymid - 2.6, "3.0 ns", fontsize=8.6, color=RED, ha="center",
            fontweight="bold")
    arrow(ax, 70, ymid + 5.0, 80, ymid + 5.0, color=GREEN, lw=2.0)
    ax.text(76.5, ymid - 2.6, "2.5 ns", fontsize=8.6, color=GREEN, ha="center",
            fontweight="bold")

    box(ax, 4, 17.0, 44, 12.5, fc=WHITE, ec=RED, lw=1.5)
    ax.text(26, 26.0, "set_input_delay 3.0", fontsize=9.2, color=RED, ha="center",
            family="monospace", fontweight="bold")
    ax.text(26, 20.8, "\"the data leaves the other chip 3.0 ns\nafter the same clock edge, so I "
                      "only have\nperiod - 3.0 left for my own logic.\"",
            fontsize=8.2, color=BODY, ha="center")

    box(ax, 52, 17.0, 44, 12.5, fc=WHITE, ec=GREEN, lw=1.5)
    ax.text(74, 26.0, "set_output_delay 2.5", fontsize=9.2, color=GREEN, ha="center",
            family="monospace", fontweight="bold")
    ax.text(74, 20.8, "\"the next chip needs the data 2.5 ns\nbefore the edge, so I must be "
                      "finished\n2.5 ns early.\"",
            fontsize=8.2, color=BODY, ha="center")

    box(ax, 4, 2.5, 92, 10.5, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, 9.6, "The most common constraint bug in the world", fontsize=9.4, color=AMBER,
            ha="center", fontweight="bold")
    ax.text(50, 5.4, "Forget these two lines and every I/O path becomes UNCONSTRAINED. "
                     "The report shows no violation\nbecause it never looked. "
                     "Always check the unconstrained-endpoint count.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "io_delay")


# -------------------------------------------------------------- the I/O budget
def io_budget():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 53.9
    title(ax, 50, H - 3, "Where the 10 ns actually goes", 13)

    x0, wtot = 8, 84
    y = H - 22.0
    segs = [("input\ndelay", 3.0, RED), ("your logic\n(what is left)", 4.5, TEAL),
            ("output\ndelay", 2.5, GREEN)]
    x = x0
    for nm, ns, col in segs:
        w = wtot * ns / 10.0
        box(ax, x, y, w, 9.0, fc=col, ec=col, r=0.5)
        ax.text(x + w / 2, y + 4.5, nm, ha="center", va="center", fontsize=8.6, color=WHITE,
                fontweight="bold")
        ax.text(x + w / 2, y - 3.2, "%.1f ns" % ns, ha="center", fontsize=9, color=col,
                fontweight="bold")
        x += w
    arrow(ax, x0, y + 13.0, x0 + wtot, y + 13.0, color=NAVY, lw=1.8, style="<|-|>")
    ax.text(50, y + 15.0, "clock period = 10.0 ns", ha="center", fontsize=9.4, color=NAVY,
            fontweight="bold")

    box(ax, 4, 3.0, 92, 17.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 17.0, "Read that middle bar again", fontsize=9.6, color=NAVY, ha="center",
            fontweight="bold")
    ax.text(50, 12.0, "You asked for 100 MHz, but your own logic only gets 4.5 ns - "
                      "the I/O ate more than half the cycle.",
            fontsize=8.8, color=BODY, ha="center")
    ax.text(50, 7.6, "If the design will not close, look here before you touch the RTL. "
                     "Registering the pins moves the\nI/O delay into its own cycle and hands "
                     "the whole 10 ns back to the logic.",
            fontsize=8.6, color=GREEN, ha="center")
    save(f, "io_budget")


# ----------------------------------------------------------------- exceptions
def timing_exceptions():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "Exceptions - telling the tool a path is not what it looks like", 12)
    ax.text(50, H - 7.2, "By default the tool checks EVERY path in one cycle. Sometimes that "
                         "is simply not the design.",
            fontsize=9, color=SLATE, ha="center")

    ytop = H - 11.0
    bh = 17.0
    box(ax, 4, ytop - bh, 44, bh, fc=WHITE, ec=AMBER, lw=1.7)
    ax.text(26, ytop - 4.0, "set_false_path", fontsize=10, color=AMBER, ha="center",
            family="monospace", fontweight="bold")
    ax.text(26, ytop - 8.0, "\"do not check this path at all\"", fontsize=8.6, color=AMBER,
            ha="center", fontstyle="italic")
    ax.text(26, ytop - 13.0, "a reset that is only ever released,\na test-mode pin, a path "
                             "that cannot\nphysically be exercised",
            fontsize=8.2, color=BODY, ha="center")

    box(ax, 52, ytop - bh, 44, bh, fc=WHITE, ec=VIOLET, lw=1.7)
    ax.text(74, ytop - 4.0, "set_multicycle_path", fontsize=10, color=VIOLET, ha="center",
            family="monospace", fontweight="bold")
    ax.text(74, ytop - 8.0, "\"this one gets N cycles, not one\"", fontsize=8.6, color=VIOLET,
            ha="center", fontstyle="italic")
    ax.text(74, ytop - 13.0, "a wide multiply whose result is only\nread every fourth cycle, "
                             "a slow\nconfiguration register",
            fontsize=8.2, color=BODY, ha="center")

    box(ax, 4, 15.0, 92, 15.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 26.6, "An exception is a PROMISE, and the tool believes you", fontsize=9.8,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 21.5, "set_false_path on a path that IS real removes the only check that "
                      "would have caught the bug.\nThe report goes green and the silicon "
                      "goes wrong. This is how real chips die.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 16.8, "Write the exception only when you can say, in one sentence, why the "
                      "path cannot matter.",
            fontsize=8.6, color=RED, ha="center", fontstyle="italic")

    ax.text(50, 10.0, "set_multicycle_path 4 -setup -from [get_cells a_q*] -to [get_cells acc*]",
            fontsize=9, color=NAVY, ha="center", family="monospace")
    ax.text(50, 6.4, "set_multicycle_path 3 -hold  -from [get_cells a_q*] -to [get_cells acc*]",
            fontsize=9, color=NAVY, ha="center", family="monospace")
    ax.text(50, 2.6, "The hold number is almost always N-1. Forget the hold line and you have "
                     "just created a hold violation.",
            fontsize=8.4, color=RED, ha="center", fontweight="bold")
    save(f, "timing_exceptions")


# --------------------------------------------------------- multicycle in time
def multicycle_waves():
    W, Hin = 11.5, 5.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 50.4
    title(ax, 50, H - 3, "What \"multicycle 4\" changes: which edge does the capturing", 12)

    x0, per = 12, 20.0
    ctop = H - 15.0
    clk_wave(ax, x0, ctop, per, 4, 5.0, color=NAVY, name="clk")
    for k in range(5):
        x = x0 + k * per
        ax.plot([x, x], [8.0, ctop + 6.0], color=GRID, lw=0.9, ls=":")
        ax.text(x, ctop + 7.0, "edge %d" % k, fontsize=7.6, color=SLATE, ha="center")

    ylaunch = ctop - 8.0
    ax.text(x0 - 1.5, ylaunch, "launch", fontsize=8.6, color=TEAL, ha="right", va="center",
            fontweight="bold")
    dot(ax, x0, ylaunch, color=TEAL, s=30)

    arrow(ax, x0, ylaunch - 6.0, x0 + per, ylaunch - 6.0, color=RED, lw=1.8, style="-|>")
    ax.text(x0 + per / 2, ylaunch - 9.0, "default: capture at edge 1\nyou get 10 ns",
            fontsize=8.2, color=RED, ha="center")

    arrow(ax, x0, ylaunch - 17.0, x0 + 4 * per, ylaunch - 17.0, color=GREEN, lw=2.2,
          style="-|>")
    ax.text(x0 + 2 * per, ylaunch - 20.0, "multicycle 4: capture at edge 4 - you get 40 ns",
            fontsize=8.6, color=GREEN, ha="center", fontweight="bold")

    ax.text(50, 4.0, "Nothing in the hardware changed. You told the tool the truth about when "
                     "the result is read.",
            fontsize=9, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 1.0, "The design must actually hold the input steady for those four cycles - "
                     "usually an enable on the capture flop.",
            fontsize=8.2, color=SLATE, ha="center", fontstyle="italic")
    save(f, "multicycle_waves")


# ------------------------------------------------------------ writing order
def sdc_checklist():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "The order to write a constraint file - and the order to debug it", 12)

    steps = [("1", "Define every clock", "create_clock for each primary clock; "
              "create_generated_clock\nfor anything a divider makes.", TEAL),
             ("2", "Add uncertainty", "set_clock_uncertainty for jitter and, before layout, "
              "for the\nskew the clock tree does not have yet.", VIOLET),
             ("3", "Constrain the I/O", "set_input_delay and set_output_delay on every port, "
              "against\nthe clock that samples it.", NAVY),
             ("4", "Only now, exceptions", "set_false_path and set_multicycle_path - each one "
              "justified in\na comment on the line above it.", AMBER),
             ("5", "Check for holes", "Report unconstrained endpoints. A clean report on a "
              "half-constrained\ndesign is worse than a failing one.", GREEN)]
    y = H - 9.5
    rh = 8.2
    for n, hd, sub, col in steps:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((9.5, y - rh / 2), 2.6, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - rh / 2, n, ha="center", va="center", fontsize=9.4, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(15, y - 2.9, hd, ha="left", fontsize=9.2, color=col, fontweight="bold")
        ax.text(15, y - 6.2, sub, ha="left", va="center", fontsize=8.1, color=BODY)
        y -= rh + 1.3

    box(ax, 4, 2.5, 92, 6.5, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 5.6, "When a timing report surprises you, suspect the constraints before "
                     "you suspect the RTL.",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    save(f, "sdc_checklist")


for fn in (why_constrain, sdc_map, create_clock_anatomy, io_delay, io_budget,
           timing_exceptions, multicycle_waves, sdc_checklist):
    fn()
