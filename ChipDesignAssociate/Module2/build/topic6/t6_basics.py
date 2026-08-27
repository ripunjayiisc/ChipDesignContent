# -*- coding: utf-8 -*-
"""Topic 6 diagrams — the fundamentals of timing."""
import _boot
from dsl import *


# ------------------------------------------------------------ setup/hold
def setup_hold_window():
    W, Hin = 11.5, 6.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 55.7
    title(ax, 50, H - 3, "The one picture the whole topic rests on", 13)
    ax.text(50, H - 7.2, "A flip-flop does not sample \"at\" the clock edge. It samples over a "
                         "WINDOW around it, and the data must be still.",
            fontsize=9, color=SLATE, ha="center")

    xe = 50.0                                # the clock edge
    ctop = H - 13.0                          # clock waveform baseline
    clk_wave(ax, 10, ctop, 26.0, 3, 5.0, color=NAVY, name="clk")
    ax.plot([xe, xe], [17.0, ctop + 6.0], color=RED, lw=1.6, ls="--", zorder=6)
    ax.text(xe, ctop + 7.6, "the active edge", fontsize=8.6, color=RED, ha="center",
            fontweight="bold")

    su, hd = 12.0, 5.5
    wtop, wh = ctop - 5.0, 5.6
    box(ax, xe - su, wtop - wh, su, wh, fc="#FDECEF", ec=RED, lw=1.4)
    box(ax, xe, wtop - wh, hd, wh, fc="#FFF7EC", ec=AMBER, lw=1.4)
    ax.text(xe - su / 2, wtop - wh / 2, "SETUP", fontsize=9, color=RED, ha="center",
            va="center", fontweight="bold")
    ax.text(xe + hd / 2, wtop - wh / 2, "HOLD", fontsize=8.2, color=AMBER, ha="center",
            va="center", fontweight="bold")
    ax.text(xe - su - 1.5, wtop - wh / 2, "data must have\nARRIVED by here", fontsize=8,
            color=RED, ha="right", va="center")
    ax.text(xe + hd + 1.5, wtop - wh / 2, "and must not\nCHANGE until here", fontsize=8,
            color=AMBER, ha="left", va="center")

    wave(ax, 10, ctop - 17.5, 7.0, [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 4.4,
         color=GREEN, name="d")
    ax.text(10, ctop - 21.5, "the data is stable right through the window - this one is fine",
            fontsize=8.2, color=GREEN, ha="left")

    box(ax, 4, 3.0, 92, 13.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 13.4, "Break either half and you get a different failure", fontsize=9.6,
            color=NAVY, fontweight="bold", ha="center")
    ax.text(27, 9.4, "SETUP violated", fontsize=9, color=RED, ha="center", fontweight="bold")
    ax.text(27, 5.8, "the data arrived too LATE.\nFix: a faster path, or a slower clock.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(73, 9.4, "HOLD violated", fontsize=9, color=AMBER, ha="center", fontweight="bold")
    ax.text(73, 5.8, "the data changed too SOON.\nFix: a SLOWER path. The clock cannot help.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "setup_hold_window")


# ------------------------------------------------------------- the path
def timing_path():
    W, Hin = 12.0, 6.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 53.3
    title(ax, 50, H - 3, "Every timing path has exactly four parts", 13)

    ybox = H - 27.0
    label_box(ax, 6, ybox, 15, 11.0, "LAUNCH\nflip-flop", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.5, lw=2.0)
    label_box(ax, 34, ybox, 26, 11.0, "COMBINATIONAL\nLOGIC", fc=LIGHT, ec=TEAL, tc=TEAL,
              size=9.5, lw=2.0)
    label_box(ax, 73, ybox, 15, 11.0, "CAPTURE\nflip-flop", fc=WHITE, ec=NAVY, tc=NAVY,
              size=9.5, lw=2.0)
    arrow(ax, 21, ybox + 5.5, 34, ybox + 5.5, color=SLATE, lw=2.0)
    arrow(ax, 60, ybox + 5.5, 73, ybox + 5.5, color=SLATE, lw=2.0)

    for n, name, x, col in [("1", "clock-to-Q", 13.5, NAVY),
                            ("2", "logic delay", 47.0, TEAL),
                            ("3", "setup time", 80.5, NAVY)]:
        ax.add_patch(Circle((x, ybox + 15.0), 2.2, fc=col, ec=col, zorder=5))
        ax.text(x, ybox + 15.0, n, ha="center", va="center", fontsize=8.6, color=WHITE,
                fontweight="bold", zorder=6)
        ax.text(x, ybox + 19.2, name, ha="center", fontsize=9.2, color=col,
                fontweight="bold")

    wire(ax, [(13.5, ybox), (13.5, ybox - 5.0), (80.5, ybox - 5.0), (80.5, ybox)],
         color=VIOLET, lw=1.8)
    ax.add_patch(Circle((47, ybox - 5.0), 2.2, fc=VIOLET, ec=VIOLET, zorder=5))
    ax.text(47, ybox - 5.0, "4", ha="center", va="center", fontsize=8.6, color=WHITE,
            fontweight="bold", zorder=6)
    ax.text(47, ybox - 8.6, "clock skew - the same clock, but not at the same instant",
            fontsize=8.4, color=VIOLET, ha="center", fontstyle="italic")

    box(ax, 4, 3.0, 92, 11.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 11.2, "and the equation that uses all four", fontsize=9.4, color=GREEN,
            fontweight="bold", ha="center")
    ax.text(50, 7.2, "setup slack  =  ( period + skew - setup - uncertainty )  -  "
                     "( clock-to-Q + logic delay )",
            fontsize=10, color=NAVY, ha="center", family="monospace")
    ax.text(50, 4.4, "|________ required time ________|      |______ arrival time ______|",
            fontsize=8.0, color=SLATE, ha="center", family="monospace")
    save(f, "timing_path")


# --------------------------------------------------------------- slack
def slack_equation():
    W, Hin = 11.5, 6.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 55.7
    title(ax, 50, H - 3, "Slack is a subtraction, and that is all it is", 13)

    ytop = H - 10.0
    ax.text(4, ytop, "ARRIVAL", fontsize=9.6, color=TEAL, fontweight="bold", ha="left")
    ax.text(4, ytop - 3.4, "when the data actually turns up", fontsize=8.2, color=SLATE,
            ha="left")
    x = 20
    for nm, wd, col in [("clock-to-Q", 10, NAVY), ("logic", 34, TEAL)]:
        box(ax, x, ytop - 9.0, wd, 5.0, fc=col, ec=col, r=0.4)
        ax.text(x + wd / 2, ytop - 6.5, nm, ha="center", va="center", fontsize=8.4,
                color=WHITE, fontweight="bold")
        x += wd

    ax.text(4, ytop - 15.0, "REQUIRED", fontsize=9.6, color=GREEN, fontweight="bold",
            ha="left")
    ax.text(4, ytop - 18.4, "when it had to be there by", fontsize=8.2, color=SLATE, ha="left")
    box(ax, 20, ytop - 24.0, 62, 5.0, fc="#EEF7F1", ec=GREEN, lw=1.6, r=0.4)
    ax.text(51, ytop - 21.5, "clock period", ha="center", va="center", fontsize=8.6,
            color=GREEN, fontweight="bold")
    box(ax, 82, ytop - 24.0, 8, 5.0, fc=RED, ec=RED, r=0.4)
    ax.text(86, ytop - 21.5, "setup", ha="center", va="center", fontsize=7.4, color=WHITE,
            fontweight="bold")

    ax.plot([64, 64], [ytop - 27.5, ytop - 3.0], color=SLATE, lw=1.0, ls=":")
    ax.plot([82, 82], [ytop - 27.5, ytop - 3.0], color=SLATE, lw=1.0, ls=":")
    arrow(ax, 64, ytop - 27.0, 82, ytop - 27.0, color=GREEN, lw=2.0, style="<|-|>")
    ax.text(73, ytop - 30.6, "SLACK", ha="center", fontsize=10, color=GREEN,
            fontweight="bold")

    box(ax, 4, 2.5, 92, 9.5, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 9.4, "Positive slack means it fits. Negative slack means it does not, "
                     "and the number is by how much.",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 5.2, "WNS is the WORST slack in the design. TNS adds up every negative slack, "
                     "so it says how BIG the problem is, not just how bad.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "slack_equation")


# --------------------------------------------------------------- setup vs hold
def setup_vs_hold():
    W, Hin = 11.5, 6.3
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 54.8
    title(ax, 50, H - 3, "Setup and hold are opposite problems", 13)

    ptop, pbot = H - 8.0, 7.0
    for x0, col, fcol, nm, sub in [
            (3, RED, "#FDECEF", "SETUP", "the data was too LATE"),
            (52, AMBER, "#FFF7EC", "HOLD", "the data changed too SOON")]:
        box(ax, x0, pbot, 45, ptop - pbot, fc=fcol, ec=col, lw=1.8)
        ax.text(x0 + 22.5, ptop - 4.0, nm, fontsize=12, color=col, ha="center",
                fontweight="bold")
        ax.text(x0 + 22.5, ptop - 8.4, sub, fontsize=9, color=col, ha="center",
                fontstyle="italic")

    rows = [("Checked against", "the NEXT clock edge", "the SAME clock edge"),
            ("Uses the period", "yes", "no - not at all"),
            ("Caused by", "too much logic between flops",
             "too little logic, plus skew"),
            ("Fixed by", "less logic, or a slower clock",
             "ADDING delay to the data path"),
            ("Slowing the clock", "helps", "does nothing whatever"),
            ("Found at", "synthesis, then again after layout",
             "layout, when skew is finally known")]
    y = ptop - 13.5
    for a, b, c in rows:
        ax.text(5.5, y, a, fontsize=8.3, color=NAVY, ha="left", fontweight="bold")
        ax.text(21.0, y, b, fontsize=8.3, color=BODY, ha="left")
        ax.text(54.5, y, a, fontsize=8.3, color=NAVY, ha="left", fontweight="bold")
        ax.text(70.0, y, c, fontsize=8.3, color=BODY, ha="left")
        y -= 4.2

    ax.text(50, 3.4, "A chip with a setup violation runs slower.", fontsize=9.2,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 0.8, "A chip with a hold violation does not work at any speed.", fontsize=9.2,
            color=RED, ha="center", fontweight="bold")
    save(f, "setup_vs_hold")


# ------------------------------------------------------------- skew
def clock_skew():
    W, Hin = 11.5, 6.7
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 58.3
    title(ax, 50, H - 3, "Clock skew helps setup and hurts hold", 12.5)
    ax.text(50, H - 7.0, "The clock does not arrive everywhere at once. The difference between "
                         "two registers is SKEW.",
            fontsize=9, color=SLATE, ha="center")

    ytop = H - 11.5
    label_box(ax, 42, ytop - 5.0, 16, 5.0, "clock source", fc=WHITE, ec=VIOLET, tc=VIOLET,
              size=8.6)
    wire(ax, [(50, ytop - 5.0), (50, ytop - 8.0)], color=VIOLET, lw=1.8)
    wire(ax, [(22, ytop - 8.0), (78, ytop - 8.0)], color=VIOLET, lw=1.8)
    wire(ax, [(22, ytop - 8.0), (22, ytop - 11.0)], color=VIOLET, lw=1.8)
    wire(ax, [(78, ytop - 8.0), (78, ytop - 14.5)], color=VIOLET, lw=2.6)
    label_box(ax, 14, ytop - 17.0, 16, 6.0, "launch\nflop", fc=WHITE, ec=NAVY, tc=NAVY,
              size=8.4)
    label_box(ax, 70, ytop - 20.5, 16, 6.0, "capture\nflop", fc=WHITE, ec=NAVY, tc=NAVY,
              size=8.4)
    ax.text(88, ytop - 12.0, "this branch is\nlonger: +0.30 ns", fontsize=8.2, color=VIOLET,
            ha="left", va="center", fontstyle="italic")

    box(ax, 4, 3.5, 45, 18.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(26.5, 19.0, "For SETUP, a late capture clock HELPS", fontsize=9, color=GREEN,
            ha="center", fontweight="bold")
    ax.text(26.5, 13.0, "The capture edge arrives later, so the\ndata has longer to get there.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(26.5, 8.6, "slack = period + skew - setup - arrival", fontsize=8.2, color=NAVY,
            ha="center", family="monospace")
    ax.text(26.5, 5.2, "Designers sometimes add skew ON PURPOSE.\nIt is called useful skew.",
            fontsize=8.2, color=GREEN, ha="center", fontstyle="italic")

    box(ax, 52, 3.5, 44, 18.0, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(74, 19.0, "For HOLD, the same skew HURTS", fontsize=9, color=RED, ha="center",
            fontweight="bold")
    ax.text(74, 13.0, "The capture edge arrives later, so the\nNEW data may already be there.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(74, 8.6, "slack = arrival - skew - hold", fontsize=8.2, color=NAVY,
            ha="center", family="monospace")
    ax.text(74, 5.2, "This is why hold problems appear only after\nlayout: before it, skew is a guess.",
            fontsize=8.2, color=RED, ha="center", fontstyle="italic")
    save(f, "clock_skew")


# ------------------------------------------------------- jitter/uncertainty
def uncertainty():
    W, Hin = 11.5, 5.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 43.5
    title(ax, 50, H - 3, "Uncertainty — margin for what you have not modelled", 12.5)

    ctop = H - 12.0
    clk_wave(ax, 12, ctop, 24.0, 3, 5.0, color=NAVY, name="ideal clk")
    for k in range(3):
        xe = 12 + 12.0 + k * 24.0
        if xe > 90:
            break
        box(ax, xe - 2.6, ctop - 1.5, 5.2, 9.0, fc=RED, ec="none", z=1)
    ax.text(50, ctop - 4.6, "the real edge lands somewhere in the red band, and it moves "
                            "from cycle to cycle",
            fontsize=8.6, color=RED, ha="center")

    items = [("JITTER", "the oscillator and the PLL are not\nperfect; the edge moves a little\n"
              "every cycle", RED),
             ("SKEW NOT YET\nMODELLED", "before layout the clock tree does\nnot exist yet - "
              "uncertainty\nstands in for it", AMBER),
             ("MARGIN", "a deliberate safety factor, so that\n\"met\" in the report means\n"
              "\"met\" on silicon", GREEN)]
    bw = 29.0
    x0 = 50 - (3 * bw + 2 * 3.5) / 2
    for i, (nm, sub, col) in enumerate(items):
        x = x0 + i * (bw + 3.5)
        box(ax, x, 7.0, bw, 16.5, fc=WHITE, ec=col, lw=1.7)
        box(ax, x, 17.5, bw, 6.0, fc=col, ec=col)
        ax.text(x + bw / 2, 20.5, nm, ha="center", va="center", fontsize=8.6, color=WHITE,
                fontweight="bold")
        ax.text(x + bw / 2, 12.0, sub, ha="center", va="center", fontsize=8.0, color=BODY)
    ax.text(50, 3.6, "set_clock_uncertainty 0.15 -setup        set_clock_uncertainty 0.05 -hold",
            fontsize=8.8, color=NAVY, ha="center", family="monospace")
    ax.text(50, 0.8, "Take it out and the report gets better while the chip does not.",
            fontsize=8.6, color=SLATE, ha="center", fontstyle="italic")
    save(f, "uncertainty")


if __name__ == "__main__":
    setup_hold_window(); timing_path(); slack_equation(); setup_vs_hold()
    clock_skew(); uncertainty()
