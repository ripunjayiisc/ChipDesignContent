# -*- coding: utf-8 -*-
"""Lecture 01 deck — the practical component, and the close."""
import _boot
from deckkit import *
from l1_deck_a import R, card_from
import l1_lab

G = 91440


def build(d):
    # ================================================== PRACTICAL
    d.section_slide(
        "PRACTICAL", "Check It Yourself",
        "Lecture 01 makes one big claim: a CAD tool rewrites a hardware "
        "description as a more detailed one without changing what it does. "
        "In this section you install four free tools and test that claim.",
        ["Install Icarus Verilog, GTKWave, Yosys and GHDL — any platform",
         "Lab 1 · simulate a counter and look at its waveform",
         "Lab 2 · watch a tool rewrite your Verilog, and prove it still works",
         "Lab 3 · count the cells at each level of the flow",
         "Lab 4 · ASIC mapping against FPGA mapping",
         "Lab 5 · the same design in Verilog and in VHDL"],
        accent=GREEN)

    s = d.slide("P.1 · THE TOOLS", "The Toolchain for This Lecture",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "toolchain", 4150000)
    card_from(d, s, y + G, l1_lab.CARDS, "toolchain")

    s = d.slide("P.1 · THE TOOLS", "Installing It — One Line per Platform",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "install_routes", 4150000)
    card_from(d, s, y + G, l1_lab.CARDS, "install_routes")

    s = d.slide("P.1 · THE TOOLS", "Checking That It Worked", accent=GREEN)
    y = d.image(s, TOP - 45720, "verify_install", 4200000)
    d.card(s, y + G, "Versions newer than these are fine",
           [[R("The figures quoted throughout this deck were produced with "
               "Icarus 12.0, Yosys 0.33 and GHDL 4.1.0. A newer synthesiser "
               "may optimise slightly differently and report a different cell "
               "count — which is itself worth noticing, because it shows that "
               "optimisation has no single right answer.")]],
           accent=GREEN, fill=CARD_G, h=1188720)

    s = d.slide("P.2 · THE LABS", "The Five Labs, and What Each One Proves")
    y = d.image(s, TOP - 45720, "lab_map", 4150000)
    card_from(d, s, y + G, l1_lab.CARDS, "lab_map")

    # ---- Lab 1
    s = d.slide("LAB 1 · make sim", "The Design: a 4-Bit Counter",
                accent=GREEN)
    y = d.code(s, TOP, [
        "// counter4 - a 4-bit up counter, written BEHAVIOURALLY.",
        "//",
        "// Nothing here says which gates to use, or how many. It says only",
        "// what the output must be after each rising clock edge. Choosing",
        "// the gates is the synthesis tool's job.",
        "module counter4 (",
        "    input  wire       clk,",
        "    input  wire       rst,     // synchronous, active high",
        "    output reg  [3:0] q",
        ");",
        "    always @(posedge clk) begin",
        "        if (rst) q <= 4'd0;",
        "        else     q <= q + 4'd1;",
        "    end",
        "endmodule",
    ], size=12.0, title="rtl/counter4.v", accent=GREEN)
    d.card(s, y + G, "Ten lines of behaviour",
           [[R("This file never mentions a gate, a flip-flop or a wire "
               "between them. That is the whole point: it is a behavioural "
               "description, and everything below it in the flow will be "
               "produced from it by a program.")]], accent=GREEN,
           fill=CARD_G)

    s = d.slide("LAB 1 · make sim", "The Test Bench", accent=GREEN)
    y = d.code(s, TOP, [
        "`timescale 1ns/1ps",
        "module tb_counter4;",
        "    reg clk = 1'b0,  rst = 1'b1;",
        "    wire [3:0] q;",
        "    counter4 dut (.clk(clk), .rst(rst), .q(q));",
        "",
        "    always #5 clk = ~clk;        // 100 MHz: a 10 ns period",
        "",
        "    initial begin",
        "        $dumpfile(\"out/counter4.vcd\");  // record for GTKWave",
        "        $dumpvars(0, tb_counter4);",
        "        @(negedge clk);  rst = 1'b0;    // release reset",
        "        ...                             // check 20 cycles",
        "        $display(\"PASS  counter4 counted 0..15 and wrapped\");",
        "    end",
        "endmodule",
    ], size=11.5, title="rtl/tb_counter4.v  (abridged)", accent=TEAL)
    d.card(s, y + G, "A test bench is not hardware",
           [[R("It has no ports, it is never synthesised, and it may use "
               "delays, loops and $display freely. It is a program whose job "
               "is to drive the hardware and watch what comes out.")]],
           accent=TEAL)

    # ---- Lab 2
    s = d.slide("LAB 2 · make transform", "HDL In, HDL Out — Twice",
                accent=VIOLET)
    yy = TOP
    d.code(s, yy, [
        "// 1. what you wrote",
        "always @(posedge clk)",
        "  begin",
        "    if (rst) q <= 4'd0;",
        "    else     q <= q + 4'd1;",
        "  end",
    ], size=12.0, x=ML, w=(MW - 2 * 137160) / 3, accent=GREEN)
    d.code(s, yy, [
        "// 2. after synthesis (RTL)",
        "assign _0_ = q + 4'h1;",
        "always @(posedge clk)",
        "  if (rst) q <= 4'h0;",
        "  else     q <= _0_;",
    ], size=12.0, x=ML + (MW + 137160) / 3, w=(MW - 2 * 137160) / 3,
        h=1430000, accent=TEAL)
    y = d.code(s, yy, [
        "// 3. after mapping (gates)",
        "assign _02_[0] = ~q[0];",
        "assign _00_ = q[0] & q[1];",
        "assign _01_ = ~(q[2] & _00_);",
        "assign _03_[3] = ~(q[3] ^ _01_);",
        "assign _03_[1] = q[0] ^ q[1];",
        "assign _03_[2] = q[2] ^ _00_;",
    ], size=12.0, x=ML + 2 * (MW + 137160) / 3, w=(MW - 2 * 137160) / 3,
        h=1960000, accent=VIOLET)
    d.card(s, y + G, "All three are Verilog",
           [[R("That is the lecture's central slide, made concrete. The tool "
               "did not compile your design into something else — it re-"
               "described it, twice, each time in more detail. The third "
               "column is a netlist: gates and the wires between them.")]],
           accent=VIOLET)

    s = d.slide("LAB 2 · make prove", "And It Still Behaves the Same",
                accent=VIOLET)
    y = d.code(s, TOP, [
        "$ make prove",
        "",
        "--- 1. the behavioural description (what the designer wrote) ---",
        "PASS  counter4 counted 0..15 and wrapped correctly",
        "",
        "--- 2. synthesise it down to gates ---",
        "    wrote out/counter4_gates.v (33 lines)",
        "",
        "--- 3. the SAME test bench, run against the gate netlist ---",
        "PASS  counter4 counted 0..15 and wrapped correctly",
        "",
        "--- 4. compare the two waveforms, cycle by cycle ---",
        "IDENTICAL - 22 transitions, same value at the same time.",
        "The synthesiser changed the DESCRIPTION, not the BEHAVIOUR.",
    ], size=11.5, title="the whole claim of Lecture 01, in one command",
        accent=VIOLET)
    d.card(s, y + G, "Why this is worth running yourself",
           [[R("One test bench, two very different descriptions, identical "
               "output at every instant. Nothing in the lecture has to be "
               "taken on trust after this.")]], accent=VIOLET)

    # ---- Lab 3
    s = d.slide("LAB 3 · make ladder", "What the Tools Actually Reported")
    y = d.image(s, TOP - 45720, "measured", 4150000)
    card_from(d, s, y + G, l1_lab.CARDS, "measured")

    # ---- Lab 4
    s = d.slide("LAB 4 · make target", "ASIC Mapping against FPGA Mapping",
                accent=AMBER)
    yy = TOP
    d.code(s, yy, [
        "=== mapped to logic GATES (the ASIC route) ===",
        "   Number of cells:         10",
        "     $_AND_                  1",
        "     $_NAND_                 1",
        "     $_NOT_                  1",
        "     $_SDFF_PP0_             4",
        "     $_XNOR_                 1",
        "     $_XOR_                  2",
    ], size=12.5, x=ML, w=(MW - 182880) / 2, h=2260000, accent=TEAL)
    y = d.code(s, yy, [
        "=== mapped to 4-input LUTs (the FPGA route) ===",
        "   Number of cells:          8",
        "     $_SDFF_PP0_             4",
        "     $lut                    4",
        "",
        "// four look-up tables replace",
        "// the six gates on the left",
    ], size=12.5, x=ML + (MW + 182880) / 2, w=(MW - 182880) / 2,
        h=2260000, accent=VIOLET)
    d.card(s, y + G, "Same source file, two different targets",
           [[R("The four flip-flops are the same either way — one per bit of "
               "the counter. What changes is the combinational logic: six "
               "dedicated gates for silicon you will manufacture, or four "
               "look-up tables inside a chip you can buy today. That is the "
               "flexibility-for-speed trade the lecturer names.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ---- Lab 5
    s = d.slide("LAB 5 · make langs", "The Same Design in Two Languages",
                accent=RED)
    y = d.code(s, TOP, [
        "$ make langs",
        "--- Verilog (Icarus) ---     PASS  counted 0..15 and wrapped",
        "--- VHDL (GHDL) ---          PASS  counted 0..15 and wrapped",
        "",
        "--- the whole run, including time zero ---",
        "they differ, and ONLY here:",
        "    <      0.000 ns   xxxx          (Verilog)",
        "    <      5.000 ns   0000",
        "    >      0.000 ns   0000          (VHDL)",
        "",
        "--- from the end of reset onwards (15 ns) ---",
        "IDENTICAL - 20 transitions, same value at the same time",
    ], size=12.5, title="two languages, one circuit", accent=RED)
    d.card(s, y + G, "The one difference is the most useful part of the lab",
           [[R("A Verilog reg holds x — unknown — until something drives "
               "it, so q reads xxxx until the reset edge clears it. The VHDL "
               "signal was declared with an initial value, so it reads 0000 "
               "from time zero. The hardware is identical: a real flip-flop "
               "also powers up unpredictably, which is why designs have "
               "resets.")]], accent=RED, fill=CARD_R, h=1097280)

    s = d.slide("P.3 · EXERCISES", "Take It Further")
    d.bullets(s, TOP, [
        [R("1.  Change the counter to 8 bits. Re-run ", s=12.0),
         R("make ladder", f=MONO_FONT, s=11.5),
         R(" and record the new cell counts. Did the number of gates double?",
           s=12.0)],
        [R("2.  Make the reset asynchronous — ", s=12.0),
         R("always @(posedge clk or posedge rst)", f=MONO_FONT, s=11.0),
         R(" — and compare the gate-level netlists before and after.",
           s=12.0)],
        [R("3.  Write a down-counter and prove it with ", s=12.0),
         R("make prove", f=MONO_FONT, s=11.5),
         R(". How many cells does it take compared with counting up?",
           s=12.0)],
        [R("4.  Open both ", s=12.0),
         R("out/counter4_behav.vcd", f=MONO_FONT, s=11.0),
         R(" and ", s=12.0), R("out/counter4_gates.vcd", f=MONO_FONT, s=11.0),
         R(" in GTKWave at the same time and align them.", s=12.0)],
        [R("5.  Try ", s=12.0), R("abc -lut 6", f=MONO_FONT, s=11.5),
         R(" instead of ", s=12.0), R("abc -lut 4", f=MONO_FONT, s=11.5),
         R(". Why do larger look-up tables need fewer of them?", s=12.0)],
        [R("6.  Write the counter in VHDL from memory, then diff your version "
           "against ", s=12.0), R("vhdl/counter4.vhd", f=MONO_FONT, s=11.0),
         R(".", s=12.0)],
    ], step=457200)
    d.lead(s, TOP + 6 * 457200 + G,
           [[R("The workbook carries all of these with full worked solutions, "
               "plus thirty more.", b=True, c=NAVY, s=12.0)]], h=320040)

    # ================================================== CLOSE
    s = d.slide("CHECKPOINT", "Ten Questions on Lecture 01", accent=NAVY)
    y = d.cols(s, TOP, [
        ("", [[R("1.  Name the five levels of the design flow, in order.",
                 s=11.5)],
              [R("2.  What are the INPUT and the OUTPUT of a CAD tool?",
                 s=11.5)],
              [R("3.  Define a netlist.", s=11.5)],
              [R("4.  What does \"register transfer\" refer to?", s=11.5)],
              [R("5.  Give two ways of specifying behaviour.", s=11.5)]],
         TEAL, CARD),
        ("", [[R("6.  What is a standard cell, and why does a library of them "
                 "exist?", s=11.5)],
              [R("7.  State Moore's Law. Is it a law of physics?", s=11.5)],
              [R("8.  Name three optimisation goals that conflict.", s=11.5)],
              [R("9.  Give one advantage of an FPGA over an ASIC, and one "
                 "the other way.", s=11.5)],
              [R("10. Why is a netlist also called a structural description?",
                 s=11.5)]],
         VIOLET, CARD)],
        h=2011680)
    d.card(s, y + G, "Answers",
           [[R("Every one of these is answered somewhere in this deck, and "
               "all ten appear with model answers in the workbook. Questions "
               "2, 3 and 10 are the ones that matter most for the rest of the "
               "module.")]], accent=NAVY)

    s = d.slide("SUMMARY", "What Lecture 01 Established")
    y = d.tiers(s, TOP, [
        ("THE PROBLEM",
         "Chips grew from a handful of transistors to billions. No human can "
         "place them, and the requirements — area, speed, power — conflict.",
         RED),
        ("THE ANSWER",
         "A standardized design flow: specification, behavioural design, data "
         "path, logic, physical, manufacturing. Each step has a defined input "
         "and output, and each is carried out by a program.", AMBER),
        ("THE MECHANISM",
         "A CAD tool reads a hardware description and writes a more detailed "
         "hardware description. It never changes what the circuit does — you "
         "proved this yourself in Lab 2.", VIOLET),
        ("THE LANGUAGE",
         "Those descriptions are written in an HDL. Verilog and VHDL are the "
         "two in common use; this course uses Verilog. An HDL is not a "
         "programming language.", TEAL),
        ("YOUR PLACE IN IT",
         "A Verilog designer works at the behavioural and data path levels. "
         "Everything below is the tools' job — which is why those two levels "
         "are what the next seven weeks teach.", GREEN)],
        h=868680, gap=36576)

    s = d.slide("NEXT", "Lecture 02 — Design Representation")
    y = d.lead(s, TOP, [
        [R("The next lecture takes the one idea this one left implicit — that "
           "the same design can be looked at from different angles — and makes "
           "it the subject.", s=13.0)]], h=640080)
    y = d.cols(s, y + G, [
        ("BEHAVIOURAL", [[R("Algorithms, specifications, Boolean expressions, "
                            "truth tables, state diagrams.", s=11.5)]],
         VIOLET, CARD),
        ("STRUCTURAL", [[R("Netlists: modules, gates and transistors, and the "
                           "wires between them.", s=11.5)]], TEAL, CARD),
        ("PHYSICAL", [[R("Floorplans, cell placement, routing, and the final "
                         "layout geometry.", s=11.5)]], AMBER, CARD_A)],
        h=1188720)
    d.card(s, y + G, "The Y-diagram",
           [[R("Lecture 02 arranges those three as the arms of a Y, with "
               "the highest level of abstraction at the outside and the "
               "finished layout at the centre. Every design step is then a "
               "move along an arm, or a jump between arms — and Module 2 "
               "lives on the behavioural and structural arms.")]],
           accent=NAVY)
