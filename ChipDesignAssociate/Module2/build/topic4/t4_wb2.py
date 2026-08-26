# -*- coding: utf-8 -*-
"""Topic 4 workbook — Part 1 continued (procedural constructs) and Part 2 (modelling)."""
import _boot
from wbkit import *
from t4_wb1 import B, N, I, M


def build(w):
    w.page_break()
    # ---------------------------------------------------------- 1.10
    w.h2("1.10  The three constructs that describe logic")
    w.image("three_constructs", 6.2, "Everything synthesisable is one of these three.")
    w.table(["Construct", "Written as", "Becomes", "Use it for"],
            [["Continuous assignment", "assign y = ...;", "A cloud of gates",
              "Short combinational expressions"],
             ["Combinational block", "always @(*) ... = ...", "A cloud of gates",
              "Longer logic: case, if/else chains"],
             ["Clocked block", "always @(posedge clk) ... <= ...", "Flip-flops plus gates",
              "Anything that must remember"]],
            widths=[1.5, 1.9, 1.3, 1.9], size=9, align_center=False)

    w.h3("Continuous assignment")
    w.para("An assign is a permanent connection, not an instruction. It is not executed once — it "
           "is always true. Whenever anything on the right-hand side changes, the left-hand side "
           "follows in zero simulation time. Think of it as solder.")
    w.code([
        "assign y        = a & b;              // one AND gate",
        "assign z        = sel ? p : q;        // a 2:1 multiplexer",
        "assign {co,sum} = a + b + cin;        // a 9-bit result split into carry and sum",
        "assign parity   = ^data;              // an XOR tree",
        "assign any_req  = |req;               // an OR tree",
        "",
        "// Order is irrelevant. These three describe ONE circuit whatever order you type them.",
        "assign c = a ^ b;",
        "assign e = c & d;",
        "assign d = ~a;",
    ], caption="Continuous assignments")
    w.bullets([
        [N("The left side must be a net ("), M("wire"), N("), never a "), M("reg"), N(".")],
        "A wire may be driven by exactly one assign. Two drivers give x.",
        "No if, case or for — expressions only. Use the conditional operator for choices.",
        "The moment you find yourself nesting three conditional operators, rewrite it as an "
        "always @(*) block with a case statement. Unreadable RTL is where bugs live.",
    ])

    w.h3("Procedural blocks")
    w.code([
        "always @(*)               begin ... end   // combinational -- gates",
        "always @(posedge clk)     begin ... end   // clocked       -- flip-flops",
        "always @(posedge clk or negedge rst_n)    // clocked with async reset",
        "",
        "initial                   begin ... end   // once, at time 0 -- SIMULATION ONLY",
        "always                    begin ... end   // forever -- testbench clock generation",
    ], caption="The forms of procedural block")
    w.para("Blocks run concurrently with each other; statements run sequentially within one block. "
           "That distinction is the whole reason hardware description works.")
    w.table(["Sensitivity", "Meaning", "Note"],
            [["@(*)", "Re-run whenever anything READ in the block changes",
              "Always use this for combinational logic"],
             ["@(a or b or sel)", "Re-run on those signals only",
              "A hand-written list is a bug waiting for the day someone adds a signal"],
             ["@(posedge clk)", "Run at the instant the clock rises",
              "Everything assigned with <= becomes a flip-flop"],
             ["@(posedge clk or negedge rst_n)", "Also run when the reset falls",
              "Asynchronous reset"],
             ["initial", "Run once at time zero",
              "No hardware equivalent in ASIC. FPGAs honour it for power-up values; do not rely "
              "on it."]],
            widths=[1.7, 2.1, 2.8], size=9, align_center=False)

    # ---------------------------------------------------------- 1.11
    w.h2("1.11  Control flow")
    w.h3("if / else is a priority structure")
    w.para("An if/else chain does not 'test conditions one after another' — nothing happens 'one "
           "after another' in a wire. It synthesises to a chain of multiplexers where the first "
           "condition has the highest priority. That chain has depth, and depth is delay.")
    w.code([
        "// Priority -- three multiplexers in series. Deeper, slower.",
        "if      (a) y = 2'd0;",
        "else if (b) y = 2'd1;",
        "else if (c) y = 2'd2;",
        "else        y = 2'd3;",
        "",
        "// Parallel -- ONE multiplexer. Shallower, faster.",
        "case (sel)",
        "  2'd0: y = 2'd0;   2'd1: y = 2'd1;",
        "  2'd2: y = 2'd2;   2'd3: y = 2'd3;",
        "endcase",
    ], caption="Priority versus parallel selection")
    w.para("Use priority when the conditions genuinely overlap and one must win — an interrupt "
           "controller, a bus arbiter. Use case when they are mutually exclusive, which is most "
           "of the time.")

    w.h3("case, casez and casex")
    w.code([
        "// case -- exact 4-state match. The workhorse. ALWAYS write a default.",
        "case (opcode)",
        "  4'b0000: y = a + b;",
        "  4'b0001: y = a - b;",
        "  default: y = 8'd0;",
        "endcase",
        "",
        "// casez -- ? and z in the LABEL are don't-care. Correct for priority encoders.",
        "casez (req)",
        "  4'b1???: grant = 2'd3;",
        "  4'b01??: grant = 2'd2;",
        "  4'b001?: grant = 2'd1;",
        "  default: grant = 2'd0;",
        "endcase",
    ], caption="case and casez")
    w.callout("casex is banned, and so are full_case / parallel_case", [
        [N("casex treats an x in the "), B("selector"), N(" as a wildcard too. An uninitialised "
           "signal will then match the FIRST label and appear to work in simulation, while the "
           "synthesised hardware does something else. It conceals precisely the bug you most need "
           "to see.")],
        [N("full_case and parallel_case are synthesis pragmas that PROMISE the tool all cases are "
           "covered and mutually exclusive. If the promise is false, simulation and synthesis "
           "silently disagree — the hardest class of bug there is. A real "), M("default"),
         N(" branch costs nothing and cannot lie.")],
    ], color=RED, fill="FDECEF", bar="C01F43")

    w.h3("Loops are unrolled, not executed")
    w.para("A for loop in synthesisable Verilog is a copy-paste instruction to the tool. It does "
           "not create a counter and takes no time. The bounds must be constants, and eight "
           "iterations means eight copies of the hardware.")
    w.code([
        "integer i;",
        "always @(*) begin",
        "  cnt = 4'd0;",
        "  for (i = 0; i < 8; i = i + 1)",
        "    cnt = cnt + data[i];        // EIGHT adders in a tree, not a loop",
        "end",
        "",
        "// Reversing a bus: 8 wires crossed over. Zero gates, zero delay.",
        "always @(*)",
        "  for (i = 0; i < 8; i = i + 1) rev[i] = fwd[7-i];",
    ], caption="Synthesisable loops")
    w.table(["Synthesisable", "Simulation only"],
            [["for with constant start, limit and step", "while — bound depends on a signal"],
             ["repeat (N) with constant N", "forever"],
             ["Loop variable is integer or genvar", "Any loop whose trip count is not known "
              "at elaboration"]],
            widths=[3.3, 3.3], size=9.5, align_center=False)
    w.para("If you need 'repeat until a signal changes', that is a state machine or a counter. "
           "Build it explicitly; the tool cannot invent it for you.")

    # ---------------------------------------------------------- 1.12
    w.h2("1.12  Functions and tasks")
    w.code([
        "// FUNCTION -- synthesisable. No time control, >=1 input, returns exactly one value.",
        "function [3:0] bcd_digit;",
        "  input [7:0] v;",
        "  begin",
        "    bcd_digit = v % 10;         // the function name IS the return variable",
        "  end",
        "endfunction",
        "",
        "assign d0 = bcd_digit(count);   // one copy of the logic HERE ...",
        "assign d1 = bcd_digit(other);   // ... and a SECOND, independent copy here",
        "",
        "// TASK -- may consume time, may have several outputs. Testbench use.",
        "task send_byte(input [7:0] b);",
        "  begin",
        "    tx_data = b; tx_start = 1'b1; @(posedge clk); tx_start = 1'b0;",
        "    wait (tx_busy == 1'b0);",
        "  end",
        "endtask",
    ], caption="Function versus task")
    w.table(["", "Function", "Task"],
            [["May consume time (#, @, wait)", "No", "Yes"],
             ["Number of outputs", "Exactly one (the return)", "Any number, via output ports"],
             ["May call a task", "No", "Yes"],
             ["Synthesisable", "Yes, if it obeys the rules", "Generally no"],
             ["Typical use", "Shared combinational logic", "Testbench stimulus sequences"]],
            widths=[2.2, 2.2, 2.2], size=9.5, align_center=False)
    w.callout("The cost that must be remembered",
              [[N("A function call is not a subroutine call. There is no 'calling' at run time: "
                  "each call site gets its own physical copy of the logic. "),
                B("Four calls to a 16-bit multiplier function means four multipliers on the die."),
                N(" If you want ONE shared unit used at different times, that is a datapath with "
                  "a multiplexer in front of it and a controller to drive it — an architectural "
                  "decision, not a syntax choice.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 1.13
    w.h2("1.13  Parameters, localparam and generate")
    w.image("parameters", 5.8, "One source file, three different circuits.")
    w.code([
        "module counter #(parameter integer W = 8, parameter [W-1:0] MAX = {W{1'b1}})",
        "  (input wire clk, rst_n, en, output reg [W-1:0] q, output wire tc);",
        "",
        "  localparam [W-1:0] ZERO = {W{1'b0}};    // localparam CANNOT be overridden",
        "  ...",
        "endmodule",
        "",
        "counter #(.W(4), .MAX(4'd9)) u_dig0 (.clk(clk), .rst_n(rst_n), ...);   // decade counter",
        "counter #(.W(16))            u_big  (.clk(clk), .rst_n(rst_n), ...);   // 16-bit counter",
    ], caption="Parameterisation")
    w.bullets([
        [B("parameter"), N(" — may be overridden at instantiation. Use for widths, depths and "
                           "timing constants that a user of the module should be able to set.")],
        [B("localparam"), N(" — may not be overridden. Use for state encodings, derived widths "
                            "and anything whose value must stay consistent with the module's "
                            "internal logic.")],
        [M("$clog2(N)"), N(" — ceiling log base 2, evaluated at elaboration. This is how you "
                           "compute 'how many bits do I need to count to N'. It is one of the "
                           "very few $ functions that is synthesisable.")],
    ])
    w.h3("generate")
    w.image("generate_block", 5.6, "A loop that creates structure, not logic.")
    w.code([
        "genvar i;",
        "generate",
        "  for (i = 0; i < W; i = i + 1) begin : bit_slice      // the label is REQUIRED",
        "    full_adder u_fa (.a(a[i]), .b(b[i]), .cin(c[i]),",
        "                     .sum(sum[i]), .cout(c[i+1]));",
        "  end",
        "endgenerate",
        "",
        "// Instances are named bit_slice[0].u_fa, bit_slice[1].u_fa, ...",
        "// Use those names in $dumpvars and in timing constraints.",
    ], caption="Topic4_Lab/rtl/adder_gen.v")
    w.para([M("generate if"), N(" chooses between whole implementations at elaboration — a "
              "carry-lookahead adder when W is large and a ripple adder when it is not, for "
              "example. The unselected branch is not elaborated at all, so it need not even be "
              "legal for the chosen parameter values.")])

    # ---------------------------------------------------------- 1.14
    w.h2("1.14  Hierarchy and instantiation")
    w.image("hierarchy", 6.0, "A module is a type; an instance is a physical copy.")
    w.para("Two instances of the same module are two separate pieces of hardware that share "
           "nothing. Instantiate by name, always.")
    w.code([
        "// BY NAME -- do this. Order-independent, self-documenting, a typo is a compile error.",
        "uart_tx u_tx (",
        "    .clk   (clk),",
        "    .rst_n (rst_n),",
        "    .data  (tx_data),",
        "    .tx    (serial_out)",
        ");",
        "",
        "// BY POSITION -- do not. Add a port to the module and every instance silently",
        "// connects the wrong wires.",
        "uart_tx u_tx (clk, rst_n, tx_data, serial_out);",
    ], caption="Instantiation")
    w.bullets([
        [N("Prefix instance names with "), M("u_"), N(" so a reader can tell an instance from a "
                                                      "signal at a glance.")],
        [N("Write an intentionally unconnected port explicitly as "), M(".name()"),
         N(" so the reader can see it was deliberate.")],
        "Hierarchical references (tb.u_dut.state) are legal in a testbench and invaluable for "
        "white-box checks. Never use them in design code.",
    ])

    # ---------------------------------------------------------- 1.15
    w.h2("1.15  Compiler directives")
    w.table(["Directive", "What it does", "Note"],
            [["`timescale 1ns/1ps", "Sets the unit and precision of delays",
              "First line of every file: unit / precision"],
             ["`define NAME value", "Text macro, referenced as `NAME",
              "GLOBAL across the whole compilation — prefix names to avoid clashes"],
             ["`include \"file.vh\"", "Textual inclusion", "For shared parameter headers"],
             ["`ifdef / `ifndef / `else / `endif", "Conditional compilation",
              "Simulation-only code; ASIC vs FPGA variants"],
             ["`default_nettype none", "Turns off implicit wire creation",
              "Put it in EVERY file — see below"],
             ["`resetall", "Restores all directives to their defaults",
              "Pair it with the line above, at the end of the file"],
             ["`celldefine / `endcelldefine", "Marks a library cell",
              "You will see it in vendor libraries"]],
            widths=[1.9, 2.2, 2.5], size=9, align_center=False)
    w.callout("`default_nettype none is the single most valuable line in the file", [
        [N("By default, a name you never declared becomes a 1-bit wire, silently. Misspell "),
         M("data_valid"), N(" as "), M("data_vaild"),
         N(" in a port connection and Verilog creates a new, undriven 1-bit wire and says "
           "nothing. Your design gets an x and you spend an afternoon on it.")],
        [N("Put "), M("`default_nettype none"),
         N(" at the top of every file and that typo becomes a compile error naming the exact "
           "line. Every file in Topic4_Lab does this, and it costs one line.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 1.16
    w.h2("1.16  System tasks and functions")
    w.table(["Task", "Purpose", "Typical use"],
            [["$display / $write", "Print once, when reached",
              "$display(\"%0t got %h\", $time, q);"],
             ["$monitor", "Print whenever any argument changes",
              "One per simulation, inside initial"],
             ["$strobe", "Print at the end of the current time step",
              "Avoids seeing half-updated values"],
             ["$time / $realtime", "Current simulation time", "Timestamping messages"],
             ["$dumpfile / $dumpvars", "Write a VCD waveform file",
              "$dumpvars(0, tb); — 0 means all levels"],
             ["$finish / $stop", "End / pause the simulation",
              "$finish at the end of your stimulus"],
             ["$random / $urandom", "Pseudo-random stimulus",
              "Seed it, so a failure reproduces"],
             ["$fatal / $error / $warning", "Report, and optionally abort",
              "Self-checking testbenches"],
             ["$clog2(N)", "Ceiling log2 — SYNTHESISABLE",
              "localparam CW = $clog2(DEPTH);"],
             ["$bits(x)", "Width of an expression — SYNTHESISABLE",
              "Generic code that adapts to its input"],
             ["$readmemh / $readmemb", "Load a memory array from a file",
              "Initialising a ROM; supported by most FPGA flows"]],
            widths=[1.8, 2.2, 2.6], size=9, align_center=False)
    w.para([N("Format specifiers: "), M("%b %o %d %h"), N(" for radix, "), M("%s"),
            N(" for a string, "), M("%t"), N(" for time, "), M("%m"),
            N(" for the hierarchical module name. Prefix the width with 0 — "), M("%0d"),
            N(" — to suppress the padding that otherwise makes output unreadable.")])

    # ---------------------------------------------------------- 1.17
    w.h2("1.17  The synthesisable subset")
    w.image("synth_subset", 6.2, "The boundary between a design and a testbench.")
    w.para("Verilog is a simulation language that happens to have a synthesisable subset. Write "
           "something outside it and the simulation may run perfectly while the synthesiser either "
           "rejects it or, worse, quietly ignores it — producing hardware that does not match your "
           "simulation.")
    w.table(["Synthesisable", "Not synthesisable"],
            [["assign, always @(*), always @(posedge clk)", "initial blocks"],
             ["if / else, case, casez", "casex (legal, but banned by every standard)"],
             ["for and repeat with constant bounds", "while, forever, and data-dependent loops"],
             ["Functions without time control", "Tasks with time control"],
             ["parameter, localparam, generate", "Delays (#5) — ignored by synthesis"],
             ["Concatenation, replication, part-selects", "real, time, event data types"],
             ["$clog2, $bits", "$display, $monitor, $random, file I/O"],
             ["Arrays, for memory inference", "Force / release, hierarchical references"]],
            widths=[3.3, 3.3], size=9.5, align_center=False)
    w.h3("The four that catch people out")
    w.numbered([
        "Delays. #5 is ignored by synthesis. Timing comes from the clock and the technology "
        "library, never from your source code. A design that 'works' only because of a delay in "
        "the RTL will fail on silicon.",
        "initial blocks. FPGA tools honour them for register power-up values; ASIC tools do not. "
        "Reset your registers with a reset signal, always.",
        "Multiple always blocks driving one signal. Illegal. One signal, one driving block, no "
        "exceptions.",
        "Mixing = and <= for the same variable. Legal Verilog, undefined behaviour in practice, "
        "and rejected by every lint tool.",
    ])

    # ---------------------------------------------------------- 1.18
    w.h2("1.18  Coding standard for this course")
    w.numbered([
        "One file, one module, and the file is named after the module.",
        "`default_nettype none at the top; `resetall at the bottom.",
        "ANSI port headers. Instantiate by name. Prefix instances with u_.",
        "Active-low signals end in _n (rst_n). Clocks are named clk.",
        "Size every literal. Never write a bare 0 or 1 into a vector.",
        "Combinational logic: always @(*) with = and a default assignment at the top of the block.",
        "Sequential logic: always @(posedge clk) with <= only.",
        "Every case has a default. Never casex. Never full_case or parallel_case.",
        "One driver per signal. Reset every state-holding register.",
        "Lint before you simulate; simulate before you synthesise; read the synthesis log for "
        "inferred latches every single time.",
    ])
    w.callout("Why the log matters more than the waveform",
              ["A latch warning in the synthesis log is telling you that the hardware does not "
               "match your intent. The simulation will often pass anyway, because in simulation "
               "the latch happens to hold the value you expected. The mismatch appears on "
               "silicon, months later, in somebody else's lab. Read the log."],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ============================================================ PART 2
    w.page_break()
    w.h1("Part 2 · Modelling Combinational and Sequential Logic")
    w.para([N("Part 1 was the language. Part 2 is the craft: for every construct, "),
            B("what hardware does it produce?"),
            N("  Synthesis is pattern matching — the tool reads your code, recognises a pattern "
              "and drops in the corresponding hardware. There is no intelligence in it, which is "
              "good news: the mapping is completely predictable once you know the patterns.")])

    # ---------------------------------------------------------- 2.1
    w.h2("2.1  The inference map")
    w.image("inference_map", 6.4, "Code pattern in, hardware out.")
    w.table(["You write", "You get", "Because"],
            [["assign y = a & b;", "An AND gate", "A continuous, combinational relationship"],
             ["always @(*) with every path assigned", "Combinational logic",
              "The output is a pure function of the inputs"],
             ["always @(*) with a path unassigned", "A LATCH",
              "The old value must be remembered on that path"],
             ["always @(posedge clk) q <= d;", "A D flip-flop",
              "The value is captured at an edge"],
             ["always @(posedge clk) with if(en)", "A flip-flop with a clock enable",
              "Capture only on some edges"],
             ["always @(posedge clk or negedge rst_n)", "A flip-flop with an async reset",
              "A second edge event forces a value"],
             ["mem[a] <= d; q <= mem[b]; in a clocked block", "A block RAM",
              "The registered read is the pattern the tool looks for"],
             ["A for loop with constant bounds", "N copies of the body", "Unrolled at elaboration"],
             ["A function call", "A copy of the function's logic per call site",
              "There is no run time to 'call' in"]],
            widths=[2.5, 1.9, 2.2], size=9, align_center=False)
    w.callout("The one question to ask of every line you write",
              [[B("“What does this become?”"),
                N("  If you cannot answer that for a line of your own RTL, you have written "
                  "something you do not understand and the tool will make its own choice. Nine "
                  "times out of ten that choice is a latch, an enormous multiplexer, or a "
                  "critical path you did not expect.")]],
              color=TEAL)

    # ---------------------------------------------------------- 2.2
    w.h2("2.2  Combinational modelling")
    w.para("Three styles, one circuit. They synthesise identically — the tool flattens all of them "
           "to the same boolean function before it optimises. Choose by readability.")
    w.code([
        "// Style 1 -- continuous assignment. Best for short expressions.",
        "assign y = sel ? b : a;",
        "",
        "// Style 2 -- always block with if/else.",
        "always @(*) begin",
        "  if (sel) y = b;",
        "  else     y = a;              // the else is what stops a latch",
        "end",
        "",
        "// Style 3 -- always block with case. Scales best beyond two choices.",
        "always @(*) begin",
        "  case (sel)",
        "    1'b0:    y = a;",
        "    default: y = b;            // default covers 1'b1, 1'bx and 1'bz",
        "  endcase",
        "end",
    ], caption="Three ways to write one multiplexer — Topic4_Lab/rtl/mux2.v uses style 1")

    # ---------------------------------------------------------- 2.3
    w.h2("2.3  Latch inference — the number one beginner bug")
    w.image("latch_inference", 6.0, "An unassigned path forces the tool to build memory.")
    w.para("If a combinational block does not assign a variable on every possible path, the "
           "variable must keep its old value when that path is taken. Keeping an old value is "
           "memory, and the only memory a level-sensitive block can produce is a transparent "
           "latch.")
    w.h3("Why a latch is bad news")
    w.bullets([
        "It is transparent while enabled — data flows straight through it — so it does not isolate "
        "one cycle from the next the way a flip-flop does.",
        "Static timing analysis of latch-based paths is far harder, and many FPGA and ASIC flows "
        "simply cannot close timing on them.",
        "It was almost certainly not what you meant, which means your design does something other "
        "than what you think it does.",
    ])
    w.h3("The two cures — use both")
    w.code([
        "// CURE 1 -- default assignment at the top, then override.",
        "always @(*) begin",
        "  y = 1'b0;                     // default: y is ALWAYS assigned",
        "  w = d[0];",
        "  if (enable) y = d[0];",
        "  case (sel)",
        "    2'b00: w = d[0];",
        "    2'b01: w = d[1];",
        "    2'b10: w = d[2];",
        "    default: ;                  // nothing needed: the default at the top covers it",
        "  endcase",
        "end",
        "",
        "// CURE 2 -- complete every branch explicitly.",
        "always @(*) begin",
        "  if (enable) y = d[0];",
        "  else        y = 1'b0;         // every if has an else",
        "  case (sel)",
        "    2'b00: w = d[0];  2'b01: w = d[1];",
        "    2'b10: w = d[2];  default: w = 1'b0;    // every case has a default",
        "  endcase",
        "end",
    ], caption="Both forms remove both latches")
    w.h3("Seeing it in a real tool report")
    w.code([
        "$ yosys -p \"read_verilog rtl/broken_examples.v; synth -top bad_latch; stat\"",
        "",
        "     $_DLATCH_N_    1",
        "     $_DLATCH_P_    1              <-- two latches, exactly as predicted",
    ], caption="Verified output — Topic4_Lab, run it yourself")
    w.para("Now add the else and the default, re-run the same command, and the two DLATCH lines "
           "vanish. That before-and-after is the exercise; reading about it is not.")

    # ---------------------------------------------------------- 2.4
    w.h2("2.4  case as multiplexer, decoder and encoder")
    w.image("case_to_mux", 6.2, "One construct, three familiar building blocks.")
    w.code([
        "// DECODER -- a variable INDEX on the left-hand side. Topic4_Lab/rtl/decoder3to8.v",
        "always @(*) begin",
        "  y = 8'b0;",
        "  if (en) y[sel] = 1'b1;",
        "end",
        "",
        "// PRIORITY ENCODER -- casez. Topic4_Lab/rtl/priority_encoder8.v",
        "always @(*) begin",
        "  casez (req)",
        "    8'b1???????: {valid, y} = {1'b1, 3'd7};",
        "    8'b01??????: {valid, y} = {1'b1, 3'd6};",
        "    8'b001?????: {valid, y} = {1'b1, 3'd5};",
        "    // ...",
        "    default:     {valid, y} = {1'b0, 3'd0};",
        "  endcase",
        "end",
    ], caption="Decoder and priority encoder")
    w.para("The valid bit matters: without it you cannot tell 'request 0 is active' from 'no "
           "request at all', because both produce y = 0.")

    # ---------------------------------------------------------- 2.5
    w.h2("2.5  Worked example — an ALU with real flags")
    w.code([
        "wire [W:0] sum_ext  = {1'b0, a} + {1'b0, b};    // ONE bit wider -> carry is free",
        "wire [W:0] diff_ext = {1'b0, a} - {1'b0, b};",
        "",
        "always @(*) begin",
        "  result = {W{1'b0}};  carry = 1'b0;  overflow = 1'b0;      // defaults -> no latch",
        "  case (op)",
        "    OP_ADD: begin",
        "      result   = sum_ext[W-1:0];",
        "      carry    = sum_ext[W];",
        "      overflow = (a[W-1] == b[W-1]) && (result[W-1] != a[W-1]);",
        "    end",
        "    OP_SUB: begin",
        "      result   = diff_ext[W-1:0];",
        "      carry    = diff_ext[W];                    // borrow",
        "      overflow = (a[W-1] != b[W-1]) && (result[W-1] != a[W-1]);",
        "    end",
        "    OP_AND: result = a & b;",
        "    OP_OR : result = a | b;",
        "    OP_XOR: result = a ^ b;",
        "    OP_SLL: result = a << b[$clog2(W)-1:0];",
        "    OP_SRL: result = a >> b[$clog2(W)-1:0];",
        "    OP_SLT: result = ($signed(a) < $signed(b)) ? {{(W-1){1'b0}}, 1'b1} : {W{1'b0}};",
        "    default: begin result = {W{1'b0}}; carry = 1'b0; overflow = 1'b0; end",
        "  endcase",
        "end",
        "",
        "assign zero     = ~|result;      // reduction NOR: one operator, a whole NOR tree",
        "assign negative = result[W-1];",
    ], caption="Topic4_Lab/rtl/alu.v")
    w.callout("Carry is not overflow", [
        [B("C is unsigned overflow; V is signed overflow."), N("  They are different questions "
           "about the same addition, and confusing them is a classic exam and interview trap.")],
        [M("8'h7F + 8'h01 = 8'h80"), N("  — no carry out at all, but a SIGNED overflow: "
                                       "127 + 1 became −128.")],
        [M("8'hFF + 8'h01 = 8'h00"), N("  — carry out is set, but NO signed overflow: "
                                       "−1 + 1 = 0 is correct.")],
        [N("The rule for addition: V is set when the two operands have the SAME sign and the "
           "result has a different one. For subtraction: when the operands have DIFFERENT signs "
           "and the result differs from the first operand.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 2.6
    w.h2("2.6  The clocked block")
    w.image("seq_template", 5.8, "One template, used everywhere.")
    w.code([
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)      q <= RESET_VALUE;      // asynchronous, active-low reset",
        "  else if (clr)    q <= {W{1'b0}};        // synchronous clear",
        "  else if (load)   q <= din;              // then load",
        "  else if (en)     q <= next_value;       // then enable",
        "end",
    ], caption="The sequential template — priority runs top to bottom")
    w.para("Everything assigned in this block becomes a flip-flop. Nothing else in the design may "
           "assign q: one signal, one driving block, no exceptions. The order of the else-if chain "
           "IS the priority of the control signals, and it is a design decision you should make "
           "consciously.")

    # ---------------------------------------------------------- 2.7
    w.h2("2.7  Blocking and non-blocking assignment")
    w.image("blocking_nonblocking", 6.0, "Two operators, two very different circuits.")
    w.callout("The rule, in two lines",
              [[N("Inside "), M("always @(*)"), N(" use "), M("="), N(".  Inside "),
                M("always @(posedge clk)"), N(" use "), M("<="),
                N(".  Never mix the two for the same variable, and never use = in a clocked "
                  "block.")]],
              color=RED, fill="FDECEF", bar="C01F43")
    w.table(["", "Blocking  =", "Non-blocking  <="],
            [["When the update happens", "Immediately, before the next statement",
              "At the end of the time step, after every RHS is sampled"],
             ["Reads see", "The value just written", "The value from before the edge"],
             ["Statement order matters?", "Yes", "No"],
             ["Models", "Combinational logic", "A bank of flip-flops"],
             ["Use in", "always @(*)", "always @(posedge clk)"]],
            widths=[1.8, 2.4, 2.4], size=9, align_center=False)
    w.h3("The evidence")
    w.code([
        "// WRONG                                  // RIGHT",
        "always @(posedge clk) begin                always @(posedge clk) begin",
        "  q1 = d;                                    q1 <= d;",
        "  q2 = q1;   // q1 is ALREADY d              q2 <= q1;   // the OLD q1",
        "end                                        end",
        "",
        "$ yosys -p \"read_verilog rtl/broken_examples.v; synth -top bad_blocking; stat\"",
        "     $_DFF_P_       1              <-- ONE flip-flop, not two. Verified.",
    ], caption="A three-line difference that halves the hardware")
    w.para("q2 follows d in the same cycle, so the tool sees two registers holding the same value "
           "and keeps one. Change the two = to <= and the same command reports 2. Nothing else in "
           "the file changes.")
    w.para([B("And if you swap the two lines?"), N("  Write "), M("q2 = q1; q1 = d;"),
            N(" and you get two flip-flops and correct behaviour — from the same operator. That "
              "is the real objection to blocking assignment in a clocked block: the hardware "
              "depends on the ORDER you typed the lines, which is not a property that real "
              "flip-flops have.")])

    # ---------------------------------------------------------- 2.8
    w.h2("2.8  The stratified event queue — why <= actually works")
    w.image("event_queue", 6.2, "Regions within one simulation time step.")
    w.para("At a single simulation time step the simulator processes events in defined regions, in "
           "order. This is what the Verilog standard calls the stratified event queue.")
    w.table(["Region", "What happens there"],
            [["Active", "Blocking assignments; evaluation of every non-blocking RHS; "
                        "continuous assignments; $display"],
             ["Inactive", "Anything explicitly scheduled with #0 (avoid using this)"],
             ["NBA", "Non-blocking assignments are APPLIED to their left-hand sides"],
             ["Monitor", "$monitor and $strobe — after everything has settled"]],
            widths=[1.3, 5.1], size=9.5, align_center=False)
    w.para("Every clocked block in the design samples its inputs in the Active region, using the "
           "values that existed before the edge; every register updates in the NBA region "
           "afterwards. So no clocked block can see another block's new value within the same "
           "edge — which is precisely the behaviour of real flip-flops, and why the order in which "
           "the simulator happens to visit your always blocks cannot change the answer. Use = in a "
           "clocked block and you throw that guarantee away.")

    # ---------------------------------------------------------- 2.9
    w.h2("2.9  Reset strategy")
    w.table(["", "Asynchronous reset", "Synchronous reset"],
            [["Written as", "@(posedge clk or negedge rst_n)", "@(posedge clk)"],
             ["Works with no clock", "Yes — safe at power-up", "No"],
             ["Cost", "Uses the flip-flop's dedicated reset pin",
              "Adds logic in front of the D input"],
             ["Timing", "Release must be synchronised", "One clock domain, easy"],
             ["Glitch shorter than a cycle", "Is captured — may be good or bad", "Is ignored"]],
            widths=[1.8, 2.4, 2.4], size=9, align_center=False)
    w.h3("The reset-release synchroniser")
    w.para("An asynchronous reset asserts instantly, which is what you want. Its release, however, "
           "can occur arbitrarily close to a clock edge, so different flip-flops can leave reset "
           "on different cycles — and one of them can go metastable. The standard solution is to "
           "assert asynchronously and release synchronously:")
    w.code([
        "reg [1:0] rst_sync;",
        "always @(posedge clk or negedge rst_n_in) begin",
        "  if (!rst_n_in) rst_sync <= 2'b00;              // asserts immediately",
        "  else           rst_sync <= {rst_sync[0], 1'b1};// releases on a clock edge",
        "end",
        "wire rst_n = rst_sync[1];      // drive the whole design from THIS",
    ], caption="Assert asynchronously, release synchronously — two flip-flops")
    w.para("Whichever style you choose, be consistent across a whole clock domain. Mixing styles "
           "gives you blocks that leave reset on different cycles and a system that starts in a "
           "state your simulation never produced.")

    # ---------------------------------------------------------- 2.10
    w.h2("2.10  Counters, shift registers and edge detection")
    w.code([
        "// COUNTER -- a register plus an incrementer.  Topic4_Lab/rtl/counter.v",
        "assign tc = en & (up ? (q == MAX[W-1:0]) : (q == {W{1'b0}}));",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)      q <= {W{1'b0}};",
        "  else if (load)   q <= din;",
        "  else if (en) begin",
        "    if (up)  q <= (q == MAX[W-1:0]) ? {W{1'b0}}  : q + 1'b1;",
        "    else     q <= (q == {W{1'b0}})  ? MAX[W-1:0] : q - 1'b1;",
        "  end",
        "end",
        "",
        "$ yosys -p \"read_verilog rtl/counter.v; synth -top counter; stat\"",
        "   Number of cells:  38        $_DFF_NP0_  4      <-- 4 bits of state, as predicted",
    ], caption="Parameterised counter, verified")
    w.para([N("Set "), M("MAX = 9"), N(" and the same source is a BCD decade counter. Chain two, "
              "using the first's "), M("tc"),
            N(" as the second's enable, and you have a 0–99 counter. That is what "
              "parameterisation buys you.")])
    w.code([
        "// SHIFT REGISTER -- the concatenation idiom.",
        "always @(posedge clk or negedge rst_n)",
        "  if (!rst_n)  q <= {W{1'b0}};",
        "  else if (en) q <= {q[W-2:0], sin};      // left shift, new bit in at the bottom",
        "",
        "// EDGE DETECTOR -- one register and a gate.  Topic4_Lab/rtl/edge_detect.v",
        "always @(posedge clk or negedge rst_n)",
        "  if (!rst_n) sig_d <= 1'b0;",
        "  else        sig_d <= sig;",
        "",
        "assign rise = sig & ~sig_d;      // high for exactly one clock cycle",
        "assign fall = ~sig & sig_d;",
        "assign any  = sig ^ sig_d;",
    ], caption="Two modules you will use in almost every design")
    w.callout("A testbench lesson from building this lab", [
        [N("The first edge-detector test failed. The cause was not the design: the testbench "
           "changed the input in the middle of a clock cycle, so the pulse was half a cycle wide "
           "and the check sampled it at the wrong moment.")],
        [B("Drive stimulus just AFTER the active clock edge, and sample just BEFORE the next one."),
         N("  Half of all 'the design is broken' reports are really this.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 2.11
    w.h2("2.11  Clock domain crossing and metastability")
    w.para("A flip-flop needs its D input stable for a setup time before the clock edge and a hold "
           "time after it. A signal arriving from another clock domain cannot honour that, so the "
           "flip-flop can enter a metastable state: an output that is neither 0 nor 1 and settles "
           "at an unpredictable moment. You cannot prevent metastability. You can only give it "
           "time to decay, which is what a synchroniser does.")
    w.code([
        "reg [1:0] sync;",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n) sync <= 2'b00;",
        "  else        sync <= {sync[0], async_in};   // stage 0 may go metastable ...",
        "end",
        "assign sync_out = sync[1];                   // ... stage 1 has a whole cycle to settle",
    ], caption="Topic4_Lab/rtl/synchroniser.v")
    w.bullets([
        "Two flip-flops minimum for a single-bit LEVEL signal. Three at very high clock rates.",
        [B("Never synchronise a multi-bit bus bit by bit."),
         N("  The bits will arrive on different cycles and you will read a value that never "
           "existed on the source side.")],
        "For a bus, use Gray-coded pointers — only one bit changes per step, so a mis-sample "
        "returns the previous value, which is safe. That is exactly how an asynchronous FIFO "
        "works.",
        "Or use a request/acknowledge handshake, holding the data stable throughout.",
        "A pulse in a fast domain can be missed entirely by a slow one. Convert it to a level, "
        "cross it, and convert it back — or use a handshake.",
    ])

    # ---------------------------------------------------------- 2.12
    w.h2("2.12  State machines")
    w.image("fsm_styles", 6.2, "One, two or three always blocks.")
    w.table(["Style", "Blocks", "Pros", "Cons"],
            [["One-block", "1 clocked", "Compact; outputs registered automatically",
              "Next-state and output logic tangled together"],
             ["Two-block", "1 clocked + 1 combinational", "State and logic clearly separated",
              "Outputs still mixed into the combinational block"],
             ["Three-block", "1 clocked + 2 combinational",
              "State, next-state and output each separate — easiest to read and review",
              "Slightly more typing; that is the whole cost"]],
            widths=[1.2, 1.6, 2.2, 2.0], size=9, align_center=False)
    w.h3("The three-block template")
    w.code([
        "// ---- BLOCK 1 : state register (and any dwell timer) ----",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)    begin state <= MAIN_GREEN; timer <= 8'd0; end",
        "  else if (tick) begin",
        "    if (done)    begin state <= next; timer <= 8'd0; end",
        "    else               timer <= timer + 1'b1;",
        "  end",
        "end",
        "",
        "// ---- BLOCK 2 : next-state logic (pure combinational) ----",
        "always @(*) begin",
        "  next = state;                        // default -> no latch, and a safe self-loop",
        "  case (state)",
        "    MAIN_GREEN : next = MAIN_YELLOW;",
        "    MAIN_YELLOW: next = SIDE_GREEN;",
        "    SIDE_GREEN : next = SIDE_YELLOW;",
        "    SIDE_YELLOW: next = MAIN_GREEN;",
        "    default    : next = MAIN_GREEN;    // SAFE FSM -- recover from an illegal state",
        "  endcase",
        "end",
        "",
        "// ---- BLOCK 3 : output logic (Moore -- depends on state ONLY) ----",
        "always @(*) begin",
        "  main_light = RED;  side_light = RED;                    // defaults",
        "  case (state)",
        "    MAIN_GREEN : begin main_light = GREEN;  side_light = RED;    end",
        "    MAIN_YELLOW: begin main_light = YELLOW; side_light = RED;    end",
        "    SIDE_GREEN : begin main_light = RED;    side_light = GREEN;  end",
        "    SIDE_YELLOW: begin main_light = RED;    side_light = YELLOW; end",
        "    default    : begin main_light = RED;    side_light = RED;    end",
        "  endcase",
        "end",
    ], caption="Topic4_Lab/rtl/traffic_fsm.v — verified 52 cells, 12 flip-flops")
    w.para("Twelve flip-flops: two for the state, eight for the timer, and two more the tool kept "
           "for the outputs. Predicting that number before you run the tool is the skill being "
           "trained.")

    w.h3("Encoding")
    w.table(["Encoding", "Flip-flops for N states", "Logic depth", "Best for"],
            [["Binary", "ceil(log2 N)", "Deeper", "ASIC, where flip-flops cost area"],
             ["Gray", "ceil(log2 N)", "Deeper", "Pointers that cross clock domains"],
             ["One-hot", "N", "Very shallow", "FPGA, where flip-flops are plentiful"]],
            widths=[1.3, 1.9, 1.3, 2.1], size=9.5, align_center=False)
    w.code([
        "(* fsm_encoding = \"one-hot\" *) reg [1:0] state, next;      // or \"binary\"",
        "",
        "// Verified with Yosys 0.33 on a 4-state FSM, after abc -g AND,OR,XOR,NAND,NOR:",
        "//   binary   :  9 cells,  2 flip-flops",
        "//   one-hot  :  9 cells,  4 flip-flops    <-- more FFs, shallower next-state logic",
        "",
        "// On a machine this small the cell counts TIE. The one-hot advantage appears when",
        "// the state count grows and the next-state decode would otherwise get deep.",
        "// Do not assume -- measure.",
    ], caption="Asking for an encoding")
    w.callout("The tool may re-encode your FSM without being asked",
              [[N("Synthesising Topic4_Lab/rtl/traffic_fsm.v with plain "), M("synth"),
                N(" gives 12 flip-flops. Eight of them are the timer. The other FOUR are the "
                  "state — even though the source declares "), M("reg [1:0] state"),
                N(". The log says why:")],
               [M("FSM_RECODE: mapping auto encoding to `one-hot` for this FSM")],
               [N("The tool detected a state machine, extracted it and chose its own encoding. "
                  "That is a perfectly good decision, and it is invisible unless you read the "
                  "log. This is why a flip-flop count that disagrees with your prediction is "
                  "worth ten minutes: sometimes you are wrong, and sometimes the tool did "
                  "something reasonable that you did not know about.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    w.h3("Moore and Mealy")
    w.table(["", "Moore", "Mealy"],
            [["Output is a function of", "State only", "State and inputs"],
             ["Reacts to an input", "One clock later", "In the same cycle"],
             ["Output glitches?", "No — it is registered", "Yes — it follows the input"],
             ["Typical state count", "More", "Fewer"],
             ["Safe to drive off-chip?", "Yes", "Not without registering it first"],
             ["Use when", "You want clean, predictable outputs",
              "You need the earliest possible response"]],
            widths=[2.1, 2.2, 2.2], size=9, align_center=False)
    w.para([N("Topic4_Lab/rtl/seq_detect_1011.v implements both in one module so you can compare "
              "the two "), M("found"),
            N(" outputs on the same waveform. Overlapping detection is handled by returning to "
              "the correct PARTIAL-match state rather than to IDLE — the sequence 1011011 "
              "contains two matches, not one.")])

    # ---------------------------------------------------------- 2.13
    w.h2("2.13  Memory inference")
    w.image("memory_inference", 5.8, "Write the pattern the tool is looking for.")
    w.code([
        "reg [W-1:0] mem [0:DEPTH-1];",
        "",
        "always @(posedge clk) begin",
        "  if (we) mem[waddr] <= wdata;",
        "  rdata <= mem[raddr];          // REGISTERED read -- this is what infers block RAM",
        "end",
    ], caption="Topic4_Lab/rtl/sync_ram.v — synchronous read")
    w.para([N("Write "), M("assign rdata = mem[raddr];"),
            N(" instead — an asynchronous read — and no FPGA block RAM can implement it, so the "
              "tool builds the whole array out of flip-flops and multiplexers. A 1 K × 8 memory "
              "that would have been one block RAM becomes 8192 flip-flops and an enormous "
              "multiplexer, and the design very likely will not fit. Same intent, wildly "
              "different silicon.")])
    w.bullets([
        "Do not reset a large memory array. There is no reset on a block RAM, so a reset forces "
        "the tool to build registers instead.",
        "Read-during-write behaviour (does a read at the same address on the same cycle return the "
        "old or the new data?) differs between technologies. If it matters, write it explicitly.",
        [M("$readmemh(\"init.hex\", mem);"), N(" inside an initial block initialises a ROM and is "
           "supported by most FPGA flows — one of the few places initial is acceptable in design "
           "code.")],
    ])

    # ---------------------------------------------------------- 2.14
    w.h2("2.14  Pipelining")
    w.image("pipelining", 6.2, "Cut a long path in half; pay one cycle of latency.")
    w.para("The clock period must be longer than the slowest combinational path between two "
           "flip-flops. If that path is too slow, insert a register in the middle. You now need "
           "two cycles to get an answer — but you can start a new one every cycle.")
    w.table(["", "Effect"],
            [["Throughput", "One result per clock, at a much higher clock frequency"],
             ["Latency", "The first result arrives N cycles later"],
             ["Area", "The pipeline registers, plus any control signal that must be delayed "
                      "to stay aligned with its data"]],
            widths=[1.3, 5.1], size=9.5, align_center=False)
    w.callout("The pipelining trap",
              [[B("Every signal travelling alongside the data must be delayed by the SAME number "
                  "of stages."),
                N("  Pipeline the datapath and forget the valid bit, and your results arrive "
                  "correctly but are marked valid two cycles early. Carry valid — and any tag, "
                  "address or ID — through an identical register chain.")]],
              color=RED, fill="FDECEF", bar="C01F43")
