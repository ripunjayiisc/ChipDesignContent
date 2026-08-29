# -*- coding: utf-8 -*-
"""Module 2 Topic 2 diagrams — the two languages, as reference cards."""
import _boot
from dsl import *


def _card(ax, x, ytop, w, heading, col, rows, size=7.6, gap=2.9, pad=3.4):
    """Draw a reference card whose height is COMPUTED from its row count.

    Sizing cards by hand is how diagrams end up with text hanging out of the
    bottom, so the height is derived instead: header, padding, one gap per
    row after the first, and a bottom margin.
    """
    h = 5.0 + pad + (len(rows) - 1) * gap + 2.6
    y = ytop - h
    box(ax, x, y, w, h, fc=WHITE, ec=col, lw=1.7)
    box(ax, x, y + h - 5.0, w, 5.0, fc=col, ec=col)
    ax.text(x + w / 2, y + h - 2.5, heading, ha="center", va="center",
            fontsize=9.0, color=WHITE, fontweight="bold")
    yy = y + h - 5.0 - pad
    for a, b in rows:
        ax.text(x + 2.0, yy, a, ha="left", va="center", fontsize=size,
                color=INK, family="monospace")
        if b:
            ax.text(x + w - 2.0, yy, b, ha="right", va="center", fontsize=7.2,
                    color=SLATE)
        yy -= gap
    return y


def verilog_card():
    W, Hin = 11.5, 11.0
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Verilog: everything you need for this topic on one "
                         "page", 12.5)
    ax.text(50, H - 7.0, "Not the whole language - the part that synthesises, "
                         "which is much smaller.",
            fontsize=9, color=SLATE, ha="center")

    y1 = _card(ax, 3, H - 11.0, 45, "THE MODULE", NAVY, [
        ("module counter4 (", ""),
        ("    input            clk,", "a 1-bit input"),
        ("    input            rst_n,", ""),
        ("    output reg [3:0] count,", "a 4-bit output you assign"),
        ("    output           tc", "in a procedural block"),
        (");", ""),
        ("    ...", ""),
        ("endmodule", "no semicolon after endmodule"),
    ], gap=3.0)

    _card(ax, 52, H - 11.0, 45, "NETS AND VARIABLES", TEAL, [
        ("wire  y;", "driven by assign or a port"),
        ("reg   q;", "assigned in always/initial"),
        ("reg [7:0] bus;", "a vector, MSB first"),
        ("reg [7:0] mem [0:255];", "an array of vectors"),
        ("localparam W = 8;", "a constant, module-scope"),
        ("parameter  N = 4;", "a constant the caller can set"),
        ("", ""),
        ("`reg` does NOT mean register.", "it means 'assigned procedurally'"),
    ], gap=3.0)

    y2 = _card(ax, 3, y1 - 3.0, 45, "THE THREE BLOCKS", VIOLET, [
        ("assign y = a & b;", "continuous - combinational"),
        ("", ""),
        ("always @(*) begin", "combinational"),
        ("    y = a & b;", "blocking  ="),
        ("end", ""),
        ("", ""),
        ("always @(posedge clk) begin", "sequential"),
        ("    q <= d;", "non-blocking  <="),
        ("end", ""),
    ], gap=2.9)

    _card(ax, 52, y1 - 3.0, 45, "OPERATORS WORTH KNOWING", GREEN, [
        ("& | ^ ~", "bitwise"),
        ("&& || !", "logical - result is 1 bit"),
        ("== !=", "equality  (x/z make it x)"),
        ("=== !==", "identity - matches x and z too"),
        ("{a, b}", "concatenation"),
        ("{4{a}}", "replication - four copies of a"),
        ("a[3:1]", "part select"),
        ("cond ? x : y", "a multiplexer, written short"),
        ("", ""),
    ], gap=2.9)

    box(ax, 3, 3.0, 94, 8.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 7.6, "The synthesisable subset is roughly this page",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 4.4, "make subset measures where the boundary actually is: "
                     "eleven constructs, three of which are refused or "
                     "silently ignored.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "verilog_card")


def vhdl_card():
    W, Hin = 11.5, 11.8
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "VHDL: the same ideas, spelled differently", 12.5)
    ax.text(50, H - 7.0, "Everything on this page has an exact counterpart on "
                         "the Verilog page.",
            fontsize=9, color=SLATE, ha="center")

    y1 = _card(ax, 3, H - 11.0, 45, "LIBRARIES AND ENTITY", NAVY, [
        ("library ieee;", "Verilog has none to declare"),
        ("use ieee.std_logic_1164.all;", "std_logic, and'/'or'"),
        ("use ieee.numeric_std.all;", "unsigned, signed, arithmetic"),
        ("", ""),
        ("entity counter is", "the INTERFACE only"),
        ("  generic (WIDTH : positive := 4);", "= parameter"),
        ("  port (", ""),
        ("    clk : in  std_logic;", ""),
        ("    cnt : out std_logic_vector(3 downto 0)", ""),
        ("  );", ""),
        ("end entity counter;", ""),
    ], gap=2.9)

    _card(ax, 52, H - 11.0, 45, "ARCHITECTURE", TEAL, [
        ("architecture rtl of counter is", "the IMPLEMENTATION"),
        ("  signal c : unsigned(3 downto 0);", "declared BEFORE begin"),
        ("begin", ""),
        ("  process (clk)", "= always @(posedge clk)"),
        ("  begin", ""),
        ("    if rising_edge(clk) then", ""),
        ("      c <= c + 1;", "<= is the signal assignment"),
        ("    end if;", ""),
        ("  end process;", ""),
        ("  cnt <= std_logic_vector(c);", "explicit type conversion"),
        ("end architecture rtl;", ""),
    ], gap=2.9)

    _card(ax, 3, y1 - 3.0, 45, "TYPES - THE REAL DIFFERENCE", VIOLET, [
        ("std_logic", "one bit: 0 1 X Z U W L H -"),
        ("std_logic_vector", "a bundle of bits, no arithmetic"),
        ("unsigned / signed", "the SAME bits, with arithmetic"),
        ("integer", "for constants and loop counters"),
        ("type state_t is (S_IDLE, S_1);", "a real enumerated type"),
        ("", ""),
        ("You must convert explicitly.", "and the compiler will make you"),
        ("Verilog would just let you add.", ""),
    ], gap=3.0)

    _card(ax, 52, y1 - 3.0, 45, "WHAT VHDL CATCHES THAT VERILOG DOES NOT",
          GREEN, [
        ("a non-exhaustive case", "will not analyse"),
        ("an illegal state value", "not a member of the type"),
        ("a width mismatch", "8 bits into 4 is an error"),
        ("mixing signed and unsigned", "an error, not a surprise"),
        ("", ""),
        ("The cost is keystrokes.", ""),
        ("The benefit is that the bug", ""),
        ("is found in the analyser,", ""),
        ("not in the lab.", ""),
    ], gap=2.9)

    box(ax, 3, 3.0, 94, 8.0, fc="#EEF7F1", ec=GREEN, lw=1.6)
    ax.text(50, 7.6, "make langs   —   both languages, two simulators, "
                     "transcripts diffed line by line",
            fontsize=8.8, color=GREEN, ha="center", fontweight="bold",
            family="monospace")
    ax.text(50, 4.4, "The counter agrees over 18 cycles; the '101' detector "
                     "agrees over 17. Same designs, different notation.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "vhdl_card")


def lang_mapping():
    W, Hin = 11.5, 10.6
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "Verilog to VHDL, line for line", 12.5)
    ax.text(50, H - 7.0, "Learn one and you can read the other in an "
                         "afternoon. This table is the afternoon.",
            fontsize=9, color=SLATE, ha="center")

    rows = [["module ... endmodule", "entity + architecture",
             "VHDL splits interface from implementation"],
            ["input / output", "port (... : in / out ...)", ""],
            ["parameter", "generic", ""],
            ["localparam", "constant", ""],
            ["wire", "signal", "VHDL has one kind, not two"],
            ["reg", "signal (or variable)", "'reg' never meant register"],
            ["[7:0]", "(7 downto 0)", "or (0 to 7) if you insist"],
            ["always @(posedge clk)", "process (clk) + rising_edge(clk)", ""],
            ["always @(*)", "process (all inputs)", "or process(all) in VHDL-2008"],
            ["<=  in a clocked block", "<=  signal assignment", "same symbol, same idea"],
            ["=   in a comb block", ":=  variable assignment", "different symbol"],
            ["case ... default", "case ... when others", "'when others' is compulsory"],
            ["localparam S = 2'd0", "type state_t is (S, ...)", "a number against a type"],
            ["generate for", "for ... generate", ""],
            ["$display", "report / write", ""],
            ["`timescale", "units are written on the value", "5 ns, not a directive"]]
    table(ax, 3, H - 10.5, ["Verilog", "VHDL", "the difference that matters"],
          rows, [26, 32, 36], 3.9, size=7.8, bold_col=[0])

    box(ax, 3, 3.0, 94, 12.0, fc=LIGHT, ec=NAVY, lw=1.6)
    ax.text(50, 11.4, "The syllabus says \"HDLs such as Verilog or VHDL\". "
                      "The word doing the work is OR.",
            fontsize=9.2, color=NAVY, ha="center", fontweight="bold")
    ax.text(50, 6.6, "Nothing in this topic depends on which one you use. The "
                     "abstraction levels, the synthesisable subset, the latch\n"
                     "rules, the three-block FSM pattern and the whole flow "
                     "are identical. Only the spelling changes.",
            fontsize=8.4, color=BODY, ha="center")
    save(f, "lang_mapping")


def testbench_anatomy():
    W, Hin = 11.5, 10.2
    f, ax = fig(W, Hin)
    H = 100 * Hin / W
    title(ax, 50, H - 3, "What a testbench is made of", 12.5)
    ax.text(50, H - 7.0, "Topic 5 goes into verification properly. This is the "
                         "minimum you need to finish Topic 2.",
            fontsize=9, color=SLATE, ha="center")

    parts = [("1  CLOCK", NAVY, "always #5 clk = ~clk;",
              "a free-running clock - nothing else generates it"),
             ("2  RESET", VIOLET, "rst_n = 0;  @(negedge clk);  rst_n = 1;",
              "released away from the sampling edge, on purpose"),
             ("3  STIMULUS", TEAL, "din = stream[i];",
              "drive on the inactive edge, sample before the active one"),
             ("4  GOLDEN MODEL", AMBER,
              "exp[i] = (s[i-2] & ~s[i-1] & s[i]);",
              "computed from the STIMULUS, never from the DUT"),
             ("5  CHECKER", RED, "if (det !== exp[i]) errors = errors + 1;",
              "the line that makes it self-checking"),
             ("6  VERDICT", GREEN,
              "if (errors==0) $display(\"PASS\"); else ...",
              "one line a human can read without a waveform")]
    y = H - 11.0
    rh = 8.6
    for nm, col, code, note in parts:
        box(ax, 3, y - rh, 94, rh, fc=WHITE, ec=col, lw=1.4)
        box(ax, 3, y - rh, 20, rh, fc=col, ec=col)
        ax.text(13, y - rh / 2, nm, ha="center", va="center", fontsize=8.6,
                color=WHITE, fontweight="bold")
        ax.text(25, y - rh / 2 + 1.8, code, ha="left", va="center",
                fontsize=7.6, color=INK, family="monospace")
        ax.text(25, y - rh / 2 - 2.2, note, ha="left", va="center",
                fontsize=7.6, color=SLATE, fontstyle="italic")
        y -= rh + 1.2

    box(ax, 3, 3.0, 94, 13.5, fc="#FDECEF", ec=RED, lw=1.7)
    ax.text(50, 12.9, "A testbench without step 4 is not a test", fontsize=9.4,
            color=RED, ha="center", fontweight="bold")
    ax.text(50, 8.2, "If the expected answer comes from the design, the test "
                     "passes whatever the design does. Every checker in this "
                     "lab\ncomputes its expectation from the stimulus - which "
                     "is why 'blocking version: 6 wrong cycles' could be "
                     "printed at all.",
            fontsize=8.4, color=BODY, ha="center")
    ax.text(50, 4.2, "Eyeballing a waveform is not step 5 either. It does not "
                     "scale past about ten cycles, and it never runs twice.",
            fontsize=8.4, color=NAVY, ha="center", fontweight="bold")
    save(f, "testbench_anatomy")


for fn in (verilog_card, vhdl_card, lang_mapping, testbench_anatomy):
    fn()
