# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — introduction to hardware description languages."""
import _boot
from dsl import *


def what_is_hdl():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "An HDL is not a programming language", FS_TITLE)
    ax.text(50, H - 10.0, "It looks like one. That resemblance is the single "
                          "biggest source of beginner bugs.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    y = H - 14.0
    bh = 25.0
    box(ax, 3, y - bh, 46, bh, fc="#F4F8FB", ec=TEAL, lw=2.0)
    ax.text(26, y - 4.6, "A PROGRAM", fontsize=FS_HEAD + 1, color=TEAL,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["statements run one after another",
                            "a variable holds a value",
                            "a loop repeats over time",
                            "you describe a PROCEDURE"]):
        ax.text(6, y - 10.0 - i * 4.4, "•", fontsize=FS_BODY, color=TEAL,
                ha="left")
        ax.text(9.5, y - 10.0 - i * 4.4, ln, fontsize=FS_SMALL, color=BODY,
                ha="left")

    box(ax, 51, y - bh, 46, bh, fc="#EEF7F1", ec=GREEN, lw=2.0)
    ax.text(74, y - 4.6, "AN HDL DESCRIPTION", fontsize=FS_HEAD + 1, color=GREEN,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["every block runs ALL THE TIME",
                            "a signal is a wire with a value on it",
                            "a loop is unrolled into hardware",
                            "you describe a STRUCTURE"]):
        ax.text(54, y - 10.0 - i * 4.4, "•", fontsize=FS_BODY, color=GREEN,
                ha="left")
        ax.text(57.5, y - 10.0 - i * 4.4, ln, fontsize=FS_SMALL, color=BODY,
                ha="left")

    ax.text(50, 4.0, "The text is a blueprint, not a recipe - which is why "
                     "\"it compiles\" means almost nothing.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "what_is_hdl")


def concurrency():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Everything happens at once", FS_TITLE)
    ax.text(50, H - 10.0, "The order you write the blocks in has no meaning "
                          "whatsoever.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    y = H - 15.0
    ax.text(24, y, "as written", fontsize=FS_BODY, color=SLATE, ha="center",
            fontweight="bold")
    ax.text(70, y, "as built", fontsize=FS_BODY, color=SLATE, ha="center",
            fontweight="bold")

    code = ["assign p = a & b;", "assign q = p | c;", "assign r = q ^ d;"]
    for i, ln in enumerate(code):
        box(ax, 4, y - 6.5 - i * 7.0, 40, 5.6, fc="#F4F8FB", ec=TEAL, lw=1.4,
            r=0.4)
        ax.text(6.5, y - 3.7 - i * 7.0, ln, fontsize=FS_MONO, color=NAVY,
                ha="left", va="center", family="monospace")

    for i, nm in enumerate(["AND", "OR", "XOR"]):
        box(ax, 62, y - 6.5 - i * 7.0, 16, 5.6, fc=WHITE, ec=TEAL, lw=1.6,
            r=0.4)
        ax.text(70, y - 3.7 - i * 7.0, nm, fontsize=FS_BODY, color=TEAL,
                ha="center", va="center", fontweight="bold")
    ax.text(82, y - 10.7, "all three exist\nat once, for ever", fontsize=FS_SMALL,
            color=GREEN, ha="left", va="center", fontstyle="italic")

    ax.text(50, 4.0, "You did not write a sequence. You wrote three facts about "
                     "three pieces of hardware.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "concurrency")


def module_anatomy():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The parts of a Verilog module", FS_TITLE)

    lines = [("module counter #(parameter WIDTH = 4) (", NAVY,
              "name, and a parameter for reuse"),
             ("    input                  clk,", TEAL, "ports: the interface"),
             ("    input                  rst,", TEAL, ""),
             ("    output reg [WIDTH-1:0] count", TEAL,
              "reg = assigned in a block"),
             (");", NAVY, ""),
             ("    always @(posedge clk) begin", VIOLET,
              "clocked: flip-flops come from here"),
             ("        if (rst) count <= 0;", VIOLET, ""),
             ("        else     count <= count + 1;", VIOLET, ""),
             ("    end", VIOLET, ""),
             ("endmodule", NAVY, "")]
    y = H - 10.0
    for txt, col, note in lines:
        ax.text(4, y, txt, fontsize=FS_MONO, color=col, ha="left",
                family="monospace")
        if note:
            ax.text(62, y, note, fontsize=FS_SMALL, color=SLATE, ha="left",
                    fontstyle="italic")
        y -= 3.4

    ax.text(50, 6.5, "reg does NOT mean register.", fontsize=FS_HEAD,
            color=AMBER, ha="center", fontweight="bold")
    ax.text(50, 2.5, "What creates a flip-flop is assigning inside "
                     "always @(posedge clk) - nothing else.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "module_anatomy")


def verilog_vhdl():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "Verilog and VHDL: the same ideas, different notation",
          FS_TITLE)

    rows = [["origin", "1984, Gateway Design Automation",
             "1983, US Dept of Defense"],
            ["standard", "IEEE 1364, then 1800", "IEEE 1076"],
            ["feel", "terse, C-like", "verbose, Ada-like"],
            ["typing", "weak - it lets you do most things",
             "strong - conversions are explicit"],
            ["case sensitive", "yes", "no"],
            ["interface / body", "one module", "entity and architecture"],
            ["a clocked block", "always @(posedge clk)",
             "process (clk) + rising_edge"],
            ["assignment", "<= and =", "<= and :="],
            ["used most in", "North America, ASIC flows",
             "Europe, defence, aerospace"]]
    table(ax, 3, H - 10.0, ["", "Verilog", "VHDL"], rows, [20, 38, 36], 3.8,
          size=FS_TABLE, bold_col=[0])

    ax.text(50, 6.0, "None of those differences are about hardware.",
            fontsize=FS_HEAD, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 2.0, "Both describe registers, logic and hierarchy, and both "
                     "synthesise to the same gates.",
            fontsize=FS_BODY, color=BODY, ha="center")
    save(f, "verilog_vhdl")


def two_languages_result():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "The same designs, in both languages, actually run",
          FS_TITLE)

    y = H - 10.0
    bh = 19.0
    box(ax, 3, y - bh, 46, bh, fc="#F4F8FB", ec=TEAL, lw=2.0)
    ax.text(26, y - 4.4, "Verilog · iverilog", fontsize=FS_HEAD, color=TEAL,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["always @(posedge clk)", "  if (rst) count <= 0;",
                            "  else if (en)",
                            "    count <= count + 1;"]):
        ax.text(6, y - 9.0 - i * 3.4, ln, fontsize=FS_MONO, color=NAVY,
                ha="left", family="monospace")

    box(ax, 51, y - bh, 46, bh, fc="#EEF7F1", ec=GREEN, lw=2.0)
    ax.text(74, y - 4.4, "VHDL · ghdl", fontsize=FS_HEAD, color=GREEN,
            ha="center", fontweight="bold")
    for i, ln in enumerate(["if rising_edge(clk) then", "  if rst = '1' then",
                            "    cnt <= (others => '0');",
                            "  elsif en = '1' then"]):
        ax.text(54, y - 9.0 - i * 3.4, ln, fontsize=FS_MONO, color=NAVY,
                ha="left", family="monospace")

    rows = [["counter", "18 cycles", "IDENTICAL"],
            ["'101' detector", "17 cycles", "IDENTICAL"]]
    table(ax, 25, y - bh - 1.5, ["design", "compared over", "diff"], rows,
          [20, 18, 16], 4.4, size=FS_TABLE, bold_col=[0], colcolors={2: GREEN})

    ax.text(50, 2.0, "Not \"they look similar\" - the logs were compared line "
                     "by line by diff.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "two_languages_result")


def event_simulation():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "How a simulator runs an HDL", FS_TITLE)

    steps = [("1", "A signal changes", "at time t, some value is different", TEAL),
             ("2", "Wake everything sensitive to it",
              "every always block and assign that reads it", TEAL),
             ("3", "Evaluate them all", "in an order the standard does not fix",
              VIOLET),
             ("4", "Schedule the results", "non-blocking updates go into a queue",
              VIOLET),
             ("5", "Apply the queue", "all at once - this is what <= means", NAVY),
             ("6", "Repeat until nothing changes", "then advance time", NAVY)]
    y = H - 9.5
    rh = 5.0
    for n, hd, sub, col in steps:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        ax.add_patch(Circle((8.0, y - rh / 2), 2.1, fc=col, ec=col, zorder=5))
        ax.text(8.0, y - rh / 2, n, ha="center", va="center", fontsize=FS_SMALL,
                color=WHITE, fontweight="bold", zorder=6)
        ax.text(13, y - rh / 2, hd, ha="left", va="center", fontsize=FS_BODY,
                color=col, fontweight="bold")
        ax.text(50, y - rh / 2, sub, ha="left", va="center", fontsize=FS_SMALL,
                color=BODY)
        y -= rh + 0.9

    ax.text(50, 1.8, "Step 3 is why RTL has coding rules at all: the evaluation "
                     "order is genuinely unspecified.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "event_simulation")


def hdl_choose():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Which HDL should you learn?", FS_TITLE)

    y = H - 9.5
    box(ax, 3, y - 12.0, 94, 12.0, fc="#EEF7F1", ec=GREEN, lw=2.0)
    ax.text(50, y - 4.4, "Learn the CONCEPTS. The notation follows in an "
                         "afternoon.",
            fontsize=FS_HEAD + 1, color=GREEN, ha="center", fontweight="bold")
    ax.text(50, y - 9.0, "registers and combinational logic  ·  the clock edge  "
                         "·  reset  ·  hierarchy  ·  the synthesisable subset",
            fontsize=FS_SMALL, color=BODY, ha="center")

    rows = [["This course", "Verilog", "what Module 2 and the labs use"],
            ["Most ASIC work", "SystemVerilog", "Verilog plus better types"],
            ["European and defence work", "VHDL", "strong typing, long lifetimes"],
            ["Increasingly", "both", "large projects mix them in one flow"]]
    table(ax, 3, y - 14.5, ["if you are doing", "use", "because"], rows,
          [30, 22, 42], 4.2, size=FS_TABLE, bold_col=[1])

    ax.text(50, 2.0, "The lab proves it rather than asserting it: two languages, "
                     "two simulators, identical transcripts.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "hdl_choose")


for fn in (what_is_hdl, concurrency, module_anatomy, verilog_vhdl,
           two_languages_result, event_simulation, hdl_choose):
    fn()
