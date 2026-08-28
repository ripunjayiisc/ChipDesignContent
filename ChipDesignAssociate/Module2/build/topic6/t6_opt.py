# -*- coding: utf-8 -*-
"""Topic 6 diagrams — fixing violations and closing timing."""
import _boot
from dsl import *


# ---------------------------------------------------------- the setup menu
def fix_setup_menu():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "A setup violation - the fixes, cheapest first", 12.5)
    ax.text(50, H - 7.2, "Work down this list. Never start at the bottom.",
            fontsize=9, color=SLATE, ha="center")

    steps = [("1", "Check the constraint first", "Is the period real? Is a false path "
              "missing? Half of all\n\"violations\" are the constraint file being wrong.",
              GREEN),
             ("2", "Let the tool try harder", "Higher effort, delay-oriented mapping. In the "
              "lab this alone\ntook a 32-bit adder from 4.6 ns to 1.9 ns.", GREEN),
             ("3", "Restructure the logic", "Balance a deep chain into a tree. Same function, "
              "log(N)\ndepth instead of N.", TEAL),
             ("4", "Pipeline it", "Cut the path with a register. Throughput stays, latency "
              "grows\nby a cycle. The biggest single win available.", TEAL),
             ("5", "Retime", "Move an existing register to a better place in the same\n"
              "logic. Latency does not change at all.", VIOLET),
             ("6", "Change the architecture", "A different adder, a different encoding, "
              "fewer operations\nper cycle. Real work, real payoff.", AMBER),
             ("7", "Slow the clock down", "Always available, always last. You are shipping "
              "a slower chip.", RED)]
    y = H - 11.0
    rh = 6.5
    for n, hd, sub, col in steps:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((9.0, y - rh / 2), 2.3, fc=col, ec=col, zorder=5))
        ax.text(9.0, y - rh / 2, n, ha="center", va="center", fontsize=8.8, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(14, y - 2.5, hd, ha="left", fontsize=9.0, color=col, fontweight="bold")
        ax.text(14, y - 4.9, sub, ha="left", va="center", fontsize=7.8, color=BODY)
        y -= rh + 1.0

    box(ax, 4, 2.0, 92, 6.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 4.8, "Steps 1 and 2 cost you minutes. Step 7 costs your customer performance "
                     "for ever.",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    save(f, "fix_setup_menu")


# ------------------------------------------------------------- pipelining
def pipelining():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Pipelining - cut the path, keep the work", 13)

    yA = H - 16.0
    ax.text(4, yA + 10.0, "BEFORE - one long combinational path", fontsize=9.4, color=RED,
            ha="left", fontweight="bold")
    label_box(ax, 6, yA, 10, 8.0, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.4)
    box(ax, 22, yA, 54, 8.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(49, yA + 4.0, "32-bit ripple carry - 32 gate delays end to end", ha="center",
            va="center", fontsize=8.6, color=RED)
    label_box(ax, 82, yA, 10, 8.0, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.4)
    arrow(ax, 16, yA + 4.0, 22, yA + 4.0, color=SLATE, lw=1.6)
    arrow(ax, 76, yA + 4.0, 82, yA + 4.0, color=SLATE, lw=1.6)
    ax.text(49, yA - 3.6, "longest path 4.094 ns   ->   244 MHz", fontsize=9, color=RED,
            ha="center", family="monospace", fontweight="bold")

    yB = H - 36.0
    ax.text(4, yB + 10.0, "AFTER - the same logic, cut in half by a register", fontsize=9.4,
            color=GREEN, ha="left", fontweight="bold")
    label_box(ax, 6, yB, 10, 8.0, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.4)
    box(ax, 22, yB, 24, 8.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(34, yB + 4.0, "lower 16 bits", ha="center", va="center", fontsize=8.4,
            color=GREEN)
    label_box(ax, 50, yB, 10, 8.0, "new\nFF", fc=WHITE, ec=VIOLET, tc=VIOLET, size=8.4,
              lw=2.0)
    box(ax, 64, yB, 12, 8.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(70, yB + 4.0, "upper", ha="center", va="center", fontsize=8.4, color=GREEN)
    label_box(ax, 82, yB, 10, 8.0, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.4)
    for x1, x2 in [(16, 22), (46, 50), (60, 64), (76, 82)]:
        arrow(ax, x1, yB + 4.0, x2, yB + 4.0, color=SLATE, lw=1.6)
    ax.text(49, yB - 3.6, "longest path 2.315 ns   ->   432 MHz", fontsize=9, color=GREEN,
            ha="center", family="monospace", fontweight="bold")

    box(ax, 4, 3.0, 44, 15.0, fc="#EEF7F1", ec=GREEN, lw=1.5)
    ax.text(26, 14.4, "what you gain", fontsize=9, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(26, 8.6, "1.8x the clock frequency, and\nthe same result every cycle once\n"
                     "the pipe is full", fontsize=8.3, color=BODY, ha="center")
    box(ax, 52, 3.0, 44, 15.0, fc="#FFF7EC", ec=AMBER, lw=1.5)
    ax.text(74, 14.4, "what you pay", fontsize=9, color=AMBER, ha="center", fontweight="bold")
    ax.text(74, 8.6, "one extra cycle of latency, one\nmore register bank, and every\n"
                     "control signal must be delayed too", fontsize=8.3, color=BODY,
            ha="center")
    save(f, "pipelining")


# ---------------------------------------------------------------- retiming
def retiming():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Retiming - move the register you already have", 13)

    yA = H - 15.0
    ax.text(4, yA + 9.5, "BEFORE - 4 ns of logic, then 1 ns", fontsize=9.2, color=RED,
            ha="left", fontweight="bold")
    label_box(ax, 5, yA, 9, 7.5, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.2)
    box(ax, 19, yA, 34, 7.5, fc="#FDECEF", ec=RED, lw=1.5)
    ax.text(36, yA + 3.75, "logic  4.0 ns", ha="center", va="center", fontsize=8.6, color=RED)
    label_box(ax, 58, yA, 9, 7.5, "FF", fc=WHITE, ec=VIOLET, tc=VIOLET, size=8.2, lw=2.0)
    box(ax, 72, yA, 14, 7.5, fc=LIGHT, ec=TEAL, lw=1.5)
    ax.text(79, yA + 3.75, "1.0 ns", ha="center", va="center", fontsize=8.6, color=TEAL)
    label_box(ax, 90, yA, 8, 7.5, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.2)
    ax.text(50, yA - 3.8, "worst stage = 4.0 ns   ->   250 MHz", fontsize=8.8, color=RED,
            ha="center", family="monospace", fontweight="bold")

    yB = H - 34.0
    ax.text(4, yB + 9.0, "AFTER - the register moved left", fontsize=9.2, color=GREEN,
            ha="left", fontweight="bold")
    label_box(ax, 5, yB, 9, 7.5, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.2)
    box(ax, 19, yB, 22, 7.5, fc="#EEF7F1", ec=GREEN, lw=1.5)
    ax.text(30, yB + 3.75, "2.5 ns", ha="center", va="center", fontsize=8.6, color=GREEN)
    label_box(ax, 46, yB, 9, 7.5, "FF", fc=WHITE, ec=VIOLET, tc=VIOLET, size=8.2, lw=2.0)
    box(ax, 60, yB, 26, 7.5, fc="#EEF7F1", ec=GREEN, lw=1.5)
    ax.text(73, yB + 3.75, "2.5 ns", ha="center", va="center", fontsize=8.6, color=GREEN)
    label_box(ax, 90, yB, 8, 7.5, "FF", fc=WHITE, ec=NAVY, tc=NAVY, size=8.2)
    arrow(ax, 62, yB + 9.5, 50, yB + 9.5, color=VIOLET, lw=1.8)
    ax.text(64, yB + 9.5, "moved this way", fontsize=8.0, color=VIOLET, ha="left",
            va="center", fontstyle="italic")
    ax.text(50, yB - 3.8, "worst stage = 2.5 ns   ->   400 MHz", fontsize=8.8, color=GREEN,
            ha="center", family="monospace", fontweight="bold")

    box(ax, 4, 3.0, 92, 13.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 12.4, "Retiming is free in a way pipelining is not", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 7.4, "No register was added, so the latency is unchanged and no control "
                     "signal needs re-aligning.\nThe tool can do this for you "
                     "(Vivado: -retiming; Yosys has no equivalent yet) - but only if your "
                     "RTL\nlets it: a register with an asynchronous reset or a fanout to "
                     "a port usually cannot move.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "retiming")


# --------------------------------------------------------- logic restructure
def logic_restructure():
    W, Hin = 11.5, 7.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 62.6
    title(ax, 50, H - 3, "Restructuring - a chain is depth N, a tree is depth log N", 12.5)

    yc = H - 17.0
    ax.text(4, yc + 9.0, "CHAIN:  a + b + c + d + e + f + g + h   as written",
            fontsize=8.8, color=RED, ha="left", fontweight="bold")
    x = 10
    for i in range(7):
        box(ax, x, yc, 6.0, 5.0, fc="#FDECEF", ec=RED, lw=1.2, r=0.4)
        ax.text(x + 3, yc + 2.5, "+", ha="center", va="center", fontsize=9, color=RED,
                fontweight="bold")
        if i:
            arrow(ax, x - 3.0, yc + 2.5, x, yc + 2.5, color=RED, lw=1.2, ms=6)
        x += 9.0
    ax.text(86, yc + 2.5, "depth 7", fontsize=9, color=RED, ha="left", va="center",
            fontweight="bold")

    yt = H - 38.0
    ax.text(4, yt + 13.5, "TREE:  ((a+b)+(c+d)) + ((e+f)+(g+h))   same answer",
            fontsize=8.8, color=GREEN, ha="left", fontweight="bold")
    rows = [([16, 32, 48, 64], yt + 7.0), ([24, 56], yt), ([40], yt - 7.0)]
    for xs, yy in rows:
        for xx in xs:
            box(ax, xx - 3, yy, 6.0, 5.0, fc="#EEF7F1", ec=GREEN, lw=1.2, r=0.4)
            ax.text(xx, yy + 2.5, "+", ha="center", va="center", fontsize=9, color=GREEN,
                    fontweight="bold")
    for a, b in [(16, 24), (32, 24), (48, 56), (64, 56), (24, 40), (56, 40)]:
        wire(ax, [(a, rows[0][1] if a in rows[0][0] else rows[1][1]),
                  (a, (rows[0][1] if a in rows[0][0] else rows[1][1]) - 2.0),
                  (b, (rows[0][1] if a in rows[0][0] else rows[1][1]) - 2.0),
                  (b, (rows[1][1] if a in rows[0][0] else rows[2][1]) + 5.0)],
             color=GREEN, lw=1.2)
    ax.text(74, yt, "depth 3", fontsize=9, color=GREEN, ha="left", va="center",
            fontweight="bold")

    box(ax, 4, 2.5, 92, 12.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 11.4, "Synthesis usually does this for you - usually", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 6.6, "Associativity lets the tool rebalance a sum. It will NOT rebalance "
                     "across a signal you\nassigned to an intermediate wire that something "
                     "else also reads - that reader pins the structure.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "logic_restructure")


# ----------------------------------------------------------------- hold race
def hold_race():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "A hold violation is a race, not a delay problem", 12.5)

    ctop = H - 13.0
    clk_wave(ax, 14, ctop, 30.0, 3, 5.0, color=NAVY, name="clk")
    xe = 14.0
    ax.plot([xe, xe], [30.0, ctop + 6.5], color=RED, lw=1.5, ls="--")
    ax.text(xe, ctop + 7.4, "one edge, two flops", fontsize=8.4, color=RED, ha="center",
            fontweight="bold")

    y1 = ctop - 10.0
    ax.text(11, y1 + 2.0, "q1", fontsize=8.6, color=TEAL, ha="right", va="center",
            fontweight="bold")
    wire(ax, [(14, y1), (17, y1), (17, y1 + 4.0), (60, y1 + 4.0)], color=TEAL, lw=2.0)
    arrow(ax, 14, y1 - 3.5, 17, y1 - 3.5, color=TEAL, lw=1.5, style="<|-|>")
    ax.text(19, y1 - 3.5, "new data arrives here - only 0.16 ns after the edge",
            fontsize=8.2, color=TEAL, ha="left", va="center")

    y2 = ctop - 22.0                         # box 29.3 .. 34.3
    box(ax, 14, y2, 6.0, 5.0, fc="#FDECEF", ec=RED, lw=1.4, r=0.4)
    ax.text(11, y2 + 2.5, "flop2\nwindow", fontsize=8.0, color=RED, ha="right", va="center",
            fontweight="bold")
    ax.text(21.5, y2 + 2.5, "the hold window: the old value must still be here for 0.035 ns",
            fontsize=8.2, color=RED, ha="left", va="center")

    box(ax, 4, 15.0, 92, 14.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 25.8, "The new data won the race - the second flop captured it a whole "
                      "cycle early", fontsize=9.4, color=RED, ha="center", fontweight="bold")
    ax.text(50, 19.5, "hold slack  =  arrival 0.164  -  skew 0.300  -  hold 0.035  "
                      "=  -0.171 ns", fontsize=9.2, color=NAVY, ha="center",
            family="monospace", fontweight="bold")

    ax.text(50, 10.0, "Notice what is NOT in that equation: the clock period.", fontsize=9.4,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 5.6, "You can run this chip at 1 Hz and it will still be broken. "
                     "A hold violation is a functional failure,\nnot a performance one - "
                     "the only fix is to make the DATA path slower.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "hold_race")


# ------------------------------------------------------------- fixing hold
def fix_hold():
    W, Hin = 11.5, 7.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 60.9
    title(ax, 50, H - 3, "Fixing hold - add delay, on purpose", 13)

    yA = H - 16.0
    ax.text(4, yA + 9.8, "BEFORE - nothing between the two flops", fontsize=9.2, color=RED,
            ha="left", fontweight="bold")
    label_box(ax, 12, yA, 12, 8.0, "FF1", fc=WHITE, ec=NAVY, tc=NAVY, size=8.6)
    label_box(ax, 70, yA, 12, 8.0, "FF2", fc=WHITE, ec=NAVY, tc=NAVY, size=8.6)
    arrow(ax, 24, yA + 4.0, 70, yA + 4.0, color=RED, lw=2.0)
    ax.text(47, yA + 6.0, "0.164 ns - too fast", fontsize=8.6, color=RED, ha="center",
            fontweight="bold")
    ax.text(88, yA + 4.0, "-0.171 ns", fontsize=9, color=RED, ha="center", va="center",
            fontweight="bold")

    yB = H - 35.0
    ax.text(4, yB + 9.8, "AFTER - two buffers inserted in the data path", fontsize=9.2,
            color=GREEN, ha="left", fontweight="bold")
    label_box(ax, 12, yB, 12, 8.0, "FF1", fc=WHITE, ec=NAVY, tc=NAVY, size=8.6)
    for x in (34, 50):
        gate(ax, "buf", x, yB + 4.0, 7.0, 6.0, ec=VIOLET)
    label_box(ax, 70, yB, 12, 8.0, "FF2", fc=WHITE, ec=NAVY, tc=NAVY, size=8.6)
    arrow(ax, 24, yB + 4.0, 31, yB + 4.0, color=GREEN, lw=1.6)
    arrow(ax, 42, yB + 4.0, 47, yB + 4.0, color=GREEN, lw=1.6)
    arrow(ax, 58, yB + 4.0, 70, yB + 4.0, color=GREEN, lw=1.6)
    ax.text(47, yB - 3.6, "delay cells - their only job is to waste time", fontsize=8.2,
            color=VIOLET, ha="center", fontstyle="italic")
    ax.text(88, yB + 4.0, "+0.071 ns", fontsize=9, color=GREEN, ha="center", va="center",
            fontweight="bold")

    box(ax, 4, 3.0, 92, 17.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 17.0, "You almost never do this by hand", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 12.4, "Place-and-route inserts hold buffers automatically, after layout, "
                      "when the real skew is known.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 8.4, "Your job in RTL is to not make it impossible: keep clock domains clean, "
                     "and never gate a clock\nby hand when an enable would do.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.2, "Adding delay costs area and power but no frequency - "
                     "which is why hold is always fixable.",
            fontsize=8.5, color=GREEN, ha="center", fontstyle="italic")
    save(f, "fix_hold")


# --------------------------------------------------------- the closure loop
def closure_loop():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "Timing closure is a loop, and you exit it once", 12.5)

    cx, cy = 50.0, H - 28.0
    r = 17.0
    nodes = [("write / fix\nthe RTL", 90, TEAL), ("synthesise", 18, NAVY),
             ("run STA", -54, VIOLET), ("read the\nworst path", -126, AMBER),
             ("decide the\nfix", 162, GREEN)]
    import math
    pts = []
    for nm, ang, col in nodes:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a) * 1.9, cy + r * math.sin(a)
        pts.append((x, y, nm, col))
    for i, (x, y, nm, col) in enumerate(pts):
        box(ax, x - 11, y - 5.0, 22, 10.0, fc=WHITE, ec=col, lw=1.7)
        ax.text(x, y, nm, ha="center", va="center", fontsize=8.6, color=col,
                fontweight="bold")
    for i in range(len(pts)):
        x1, y1, _, _ = pts[i]
        x2, y2, _, c2 = pts[(i + 1) % len(pts)]
        dx, dy = x2 - x1, y2 - y1
        d = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / d, dy / d
        arrow(ax, x1 + ux * 13.0, y1 + uy * 6.5, x2 - ux * 13.0, y2 - uy * 6.5,
              color=SLATE, lw=1.5, ms=8)

    box(ax, 4, 3.0, 92, 18.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 18.0, "You leave the loop when all three are true", fontsize=9.6, color=GREEN,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["WNS >= 0 at the slow corner, with real uncertainty in the "
                            "constraint",
                            "hold slack >= 0 at the fast corner",
                            "zero unconstrained endpoints - the report actually looked "
                            "at everything"]):
        ax.text(9, 13.4 - i * 3.6, "✓", fontsize=9.4, color=GREEN, ha="left",
                fontweight="bold")
        ax.text(13, 13.4 - i * 3.6, ln, fontsize=8.5, color=BODY, ha="left")
    save(f, "closure_loop")


# ------------------------------------------------------- measured lab results
def measured_results():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "The numbers you will measure yourself in the lab", 12.5)
    ax.text(50, H - 7.2, "Every figure below came out of the STA engine you are about "
                         "to build.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["32-bit ripple, area mapping", "4.094 ns", "244 MHz", "the baseline"],
            ["32-bit a+b, area mapping", "4.615 ns", "217 MHz", "SLOWER - see below"],
            ["32-bit a+b, delay mapping", "1.939 ns", "516 MHz", "same RTL, 2.4x faster"],
            ["hold demo, 0.30 ns skew", "-0.165 ns", "broken", "fails at any frequency"],
            ["hold demo, delay added", "+0.071 ns", "works", "two cells fixed it"],
            ["slow path, no exception", "-1.193 ns", "false alarm", "the tool was misled"],
            ["slow path, multicycle 4", "+0.392 ns", "real", "one SDC line"]]
    table(ax, 4, H - 10.5, ["design / experiment", "worst slack", "result", "what it teaches"],
          rows, [34, 18, 16, 24], 4.6, size=8.0, bold_col=[1],
          colcolors={1: NAVY})

    box(ax, 4, 3.0, 92, 18.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 18.4, "Read rows 2 and 3 again - this is the lesson of the whole topic",
            fontsize=9.5, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 13.0, "The SAME RTL, a + b, ran at 217 MHz and at 516 MHz. Nothing in the "
                      "source changed.\nOnly the synthesis option did.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 7.4, "\"Describe intent, not structure\" is only half the rule.\n"
                     "The other half is: check what your tool did with it.",
            fontsize=9.0, color=NAVY, ha="center", fontweight="bold")
    save(f, "measured_results")


for fn in (fix_setup_menu, pipelining, retiming, logic_restructure, hold_race,
           fix_hold, closure_loop, measured_results):
    fn()
