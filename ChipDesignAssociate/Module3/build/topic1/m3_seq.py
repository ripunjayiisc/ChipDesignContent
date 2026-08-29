# -*- coding: utf-8 -*-
"""Module 3 Topic 1 diagrams — sequential timing, races, Fmax."""
import _boot
from dsl import *


# --------------------------------------------------------------- races
def races():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 73.0
    title(ax, 50, H - 3, "A race: two state variables change, and the order is not fixed",
          12)
    ax.text(50, H - 7.2, "Hazards are about one output. Races are about the state a "
                         "machine lands in.",
            fontsize=9, color=SLATE, ha="center")

    ytop = H - 12.0
    ax.text(50, ytop, "present state 00, and an input change asks for state 11",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")

    yb = ytop - 8.0
    label_box(ax, 40, yb, 20, 8.0, "00", fc=WHITE, ec=NAVY, tc=NAVY, size=11, lw=2.0)
    label_box(ax, 8, yb - 16.0, 20, 8.0, "10", fc=LIGHT, ec=SLATE, tc=SLATE, size=11)
    label_box(ax, 72, yb - 16.0, 20, 8.0, "01", fc=LIGHT, ec=SLATE, tc=SLATE, size=11)
    label_box(ax, 40, yb - 30.0, 20, 8.0, "11", fc=WHITE, ec=GREEN, tc=GREEN,
              size=11, lw=2.0)

    arrow(ax, 42, yb, 24, yb - 8.0, color=VIOLET, lw=1.8)
    arrow(ax, 58, yb, 76, yb - 8.0, color=VIOLET, lw=1.8)
    arrow(ax, 22, yb - 16.0, 42, yb - 22.0, color=VIOLET, lw=1.8)
    arrow(ax, 78, yb - 16.0, 58, yb - 22.0, color=VIOLET, lw=1.8)
    ax.text(24, yb - 5.0, "if the first bit\nwins the race", fontsize=7.8,
            color=VIOLET, ha="center")
    ax.text(76, yb - 5.0, "if the second bit\nwins", fontsize=7.8, color=VIOLET,
            ha="center")

    box(ax, 4, 3.0, 44, 19.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(26, 19.6, "NON-CRITICAL race", fontsize=9.4, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(26, 13.0, "Both routes end up in 11.\nThe order changed the journey,\n"
                      "not the destination.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(26, 6.0, "Ugly, but it works.", fontsize=8.4, color=GREEN, ha="center",
            fontstyle="italic")

    box(ax, 52, 3.0, 44, 19.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(74, 19.6, "CRITICAL race", fontsize=9.4, color=RED, ha="center",
            fontweight="bold")
    ax.text(74, 13.0, "One route sticks in 10 or 01.\nThe machine ends up in a\n"
                      "different state depending on\nwhich gate was faster.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(74, 5.0, "A real bug, and delay-dependent.", fontsize=8.4, color=RED,
            ha="center", fontstyle="italic")
    save(f, "races")


def races_cure():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Why synchronous design makes races and hazards go away", 12)

    y = H - 11.0
    rows = [("Asynchronous circuit", "state changes whenever an input changes",
             "races and essential hazards are REAL and must be designed out", RED,
             "#FDECEF"),
            ("Synchronous circuit", "state changes only on a clock edge",
             "everything settles between edges; the clock is the referee", GREEN,
             "#EEF7F1")]
    rh = 14.0
    for nm, what, effect, col, fill in rows:
        box(ax, 4, y - rh, 92, rh, fc=fill, ec=col, lw=1.7)
        ax.text(8, y - 4.4, nm, fontsize=9.6, color=col, ha="left", fontweight="bold")
        ax.text(8, y - 8.2, what, fontsize=8.5, color=BODY, ha="left")
        ax.text(8, y - 11.4, effect, fontsize=8.5, color=col, ha="left",
                fontstyle="italic")
        y -= rh + 2.5

    box(ax, 4, 3.0, 92, 20.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 19.6, "Which is why this topic spends its time on setup and hold",
            fontsize=9.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 14.4, "In a synchronous design the question is never \"did it glitch?\" "
                      "- it is \"had it stopped glitching\nby the time the clock edge "
                      "arrived?\". That question is setup and hold, and it is what "
                      "STA answers.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 8.4, "The exceptions are the places with no clock to referee them: "
                     "logic that drives a clock, a latch\nenable, or an asynchronous "
                     "reset - and any genuinely asynchronous interface. "
                     "There, hazards\nare still yours to remove.",
            fontsize=8.6, color=AMBER, ha="center")
    save(f, "races_cure")


# ------------------------------------------------------ the sampling window
def setup_hold():
    W, Hin = 11.5, 6.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 57.4
    title(ax, 50, H - 3, "Sequential timing: the window a flip-flop needs", 12.5)
    ax.text(50, H - 7.4, "A flip-flop does not sample AT the edge. It samples over a "
                         "window around it.",
            fontsize=9, color=SLATE, ha="center")

    xe = 50.0
    ctop = H - 14.0
    clk_wave(ax, 12, ctop, 26.0, 3, 5.0, color=NAVY, name="clk")
    ax.plot([xe, xe], [20.0, ctop + 6.0], color=RED, lw=1.6, ls="--", zorder=6)

    su, hd = 12.0, 5.5
    wtop, wh = ctop - 6.0, 5.6
    box(ax, xe - su, wtop - wh, su, wh, fc="#FDECEF", ec=RED, lw=1.4)
    box(ax, xe, wtop - wh, hd, wh, fc="#FFF7EC", ec=AMBER, lw=1.4)
    ax.text(xe - su / 2, wtop - wh / 2, "SETUP", fontsize=9, color=RED, ha="center",
            va="center", fontweight="bold")
    ax.text(xe + hd / 2, wtop - wh / 2, "HOLD", fontsize=8.2, color=AMBER,
            ha="center", va="center", fontweight="bold")
    ax.text(xe - su - 1.5, wtop - wh / 2, "data must have ARRIVED", fontsize=8.2,
            color=RED, ha="right", va="center")
    ax.text(xe + hd + 1.5, wtop - wh / 2, "and must not CHANGE", fontsize=8.2,
            color=AMBER, ha="left", va="center")

    box(ax, 4, 3.0, 44, 15.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(26, 14.6, "SETUP violated", fontsize=9.4, color=RED, ha="center",
            fontweight="bold")
    ax.text(26, 9.0, "the data arrived too late.\nThe chip runs, but only at a\n"
                     "lower clock frequency.",
            fontsize=8.4, color=BODY, ha="center")

    box(ax, 52, 3.0, 44, 15.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(74, 14.6, "HOLD violated", fontsize=9.4, color=AMBER, ha="center",
            fontweight="bold")
    ax.text(74, 9.0, "the data changed too soon.\nThe chip does not work at\n"
                     "any clock frequency at all.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "setup_hold")


# --------------------------------------------------------------- Fmax
def fmax_derivation():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Maximum frequency of operation, derived", 13)

    y = H - 11.0
    steps = [("The data must arrive before the next edge needs it",
              "t_cq + t_logic  <=  T + t_skew - t_setup - t_unc", NAVY),
             ("Rearranged, that is the smallest period the design allows",
              "T  >=  t_cq + t_logic + t_setup + t_unc - t_skew", TEAL),
             ("And the fastest clock is one over that",
              "Fmax  =  1 / ( t_cq + t_logic + t_setup + t_unc - t_skew )", GREEN)]
    for hd, eq, col in steps:
        ax.text(50, y, hd, fontsize=9.2, color=col, ha="center", fontweight="bold")
        ax.text(50, y - 4.6, eq, fontsize=10.5, color=NAVY, ha="center",
                family="monospace")
        y -= 12.0

    box(ax, 4, 3.0, 92, 18.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 17.6, "t_logic is the LONGEST path, and only the longest one",
            fontsize=9.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 12.2, "Every other path in the design could be twice as fast and Fmax "
                      "would not move. That is why timing\nwork is always about one "
                      "path at a time - and why fixing it usually reveals the next one.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 6.0, "Note the sign on skew: a capture clock that arrives LATE gives "
                     "the data more time, so it raises\nFmax. It also eats your hold "
                     "margin by exactly the same amount.",
            fontsize=8.5, color=AMBER, ha="center")
    save(f, "fmax_derivation")


def fmax_one_stage():
    W, Hin = 11.5, 6.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 59.1
    title(ax, 50, H - 3, "Fmax is set by ONE stage - the measurement", 12.5)

    yb = H - 22.0
    stages = [("stage 1", "add", 2.0, TEAL), ("stage 2", "xor", 1.2, TEAL),
              ("stage 3", "16-bit multiply", 8.0, RED), ("stage 4", "add", 2.0, TEAL)]
    tot = sum(s[2] for s in stages)
    x = 8.0
    wtot = 84.0
    for nm, what, v, col in stages:
        w = wtot * v / tot
        box(ax, x, yb, w, 10.0, fc=col, ec=col, r=0.5)
        ax.text(x + w / 2, yb + 6.4, nm, ha="center", va="center", fontsize=8.4,
                color=WHITE, fontweight="bold")
        ax.text(x + w / 2, yb + 3.0, what, ha="center", va="center", fontsize=7.6,
                color=WHITE)
        x += w
    ax.text(50, yb + 13.0, "pipe_unbal - one stage carries most of the work",
            fontsize=9, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, yb - 4.0, "the clock has to fit the WIDEST box, not the average one",
            fontsize=8.6, color=RED, ha="center", fontstyle="italic")

    rows = [["pipe_unbal", "one heavy stage", "2.742 ns", "364.7 MHz"],
            ["pipe_bal", "heavy stage split in two", "2.113 ns", "473.2 MHz"]]
    table(ax, 8, yb - 8.0, ["design", "what changed", "longest path", "Fmax"],
          rows, [22, 32, 18, 18], 5.0, size=8.6, bold_col=[0, 3],
          colcolors={3: GREEN})

    box(ax, 4, 3.0, 92, 11.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 10.6, "1.30x the clock, from adding one register", fontsize=9.4,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 6.0, "Same arithmetic, same result, one more cycle of latency. "
                     "Nothing was made faster - the work\nwas just distributed so that "
                     "no single stage sets a slow speed limit for all of them.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "fmax_one_stage")


# -------------------------------------------------------- setup violation
def setup_violation():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "A real setup violation, and the fix that clears it", 12.5)
    ax.text(50, H - 7.2, "Same constraint file, same 400 MHz target, two versions of "
                         "the same design.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["pipe_unbal", "400 MHz", "-0.322 ns", "VIOLATED"],
            ["pipe_bal", "400 MHz", "+0.307 ns", "MET"]]
    table(ax, 10, H - 11.0, ["design", "target", "worst slack", "verdict"],
          rows, [24, 18, 20, 18], 5.4, size=9.2, bold_col=[0, 2],
          colcolors={3: NAVY})

    box(ax, 4, 15.0, 92, 15.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 27.0, "Read the two slack numbers as a fraction of the period",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 21.4, "The period is 2.5 ns. -0.322 ns is 13% over budget - too much "
                      "for a synthesis option to find,\nand about right for one "
                      "pipeline cut. That arithmetic tells you which fix to reach for "
                      "before\nyou try any of them.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 4, 2.5, 92, 10.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 9.6, "The fix was not a faster tool setting. It was one more register.",
            fontsize=9.2, color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 5.0, "Splitting the heavy stage moved the whole design from failing to "
                     "passing, at the same frequency.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "setup_violation")


# --------------------------------------------------------- hold violation
def hold_violation():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "Hold does not care what the clock period is", 12.5)
    ax.text(50, H - 7.4, "The same design analysed at three wildly different "
                         "frequencies.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["4.0 ns", "250 MHz", "-0.119 ns", "VIOLATED"],
            ["40.0 ns", "25 MHz", "-0.119 ns", "VIOLATED"],
            ["400.0 ns", "2.5 MHz", "-0.119 ns", "VIOLATED"]]
    table(ax, 12, H - 11.0, ["clock period", "frequency", "hold slack", "verdict"],
          rows, [20, 18, 20, 18], 4.8, size=9.0, bold_col=[0, 2],
          colcolors={2: RED})

    box(ax, 4, 20.0, 92, 12.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 29.0, "A hundred-fold change in frequency. No change at all in the "
                      "violation.", fontsize=9.4, color=RED, ha="center",
            fontweight="bold")
    ax.text(50, 24.0, "Both flops are triggered by the SAME edge, so the period never "
                      "enters the race. This is a\nfunctional failure, not a "
                      "performance one - the chip is broken at every speed.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 4, 3.0, 92, 14.5, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 14.0, "So the fix is the clock tree, or the data path - never the clock "
                      "frequency", fontsize=9.4, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(50, 9.2, "Rebalancing the tree so the capture register sees 0.10 ns of skew "
                     "instead of 0.25 ns:",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.2, "-0.119 ns VIOLATED   ->   +0.031 ns MET",
            fontsize=9.6, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    save(f, "hold_violation")


def hold_why_late():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "Why hold violations turn up so late in a project", 12.5)

    y = H - 10.0
    stages = [("RTL and synthesis", "no clock tree exists at all, so skew is zero",
               "hold passes trivially - and means nothing", TEAL),
              ("Clock-tree synthesis", "the tree is built; real skew appears",
               "hold violations arrive, often in their hundreds", RED),
              ("Place and route", "buffers inserted on the offending data paths",
               "hold closes; setup gets slightly worse", GREEN)]
    rh = 11.5
    for nm, what, effect, col in stages:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.6)
        ax.text(8, y - 3.8, nm, fontsize=9.4, color=col, ha="left", fontweight="bold")
        ax.text(8, y - 7.0, what, fontsize=8.4, color=BODY, ha="left")
        ax.text(8, y - 9.8, effect, fontsize=8.4, color=col, ha="left",
                fontstyle="italic")
        y -= rh + 2.0

    box(ax, 4, 3.0, 92, 10.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 10.0, "This is normal, and it is why hold is a layout problem more "
                      "often than an RTL one", fontsize=9.2, color=NAVY, ha="center",
            fontweight="bold")
    ax.text(50, 5.4, "What RTL can do is not make it impossible: no hand-gated clocks, "
                     "no unsynchronised crossings,\nno logic on an asynchronous reset.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "hold_why_late")


def sta_blind_to_hazards():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Two tools, one circuit, two different questions", 12.5)

    y = H - 10.0
    cols = [("STATIC TIMING ANALYSIS", "sta/sta.py, PrimeTime, Vivado",
             ["How long is the longest path?",
              "How long is the shortest path?",
              "Does every path fit in a clock cycle?"],
             ["sees setup and hold violations",
              "is BLIND to every hazard"], TEAL, "#F4F8FB"),
            ("GATE-LEVEL SIMULATION", "iverilog with delays",
             ["What does the output do over time?",
              "Does it pass through a wrong value?",
              "How many times does it change?"],
             ["sees every glitch you stimulate",
              "misses any path you never exercise"], VIOLET, "#F2F0FA")]
    bw = 44.0
    for i, (nm, tool, qs, verdicts, col, fill) in enumerate(cols):
        x = 4 + i * 48
        box(ax, x, y - 30.0, bw, 30.0, fc=fill, ec=col, lw=1.7)
        box(ax, x, y - 6.0, bw, 6.0, fc=col, ec=col)
        ax.text(x + bw / 2, y - 3.0, nm, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, y - 9.0, tool, ha="center", fontsize=8.0, color=SLATE,
                fontstyle="italic")
        yy = y - 13.0
        for q in qs:
            ax.text(x + 2.5, yy, "• " + q, fontsize=8.0, color=BODY, ha="left")
            yy -= 3.4
        yy -= 1.2
        for v in verdicts:
            ax.text(x + 2.5, yy, v, fontsize=8.0, color=col, ha="left",
                    fontweight="bold")
            yy -= 3.4

    box(ax, 4, 3.0, 92, 18.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 17.6, "Neither tool is a superset of the other", fontsize=9.6,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 12.4, "Run STA on hz_static1.v and every path meets timing, because "
                      "every path does meet timing.\nThe glitch is still there. "
                      "Run a zero-delay RTL simulation and the glitch is not there "
                      "either,\nbecause zero-delay simulation has no delays to race.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 5.0, "You need the delay-annotated simulation for hazards, and STA for "
                     "setup and hold. That is why this\nlab uses both on the same "
                     "circuit.",
            fontsize=8.6, color=NAVY, ha="center", fontweight="bold")
    save(f, "sta_blind_to_hazards")


for fn in (races, races_cure, setup_hold, fmax_derivation, fmax_one_stage,
           setup_violation, hold_violation, hold_why_late, sta_blind_to_hazards):
    fn()
