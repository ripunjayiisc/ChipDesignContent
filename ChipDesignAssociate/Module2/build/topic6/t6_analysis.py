# -*- coding: utf-8 -*-
"""Topic 6 diagrams — how static timing analysis actually works."""
import _boot
from dsl import *


# --------------------------------------------------------- STA vs simulation
def sta_vs_sim():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Why STA replaced timing simulation", 13)

    ytop = H - 8.5
    bh = 29.0
    box(ax, 4, ytop - bh, 44, bh, fc=WHITE, ec=AMBER, lw=1.7)
    ax.text(26, ytop - 4.2, "TIMING SIMULATION", fontsize=10, color=AMBER, ha="center",
            fontweight="bold")
    ax.text(26, ytop - 8.0, "runs vectors through a delay model", fontsize=8.4, color=SLATE,
            ha="center", fontstyle="italic")
    for dy, ln in zip([0.0, 4.4, 10.6, 15.0],
                      ["needs stimulus you have to write",
                       "only checks the paths your vectors\nhappen to exercise",
                       "slow - hours for a medium design",
                       "silent about the path you forgot"]):
        ax.text(7.0, ytop - 12.5 - dy, "-  " + ln, fontsize=8.3, color=BODY, ha="left",
                va="top")

    box(ax, 52, ytop - bh, 44, bh, fc=WHITE, ec=GREEN, lw=1.7)
    ax.text(74, ytop - 4.2, "STATIC TIMING ANALYSIS", fontsize=10, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(74, ytop - 8.0, "walks the graph, no vectors at all", fontsize=8.4, color=SLATE,
            ha="center", fontstyle="italic")
    for dy, ln in zip([0.0, 4.4, 10.6, 15.0],
                      ["no stimulus needed",
                       "checks EVERY path, exhaustively",
                       "seconds to minutes",
                       "tells you the worst one by name"]):
        ax.text(55.0, ytop - 12.5 - dy, "-  " + ln, fontsize=8.3, color=BODY, ha="left",
                va="top")

    box(ax, 4, 3.0, 92, 17.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 17.0, "\"Static\" means it does not care what the values are", fontsize=9.8,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 12.2, "STA never asks whether a path can be activated - only how long it is. "
                      "That is its strength\n(nothing is missed) and its one weakness "
                      "(a path that can never switch is still reported).",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 6.0, "The paths that can never switch are called FALSE PATHS. "
                     "Removing them is your job, not the tool's -\nwhich is exactly why "
                     "set_false_path exists.",
            fontsize=8.5, color=TEAL, ha="center")
    save(f, "sta_vs_sim")


# ------------------------------------------------------------ the timing graph
def timing_graph():
    W, Hin = 11.5, 6.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 57.4
    title(ax, 50, H - 3, "Step 1 - the netlist becomes a graph of delays", 12.5)
    ax.text(50, H - 7.2, "Every pin is a node. Every cell and every wire is an edge with a "
                         "number on it.",
            fontsize=9, color=SLATE, ha="center")

    yc = H - 21.0                            # the centre line everything sits on
    label_box(ax, 4, yc - 4.5, 12, 9.0, "FF1", fc=WHITE, ec=NAVY, tc=NAVY, size=9)
    gA = gate(ax, "and", 25, yc, 8.0, 7.0, ec=TEAL)
    gX = gate(ax, "xor", 45, yc, 8.0, 7.0, ec=TEAL)
    gO = gate(ax, "or", 64, yc, 8.0, 7.0, ec=TEAL)
    label_box(ax, 84, yc - 4.5, 12, 9.0, "FF2", fc=WHITE, ec=NAVY, tc=NAVY, size=9)

    arrow(ax, 16, yc, gA[0][0][0], yc, color=SLATE, lw=1.5)
    arrow(ax, gA[1][0], yc, gX[0][0][0], yc, color=SLATE, lw=1.5)
    arrow(ax, gX[1][0], yc, gO[0][0][0], yc, color=SLATE, lw=1.5)
    arrow(ax, gO[1][0], yc, 84, yc, color=SLATE, lw=1.5)

    labs = [(10, "clock-to-Q\n0.145", VIOLET), (29, "AND2\n0.062", TEAL),
            (49, "XOR2\n0.088", TEAL), (68, "OR2\n0.041", TEAL),
            (90, "setup\n0.090", RED)]
    for x, t, col in labs:
        ax.text(x, yc + 7.0, t, fontsize=8.2, color=col, ha="center", va="bottom",
                fontweight="bold")

    ax.text(50, yc - 10.5, "arrival at FF2/D  =  0.145 + 0.062 + 0.088 + 0.041  =  0.336 ns",
            fontsize=9.4, color=NAVY, ha="center", family="monospace", fontweight="bold")

    box(ax, 4, 3.0, 92, 20.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 19.8, "Three rules that make the whole thing work", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    for i, (n, ln) in enumerate([
            ("1", "Arrival time flows FORWARD. At a node with several inputs, "
                  "keep the LATEST (for setup)."),
            ("2", "Required time flows BACKWARD from the capture flop, "
                  "starting at period - setup."),
            ("3", "slack = required - arrival, computed at every endpoint. "
                  "Negative means it does not fit.")]):
        ax.text(7.5, 15.0 - i * 4.2, n + ".", fontsize=8.8, color=TEAL, ha="left",
                fontweight="bold")
        ax.text(11.5, 15.0 - i * 4.2, ln, fontsize=8.5, color=BODY, ha="left")
    save(f, "timing_graph")


# --------------------------------------------------- arrival / required / slack
def arrival_required():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "Step 2 - two sweeps, then one subtraction", 12.5)

    yA = H - 12.0
    ax.text(4, yA + 4.0, "FORWARD SWEEP - arrival time", fontsize=9.6, color=TEAL, ha="left",
            fontweight="bold")
    xs = [10, 30, 50, 70, 90]
    vals = ["0.000", "0.145", "0.207", "0.295", "0.336"]
    for i, (x, v) in enumerate(zip(xs, vals)):
        ax.add_patch(Circle((x, yA - 3.5), 3.4, fc=TEAL if i else NAVY, ec="none", zorder=4))
        ax.text(x, yA - 3.5, v, ha="center", va="center", fontsize=7.4, color=WHITE,
                fontweight="bold", zorder=5)
        if i:
            arrow(ax, xs[i - 1] + 3.6, yA - 3.5, x - 3.6, yA - 3.5, color=TEAL, lw=1.6)
    ax.text(10, yA - 9.0, "clk edge", fontsize=7.8, color=SLATE, ha="center")
    ax.text(90, yA - 9.0, "FF2/D", fontsize=7.8, color=SLATE, ha="center")
    ax.text(50, yA - 9.0, "each node keeps the LATEST arrival that reaches it", fontsize=8.2,
            color=TEAL, ha="center", fontstyle="italic")

    yR = H - 30.0
    ax.text(4, yR + 4.0, "BACKWARD SWEEP - required time", fontsize=9.6, color=GREEN, ha="left",
            fontweight="bold")
    rvals = ["0.624", "0.769", "0.831", "0.919", "0.960"]
    for i, (x, v) in enumerate(zip(xs, rvals)):
        ax.add_patch(Circle((x, yR - 3.5), 3.4, fc=GREEN if i < 4 else NAVY, ec="none",
                            zorder=4))
        ax.text(x, yR - 3.5, v, ha="center", va="center", fontsize=7.4, color=WHITE,
                fontweight="bold", zorder=5)
        if i:
            arrow(ax, x - 3.6, yR - 3.5, xs[i - 1] + 3.6, yR - 3.5, color=GREEN, lw=1.6)
    ax.text(90, yR - 9.0, "period 1.05 - setup 0.09 = 0.960", fontsize=8.2, color=GREEN,
            ha="right", fontstyle="italic")
    ax.text(10, yR - 9.0, "each node keeps the EARLIEST it is needed", fontsize=8.2,
            color=GREEN, ha="left", fontstyle="italic")

    box(ax, 4, 3.0, 92, 18.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 18.6, "and now the subtraction, at the endpoint", fontsize=9.6, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(50, 13.0, "slack  =  required 0.960  -  arrival 0.336  =  +0.624 ns   MET",
            fontsize=11, color=NAVY, ha="center", family="monospace", fontweight="bold")
    ax.text(50, 7.4, "Do that at every endpoint and you have the whole report. "
                     "The worst answer is the WNS.\nA design with a million flops is "
                     "a million of these subtractions - which is why STA is fast.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "arrival_required")


# ---------------------------------------------------------- reading the report
def report_anatomy():
    W, Hin = 11.5, 6.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 59.1
    title(ax, 50, H - 3, "Reading a timing report - it is always the same six things", 12.5)

    lines = [
        ("Startpoint: a_q[3]_reg  (rising edge-triggered by clk)", NAVY, 1),
        ("Endpoint:   acc[7]_reg  (rising edge-triggered by clk)", NAVY, 1),
        ("Path Group: clk        Path Type: max (setup)", SLATE, 0),
        ("", BODY, 0),
        ("  incr    arrival   point", SLATE, 1),
        ("  0.000   0.000     clock clk (rise edge)", BODY, 0),
        ("  0.145   0.145     a_q[3]_reg/Q     (DFF)", BODY, 0),
        ("  0.117   0.262     u21/Y            (XOR2)", BODY, 0),
        ("  0.088   0.350     u34/Y            (AND2)", BODY, 0),
        ("  0.041   0.391     acc[7]_reg/D     (DFF)", BODY, 0),
        ("                    data arrival time      0.391", TEAL, 1),
        ("", BODY, 0),
        ("                    clock period           1.050", BODY, 0),
        ("                    clock uncertainty     -0.050", BODY, 0),
        ("                    library setup         -0.090", BODY, 0),
        ("                    data required time     0.910", GREEN, 1),
        ("", BODY, 0),
        ("                    SLACK (MET)           +0.519", GREEN, 1),
    ]
    box(ax, 3, H - 51.0, 62, 42.5, fc="#0E2A47", ec=NAVY, lw=1.4)
    y = H - 11.0
    for txt, col, bold in lines:
        c = {NAVY: "#8FD3E8", SLATE: "#9AAEC0", BODY: "#DCE6EE",
             TEAL: "#5BD6C0", GREEN: "#7BE0A0"}[col]
        ax.text(5.0, y, txt, fontsize=7.2, color=c, ha="left", family="monospace",
                fontweight="bold" if bold else "normal")
        y -= 2.28

    notes = [("WHERE it starts", "the launch flop - if it is a port,\nyour input delay is "
              "in play", H - 12.0, NAVY),
             ("WHERE it ends", "the capture flop, and the clock\nthat captures it", H - 21.0,
              NAVY),
             ("HOW it got there", "one line per cell, with the\nincremental delay", H - 30.0,
              TEAL),
             ("HOW LONG it had", "period, minus uncertainty,\nminus setup", H - 39.0, GREEN),
             ("THE ANSWER", "slack. Everything above exists\nto produce this number.",
              H - 48.0, RED)]
    for hd, sub, yy, col in notes:
        ax.text(67, yy, hd, fontsize=8.6, color=col, ha="left", fontweight="bold")
        ax.text(67, yy - 4.0, sub, fontsize=8.0, color=BODY, ha="left", va="center")

    ax.text(50, 4.0, "Read it bottom-up: the slack tells you IF, the incr column tells you "
                     "WHERE.",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    save(f, "report_anatomy")


# ------------------------------------------------------------ four path groups
def path_groups():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "Four kinds of path - and every design has all four", 12.5)

    yb = H - 22.0
    box(ax, 22, yb - 4.0, 56, 18.0, fc=LIGHT, ec=NAVY, lw=1.8)
    ax.text(50, yb + 11.6, "your design", fontsize=8.6, color=NAVY, ha="center",
            fontweight="bold")
    label_box(ax, 30, yb + 1.0, 12, 8.0, "REG", fc=WHITE, ec=TEAL, tc=TEAL, size=8.6)
    label_box(ax, 58, yb + 1.0, 12, 8.0, "REG", fc=WHITE, ec=TEAL, tc=TEAL, size=8.6)
    arrow(ax, 42, yb + 5.0, 58, yb + 5.0, color=TEAL, lw=2.0)
    ax.text(50, yb + 7.0, "reg to reg", fontsize=8.0, color=TEAL, ha="center",
            fontweight="bold")

    ax.text(6, yb + 5.0, "IN", fontsize=9, color=VIOLET, ha="center", va="center",
            fontweight="bold")
    arrow(ax, 9, yb + 5.0, 30, yb + 5.0, color=VIOLET, lw=1.8)
    ax.text(94, yb + 5.0, "OUT", fontsize=9, color=AMBER, ha="center", va="center",
            fontweight="bold")
    arrow(ax, 70, yb + 5.0, 90, yb + 5.0, color=AMBER, lw=1.8)
    wire(ax, [(9, yb + 5.0), (9, yb - 8.0), (90, yb - 8.0), (90, yb + 5.0)], color=RED,
         lw=1.5, ls="--")
    ax.text(50, yb - 10.0, "in to out - pure combinational, no flop at all", fontsize=8.2,
            color=RED, ha="center", fontstyle="italic")

    rows = [["reg -> reg", "the internal logic", "create_clock", "most of your paths"],
            ["in -> reg", "the world into you", "set_input_delay", "forgotten most often"],
            ["reg -> out", "you into the world", "set_output_delay", "forgotten second most"],
            ["in -> out", "straight through", "both, on the same path",
             "rare, and usually a mistake"]]
    table(ax, 4, 29.0, ["path group", "what it is", "constrained by", "in practice"],
          rows, [16, 24, 26, 26], 4.6, size=8.2, bold_col=0)

    ax.text(50, 1.8, "A report that only shows reg-to-reg paths is a report on "
                     "a quarter of your design.",
            fontsize=9.2, color=RED, ha="center", fontweight="bold")
    save(f, "path_groups")


# -------------------------------------------------------------- WNS / TNS
def wns_tns():
    W, Hin = 11.5, 6.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 57.4
    title(ax, 50, H - 3, "WNS and TNS say different things - you need both", 12.5)

    base = 28.0
    bars = [(-0.42, RED), (-0.31, RED), (-0.28, RED), (-0.19, RED), (-0.11, RED),
            (-0.05, RED), (0.08, GREEN), (0.21, GREEN), (0.34, GREEN), (0.52, GREEN),
            (0.61, GREEN), (0.77, GREEN)]
    x = 10
    bw = 5.6
    for v, col in bars:
        h = v * 22.0
        box(ax, x, base if v > 0 else base + h, bw, abs(h), fc=col, ec=col, r=0.3)
        x += bw + 1.2
    ax.plot([8, 92], [base, base], color=NAVY, lw=1.5)
    ax.text(6.5, base, "0", fontsize=8.2, color=NAVY, ha="right", va="center",
            fontweight="bold")
    ax.text(50, base + 20.0, "slack of every endpoint, sorted", fontsize=8.6, color=SLATE,
            ha="center")

    ax.plot([10, 15.6], [base - 9.24, base - 9.24], color=NAVY, lw=1.2, ls=":")
    ax.text(17.5, base - 11.5, "WNS = -0.42 ns\nthe single worst path", fontsize=8.4,
            color=RED, ha="left", va="center", fontweight="bold")
    ax.text(60, base - 11.5, "TNS = -1.36 ns over 6 endpoints\nthe size of the whole problem",
            fontsize=8.4, color=AMBER, ha="left", va="center", fontweight="bold")

    box(ax, 4, 3.0, 44, 12.0, fc=WHITE, ec=RED, lw=1.5)
    ax.text(26, 12.0, "WNS -0.42, TNS -0.42", fontsize=8.8, color=RED, ha="center",
            fontweight="bold")
    ax.text(26, 7.0, "one bad path. Fix that path\nand you are done today.",
            fontsize=8.3, color=BODY, ha="center")
    box(ax, 52, 3.0, 44, 12.0, fc=WHITE, ec=AMBER, lw=1.5)
    ax.text(74, 12.0, "WNS -0.42, TNS -180", fontsize=8.8, color=AMBER, ha="center",
            fontweight="bold")
    ax.text(74, 7.0, "hundreds of bad paths. The\ntarget itself is wrong.",
            fontsize=8.3, color=BODY, ha="center")
    save(f, "wns_tns")


# ----------------------------------------------------------------- Fmax
def fmax_idea():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Fmax - the number the datasheet quotes", 13)

    ax.text(50, H - 10.0, "Fmax  =  1 / ( longest path delay )", fontsize=12.5, color=NAVY,
            ha="center", family="monospace", fontweight="bold")
    ax.text(50, H - 14.5, "longest path = clock-to-Q + logic + setup + uncertainty - skew",
            fontsize=8.8, color=SLATE, ha="center")

    rows = [["2.196 ns", "455 MHz", "16-bit ripple-carry adder"],
            ["4.094 ns", "244 MHz", "32-bit ripple-carry adder"],
            ["2.315 ns", "432 MHz", "the same 32-bit adder, pipelined in two"],
            ["1.939 ns", "516 MHz", "32-bit a + b, delay-oriented mapping"]]
    table(ax, 12, H - 17.5, ["longest path", "Fmax", "design"], rows, [20, 18, 46], 5.0,
          size=8.6, bold_col=[0, 1],
          colcolors={0: NAVY, 1: GREEN})

    box(ax, 4, 3.0, 92, 15.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 14.2, "One path sets the speed of the entire chip", fontsize=9.8, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 9.0, "Not the average path. Not the second worst. The single longest one. "
                     "Everything else\nin the design could be twice as fast and the "
                     "number would not move.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 4.6, "This is why timing work is always about ONE path at a time - "
                     "the critical path.",
            fontsize=8.7, color=TEAL, ha="center", fontstyle="italic")
    save(f, "fmax_idea")


# -------------------------------------------------------- corners and derating
def corners():
    W, Hin = 11.5, 6.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 57.4
    title(ax, 50, H - 3, "One netlist, several silicons - PVT corners", 12.5)
    ax.text(50, H - 7.2, "The same chip is slower when it is hot and starved of voltage, "
                         "and faster when it is cold.",
            fontsize=9, color=SLATE, ha="center")

    yb = H - 13.0
    cards = [("SLOW corner", "slow silicon, low voltage,\nhigh temperature",
              "checks SETUP\nthe chip must still be fast enough", RED),
             ("FAST corner", "fast silicon, high voltage,\nlow temperature",
              "checks HOLD\nthe data must not race ahead", GREEN),
             ("TYPICAL", "nominal everything",
              "for power and sanity -\nnever sign off on it alone", SLATE)]
    bw = 29.0
    x0 = 50 - (3 * bw + 2 * 3.5) / 2
    for i, (nm, pvt, use, col) in enumerate(cards):
        x = x0 + i * (bw + 3.5)
        box(ax, x, yb - 21.0, bw, 21.0, fc=WHITE, ec=col, lw=1.7)
        box(ax, x, yb - 6.0, bw, 6.0, fc=col, ec=col)
        ax.text(x + bw / 2, yb - 3.0, nm, ha="center", va="center", fontsize=9.2, color=WHITE,
                fontweight="bold")
        ax.text(x + bw / 2, yb - 10.5, pvt, ha="center", va="center", fontsize=8.2,
                color=BODY)
        ax.text(x + bw / 2, yb - 17.0, use, ha="center", va="center", fontsize=8.2,
                color=col, fontweight="bold")

    box(ax, 4, 3.0, 92, 16.5, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, 16.0, "Why setup and hold are checked at OPPOSITE corners", fontsize=9.6,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 11.0, "Setup is a race against the clock, so the danger is SLOW logic - "
                      "check it at the slow corner.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 7.6, "Hold is a race against the previous edge, so the danger is FAST logic - "
                     "check it at the fast corner.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.2, "A design that passes both corners passes every chip in between.",
            fontsize=8.6, color=GREEN, ha="center", fontweight="bold")
    save(f, "corners")


for fn in (sta_vs_sim, timing_graph, arrival_required, report_anatomy, path_groups,
           wns_tns, fmax_idea, corners):
    fn()
