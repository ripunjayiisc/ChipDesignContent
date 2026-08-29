# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — the RTL design process and methodology."""
import _boot
from dsl import *


def design_flow():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "The RTL design flow, and where this topic sits",
          FS_TITLE)

    stages = [("SPECIFICATION", "what it must do, in words, before any code",
               NAVY, ""),
              ("MICRO-ARCHITECTURE", "cycles, registers, partitioning", NAVY,
               "Topic 2"),
              ("RTL CODING", "the design, written in an HDL", TEAL,
               "Topics 2, 4"),
              ("LINT", "coding rules, checked mechanically", TEAL, "Topic 2"),
              ("SIMULATION", "does it do what the spec says?", VIOLET,
               "Topic 5"),
              ("SYNTHESIS", "RTL becomes a gate netlist", VIOLET, "Topics 2, 4"),
              ("GATE-LEVEL CHECK", "does the netlist still do it?", GREEN,
               "Topic 2"),
              ("TIMING ANALYSIS", "is it fast enough?", GREEN, "Topic 6"),
              ("PLACE AND ROUTE", "gates become geometry", AMBER, "Module 3"),
              ("SIGN-OFF", "every check passes at every corner", AMBER,
               "Module 3")]
    y = H - 9.0
    rh = 3.6
    for nm, what, col, where in stages:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.3)
        box(ax, 3, y - rh, 29, rh, fc=col, ec=col)
        ax.text(17.5, y - rh / 2, nm, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold")
        ax.text(33, y - rh / 2, what, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        if where:
            ax.text(95, y - rh / 2, where, ha="right", va="center",
                    fontsize=FS_SMALL - 1, color=col, fontstyle="italic")
        y -= rh + 0.6

    ax.text(50, 2.5, "Every arrow points both ways in practice: a timing failure "
                     "sends you back to the RTL.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "design_flow")


def flow_executed():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "A methodology is a set of gates, not a set of "
                           "suggestions", FS_TITLE)
    ax.text(50, H - 10.0, "make flow  -  seven stages on one design, each "
                          "producing evidence.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    rows = [["1", "SPEC", "written before the RTL", "4 sentences"],
            ["2", "LINT", "tools/rtl_lint.py", "0 issues"],
            ["3", "RTL SIMULATION", "iverilog, 18 cycles", "wraps at 15"],
            ["4", "SYNTHESIS", "yosys", "12 cells"],
            ["5", "GATE SIMULATION", "the netlist, same stimulus", "18 cycles"],
            ["6", "COMPARE", "RTL against gate transcript", "identical"],
            ["7", "PROVE", "formal equivalence", "proven by induction"]]
    table(ax, 3, H - 13.0, ["", "stage", "what runs", "evidence produced"], rows,
          [7, 26, 32, 29], 3.9, size=FS_TABLE, bold_col=[1],
          colcolors={3: GREEN})

    ax.text(50, 2.0, "Stage 6 says they agree on the 18 cycles tested. Stage 7 "
                     "proves they agree on EVERY input sequence.",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold")
    save(f, "flow_executed")


def synth_subset():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "Which Verilog actually synthesises - measured",
          FS_TITLE)

    rows = [["always @* with full case", "OK", "10", "clean"],
            ["clocked block with <=", "OK", "8", "8 flip-flops"],
            ["if with no else", "OK", "1", "inferred a LATCH"],
            ["incomplete sensitivity list", "OK", "1", "built anyway"],
            ["#5 delay in RTL", "OK", "1", "the delay silently vanished"],
            ["initial block", "OK", "10", "accepted - FPGA only, not ASIC"],
            ["for loop, constant bounds", "OK", "7", "unrolled into 7 gates"],
            ["while loop, data-dependent", "REFUSED", "-", "not a constant "
             "function"],
            ["real (floating point)", "REFUSED", "-", "syntax error"],
            ["a / b   variable divisor", "OK", "371", "a full divider"],
            ["a / 4   constant divisor", "OK", "0", "no logic at all - wires"]]
    table(ax, 3, H - 10.0, ["construct", "synth", "cells", "what the tool said"],
          rows, [30, 14, 12, 38], 3.4, size=FS_TABLE, bold_col=[0, 2],
          colcolors={2: NAVY})

    ax.text(50, 5.5, "371 cells against 0, for the same operator.",
            fontsize=FS_HEAD, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 1.8, "The difference is entirely what you divided BY.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "synth_subset")


def latch_inference():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The inferred latch: the most common RTL bug there is",
          FS_TITLE)

    y = H - 10.0
    box(ax, 22, y - 16.0, 56, 16.0, fc="#FDECEF", ec=RED, lw=2.0)
    ax.text(50, y - 4.5, "always @* begin", fontsize=13, color=NAVY,
            ha="center", family="monospace")
    ax.text(50, y - 8.5, "    if (en) y = d;", fontsize=13, color=NAVY,
            ha="center", family="monospace")
    ax.text(50, y - 12.5, "end", fontsize=13, color=NAVY, ha="center",
            family="monospace")

    ax.text(50, y - 19.5, "no else - so you never said what y is when en = 0",
            fontsize=FS_BODY, color=RED, ha="center", fontstyle="italic")
    arrow(ax, 50, y - 21.5, 50, y - 25.0, color=NAVY, lw=2.2, ms=13)

    label_box(ax, 32, y - 33.0, 36, 7.5, "$_DLATCH_P_", fc=WHITE, ec=RED,
              tc=RED, size=FS_HEAD, lw=2.2)

    ax.text(50, 3.0, "A level-sensitive latch you did not ask for - and it is "
                     "not an error, so nothing stops you.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "latch_inference")


def sim_synth_mismatch():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "When simulation and silicon disagree", FS_TITLE,
          color=RED)
    ax.text(50, H - 10.0, "always @(a) begin  y = a & b;  end     "
                          "- b is read, but not in the list.",
            fontsize=FS_SUB, color=SLATE, ha="center", family="monospace")

    rows = [["start", "0", "0", "0", "0", ""],
            ["change a", "1", "0", "0", "0", ""],
            ["change b", "1", "1", "0", "1", "DISAGREE"],
            ["change b", "1", "0", "0", "0", ""],
            ["change a", "0", "0", "0", "0", ""],
            ["change b", "0", "1", "0", "0", ""]]
    table(ax, 8, H - 14.0, ["stimulus", "a", "b", "RTL y", "NETLIST y", ""], rows,
          [22, 8, 8, 12, 14, 20], 3.7, size=FS_TABLE, bold_col=[0],
          colcolors={5: RED})

    ax.text(50, 5.5, "Your testbench was verifying a circuit that will never be "
                     "built.", fontsize=FS_HEAD, color=RED, ha="center",
            fontweight="bold")
    ax.text(50, 1.8, "One disagreement in six - and nothing anywhere reported an "
                     "error. Never maintain a sensitivity list by hand.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "sim_synth_mismatch")


def lint_rules():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Seven rules, checked by a tool instead of by memory",
          FS_TITLE)

    rows = [["L001", "blocking (=) in a clocked block",
             "two blocks see half-updated values"],
            ["L002", "non-blocking (<=) in a combinational block",
             "simulates as a register, builds as logic"],
            ["L003", "= and <= mixed in one block", "no reader can tell the intent"],
            ["L004", "explicit sensitivity list", "you maintain it, for ever"],
            ["L005", "if with no else in a combinational block", "infers a LATCH"],
            ["L006", "case with no default", "infers a LATCH"],
            ["L007", "signal driven from two always blocks", "two drivers"]]
    table(ax, 3, H - 9.5, ["rule", "what it catches", "why it matters"], rows,
          [10, 44, 40], 4.0, size=FS_TABLE, bold_col=[0])

    ax.text(50, 5.0, "16 files  ·  linter and Yosys agree on every one  ·  0 "
                     "disagreements",
            fontsize=FS_BODY, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 1.5, "L005 and L006 are not opinions - they predict what a "
                     "synthesiser will build, and make lintcheck settles it.",
            fontsize=FS_SMALL, color=BODY, ha="center")
    save(f, "lint_rules")


def coding_rules():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The RTL coding rules, in one place", FS_TITLE)

    groups = [("Combinational logic", GREEN,
               ["always @*  - never a hand-written", "sensitivity list",
                "", "blocking assignments (=) only", "",
                "assign every output on every path"]),
              ("Sequential logic", TEAL,
               ["always @(posedge clk) - one clock,", "one edge",
                "", "non-blocking assignments (<=) only", "",
                "one signal, one always block, ever"]),
              ("Never in synthesisable RTL", RED,
               ["# delays, initial, real, unbounded", "loops",
                "", "both clock edges in one path", "",
                "a clock built from logic - use an enable"])]
    top = H - 9.5
    bh = 30.0
    x = 3
    for nm, col, items in groups:
        box(ax, x, top - bh, 30.6, bh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, top - 7.0, 30.6, 7.0, fc=col, ec=col)
        ax.text(x + 15.3, top - 3.5, nm, ha="center", va="center",
                fontsize=FS_BODY, color=WHITE, fontweight="bold")
        for i, it in enumerate(items):
            if it:
                ax.text(x + 1.6, top - 10.5 - i * 3.0, it, fontsize=FS_SMALL - 0.5,
                        color=BODY, ha="left", va="center")
        x += 32.7

    ax.text(50, 4.0, "None of these are style preferences. Each one exists "
                     "because breaking it produces a simulate/build mismatch.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "coding_rules")


def partitioning():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Micro-architecture: the decisions RTL cannot make "
                           "for you", FS_TITLE)

    rows = [["How many clock cycles?", "one big cycle, or a pipeline",
             "Fmax, latency, area"],
            ["Where do the registers go?", "stage boundaries", "Fmax, directly"],
            ["What is shared?", "one multiplier reused, or four in parallel",
             "area against throughput"],
            ["How is it partitioned?", "module boundaries, hierarchy",
             "readability and reuse"],
            ["What is the interface?", "handshake, valid/ready, fixed latency",
             "how easily it plugs in"],
            ["Where does reset reach?", "everything, or only what needs it",
             "area, routing congestion"]]
    table(ax, 3, H - 9.5, ["the decision", "the options", "what it costs you"],
          rows, [26, 38, 30], 4.2, size=FS_TABLE, bold_col=[0])

    ax.text(50, 5.5, "A synthesiser is better than you are at choosing gates.",
            fontsize=FS_HEAD, color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 1.8, "It is not better than you at any row above, and it will "
                     "not warn you that you chose badly.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "partitioning")


def reuse():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Writing RTL that someone else can use", FS_TITLE)

    items = [("Parameterise, do not duplicate",
              "WIDTH as a parameter, not four copies", TEAL),
             ("One clock, stated in the name",
              "clk, and which domain it belongs to", TEAL),
             ("Reset policy, written down",
              "sync or async, high or low - pick one", NAVY),
             ("No magic numbers",
              "a named localparam beats 8'd47 in a case", NAVY),
             ("An interface, not a pile of wires",
              "valid/ready is understood everywhere", VIOLET),
             ("A testbench that ships with it",
              "IP without one is a liability, not an asset", GREEN)]
    y = H - 9.5
    rh = 4.6
    for hd, sub, col in items:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        ax.text(6, y - rh / 2, hd, ha="left", va="center", fontsize=FS_BODY,
                color=col, fontweight="bold")
        ax.text(50, y - rh / 2, sub, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        y -= rh + 0.9

    ax.text(50, 2.5, "Could a colleague drop it into another design next year "
                     "without asking you anything?",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "reuse")


for fn in (design_flow, flow_executed, synth_subset, latch_inference,
           sim_synth_mismatch, lint_rules, coding_rules, partitioning, reuse):
    fn()
