"""Topic 3C diagrams: registers, counters, state machines, tooling."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsl import *
from d_seq import ff_symbol
import numpy as np


def shift_registers():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Registers — flip-flops working as a group", 13.0, NAVY)
    # ---- 4-bit shift register schematic ----
    box(ax, 2.0, 21.0, 96.0, 17.0, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(50, 36.2, "4-bit serial-in / parallel-out shift register — each Q feeds the next D",
            ha="center", va="center", fontsize=10.0, color=NAVY, fontweight="bold")
    cy, bw2 = 29.0, 8.6
    xs = [17.0, 35.0, 53.0, 71.0]
    for i, x in enumerate(xs):
        ff_symbol(ax, x, cy - 4.2, bw2, 8.4, [("D", NAVY), ("clk", RED)], [("Q", NAVY)],
                  ec=TEAL, clk_idx=1, size=7.6)
        ax.text(x + bw2 / 2, cy + 5.6, "FF%d" % i, ha="center", va="center", fontsize=8.2,
                color=TEAL, fontweight="bold")
        ax.text(x + bw2 + 1.6, cy + 3.4, "Q$_%d$" % i, ha="center", va="center", fontsize=8.4,
                color=GREEN, fontweight="bold")
        if i < 3:
            arrow(ax, x + bw2 + 3.2, cy + 1.4, xs[i + 1] - 3.2, cy + 1.4,
                  color=SLATE, lw=1.5, ms=9)
    wire(ax, [(9.0, cy + 1.4), (13.8, cy + 1.4)], color=INK, lw=1.5)
    ax.text(8.4, cy + 1.4, "serial in", ha="right", va="center", fontsize=8.6,
            color=AMBER, fontweight="bold")
    wire(ax, [(79.6, cy + 1.4), (85.0, cy + 1.4)], color=INK, lw=1.5)
    ax.text(85.6, cy + 1.4, "serial out", ha="left", va="center", fontsize=8.6,
            color=AMBER, fontweight="bold")
    wire(ax, [(9.0, 25.4), (75.6, 25.4)], color=RED, lw=1.5)
    ax.text(8.4, 25.4, "clk", ha="right", va="center", fontsize=8.6, color=RED, fontweight="bold")
    for x in xs:
        wire(ax, [(x - 3.2, cy - 1.4), (x - 4.6, cy - 1.4), (x - 4.6, 25.4)], color=RED, lw=1.2)
        dot(ax, x - 4.6, 25.4, color=RED)
    ax.text(50, 22.4, "One clock edge shifts every bit one position to the right.  "
            "Every Q is also a parallel output — that is what makes it SIPO.",
            ha="center", va="center", fontsize=8.0, color=SLATE, style="italic")

    # ---- the four transfer modes ----
    modes = [("SISO", "serial in\nserial out", "1 bit in, 1 bit out,\nn cycles to fill", TEAL),
             ("SIPO", "serial in\nparallel out", "shift in bit by bit,\nread all n at once", GREEN),
             ("PISO", "parallel in\nserial out", "load all n at once,\nshift out bit by bit", AMBER),
             ("PIPO", "parallel in\nparallel out", "load and read in one\nedge — a plain register", SLATE)]
    cwd = 23.4
    for i, (nm, sub, note, c) in enumerate(modes):
        x = 1.6 + i * (cwd + 1.5)
        box(ax, x, 3.0, cwd, 15.5, fc=LIGHT, ec=c, lw=1.6)
        ax.add_patch(FancyBboxPatch((x, 14.0), cwd, 4.5, boxstyle="round,pad=0,rounding_size=1.0",
                                    fc=c, ec=c, lw=1.0, zorder=3))
        ax.add_patch(Rectangle((x, 14.0), cwd, 2.3, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + cwd / 2, 16.2, nm, ha="center", va="center", fontsize=10.5,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + cwd / 2, 10.6, sub, ha="center", va="center", fontsize=8.4,
                color=NAVY, fontweight="bold", linespacing=1.4)
        ax.text(x + cwd / 2, 5.6, note, ha="center", va="center", fontsize=7.6,
                color=BODY, linespacing=1.5)
    save(f, "shift_registers")


def counters():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Counters — ripple (asynchronous) versus synchronous", 13.0, NAVY)
    cy = 31.0
    # ---------- ripple ----------
    box(ax, 2.0, 21.5, 46.0, 17.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(25.0, 37.4, "RIPPLE (asynchronous) counter", ha="center", va="center",
            fontsize=10.0, color=RED, fontweight="bold")
    ffw = 6.5
    rx = [8.5, 23.0, 37.5]
    for i, x in enumerate(rx):
        ff_symbol(ax, x, cy - 3.6, ffw, 7.2, [("T", NAVY), ("clk", RED)], [("Q", NAVY)],
                  ec=RED, clk_idx=1, size=7.0)
        ax.text(x + ffw / 2, cy + 5.4, "Q$_%d$" % i, ha="center", va="center", fontsize=8.4,
                color=NAVY, fontweight="bold")
        ax.text(x - 3.8, cy + 1.2, "1", ha="right", va="center", fontsize=7.6,
                color=SLATE, fontweight="bold")
        if i < 2:
            xn = rx[i + 1]
            wire(ax, [(x + ffw + 3.2, cy), (x + ffw + 3.2, cy - 1.2)], color=RED, lw=1.4)
            arrow(ax, x + ffw + 3.2, cy - 1.2, xn - 3.1, cy - 1.2, color=RED, lw=1.4, ms=8)
    ax.text(5.3, cy - 3.4, "clk", ha="center", va="center", fontsize=7.6,
            color=RED, fontweight="bold")
    ax.text(25.0, 22.6, "each flip-flop is clocked by the PREVIOUS stage's output",
            ha="center", va="center", fontsize=8.0, color=RED, fontweight="bold")

    # ---------- synchronous ----------
    box(ax, 52.0, 21.5, 46.0, 17.5, fc="#E4F4EC", ec=GREEN, lw=1.7)
    ax.text(75.0, 37.4, "SYNCHRONOUS counter", ha="center", va="center",
            fontsize=10.0, color=GREEN, fontweight="bold")
    sx = [60.0, 74.0, 88.0]
    for i, x in enumerate(sx):
        ff_symbol(ax, x, cy - 3.6, ffw, 7.2, [("T", NAVY), ("clk", RED)], [("Q", NAVY)],
                  ec=GREEN, clk_idx=1, size=7.0)
        ax.text(x + ffw / 2, cy + 5.4, "Q$_%d$" % i, ha="center", va="center", fontsize=8.4,
                color=NAVY, fontweight="bold")
    wire(ax, [(56.5, 25.4), (84.8, 25.4)], color=RED, lw=1.6)
    ax.text(56.0, 26.9, "clk", ha="left", va="center", fontsize=7.6, color=RED, fontweight="bold")
    for x in sx:
        wire(ax, [(x - 3.2, cy - 1.2), (x - 4.2, cy - 1.2), (x - 4.2, 25.4)], color=RED, lw=1.3)
        dot(ax, x - 4.2, 25.4, color=RED)
    ax.text(75.0, 22.6, "EVERY flip-flop shares ONE clock; AND gates decide who toggles",
            ha="center", va="center", fontsize=8.0, color=GREEN, fontweight="bold")

    # ---------- timing comparison ----------
    box(ax, 2.0, 2.5, 96.0, 17.0, fc=WHITE, ec=GRID, lw=1.4)
    ax.text(50, 17.8, "Why it matters — in a ripple counter the outputs do NOT change together",
            ha="center", va="center", fontsize=9.6, color=NAVY, fontweight="bold")
    x0, ww, u = 14.0, 3.5, 5.0
    wave(ax, x0, 12.0, ww, [0, 1] * 6, u, color=NAVY, name="clk", name_size=8.4, label_dx=1.6)
    wave(ax, x0 + 0.9, 8.0, ww, [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], u, color=TEAL,
         name="Q$_0$", name_size=8.4, label_dx=2.5)
    wave(ax, x0 + 1.8, 4.0, ww, [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], u, color=AMBER,
         name="Q$_1$", name_size=8.4, label_dx=3.4)
    for k in (2, 6, 10):
        xe = x0 + k * ww
        ax.plot([xe, xe], [3.4, 15.2], color=RED, lw=0.9, ls=(0, (3, 3)), zorder=2)
    ax.text(60.0, 11.0, "Each stage adds one t$_{cq}$ of skew, so an n-bit ripple counter can\n"
            "read out a WRONG value for up to n × t$_{cq}$ after every edge.\n\n"
            "A synchronous counter changes every bit on the same edge — which is\n"
            "why it is the only kind you should ever synthesise.",
            ha="left", va="center", fontsize=7.8, color=BODY, linespacing=1.8)
    save(f, "counters")


def mod10_design():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Worked design — a mod-10 (BCD) synchronous up-counter", 13.0, NAVY)
    rows = []
    for n in range(10):
        nxt = (n + 1) % 10
        rows.append(["%d" % n, format(n, "04b"), format(nxt, "04b"), "%d" % nxt])
    table(ax, 3.0, H - 5.6, ["count", "Q$_3$Q$_2$Q$_1$Q$_0$", "next state", "= count"],
          rows, [8.0, 12.0, 12.0, 8.0], 2.95, size=8.4, head_fc=NAVY, bold_col=[2],
          colcolors={2: GREEN})
    ax.text(23.0, 3.2, "the 1001 → 0000 wrap is the ONLY special row",
            ha="center", va="center", fontsize=8.2, color=RED, fontweight="bold")

    box(ax, 46.0, 22.0, 52.0, 16.5, fc=LIGHT, ec=TEAL, lw=1.7)
    ax.text(48.4, 36.4, "Gate-level answer  (D flip-flops)", ha="left", va="center",
            fontsize=9.8, color=TEAL, fontweight="bold")
    eqs = ["D$_0$  =  Q$_0$'",
           "D$_1$  =  Q$_1$ ⊕ (Q$_0$ · Q$_3$')",
           "D$_2$  =  Q$_2$ ⊕ (Q$_1$ · Q$_0$)",
           "D$_3$  =  Q$_3$ ⊕ (Q$_3$·Q$_0$ + Q$_2$·Q$_1$·Q$_0$)"]
    for j, e in enumerate(eqs):
        ax.text(50.0, 33.0 - j * 2.8, e, ha="left", va="center", fontsize=9.0,
                color=NAVY, fontweight="bold")
    ax.text(48.4, 22.9, "Derived from the excitation table, then K-map minimised.",
            ha="left", va="center", fontsize=7.8, color=SLATE, style="italic")

    box(ax, 46.0, 3.0, 52.0, 17.0, fc="#E4F4EC", ec=GREEN, lw=1.7)
    ax.text(48.4, 18.0, "…and how you would actually write it in RTL", ha="left", va="center",
            fontsize=9.8, color=GREEN, fontweight="bold")
    code = ["always @(posedge clk or posedge rst)", "  if (rst)          count <= 4'd0;",
            "  else if (count == 4'd9) count <= 4'd0;", "  else              count <= count + 1'b1;"]
    for j, ln in enumerate(code):
        ax.text(48.4, 15.4 - j * 2.4, ln, ha="left", va="center", fontsize=8.0,
                color=NAVY, family="DejaVu Sans Mono")
    ax.text(72.0, 5.2, "Same circuit. The synthesiser derives those four equations for you —\n"
            "but you must be able to check that it did the right thing.",
            ha="center", va="center", fontsize=7.6, color=BODY, linespacing=1.6)
    save(f, "mod10_design")


def moore_mealy():
    W, Hin = 13, 5.0
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 38.46
    title(ax, 50, H - 2.0, "Moore vs Mealy — where the output logic gets its inputs", 13.0, NAVY)
    for k, (x0, nm, c, bg) in enumerate([(2.0, "MOORE", TEAL, "#E8F5F7"),
                                         (51.0, "MEALY", AMBER, "#FFF6EC")]):
        wd = 47.0
        box(ax, x0, 10.0, wd, 23.5, fc=bg, ec=c, lw=1.8)
        ax.text(x0 + wd / 2, 31.6, nm, ha="center", va="center", fontsize=11.5,
                color=c, fontweight="bold")
        ny, oy, ry = 25.5, 15.0, 20.2
        label_box(ax, x0 + 12.0, ny - 2.6, 13.0, 5.2, "next-state\nlogic", fc=WHITE, ec=c,
                  tc=NAVY, size=7.6, lw=1.6)
        label_box(ax, x0 + 29.0, ny - 2.6, 11.0, 5.2, "state\nregister", fc=WHITE, ec=RED,
                  tc=RED, size=7.6, lw=1.6)
        label_box(ax, x0 + 12.0, oy - 2.6, 13.0, 5.2, "output\nlogic", fc=WHITE, ec=c,
                  tc=NAVY, size=7.6, lw=1.6)
        arrow(ax, x0 + 25.0, ny, x0 + 28.6, ny, color=SLATE, lw=1.5, ms=9)
        arrow(ax, x0 + 6.0, ny, x0 + 11.6, ny, color=SLATE, lw=1.5, ms=9)
        ax.text(x0 + 5.4, ny, "in", ha="right", va="center", fontsize=8.6,
                color=NAVY, fontweight="bold")
        # state feedback bus
        wire(ax, [(x0 + 40.0, ny), (x0 + 43.0, ny), (x0 + 43.0, ry), (x0 + 8.5, ry),
                  (x0 + 8.5, ny - 1.6)], color=RED, lw=1.5)
        dot(ax, x0 + 43.0, ny, color=RED)
        arrow(ax, x0 + 8.5, ny - 1.4, x0 + 11.6, ny - 1.4, color=RED, lw=1.5, ms=8)
        wire(ax, [(x0 + 8.5, ry), (x0 + 8.5, oy)], color=RED, lw=1.5)
        arrow(ax, x0 + 8.5, oy, x0 + 11.6, oy, color=RED, lw=1.5, ms=8)
        ax.text(x0 + 24.0, ry + 1.3, "present state", ha="center", va="center", fontsize=7.4,
                color=RED, fontweight="bold")
        arrow(ax, x0 + 25.0, oy, x0 + 31.0, oy, color=SLATE, lw=1.5, ms=9)
        ax.text(x0 + 31.8, oy, "out", ha="left", va="center", fontsize=8.6,
                color=GREEN, fontweight="bold")
        if k == 1:
            wire(ax, [(x0 + 8.0, ny), (x0 + 8.0, 11.6), (x0 + 15.0, 11.6),
                      (x0 + 15.0, oy - 2.6)], color=AMBER, lw=1.7)
            dot(ax, x0 + 8.0, ny, color=AMBER)
            arrow(ax, x0 + 15.0, 12.4, x0 + 15.0, oy - 2.7, color=AMBER, lw=1.7, ms=9)
            ax.text(x0 + 22.0, 11.2, "the input also drives the output", ha="left",
                    va="center", fontsize=7.6, color=AMBER, fontweight="bold")
    facts = [(2.0, TEAL, ["Output = f(state) only",
                          "Output changes only just after a clock edge",
                          "Glitch-free, easy to time — safer",
                          "Usually needs MORE states",
                          "Reacts one cycle later"]),
             (51.0, AMBER, ["Output = f(state, input)",
                            "Output can change the moment the input does",
                            "Can glitch — must be registered before use",
                            "Usually needs FEWER states",
                            "Reacts one cycle earlier"])]
    for x0, c, items in facts:
        for j, it in enumerate(items):
            ax.text(x0 + 2.0, 8.4 - j * 1.75, "·  " + it, ha="left", va="center",
                    fontsize=8.0, color=BODY)
    save(f, "moore_mealy")


def fsm_procedure():
    W, Hin = 13, 4.0
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 30.77
    title(ax, 50, H - 2.0, "The six steps of finite-state-machine design", 13.0, NAVY)
    steps = [("1", "Draw the\nstate diagram", "one bubble per\nthing to remember", TEAL),
             ("2", "Write the\nstate table", "present state + input\n→ next state + output", TEAL),
             ("3", "Minimise\nstates", "merge equivalent\nstates (optional)", AMBER),
             ("4", "Assign an\nencoding", "binary · Gray · one-hot", AMBER),
             ("5", "Derive the\nlogic", "next-state and output\nequations per bit", GREEN),
             ("6", "Implement\n& verify", "registers + gates,\nthen simulate", GREEN)]
    bw, gap = 14.4, 2.2
    x0 = (100 - (6 * bw + 5 * gap)) / 2
    by, bh = 6.5, 16.5
    for i, (n, head, sub, c) in enumerate(steps):
        x = x0 + i * (bw + gap)
        box(ax, x, by, bw, bh, fc=WHITE, ec=c, lw=1.8)
        ax.add_patch(Circle((x + bw / 2, by + bh - 3.0), 2.0, fc=c, ec=c, zorder=4))
        ax.text(x + bw / 2, by + bh - 3.0, n, ha="center", va="center", fontsize=10,
                color="white", fontweight="bold", zorder=6)
        ax.text(x + bw / 2, by + bh - 8.2, head, ha="center", va="center", fontsize=8.8,
                color=NAVY, fontweight="bold", linespacing=1.4)
        ax.text(x + bw / 2, by + 2.8, sub, ha="center", va="center", fontsize=6.9,
                color=SLATE, linespacing=1.4)
        if i < 5:
            arrow(ax, x + bw + 0.3, by + bh / 2, x + bw + gap - 0.3, by + bh / 2,
                  color=SLATE, lw=1.8, ms=9)
    ax.text(50, 3.0, "In RTL you write steps 1–2 directly as a Verilog case statement and let the synthesiser do steps 3–5. "
            "Step 6 is still yours.",
            ha="center", va="center", fontsize=8.8, color=BODY, style="italic")
    save(f, "fsm_procedure")


def state_encoding():
    W, Hin = 13, 4.4
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 33.85
    title(ax, 50, H - 2.0, "State encoding — the same FSM, three different silicon costs", 13.0, NAVY)
    rows = [["S$_0$", "000", "000", "00001"],
            ["S$_1$", "001", "001", "00010"],
            ["S$_2$", "010", "011", "00100"],
            ["S$_3$", "011", "010", "01000"],
            ["S$_4$", "100", "110", "10000"]]
    table(ax, 4.0, 27.5, ["state", "BINARY", "GRAY", "ONE-HOT"], rows,
          [9.0, 10.0, 10.0, 12.0], 3.2, size=9.0, head_fc=NAVY, bold_col=[1, 2, 3])
    cards = [("BINARY", TEAL, ["⌈log₂n⌉ flip-flops — fewest", "More next-state logic",
                               "Default for large FSMs", "5 states → 3 FFs"]),
             ("GRAY", AMBER, ["Same FF count as binary", "One bit changes per step",
                              "Less switching → less power", "Good for counters/pointers"]),
             ("ONE-HOT", GREEN, ["n flip-flops — most", "Next-state logic is trivial",
                                 "Fastest; ideal on FPGAs", "5 states → 5 FFs"])]
    cwd = 29.0
    for i, (nm, c, items) in enumerate(cards):
        x = 48.0 + (i % 3) * 0 if False else 0
    for i, (nm, c, items) in enumerate(cards):
        x = 4.0 + i * (cwd + 1.5) if False else 50.0 + (i - 1) * 0
    xs = [50.0, 66.0, 82.0]
    for i, (nm, c, items) in enumerate(cards):
        x = xs[i]
        box(ax, x, 5.5, 15.0, 24.0, fc=LIGHT, ec=c, lw=1.7)
        ax.add_patch(FancyBboxPatch((x, 25.0), 15.0, 4.5, boxstyle="round,pad=0,rounding_size=1.0",
                                    fc=c, ec=c, lw=1.0, zorder=3))
        ax.add_patch(Rectangle((x, 25.0), 15.0, 2.3, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + 7.5, 27.2, nm, ha="center", va="center", fontsize=9.4,
                color="white", fontweight="bold", zorder=6)
        for j, it in enumerate(items):
            ax.text(x + 0.9, 22.4 - j * 4.6, it, ha="left", va="center", fontsize=7.0,
                    color=BODY, linespacing=1.4, wrap=True)
    ax.text(50.0, 3.0, "Verilog: use `localparam` (or an enum) for state names and let the tool pick the encoding — "
            "then CHECK the synthesis report.",
            ha="center", va="center", fontsize=8.2, color=BODY, style="italic")
    save(f, "state_encoding")


def fsm_1011():
    W, Hin = 13, 5.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 43.08
    title(ax, 50, H - 2.0, "Moore state diagram — a '1011' sequence detector (overlapping)",
          13.0, NAVY)
    cy, r = 26.0, 5.2
    xs = [11.0, 30.5, 50.0, 69.5, 89.0]
    names = ["S0", "S1", "S2", "S3", "S4"]
    mean = ["start", "seen 1", "seen 10", "seen 101", "seen 1011"]
    outs = ["0", "0", "0", "0", "1"]
    for i, x in enumerate(xs):
        c = GREEN if i == 4 else TEAL
        ax.add_patch(Circle((x, cy), r, fc="#E4F4EC" if i == 4 else WHITE, ec=c, lw=2.2, zorder=4))
        if i == 4:
            ax.add_patch(Circle((x, cy), r - 0.9, fc="none", ec=c, lw=1.1, zorder=5))
        ax.text(x, cy + 2.3, names[i], ha="center", va="center", fontsize=10.5,
                color=NAVY, fontweight="bold", zorder=6)
        ax.text(x, cy - 0.2, mean[i], ha="center", va="center", fontsize=6.4,
                color=SLATE, zorder=6)
        ax.text(x, cy - 2.7, "Z = " + outs[i], ha="center", va="center", fontsize=8.4,
                color=GREEN if i == 4 else SLATE, fontweight="bold", zorder=6)

    # ---- forward transitions (straight, between adjacent states) ----
    for a_, b_, lab in [(0, 1, "1"), (1, 2, "0"), (2, 3, "1"), (3, 4, "1")]:
        arrow(ax, xs[a_] + r, cy, xs[b_] - r, cy, color=NAVY, lw=1.8, ms=11)
        ax.text((xs[a_] + xs[b_]) / 2, cy + 2.2, lab, ha="center", va="center",
                fontsize=10, color=NAVY, fontweight="bold")

    # ---- self loops ----
    for i, lab in [(0, "0"), (1, "1")]:
        x = xs[i]
        lc = (x, cy + r + 2.7)
        ax.add_patch(Arc(lc, 6.2, 6.2, theta1=-70, theta2=250, ec=SLATE, lw=1.7, zorder=4))
        ex = x + 3.1 * np.cos(np.radians(250))
        ax.add_patch(Polygon([(ex - 0.85, cy + r + 1.1), (ex + 0.85, cy + r + 1.1),
                              (ex, cy + r - 0.6)], fc=SLATE, ec="none", zorder=6))
        ax.text(x, cy + r + 7.2, lab, ha="center", va="center", fontsize=10,
                color=SLATE, fontweight="bold")

    # ---- backward transitions (arcs under the row) ----
    back = [(3, 2, "0", -0.45, RED), (2, 0, "0", -0.30, RED),
            (4, 2, "0", -0.32, AMBER), (4, 1, "1", -0.46, VIOLET)]
    for a_, b_, lab, rad, c in back:
        ax1, ay1 = xs[a_] - r * 0.68, cy - r * 0.72
        ax2, ay2 = xs[b_] + r * 0.68, cy - r * 0.72
        arrow(ax, ax1, ay1, ax2, ay2, color=c, lw=1.7, ms=10, rad=rad)
        sag = abs(rad) * abs(ax1 - ax2) / 2.0
        ax.text((ax1 + ax2) / 2, ay1 - sag - 1.5, lab, ha="center", va="center",
                fontsize=9.6, color=c, fontweight="bold")

    box(ax, 2.0, 0.8, 96.0, 5.8, fc=LIGHT, ec=TEAL, lw=1.5)
    ax.text(50, 4.4, "Each state remembers HOW MUCH of the pattern has matched so far — that is all a state ever is.",
            ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="bold")
    ax.text(50, 2.1, "'Overlapping' means that after a hit we keep the longest useful suffix, so S4 on input '1' goes to S1, not back to S0.",
            ha="center", va="center", fontsize=8.6, color=NAVY, fontweight="bold")
    save(f, "fsm_1011")


def fsm_1011_timing():
    W, Hin = 13, 4.8
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 36.92
    title(ax, 50, H - 2.0, "Same input, two machines — Moore asserts one cycle after Mealy",
          13.0, NAVY)
    bits = [1, 0, 1, 1, 0, 1, 1, 0]
    n = len(bits)
    x0, ww, u = 12.0, 8.2, 6.0
    trans = {0: {0: 0, 1: 1}, 1: {0: 2, 1: 1}, 2: {0: 0, 1: 3},
             3: {0: 2, 1: 4}, 4: {0: 2, 1: 1}}
    # present state during cycle i = state the register holds while bits[i] is applied
    present, st = [], 0
    for b_ in bits:
        present.append(st)
        st = trans[st][b_]
    clk = []
    for _ in range(n):
        clk += [0, 1]
    wave(ax, x0, 28.0, ww / 2, clk, u, color=NAVY, name="clk", name_size=9.0, label_dx=2.0)
    wave(ax, x0, 21.5, ww, bits, u, color=AMBER, name="X (input)", name_size=9.0, label_dx=2.0)
    for i in range(n):
        xx = x0 + i * ww
        ax.text(xx + ww / 2, 24.0, str(bits[i]), ha="center", va="center", fontsize=9.0,
                color=AMBER, fontweight="bold")
        s_ = present[i]
        ax.add_patch(Rectangle((xx, 15.0), ww, 4.4, fc="#E4F4EC" if s_ == 4 else LIGHT,
                               ec=GRID, lw=1.0, zorder=3))
        ax.text(xx + ww / 2, 17.2, "S%d" % s_, ha="center", va="center", fontsize=8.6,
                color=GREEN if s_ == 4 else NAVY, fontweight="bold", zorder=5)
    ax.text(x0 - 2.0, 17.2, "state", ha="right", va="center", fontsize=9.0,
            color=NAVY, fontweight="bold")
    moore = [1 if present[i] == 4 else 0 for i in range(n)]
    mealy = [1 if (present[i] == 3 and bits[i] == 1) else 0 for i in range(n)]
    wave(ax, x0, 8.4, ww, mealy, u, color=RED, name="Z (Mealy)", name_size=9.0, label_dx=2.0)
    wave(ax, x0, 1.8, ww, moore, u, color=GREEN, name="Z (Moore)", name_size=9.0, label_dx=2.0)
    for i in range(n):
        if mealy[i] or moore[i]:
            xx = x0 + i * ww
            ax.add_patch(Rectangle((xx, 1.4), ww, 12.6,
                                   fc=RED if mealy[i] else GREEN, alpha=0.07,
                                   ec="none", zorder=1))
    nx = x0 + n * ww + 2.0
    ax.text(nx, 28.6, "X = 1 0 1 1 0 1 1 0", ha="left", va="center", fontsize=8.6,
            color=NAVY, fontweight="bold")
    ax.text(nx, 20.0, "MEALY asserts Z during\nthe very cycle whose input\ncompletes 1011 — it can\nsee X directly.",
            ha="left", va="center", fontsize=7.4, color=RED, linespacing=1.6)
    ax.text(nx, 9.0, "MOORE asserts Z in the\nNEXT cycle, once the clock\nedge has actually moved\nthe register into S4.",
            ha="left", va="center", fontsize=7.4, color=GREEN, linespacing=1.6)
    save(f, "fsm_1011_timing")


def fsmd():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 35.38
    title(ax, 50, H - 2.0, "Putting it all together — the controller + datapath (FSMD) view",
          13.0, NAVY)
    box(ax, 4.0, 8.0, 38.0, 22.0, fc="#FFF6EC", ec=AMBER, lw=1.9)
    ax.text(23.0, 31.4, "CONTROLLER  —  an FSM", ha="center", va="center", fontsize=10,
            color=AMBER, fontweight="bold")
    label_box(ax, 9.0, 20.0, 12.0, 6.0, "next-state\nlogic", fc=WHITE, ec=AMBER, tc=NAVY,
              size=7.6, lw=1.5)
    label_box(ax, 25.0, 20.0, 12.0, 6.0, "state\nregister", fc=WHITE, ec=RED, tc=RED,
              size=7.6, lw=1.5)
    label_box(ax, 17.0, 10.5, 12.0, 6.0, "output\nlogic", fc=WHITE, ec=AMBER, tc=NAVY,
              size=7.6, lw=1.5)
    arrow(ax, 21.0, 23.0, 24.6, 23.0, color=SLATE, lw=1.5, ms=9)
    wire(ax, [(37.0, 23.0), (39.4, 23.0), (39.4, 17.6), (6.6, 17.6), (6.6, 22.0)], color=RED, lw=1.4)
    arrow(ax, 6.6, 22.0, 8.6, 22.0, color=RED, lw=1.4, ms=8)
    wire(ax, [(6.6, 17.6), (6.6, 13.5)], color=RED, lw=1.4)
    arrow(ax, 6.6, 13.5, 16.6, 13.5, color=RED, lw=1.4, ms=8)

    box(ax, 58.0, 8.0, 38.0, 22.0, fc="#E8F5F7", ec=TEAL, lw=1.9)
    ax.text(77.0, 31.4, "DATAPATH  —  combinational + registers", ha="center", va="center",
            fontsize=10, color=TEAL, fontweight="bold")
    for j, (nm, yy) in enumerate([("registers", 23.0), ("ALU / adder / shifter", 17.0),
                                  ("multiplexers", 11.0)]):
        label_box(ax, 63.0, yy - 2.2, 28.0, 4.4, nm, fc=WHITE, ec=TEAL, tc=NAVY,
                  size=8.4, lw=1.5)
    arrow(ax, 43.0, 23.0, 57.4, 23.0, color=AMBER, lw=2.0, ms=11)
    ax.text(50.0, 25.2, "control signals", ha="center", va="center", fontsize=8.4,
            color=AMBER, fontweight="bold")
    ax.text(50.0, 21.0, "load, shift, select, enable", ha="center", va="center",
            fontsize=7.2, color=SLATE)
    arrow(ax, 57.4, 12.5, 43.0, 12.5, color=GREEN, lw=2.0, ms=11)
    ax.text(50.0, 14.6, "status flags", ha="center", va="center", fontsize=8.4,
            color=GREEN, fontweight="bold")
    ax.text(50.0, 10.4, "zero, negative, done", ha="center", va="center",
            fontsize=7.2, color=SLATE)
    box(ax, 4.0, 1.0, 92.0, 6.0, fc=LIGHT, ec=NAVY, lw=1.5)
    ax.text(50, 4.0, "The controller decides WHEN; the datapath decides WHAT.  Every processor, DMA engine,\n"
            "UART and SPI controller you will ever write has exactly this shape.",
            ha="center", va="center", fontsize=8.4, color=NAVY, fontweight="bold", linespacing=1.6)
    save(f, "fsmd")


def toolchain():
    W, Hin = 13, 4.6
    f, ax = fig(W, Hin); H = 100 * Hin / W            # 35.38
    title(ax, 50, H - 2.0, "The open-source toolchain used in this topic's labs", 13.0, NAVY)
    tools = [("Logisim-\nEvolution", "draw and click\nlogic circuits", "visual intuition", TEAL),
             ("Icarus\nVerilog", "compile + simulate\nVerilog (iverilog/vvp)", "does it behave?", AMBER),
             ("GTKWave", "view the .vcd\nwaveform dump", "why did it do that?", GREEN),
             ("Yosys", "synthesise RTL to\na gate netlist", "what hardware appears?", NAVY)]
    bw, gap = 21.5, 3.6
    x0 = (100 - (4 * bw + 3 * gap)) / 2
    by, bh = 11.0, 18.0
    for i, (nm, what, why, c) in enumerate(tools):
        x = x0 + i * (bw + gap)
        box(ax, x, by, bw, bh, fc=WHITE, ec=c, lw=1.9)
        ax.add_patch(FancyBboxPatch((x, by + bh - 6.4), bw, 6.4,
                     boxstyle="round,pad=0,rounding_size=1.2", fc=c, ec=c, lw=1.2, zorder=3))
        ax.add_patch(Rectangle((x, by + bh - 6.4), bw, 3.2, fc=c, ec=c, lw=0, zorder=4))
        ax.text(x + bw / 2, by + bh - 3.2, nm, ha="center", va="center", fontsize=9.6,
                color="white", fontweight="bold", zorder=6, linespacing=1.3)
        ax.text(x + bw / 2, by + 7.6, what, ha="center", va="center", fontsize=8.0,
                color=NAVY, linespacing=1.5)
        ax.text(x + bw / 2, by + 2.6, why, ha="center", va="center", fontsize=8.0,
                color=c, fontweight="bold")
        if i < 3:
            arrow(ax, x + bw + 0.5, by + bh / 2, x + bw + gap - 0.5, by + bh / 2,
                  color=SLATE, lw=2.0, ms=11)
    box(ax, 4.0, 2.0, 92.0, 6.6, fc=LIGHT, ec=TEAL, lw=1.5)
    ax.text(50, 6.4, "All four are free, open-source and run on Windows, Linux and macOS.",
            ha="center", va="center", fontsize=9.0, color=NAVY, fontweight="bold")
    ax.text(50, 3.6, "Ubuntu / WSL:   sudo apt install iverilog gtkwave yosys        "
            "macOS:   brew install icarus-verilog gtkwave yosys        "
            "Windows:   use WSL2, or OSS CAD Suite",
            ha="center", va="center", fontsize=7.6, color=BODY, family="DejaVu Sans")
    ax.text(50, 31.0, "one flow:   draw it  →  describe it in Verilog  →  simulate it  →  look at it  →  synthesise it",
            ha="center", va="center", fontsize=9.4, color=SLATE, style="italic")
    save(f, "toolchain")


if __name__ == "__main__":
    shift_registers(); counters(); mod10_design(); moore_mealy()
    fsm_procedure(); state_encoding(); fsm_1011(); fsm_1011_timing()
    fsmd(); toolchain()
