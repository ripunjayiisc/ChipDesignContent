# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — the RTL design process and methodology."""
import _boot
from dsl import *


def design_flow():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 81.7
    title(ax, 50, H - 3, "The RTL design flow, and where this topic sits", 12.5)

    stages = [("SPECIFICATION", "what it must do, in words, before any code", NAVY,
               ""),
              ("MICRO-ARCHITECTURE", "how many cycles, which registers, what "
               "partitioning", NAVY, "Topic 2"),
              ("RTL CODING", "the design, written in an HDL", TEAL, "Topics 2, 4"),
              ("LINT", "coding rules, checked mechanically - seconds", TEAL,
               "Topic 2"),
              ("SIMULATION", "does it do what the spec says?", VIOLET, "Topic 5"),
              ("SYNTHESIS", "RTL becomes a gate netlist", VIOLET, "Topic 2, 4"),
              ("GATE-LEVEL CHECK", "does the netlist still do it?", GREEN,
               "Topic 2"),
              ("TIMING ANALYSIS", "is it fast enough, and does it work at all?",
               GREEN, "Topic 6"),
              ("PLACE AND ROUTE", "gates become geometry", AMBER, "Module 3"),
              ("SIGN-OFF", "every check passes at every corner", AMBER, "Module 3")]
    y = H - 8.0
    rh = 5.4
    for nm, what, col, where in stages:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.2)
        box(ax, 3, y - rh, 27, rh, fc=col, ec=col)
        ax.text(16.5, y - rh / 2, nm, ha="center", va="center", fontsize=8.4,
                color=WHITE, fontweight="bold")
        ax.text(32, y - rh / 2, what, ha="left", va="center", fontsize=8.2,
                color=BODY)
        if where:
            ax.text(94, y - rh / 2, where, ha="right", va="center", fontsize=7.8,
                    color=col, fontstyle="italic")
        y -= rh + 0.9

    box(ax, 3, 3.0, 94, 8.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 8.0, "Every arrow points both ways in practice", fontsize=9.2,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.4, "A timing failure sends you back to the RTL; a synthesis surprise "
                     "sends you back to the micro-architecture.",
            fontsize=8.3, color=BODY, ha="center")
    save(f, "design_flow")


def flow_executed():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "A methodology is a set of gates, not a set of suggestions",
          12)
    ax.text(50, H - 7.4, "make flow  -  seven stages on one design, each producing "
                         "evidence.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["1", "SPEC", "written before the RTL", "4 sentences"],
            ["2", "LINT", "tools/rtl_lint.py", "0 issues"],
            ["3", "RTL SIMULATION", "iverilog, 18 cycles", "wraps at 15, tc correct"],
            ["4", "SYNTHESIS", "yosys", "12 cells"],
            ["5", "GATE SIMULATION", "the netlist, same stimulus", "18 cycles"],
            ["6", "COMPARE", "RTL against gate transcript", "identical"],
            ["7", "PROVE", "formal equivalence", "proven by induction"]]
    table(ax, 3, H - 10.5, ["", "stage", "what runs", "evidence produced"],
          rows, [7, 26, 32, 29], 5.0, size=8.4, bold_col=[1],
          colcolors={3: GREEN})

    box(ax, 3, 3.0, 94, 15.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 14.6, "Stage 7 is the one worth understanding", fontsize=9.4,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 9.6, "Stage 6 says the two agree on the 18 cycles that were tested. "
                     "Stage 7 proves they agree on\nEVERY input sequence, by "
                     "induction, without enumerating any of them.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.6, "The script stops at the first stage that fails. That is what "
                     "makes it a methodology.",
            fontsize=8.4, color=NAVY, ha="center", fontstyle="italic")
    save(f, "flow_executed")


def synth_subset():
    W, Hin = 11.5, 9.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 85.2
    title(ax, 50, H - 3, "Which Verilog actually synthesises - measured", 12.5)
    ax.text(50, H - 7.2, "\"Verilog is not a programming language\" stays a slogan "
                         "until you watch a tool refuse.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["always @* with full case", "OK", "10", "clean"],
            ["clocked block with <=", "OK", "8", "8 flip-flops"],
            ["if with no else", "OK", "1", "inferred a LATCH"],
            ["incomplete sensitivity list", "OK", "1", "built anyway - see next slide"],
            ["#5 delay in RTL", "OK", "1", "the delay silently vanished"],
            ["initial block", "OK", "10", "accepted - FPGA only, not ASIC"],
            ["for loop, constant bounds", "OK", "7", "unrolled into 7 gates"],
            ["while loop, data-dependent", "REFUSED", "-", "\"only allowed in "
             "constant functions\""],
            ["real (floating point)", "REFUSED", "-", "\"syntax error, unexpected "
             "TOK_REAL\""],
            ["a / b  (variable divisor)", "OK", "371", "a full combinational divider"],
            ["a / 4  (constant divisor)", "OK", "0", "no logic at all - just wires"]]
    table(ax, 3, H - 10.0, ["construct", "synth", "cells", "what the tool said"],
          rows, [30, 14, 12, 38], 4.6, size=8.2, bold_col=[0, 2],
          colcolors={2: NAVY})

    box(ax, 3, 3.0, 94, 12.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 12.0, "371 cells against 0, for the same operator", fontsize=9.4,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 7.2, "The difference is entirely what you divided BY. A constant power "
                     "of two is a rename of wires;\na variable divisor is one of the "
                     "largest things you can ask for by accident.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "synth_subset")


def latch_inference():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "The inferred latch: the most common RTL bug there is", 12.5)

    y = H - 10.0
    box(ax, 4, y - 16.0, 92, 16.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, y - 4.0, "always @* begin", fontsize=9.6, color=NAVY, ha="center",
            family="monospace")
    ax.text(50, y - 7.6, "    if (en) y = d;", fontsize=9.6, color=NAVY,
            ha="center", family="monospace")
    ax.text(50, y - 11.2, "end", fontsize=9.6, color=NAVY, ha="center",
            family="monospace")
    ax.text(50, y - 14.4, "there is no else, so you never said what y is when en = 0",
            fontsize=8.6, color=RED, ha="center", fontstyle="italic")

    ax.text(50, y - 20.0, "so the tool must build something that REMEMBERS",
            fontsize=9.4, color=NAVY, ha="center", fontweight="bold")

    y2 = y - 24.0
    label_box(ax, 34, y2 - 9.0, 32, 9.0, "$_DLATCH_P_", fc=WHITE, ec=RED, tc=RED,
              size=9.4, lw=2.0)
    ax.text(50, y2 - 12.6, "a level-sensitive latch you did not ask for",
            fontsize=8.4, color=RED, ha="center")

    box(ax, 4, 3.0, 92, 13.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 12.6, "Why it is worse than an error", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 7.6, "It is not an error at all. The tool builds it, mentions it in a "
                     "log nobody reads, and hands you a\ndesign with a memory element "
                     "in the middle of what you thought was combinational logic -\n"
                     "which then has its own timing requirements, and breaks your "
                     "static timing analysis.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "latch_inference")


def sim_synth_mismatch():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 81.7
    title(ax, 50, H - 3, "When simulation and silicon disagree", 13, color=RED)
    ax.text(50, H - 7.4, "always @(a) begin  y = a & b;  end        "
                         "- b is read, but not in the list.",
            fontsize=8.8, color=SLATE, ha="center", family="monospace")

    rows = [["start", "0", "0", "0", "0", ""],
            ["change a", "1", "0", "0", "0", ""],
            ["change b", "1", "1", "0", "1", "DISAGREE"],
            ["change b", "1", "0", "0", "0", ""],
            ["change a", "0", "0", "0", "0", ""],
            ["change b", "0", "1", "0", "0", ""]]
    table(ax, 8, H - 11.0, ["stimulus", "a", "b", "RTL y", "NETLIST y", ""],
          rows, [22, 8, 8, 12, 14, 20], 4.8, size=8.6, bold_col=[0],
          colcolors={5: RED})

    box(ax, 4, 19.0, 92, 15.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 31.6, "Your testbench was verifying a circuit that will never be built",
            fontsize=9.6, color=RED, ha="center", fontweight="bold")
    ax.text(50, 26.4, "The RTL only re-evaluates when a changes, so y goes stale "
                      "whenever b moves alone.\nSynthesis ignored the sensitivity "
                      "list entirely and built the AND gate you meant.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 21.0, "One disagreement in six - and nothing anywhere reported an "
                      "error.",
            fontsize=8.6, color=RED, ha="center", fontweight="bold")

    box(ax, 4, 3.0, 92, 13.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 12.6, "Which is why the rule is: never maintain a sensitivity list "
                      "by hand", fontsize=9.4, color=GREEN, ha="center",
            fontweight="bold")
    ax.text(50, 7.6, "always @*  builds it for you, and keeps it correct every time "
                     "you edit the block.\nSystemVerilog's always_comb does the same "
                     "and also makes the tool check it.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "sim_synth_mismatch")


def lint_rules():
    W, Hin = 11.5, 9.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 80.0
    title(ax, 50, H - 3, "Seven rules, checked by a tool instead of by memory", 12.5)

    rows = [["L001", "blocking (=) in a clocked block",
             "two blocks see half-updated values"],
            ["L002", "non-blocking (<=) in a combinational block",
             "simulates like a register, synthesises as logic"],
            ["L003", "= and <= mixed in one block", "no reader can tell the intent"],
            ["L004", "explicit sensitivity list", "you have to maintain it, for ever"],
            ["L005", "if with no else in a combinational block", "infers a LATCH"],
            ["L006", "case with no default", "infers a LATCH"],
            ["L007", "signal driven from two always blocks",
             "two drivers - last one to run wins"]]
    table(ax, 3, H - 9.0, ["rule", "what it catches", "why it matters"],
          rows, [10, 42, 42], 5.4, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 20.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, 19.6, "And the two latch rules are not opinions", fontsize=9.4,
            color=GREEN, ha="center", fontweight="bold")
    ax.text(50, 14.6, "L005 and L006 claim a synthesiser will build a latch. That is a "
                      "claim about what a tool does,\nso the tool settles it: "
                      "make lintcheck runs both and compares.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 8.4, "10 files  ·  linter and Yosys agree on every one  ·  0 "
                     "disagreements",
            fontsize=9.0, color=NAVY, ha="center", family="monospace",
            fontweight="bold")
    ax.text(50, 4.4, "A linter that cries wolf gets switched off; one that stays "
                     "quiet is worse than none at all.",
            fontsize=8.4, color=SLATE, ha="center", fontstyle="italic")
    save(f, "lint_rules")


def coding_rules():
    W, Hin = 11.5, 8.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 76.5
    title(ax, 50, H - 3, "The RTL coding rules, in one place", 13)

    y = H - 9.0
    groups = [("Combinational logic", GREEN,
               ["always @*  - never a hand-written sensitivity list",
                "blocking assignments (=) only",
                "assign every output on every path - else, or default"]),
              ("Sequential logic", TEAL,
               ["always @(posedge clk) - one clock, one edge",
                "non-blocking assignments (<=) only",
                "one signal, one always block, for ever"]),
              ("Never in synthesisable RTL", RED,
               ["# delays, initial blocks, real, unbounded loops",
                "both clock edges in the same path",
                "a clock built from combinational logic - use an enable"])]
    bh = 15.0
    for nm, col, items in groups:
        box(ax, 3, y - bh, 94, bh, fc=WHITE, ec=col, lw=1.6)
        box(ax, 3, y - 5.0, 94, 5.0, fc=col, ec=col)
        ax.text(6, y - 2.5, nm, ha="left", va="center", fontsize=9.2, color=WHITE,
                fontweight="bold")
        for i, it in enumerate(items):
            ax.text(7, y - 8.0 - i * 3.1, "•", fontsize=8.4, color=col, ha="left")
            ax.text(10, y - 8.0 - i * 3.1, it, fontsize=8.3, color=BODY, ha="left")
        y -= bh + 1.8

    box(ax, 3, 3.0, 94, 12.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 11.6, "None of these are style preferences", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 6.8, "Every one of them exists because breaking it produces a design "
                     "that simulates differently from\nthe way it is built - and that "
                     "class of bug survives every test you write.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "coding_rules")


def partitioning():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Micro-architecture: the decisions RTL cannot make for you",
          12.5)
    ax.text(50, H - 7.2, "Synthesis chooses gates. It does not choose any of these.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["How many clock cycles?", "one big cycle, or a pipeline",
             "Fmax, latency, area"],
            ["Where do the registers go?", "stage boundaries", "Fmax, and directly"],
            ["What is shared?", "one multiplier reused, or four in parallel",
             "area against throughput"],
            ["How is it partitioned?", "module boundaries, hierarchy",
             "readability, reuse, synthesis runtime"],
            ["What is the interface?", "handshake, valid/ready, fixed latency",
             "how easily it plugs into anything else"],
            ["Where does reset reach?", "everything, or only what needs it",
             "area, and routing congestion"]]
    table(ax, 3, H - 10.0, ["the decision", "the options", "what it costs you"],
          rows, [26, 38, 30], 5.2, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 15.5, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 15.0, "This is where the engineering is", fontsize=9.6, color=AMBER,
            ha="center", fontweight="bold")
    ax.text(50, 10.0, "A synthesiser is better than you are at choosing gates. It is "
                      "not better than you are at any of the\nrows above, and it will "
                      "not warn you that you chose badly - it will faithfully build "
                      "what you asked for.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.6, "Make these decisions on paper, before the first line of RTL.",
            fontsize=8.6, color=NAVY, ha="center", fontweight="bold")
    save(f, "partitioning")


def reuse():
    W, Hin = 11.5, 7.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 66.1
    title(ax, 50, H - 3, "Writing RTL that someone else can use", 12.5)
    ax.text(50, H - 7.2, "Module 2's terminal outcomes ask for reusable IP. "
                         "Reuse is a property you design in.",
            fontsize=8.8, color=SLATE, ha="center")

    items = [("Parameterise, do not duplicate",
              "WIDTH as a parameter, not four copies of the file", TEAL),
             ("One clock, stated in the name",
              "clk, and a comment saying which domain it belongs to", TEAL),
             ("Reset policy, written down",
              "synchronous or asynchronous, active high or low - pick one and "
              "keep it", NAVY),
             ("No magic numbers",
              "localparam with a name beats 8'd47 buried in a case", NAVY),
             ("An interface, not a pile of wires",
              "valid/ready is understood everywhere; your own scheme is not",
              VIOLET),
             ("A testbench that ships with it",
              "IP without a testbench is a liability, not an asset", GREEN)]
    y = H - 10.5
    rh = 5.6
    for hd, sub, col in items:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.3)
        ax.text(7, y - rh / 2, hd, ha="left", va="center", fontsize=8.8, color=col,
                fontweight="bold")
        ax.text(42, y - rh / 2, sub, ha="left", va="center", fontsize=8.1,
                color=BODY)
        y -= rh + 1.1

    box(ax, 3, 3.0, 94, 10.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 9.6, "The test for reusable IP", fontsize=9.2, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 5.4, "Could a colleague drop it into a different design, next year, "
                     "without asking you anything?\nIf the answer needs a "
                     "conversation, it is not reusable yet.",
            fontsize=8.5, color=BODY, ha="center")
    save(f, "reuse")


for fn in (design_flow, flow_executed, synth_subset, latch_inference,
           sim_synth_mismatch, lint_rules, coding_rules, partitioning, reuse):
    fn()
