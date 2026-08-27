# -*- coding: utf-8 -*-
"""Topic 5 diagrams — verification fundamentals."""
import _boot
from dsl import *


# --------------------------------------------------------------- why verify
def why_verify():
    W, Hin = 12.0, 5.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 45.0
    title(ax, 50, H - 3, "Verification is where the engineering time goes", 13)

    # ---- effort split -----------------------------------------------------
    ax.text(4, H - 7.5, "Typical effort on a real ASIC or FPGA block", fontsize=9.5,
            color=SLATE, ha="left")
    segs = [("RTL design", 30, TEAL), ("Verification", 55, AMBER),
            ("Synthesis & timing", 15, GREEN)]
    x = 4
    for name, pct, col in segs:
        w = pct * 0.92
        box(ax, x, H - 14.5, w, 5.5, fc=col, ec=col, r=0.6)
        ax.text(x + w / 2, H - 11.75, "%d%%" % pct, ha="center", va="center",
                fontsize=10.5, color=WHITE, fontweight="bold")
        ax.text(x + w / 2, H - 16.9, name, ha="center", va="center", fontsize=8.8,
                color=col, fontweight="bold")
        x += w

    ax.plot([4, 96], [H - 19.8, H - 19.8], color=GRID, lw=1.0)

    # ---- cost of a bug, by the stage that finds it ------------------------
    ax.text(4, H - 22.8, "Relative cost of finding the SAME bug, by the stage that finds it",
            fontsize=9.5, color=SLATE, ha="left")
    stages = [("lint", 1, GREEN), ("simulation", 3, GREEN), ("synthesis", 8, TEAL),
              ("FPGA lab", 25, AMBER), ("silicon", 60, RED)]
    x0, y0, bw, gap = 6.0, 5.5, 13.0, 3.0
    for i, (name, cost, col) in enumerate(stages):
        h = cost * 0.26                     # 60 -> 15.6, top at 21.1
        x = x0 + i * (bw + gap)
        box(ax, x, y0, bw, max(h, 0.5), fc=col, ec=col, r=0.5)
        ax.text(x + bw / 2, y0 - 2.6, name, ha="center", va="center", fontsize=9,
                color=NAVY, fontweight="bold")
        ax.text(x + bw / 2, y0 + max(h, 0.5) + 1.6, "x%d" % cost, ha="center",
                va="center", fontsize=9, color=col, fontweight="bold")

    ax.text(7, 15.5,
            "A bug caught by a linter costs a second.\n"
            "The same bug found after tape-out costs a respin.",
            ha="left", va="center", fontsize=9.5, color=BODY)
    save(f, "why_verify")


# ------------------------------------------------------------ verification gap
def verification_gap():
    W, Hin = 11.0, 4.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The verification gap — and what closes it", 13)

    box(ax, 4, 6, 44, H - 13, fc=LIGHT, ec=GRID)
    ax.text(26, H - 10.5, "The problem", fontsize=10.5, color=NAVY, fontweight="bold",
            ha="center")
    lines = [("Design size", "doubles every ~2 years", TEAL),
             ("States to check", "grows EXPONENTIALLY with registers", RED),
             ("A 32-bit adder", "2^64 input pairs — 500 000 years", RED),
             ("Exhaustive testing", "impossible for anything real", RED)]
    y = H - 15
    for a, b, c in lines:
        ax.text(7, y, "· " + a, fontsize=9, color=NAVY, fontweight="bold", ha="left")
        ax.text(23, y, b, fontsize=9, color=c, ha="left")
        y -= 4.6

    box(ax, 52, 6, 44, H - 13, fc="#EEF7F1", ec=GREEN)
    ax.text(74, H - 10.5, "What we do instead", fontsize=10.5, color=GREEN,
            fontweight="bold", ha="center")
    lines2 = [("Directed tests", "for the cases you can name"),
              ("Constrained random", "for the ones you cannot"),
              ("Assertions", "check rules on EVERY cycle"),
              ("Coverage", "measures what was actually reached")]
    y = H - 15
    for a, b in lines2:
        ax.text(55, y, "· " + a, fontsize=9, color=NAVY, fontweight="bold", ha="left")
        ax.text(71, y, b, fontsize=9, color=BODY, ha="left")
        y -= 4.6
    ax.text(74, 8.6, "Not proof — evidence, measured.", fontsize=9, color=GREEN,
            ha="center", fontstyle="italic")
    save(f, "verification_gap")


# ------------------------------------------------------------------ ver flow
def ver_flow():
    W, Hin = 12.0, 4.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "The verification loop — it ends at coverage, not at PASS", 13)

    steps = [("SPECIFICATION", "what the block\nmust do", NAVY),
             ("VERIFICATION\nPLAN", "what would\nconvince me", VIOLET),
             ("TESTBENCH", "stimulus, model,\nchecks", TEAL),
             ("RUN", "regression,\nmany seeds", GREEN),
             ("COVERAGE", "what did I\nactually test?", AMBER)]
    bw, gap = 16.0, 3.6
    x0 = 50 - (len(steps) * bw + (len(steps) - 1) * gap) / 2
    ytop = H - 9
    for i, (name, sub, col) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 13, bw, 13, fc=WHITE, ec=col, lw=1.9)
        box(ax, x, ytop - 4.6, bw, 4.6, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.3, name, ha="center", va="center", fontsize=8.6,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ytop - 8.8, sub, ha="center", va="center", fontsize=8.4,
                color=BODY)
        if i < len(steps) - 1:
            arrow(ax, x + bw, ytop - 6.5, x + bw + gap, ytop - 6.5, color=SLATE, lw=1.8)

    # feedback arrow: coverage holes -> new stimulus
    xa = x0 + 4 * (bw + gap) + bw / 2
    xb = x0 + 2 * (bw + gap) + bw / 2
    wire(ax, [(xa, ytop - 13), (xa, 6.5), (xb, 6.5), (xb, ytop - 13)], color=AMBER, lw=1.8)
    arrow(ax, xb, 7.5, xb, ytop - 13, color=AMBER, lw=1.8)
    ax.text((xa + xb) / 2, 4.4, "holes found  ->  write the stimulus that fills them",
            ha="center", fontsize=9, color=AMBER, fontweight="bold")
    save(f, "ver_flow")


# ------------------------------------------------------- directed vs random
def directed_vs_random():
    W, Hin = 11.0, 4.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Directed and constrained-random — you need both", 13)

    # left: directed - a few precise darts
    box(ax, 4, 6, 43, H - 13, fc=WHITE, ec=TEAL, lw=1.8)
    ax.text(25.5, H - 10.5, "DIRECTED", fontsize=11, color=TEAL, fontweight="bold",
            ha="center")
    ax.text(25.5, H - 14.5, "you name the case, you write the check",
            fontsize=8.8, color=SLATE, ha="center", fontstyle="italic")
    pts = [(12, 14), (20, 22), (32, 12), (38, 24), (26, 17)]
    box(ax, 8, 9, 35, 20, fc=LIGHT, ec=GRID)
    ax.text(25.5, 30.6, "the space of all possible behaviour", fontsize=8,
            color=SLATE, ha="center")
    for px, py in pts:
        ax.plot([px], [py], "o", ms=7, color=TEAL, zorder=5)
    ax.text(25.5, 6.8, "hits exactly what you thought of — and nothing else",
            fontsize=8.6, color=BODY, ha="center")

    # right: random - a cloud
    box(ax, 53, 6, 43, H - 13, fc=WHITE, ec=AMBER, lw=1.8)
    ax.text(74.5, H - 10.5, "CONSTRAINED-RANDOM", fontsize=11, color=AMBER,
            fontweight="bold", ha="center")
    ax.text(74.5, H - 14.5, "you name the CONSTRAINTS, the tool picks the case",
            fontsize=8.8, color=SLATE, ha="center", fontstyle="italic")
    box(ax, 57, 9, 35, 20, fc=LIGHT, ec=GRID)
    ax.text(74.5, 30.6, "the same space", fontsize=8, color=SLATE, ha="center")
    import math
    for i in range(60):
        a = (i * 2.399)
        rr = 8.5 * math.sqrt((i + 1) / 60.0)
        px = 74.5 + rr * math.cos(a) * 1.7
        py = 19 + rr * math.sin(a) * 0.95
        ax.plot([px], [py], "o", ms=3.4, color=AMBER, alpha=0.8, zorder=5)
    ax.plot([88], [12], "*", ms=13, color=RED, zorder=6)
    ax.text(88, 9.2, "the bug you\nnever imagined", fontsize=7.6, color=RED,
            ha="center", va="top", fontweight="bold")
    save(f, "directed_vs_random")


# ------------------------------------------------------------- bug escape
def bug_escape():
    W, Hin = 11.5, 3.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Each stage is a filter — and each one you skip lets bugs through", 12.5)

    stages = [("LINT", "width, latches,\nundriven nets", GREEN),
              ("SIMULATION", "wrong behaviour,\nprotocol errors", TEAL),
              ("ASSERTIONS", "rule broken, at\nthe exact cycle", VIOLET),
              ("COVERAGE", "what was never\nexercised at all", AMBER),
              ("SYNTHESIS", "structure the\nsimulator hid", NAVY)]
    bw, gap = 16.5, 3.0
    x0 = 50 - (len(stages) * bw + (len(stages) - 1) * gap) / 2
    y = H - 22
    for i, (name, sub, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        box(ax, x, y, bw, 13.5, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, y + 9.2, bw, 4.3, fc=col, ec=col)
        ax.text(x + bw / 2, y + 11.35, name, ha="center", va="center", fontsize=8.6,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, y + 4.4, sub, ha="center", va="center", fontsize=8.2,
                color=BODY)
        if i < len(stages) - 1:
            arrow(ax, x + bw, y + 6.7, x + bw + gap, y + 6.7, color=SLATE, lw=1.7)
    arrow(ax, x0 - 4.5, y + 6.7, x0, y + 6.7, color=RED, lw=2.2)
    ax.text(x0 - 5.5, y + 6.7, "bugs", ha="right", va="center", fontsize=9.5,
            color=RED, fontweight="bold")
    xe = x0 + (len(stages) - 1) * (bw + gap) + bw
    arrow(ax, xe, y + 6.7, xe + 4.5, y + 6.7, color=GREEN, lw=2.2)
    ax.text(xe + 5.5, y + 6.7, "silicon", ha="left", va="center", fontsize=9.5,
            color=GREEN, fontweight="bold")
    ax.text(50, y - 4.5,
            "Run them cheapest first. A bug that a one-second lint would have named "
            "should never reach a waveform viewer.",
            ha="center", fontsize=9, color=BODY)
    save(f, "bug_escape")


# ------------------------------------------------------- checker taxonomy
def checker_taxonomy():
    W, Hin = 11.5, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Four ways to decide whether the answer was right", 13)

    items = [("A HUMAN LOOKS\nAT THE WAVEFORM", RED,
              "Not a check. Cannot run\novernight, cannot run in a\nregression, will stop being\ndone within a week."),
             ("HARD-CODED\nEXPECTED VALUES", AMBER,
              "Works up to about twenty\ncases. Beyond that, writing\nthem is where the bugs\nstart to live."),
             ("A REFERENCE MODEL\n+ SCOREBOARD", GREEN,
              "An independent model of the\nSPEC computes the answer.\nNow every cycle can be\nchecked, not just some."),
             ("ASSERTIONS", VIOLET,
              "The rule itself, checked on\nEVERY edge of EVERY test,\nreporting at the cycle it\nbroke, not at the output.")]
    bw, gap = 22.0, 3.5
    x0 = 50 - (len(items) * bw + (len(items) - 1) * gap) / 2
    for i, (name, col, body) in enumerate(items):
        x = x0 + i * (bw + gap)
        box(ax, x, 6, bw, H - 13, fc=WHITE, ec=col, lw=1.9)
        box(ax, x, H - 16.5, bw, 9.5, fc=col, ec=col)
        ax.text(x + bw / 2, H - 11.75, name, ha="center", va="center", fontsize=9,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, H - 25.5, body, ha="center", va="center", fontsize=8.3,
                color=BODY)
        ax.text(x + bw / 2, 8.6, ["weakest", "", "", "strongest"][i], ha="center",
                fontsize=8.4, color=col, fontweight="bold", fontstyle="italic")
    save(f, "checker_taxonomy")


# --------------------------------------------------------------- coverage
def coverage_types():
    W, Hin = 11.0, 4.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Two kinds of coverage — and only one of them knows the spec", 13)

    box(ax, 4, 6, 43, H - 13, fc=WHITE, ec=TEAL, lw=1.8)
    ax.text(25.5, H - 10.5, "CODE COVERAGE", fontsize=11, color=TEAL,
            fontweight="bold", ha="center")
    ax.text(25.5, H - 14.2, "computed by the tool, automatically", fontsize=8.6,
            color=SLATE, ha="center", fontstyle="italic")
    rows = [("line", "was this line executed?"),
            ("branch", "was each if/else arm taken?"),
            ("condition", "did each sub-expression take both values?"),
            ("toggle", "did each bit go 0->1 and 1->0?"),
            ("FSM state", "was each state entered, each arc taken?")]
    y = H - 18.5
    for a, b in rows:
        ax.text(7, y, a, fontsize=8.8, color=NAVY, fontweight="bold", ha="left")
        ax.text(17.5, y, b, fontsize=8.5, color=BODY, ha="left")
        y -= 4.0
    ax.text(25.5, 8.2, "100% code coverage still proves nothing about\n"
                       "behaviour you never wrote code for.",
            ha="center", fontsize=8.4, color=RED, fontstyle="italic")

    box(ax, 52, 6, 44, H - 13, fc=WHITE, ec=AMBER, lw=1.8)
    ax.text(74, H - 10.5, "FUNCTIONAL COVERAGE", fontsize=11, color=AMBER,
            fontweight="bold", ha="center")
    ax.text(74, H - 14.2, "written by YOU, from the specification", fontsize=8.6,
            color=SLATE, ha="center", fontstyle="italic")
    rows2 = [("did the FIFO ever reach full?", "no tool can ask this for you"),
             ("read and write on the same cycle?", "it is a spec-level event"),
             ("...while empty? ...while full?", "the corner cases, named"),
             ("did the pointers wrap?", "a sequence, not a state"),
             ("full -> empty -> full?", "a scenario over time")]
    y = H - 18.5
    for a, b in rows2:
        ax.text(55, y, "· " + a, fontsize=8.6, color=NAVY, ha="left")
        y -= 4.0
    ax.text(74, 8.2, "This is the list that says when you are FINISHED.",
            ha="center", fontsize=8.6, color=GREEN, fontweight="bold")
    save(f, "coverage_types")


# --------------------------------------------------------------- ver plan
def ver_plan():
    W, Hin = 11.0, 4.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "A verification plan is one table, written before the testbench", 12.5)

    cols = ["Feature from the spec", "How it is checked", "Stimulus", "Coverage bin", "Status"]
    rows = [["Words come out in order", "scoreboard, every cycle", "random", "write/read accepted", "done"],
            ["Never writes when full", "assertion a_full_iff_depth", "write-heavy", "write while full", "done"],
            ["Never reads when empty", "assertion a_count_range", "read-heavy", "read while empty", "done"],
            ["Simultaneous r+w holds count", "assertion a_step_both", "balanced", "r+w same cycle", "done"],
            ["r+w while EMPTY writes", "scoreboard", "balanced", "r+w while empty", "done"],
            ["Reset empties the FIFO", "directed check", "directed", "post-reset state", "done"],
            ["Pointers wrap correctly", "scoreboard", "long random", "pointers wrapped", "done"]]
    cw = [26, 22, 14, 20, 10]
    table(ax, 4, H - 8, cols, rows, cw, 4.4, size=8.0, bold_col=0,
          colcolors={4: GREEN})
    ax.text(50, 4.2, "Written FIRST, reviewed like the design, and the 'Status' column is what "
                     "the project manager actually asks about.",
            ha="center", fontsize=8.8, color=BODY, fontstyle="italic")
    save(f, "ver_plan")


# ----------------------------------------------------------- clinic matrix
def clinic_matrix():
    W, Hin = 12.0, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3.2,
          "The whole of Topic 5, in one table — measured, not asserted", 13)
    ax.text(50, H - 7.6,
            "The same three testbenches, run against the correct FIFO and five broken copies. "
            "Every cell is real output from Topic5_Lab.",
            ha="center", fontsize=8.8, color=SLATE)

    cols = ["testbench", "fifo", "b1", "b2", "b3", "b4", "b5", "bugs caught"]
    rows = [["V1  naive directed", "pass", "pass", "pass", "pass", "pass", "pass", "0 of 5"],
            ["V2  model + corners", "pass", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT", "pass", "4 of 5"],
            ["V3  constrained-random", "pass", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT", "5 of 5"]]
    cw = [26, 9, 9, 9, 9, 9, 9, 14]
    x0 = 50 - sum(cw) / 2
    ytop = H - 11

    # header
    cx = x0
    for i, c in enumerate(cols):
        ax.add_patch(Rectangle((cx, ytop - 5.2), cw[i], 5.2, fc=NAVY, ec=NAVY, lw=0.8, zorder=3))
        ax.text(cx + cw[i] / 2, ytop - 2.6, c, ha="center", va="center", fontsize=8.4,
                color=WHITE, fontweight="bold", zorder=4)
        cx += cw[i]
    yy = ytop - 5.2
    for r, row in enumerate(rows):
        cx = x0
        for i, cell in enumerate(row):
            if i == 0:
                bg, tc, wt = LIGHT, NAVY, "bold"
            elif cell == "CAUGHT":
                bg, tc, wt = "#EEF7F1", GREEN, "bold"
            elif cell == "pass" and i > 1:
                bg, tc, wt = "#FDECEF", RED, "bold"
            elif i == 7:
                bg, tc, wt = WHITE, NAVY, "bold"
            else:
                bg, tc, wt = WHITE, BODY, "normal"
            ax.add_patch(Rectangle((cx, yy - 6.4), cw[i], 6.4, fc=bg, ec=GRID, lw=0.8, zorder=3))
            ax.text(cx + cw[i] / 2, yy - 3.2, cell, ha="center", va="center", fontsize=8.6,
                    color=tc, fontweight=wt, zorder=4)
            cx += cw[i]
        yy -= 6.4

    ax.text(x0, yy - 4.0,
            "\"pass\" on a BROKEN design (red) means the testbench MISSED the bug.",
            ha="left", fontsize=9, color=RED, fontweight="bold")
    ax.text(x0, yy - 8.4,
            "\"CAUGHT\" (green) means it failed — which on a broken design is the CORRECT result.",
            ha="left", fontsize=9, color=GREEN, fontweight="bold")
    ax.text(x0, yy - 13.2,
            "A testbench is not finished when it passes. It is finished when it would fail if the design were wrong.",
            ha="left", fontsize=9.4, color=NAVY, fontweight="bold", fontstyle="italic")
    save(f, "clinic_matrix")


if __name__ == "__main__":
    why_verify(); verification_gap(); ver_flow(); directed_vs_random()
    bug_escape(); checker_taxonomy(); coverage_types(); ver_plan(); clinic_matrix()
