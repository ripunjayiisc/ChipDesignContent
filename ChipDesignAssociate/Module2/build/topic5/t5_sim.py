# -*- coding: utf-8 -*-
"""Topic 5 diagrams — simulation engine, waveforms and debugging."""
import _boot
from dsl import *


# ------------------------------------------------------------- sim engine
def sim_engine():
    W, Hin = 11.5, 5.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 43.5
    title(ax, 50, H - 3, "How a simulator actually works — events, not instructions", 12.5)
    ax.text(50, H - 7.2, "A digital simulator does not step through your code. It keeps a "
                         "queue of scheduled EVENTS, ordered by time.",
            fontsize=9, color=SLATE, ha="center")

    # time wheel
    ts = [0, 5, 10, 15, 20]
    x0, bw, gap = 6, 15.0, 3.0
    ytop = H - 12.0
    for i, t in enumerate(ts):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 8.0, bw, 8.0, fc=WHITE, ec=TEAL, lw=1.7)
        box(ax, x, ytop - 3.4, bw, 3.4, fc=TEAL, ec=TEAL)
        ax.text(x + bw / 2, ytop - 1.7, "t = %d ns" % t, ha="center", va="center",
                fontsize=8.4, color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ytop - 5.8, ["clk 0->1", "clk 1->0", "clk 0->1",
                                         "clk 1->0", "clk 0->1"][i],
                ha="center", va="center", fontsize=8.0, color=BODY, family="monospace")
        if i < len(ts) - 1:
            arrow(ax, x + bw, ytop - 4.0, x + bw + gap, ytop - 4.0, color=SLATE, lw=1.6)

    ax.text(50, ytop - 11.0,
            "At each time the simulator wakes only the blocks SENSITIVE to what changed, "
            "runs them to completion, and moves on.",
            fontsize=8.8, color=BODY, ha="center")

    # two consequences
    box(ax, 4, 3.0, 45, 15.5, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(26.5, 16.0, "Why this is fast", fontsize=9.4, color=GREEN,
            fontweight="bold", ha="center")
    ax.text(26.5, 9.0, "Nothing is evaluated unless one of its\ninputs changed. A design "
                        "that is mostly idle\ncosts almost nothing to simulate — which is\nwhy "
                        "a clock that never stops is expensive.",
            fontsize=8.4, color=BODY, ha="center")

    box(ax, 52, 3.0, 44, 15.5, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(74, 16.0, "Why time can stand still", fontsize=9.4, color=AMBER,
            fontweight="bold", ha="center")
    ax.text(74, 9.0, "Several events can be scheduled at the\nSAME simulation time. The "
                      "simulator works\nthrough them all before the clock advances.\n"
                      "That is where races come from.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "sim_engine")


# ---------------------------------------------------------- event regions
def event_regions():
    W, Hin = 11.5, 6.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 53.9
    title(ax, 50, H - 3, "Inside ONE time step — the stratified event queue", 12.5)
    ax.text(50, H - 7.2, "This is why <= works, and why \\$display and \\$strobe can print "
                         "different things at the same instant.",
            fontsize=9, color=SLATE, ha="center")

    regions = [("ACTIVE", TEAL,
                "blocking assignments (=)\nevaluate every <= right-hand side\ncontinuous assigns\n\\$display"),
               ("INACTIVE", SLATE, "anything scheduled with #0\n\n(avoid using this)"),
               ("NBA", GREEN,
                "non-blocking assignments\nare APPLIED to their\nleft-hand sides"),
               ("MONITOR", AMBER, "\\$monitor and \\$strobe\nrun here — after\neverything settled")]
    bw, gap = 21.0, 3.5
    x0 = 50 - (4 * bw + 3 * gap) / 2
    ytop = H - 11.5
    for i, (name, col, body) in enumerate(regions):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 21.0, bw, 21.0, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, ytop - 4.6, bw, 4.6, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.3, name, ha="center", va="center", fontsize=9.2,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ytop - 13.0, body, ha="center", va="center", fontsize=8.0,
                color=BODY)
        if i < 3:
            arrow(ax, x + bw, ytop - 10.5, x + bw + gap, ytop - 10.5, color=SLATE, lw=1.8)

    box(ax, 4, 4.0, 92, 12.5, fc=LIGHT, ec=GREEN, lw=1.6)
    ax.text(50, 13.6, "What the separation buys you", fontsize=9.6, color=GREEN,
            fontweight="bold", ha="center")
    ax.text(50, 9.4, "Every clocked block samples its inputs in ACTIVE, using values from BEFORE "
                     "the edge; every register updates later, in NBA.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 6.0, "So no clocked block sees another block's new value on the same edge — "
                     "exactly like real flip-flops.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "event_regions")


# ------------------------------------------------------- compile/elab/run
def compile_elab_run():
    W, Hin = 11.5, 5.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 48.7
    title(ax, 50, H - 3, "Every simulator does the same three steps", 12.5)

    steps = [("ANALYSE", "read the source,\ncheck the syntax,\nbuild each module", TEAL),
             ("ELABORATE", "build the hierarchy,\nresolve parameters,\nconnect the wires", VIOLET),
             ("RUN", "execute the event\nqueue until \\$finish", GREEN)]
    bw, gap = 24.0, 6.0
    x0 = 50 - (3 * bw + 2 * gap) / 2
    ytop = H - 8.5
    for i, (name, body, col) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 13.0, bw, 13.0, fc=WHITE, ec=col, lw=1.9)
        box(ax, x, ytop - 4.4, bw, 4.4, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.2, name, ha="center", va="center", fontsize=9.6,
                color=WHITE, fontweight="bold")
        ax.text(x + bw / 2, ytop - 8.8, body, ha="center", va="center", fontsize=8.4,
                color=BODY)
        if i < 2:
            arrow(ax, x + bw, ytop - 6.5, x + bw + gap, ytop - 6.5, color=SLATE, lw=2.0)

    cols = ["", "analyse", "elaborate", "run"]
    rows = [["Icarus Verilog", "iverilog -o sim.vvp ...", "(part of iverilog)", "vvp sim.vvp"],
            ["Verilator", "verilator --binary ...", "(part of the build)", "./obj_dir/<top>"],
            ["Vivado xsim", "xvlog <files>", "xelab -debug typical <top>", "xsim <snap> -runall"],
            ["ModelSim / Questa", "vlog <files>", "(part of vsim)", "vsim -c work.<top>; run -all"]]
    cw = [22, 24, 24, 26]
    table(ax, 50 - sum(cw) / 2, ytop - 16.5, cols, rows, cw, 4.3, size=8.0, bold_col=0)
    save(f, "compile_elab_run")


# --------------------------------------------------------------- vcd flow
def vcd_flow():
    W, Hin = 11.5, 4.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 36.5
    title(ax, 50, H - 3, "How a waveform gets onto your screen", 12.5)

    items = [("YOUR TESTBENCH", "\\$dumpfile(\"v3.vcd\");\n\\$dumpvars(0, tb);", TEAL),
             ("THE SIMULATOR", "writes a line every\ntime a signal changes", NAVY),
             ("dump.vcd", "a plain text file.\nIt can be enormous.", AMBER),
             ("GTKWave", "reads it, draws it,\nand searches it", GREEN)]
    bw, gap = 20.0, 5.0
    x0 = 50 - (4 * bw + 3 * gap) / 2
    ytop = H - 8.0
    for i, (name, body, col) in enumerate(items):
        x = x0 + i * (bw + gap)
        box(ax, x, ytop - 12.5, bw, 12.5, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, ytop - 4.3, bw, 4.3, fc=col, ec=col)
        ax.text(x + bw / 2, ytop - 2.15, name, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold", family="monospace" if "." in name else "sans-serif")
        ax.text(x + bw / 2, ytop - 8.6, body, ha="center", va="center", fontsize=8.0,
                color=BODY, family="monospace" if "dump" in body else "sans-serif")
        if i < 3:
            arrow(ax, x + bw, ytop - 6.3, x + bw + gap, ytop - 6.3, color=SLATE, lw=1.9)

    box(ax, 4, 2.5, 92, 13.0, fc="#FFF7EC", ec=AMBER, lw=1.6)
    ax.text(50, 13.2, "Dumping is usually the most expensive thing your simulation does",
            fontsize=9.4, color=AMBER, fontweight="bold", ha="center")
    ax.text(50, 9.6, "\\$dumpvars(0, tb);  dumps every signal at every level — start here, on one test.",
            fontsize=8.4, color=BODY, ha="center", family="monospace")
    ax.text(50, 6.4, "\\$dumpvars(1, tb.u_dut);  dumps one level of one instance — for when the file gets too big to open.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(50, 4.2, "A regression dumps NOTHING, and re-runs only the failing seed with dumping switched on.",
            fontsize=8.4, color=NAVY, ha="center", fontweight="bold")
    save(f, "vcd_flow")


# ------------------------------------------------------------ gtkwave tour
def gtkwave_tour():
    W, Hin = 13.0, 4.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 35.4
    title(ax, 50, H - 2.8, "Reading a waveform viewer", 12.5)

    wtop, wbot = H - 6.5, 2.5
    box(ax, 3, wbot, 94, wtop - wbot, fc=WHITE, ec=NAVY, lw=1.8)
    box(ax, 3, wtop - 3.8, 94, 3.8, fc=NAVY, ec=NAVY)
    ax.text(5.5, wtop - 1.9, "GTKWave   —   v3.vcd", fontsize=7.8, color=WHITE,
            ha="left", fontweight="bold")

    ptop, pbot = wtop - 5.2, wbot + 2.0
    box(ax, 5, pbot, 19, ptop - pbot, fc=LIGHT, ec=GRID)
    box(ax, 25, pbot, 70, ptop - pbot, fc=WHITE, ec=GRID)

    rows = [("clk",           None,  NAVY),
            ("rst_n",         [0, 1, 1, 1, 1, 1, 1, 1], GREEN),
            ("wr_en",         [0, 0, 1, 1, 0, 0, 1, 1], TEAL),
            ("wr_data[7:0]",  "bus",  TEAL),
            ("rd_en",         [0, 0, 0, 1, 1, 0, 0, 1], VIOLET),
            ("rd_data[7:0]",  "bus2", VIOLET),
            ("full",          [0, 0, 0, 0, 0, 1, 1, 0], RED),
            ("empty",         [1, 1, 0, 0, 0, 0, 0, 0], AMBER)]
    step = (ptop - pbot - 2.4) / len(rows)
    y = ptop - 3.2
    for i, (name, seq, col) in enumerate(rows):
        yy = y - i * step
        ax.text(6.5, yy + 0.9, name, fontsize=6.4, color=NAVY, ha="left",
                family="monospace", va="center")
        if seq is None:
            clk_wave(ax, 27, yy, 7.6, 4, 1.9, color=col, name=None)
        elif seq in ("bus", "bus2"):
            labels = ["A1", "B2", "C3", "D4"] if seq == "bus" else ["xx", "A1", "B2", "C3"]
            for k in range(4):
                bx = 27 + k * 7.6
                box(ax, bx, yy, 7.2, 1.9, fc=LIGHT, ec=col, lw=0.8, r=0.25)
                ax.text(bx + 3.6, yy + 0.95, labels[k], fontsize=5.8, color=NAVY,
                        ha="center", va="center", family="monospace")
        else:
            wave(ax, 27, yy, 3.8, seq, 1.9, color=col, name=None)

    mx = 27 + 7.6 * 4
    ax.plot([mx, mx], [pbot + 0.8, ptop - 1.2], color=RED, lw=1.3, ls="--", zorder=6)
    ax.text(mx + 1.0, pbot + 1.4, "marker: the first WRONG cycle", fontsize=6.6, color=RED,
            ha="left", fontweight="bold")
    save(f, "gtkwave_tour")


# ----------------------------------------------------------------- debug
def debug_method():
    W, Hin = 11.5, 5.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 50.4
    title(ax, 50, H - 3, "Debugging is a procedure, not a talent", 13)

    ptop, pbot = H - 7.5, 24.0
    # ---- bisect in time ----
    box(ax, 4, pbot, 45, ptop - pbot, fc=WHITE, ec=TEAL, lw=1.8)
    ax.text(26.5, ptop - 3.4, "BISECT IN TIME", fontsize=9.6, color=TEAL,
            fontweight="bold", ha="center")
    ty = ptop - 10.5
    ax.plot([9, 44], [ty, ty], color=SLATE, lw=1.6)
    for xx, lab, col in [(9, "reset", GREEN), (26.5, "?", AMBER), (44, "you noticed", RED)]:
        ax.plot([xx], [ty], "o", ms=6, color=col, zorder=5)
        ax.text(xx, ty + 2.4, lab, fontsize=7.6, color=col, ha="center")
    ax.text(26.5, pbot + 3.4, "Find the FIRST cycle where reality and the model\n"
                              "disagree — never the cycle where you noticed.",
            fontsize=8.2, color=BODY, ha="center")

    # ---- bisect in space ----
    box(ax, 52, pbot, 44, ptop - pbot, fc=WHITE, ec=VIOLET, lw=1.8)
    ax.text(74, ptop - 3.4, "BISECT IN SPACE", fontsize=9.6, color=VIOLET,
            fontweight="bold", ha="center")
    for i, (nm, col) in enumerate([("input", GREEN), ("stage 1", GREEN),
                                   ("stage 2", AMBER), ("output", RED)]):
        x = 55 + i * 10.0
        box(ax, x, ty + 0.5, 8.0, 4.6, fc=WHITE, ec=col, lw=1.4)
        ax.text(x + 4, ty + 2.8, nm, fontsize=7.0, color=col, ha="center", va="center")
        if i < 3:
            arrow(ax, x + 8, ty + 2.8, x + 10, ty + 2.8, color=SLATE, lw=1.2)
    ax.text(74, pbot + 2.8, "Walk backwards from the wrong signal to whatever\n"
                            "drives it, and repeat, until the first wrong signal.",
            fontsize=8.2, color=BODY, ha="center")

    # ---- the ladder ----
    ax.text(4, 19.5, "The ladder — cheapest rung first", fontsize=9.6, color=NAVY,
            fontweight="bold", ha="left")
    steps = ["read the error message — it names the file and line",
             "run the linter — one second, and it may name it outright",
             "read your own diff — what changed since it last worked?",
             "add \\$display at the failure, printing the INPUTS too",
             "open the waveform at the first failing cycle",
             "walk backwards to the first signal that was wrong",
             "synthesise — a latch explains a whole class of symptoms",
             "reduce the test to the smallest case that still fails"]
    for i, t in enumerate(steps):
        cx = 5 if i < 4 else 51
        yy = 15.0 - (i % 4) * 3.7
        ax.add_patch(Circle((cx + 1.8, yy), 1.5, fc=NAVY, ec=NAVY, zorder=5))
        ax.text(cx + 1.8, yy, str(i + 1), ha="center", va="center", fontsize=6.6,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(cx + 4.4, yy, t, fontsize=8.0, color=BODY, ha="left", va="center")
    save(f, "debug_method")


# ---------------------------------------------------------------- x chase
def x_chase():
    W, Hin = 11.0, 4.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 43.6
    title(ax, 50, H - 3, "Chasing an x back to its source", 12.5)
    ax.text(50, H - 7.0, "x is contagious. The signal where you NOTICED it is almost never "
                         "the signal that caused it.",
            fontsize=9, color=SLATE, ha="center")

    chain = [("rst_n\nnever asserted", "THE CAUSE"),
             ("state\nregister", ""),
             ("next_state\nlogic", ""),
             ("data_valid", ""),
             ("rd_data", "where you noticed")]
    bw, gap = 15.0, 4.5
    x0 = 50 - (5 * bw + 4 * gap) / 2
    y = H - 25.5
    arrow(ax, x0 + 4 * (bw + gap) + bw / 2, y + 12.0, x0 + bw / 2, y + 12.0,
          color=VIOLET, lw=2.0)
    ax.text(50, y + 14.0, "you search THIS way", fontsize=8.6, color=VIOLET,
            ha="center", fontweight="bold")
    for i, (name, note) in enumerate(chain):
        x = x0 + i * (bw + gap)
        key = i in (0, 4)
        box(ax, x, y, bw, 9.0, fc="#FDECEF" if key else WHITE,
            ec=RED if key else SLATE, lw=2.2 if key else 1.5)
        ax.text(x + bw / 2, y + 4.5, name, ha="center", va="center", fontsize=8.2,
                color=RED if key else NAVY, fontweight="bold")
        if note:
            ax.text(x + bw / 2, y - 3.0, note, ha="center", va="center", fontsize=8.0,
                    color=RED, fontweight="bold")
        if i < 4:
            arrow(ax, x + bw, y + 4.5, x + bw + gap, y + 4.5, color=RED, lw=1.7)

    box(ax, 4, 3.5, 92, 10.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 10.8, "In the viewer: add the suspect signal, find the FIRST edge where it goes x, "
                      "add whatever drives it, repeat.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 7.0, "In the testbench, always compare with  ===  and  !==",
            fontsize=8.6, color=RED, ha="center", fontweight="bold")
    ax.text(50, 4.6, "with  !=  an x compares as x, which is not true — so the check silently passes",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "x_chase")


# --------------------------------------------------------- failure signatures
def failure_signatures():
    W, Hin = 11.5, 5.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                       # 50.4
    title(ax, 50, H - 3.2, "Symptom to cause — the table to put on the lab wall", 12.5)

    cols = ["What you see", "Almost always means", "Where to look first"]
    rows = [["x on everything, from time 0", "a register was never reset", "the reset path"],
            ["x appears part-way through", "two drivers, or a read past the end of a vector",
             "every assign to that signal"],
            ["off by one cycle", "a check sampled before the NBA update landed", "the testbench, not the DUT"],
            ["off by one COUNT", "a boundary: <= where < was meant", "the comparison in the RTL"],
            ["a pulse is half a cycle wide", "stimulus driven on the clock edge", "the testbench driver"],
            ["works for some data, not others", "width truncation somewhere", "run the linter"],
            ["passes at one parameter, fails at another", "a constant sliced too narrow", "every [W-1:0] on a constant"],
            ["testbench passes, hardware fails", "casex, full_case, or an initial block", "grep the RTL for all three"],
            ["FSM stuck in a state it cannot leave", "no default branch", "the next-state case"],
            ["simulation is unbearably slow", "waveform dumping, or a testbench loop with no delay",
             "\\$dumpvars scope"]]
    cw = [34, 38, 24]
    table(ax, 50 - sum(cw) / 2, H - 8.0, cols, rows, cw, 3.2, size=8.0, bold_col=0)
    ax.text(50, 2.6, "Every row is a real failure mode from Topic 4 and Topic 5. "
                     "Recognising the signature is most of the debugging.",
            ha="center", fontsize=8.6, color=BODY, fontstyle="italic")
    save(f, "failure_signatures")


if __name__ == "__main__":
    sim_engine(); event_regions(); compile_elab_run(); vcd_flow()
    gtkwave_tour(); debug_method(); x_chase(); failure_signatures()
