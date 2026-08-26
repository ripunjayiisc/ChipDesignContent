# -*- coding: utf-8 -*-
"""Topic 4 deck — 4A continued: procedural blocks, control flow, reuse, directives, subset."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def C(t, **kw):
    d = {"t": t}
    d.update(kw)
    return [d]


def build(d):
    # ============================================================ three constructs
    s = d.slide("TOPIC 4A · CONSTRUCTS", "The Three Ways to Describe Logic")
    y = d.lead(s, TOP, [[
        R("Everything synthesisable in Verilog is written with one of three constructs. ",
          b=True, c=NAVY, s=12.5),
        R("Learn what each one BECOMES and you can already read most RTL. The rest of subtopic "
          "4b is simply the detail of using them correctly.")]], h=548640)
    y = d.image(s, y + 45720, "three_constructs", 3383280)
    d.table(s, y + G,
            ["Construct", "Written as", "Becomes", "Use it for"],
            [["Continuous assignment", "assign y = ...;", "A cloud of gates", "Short combinational expressions"],
             ["Combinational block", "always @(*) ... = ...", "A cloud of gates", "Longer logic: case, if/else chains"],
             ["Clocked block", "always @(posedge clk) ... <= ...", "Flip-flops + gates", "Anything that must remember"]],
            [2560320, 3200400, 2011680, 3474720], rh=283464, bold_cols=(0,), size=10)

    # ============================================================ assign
    s = d.slide("TOPIC 4A · CONTINUOUS ASSIGN", "assign — Wiring, Not Instruction")
    y = d.lead(s, TOP, [[
        R("An assign statement is a permanent connection. ", b=True, c=NAVY, s=12.5),
        R("It is not executed once — it is ALWAYS true. Whenever anything on the right-hand side "
          "changes, the left-hand side follows, in zero simulation time. Think of it as solder, "
          "not as a line of a program.")]], h=594360)
    y = d.code(s, y + 45720, [
        C("// The right-hand side is re-evaluated whenever ANY of a, b, sel, cin changes.", c=RGBColor(0x7F,0x9C,0xB5)),
        "assign y     = a & b;                 // one AND gate",
        "assign z     = sel ? p : q;           // a 2:1 multiplexer",
        "assign {co, sum} = a + b + cin;       // a 9-bit result split into carry and sum",
        "assign parity    = ^data;             // an XOR tree",
        "assign any_req   = |req;              // an OR tree",
        "",
        C("// Order does not matter. These three lines describe the same circuit", c=RGBColor(0x7F,0x9C,0xB5)),
        C("// no matter which order you type them in — because they are wires.", c=RGBColor(0x7F,0x9C,0xB5)),
        "assign c = a ^ b;",
        "assign e = c & d;",
        "assign d = ~a;",
    ], size=10.5, title="Continuous assignments — order-independent, always live")
    d.cols(s, y + G, [
        ("Rules",
         [[R("· The left side must be a ", s=10.5), R("wire", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" (net), never a reg.", s=10.5)],
          [R("· A wire may be driven by only ONE assign. Two drivers give x.", s=10.5)],
          [R("· No if/case/for — expressions only. Use ?: for choices.", s=10.5)]], TEAL, CARD),
        ("When to reach for it",
         [[R("Use assign for anything that fits comfortably on one line and has no choice "
             "structure. The moment you find yourself nesting three conditional operators, stop "
             "and rewrite it as an ", s=10.5),
           R("always @(*)", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R(" block with a case statement — it will be far easier to read and reviews better.",
             s=10.5)]], GREEN, CARD_G)], h=1325880)

    # ============================================================ procedural blocks
    s = d.slide("TOPIC 4A · PROCEDURAL BLOCKS", "initial and always — and What a Sensitivity List Means")
    y = d.lead(s, TOP, [[
        R("A procedural block contains statements that run in order, inside the block. ",
          b=True, c=NAVY, s=12.5),
        R("The block itself is triggered by its sensitivity list. Blocks run CONCURRENTLY with "
          "each other; statements run SEQUENTIALLY within one block.")]], h=548640)
    y = d.code(s, y + 45720, [
        "always @(*)          begin ... end   // re-runs whenever any input changes  -> combinational",
        "always @(posedge clk) begin ... end   // runs once per rising clock edge      -> flip-flops",
        "always @(posedge clk or negedge rst_n) // adds an ASYNCHRONOUS reset",
        "",
        "initial              begin ... end   // runs ONCE at time 0 -- SIMULATION ONLY",
        "always               begin ... end   // runs forever -- used for clock generation in a TB",
    ], size=10.5, title="The forms you will meet")
    y = d.tiers(s, y + G, [
        ("@(*)", "Automatic sensitivity: the tool works out every signal READ inside the block "
                 "and triggers on all of them. Always use this form for combinational logic — a "
                 "hand-written list such as @(a or b) is a bug waiting to happen the day someone "
                 "adds a signal to the expression and forgets the list.", TEAL),
        ("@(posedge clk)", "Edge sensitivity: the block runs at the instant the clock rises, and "
                           "at no other time. Everything assigned with <= inside becomes a "
                           "flip-flop clocked by clk.", GREEN),
        ("initial", "Runs once at time zero. There is no hardware equivalent of 'do this once at "
                    "time zero' in ASIC logic, so initial is for testbenches. (FPGA tools DO honour "
                    "initial for register power-up values; ASIC tools do not — never rely on it.)",
         AMBER)], h=822960, gap=45720)

    # ============================================================ if / else
    s = d.slide("TOPIC 4A · CONTROL FLOW", "if / else — a Priority Structure in Hardware")
    y = d.lead(s, TOP, [[
        R("An if/else chain does not 'test conditions one after another'. ", b=True, c=NAVY, s=12.5),
        R("It synthesises to a chain of multiplexers in which the FIRST condition has the highest "
          "priority. That chain has depth — and depth is delay.")]], h=548640)
    y = d.cols(s, y + 45720, [
        ("Priority — deep, slow, sometimes required",
         [[R("if (a) y = 0;", f=MONO_FONT, s=10)],
          [R("else if (b) y = 1;", f=MONO_FONT, s=10)],
          [R("else if (c) y = 2;", f=MONO_FONT, s=10)],
          [R("else        y = 3;", f=MONO_FONT, s=10)],
          [R("Three multiplexers in series. Use it when the conditions really do overlap and one "
             "must win — an interrupt controller, a bus arbiter.", s=10, c=SLATE)]], AMBER, CARD_A),
        ("Parallel — shallow, fast",
         [[R("case (sel)", f=MONO_FONT, s=10)],
          [R("  2'd0: y = 0;   2'd1: y = 1;", f=MONO_FONT, s=10)],
          [R("  2'd2: y = 2;   2'd3: y = 3;", f=MONO_FONT, s=10)],
          [R("endcase", f=MONO_FONT, s=10)],
          [R("One multiplexer. Use it when the conditions are mutually exclusive — which they "
             "usually are.", s=10, c=SLATE)]], GREEN, CARD_G)], h=1645920)
    d.card(s, y + G, "The rule that prevents accidental latches",
           [[R("Inside always @(*), every branch must assign every output. ", b=True, c=RED),
             R("If a path through the code leaves a variable unassigned, the synthesiser must "
               "build something that REMEMBERS the old value — a latch. Two ways to guarantee "
               "you never do this: (1) write a "),
             R("default assignment", b=True, c=GREEN),
             R(" at the top of the block, or (2) always write a final "),
             R("else", f=MONO_FONT, b=True, c=GREEN), R(" / "),
             R("default:", f=MONO_FONT, b=True, c=GREEN),
             R(". We come back to this in detail in 4b.")]],
           accent=RED, fill=CARD_R, h=1005840)

    # ============================================================ case
    s = d.slide("TOPIC 4A · CASE", "case, casez, casex — and Why casex Is Banned")
    y = d.lead(s, TOP, [[
        R("case compares the selector against each label using 4-state equality. ",
          b=True, c=NAVY, s=12.5),
        R("Its two wildcard variants let labels contain don't-cares — one of them safely, one of "
          "them not.")]], h=502920)
    y = d.code(s, y + 45720, [
        C("// case  -- exact match, including x and z. The workhorse.", c=RGBColor(0x7F,0x9C,0xB5)),
        "case (opcode)",
        "  4'b0000: y = a + b;",
        "  4'b0001: y = a - b;",
        "  default: y = 8'd0;        // ALWAYS write a default",
        "endcase",
        "",
        C("// casez -- ? and z in the LABEL are don't-care. Correct for priority encoders.", c=RGBColor(0x7F,0x9C,0xB5)),
        "casez (req)",
        "  4'b1???: grant = 2'd3;    // bit 3 set -- lower bits irrelevant",
        "  4'b01??: grant = 2'd2;",
        "  4'b001?: grant = 2'd1;",
        "  default: grant = 2'd0;",
        "endcase",
    ], size=10, title="case and casez")
    d.cols(s, y + G, [
        ("casex — do not use it",
         [[R("casex also treats an ", s=10.5), R("x in the SELECTOR", b=True, c=RED, s=10.5),
           R(" as a wildcard. During simulation an uninitialised signal will then match the FIRST "
             "label and appear to work, while the synthesised hardware behaves differently. It "
             "hides exactly the bug you most need to see. Most coding standards ban it outright.",
             s=10.5)]], RED, CARD_R),
        ("full_case / parallel_case",
         [[R("These synthesis pragmas promise the tool that all cases are covered / mutually "
             "exclusive. If the promise is false, ", s=10.5),
           R("simulation and synthesis silently disagree", b=True, c=RED, s=10.5),
           R(" — the hardest class of bug there is. Write a real default instead; it costs "
             "nothing and cannot lie.", s=10.5)]], AMBER, CARD_A)], h=1188720)

    # ============================================================ loops
    s = d.slide("TOPIC 4A · LOOPS", "for, while, repeat — Loops Are Unrolled, Not Executed")
    y = d.lead(s, TOP, [[
        R("A for loop in synthesisable Verilog is a copy-paste instruction to the tool. ",
          b=True, c=NAVY, s=12.5),
        R("It does not create a counter or take time. The tool duplicates the loop body once per "
          "iteration — so the bounds must be constants, and eight iterations means eight copies "
          "of the hardware.")]], h=594360)
    y = d.code(s, y + 45720, [
        "integer i;",
        "always @(*) begin",
        "  cnt = 4'd0;",
        "  for (i = 0; i < 8; i = i + 1)",
        "    cnt = cnt + data[i];        // becomes 8 adders in a tree -- NOT a loop in hardware",
        "end",
        "",
        C("// Reversing a bus -- 8 wires crossed over, zero gates, zero delay.", c=RGBColor(0x7F,0x9C,0xB5)),
        "always @(*)",
        "  for (i = 0; i < 8; i = i + 1) rev[i] = fwd[7-i];",
    ], size=10.5, title="Synthesisable loop — constant bounds")
    d.cols(s, y + G, [
        ("Synthesisable",
         [[R("for", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  with constant start, limit and step.", s=10.5)],
          [R("repeat (N)", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  with constant N — also unrolled.", s=10.5)],
          [R("Loop variable is ", s=10.5), R("integer", f=MONO_FONT, s=10.5),
           R(" or ", s=10.5), R("genvar", f=MONO_FONT, s=10.5),
           R(" — it does not exist in the hardware.", s=10.5)]], GREEN, CARD_G),
        ("Simulation only",
         [[R("while", f=MONO_FONT, b=True, c=RED, s=10.5),
           R(", ", s=10.5), R("forever", f=MONO_FONT, b=True, c=RED, s=10.5),
           R(", and any loop whose bound depends on a signal. The tool cannot know how many "
             "copies to make, so it refuses.", s=10.5)],
          [R("If you need 'repeat until a signal changes', that is a state machine or a counter — "
             "build it explicitly.", s=10.5, i=True, c=SLATE)]], RED, CARD_R)], h=1188720)

    # ============================================================ tasks & functions
    s = d.slide("TOPIC 4A · REUSE", "Functions and Tasks")
    y = d.lead(s, TOP, [[
        R("A function is a named expression; a task is a named block of statements. ",
          b=True, c=NAVY, s=12.5),
        R("A function that obeys the rules synthesises — into a duplicate copy of its logic at "
          "every call site. Tasks are, in practice, a testbench tool.")]], h=548640)
    y = d.code(s, y + 45720, [
        C("// FUNCTION -- synthesisable. No time control, at least one input, returns one value.", c=RGBColor(0x7F,0x9C,0xB5)),
        "function [3:0] bcd_digit;",
        "  input [7:0] v;",
        "  begin",
        "    bcd_digit = v % 10;        // the function name IS the return variable",
        "  end",
        "endfunction",
        "assign d0 = bcd_digit(count);  // one copy of the logic here ...",
        "assign d1 = bcd_digit(other);  // ... and a SECOND, independent copy here",
        C("// TASK -- may consume time, may have multiple outputs. Testbench use.", c=RGBColor(0x7F,0x9C,0xB5)),
        "task send_byte(input [7:0] b);",
        "  begin",
        "    tx_data = b; tx_start = 1'b1; @(posedge clk); tx_start = 1'b0;",
        "    wait (tx_busy == 1'b0);",
        "  end",
        "endtask",
    ], size=9.5, title="Function vs task")
    d.card(s, y + G, "The cost you must remember",
           [[R("A function call is not a subroutine call — there is no 'calling' at run time. "
               "Each call site gets its own physical copy of the logic. ", b=True, c=AMBER),
             R("Four calls to a 16-bit multiplier function means four multipliers on the die. If "
               "you want ONE shared unit used at different times, that is a datapath with a "
               "multiplexer in front of it and a controller — a design decision, not a syntax "
               "choice.")]],
           accent=AMBER, fill=CARD_A, h=960120)

    # ============================================================ parameters
    s = d.slide("TOPIC 4A · PARAMETERS", "Writing One Module That Fits Every Size")
    y = d.lead(s, TOP, [[
        R("A parameter is a constant that the instantiating module can override. ",
          b=True, c=NAVY, s=12.5),
        R("Parameterising is the difference between an 8-bit counter and a counter — between code "
          "you write once and code you copy and edit five times, introducing a bug in the "
          "fourth copy.")]], h=594360)
    y = d.image(s, y + 45720, "parameters", 2377440)
    y = d.code(s, y + G, [
        "module counter #(parameter integer W = 8, parameter [W-1:0] MAX = {W{1'b1}})",
        "  (input clk, rst_n, en, output reg [W-1:0] q, output wire tc);",
        "  localparam [W-1:0] ZERO = {W{1'b0}};   // localparam CANNOT be overridden",
        "  assign tc = en & (q == MAX);",
        "  ...",
        "endmodule",
        "",
        "counter #(.W(4), .MAX(4'd9)) u_dig0 (.clk(clk), .rst_n(rst_n), ...);  // a decade counter",
    ], size=9.5, title="Parameterised module and an override")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Use ", s=10.5), R("localparam", f=MONO_FONT, b=True, c=GREEN, s=10.5),
        R(" for anything derived or internal — state encodings, computed widths — so that a "
          "careless override cannot break the module's internal consistency. Use ", s=10.5),
        R("$clog2(N)", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" to compute the number of bits needed to count to N.", s=10.5)]])

    # ============================================================ generate
    s = d.slide("TOPIC 4A · GENERATE", "generate — Building Structure Out of a Loop")
    y = d.lead(s, TOP, [[
        R("generate lets a loop or an if create INSTANCES and blocks, not just logic. ",
          b=True, c=NAVY, s=12.5),
        R("It runs at elaboration time — before simulation starts — and its result is a fixed "
          "structure. This is how you build an N-bit ripple adder from one full-adder module.")]],
        h=594360)
    y = d.image(s, y + 45720, "generate_block", 2743200)
    y = d.code(s, y + G, [
        "genvar i;",
        "generate",
        "  for (i = 0; i < W; i = i + 1) begin : bit_slice     // the label is REQUIRED",
        "    full_adder u_fa (.a(a[i]), .b(b[i]), .cin(c[i]), .sum(sum[i]), .cout(c[i+1]));",
        "  end",
        "endgenerate",
        C("// Instances are named bit_slice[0].u_fa, bit_slice[1].u_fa, ... -- use these in $dumpvars", c=RGBColor(0x7F,0x9C,0xB5)),
    ], size=10, title="generate for — Topic4_Lab/rtl/adder_gen.v")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("generate if", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" selects between whole implementations at elaboration — for example a fast "
          "carry-lookahead adder when W is large and a small ripple adder when it is not. The "
          "unselected branch is not elaborated at all, so it need not even be legal for the "
          "chosen parameters.", s=10.5)]])

    # ============================================================ hierarchy
    s = d.slide("TOPIC 4A · HIERARCHY", "Instantiating Modules — Always By Name")
    y = d.lead(s, TOP, [[
        R("Real designs are trees of modules. ", b=True, c=NAVY, s=12.5),
        R("A module is a TYPE; an instance is a physical copy. Two instances of the same module "
          "are two separate pieces of hardware that share nothing.")]], h=548640)
    y = d.image(s, y + 45720, "hierarchy", 2560320)
    y = d.cols(s, y + G, [
        ("By name — do this",
         [[R("uart_tx u_tx (", f=MONO_FONT, s=10)],
          [R("  .clk    (clk),", f=MONO_FONT, s=10)],
          [R("  .rst_n  (rst_n),", f=MONO_FONT, s=10)],
          [R("  .data   (tx_data),", f=MONO_FONT, s=10)],
          [R("  .tx     (serial_out));", f=MONO_FONT, s=10)],
          [R("Order-independent, self-documenting, and a typo is a compile error.", s=10, c=SLATE)]],
         GREEN, CARD_G),
        ("By position — do not",
         [[R("uart_tx u_tx (clk, rst_n,", f=MONO_FONT, s=10)],
          [R("              tx_data, serial_out);", f=MONO_FONT, s=10)],
          [R("", s=10)],
          [R("Add a port to the module and every instance silently connects the wrong wires. "
             "Legal, common in old code, and a permanent source of accidents.", s=10, c=SLATE)]],
         RED, CARD_R)], h=1463040)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Naming convention used throughout this course: instances are prefixed ", s=10.5),
        R("u_", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R("; an unconnected output is written ", s=10.5),
        R(".name()", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" explicitly so a reader can see it was deliberate.", s=10.5)]])

    # ============================================================ directives
    s = d.slide("TOPIC 4A · DIRECTIVES", "Compiler Directives — the Backtick Family")
    y = d.lead(s, TOP, [[
        R("Directives are processed before compilation, like C's preprocessor. ",
          b=True, c=NAVY, s=12.5),
        R("They begin with a backtick, not a hash, and they are NOT terminated with a semicolon.")]],
        h=502920)
    y = d.table(s, y + 45720,
                ["Directive", "What it does", "Note"],
                [["`timescale 1ns/1ps", "Sets the unit and precision of delays",
                  "First line of every file; unit / precision"],
                 ["`define NAME value", "Text macro, referenced as `NAME", "GLOBAL — prefix to avoid clashes"],
                 ["`include \"file.vh\"", "Textual inclusion", "Use for shared parameter headers"],
                 ["`ifdef / `ifndef / `endif", "Conditional compilation", "Simulation-only code, ASIC vs FPGA"],
                 ["`default_nettype none", "Turns off implicit wire creation", "Put it in EVERY file. See below."],
                 ["`resetall", "Restores defaults", "Pair with the line above at end of file"]],
                [2926080, 4754880, 3566160], rh=283464, bold_cols=(0,), size=10,
                col_colors={0: NAVY})
    d.card(s, y + G, "`default_nettype none — the single most valuable line in the file", 
           [[R("By default, a name you never declared becomes a 1-bit wire, silently. Misspell "),
             R("data_valid", f=MONO_FONT, b=True, c=RED),
             R(" as "), R("data_vaild", f=MONO_FONT, b=True, c=RED),
             R(" in a port connection and Verilog creates a new, undriven 1-bit wire and says "
               "nothing; your design gets an x and you spend an afternoon on it.")],
            [R("Put "), R("`default_nettype none", f=MONO_FONT, b=True, c=GREEN),
             R(" at the top of every file and that typo becomes a compile error on the exact "
               "line. Every file in Topic4_Lab does this.")]],
           accent=GREEN, fill=CARD_G, h=1188720)

    # ============================================================ system tasks
    s = d.slide("TOPIC 4A · SYSTEM TASKS", "The Dollar Family — Your Simulation Instruments")
    y = d.lead(s, TOP, [[
        R("System tasks are built-in routines the SIMULATOR provides. ", b=True, c=NAVY, s=12.5),
        R("None of them synthesise — they are how you observe and control a simulation. Two of "
          "them ($clog2 and $bits) are exceptions that are legal in synthesisable code because "
          "they are evaluated at elaboration.")]], h=594360)
    y = d.table(s, y + 45720,
                ["Task", "Purpose", "Typical use"],
                [["$display / $write", "Print once, when reached", "$display(\"%0t got %h\", $time, q);"],
                 ["$monitor", "Print whenever any argument changes", "One per simulation, in initial"],
                 ["$time / $realtime", "Current simulation time", "Timestamping messages"],
                 ["$dumpfile / $dumpvars", "Write a VCD waveform file", "$dumpvars(0, tb); — 0 = all levels"],
                 ["$finish / $stop", "End / pause the simulation", "$finish at the end of your stimulus"],
                 ["$random / $urandom", "Pseudo-random stimulus", "Seed it so failures reproduce"],
                 ["$fatal / $error", "Report and optionally abort", "Self-checking testbenches"],
                 ["$clog2(N)", "Ceiling log2 — SYNTHESISABLE", "localparam CW = $clog2(DEPTH);"]],
                [2377440, 4023360, 4846320], rh=274320, bold_cols=(0,), size=10,
                col_colors={0: NAVY})
    d.text(s, ML, y + 45720, MW, 320040, [[
        R("Format specifiers: ", s=10.5), R("%b %o %d %h", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" for radix, ", s=10.5), R("%s", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" string, ", s=10.5), R("%t", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" time. Prefix with 0 — ", s=10.5), R("%0d", f=MONO_FONT, b=True, c=GREEN, s=10.5),
        R(" — to drop the padding that otherwise makes output unreadable.", s=10.5)]])

    # ============================================================ synth subset
    s = d.slide("TOPIC 4A · THE SUBSET", "What Synthesises, and What Does Not", AMBER)
    y = d.lead(s, TOP, [[
        R("This is the boundary that separates a design from a testbench. ", b=True, c=NAVY,
          s=12.5),
        R("Verilog is a simulation language that HAPPENS to have a synthesisable subset. If you "
          "write something outside it, the simulation may run perfectly and the synthesiser will "
          "either reject it or — worse — quietly ignore it.")]], h=594360)
    y = d.image(s, y + 45720, "synth_subset", 3200400)
    d.cols(s, y + G, [
        ("The four that catch people out",
         [[R("· Delays. ", b=True, c=RED, s=10.5),
           R("#5 is ignored by synthesis. Timing comes from the clock and the technology, never "
             "from your source.", s=10.5)],
          [R("· initial blocks. ", b=True, c=RED, s=10.5),
           R("Reset your registers with a reset signal.", s=10.5)]], RED, CARD_R),
        ("...continued",
         [[R("· Multiple always blocks driving one signal. ", b=True, c=RED, s=10.5),
           R("Illegal. One signal, one driver, one block.", s=10.5)],
          [R("· Mixing = and <= for the same variable. ", b=True, c=RED, s=10.5),
           R("Legal Verilog, undefined behaviour in practice, rejected by every lint tool.",
             s=10.5)]], RED, CARD_R)], h=1188720)

    # ============================================================ style
    s = d.slide("TOPIC 4A · STYLE", "House Rules — The Checklist Used in This Course")
    d.lead(s, TOP, [[
        R("Every rule below exists because breaking it has cost somebody a day. ", b=True,
          c=NAVY, s=12.5),
        R("They are the standing lint rules for all labs in Topic 4.")]], h=411480)
    y = 1600200
    y = d.bullets(s, y, [
        [R("One file, one module, and the file is named after the module.", s=11)],
        [R("`default_nettype none", f=MONO_FONT, b=True, c=NAVY, s=11),
         R(" at the top; ", s=11), R("`resetall", f=MONO_FONT, b=True, c=NAVY, s=11),
         R(" at the bottom.", s=11)],
        [R("ANSI port headers. Instantiate by name. Prefix instances with ", s=11),
         R("u_", f=MONO_FONT, b=True, c=NAVY, s=11), R(".", s=11)],
        [R("Active-low signals end in ", s=11), R("_n", f=MONO_FONT, b=True, c=NAVY, s=11),
         R("  (", s=11), R("rst_n", f=MONO_FONT, s=11),
         R("). Clocks are ", s=11), R("clk", f=MONO_FONT, s=11), R(".", s=11)],
        [R("Size every literal. Never write a bare 0 or 1 into a vector.", s=11)],
        [R("Combinational: ", s=11), R("always @(*)", f=MONO_FONT, b=True, c=GREEN, s=11),
         R(" with ", s=11), R("=", f=MONO_FONT, b=True, c=GREEN, s=11),
         R(" and a default assignment.  Sequential: ", s=11),
         R("always @(posedge clk)", f=MONO_FONT, b=True, c=GREEN, s=11),
         R(" with ", s=11), R("<=", f=MONO_FONT, b=True, c=GREEN, s=11), R(" only.", s=11)],
        [R("Every case has a ", s=11), R("default", f=MONO_FONT, b=True, c=NAVY, s=11),
         R(". Never casex. Never full_case/parallel_case.", s=11)],
        [R("One driver per signal. Reset every state-holding register.", s=11)],
        [R("Lint with Verilator before you simulate; simulate before you synthesise; check the "
           "synthesis log for inferred latches every single time.", s=11)],
    ], accent=TEAL, step=283464)
    d.card(s, y + G, "Why the log matters more than the waveform",
           [[R("A latch warning in the synthesis log is telling you the hardware does not match "
               "your intent. The simulation will often pass anyway, because in simulation the "
               "latch happens to hold the value you expected. The mismatch appears on silicon. "
               "Read the log.")]],
           accent=AMBER, fill=CARD_A, h=776224)

    # ============================================================ 4A checkpoint
    s = d.slide("TOPIC 4A · CHECKPOINT", "Before We Move On — Ten Questions")
    d.lead(s, TOP, [[
        R("Ask the room. Do not move to 4b until most of these come back quickly. ",
          b=True, c=NAVY, s=12.5),
        R("Answers are in the workbook, section T4-A.")]], h=411480)
    y = 1554480
    y = d.cols(s, y, [
        ("Questions 1–5",
         [[R("1. Is ", s=10.5), R("reg", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" a register? When is it, and when is it not?", s=10.5)],
          [R("2. What width and sign does the literal ", s=10.5),
           R("12", f=MONO_FONT, b=True, c=NAVY, s=10.5), R(" have?", s=10.5)],
          [R("3. What does ", s=10.5), R("{3{2'b10}}", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" evaluate to, and how wide is it?", s=10.5)],
          [R("4. Give one bit of output: ", s=10.5),
           R("^8'b1101_0110", f=MONO_FONT, b=True, c=NAVY, s=10.5), R(" = ?", s=10.5)],
          [R("5. Why is ", s=10.5), R("a && b", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" not the same as ", s=10.5), R("a & b", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R("?", s=10.5)]], TEAL, CARD),
        ("Questions 6–10",
         [[R("6. How many adders does an unrolled 8-iteration for loop create?", s=10.5)],
          [R("7. Name two things that make code un-synthesisable.", s=10.5)],
          [R("8. What is the difference between ", s=10.5),
           R("parameter", f=MONO_FONT, b=True, c=NAVY, s=10.5), R(" and ", s=10.5),
           R("localparam", f=MONO_FONT, b=True, c=NAVY, s=10.5), R("?", s=10.5)],
          [R("9. Why does every file start with ", s=10.5),
           R("`default_nettype none", f=MONO_FONT, b=True, c=NAVY, s=10.5), R("?", s=10.5)],
          [R("10. Why is casex banned?", s=10.5)]], GREEN, CARD_G)], h=2011680)
    d.card(s, y + G, "If question 1 or 5 gave the room trouble",
           [[R("Go back to slides 11 and 16 now rather than pressing on. Everything in 4b is "
               "built on knowing what a reg becomes and how wide an expression is; a class that "
               "is shaky on those two will not follow the latch discussion at all.")]],
           accent=AMBER, fill=CARD_A, h=776224)
