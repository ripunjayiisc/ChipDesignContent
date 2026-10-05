# -*- coding: utf-8 -*-
"""Lecture 01 diagrams — the steps of the flow, one at a time."""
import _boot
from dsl import *
from l1_kit import wrap, note, column_cards, rowcards, chars_for

CARDS = {
    "behavioral_forms": (
        "What they have in common",
        "Not one of these says how the circuit is BUILT. Each one says only "
        "what the circuit must DO. That is what makes them behavioural — and "
        "it is why a synthesis tool is free to build them in whichever way is "
        "cheapest.", "VIOLET"),
    "netlist_graph": (
        "Why a graph, and not a drawing",
        "Because a graph is something a program can hold in memory and "
        "transform. Every CAD step after this one — optimisation, mapping, "
        "placement, routing — is an operation on this graph.", "TEAL"),
    "netlist_levels": (
        "The same design, three times",
        "Each level is a netlist. What changes is only what counts as a "
        "vertex. Synthesis is the process of rewriting a netlist in terms of "
        "smaller vertices.", "NAVY"),
    "struct_vs_behav": (
        "Both are legal Verilog, and both describe the same adder",
        "You will write far more behavioural code than structural. But the "
        "tool's OUTPUT is always structural — which is why you must be able to "
        "read it.", "NAVY"),
    "standard_cell": (
        "Why a library exists at all",
        "Laying out a NAND gate correctly takes a skilled engineer a long "
        "time. Doing it once, perfectly, and then reusing it a million times "
        "is the only way the numbers work.", "GREEN"),
    "opt_conflict": (
        "\"These requirements are often conflicting\"",
        "A synthesis tool does not find THE answer — there isn't one. It "
        "finds an answer that satisfies the constraints you gave it. Give it "
        "different constraints and you get different hardware from the same "
        "Verilog.", "AMBER"),
    "physical_design": (
        "Why the shapes are all rectangles",
        "Because they are printed photographically, layer by layer, onto a "
        "silicon wafer. Regular shapes expose cleanly and etch predictably; "
        "awkward ones do not.", "AMBER"),
    "asic_vs_fpga": (
        "\"Much greater flexibility, but less speed\"",
        "The trade-off the lecturer names. An FPGA is a chip already "
        "manufactured, full of configurable blocks you program in your own "
        "laboratory. An ASIC is a chip built for your design alone.", "NAVY"),
    "struct_vs_behav_extra": (
        "Two consequences",
        "A netlist IS a structural description — the lecturer says so "
        "explicitly. And synthesis is simply the act of turning one into the "
        "other: you write behavioural Verilog, and the tool emits structural "
        "Verilog.", "GREEN"),
    "standard_cell_extra": (
        "A cell is all of these at once",
        "A standard cell is stored in a library as a symbol to place, a truth "
        "table to simulate, a timing model, and a finished piece of layout. "
        "Synthesis picks cells from that library; the place-and-route tool "
        "stamps their layouts down.", "TEAL"),
    "course_roadmap_extra": (
        "Notice what is missing",
        "Nothing after logic design. Physical design, manufacturing and test "
        "are real and essential, but in this course they are the tools' job. "
        "Your work ends at a netlist.", "NAVY"),
    "other_steps": (
        "Where each of these returns in the course",
        "Simulation is used in almost every lecture from Week 1 onwards, and "
        "Week 5 is devoted to test benches. Formal verification and testability "
        "are named here, but are beyond this course's scope.", "GREEN"),
}


def behavioral_forms():
    f, ax, H = panel(4.40)

    top = H - 1.5
    bh = 31.0
    w = 23.0
    gap = 1.7
    heads = [("BOOLEAN EXPRESSION", TEAL), ("TRUTH TABLE", VIOLET),
             ("FINITE-STATE MACHINE", GREEN), ("HIGH-LEVEL ALGORITHM", AMBER)]
    xs = [2.5 + i * (w + gap) for i in range(4)]
    for x, (head, col) in zip(xs, heads):
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.2, w, 4.2, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.1, head, ha="center", va="center",
                fontsize=8.4, color=WHITE, fontweight="bold")

    # 1 — a boolean expression
    x = xs[0]
    ax.text(x + w / 2, top - 12.0, "y  =  a·b  +  a'·c", ha="center",
            va="center", fontsize=FS_BODY, color=INK,
            family="DejaVu Sans Mono")
    wrap(ax, x + w / 2, top - 17.0, w - 3.0, "Algebra over 0 and 1. Compact, "
         "and exactly what a two-level logic minimiser wants as input.",
         FS_SMALL - 1.5, ha="center", lh=2.5)

    # 2 — a truth table
    x = xs[1]
    tw, trh = 4.4, 2.3
    tx = x + (w - 3 * tw) / 2
    ty = top - 6.4
    for j, hcell in enumerate(("a", "b", "y")):
        box(ax, tx + j * tw, ty - trh, tw, trh, fc=VIOLET, ec=VIOLET, lw=0.6,
            r=0.0)
        ax.text(tx + j * tw + tw / 2, ty - trh / 2, hcell, ha="center",
                va="center", fontsize=FS_SMALL - 1.5, color=WHITE,
                fontweight="bold")
    for i, row in enumerate((("0", "0", "0"), ("0", "1", "1"),
                             ("1", "0", "1"), ("1", "1", "0"))):
        yy = ty - trh * (i + 1)
        for j, cell in enumerate(row):
            box(ax, tx + j * tw, yy - trh, tw, trh,
                fc=WHITE if i % 2 == 0 else LIGHT, ec=GRID, lw=0.6, r=0.0)
            ax.text(tx + j * tw + tw / 2, yy - trh / 2, cell, ha="center",
                    va="center", fontsize=FS_SMALL - 1.5, color=BODY)
    wrap(ax, x + w / 2, top - 20.4, w - 3.0, "Every input combination listed "
         "with its output. Unambiguous, but doubles in size per extra input.",
         FS_SMALL - 1.5, ha="center", lh=2.5)

    # 3 — a two-state machine
    x = xs[2]
    c1 = (x + w * 0.3, top - 12.0)
    c2 = (x + w * 0.72, top - 12.0)
    for (cxx, cyy), lab in ((c1, "S0"), (c2, "S1")):
        ax.add_patch(Circle((cxx, cyy), 2.6, fc=WHITE, ec=GREEN, lw=1.8,
                            zorder=4))
        ax.text(cxx, cyy, lab, ha="center", va="center", fontsize=FS_SMALL - 1.0,
                color=GREEN, fontweight="bold", zorder=5)
    arrow(ax, c1[0] + 2.7, c1[1] + 1.0, c2[0] - 2.7, c2[1] + 1.0, color=SLATE,
          lw=1.4, ms=8, rad=-0.45)
    arrow(ax, c2[0] - 2.7, c2[1] - 1.0, c1[0] + 2.7, c1[1] - 1.0, color=SLATE,
          lw=1.4, ms=8, rad=-0.45)
    ax.text((c1[0] + c2[0]) / 2, c1[1] + 4.4, "in=1", ha="center", va="center",
            fontsize=FS_SMALL - 2.5, color=SLATE)
    ax.text((c1[0] + c2[0]) / 2, c1[1] - 4.4, "in=0", ha="center", va="center",
            fontsize=FS_SMALL - 2.5, color=SLATE)
    wrap(ax, x + w / 2, top - 18.0, w - 3.0, "States and the transitions "
         "between them. The natural way to say what a sequential circuit does.",
         FS_SMALL - 1.5, ha="center", lh=2.5)

    # 4 — pseudo-code
    x = xs[3]
    for i, ln in enumerate(("count = 0", "repeat forever:",
                            "   wait for clock", "   count = count + 1")):
        ax.text(x + 2.2, top - 7.8 - i * 2.7, ln, ha="left", va="center",
                fontsize=FS_SMALL - 2.0, color=INK,
                family="DejaVu Sans Mono")
    wrap(ax, x + w / 2, top - 20.4, w - 3.0, "An algorithm, written much as "
         "you would in C. The highest level of abstraction in the flow.",
         FS_SMALL - 1.5, ha="center", lh=2.5)
    save(f, "behavioral_forms")


def netlist_graph():
    f, ax, H = panel(4.44)
    title(ax, 50, H - 3.5, "\"The vertices indicate components, and the edges "
          "indicate interconnections.\"", size=FS_SUB, color=SLATE,
          weight="normal")

    cy = (H - 7) / 2.0 + 2.0
    nodes = {"A": (6.0, cy + 7.0, SLATE, "input"),
             "B": (6.0, cy - 7.0, SLATE, "input"),
             "U1": (24.0, cy + 7.0, TEAL, "adder"),
             "U2": (24.0, cy - 7.0, VIOLET, "multiplier"),
             "U3": (43.0, cy, GREEN, "adder"),
             "Y": (60.0, cy, AMBER, "output")}
    edges = [("A", "U1", "a[7:0]"), ("B", "U1", ""), ("B", "U2", "b[7:0]"),
             ("A", "U2", ""), ("U1", "U3", "sum"), ("U2", "U3", "prod")]
    for a, b, lab in edges:
        (x1, y1, _, _), (x2, y2, _, _) = nodes[a], nodes[b]
        arrow(ax, x1 + 3.6, y1, x2 - 3.6, y2, color=SLATE, lw=1.6, ms=10)
        if lab:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.5, lab, ha="center",
                    va="center", fontsize=FS_SMALL - 2.5, color=SLATE)
    arrow(ax, nodes["U3"][0] + 3.6, cy, nodes["Y"][0] - 3.6, cy, color=SLATE,
          lw=1.6, ms=10)
    for name, (x, y, col, kind) in nodes.items():
        ax.add_patch(Circle((x, y), 3.6, fc=WHITE, ec=col, lw=2.0, zorder=5))
        ax.text(x, y, name, ha="center", va="center", fontsize=FS_SMALL - 0.5,
                color=col, fontweight="bold", zorder=6)
        ax.text(x, y - 5.6, kind, ha="center", va="center",
                fontsize=FS_SMALL - 2.0, color=SLATE, zorder=6)

    rowcards(ax, 70.0, H - 6, 28.0, [
        ("VERTEX", "one component", TEAL),
        ("EDGE", "a wire between two", VIOLET),
        ("THE WHOLE GRAPH", "the design itself", GREEN)], gap=1.4)
    save(f, "netlist_graph")


def netlist_levels():
    f, ax, H = panel(3.94)
    title(ax, 50, H - 3.5, "\"Netlist may be specified at various levels, where "
          "the components may be functional modules, gates or transistors.\"",
          size=FS_SUB, color=SLATE, weight="normal")

    top = H - 7
    bh = 20.0
    w = 31.0
    gap = 1.7
    specs = [("FUNCTIONAL LEVEL", TEAL, ["ADDER", "MUX", "REG"],
              "a handful of blocks"),
             ("GATE LEVEL", GREEN, ["AND", "XOR", "NOT"], "dozens of cells"),
             ("TRANSISTOR LEVEL", AMBER, ["nMOS", "pMOS", "nMOS"],
              "hundreds of devices")]
    for i, (head, col, parts, count) in enumerate(specs):
        x = 2.5 + i * (w + gap)
        box(ax, x, top - bh, w, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 4.2, w, 4.2, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, top - 2.1, head, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        bw = 7.6
        bx = x + (w - 3 * bw - 2 * 2.2) / 2
        byy = top - 11.0
        for j, pname in enumerate(parts):
            px = bx + j * (bw + 2.2)
            box(ax, px, byy - 4.2, bw, 4.2, fc=LIGHT, ec=col, lw=1.4)
            ax.text(px + bw / 2, byy - 2.1, pname, ha="center", va="center",
                    fontsize=FS_SMALL - 2.0, color=col, fontweight="bold")
            if j < 2:
                arrow(ax, px + bw + 0.2, byy - 2.1, px + bw + 2.0, byy - 2.1,
                      color=SLATE, lw=1.3, ms=7)
        ax.text(x + w / 2, top - 17.4, count, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=SLATE, fontstyle="italic")
        if i < 2:
            arrow(ax, x + w + 0.2, top - bh / 2, x + w + gap - 0.2,
                  top - bh / 2, color=SLATE, lw=1.8, ms=10)
    ax.text(50, top - bh - 3.6, "synthesis moves you left to right — never the "
            "other way", ha="center", va="center", fontsize=FS_SMALL,
            color=NAVY, fontweight="bold")
    save(f, "netlist_levels")


def struct_vs_behav():
    f, ax, H = panel(3.40)

    column_cards(ax, 2.5, H - 1.5, 95.5, [
        ("BEHAVIOURAL — say WHAT it does",
         "You describe the result. \"The output is the sum of the two inputs.\" "
         "You say nothing about which gates are used, or how many. The "
         "synthesis tool chooses.", VIOLET),
        ("STRUCTURAL — say WHAT IT IS MADE OF",
         "You name the parts and wire them together. \"Instantiate a half "
         "adder here, another there, and an OR gate across their carries.\" "
         "This is a netlist, written as text.", TEAL)], gap=2.4)

    save(f, "struct_vs_behav")


def standard_cell():
    f, ax, H = panel(4.24)
    title(ax, 50, H - 3.5, "\"A pre-designed circuit module — like gates, "
          "flip-flops, a multiplexer — at the layout level.\"", size=FS_SUB,
          color=SLATE, weight="normal")

    top = H - 7
    bh = 21.0
    # three views of one cell, side by side
    w = 30.6
    # 1: the symbol
    box(ax, 2.5, top - bh, w, bh, fc=WHITE, ec=TEAL, lw=1.8)
    box(ax, 2.5, top - 4.0, w, 4.0, fc=TEAL, ec=TEAL, lw=1.0)
    ax.text(2.5 + w / 2, top - 2.0, "THE SYMBOL", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
    gate(ax, "NAND", 11.5, top - 11.0, w=10.0, h=7.5, ec=NAVY, stub=3.0)
    ax.text(2.5 + w / 2, top - 18.0, "what you draw", ha="center", va="center",
            fontsize=FS_SMALL - 1.5, color=SLATE)

    # 2: the behaviour
    x = 2.5 + w + 1.85
    box(ax, x, top - bh, w, bh, fc=WHITE, ec=VIOLET, lw=1.8)
    box(ax, x, top - 4.0, w, 4.0, fc=VIOLET, ec=VIOLET, lw=1.0)
    ax.text(x + w / 2, top - 2.0, "THE BEHAVIOUR", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
    tw, trh = 4.2, 2.2
    tx = x + (w - 3 * tw) / 2
    ty = top - 5.4
    for j, hcell in enumerate(("a", "b", "y")):
        box(ax, tx + j * tw, ty - trh, tw, trh, fc=VIOLET, ec=VIOLET, lw=0.6,
            r=0.0)
        ax.text(tx + j * tw + tw / 2, ty - trh / 2, hcell, ha="center",
                va="center", fontsize=FS_SMALL - 2.0, color=WHITE,
                fontweight="bold")
    for i, row in enumerate((("0", "0", "1"), ("0", "1", "1"),
                             ("1", "0", "1"), ("1", "1", "0"))):
        yy = ty - trh * (i + 1)
        for j, cell in enumerate(row):
            box(ax, tx + j * tw, yy - trh, tw, trh,
                fc=WHITE if i % 2 == 0 else LIGHT, ec=GRID, lw=0.6, r=0.0)
            ax.text(tx + j * tw + tw / 2, yy - trh / 2, cell, ha="center",
                    va="center", fontsize=FS_SMALL - 2.0, color=BODY)
    ax.text(x + w / 2, top - 18.0, "what it computes", ha="center", va="center",
            fontsize=FS_SMALL - 1.5, color=SLATE)

    # 3: the layout
    x = 2.5 + 2 * (w + 1.85)
    box(ax, x, top - bh, w, bh, fc=WHITE, ec=AMBER, lw=1.8)
    box(ax, x, top - 4.0, w, 4.0, fc=AMBER, ec=AMBER, lw=1.0)
    ax.text(x + w / 2, top - 2.0, "THE LAYOUT", ha="center", va="center",
            fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
    lx, ly, lw_, lh_ = x + 4.0, top - 16.4, w - 8.0, 10.0
    box(ax, lx, ly, lw_, lh_, fc="#FFF7EC", ec=AMBER, lw=1.2)
    for k in range(4):
        box(ax, lx + 1.2 + k * (lw_ - 2.4) / 4.0, ly + 1.2,
            (lw_ - 2.4) / 4.0 - 0.8, lh_ - 2.4,
            fc=[TEAL, VIOLET, TEAL, VIOLET][k], ec="none", lw=0, r=0.2)
    ax.text(x + w / 2, top - 18.6, "the shapes on silicon", ha="center",
            va="center", fontsize=FS_SMALL - 1.5, color=SLATE)

    save(f, "standard_cell")


def opt_conflict():
    f, ax, H = panel(3.49)

    column_cards(ax, 2.5, H - 1.5, 95.5, [
        ("FEWER GATES",
         "Fewer cells means less silicon area, and a cheaper chip. But the "
         "cheapest structure is often a deep one — and deep means slow.",
         TEAL),
        ("FEWER GATE LEVELS",
         "The depth of the logic is its delay, and delay is what limits your "
         "clock. Flattening it costs extra gates, and so costs area.",
         VIOLET),
        ("FEWER SIGNAL TRANSITIONS",
         "Every time a gate output changes, charge moves and energy is spent. "
         "Reducing that switching is dynamic power saved — usually by adding "
         "control logic.", AMBER)], gap=2.0)
    save(f, "opt_conflict")


def physical_design():
    f, ax, H = panel(3.85)

    layers = [("METAL 3", "long-distance wiring", "#7A4FBF"),
              ("METAL 2", "block-to-block wiring", "#1B9AAA"),
              ("METAL 1", "wiring inside a cell", "#2A9D5C"),
              ("POLYSILICON", "transistor gates", "#C77514"),
              ("DIFFUSION", "transistor sources and drains", "#D6224A"),
              ("SUBSTRATE", "the silicon wafer itself", "#5A6B7B")]
    top = H - 2.5
    lh_ = 4.2
    y = top
    for name, what, col in layers:
        # a stack of plates, each offset a little to suggest depth
        box(ax, 8.0, y - lh_, 34.0, lh_, fc=col, ec=col, lw=0, r=0.4)
        ax.text(25.0, y - lh_ / 2, name, ha="center", va="center",
                fontsize=FS_SMALL - 1.0, color=WHITE, fontweight="bold")
        ax.text(45.0, y - lh_ / 2, what, ha="left", va="center",
                fontsize=FS_SMALL - 0.5, color=BODY)
        y -= lh_ + 0.9

    ax.text(45.0, top + 1.6, "a modern chip has 10–15 of these layers",
            ha="left", va="center", fontsize=FS_SMALL - 1.0, color=SLATE,
            fontstyle="italic")
    save(f, "physical_design")


def asic_vs_fpga():
    f, ax, H = panel(3.99)

    headers = ["", "ASIC  (fabricate a chip)", "FPGA  (program a device)"]
    rows = [["What you receive", "masks, then wafers from a foundry",
             "a bitstream you load into a board"],
            ["Turnaround", "weeks to months", "minutes"],
            ["Cost to start", "very high — mask sets dominate",
             "the price of the board"],
            ["Cost per unit at volume", "very low", "stays high"],
            ["Speed", "highest", "lower — logic is configurable, not fixed"],
            ["Can you change it after?", "no — respin and pay again",
             "yes, reprogram in the lab"],
            ["Used for", "high volume, or when speed decides",
             "prototypes, small runs, teaching"]]
    widths = [26.0, 33.0, 36.5]
    x0 = 2.5
    y = H - 2
    rh = 4.0
    cx = x0
    for wdt, h in zip(widths, headers):
        box(ax, cx, y - rh, wdt, rh, fc=NAVY, ec=NAVY, lw=0.8, r=0.0)
        ax.text(cx + wdt / 2, y - rh / 2, h, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        cx += wdt
    y -= rh
    for i, row in enumerate(rows):
        cx = x0
        for j, (wdt, cell) in enumerate(zip(widths, row)):
            box(ax, cx, y - rh, wdt, rh, fc=WHITE if i % 2 == 0 else LIGHT,
                ec=GRID, lw=0.8, r=0.0)
            ax.text(cx + wdt / 2, y - rh / 2, cell, ha="center", va="center",
                    fontsize=FS_SMALL - 1.5,
                    color=NAVY if j == 0 else (TEAL if j == 1 else VIOLET),
                    fontweight="bold" if j == 0 else "normal")
            cx += wdt
        y -= rh
    save(f, "asic_vs_fpga")


def other_steps():
    f, ax, H = panel(3.60)

    column_cards(ax, 2.5, H - 1.5, 95.5, [
        ("SIMULATION — to verify",
         "Apply stimulus to the description and watch what comes out. Done at "
         "the logic, switch and circuit level. This is the one you will use "
         "constantly, from Lab 1 onwards.", GREEN),
        ("FORMAL VERIFICATION",
         "Prove mathematically that the design meets its specification, "
         "instead of testing it case by case. Powerful, and named here — but "
         "beyond this course.", VIOLET),
        ("TESTABILITY AND ATPG",
         "Once a chip has been manufactured, you still have to check that THIS "
         "copy of it works. That needs patterns designed to expose "
         "manufacturing faults.", AMBER)], gap=2.0)
    save(f, "other_steps")


def course_roadmap():
    f, ax, H = panel(4.20)

    bands = [("Behavioral / Data Path",
              "Weeks 1–4 · language features, description styles, procedural "
              "assignment, blocking vs non-blocking", VIOLET, 8.0),
             ("Verification",
              "Week 5 · test benches, and modelling finite state machines",
              GREEN, 7.0),
             ("Synthesis-aware coding",
              "Week 6 · synthesizable Verilog, and recommended practices",
              TEAL, 7.0),
             ("Structure and case studies",
              "Weeks 7–8 · memory, register banks, pipelining, switch level, "
              "and a complete processor", AMBER, 8.0)]
    y = H - 2.5
    for name, detail, col, bh in bands:
        box(ax, 2.5, y - bh, 95.5, bh, fc=WHITE, ec=col, lw=1.6)
        box(ax, 2.5, y - bh, 24.0, bh, fc=col, ec=col, lw=1.0)
        wrap(ax, 14.5, y - bh / 2 + 1.3, 19.0, name, FS_SMALL - 1.0,
             color=WHITE, ha="center", weight="bold", lh=2.6)
        wrap(ax, 28.5, y - bh / 2 + 1.3, 64.0, detail, FS_SMALL - 1.0, lh=2.6)
        y -= bh + 1.2

    save(f, "course_roadmap")


if __name__ == "__main__":
    behavioral_forms()
    netlist_graph()
    netlist_levels()
    struct_vs_behav()
    standard_cell()
    opt_conflict()
    physical_design()
    asic_vs_fpga()
    other_steps()
    course_roadmap()
