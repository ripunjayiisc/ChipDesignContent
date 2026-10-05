# -*- coding: utf-8 -*-
"""Lecture 01 workbook — Part 4: installing the tools, and the five labs."""
import _boot
from wbkit import *


def build(w):
    w.h1("Part 4 · The Practical Component")

    w.para("Everything in this part is something you run. Every output printed "
           "below was produced by actually running the command above it, on a "
           "clean machine, with the versions named in section 4.1.")

    # ===================================================== 4.1 install
    w.h2("4.1  Installing the toolchain")

    w.para("Four programs, one for each thing the lecture says a CAD flow must "
           "do. All four are open source and run on Windows, macOS and Linux.")
    w.image("toolchain", width=6.6)

    w.table(["Tool", "What it does", "Used in"],
            [["Icarus Verilog", "compiles and simulates Verilog",
              "Labs 1, 2, 5"],
             ["GTKWave", "draws the waveforms a simulation recorded",
              "Lab 1"],
             ["Yosys", "synthesis — the CAD tool of the lecture",
              "Labs 2, 3, 4"],
             ["GHDL", "compiles and simulates VHDL", "Lab 5"]],
            widths=[1.5, 3.3, 1.9], size=10)

    w.h3("Linux (Ubuntu or Debian)")
    w.code([
        "sudo apt update",
        "sudo apt install -y iverilog gtkwave yosys ghdl",
    ])

    w.h3("macOS (Homebrew)")
    w.code([
        "brew install icarus-verilog",
        "brew install --cask gtkwave",
        "brew install yosys ghdl",
    ])

    w.h3("Windows")
    w.para("Use the Windows Subsystem for Linux. It gives you a real Ubuntu "
           "inside Windows, and every command in this workbook then works "
           "unchanged. Open PowerShell as Administrator and run:")
    w.code([
        "wsl --install",
    ])
    w.para("Restart when it asks you to, open the Ubuntu application it "
           "installed, and then follow the Linux instructions above.")

    w.callout("GTKWave on WSL", [
        "GTKWave is a graphical program and needs a display. Recent versions "
        "of Windows provide one automatically (WSLg) and GTKWave will simply "
        "open. If it complains that DISPLAY is not set, either update WSL "
        "with  wsl --update  , or install GTKWave natively on Windows and open "
        "the .vcd files from there — they are ordinary files in your WSL home "
        "directory.",
    ], color=AMBER, bar="C77514", fill="FFF7EC")

    w.h3("Checking that it worked")
    w.para("Run all four. Each must print a version number.")
    w.code([
        "$ iverilog -V",
        "Icarus Verilog version 12.0 (stable)",
        "",
        "$ yosys -V",
        "Yosys 0.33 (git sha1 2584903a060)",
        "",
        "$ ghdl --version",
        "GHDL 4.1.0 (Ubuntu 4.1.0+dfsg-0ubuntu2.1) [Dunoon edition]",
        "",
        "$ gtkwave --version",
        "GTKWave Analyzer v3.3.x",
    ], caption="the versions these labs were produced with")

    w.callout("If a version differs", [
        "Newer is fine. A newer synthesiser may optimise slightly differently "
        "and report a different cell count from the ones printed in this "
        "workbook. That is worth noticing rather than worrying about: it "
        "demonstrates directly that optimisation has no single right answer.",
    ], color=GREEN, bar="2A9D5C", fill="EEF7F1")

    w.h3("Getting the lab files")
    w.code([
        "cd ChipDesignAssociate/VerilogCourse/Lecture01_Lab",
        "make            # runs every lab in order",
    ])
    w.para("The directory contains:")
    w.table(["Path", "What is in it"],
            [["rtl/counter4.v", "the design, written behaviourally"],
             ["rtl/tb_counter4.v", "the test bench"],
             ["vhdl/counter4.vhd", "the same design in VHDL"],
             ["vhdl/tb_counter4.vhd", "the VHDL test bench"],
             ["scripts/*.ys", "the Yosys scripts, one per level of the flow"],
             ["scripts/*.sh", "the lab drivers"],
             ["scripts/vcd_q.py", "reads a waveform file and prints one signal"],
             ["Makefile", "one target per lab"],
             ["out/", "everything the labs produce (created on first run)"]],
            widths=[2.2, 4.5], size=10, align_center=False)

    w.page_break()

    # ===================================================== Lab 1
    w.h2("4.2  Lab 1 — simulate a counter and look at it")

    w.callout("What this lab proves", [
        "That you can take a description of hardware, run it, and see what it "
        "does. This is the \"simulation for verification\" step of the design "
        "flow.",
    ], color=GREEN, bar="2A9D5C", fill="EEF7F1")

    w.h3("The design")
    w.code([
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
    ], caption="rtl/counter4.v")

    w.para("Read it as a description, not as a program. It says: there is a "
           "four-bit register called q; on every rising edge of clk, it takes "
           "either zero or its own value plus one. It does not say how.")

    w.h3("The test bench")
    w.code([
        "`timescale 1ns/1ps",
        "module tb_counter4;",
        "    reg        clk = 1'b0;",
        "    reg        rst = 1'b1;",
        "    wire [3:0] q;",
        "    integer    errors = 0;",
        "    integer    i;",
        "    reg  [3:0] expected;",
        "",
        "    counter4 dut (.clk(clk), .rst(rst), .q(q));",
        "",
        "    always #5 clk = ~clk;          // 100 MHz: a 10 ns period",
        "",
        "    initial begin",
        "        $dumpfile(\"out/counter4.vcd\");",
        "        $dumpvars(0, tb_counter4);",
        "",
        "        @(negedge clk);",
        "        if (q !== 4'd0) errors = errors + 1;",
        "        rst      = 1'b0;",
        "        expected = 4'd1;",
        "",
        "        for (i = 0; i < 20; i = i + 1) begin",
        "            @(negedge clk);",
        "            if (q !== expected) errors = errors + 1;",
        "            expected = expected + 4'd1;",
        "        end",
        "",
        "        if (errors == 0)",
        "            $display(\"PASS  counter4 counted 0..15 and wrapped\");",
        "        $finish;",
        "    end",
        "endmodule",
    ], caption="rtl/tb_counter4.v (abridged — the full file prints each "
               "mismatch)")

    w.callout("Why expected starts at 1, not 0", [
        "The rising edge at 5 ns happens while rst is still high, so the "
        "register is cleared there. Reset is released on the falling edge at "
        "10 ns, which means the next rising edge — at 15 ns — is already the "
        "first counting edge.",
        "This off-by-one is the single most common mistake in a first test "
        "bench. Getting it right means thinking about WHEN each edge happens, "
        "which is exactly the habit the rest of the course needs.",
    ], color=VIOLET, bar="7A4FBF")

    w.h3("Run it")
    w.code([
        "$ make sim",
        "iverilog -g2012 -o out/tb_counter4.vvp rtl/counter4.v rtl/tb_counter4.v",
        "vvp out/tb_counter4.vvp",
        "VCD info: dumpfile out/counter4.vcd opened for output.",
        "PASS  counter4 counted 0..15 and wrapped correctly",
    ])

    w.para("Two commands ran. The first, iverilog, compiled the design and the "
           "test bench into a simulation program. The second, vvp, ran it.")

    w.h3("Look at the waveform")
    w.code([
        "$ make wave",
    ])
    w.para("GTKWave opens. Drag clk, rst and q from the signal list into the "
           "wave window. You should see q change immediately after each rising "
           "clock edge, counting 1, 2, 3 … 15, 0, 1 …")

    w.callout("What to notice in the waveform", [
        "q is xxxx — unknown — until the first clock edge. A Verilog reg holds "
        "x until something drives it, and a real flip-flop likewise powers up "
        "in an unpredictable state. That is why every design has a reset.",
        "q changes AFTER the clock edge, not at it. That delay is the "
        "flip-flop's clock-to-Q time, and it is the first thing that eats into "
        "your clock period.",
    ], color=TEAL)

    w.page_break()

    # ===================================================== Lab 2
    w.h2("4.3  Lab 2 — watch a CAD tool rewrite your Verilog")

    w.callout("What this lab proves", [
        "The central claim of Lecture 01: that a CAD tool transforms an HDL "
        "input into an HDL output containing more detail about the hardware, "
        "without changing what the circuit does.",
    ], color=VIOLET, bar="7A4FBF")

    w.h3("Step 1 — the transformation, twice")
    w.code([
        "$ make transform",
    ])
    w.para("This prints three descriptions of the same counter. The first is "
           "what you wrote:")
    w.code([
        "always @(posedge clk) begin",
        "    if (rst) q <= 4'd0;",
        "    else     q <= q + 4'd1;",
        "end",
    ], caption="1 — behavioural, written by a human")

    w.para("The second is what Yosys produced after synthesis. It is still "
           "Verilog, but the increment has become a named component with its "
           "own wire:")
    w.code([
        "wire [3:0] _0_;",
        "assign _0_ = q + 4'h1;          // an incrementer",
        "always @(posedge clk)           // a 4-bit register",
        "  if (rst) q <= 4'h0;           // with a synchronous reset",
        "  else     q <= _0_;",
    ], caption="2 — register transfer level, written by Yosys")

    w.para("The third is what Yosys produced after mapping to gates. Still "
           "Verilog, and now every operation is a single logic function:")
    w.code([
        "assign _02_[0] = ~q[0];",
        "assign _00_ = q[0] & q[1];",
        "assign _01_ = ~(q[2] & _00_);",
        "assign _03_[3] = ~(q[3] ^ _01_);",
        "assign _03_[1] = q[0] ^ q[1];",
        "assign _03_[2] = q[2] ^ _00_;",
    ], caption="3 — gate level, written by Yosys")

    w.callout("Look at what just happened", [
        "All three files are Verilog. The tool did not compile your design "
        "into something else — it re-described it, twice, each time in more "
        "detail. The third is a netlist: gates, and the wires between them.",
    ], color=VIOLET, bar="7A4FBF")

    w.h3("Step 2 — and it still behaves the same")

    w.para("A more detailed description is only useful if it is still the same "
           "circuit. Run the SAME test bench against the gate netlist:")
    w.code([
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
    ])

    w.para("One test bench, two very different descriptions, identical output "
           "at every instant. Nothing in the lecture has to be taken on trust "
           "after this.")

    w.callout("How the gate netlist can be simulated at all", [
        [("Yosys emits primitives with names like ", {}),
         ("$_AND_", {"f": MONOF, "s": 10}), (" and ", {}),
         ("$_SDFF_PP0_", {"f": MONOF, "s": 10}),
         (". Yosys ships a file, ", {}), ("simcells.v", {"f": MONOF, "s": 10}),
         (", that defines them as ordinary Verilog modules; the lab script "
          "finds it and passes it to Icarus along with the netlist.", {})],
    ], color=TEAL)

    w.page_break()

    # ===================================================== Lab 3
    w.h2("4.4  Lab 3 — count the cells at each level")

    w.callout("What this lab proves", [
        "That detail really does increase down the ladder, in a way you can "
        "put a number on.",
    ], color=TEAL)

    w.code([
        "$ make ladder",
        "",
        "LEVEL                         CELLS   WHAT THEY ARE",
        "-------------------------- --------   -------------",
        "1  Behavioural (source)           -   10 lines of Verilog - no cells",
        "2  Data path (RTL)                2   $add x1  $sdff x1",
        "3  Logic (gates)                 10   $_AND_ x1  $_NAND_ x1  $_NOT_ x1",
        "                                      $_SDFF_PP0_ x4  $_XNOR_ x1",
        "                                      $_XOR_ x2",
        "   same, for an FPGA              8   $_SDFF_PP0_ x4  $lut x4",
    ])

    w.para("Read it downwards. Ten lines of behaviour became two RTL "
           "components — one adder and one four-bit register, which is exactly "
           "what section 3.6 said \"data path design\" means. Those two became "
           "ten gate-level cells: four flip-flops, one per bit, and six logic "
           "gates to compute the next value.")

    w.image("measured", width=6.6, caption="the same table, as the slide shows it")

    w.callout("A detail worth noticing", [
        [("One ", {}), ("$sdff", {"f": MONOF, "s": 10}),
         (" at RTL became four ", {}),
         ("$_SDFF_PP0_", {"f": MONOF, "s": 10}),
         (" at gate level. At RTL a register is one component that happens to "
          "be four bits wide; at gate level each bit is its own flip-flop. The "
          "vocabulary changed, not the circuit.", {})],
    ], color=NAVY)

    # ===================================================== Lab 4
    w.h2("4.5  Lab 4 — ASIC mapping against FPGA mapping")

    w.callout("What this lab proves", [
        "That the same Verilog produces different hardware depending on what "
        "you are building it for — the flexibility-for-speed trade the "
        "lecturer names when he introduces FPGAs.",
    ], color=AMBER, bar="C77514", fill="FFF7EC")

    w.code([
        "$ make target",
        "",
        "=== mapped to logic GATES (the ASIC route) ===",
        "   Number of cells:         10",
        "     $_AND_                  1",
        "     $_NAND_                 1",
        "     $_NOT_                  1",
        "     $_SDFF_PP0_             4",
        "     $_XNOR_                 1",
        "     $_XOR_                  2",
        "",
        "=== mapped to 4-input LOOK-UP TABLES (the FPGA route) ===",
        "   Number of cells:          8",
        "     $_SDFF_PP0_             4",
        "     $lut                    4",
    ])

    w.para("The flip-flops are the same either way — one per bit of the "
           "counter. What changes is the combinational logic: six dedicated "
           "gates for silicon you will manufacture, or four look-up tables "
           "inside a chip you can buy today.")

    w.table(["", "ASIC", "FPGA"],
            [["What you receive", "masks, then wafers from a foundry",
              "a bitstream you load into a board"],
             ["Turnaround", "weeks to months", "minutes"],
             ["Cost to start", "very high — mask sets dominate",
              "the price of the board"],
             ["Cost per unit at volume", "very low", "stays high"],
             ["Speed", "highest", "lower — logic is configurable, not fixed"],
             ["Changeable after?", "no — respin and pay again",
              "yes, reprogram in the lab"]],
            widths=[1.6, 2.6, 2.6], size=9.5, align_center=False)

    w.h3("Why a LUT replaces several gates")
    w.para("A four-input look-up table is a small memory holding sixteen bits. "
           "Program those sixteen bits and it can compute ANY function of four "
           "inputs. So a chain of two or three gates with four inputs between "
           "them collapses into one LUT — which is why the FPGA cell count is "
           "lower even though the chip is slower.")

    w.page_break()

    # ===================================================== Lab 5
    w.h2("4.6  Lab 5 — the same design in two languages")

    w.callout("What this lab proves", [
        "That the choice between Verilog and VHDL is a matter of style, not of "
        "what the hardware can do.",
    ], color=RED, bar="C01F43", fill="FDECEF")

    w.code([
        "$ make langs",
        "",
        "--- Verilog (Icarus) ---",
        "PASS  counter4 counted 0..15 and wrapped correctly",
        "",
        "--- VHDL (GHDL) ---",
        "PASS  counter4 counted 0..15 and wrapped correctly",
        "",
        "--- the whole run, including time zero ---",
        "they differ, and ONLY here:",
        "    1,2c1",
        "    <      0.000 ns   xxxx",
        "    <      5.000 ns   0000",
        "    ---",
        "    >      0.000 ns   0000",
        "",
        "--- from the end of reset onwards (15 ns) ---",
        "IDENTICAL - 20 transitions, same value at the same time",
    ])

    w.callout("The one difference is the most useful part of the lab", [
        [("A Verilog ", {}), ("reg", {"f": MONOF, "s": 10}),
         (" holds x — unknown — until something drives it, so q reads xxxx "
          "until the reset edge at 5 ns clears it. The VHDL signal was "
          "declared with an initial value, so it reads 0000 from time zero.",
          {})],
        "The described hardware is identical. A real flip-flop also powers up "
        "in an unpredictable state, which is exactly why every design has a "
        "reset — and why the Verilog behaviour is arguably the more honest "
        "model of the two.",
    ], color=RED, bar="C01F43", fill="FDECEF")

    w.h3("How the comparison is done")
    w.para("Icarus and GHDL write their waveform files with different "
           "timescales and different internal identifiers, so the raw files "
           "cannot be compared directly. The lab includes a small reader that "
           "normalises both to nanoseconds and to plain binary:")
    w.code([
        "$ python3 scripts/vcd_q.py out/counter4.vcd q | head -4",
        "     0.000 ns   xxxx",
        "     5.000 ns   0000",
        "    15.000 ns   0001",
        "    25.000 ns   0010",
    ])
    w.para("Two details in that script are worth knowing about, because both "
           "are easy to get wrong. Times are kept as whole femtoseconds rather "
           "than floating-point nanoseconds, because comparing floating-point "
           "times across two different timescales is unreliable. And a vector "
           "is padded on the left with 0, except that a value starting with x "
           "or z extends with that character — which is why the first line "
           "above reads xxxx and not 000x.")

    w.h3("A note on GHDL back ends")
    w.para("GHDL has several code generators. With the mcode back end — the "
           "usual one on Ubuntu — ghdl -e does not write an executable file "
           "and you run the simulation with ghdl -r. With the LLVM or GCC back "
           "ends, ghdl -e produces a binary you run directly. The lab script "
           "uses ghdl -r, which works with all of them.")

    w.page_break()
