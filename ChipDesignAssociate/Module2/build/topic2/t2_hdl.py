# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — introduction to hardware description languages."""
import _boot
from dsl import *


def what_is_hdl():
    W, Hin = 11.5, 7.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 64.3
    title(ax, 50, H - 3, "An HDL is not a programming language", 13)
    ax.text(50, H - 7.4, "It looks like one. That resemblance is the single biggest "
                         "source of beginner bugs.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 12.0
    box(ax, 4, y - 24.0, 44, 24.0, fc="#F4F8FB", ec=TEAL, lw=1.7)
    ax.text(26, y - 4.4, "A PROGRAM", fontsize=10, color=TEAL, ha="center",
            fontweight="bold")
    for i, ln in enumerate(["statements run one after another",
                            "a variable holds a value",
                            "a loop repeats over time",
                            "a function is called and returns",
                            "you describe a PROCEDURE"]):
        ax.text(7, y - 9.0 - i * 3.4, "•", fontsize=8.4, color=TEAL, ha="left")
        ax.text(10, y - 9.0 - i * 3.4, ln, fontsize=8.4, color=BODY, ha="left")

    box(ax, 52, y - 24.0, 44, 24.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(74, y - 4.4, "AN HDL DESCRIPTION", fontsize=10, color=GREEN,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["every block runs ALL THE TIME",
                            "a signal is a wire with a value on it",
                            "a loop is unrolled into hardware",
                            "a module is INSTANTIATED and exists",
                            "you describe a STRUCTURE"]):
        ax.text(55, y - 9.0 - i * 3.4, "•", fontsize=8.4, color=GREEN, ha="left")
        ax.text(58, y - 9.0 - i * 3.4, ln, fontsize=8.4, color=BODY, ha="left")

    box(ax, 4, 3.0, 92, 20.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 19.6, "The sentence to keep in your head", fontsize=9.6, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 14.0, "You are not writing instructions for a machine to follow. "
                      "You are writing a DESCRIPTION of a\nmachine, which a tool will "
                      "then build. The text is a blueprint, not a recipe.",
            fontsize=8.8, color=BODY, ha="center")
    ax.text(50, 6.8, "Which is why \"it compiles\" means almost nothing, and why a "
                     "construct can be perfectly legal\nVerilog and still have no "
                     "hardware meaning at all.",
            fontsize=8.6, color=RED, ha="center")
    save(f, "what_is_hdl")


def concurrency():
    W, Hin = 11.5, 8.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "Everything happens at once", 13)
    ax.text(50, H - 7.2, "The order you write the blocks in has no meaning whatsoever.",
            fontsize=9, color=SLATE, ha="center")

    y = H - 12.0
    ax.text(26, y, "as written", fontsize=9.2, color=SLATE, ha="center",
            fontweight="bold")
    ax.text(74, y, "as built", fontsize=9.2, color=SLATE, ha="center",
            fontweight="bold")

    code = ["assign p = a & b;", "assign q = p | c;", "assign r = q ^ d;"]
    for i, ln in enumerate(code):
        box(ax, 6, y - 6.0 - i * 6.5, 40, 5.2, fc="#F4F8FB", ec=TEAL, lw=1.2, r=0.4)
        ax.text(8, y - 3.4 - i * 6.5, ln, fontsize=8.6, color=NAVY, ha="left",
                va="center", family="monospace")

    for i, (nm, col) in enumerate([("AND", TEAL), ("OR", TEAL), ("XOR", TEAL)]):
        box(ax, 66, y - 6.0 - i * 6.5, 16, 5.2, fc=WHITE, ec=col, lw=1.4, r=0.4)
        ax.text(74, y - 3.4 - i * 6.5, nm, fontsize=8.6, color=col, ha="center",
                va="center", fontweight="bold")
    ax.text(88, y - 9.9, "all three\nexist at once,\nfor ever",
            fontsize=8.2, color=GREEN, ha="left", va="center", fontstyle="italic")

    box(ax, 4, 17.0, 92, 14.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 28.6, "Write those three lines in any order you like", fontsize=9.4,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 23.6, "The circuit is identical. Put the r line first and it still "
                      "works, because you did not write a\nsequence - you wrote three "
                      "facts about three pieces of hardware that all exist together.",
            fontsize=8.6, color=BODY, ha="center")

    box(ax, 4, 3.0, 92, 12.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 11.6, "The one place order DOES matter", fontsize=9.4, color=NAVY,
            ha="center", fontweight="bold")
    ax.text(50, 6.8, "Inside a single always block using blocking assignments (=), "
                     "statements run in order, like software.\nThat is exactly why "
                     "mixing = and <= in one block is confusing enough to be a lint "
                     "rule.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "concurrency")


def module_anatomy():
    W, Hin = 11.5, 8.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 74.8
    title(ax, 50, H - 3, "The parts of a Verilog module", 13)

    lines = [("module counter #(parameter WIDTH = 4) (", NAVY,
              "name, and parameters that let it be reused at other sizes"),
             ("    input                  clk,", TEAL, "ports: the interface"),
             ("    input                  rst,", TEAL, ""),
             ("    output reg [WIDTH-1:0] count", TEAL,
              "reg here means 'assigned in an always block', NOT a flip-flop"),
             (");", NAVY, ""),
             ("", NAVY, ""),
             ("    always @(posedge clk) begin", VIOLET,
              "a clocked block: this is where flip-flops come from"),
             ("        if (rst) count <= 0;", VIOLET, ""),
             ("        else     count <= count + 1;", VIOLET, ""),
             ("    end", VIOLET, ""),
             ("", NAVY, ""),
             ("endmodule", NAVY, "")]
    y = H - 9.0
    for txt, col, note in lines:
        if txt:
            ax.text(5, y, txt, fontsize=8.8, color=col, ha="left",
                    family="monospace")
        if note:
            ax.text(56, y, note, fontsize=7.8, color=SLATE, ha="left",
                    fontstyle="italic")
        y -= 3.5

    box(ax, 4, 3.0, 92, 19.0, fc="#FFF7EC", ec=AMBER, lw=1.7)
    ax.text(50, 18.6, "The word that confuses everyone: reg", fontsize=9.6,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 13.4, "reg does NOT mean register. It means \"this signal is assigned "
                      "inside a procedural block\".\nA reg assigned in an always @* "
                      "block becomes pure combinational logic.",
            fontsize=8.7, color=BODY, ha="center")
    ax.text(50, 6.8, "What actually creates a flip-flop is assigning inside "
                     "always @(posedge clk) - nothing else.\n"
                     "SystemVerilog renamed reg to logic precisely to end this "
                     "confusion.",
            fontsize=8.6, color=NAVY, ha="center")
    save(f, "module_anatomy")


def verilog_vhdl():
    W, Hin = 11.5, 9.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 81.7
    title(ax, 50, H - 3, "Verilog and VHDL: the same ideas, different notation", 12.5)

    rows = [["origin", "1984, Gateway Design Automation",
             "1983, US Department of Defense"],
            ["standard", "IEEE 1364, then 1800 (SystemVerilog)", "IEEE 1076"],
            ["feel", "terse, C-like", "verbose, Ada-like"],
            ["typing", "weak - it will let you do most things",
             "strong - explicit conversions required"],
            ["case sensitive", "yes", "no"],
            ["interface / body", "one module", "entity and architecture, separately"],
            ["a clocked block", "always @(posedge clk)",
             "process (clk) ... if rising_edge(clk)"],
            ["assignment", "<= and =", "<= and :="],
            ["used most in", "North America, ASIC flows", "Europe, defence, aerospace"]]
    table(ax, 3, H - 9.0, ["", "Verilog", "VHDL"],
          rows, [20, 38, 36], 5.0, size=8.4, bold_col=[0])

    box(ax, 3, 3.0, 94, 15.5, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 15.0, "None of those differences are about hardware", fontsize=9.6,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 10.0, "Both describe registers, combinational logic and hierarchy. "
                      "Both synthesise to the same gates.\nAn engineer who "
                      "understands RTL can read the other one after an afternoon; "
                      "an engineer who has\nonly memorised syntax can read neither.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 4.4, "The syllabus says \"Verilog or VHDL\". The word doing the work "
                     "is OR.",
            fontsize=8.6, color=TEAL, ha="center", fontweight="bold")
    save(f, "verilog_vhdl")


def two_languages_result():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 69.6
    title(ax, 50, H - 3, "The same designs, in both languages, actually run",
          13)

    y = H - 11.0
    box(ax, 4, y - 20.0, 44, 20.0, fc="#F4F8FB", ec=TEAL, lw=1.7)
    ax.text(26, y - 4.2, "Verilog · iverilog", fontsize=9.4, color=TEAL,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["always @(posedge clk)", "  if (rst) count <= 0;",
                            "  else if (en)",
                            "    count <= count + 1;", "assign tc = &count;"]):
        ax.text(7, y - 8.0 - i * 2.7, ln, fontsize=7.8, color=NAVY, ha="left",
                family="monospace")

    box(ax, 52, y - 20.0, 44, 20.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(74, y - 4.2, "VHDL · ghdl", fontsize=9.4, color=GREEN, ha="center",
            fontweight="bold")
    for i, ln in enumerate(["if rising_edge(clk) then", "  if rst = '1' then",
                            "    cnt <= (others => '0');",
                            "  elsif en = '1' then",
                            "    cnt <= cnt + 1;"]):
        ax.text(55, y - 8.0 - i * 2.7, ln, fontsize=7.8, color=NAVY, ha="left",
                family="monospace")

    rows = [["counter", "rtl/counter.v", "vhdl/counter.vhd", "18", "IDENTICAL"],
            ["'101' detector", "fsm/seq101_moore.v", "vhdl/seq101_moore.vhd", "17",
             "IDENTICAL"]]
    table(ax, 4, 36.0, ["design", "Verilog", "VHDL", "cycles", "diff"],
          rows, [18, 26, 28, 10, 10], 5.0, size=8.0, bold_col=[0],
          colcolors={4: GREEN})

    box(ax, 4, 3.0, 92, 16.0, fc=LIGHT, ec=NAVY, lw=1.7)
    ax.text(50, 15.6, "Two languages, two simulators, transcripts diffed",
            fontsize=9.6, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 11.0, "Not \"they look similar\". The logs were compared line by "
                      "line by diff, and there was nothing to report.",
            fontsize=8.6, color=BODY, ha="center")
    ax.text(50, 6.0, "The state machine is the interesting one: VHDL gives the states "
                     "a real enumerated TYPE, so an illegal\nstate will not compile. "
                     "Verilog gives them numbers.",
            fontsize=8.6, color=GREEN, ha="center", fontweight="bold")
    save(f, "two_languages_result")


def event_simulation():
    W, Hin = 11.5, 8.4
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 73.0
    title(ax, 50, H - 3, "How a simulator runs an HDL", 13)
    ax.text(50, H - 7.2, "Nothing runs continuously. The simulator jumps from event "
                         "to event.",
            fontsize=9, color=SLATE, ha="center")

    steps = [("1", "A signal changes", "at time t, some value is different", TEAL),
             ("2", "Wake everything sensitive to it",
              "every always block and assign that reads it", TEAL),
             ("3", "Evaluate them all", "in an order the standard does not fix",
              VIOLET),
             ("4", "Schedule the results", "non-blocking updates go into a queue",
              VIOLET),
             ("5", "Apply the queue", "all at once - this is what <= means", NAVY),
             ("6", "Repeat until nothing changes", "then advance time", NAVY)]
    y = H - 11.5
    rh = 6.4
    for n, hd, sub, col in steps:
        box(ax, 4, y - rh, 92, rh, fc=WHITE, ec=col, lw=1.3)
        ax.add_patch(Circle((9.5, y - rh / 2), 2.3, fc=col, ec=col, zorder=5))
        ax.text(9.5, y - rh / 2, n, ha="center", va="center", fontsize=8.8,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(15, y - rh / 2 + 1.2, hd, ha="left", va="center", fontsize=8.8,
                color=col, fontweight="bold")
        ax.text(15, y - rh / 2 - 1.8, sub, ha="left", va="center", fontsize=8.0,
                color=BODY)
        y -= rh + 1.1

    box(ax, 4, 3.0, 92, 14.0, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 13.6, "Step 3 is why RTL has coding rules at all", fontsize=9.4,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 8.6, "The order blocks are evaluated in is genuinely unspecified. "
                     "Two clocked blocks using blocking\nassignments can see each "
                     "other's half-finished work, and which one wins may differ "
                     "between\nsimulators, or between runs. Non-blocking assignment "
                     "exists to make that impossible.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "event_simulation")


def hdl_choose():
    W, Hin = 11.5, 8.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W                        # 71.3
    title(ax, 50, H - 3, "Which HDL should you learn?", 13)

    y = H - 10.0
    box(ax, 4, y - 16.0, 92, 16.0, fc="#EEF7F1", ec=GREEN, lw=1.7)
    ax.text(50, y - 5.0, "Learn the CONCEPTS. The notation follows in an afternoon.",
            fontsize=10.5, color=GREEN, ha="center", fontweight="bold")
    ax.text(50, y - 11.0, "registers and combinational logic  ·  the clock edge  ·  "
                          "reset  ·  hierarchy\nblocking against non-blocking  ·  the "
                          "synthesisable subset  ·  what a tool will build",
            fontsize=8.6, color=BODY, ha="center")

    rows = [["This course", "Verilog", "it is what Module 2 and the labs use"],
            ["Most ASIC work", "SystemVerilog", "Verilog plus better types and "
             "verification"],
            ["Much European and defence work", "VHDL", "strong typing, long "
             "project lifetimes"],
            ["Increasingly", "both", "large projects mix them in one flow"]]
    table(ax, 4, y - 19.0, ["if you are doing", "use", "because"],
          rows, [34, 20, 38], 5.0, size=8.4, bold_col=[1])

    box(ax, 4, 3.0, 92, 10.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 9.6, "The lab proves the point rather than asserting it", fontsize=9.2,
            color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 5.4, "The same counter, written in both, simulated by two different "
                     "simulators, produced identical\ntranscripts over 18 cycles.",
            fontsize=8.6, color=BODY, ha="center")
    save(f, "hdl_choose")


for fn in (what_is_hdl, concurrency, module_anatomy, verilog_vhdl,
           two_languages_result, event_simulation, hdl_choose):
    fn()
