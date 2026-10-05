# -*- coding: utf-8 -*-
"""Lecture 01 workbook — Part 3: the design flow, step by step."""
import _boot
from wbkit import *


def build(w):
    w.h1("Part 3 · The Design Flow, Step by Step")

    w.h2("3.1  What a design flow is")

    w.para("A VLSI design flow is a standardized set of design procedures: a "
           "step-by-step route from a specification down to the hardware you "
           "actually build. Each step has a defined input, a defined output "
           "and a defined way of being checked.")
    w.image("design_flow_steps", width=6.6)

    w.callout("Why it had to be standardized", [
        "Dozens of engineers, several companies and a fabrication plant all "
        "work on one chip. A standard flow means the work can be divided up, "
        "and that a mistake is caught at the step that made it rather than "
        "three steps later.",
    ], color=NAVY)

    w.h2("3.2  What a CAD tool actually does")

    w.para([("This is the central idea of the whole lecture, and it is worth "
             "memorising in the lecturer's own words: ", {}),
            ("a CAD tool transforms its HDL input into an HDL output that "
             "contains more detailed information about the hardware.",
             {"b": True, "c": TEAL})])
    w.image("cad_transform", width=6.6)

    w.para("Read that carefully. Both the input and the output are hardware "
           "descriptions. Nothing is ever \"compiled into a program\". The "
           "design simply gets described in progressively more concrete terms, "
           "until the last description is a set of shapes a factory can print.")

    w.table(["This transformation", "Turns this", "Into this"],
            [["Synthesis", "behaviour", "register transfer level"],
             ["Technology mapping", "register transfer level", "gates"],
             ["Cell design", "gates", "transistors"],
             ["Layout", "transistors", "polygons on fabrication layers"]],
            widths=[1.9, 2.4, 2.5], size=10)

    w.callout("You will check this yourself", [
        "Lab 2 runs exactly these transformations on a ten-line counter, "
        "prints all three descriptions side by side, and then runs the same "
        "test bench against the first and the last to show they behave "
        "identically.",
    ], color=VIOLET, bar="7A4FBF")

    w.h2("3.3  The two competing HDLs")

    w.para("Two hardware description languages are in common use: Verilog and "
           "VHDL. Both can describe the same hardware, and a synthesis tool "
           "will produce the same gates from either. The choice between them "
           "is a matter of house style, existing code and local convention — "
           "not of what the silicon can do.")
    w.image("hdl_family", width=6.6)

    w.para("There are others. SystemVerilog is a large superset of Verilog "
           "aimed mostly at verification; SystemC is a C++ class library used "
           "for modelling whole systems before the hardware is written. This "
           "course uses Verilog.")

    w.h3("The same counter in both languages")
    w.code([
        "// Verilog",
        "module counter4 (",
        "    input  wire       clk,",
        "    input  wire       rst,",
        "    output reg  [3:0] q",
        ");",
        "    always @(posedge clk) begin",
        "        if (rst) q <= 4'd0;",
        "        else     q <= q + 4'd1;",
        "    end",
        "endmodule",
    ], caption="rtl/counter4.v")
    w.code([
        "-- VHDL",
        "library ieee;",
        "use ieee.std_logic_1164.all;",
        "use ieee.numeric_std.all;",
        "",
        "entity counter4 is",
        "    port (clk : in  std_logic;",
        "          rst : in  std_logic;",
        "          q   : out std_logic_vector(3 downto 0));",
        "end entity counter4;",
        "",
        "architecture rtl of counter4 is",
        "    signal cnt : unsigned(3 downto 0) := (others => '0');",
        "begin",
        "    process (clk)",
        "    begin",
        "        if rising_edge(clk) then",
        "            if rst = '1' then cnt <= (others => '0');",
        "            else              cnt <= cnt + 1;",
        "            end if;",
        "        end if;",
        "    end process;",
        "    q <= std_logic_vector(cnt);",
        "end architecture rtl;",
    ], caption="vhdl/counter4.vhd — the same hardware")

    w.para("VHDL is more verbose and far more strongly typed: the count is "
           "held as an unsigned value and has to be converted explicitly "
           "before it leaves the entity. Lab 5 simulates both and compares the "
           "waveforms.")

    w.h2("3.4  The ladder")

    w.para("The lecturer's \"simplistic view of the design flow\" is a ladder. "
           "Each box is a description; each arrow is a CAD tool.")
    w.image("flow_ladder", width=6.6)

    w.para("Three things are worth noticing. Each box is a document, not a "
           "stage of manufacture — it says what the circuit is, in a different "
           "vocabulary each time. Each arrow is a program that reads the "
           "description above it and writes the one below, adding detail that "
           "was not there before. And you never climb back up: each level "
           "fixes decisions that the level above deliberately left open.")

    w.h3("One circuit, all five levels")
    w.image("ladder_example", width=6.6)
    w.para("All five describe exactly the same 4-bit counter. A designer "
           "writes the first one. Tools produce the other four.")

    w.h3("What counts as a \"component\" changes at each level")
    w.image("abstraction_what_changes", width=6.6)
    w.para("Read the last column. The number of things to keep track of grows "
           "by roughly a factor of ten at every level, which is exactly why a "
           "designer works at the top of the table and lets tools handle the "
           "bottom.")

    w.page_break()

    # ---------------------------------------------------------- the steps
    w.h2("3.5  Behavioral design")

    w.para("At this level you specify the functionality of the design in terms "
           "of its behaviour. You say what you want, not how it is done. There "
           "are four common ways of writing it down.")
    w.image("behavioral_forms", width=6.6)

    w.para("Not one of these says how the circuit is BUILT. That is what makes "
           "them behavioural, and it is why a synthesis tool is free to build "
           "them in whichever way is cheapest under the constraints you set.")

    w.h2("3.6  Data path design, and what a netlist is")

    w.para("One step down, the components are no longer statements. They are "
           "registers, adders, multipliers, multiplexers, decoders and buses — "
           "things you could point at on a block diagram. This level is called "
           "register transfer level, and the name says what happens: on each "
           "clock edge, values are TRANSFERRED between REGISTERS, possibly "
           "through some logic on the way.")

    w.para("The output of this step is a netlist.")
    w.image("netlist_graph", width=6.6)

    w.callout("A netlist, defined", [
        [("A netlist is a ", {}), ("directed graph", {"b": True, "c": TEAL}),
         (". Its vertices are components; its edges are the interconnections "
          "between them. The whole graph is the design.", {})],
        "Why a graph rather than a drawing? Because a graph is something a "
        "program can hold in memory and transform. Every CAD step after this "
        "one — optimisation, technology mapping, placement, routing — is an "
        "operation on this graph.",
    ], color=TEAL)

    w.para("A netlist can be written at several levels. What changes is only "
           "what counts as a vertex.")
    w.image("netlist_levels", width=6.6)

    w.h3("Structural and behavioural, again")
    w.para("The lecturer says it explicitly: a netlist specification is also "
           "referred to as a structural design. The two words mean the same "
           "thing, and that gives the clearest possible statement of what "
           "synthesis is.")
    w.image("struct_vs_behav", width=6.6)

    w.callout("Synthesis, in one sentence", [
        "You write behavioural Verilog; the tool emits structural Verilog.",
    ], color=GREEN, bar="2A9D5C", fill="EEF7F1")

    w.para("Here is the same two-bit adder written both ways. Both are legal "
           "Verilog and both describe the same hardware.")
    w.code([
        "// BEHAVIOURAL - say what it does",
        "module add2 (input a, b, cin, output sum, cout);",
        "    assign {cout, sum} = a + b + cin;",
        "endmodule",
    ], caption="one line; the tool picks the gates")
    w.code([
        "// STRUCTURAL - say what it is made of",
        "module add2 (input a, b, cin, output sum, cout);",
        "    wire s1, c1, c2;",
        "    xor  u1 (s1,   a,  b);",
        "    and  u2 (c1,   a,  b);",
        "    xor  u3 (sum,  s1, cin);",
        "    and  u4 (c2,   s1, cin);",
        "    or   u5 (cout, c1, c2);",
        "endmodule",
    ], caption="five named gates, wired together — a netlist written as text")

    w.para("You will write far more behavioural code than structural. But the "
           "tool's output is always structural, which is exactly why you have "
           "to be able to read it.")

    w.h2("3.7  Logic design and standard cells")

    w.para("One step down again, the netlist's components become gates and "
           "flip-flops — or, more usefully, standard cells.")
    w.image("standard_cell", width=6.6)

    w.callout("What a standard cell is", [
        "A pre-designed circuit module — a gate, a flip-flop, a small "
        "multiplexer — held in a library as all of these at once: a symbol to "
        "place, a truth table to simulate, a timing model, and a finished "
        "piece of layout.",
        "Laying out a NAND gate correctly takes a skilled engineer a long "
        "time. Doing it once, perfectly, and then reusing it a million times "
        "is the only way the numbers work.",
    ], color=GREEN, bar="2A9D5C", fill="EEF7F1")

    w.para("At this level various logic optimisation techniques are applied to "
           "obtain a cost-effective design. The lecturer warns that the goals "
           "conflict, and names three.")
    w.image("opt_conflict", width=6.6)

    w.h2("3.8  Physical design and manufacturing")

    w.para("The last step generates the layout that goes to the foundry. At "
           "this level the design is a very large number of regular geometric "
           "shapes — mostly rectangles — one set per fabrication layer.")
    w.image("physical_design", width=6.6)

    w.para("They are rectangles because they are printed photographically, "
           "layer by layer, onto a silicon wafer: regular shapes expose "
           "cleanly and etch predictably, awkward ones do not.")

    w.h3("Or do not fabricate at all")
    w.para("The lecturer names the alternative: a field programmable gate "
           "array. An FPGA is a chip that has already been manufactured, full "
           "of configurable logic blocks that you program in your own "
           "laboratory. You get much greater flexibility, at the cost of "
           "speed.")
    w.image("asic_vs_fpga", width=6.6)

    w.h2("3.9  The other steps")

    w.para("The five rungs are not the whole flow. Three more steps run "
           "alongside them.")
    w.image("other_steps", width=6.6)

    w.para("Simulation is the one you will use constantly, from Lab 1 onwards, "
           "and Week 5 of the course is devoted to writing test benches. "
           "Formal verification and testability analysis are named here but "
           "are beyond this course's scope.")

    w.h2("3.10  Where the rest of the course sits")
    w.image("course_roadmap", width=6.6)
    w.para("Notice what is missing: nothing after logic design. Physical "
           "design, manufacturing and test are real and essential, but in this "
           "course they are the tools' job. Your work ends at a netlist.")

    w.page_break()
