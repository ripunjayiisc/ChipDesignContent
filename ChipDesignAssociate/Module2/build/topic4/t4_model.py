# -*- coding: utf-8 -*-
"""Topic 4b diagrams: modelling combinational and sequential logic in HDL."""
import _boot
from dsl import *
import numpy as np


def three_constructs():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "The three ways to describe logic — and what each becomes", 13.0, NAVY)
    cards = [("assign", TEAL, "#E8F5F7", "continuous assignment",
              ["Drives a  wire , continuously.", "The right-hand side is re-evaluated",
               "whenever ANY operand changes.", "", "Always combinational.",
               "Cannot infer a flip-flop or a latch."],
              "assign y = a & b;"),
             ("always @(*)", AMBER, "#FFF6EC", "combinational procedural block",
              ["Drives a  reg , but builds GATES.", "Re-runs whenever any signal it READS",
               "changes — @(*) works that out for you.", "",
               "Combinational IF you assign every", "output on every path. Otherwise: LATCH."],
              "always @(*) y = a & b;"),
             ("always @(posedge clk)", GREEN, "#E4F4EC", "sequential procedural block",
              ["Drives a  reg , and builds", "FLIP-FLOPS — one per bit assigned.", "",
               "Runs ONLY on the clock edge.", "Use non-blocking  <=  here,",
               "always, without exception."],
              "always @(posedge clk) q <= d;")]
    cw = 31.4
    for i, (nm, c, bg, sub, lines, code) in enumerate(cards):
        x = 2.0 + i * (cw + 1.5)
        box(ax, x, 5.0, cw, 29.0, fc=bg, ec=c, lw=1.9)
        ax.add_patch(FancyBboxPatch((x, 29.0), cw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 29.0), cw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, 31.5, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=6, family="DejaVu Sans Mono")
        ax.text(x + cw / 2, 26.8, sub, ha="center", va="center", fontsize=8.6,
                color=c, fontweight="bold")
        for j, ln in enumerate(lines):
            if not ln:
                continue
            ax.text(x + 1.6, 23.6 - j * 2.5, ln, ha="left", va="center", fontsize=8.0, color=BODY)
        box(ax, x + 1.4, 6.0, cw - 2.8, 3.6, fc="#11212F", ec="#11212F", r=0.6)
        ax.text(x + cw / 2, 7.8, code, ha="center", va="center", fontsize=7.8,
                color="#DCE6F0", family="DejaVu Sans Mono")
    ax.text(50, 2.4, "Choosing between them is not a style question. It decides whether you get "
            "wires, gates, or registers.",
            ha="center", va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    save(f, "three_constructs")


def latch_inference():
    W, Hin = 13, 5.4
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 41.54
    title(ax, 50, H - 2.0, "The inferred latch — the most common beginner bug in RTL", 13.0, NAVY)
    # WRONG
    box(ax, 2.0, 21.0, 46.5, 17.0, fc="#FDECEF", ec=RED, lw=1.9)
    ax.text(25.25, 36.4, "WRONG — incomplete assignment", ha="center", va="center",
            fontsize=10.2, color=RED, fontweight="bold")
    bad = ["always @(*) begin", "    if (sel)", "        y = a;", "end"]
    for i, ln in enumerate(bad):
        ax.text(5.0, 33.2 - i * 2.2, ln, ha="left", va="center", fontsize=9.0,
                color=BODY, family="DejaVu Sans Mono")
    ax.text(25.25, 23.6, "sel = 0  →  y is not assigned  →  'hold the old y'\n"
            "→  the only thing that can hold a value is a LATCH",
            ha="center", va="center", fontsize=8.4, color=RED, fontweight="bold", linespacing=1.6)
    # RIGHT
    box(ax, 51.5, 21.0, 46.5, 17.0, fc="#E4F4EC", ec=GREEN, lw=1.9)
    ax.text(74.75, 36.4, "RIGHT — default first", ha="center", va="center",
            fontsize=10.2, color=GREEN, fontweight="bold")
    good = ["always @(*) begin", "    y = 1'b0;      // default", "    if (sel)", "        y = a;", "end"]
    for i, ln in enumerate(good):
        ax.text(54.5, 33.6 - i * 2.2, ln, ha="left", va="center", fontsize=9.0,
                color=BODY, family="DejaVu Sans Mono")
    ax.text(74.75, 23.0, "every path assigns y  →  pure gates, a 2:1 MUX",
            ha="center", va="center", fontsize=8.6, color=GREEN, fontweight="bold")

    # the three rules
    box(ax, 2.0, 9.0, 96.0, 10.2, fc=LIGHT, ec=TEAL, lw=1.7)
    ax.text(50, 17.6, "Three rules that make an accidental latch impossible", ha="center",
            va="center", fontsize=10, color=TEAL, fontweight="bold")
    rules = ["1.  Assign every output a DEFAULT value at the top of the block.",
             "2.  Give every  case  a  default:  branch — even if it is unreachable.",
             "3.  Never write a bare  if  without an  else  in a combinational block."]
    for i, r in enumerate(rules):
        ax.text(6.0, 14.6 - i * 2.2, r, ha="left", va="center", fontsize=9.0, color=NAVY)

    box(ax, 2.0, 1.2, 96.0, 7.0, fc="#FFF6EC", ec=AMBER, lw=1.6)
    ax.text(50, 6.4, "How to catch one", ha="center", va="center", fontsize=9.6,
            color=AMBER, fontweight="bold")
    ax.text(50, 3.4, "Yosys prints  $_DLATCH_  cells in  stat .   Vivado logs  "
            "'[Synth 8-327] inferring latch for variable y'.\n"
            "ModelSim and Verilator warn too. Treat EVERY such message as an error, never a warning.",
            ha="center", va="center", fontsize=8.4, color=BODY, linespacing=1.7)
    save(f, "latch_inference")


def blocking_nonblocking():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 43.08
    title(ax, 50, H - 2.0, "Blocking vs non-blocking — same code, different hardware", 13.0, NAVY)

    def ff(xx, cy, c, lab):
        box(ax, xx, cy - 2.5, 8.0, 5.0, fc=WHITE, ec=c, lw=1.7, r=0.6)
        ax.add_patch(Polygon([(xx, cy - 0.9), (xx + 1.4, cy - 1.5), (xx, cy - 2.1)],
                             fc="none", ec=c, lw=1.2, zorder=6))
        ax.text(xx + 2.6, cy + 1.2, "D", ha="center", va="center", fontsize=7.0,
                color=NAVY, family="DejaVu Sans Mono")
        ax.text(xx + 6.2, cy + 1.2, "Q", ha="center", va="center", fontsize=7.0,
                color=NAVY, family="DejaVu Sans Mono")
        ax.text(xx + 4.0, cy - 1.4, lab, ha="center", va="center", fontsize=8.4,
                color=c, fontweight="bold")

    cy = 24.0
    # ---------- left: non-blocking -> two flip-flops ----------
    box(ax, 2.0, 19.0, 46.5, 19.5, fc="#E4F4EC", ec=GREEN, lw=1.9)
    ax.text(25.25, 36.8, "NON-BLOCKING  <=   →  two flip-flops", ha="center", va="center",
            fontsize=10.0, color=GREEN, fontweight="bold")
    for i, ln in enumerate(["always @(posedge clk) begin", "    q1 <= d;", "    q2 <= q1;", "end"]):
        ax.text(5.0, 34.0 - i * 1.9, ln, ha="left", va="center", fontsize=8.4,
                color=BODY, family="DejaVu Sans Mono")
    ff(11.0, cy, GREEN, "q1")
    ff(27.0, cy, GREEN, "q2")
    arrow(ax, 6.6, cy + 1.2, 10.8, cy + 1.2, color=INK, lw=1.5, ms=9)
    ax.text(6.0, cy + 1.2, "d", ha="right", va="center", fontsize=9, color=NAVY, fontweight="bold")
    arrow(ax, 19.2, cy + 1.2, 26.8, cy + 1.2, color=INK, lw=1.5, ms=9)
    arrow(ax, 35.2, cy + 1.2, 39.6, cy + 1.2, color=INK, lw=1.5, ms=9)
    ax.text(40.2, cy + 1.2, "q2", ha="left", va="center", fontsize=9, color=GREEN, fontweight="bold")
    ax.text(25.25, 20.2, "each <= reads the OLD value  →  a true two-stage shift register",
            ha="center", va="center", fontsize=7.8, color=GREEN, fontweight="bold")

    # ---------- right: blocking -> one flip-flop ----------
    box(ax, 51.5, 19.0, 46.5, 19.5, fc="#FDECEF", ec=RED, lw=1.9)
    ax.text(74.75, 36.8, "BLOCKING  =   →  ONE flip-flop", ha="center", va="center",
            fontsize=10.0, color=RED, fontweight="bold")
    for i, ln in enumerate(["always @(posedge clk) begin", "    q1 = d;", "    q2 = q1;", "end"]):
        ax.text(54.5, 34.0 - i * 1.9, ln, ha="left", va="center", fontsize=8.4,
                color=BODY, family="DejaVu Sans Mono")
    ff(66.0, cy, RED, "q1=q2")
    arrow(ax, 61.6, cy + 1.2, 65.8, cy + 1.2, color=INK, lw=1.5, ms=9)
    ax.text(61.0, cy + 1.2, "d", ha="right", va="center", fontsize=9, color=NAVY, fontweight="bold")
    wire(ax, [(74.2, cy + 1.2), (80.0, cy + 1.2)], color=INK, lw=1.5)
    dot(ax, 78.0, cy + 1.2)
    ax.text(80.8, cy + 2.6, "q1", ha="left", va="center", fontsize=9, color=RED, fontweight="bold")
    ax.text(80.8, cy - 0.2, "q2", ha="left", va="center", fontsize=9, color=RED, fontweight="bold")
    ax.text(74.75, 20.2, "q1 updates at once, so q2 gets d too — and the order becomes a RACE",
            ha="center", va="center", fontsize=7.8, color=RED, fontweight="bold")

    # ---------- the rule ----------
    box(ax, 2.0, 8.0, 96.0, 9.0, fc=LIGHT, ec=NAVY, lw=1.8)
    ax.text(50, 15.4, "The rule — no exceptions, ever", ha="center", va="center",
            fontsize=10.5, color=NAVY, fontweight="bold")
    ax.text(27.0, 12.2, "always @(posedge clk)", ha="center", va="center", fontsize=9.4,
            color=NAVY, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(27.0, 9.8, "use  <=  (non-blocking)", ha="center", va="center", fontsize=9.4,
            color=GREEN, fontweight="bold")
    ax.text(73.0, 12.2, "always @(*)", ha="center", va="center", fontsize=9.4,
            color=NAVY, family="DejaVu Sans Mono", fontweight="bold")
    ax.text(73.0, 9.8, "use  =  (blocking)", ha="center", va="center", fontsize=9.4,
            color=GREEN, fontweight="bold")
    ax.text(50, 5.6, "Never mix the two in one block.   Never assign the same signal from two blocks.",
            ha="center", va="center", fontsize=9.2, color=RED, fontweight="bold")
    ax.text(50, 2.6, "Why it works: non-blocking assignments sample every right-hand side FIRST, "
            "then update together at the end of the time step —\nwhich is exactly what a bank of "
            "flip-flops does on a clock edge.",
            ha="center", va="center", fontsize=8.4, color=BODY, linespacing=1.7)
    save(f, "blocking_nonblocking")


def event_queue():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 38.46
    title(ax, 50, H - 2.0, "Why the rule works — Verilog's event queue for one time step", 13.0, NAVY)
    regions = [("ACTIVE", TEAL,
                "blocking assignments  =\ncontinuous assign\n\\$display, gate evaluation"),
               ("INACTIVE", SLATE, "#0 delayed events\n(never use these in RTL)"),
               ("NBA", GREEN,
                "NON-BLOCKING updates  <=\nare APPLIED here"),
               ("MONITOR", AMBER, "\\$monitor, \\$strobe\nread the settled values")]
    bw = 22.6
    for i, (nm, c, desc) in enumerate(regions):
        x = 2.0 + i * (bw + 1.5)
        box(ax, x, 14.0, bw, 15.0, fc=LIGHT, ec=c, lw=1.8)
        ax.add_patch(FancyBboxPatch((x, 24.5), bw, 4.5,
                     boxstyle="round,pad=0,rounding_size=1.1", fc=c, ec=c, lw=1.1, zorder=3))
        ax.add_patch(Rectangle((x, 24.5), bw, 2.3, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + bw / 2, 26.8, nm, ha="center", va="center", fontsize=10,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + bw / 2, 19.0, desc, ha="center", va="center", fontsize=8.0,
                color=BODY, linespacing=1.7)
        ax.text(x + bw / 2, 30.6, "%d" % (i + 1), ha="center", va="center", fontsize=9.4,
                color=c, fontweight="bold")
        if i < 3:
            arrow(ax, x + bw + 0.2, 21.5, x + bw + 1.3, 21.5, color=SLATE, lw=1.8, ms=10)
    ax.text(50, 32.8, "the simulator empties region 1 completely, THEN region 2, and so on — "
            "all at the same simulation time",
            ha="center", va="center", fontsize=9.0, color=SLATE, style="italic")

    box(ax, 2.0, 2.0, 96.0, 10.5, fc="#E4F4EC", ec=GREEN, lw=1.7)
    ax.text(50, 10.8, "Trace  q1 <= d;  q2 <= q1;  through one clock edge", ha="center",
            va="center", fontsize=9.8, color=GREEN, fontweight="bold")
    steps = ["ACTIVE:  both right-hand sides are SAMPLED — d and the OLD q1 are read and held",
             "NBA:     both left-hand sides are UPDATED — q1 gets d, q2 gets the OLD q1",
             "Result:  two flip-flops in series, and the answer does not depend on the order you wrote the lines"]
    for i, st in enumerate(steps):
        ax.text(6.0, 7.6 - i * 2.2, st, ha="left", va="center", fontsize=8.6,
                color=NAVY if i < 2 else GREEN, fontweight="bold" if i == 2 else "normal",
                family="DejaVu Sans Mono" if i < 2 else "DejaVu Sans")
    save(f, "event_queue")


def seq_template():
    W, Hin = 13, 6.0
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 46.15
    title(ax, 50, H - 2.0, "The four sequential templates you will use every day", 13.0, NAVY)
    tmpl = [("Plain register", TEAL,
             ["always @(posedge clk)", "    q <= d;"],
             "no reset — pipeline stages only"),
            ("Synchronous reset", TEAL,
             ["always @(posedge clk)", "    if (!rst_n) q <= 4'd0;", "    else        q <= d;"],
             "reset is one more input to the D logic"),
            ("Asynchronous reset", AMBER,
             ["always @(posedge clk or negedge rst_n)", "    if (!rst_n) q <= 4'd0;",
              "    else        q <= d;"],
             "works with no clock — the ASIC choice"),
            ("Async reset + clock enable", GREEN,
             ["always @(posedge clk or negedge rst_n)", "    if (!rst_n)   q <= 4'd0;",
              "    else if (en)  q <= d;"],
             "THE workhorse — use this by default")]
    y = H - 4.8
    for nm, c, lines, note in tmpl:
        hgt = 1.2 + 1.75 * len(lines) + 1.4
        box(ax, 2.0, y - hgt, 96.0, hgt, fc=LIGHT, ec=c, lw=1.5)
        box(ax, 2.0, y - hgt, 27.0, hgt, fc=c, ec=c)
        ax.text(15.5, y - hgt / 2 + 1.3, nm, ha="center", va="center", fontsize=9.6,
                color="white", fontweight="bold")
        ax.text(15.5, y - hgt / 2 - 1.8, note, ha="center", va="center", fontsize=6.6,
                color="white")
        for j, ln in enumerate(lines):
            ax.text(31.0, y - 2.2 - j * 1.75, ln, ha="left", va="center", fontsize=8.6,
                    color=BODY, family="DejaVu Sans Mono")
        y -= hgt + 0.8
    box(ax, 2.0, 1.0, 96.0, 6.4, fc="#FDECEF", ec=RED, lw=1.6)
    ax.text(50, 5.6, "Two things that are ALWAYS wrong in a clocked block", ha="center",
            va="center", fontsize=9.6, color=RED, fontweight="bold")
    ax.text(50, 2.8, "Anything except clk and an async reset in the sensitivity list.        "
            "Using  =  instead of  <=.",
            ha="center", va="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "seq_template")


def fsm_styles():
    W, Hin = 13, 5.2
    f, ax = fig(W, Hin); H = 100 * Hin / W                 # 40.0
    title(ax, 50, H - 2.0, "Three FSM coding styles — and which one to standardise on", 13.0, NAVY)
    styles = [("ONE block", RED, "#FDECEF",
               ["Everything in one", "always @(posedge clk)", "", "State AND outputs are",
                "registered together.", "", "Compact — and the hardest", "to read or to debug."],
               "avoid"),
              ("TWO blocks", AMBER, "#FFF6EC",
               ["Block 1: state register", "Block 2: next-state AND", "                 output logic",
                "", "Fewer lines than three,", "but mixes two concerns", "in one always block."],
               "acceptable"),
              ("THREE blocks", GREEN, "#E4F4EC",
               ["Block 1: state register", "Block 2: next-state logic", "Block 3: output logic",
                "", "Matches the Huffman model", "exactly. Each block is short", "enough to read at a glance."],
               "USE THIS")]
    cw = 31.4
    for i, (nm, c, bg, lines, verdict) in enumerate(styles):
        x = 2.0 + i * (cw + 1.5)
        box(ax, x, 7.0, cw, 28.0, fc=bg, ec=c, lw=1.9)
        ax.add_patch(FancyBboxPatch((x, 30.0), cw, 5.0,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, 30.0), cw, 2.5, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cw / 2, 32.5, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=6)
        for j, ln in enumerate(lines):
            if not ln:
                continue
            ax.text(x + 2.0, 27.0 - j * 2.1, ln, ha="left", va="center", fontsize=8.2,
                    color=BODY, family="DejaVu Sans Mono" if "always" in ln or "Block" in ln
                    else "DejaVu Sans")
        box(ax, x + 6.0, 7.7, cw - 12.0, 3.2, fc=c, ec=c, r=0.8)
        ax.text(x + cw / 2, 9.3, verdict, ha="center", va="center", fontsize=9.4,
                color="white", fontweight="bold")
    box(ax, 2.0, 1.0, 96.0, 5.4, fc=LIGHT, ec=TEAL, lw=1.6)
    ax.text(50, 3.7, "All three synthesise to the same gates. The difference is how easily a "
            "human — including you, in six months — can read and change it.",
            ha="center", va="center", fontsize=8.8, color=NAVY, fontweight="bold")
    save(f, "fsm_styles")


if __name__ == "__main__":
    three_constructs(); latch_inference(); blocking_nonblocking()
    event_queue(); seq_template(); fsm_styles()
