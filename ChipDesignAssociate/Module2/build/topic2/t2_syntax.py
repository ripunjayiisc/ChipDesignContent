# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — the two languages, as reference cards.

Reference pages use the taller PHT panel: they carry more rows than a normal
slide diagram, and they are meant to be read rather than glanced at. Even so
the type is set large enough to survive being scaled onto a slide.
"""
import _boot
from dsl import *


def _card(ax, x, ytop, w, heading, col, rows, size=10.6, gap=3.5, pad=4.0):
    """A reference card whose height is COMPUTED from its row count."""
    h = 6.0 + pad + (len(rows) - 1) * gap + 3.0
    y = ytop - h
    box(ax, x, y, w, h, fc=WHITE, ec=col, lw=2.0)
    box(ax, x, y + h - 6.0, w, 6.0, fc=col, ec=col)
    ax.text(x + w / 2, y + h - 3.0, heading, ha="center", va="center",
            fontsize=FS_HEAD, color=WHITE, fontweight="bold")
    yy = y + h - 6.0 - pad
    for a, b in rows:
        ax.text(x + 2.2, yy, a, ha="left", va="center", fontsize=size,
                color=INK, family="monospace")
        if b:
            ax.text(x + w - 2.2, yy, b, ha="right", va="center", fontsize=9.8,
                    color=SLATE)
        yy -= gap
    return y


def verilog_card():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "Verilog: the part that synthesises", FS_TITLE)
    ax.text(50, H - 10.0, "Not the whole language - the part you need for this "
                          "topic, which is much smaller.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    _card(ax, 3, H - 14.5, 46, "THE MODULE", NAVY, [
        ("module counter4 (", ""),
        ("    input            clk,", "a 1-bit input"),
        ("    input            rst_n,", ""),
        ("    output reg [3:0] count,", "assigned in a block"),
        ("    output           tc", ""),
        (");   ...   endmodule", "no semicolon after it"),
    ])

    _card(ax, 51, H - 14.5, 46, "NETS AND VARIABLES", TEAL, [
        ("wire  y;", "driven by assign"),
        ("reg   q;", "assigned in always"),
        ("reg [7:0] bus;", "a vector, MSB first"),
        ("reg [7:0] mem [0:255];", "an array of vectors"),
        ("localparam W = 8;", "constant, module scope"),
        ("parameter  N = 4;", "the caller can set it"),
    ])

    ax.text(50, 4.0, "reg does NOT mean register. It means 'assigned in a "
                     "procedural block'.",
            fontsize=FS_BODY, color=AMBER, ha="center", fontweight="bold")
    save(f, "verilog_card")


def verilog_card2():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "Verilog: the three kinds of block, and the "
                           "operators", FS_TITLE)

    _card(ax, 3, H - 9.0, 46, "THE THREE BLOCKS", VIOLET, [
        ("assign y = a & b;", "continuous"),
        ("", ""),
        ("always @(*) begin", "combinational"),
        ("    y = a & b;", "blocking  ="),
        ("end", ""),
        ("", ""),
        ("always @(posedge clk) begin", "sequential"),
        ("    q <= d;", "non-blocking  <="),
        ("end", ""),
    ])

    _card(ax, 51, H - 9.0, 46, "OPERATORS WORTH KNOWING", GREEN, [
        ("& | ^ ~", "bitwise"),
        ("&& || !", "logical - one bit out"),
        ("== !=", "equality (x/z give x)"),
        ("=== !==", "identity - matches x, z"),
        ("{a, b}", "concatenation"),
        ("{4{a}}", "replication"),
        ("a[3:1]", "part select"),
        ("cond ? x : y", "a multiplexer"),
        ("", ""),
    ])

    ax.text(50, 3.5, "make subset  measures where the synthesisable boundary "
                     "actually is.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "verilog_card2")


def vhdl_card():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "VHDL: the same ideas, spelled differently", FS_TITLE)
    ax.text(50, H - 10.0, "Everything here has an exact counterpart on the "
                          "Verilog page.",
            fontsize=FS_SUB, color=SLATE, ha="center")

    _card(ax, 3, H - 14.5, 46, "LIBRARIES AND ENTITY", NAVY, [
        ("library ieee;", "Verilog has none"),
        ("use ieee.std_logic_1164.all;", "std_logic"),
        ("use ieee.numeric_std.all;", "unsigned, arithmetic"),
        ("", ""),
        ("entity counter is", "the INTERFACE only"),
        ("  generic (WIDTH : positive);", "= parameter"),
        ("  port (clk : in std_logic);", ""),
        ("end entity counter;", ""),
    ], size=10.0)

    _card(ax, 51, H - 14.5, 46, "ARCHITECTURE", TEAL, [
        ("architecture rtl of counter is", ""),
        ("  signal c : unsigned(3 downto 0);", ""),
        ("begin", "the IMPLEMENTATION"),
        ("  process (clk)", "= always @(posedge)"),
        ("  begin", ""),
        ("    if rising_edge(clk) then", ""),
        ("      c <= c + 1;", "<= assigns a signal"),
        ("    end if;  end process;", ""),
    ], size=10.0)

    ax.text(50, 3.5, "VHDL splits the interface from the implementation. "
                     "Verilog puts both in one module.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "vhdl_card")


def vhdl_card2():
    f, ax, H = panel(PHT)
    title(ax, 50, H - 4.5, "VHDL: types, and what they catch", FS_TITLE)

    _card(ax, 3, H - 9.0, 46, "TYPES - THE REAL DIFFERENCE", VIOLET, [
        ("std_logic", "0 1 X Z U W L H"),
        ("std_logic_vector", "bits, no arithmetic"),
        ("unsigned / signed", "bits, with arithmetic"),
        ("integer", "constants and loops"),
        ("type state_t is", "a real enumerated"),
        ("     (S_IDLE, S_1);", "type"),
        ("", ""),
        ("Conversions are explicit,", "and the compiler"),
        ("every time.", "will make you."),
    ], size=10.0)

    _card(ax, 51, H - 9.0, 46, "WHAT VHDL CATCHES", GREEN, [
        ("a non-exhaustive case", "will not analyse"),
        ("an illegal state value", "not in the type"),
        ("a width mismatch", "8 into 4 is an error"),
        ("signed mixed with unsigned", ""),
        ("", ""),
        ("The cost is keystrokes.", ""),
        ("The benefit is that the bug", ""),
        ("is found in the analyser,", ""),
        ("not in the lab.", ""),
    ], size=10.0)

    ax.text(50, 3.5, "make langs   —   both languages, two simulators, "
                     "transcripts diffed",
            fontsize=FS_BODY, color=GREEN, ha="center", fontweight="bold",
            family="monospace")
    save(f, "vhdl_card2")


def lang_mapping():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Verilog to VHDL, line for line  (1 of 2)", FS_TITLE)

    rows = [["module ... endmodule", "entity + architecture",
             "VHDL splits interface from body"],
            ["input / output", "port (... : in / out ...)", ""],
            ["parameter", "generic", ""],
            ["localparam", "constant", ""],
            ["wire", "signal", "VHDL has one kind, not two"],
            ["reg", "signal (or variable)", "'reg' never meant register"],
            ["[7:0]", "(7 downto 0)", "or (0 to 7) if you insist"],
            ["generate for", "for ... generate", ""]]
    table(ax, 3, H - 9.5, ["Verilog", "VHDL", "the difference that matters"],
          rows, [26, 30, 38], 4.0, size=FS_TABLE, bold_col=[0])
    save(f, "lang_mapping")


def lang_mapping2():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "Verilog to VHDL, line for line  (2 of 2)", FS_TITLE)

    rows = [["always @(posedge clk)", "process (clk) + rising_edge(clk)", ""],
            ["always @(*)", "process (all inputs)", "process(all) in VHDL-2008"],
            ["<=  in a clocked block", "<=  signal assignment", "same idea"],
            ["=   in a comb block", ":=  variable assignment", "different symbol"],
            ["case ... default", "case ... when others", "'when others' is compulsory"],
            ["localparam S = 2'd0", "type state_t is (S, ...)", "a number against a type"],
            ["$display", "report / write", ""]]
    table(ax, 3, H - 9.5, ["Verilog", "VHDL", "the difference that matters"],
          rows, [26, 30, 38], 4.0, size=FS_TABLE, bold_col=[0])

    ax.text(50, 3.0, "The syllabus says \"HDLs such as Verilog or VHDL\". The "
                     "word doing the work is OR.",
            fontsize=FS_BODY, color=NAVY, ha="center", fontweight="bold")
    save(f, "lang_mapping2")


def testbench_anatomy():
    f, ax, H = panel()
    title(ax, 50, H - 4.5, "What a testbench is made of", FS_TITLE)

    parts = [("1  CLOCK", NAVY, "always #5 clk = ~clk;"),
             ("2  RESET", VIOLET, "rst_n = 0;  @(negedge clk);  rst_n = 1;"),
             ("3  STIMULUS", TEAL, "din = stream[i];"),
             ("4  GOLDEN MODEL", AMBER, "exp[i] = s[i-2] & ~s[i-1] & s[i];"),
             ("5  CHECKER", RED, "if (det !== exp[i]) errors = errors + 1;"),
             ("6  VERDICT", GREEN, "if (errors==0) $display(\"PASS\");")]
    y = H - 9.0
    rh = 5.0
    for nm, col, code in parts:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.5)
        box(ax, 3, y - rh, 26, rh, fc=col, ec=col)
        ax.text(16, y - rh / 2, nm, ha="center", va="center", fontsize=FS_BODY,
                color=WHITE, fontweight="bold")
        ax.text(31, y - rh / 2, code, ha="left", va="center", fontsize=FS_MONO,
                color=INK, family="monospace")
        y -= rh + 0.9

    ax.text(50, 2.2, "Step 4 is the one people leave out - and a testbench "
                     "without it is not a test.",
            fontsize=FS_BODY, color=RED, ha="center", fontweight="bold")
    save(f, "testbench_anatomy")


for fn in (verilog_card, verilog_card2, vhdl_card, vhdl_card2, lang_mapping,
           lang_mapping2, testbench_anatomy):
    fn()
