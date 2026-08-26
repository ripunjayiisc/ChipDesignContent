# -*- coding: utf-8 -*-
"""Topic 4 workbook — Part 5 exercises, Part 6 solutions, Part 7 reference."""
import _boot
from wbkit import *
from t4_wb1 import B, N, I, M


def _paras(body):
    """Normalise a body argument into a list of paragraphs.

    A paragraph is a str or a list of runs. A bare run — the (text, attrs)
    tuple returned by B/N/I/M — is wrapped so it becomes its own paragraph.
    """
    if isinstance(body, str) or isinstance(body, tuple):
        body = [body]
    return [[b] if isinstance(b, tuple) else b for b in body]


def ex(w, n, title, body=None, code=None, size=8.8):
    w.h4("Exercise %d · %s" % (n, title))
    if body:
        body = _paras(body)
        for b in body:
            w.para(b)
    if code:
        w.code(code, size=size)


def sol(w, n, body=None, code=None, size=8.8):
    p = w.d.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Solution %d" % n)
    r.font.name = HEADF; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = GREEN
    if body:
        body = _paras(body)
        for b in body:
            w.para(b)
    if code:
        w.code(code, size=size)


def build_exercises(w):
    w.page_break()
    w.h1("Part 5 · Practice Exercises")
    w.para("Sixty exercises in five blocks. Block A checks that you know the language; block B is "
           "the one that builds the skill this module assesses — predicting hardware from source; "
           "block C is debugging; block D is design; block E is verification and tools. Full "
           "worked solutions are in Part 6.")
    w.table(["Block", "Exercises", "What it trains"],
            [["A", "1–12", "Language recall — types, literals, widths, operators"],
             ["B", "13–26", "Prediction — what does this code become in hardware?"],
             ["C", "27–38", "Debugging — find the fault and say which tool would catch it"],
             ["D", "39–52", "Design — write the RTL from a specification"],
             ["E", "53–60", "Verification and tools"]],
            widths=[0.7, 1.1, 4.6], size=9.5, align_center=False)

    # ---------------------------------------------------------- A
    w.h2("Block A · Language recall")
    ex(w, 1, "reg and register",
       "Is a variable declared reg always a register in hardware? Give one case where it is and "
       "one where it is not, with a line of code for each.")
    ex(w, 2, "Literal width and sign",
       "State the width and signedness of each of these literals: 8'd10, 4'b1010, 12, -8'd1, "
       "8'sd200, 8'hFF, 8'bx.")
    ex(w, 3, "Replication and concatenation",
       "Evaluate and give the width of each: {3{2'b10}}, {2'b11, {3{1'b0}}, 3'b101}, {4'hA, 4'h5}.")
    ex(w, 4, "Reduction operators",
       "Give the single-bit result of each, for data = 8'b1101_0110:  ^data,  |data,  &data,  "
       "~|data.")
    ex(w, 5, "Logical versus bitwise",
       "For a = 4'b0011 and b = 4'b1100, give the value and width of a && b, a & b, !a and ~a.")
    ex(w, 6, "Vectors and arrays",
       "Which of these are legal, and what does each mean?",
       code=["reg [7:0] v;      reg u [0:7];      reg [7:0] m [0:255];",
             "",
             "(a) v[3:0]      (b) u[3:0]      (c) m[17]      (d) m[17][3:0]      (e) m[3:0]"])
    ex(w, 7, "Indexed part-select",
       [[N("Why is "), M("d[i:j]"), N(" illegal when i and j are signals, while "),
         M("d[i +: 4]"), N(" is legal? What hardware does the legal form produce?")]])
    ex(w, 8, "wire or reg",
       "For each, say whether the signal should be declared wire or reg, and why: (a) a module "
       "output driven by an assign; (b) a module output driven inside always @(posedge clk); "
       "(c) an internal signal connecting two instances; (d) a variable assigned inside "
       "always @(*).")
    ex(w, 9, "parameter and localparam",
       "State the difference, and give one situation where using parameter instead of localparam "
       "would allow a user of your module to break it.")
    ex(w, 10, "Directives",
       [[N("What does "), M("`default_nettype none"), N(" do, and what class of bug does it turn "
          "from a silent x into a compile error? Give a concrete example.")]])
    ex(w, 11, "System tasks",
       [[N("Which of these are synthesisable: "), M("$display"), N(", "), M("$clog2"), N(", "),
         M("$random"), N(", "), M("$bits"), N(", "), M("$finish"), N("? For each synthesisable "
          "one, give a use in design code.")]])
    ex(w, 12, "Timescale",
       [[N("A file begins "), M("`timescale 1ns / 1ps"), N(". A statement says "), M("#5;"),
         N(". How much simulated time passes? What changes if the timescale becomes "),
         M("`timescale 10ns / 1ns"), N("?")]])

    # ---------------------------------------------------------- B
    w.h2("Block B · Predict the hardware")
    w.para("For each snippet: say what the synthesiser produces, and how many flip-flops (if any). "
           "Then check your answer with Yosys.")
    ex(w, 13, "A one-liner", code=["assign y = sel ? b : a;      // a, b, y are [7:0]"])
    ex(w, 14, "A missing else", code=["always @(*)",
                                      "  if (en) y = d;"])
    ex(w, 15, "Blocking in a clocked block",
       code=["always @(posedge clk) begin",
             "  q1 = d;",
             "  q2 = q1;",
             "end"])
    ex(w, 16, "The same, reordered",
       code=["always @(posedge clk) begin",
             "  q2 = q1;",
             "  q1 = d;",
             "end"])
    ex(w, 17, "A concatenation in a clocked block",
       code=["always @(posedge clk)",
             "  q <= {q[6:0], sin};       // q is [7:0]"])
    ex(w, 18, "An unrolled loop",
       code=["integer i;",
             "always @(*) begin",
             "  s = 4'd0;",
             "  for (i = 0; i < 8; i = i + 1) s = s + data[i];",
             "end"])
    ex(w, 19, "A reduction", code=["assign z = ~|result;         // result is [7:0]"])
    ex(w, 20, "A registered read",
       code=["reg [7:0] mem [0:1023];",
             "always @(posedge clk) begin",
             "  if (we) mem[waddr] <= wdata;",
             "  rdata <= mem[raddr];",
             "end"])
    ex(w, 21, "An asynchronous read",
       code=["reg [7:0] mem [0:1023];",
             "always @(posedge clk) if (we) mem[waddr] <= wdata;",
             "assign rdata = mem[raddr];"],
       body="How does this differ from exercise 20 in the hardware produced, and why does it "
            "matter on an FPGA?")
    ex(w, 22, "A variable index on the left",
       code=["always @(*) begin",
             "  y = 8'b0;",
             "  if (en) y[sel] = 1'b1;    // sel is [2:0]",
             "end"])
    ex(w, 23, "A function called twice",
       code=["function [15:0] scale; input [7:0] v; scale = v * 8'd37; endfunction",
             "assign p = scale(a);",
             "assign q = scale(b);"])
    ex(w, 24, "An if/else chain versus a case",
       body="Both snippets below compute the same function. Which produces the shallower logic, "
            "and why does that matter?",
       code=["// (a)                          // (b)",
             "if      (s==2'd0) y = w;       case (s)",
             "else if (s==2'd1) y = x;         2'd0: y = w;   2'd1: y = x;",
             "else if (s==2'd2) y = y2;        2'd2: y = y2;  default: y = z;",
             "else              y = z;       endcase"])
    ex(w, 25, "A counter",
       code=["always @(posedge clk or negedge rst_n)",
             "  if (!rst_n)  q <= 8'd0;",
             "  else if (en) q <= (q == 8'd199) ? 8'd0 : q + 1'b1;"],
       body="How many flip-flops? What is the largest value q ever holds? What would change if "
            "the comparison were q == 8'd255?")
    ex(w, 26, "A three-block FSM",
       body="Topic4_Lab/rtl/traffic_fsm.v synthesises to 52 cells and 12 flip-flops. Account for "
            "the 12 flip-flops by naming the registers in the source and their widths.")

    # ---------------------------------------------------------- C
    w.h2("Block C · Find the bug")
    w.para("For each: name the fault, say what the symptom would be, and state which stage of the "
           "flow — lint, simulation or synthesis — would catch it first.")
    ex(w, 27, "Adder", code=["wire [3:0] a, b;",
                             "wire [3:0] sum;",
                             "assign sum = a + b;"])
    ex(w, 28, "Combinational block",
       code=["always @(a or b)",
             "  y = a & b & c;"])
    ex(w, 29, "Case", code=["always @(*)",
                            "  case (sel)",
                            "    2'b00: y = d0;",
                            "    2'b01: y = d1;",
                            "    2'b10: y = d2;",
                            "  endcase"])
    ex(w, 30, "Two drivers",
       code=["always @(posedge clk) q <= d;",
             "assign q = 1'b0;"])
    ex(w, 31, "Reset", code=["always @(posedge clk)",
                             "  q <= d;                    // no reset anywhere in the design"])
    ex(w, 32, "Shift register",
       code=["always @(posedge clk) begin",
             "  stage1 = din;",
             "  stage2 = stage1;",
             "  stage3 = stage2;",
             "end"])
    ex(w, 33, "Parameter slice",
       code=["localparam integer CW = $clog2(CLKS_PER_BIT);",
             "reg [CW-1:0] cnt;",
             "always @(posedge clk)",
             "  if (cnt == CLKS_PER_BIT[CW-1:0]) cnt <= 0; else cnt <= cnt + 1'b1;"],
       body="This is the real UART bug. Explain precisely why it fails at CLKS_PER_BIT = 16 but "
            "not at CLKS_PER_BIT = 434.")
    ex(w, 34, "Testbench comparison",
       code=["if (y != expected) $display(\"FAIL\");"])
    ex(w, 35, "Clock domain crossing",
       code=["always @(posedge clk_b)",
             "  data_b <= data_a;          // data_a is [7:0], generated in clk_a's domain"])
    ex(w, 36, "FSM", code=["always @(*) begin",
                           "  case (state)",
                           "    IDLE: next = RUN;",
                           "    RUN : next = DONE;",
                           "    DONE: next = IDLE;",
                           "  endcase",
                           "end"])
    ex(w, 37, "Testbench stimulus",
       code=["always #5 clk = ~clk;",
             "initial begin",
             "  rst_n = 0;",
             "  @(posedge clk) rst_n = 1;      // released exactly on an edge",
             "  ...",
             "end"])
    ex(w, 38, "Pipeline",
       code=["always @(posedge clk) begin",
             "  s1 <= a * b;",
             "  s2 <= s1 + c;",
             "  result <= s2;",
             "end",
             "assign result_valid = in_valid;   // not delayed"])

    # ---------------------------------------------------------- D
    w.h2("Block D · Write the RTL")
    w.para("Write synthesisable Verilog that follows the coding standard in section 1.18. For each, "
           "also write a self-checking testbench that prints PASS or FAIL.")
    ex(w, 39, "4:1 multiplexer",
       "Parameterised width W, inputs d0..d3, a 2-bit select, one output. Use a case statement.")
    ex(w, 40, "Binary-to-Gray and Gray-to-binary",
       "Two combinational modules, parameterised width. Gray code changes exactly one bit between "
       "consecutive values; state the formula you used.")
    ex(w, 41, "Parity generator and checker",
       "An 8-bit even-parity generator, and a checker that raises an error output when a 9-bit "
       "received word has the wrong parity. One operator each.")
    ex(w, 42, "Barrel shifter",
       "An 8-bit barrel shifter with a 3-bit shift amount and a direction input, using a "
       "generate-free single expression. Say how many multiplexer levels it produces.")
    ex(w, 43, "Comparator",
       "A parameterised magnitude comparator with gt, eq and lt outputs. Handle the signed case "
       "as a parameter.")
    ex(w, 44, "Register file",
       "A 16 × 8 register file with one write port and two read ports, all synchronous to one "
       "clock. Write port has an enable; register 0 always reads as zero.")
    ex(w, 45, "Programmable clock divider",
       "Given a parameter DIV, produce a single-cycle tick every DIV clocks. Do not gate the "
       "clock. State the flip-flop count as a function of DIV.")
    ex(w, 46, "Debouncer",
       "A switch debouncer: the output changes only when the input has been stable for N "
       "consecutive clocks. N is a parameter.")
    ex(w, 47, "Pulse stretcher",
       "Turn a single-cycle pulse into an output that stays high for exactly N cycles, ignoring "
       "further pulses while it is high.")
    ex(w, 48, "Round-robin arbiter",
       "Four requesters, one grant output, one-hot. After granting requester i, the next search "
       "starts at i+1. State whether your grant is Moore or Mealy.")
    ex(w, 49, "Sequence detector",
       "Detect the overlapping sequence 1101 on a serial input. Provide BOTH a Moore and a Mealy "
       "output and explain the one-cycle difference.")
    ex(w, 50, "Stack (LIFO)",
       "A depth-8, 8-bit stack with push, pop, full and empty. Guard the pointer inside the "
       "module. What happens on a simultaneous push and pop?")
    ex(w, 51, "SPI master (mode 0)",
       "Shift out 8 bits MSB first on the falling edge of sclk, sample miso on the rising edge, "
       "with a programmable clock divider and a busy output.")
    ex(w, 52, "UART with parity",
       "Extend Topic4_Lab's uart_tx and uart_rx to support an optional odd or even parity bit, "
       "selected by a parameter, with a parity_error output on the receiver.")

    # ---------------------------------------------------------- E
    w.h2("Block E · Verification and tools")
    ex(w, 53, "Self-checking conversion",
       "Take a testbench that only prints values and convert it into a self-checking one. List "
       "the six parts from section 3.3 and say where each appears in your version.")
    ex(w, 54, "Scoreboard",
       "Write a scoreboard for Topic4_Lab's sync_fifo that is independent of the design, and use "
       "it with 500 randomised, seeded push/pop operations.")
    ex(w, 55, "Coverage list",
       "For the door_lock FSM of tutorial T5, write the coverage list: every state, every "
       "transition, and every boundary condition your testbench must exercise.")
    ex(w, 56, "Reproduce the UART bug",
       "Reintroduce the CLKS_PER_BIT[CW-1:0] truncation into a copy of uart_rx.v. Then write a "
       "testbench that sends all 256 byte values and counts the failures, and run it at "
       "CLKS_PER_BIT = 8, 16, 27, 32, 64, 100 and 434. Some of those values fail catastrophically "
       "and some do not fail at all. Work out the rule that separates the two groups, and prove "
       "it from the definition of $clog2.")
    ex(w, 57, "Lint triage",
       "Run Verilator on rtl/broken_examples.v and classify every message as: a real bug, a style "
       "warning, or a false positive. Justify each classification.")
    ex(w, 58, "Predict then measure",
       "For any three designs in Topic4_Lab, write down your predicted flip-flop count, then run "
       "Yosys. Where you were wrong, explain why in one sentence each.")
    ex(w, 59, "Vendor flow",
       "Using scripts/vivado_synth.tcl (or ModelSim's .do file), synthesise uart_tx and report: "
       "LUT count, flip-flop count, and worst negative slack at a 50 MHz constraint. Compare the "
       "flip-flop count with the Yosys figure of 27 and explain any difference.")
    ex(w, 60, "Timing experiment",
       "Take adder_gen.v and synthesise it at W = 4, 16 and 64 with a clock constraint. Plot the "
       "worst path delay against W. Then replace the whole module with assign sum = a + b; and "
       "compare. What does the result tell you about describing intent versus structure?")


def build_solutions(w):
    w.page_break()
    w.h1("Part 6 · Worked Solutions")

    w.h2("Block A")
    sol(w, 1, [[N("No. "), M("reg"), N(" is a simulator variable, not a hardware register. It "
                 "becomes a flip-flop only when it is assigned inside a clocked block.")]],
        code=["always @(posedge clk) q <= d;   // reg q -> a flip-flop",
              "always @(*)           y = a & b; // reg y -> pure combinational logic, no storage"])
    sol(w, 2, None, code=[
        "8'd10     8 bits, unsigned        00001010",
        "4'b1010   4 bits, unsigned        1010",
        "12        32 bits, SIGNED         the trap: no width means 32-bit signed",
        "-8'd1     8 bits, unsigned bits   11111111  (two's complement of 1)",
        "8'sd200   8 bits, SIGNED          11001000  = -56, not 200",
        "8'hFF     8 bits, unsigned        11111111  = 255",
        "8'bx      8 bits                  xxxxxxxx  (x fills the width)"])
    sol(w, 3, None, code=[
        "{3{2'b10}}                    = 6'b101010          width 6",
        "{2'b11, {3{1'b0}}, 3'b101}    = 8'b11000101        width 2+3+3 = 8",
        "{4'hA, 4'h5}                  = 8'hA5              width 8"])
    sol(w, 4, "data = 8'b1101_0110 has five 1s.", code=[
        "^data  = 1'b1     odd number of 1s -> parity is 1",
        "|data  = 1'b1     at least one bit is set",
        "&data  = 1'b0     not all bits are set",
        "~|data = 1'b0     the value is not zero"])
    sol(w, 5, None, code=[
        "a && b = 1'b1     1 bit: both operands are non-zero",
        "a &  b = 4'b0000  4 bits: bitwise AND of 0011 and 1100",
        "!a     = 1'b0     1 bit: a is non-zero, so 'not a' is false",
        "~a     = 4'b1100  4 bits: every bit inverted"])
    sol(w, 6, None, code=[
        "(a) v[3:0]     LEGAL    the bottom nibble of an 8-bit vector",
        "(b) u[3:0]     ILLEGAL  u is an ARRAY of 1-bit elements; you cannot slice an array",
        "(c) m[17]      LEGAL    one 8-bit element of the memory",
        "(d) m[17][3:0] LEGAL    the bottom nibble of that element",
        "(e) m[3:0]     ILLEGAL  again, an array cannot be sliced"])
    sol(w, 7, [[N("A synthesiser must know the WIDTH of every expression at elaboration. With "),
                M("d[i:j]"), N(" and variable bounds the width is unknown, so the expression is "
                  "illegal. "), M("d[i +: 4]"),
                N(" has a constant width of 4 and only a variable position, which is exactly what "
                  "a multiplexer does — so it synthesises to a multiplexer that selects a 4-bit "
                  "window out of d.")]])
    sol(w, 8, None, code=[
        "(a) wire  -- an assign may only drive a net",
        "(b) reg   -- a procedural block may only assign a variable",
        "(c) wire  -- a plain connection between two instances, one driver",
        "(d) reg   -- assigned inside a procedural block; still combinational, not a register"])
    sol(w, 9, [[M("parameter"), N(" may be overridden at instantiation; "), M("localparam"),
                N(" may not. Declaring a state encoding as a parameter lets a user write "),
                M("fsm #(.IDLE(3'd7)) u_f (...)"),
                N(" and silently change the meaning of every case label inside the module, "
                  "breaking logic that the module's author verified. State encodings, derived "
                  "widths and internal constants should always be localparam.")]])
    sol(w, 10, [[N("It disables implicit net declaration. Without it, an undeclared name becomes "
                   "a 1-bit wire with no driver, silently. Misspell "), M("data_valid"),
                 N(" as "), M("data_vaild"), N(" in a port connection and you get an undriven "
                   "wire, an x on that port, and no message at all. With the directive it is a "
                   "compile error on the exact line.")]])
    sol(w, 11, [[M("$clog2"), N(" and "), M("$bits"),
                 N(" are synthesisable, because they are evaluated at elaboration. "),
                 M("$display"), N(", "), M("$random"), N(" and "), M("$finish"),
                 N(" are simulation only.")]],
        code=["localparam integer AW = $clog2(DEPTH);      // address width from depth",
              "localparam integer W  = $bits(some_signal);  // adapt to whatever was passed in"])
    sol(w, 12, [[N("With "), M("`timescale 1ns / 1ps"), N(", "), M("#5"),
                 N(" advances time by 5 ns, rounded to the nearest picosecond. With "),
                 M("`timescale 10ns / 1ns"), N(" the same "), M("#5"),
                 N(" advances 50 ns. Every delay in the file changes meaning — which is why the "
                   "timescale should be identical in every file, or set once in a shared "
                   "header.")]])

    w.h2("Block B")
    sol(w, 13, "One 8-bit 2:1 multiplexer — eight 2:1 multiplexer bits. No flip-flops: there is "
               "no clock.")
    sol(w, 14, "A transparent latch on y, enabled by en. There is no else, so on the path where "
               "en is low y must keep its old value, and the only storage a level-sensitive block "
               "can produce is a latch. Yosys reports $_DLATCH_P_.")
    sol(w, 15, "ONE flip-flop. q1 takes d; the next statement gives q2 the NEW q1, which is d. The "
               "tool sees two registers holding the same value and keeps one. Verified in "
               "Topic4_Lab as bad_blocking.")
    sol(w, 16, "TWO flip-flops, and correct shift-register behaviour — from the same operator. "
               "This is the real objection to blocking assignment in a clocked block: the "
               "hardware depends on the order you typed the lines, which is not a property real "
               "flip-flops have.")
    sol(w, 17, "An 8-bit shift register: 8 flip-flops. Each bit's D input is the previous bit's Q, "
               "and sin feeds bit 0.")
    sol(w, 18, "An adder tree with eight one-bit addends — seven adds, which the tool will "
               "balance into a tree about three levels deep. No flip-flops. Note that s is only "
               "4 bits, which is enough for a maximum of 8, so nothing truncates here.")
    sol(w, 19, "An 8-input NOR reduction tree producing one bit: the zero flag. No flip-flops.")
    sol(w, 20, "A 1 K × 8 block RAM with a registered read port and a synchronous write port. The "
               "array itself is a RAM primitive, not flip-flops; rdata is one 8-bit output "
               "register.")
    sol(w, 21, "The read is asynchronous, and no FPGA block RAM can do an asynchronous read. The "
               "tool must therefore build the entire array from flip-flops — 8192 of them — plus "
               "a 1024-to-1 multiplexer per output bit. The design will very likely not fit, and "
               "if it does it will be slow. Same intent, wildly different silicon.")
    sol(w, 22, "A 3-to-8 decoder with an enable. The variable index on the left-hand side, "
               "combined with the default of all zeros, is exactly the decoder pattern. No "
               "flip-flops.")
    sol(w, 23, "TWO independent multipliers. A function call is not a subroutine call — each call "
               "site gets its own physical copy of the logic. If you want one shared multiplier "
               "used at different times, that is a datapath with a multiplexer and a controller.")
    sol(w, 24, "(b) is shallower. The if/else chain is a priority structure and synthesises to "
               "three multiplexers in series; the case is a parallel structure and synthesises to "
               "one 4:1 multiplexer. Depth is delay, so on a critical path the difference is real "
               "— and (b) is easier to read as well.")
    sol(w, 25, "Eight flip-flops (q is [7:0]). The largest value q holds is 199, because it wraps "
               "to 0 on the cycle after 199. If the comparison were q == 8'd255, the explicit "
               "wrap becomes redundant — an 8-bit counter wraps from 255 to 0 by itself — and the "
               "comparator logic would be optimised away, saving cells.")
    sol(w, 26,
        "This is the exercise where most people get it wrong, and the reason is worth knowing. "
        "The obvious answer — 2 for the state and 8 for the timer — gives 10, not 12. The "
        "outputs are combinational (always @(*)), so they contribute nothing. The missing two "
        "come from the tool, not from your source:",
        code=[
        "timer       reg [7:0]                     ->   8  $_DFFE_PN0P_  (enabled by tick)",
        "state       reg [1:0], RE-ENCODED one-hot ->   4  (3 $_DFF_PN0_ + 1 $_DFF_PN1_)",
        "                                              ---",
        "                                               12  as reported",
        "",
        "$ grep -i fsm build/synth_traffic_fsm.txt",
        "  FSM_RECODE pass (re-assigning FSM state encoding)",
        "  Recoding FSM `$fsm$\\state$49' ... mapping auto encoding to `one-hot` for this FSM",
        "",
        "// The DFF_PN1_ is the one-hot bit for MAIN_GREEN -- it resets to 1, the others to 0."])

    w.h2("Block C")
    sol(w, 27, "Width truncation. sum is 4 bits but a + b can produce 5. 9 + 8 gives 17, which "
               "truncates to 1. Symptom: arithmetic that is correct for small values and wrong "
               "for large ones. Caught first by LINT (Verilator WIDTHTRUNC). Fix: make sum "
               "[4:0], or write assign {cout, sum} = a + b;")
    sol(w, 28, "Incomplete sensitivity list: c is read but not listed, so the block does not "
               "re-run when c changes. Symptom: simulation and synthesis disagree — synthesis "
               "builds the correct combinational logic, simulation does not. Caught first by "
               "LINT. Fix: always @(*).")
    sol(w, 29, "No default, and 2'b11 is not covered, so y latches on that input. Symptom: an "
               "inferred latch in the synthesis report and a design that is hard to time. Caught "
               "first by LINT, and unmistakably by SYNTHESIS. Fix: add default: y = d0; or a "
               "default assignment at the top of the block.")
    sol(w, 30, "Two drivers on q — one procedural, one continuous. This is illegal for a reg and "
               "gives x where they conflict. Caught first by the COMPILER or LINT. Fix: one "
               "signal, one driving block.")
    sol(w, 31, "No reset. The flip-flop's power-up value is unknown, so q is x from time zero and "
               "the x propagates through the whole design. Symptom: everything is x and nothing "
               "works. Caught first by SIMULATION. FPGA tools may hide this by honouring an "
               "initial value; ASIC tools will not. Fix: reset every state-holding register.")
    sol(w, 32, "Blocking assignments in a clocked block. All three stages collapse: stage3 "
               "receives din in the same cycle, so instead of a three-deep pipeline you get one "
               "flip-flop. Caught first by LINT (most linters flag = in a clocked block), and "
               "visibly by SYNTHESIS (one flip-flop instead of three). Fix: use <=.")
    sol(w, 33, [N("CLKS_PER_BIT is sliced to CW bits, but CLKS_PER_BIT itself does not FIT in CW "
                  "bits — CW is the width needed to count from 0 to CLKS_PER_BIT−1, one short. "
                  "At 16, CW = $clog2(16) = 4 and 16 truncates to 0, so the counter compares "
                  "against zero and the timing collapses. At 434, CW = $clog2(434) = 9 and 434 "
                  "fits in 9 bits, so the slice loses nothing and the bug is invisible."),
                B("  This is why you must test at more than one parameter value.")],
        code=["// Fix: compute as an integer, then slice at the point of use.",
              "localparam integer FULL_BIT = CLKS_PER_BIT - 1;",
              "... if (cnt == FULL_BIT[CW-1:0]) ..."])
    sol(w, 34, [[M("!="), N(" is the two-state comparison. If y is x, "), M("y != expected"),
                 N(" evaluates to x, which is not true, so the check passes and the bug escapes "
                   "silently. Use "), M("!=="), N(" in testbenches. Caught by nothing but "
                   "review — which is why it is worth knowing.")]])
    sol(w, 35, "An 8-bit bus crossing a clock domain with no synchronisation at all. Each bit can "
               "go metastable independently and the bits can settle on different cycles, so "
               "clk_b can read a value that never existed in clk_a's domain. Fix: use Gray coding "
               "if the value is a counter or pointer, or a request/acknowledge handshake with the "
               "data held stable. Two-flop synchronisers are for SINGLE bits only. Caught by a "
               "CDC lint tool, or by review; ordinary simulation will not show it.")
    sol(w, 36, "No default branch. Symptom: next latches when state is anything other than the "
               "three listed values — and, with more states than encodings, the machine can "
               "become stuck in an illegal state from which it never recovers. Caught by "
               "SYNTHESIS (latch warning). Fix: default: next = IDLE; which both removes the "
               "latch and makes the FSM safe.")
    sol(w, 37, "Reset is released exactly on a clock edge — a race between the reset and the "
               "clock, so the state register sees an ambiguous condition and can stay x for "
               "cycles. Symptom: the design appears broken at the start of every run. Fix: "
               "release a small delay after the edge:  @(posedge clk); #1 rst_n = 1;  This exact "
               "bug cost time while building Topic4_Lab.")
    sol(w, 38, "The datapath is pipelined three deep but result_valid is not delayed at all, so "
               "results are flagged valid three cycles before they exist. Fix: pass valid through "
               "an identical three-stage register chain. Every tag, address or ID travelling with "
               "the data needs the same treatment. Caught by SIMULATION, if the testbench checks "
               "valid — which is exactly why it must.")

    w.h2("Block D")
    sol(w, 39, None, code=[
        "`default_nettype none",
        "module mux4 #(parameter integer W = 8)(",
        "    input  wire [W-1:0] d0, d1, d2, d3,",
        "    input  wire [1:0]   sel,",
        "    output reg  [W-1:0] y);",
        "  always @(*) begin",
        "    case (sel)",
        "      2'd0:    y = d0;",
        "      2'd1:    y = d1;",
        "      2'd2:    y = d2;",
        "      default: y = d3;        // covers 2'd3, x and z -- no latch",
        "    endcase",
        "  end",
        "endmodule",
        "`default_nettype wire"])
    sol(w, 40, "Binary to Gray: g = b ^ (b >> 1). Gray to binary: each output bit is the XOR of "
               "all Gray bits from the MSB down to that position — an XOR prefix chain.",
        code=[
        "module bin2gray #(parameter integer W = 4)(",
        "    input wire [W-1:0] b, output wire [W-1:0] g);",
        "  assign g = b ^ (b >> 1);",
        "endmodule",
        "",
        "module gray2bin #(parameter integer W = 4)(",
        "    input wire [W-1:0] g, output reg [W-1:0] b);",
        "  integer i;",
        "  always @(*) begin",
        "    b[W-1] = g[W-1];",
        "    for (i = W-2; i >= 0; i = i - 1) b[i] = b[i+1] ^ g[i];",
        "  end",
        "endmodule"])
    sol(w, 41, None, code=[
        "assign parity_bit = ^data;              // even parity: makes the 9-bit word even",
        "assign parity_err = ^{data, parity_bit};// 1 if the received word has odd parity"])
    sol(w, 42, "Three multiplexer levels — one per bit of the shift amount, each shifting by "
               "1, 2 and 4 respectively. That is what a shift operator with a variable amount "
               "synthesises to.",
        code=[
        "module barrel8 (input wire [7:0] d, input wire [2:0] amt, input wire left,",
        "                output wire [7:0] y);",
        "  assign y = left ? (d << amt) : (d >> amt);",
        "endmodule"])
    sol(w, 43, None, code=[
        "module cmp #(parameter integer W = 8, parameter SIGNED_CMP = 0)(",
        "    input wire [W-1:0] a, b, output wire gt, eq, lt);",
        "  wire s_gt = ($signed(a) >  $signed(b));",
        "  wire s_lt = ($signed(a) <  $signed(b));",
        "  assign eq = (a == b);",
        "  assign gt = SIGNED_CMP ? s_gt : (a > b);",
        "  assign lt = SIGNED_CMP ? s_lt : (a < b);",
        "endmodule"])
    sol(w, 44, "16 × 8 = 128 flip-flops if the tool builds registers, or one small distributed "
               "RAM. Register 0 is forced to zero at the READ side so a write to it is harmless.",
        code=[
        "reg [7:0] rf [0:15];",
        "always @(posedge clk)",
        "  if (we && (wa != 4'd0)) rf[wa] <= wd;",
        "assign rd0 = (ra0 == 4'd0) ? 8'd0 : rf[ra0];",
        "assign rd1 = (ra1 == 4'd0) ? 8'd0 : rf[ra1];"])
    sol(w, 45, "$clog2(DIV) flip-flops for the counter, plus one for the tick if you register it. "
               "Never gate the clock: produce an ENABLE and use it on the clock enable of "
               "downstream registers.",
        code=[
        "localparam integer CW = $clog2(DIV);",
        "reg [CW-1:0] cnt;",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)              begin cnt <= {CW{1'b0}}; tick <= 1'b0; end",
        "  else if (cnt == DIV-1)   begin cnt <= {CW{1'b0}}; tick <= 1'b1; end",
        "  else                     begin cnt <= cnt + 1'b1; tick <= 1'b0; end",
        "end"])
    sol(w, 46, None, code=[
        "reg [1:0] sync;  reg [CW-1:0] cnt;  reg q;",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n) begin sync <= 2'b00; cnt <= 0; q <= 1'b0; end",
        "  else begin",
        "    sync <= {sync[0], din};                 // synchronise the asynchronous switch",
        "    if (sync[1] == q)      cnt <= 0;        // agrees with the output: restart",
        "    else if (cnt == N-1) begin q <= sync[1]; cnt <= 0; end   // stable long enough",
        "    else                   cnt <= cnt + 1'b1;",
        "  end",
        "end"])
    sol(w, 47, None, code=[
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)                begin cnt <= 0; y <= 1'b0; end",
        "  else if (!y && pulse_in)   begin cnt <= N-1; y <= 1'b1; end",
        "  else if (y && (cnt != 0))        cnt <= cnt - 1'b1;",
        "  else if (y)                      y   <= 1'b0;",
        "end"])
    sol(w, 48, "The grant here is Mealy: it depends on req as well as on the stored pointer, so "
               "it responds in the same cycle. Register it if it leaves the chip.",
        code=[
        "reg [1:0] ptr;                           // where to start searching",
        "reg [3:0] grant;",
        "integer i; reg found;",
        "always @(*) begin",
        "  grant = 4'b0000; found = 1'b0;",
        "  for (i = 0; i < 4; i = i + 1)",
        "    if (!found && req[(ptr + i) % 4]) begin",
        "      grant[(ptr + i) % 4] = 1'b1; found = 1'b1;",
        "    end",
        "end",
        "always @(posedge clk or negedge rst_n)",
        "  if (!rst_n)     ptr <= 2'd0;",
        "  else if (found) ptr <= (ptr + i) % 4 + 1;   // resume after the one just granted"])
    sol(w, 49, "The Mealy output pulses on the clock edge where the final 1 arrives; the Moore "
               "output pulses one cycle later, because it is decoded from the state the machine "
               "has just entered. Overlap is handled by returning to state S1 (a '1' seen) rather "
               "than to IDLE after a match.",
        code=[
        "localparam [2:0] S0=0, S1=1, S11=2, S110=3, S1101=4;",
        "always @(*) begin",
        "  next = S0;",
        "  case (state)",
        "    S0   : next = din ? S1    : S0;",
        "    S1   : next = din ? S11   : S0;",
        "    S11  : next = din ? S11   : S110;",
        "    S110 : next = din ? S1101 : S0;",
        "    S1101: next = din ? S11   : S0;      // OVERLAP: 1101 then 1 restarts at S11",
        "    default: next = S0;",
        "  endcase",
        "end",
        "assign found_moore = (state == S1101);              // one cycle later",
        "assign found_mealy = (state == S110) && din;        // same cycle"])
    sol(w, 50, "On a simultaneous push and pop the pointer is unchanged and the pushed word "
               "replaces the popped one — decide this deliberately and document it, because both "
               "behaviours are defensible and a caller will assume one of them.",
        code=[
        "reg [7:0] mem [0:7];",
        "reg [3:0] sp;                            // 4 bits for depth 8: the extra bit",
        "wire do_push = push & ~full;",
        "wire do_pop  = pop  & ~empty;",
        "assign empty = (sp == 4'd0);",
        "assign full  = (sp == 4'd8);",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n) sp <= 4'd0;",
        "  else begin",
        "    if (do_push) mem[sp[2:0]] <= din;",
        "    case ({do_push, do_pop})",
        "      2'b10: sp <= sp + 1'b1;",
        "      2'b01: sp <= sp - 1'b1;",
        "      default: ;                         // both or neither: sp unchanged",
        "    endcase",
        "  end",
        "end",
        "assign dout = mem[sp[2:0] - 1'b1];"])
    sol(w, 51, "Mode 0 means CPOL = 0 and CPHA = 0: sclk idles low, data is sampled on the rising "
               "edge and changed on the falling edge. The bit counter and the divider are two "
               "separate counters; do not try to derive one from the other.",
        code=[
        "// Sketch of the FSM: IDLE -> (start) -> SHIFT (16 half-periods) -> DONE -> IDLE",
        "// On each divider terminal count, toggle sclk.",
        "//   sclk 0->1 (rising): shift miso into the receive register",
        "//   sclk 1->0 (falling): present the next mosi bit",
        "// busy is high from start until the eighth rising edge has been consumed."])
    sol(w, 52, "Add a PARITY parameter (0 none, 1 odd, 2 even) and one extra state to each FSM. "
               "The transmitter sends ^data (even) or ~^data (odd) after the eighth data bit; the "
               "receiver samples that bit into a register and compares.",
        code=[
        "// transmitter, in the state after the last data bit:",
        "PARITY_ST: begin tx <= (PARITY == 1) ? ~^shifter_orig : ^shifter_orig; ... end",
        "",
        "// receiver, in the equivalent state:",
        "PARITY_ST: begin",
        "  par_rx <= rx_sync;",
        "  parity_error <= rx_sync !== ((PARITY == 1) ? ~^shifter : ^shifter);",
        "end"])

    w.h2("Block E")
    sol(w, 53, "The six parts: (1) instantiate the DUT; (2) one check task that is the only place "
               "a verdict is formed; (3) a waveform dump; (4) stimulus, each step followed by a "
               "check; (5) a final PASS/FAIL print driven by an error counter; (6) $finish. If "
               "your testbench has no error counter, it is not self-checking — it is a "
               "demonstration.")
    sol(w, 54, "The scoreboard must be written from the FIFO's SPECIFICATION and must never read "
               "the design's internal pointers. Model it as a simple array plus head and tail "
               "indices; push and pop the model in the same tasks that drive the DUT, and compare "
               "count, empty, full and rd_data after every operation. Seed $random so a failure "
               "reproduces exactly.")
    sol(w, 55, "States: START, GOT2, GOT21, UNLOCKED, ALARM. Transitions: correct key from each "
               "state; wrong key from each state; the wrong-key counter reaching 3; reset from "
               "ALARM. Boundaries: the unlocked pulse being exactly four cycles, not three or "
               "five; two wrong keys followed by a correct one (the counter must NOT reset — or "
               "must, depending on your specification: decide and test what you decided); "
               "key_valid low for many cycles between keys.")
    sol(w, 56,
        [N("Measured result, running the reintroduced bug against all 256 byte values under "
           "Icarus Verilog 12.0:")],
        code=[
        "CPB=8    failures=254/256",
        "CPB=16   failures=255/256",
        "CPB=27   failures=  0/256",
        "CPB=32   failures=255/256",
        "CPB=64   failures=255/256",
        "CPB=100  failures=  0/256",
        "CPB=434  failures=  0/256"])
    w.para([B("The rule: the bug appears exactly when CLKS_PER_BIT is a power of two."),
            N("  CW is defined as $clog2(CLKS_PER_BIT) = ceil(log2 N), which is the number of "
              "bits needed to count from 0 to N−1. For any N that is NOT a power of two, "
              "N < 2^ceil(log2 N), so N itself still fits in CW bits and the slice loses "
              "nothing — the design works by luck. For N = 2^k, ceil(log2 N) = k and N = 2^k "
              "needs k+1 bits, so it truncates to zero and the timing collapses.")])
    w.para([N("This is why 434 — the real 50 MHz / 115 200 value — hides the bug completely, "
              "while 16, chosen only to make simulations short, exposes it. "),
            B("A parameterised module must be tested at more than one parameter value, and at "
              "least one of them should be awkward.")])
    sol(w, 57, "Real bugs: WIDTHTRUNC on bad_width; the latch warnings on bad_latch; the blocking "
               "assignment in a clocked block in bad_blocking. Style warnings: DECLFILENAME "
               "(module name does not match the file), which is real but harmless in a file that "
               "deliberately holds several modules. There should be no genuine false positives — "
               "if you believe you have found one, take it seriously and prove it before you "
               "suppress it.")
    sol(w, 58, "Common reasons a prediction is wrong: the tool kept an output register you did "
               "not count; the tool optimised away state you thought was needed because it is "
               "never read; a constant propagated and removed a whole counter; or you forgot that "
               "a parameterised width is bigger than the default. Each of those is worth "
               "understanding — they are how you learn to read your own RTL as hardware.")
    sol(w, 59, "The counts will not match exactly. Yosys reports generic cells against a simple "
               "internal library; Vivado maps to real Artix-7 LUTs, flip-flops and carry chains, "
               "and it will often keep a couple of extra flip-flops for I/O registers or "
               "retiming. The flip-flop count should be close to 27 — within a few. A large "
               "difference means one of the two tools understood your design differently from "
               "how you did, and that is worth ten minutes of your time.")
    sol(w, 60, "The ripple adder's worst path grows roughly linearly with W, because the carry "
               "must propagate through every stage. The plain + is handed to the tool as intent "
               "rather than structure, and the tool selects a carry-lookahead or carry-select "
               "implementation — or, on an FPGA, the dedicated carry chain — which grows far more "
               "slowly. Lesson: describe INTENT and let the tool choose the structure, unless you "
               "have a specific, measured reason not to.")


def build_reference(w):
    w.page_break()
    w.h1("Part 7 · Reference")

    w.h2("7.1  Glossary")
    w.table(["Term", "Meaning"],
            [["RTL", "Register-transfer level — describing what happens to data between clock "
                     "edges, without specifying which gates do it."],
             ["Synthesis", "Translating RTL into a gate-level netlist for a target technology."],
             ["Netlist", "A list of gates and flip-flops and the wires between them — what "
                         "synthesis outputs."],
             ["Elaboration", "Building the hierarchy and resolving parameters and generate blocks, "
                             "before simulation or synthesis."],
             ["Inference", "The synthesiser recognising a code pattern and producing the "
                           "corresponding hardware."],
             ["Latch", "Level-sensitive storage; transparent while enabled. In RTL, almost always "
                       "an accident."],
             ["Flip-flop", "Edge-triggered storage; captures at one clock edge and holds until the "
                           "next."],
             ["Blocking (=)", "Assignment that takes effect immediately. Combinational blocks "
                              "only."],
             ["Non-blocking (<=)", "Assignment applied at the end of the time step. Clocked blocks "
                                   "only."],
             ["Sensitivity list", "The events that make a procedural block run."],
             ["Net / variable", "wire is a net, driven continuously; reg is a variable, assigned "
                                "in a procedural block."],
             ["Four-state logic", "0, 1, x (unknown) and z (high impedance)."],
             ["FSM", "Finite state machine — a state register plus next-state and output logic."],
             ["Moore / Mealy", "Outputs from state alone / from state and inputs."],
             ["One-hot", "A state encoding using one flip-flop per state, exactly one of which "
                         "is 1."],
             ["FSMD", "Finite state machine with a datapath — a controller plus the registers and "
                      "arithmetic it steers."],
             ["Metastability", "A flip-flop's output settling unpredictably after a setup or hold "
                               "violation."],
             ["CDC", "Clock domain crossing — moving a signal between two unrelated clocks."],
             ["Synchroniser", "Two or more chained flip-flops that give metastability time to "
                              "decay."],
             ["Pipelining", "Inserting registers to shorten the longest combinational path."],
             ["Slack / WNS", "Time left over on a timing path; worst negative slack is the worst "
                             "such path."],
             ["Testbench", "A port-less module that instantiates the design, drives it and checks "
                           "the results automatically."],
             ["Scoreboard", "An independent model of expected behaviour, written from the "
                            "specification."],
             ["VCD", "Value Change Dump — the waveform format $dumpvars writes and GTKWave reads."],
             ["Lint", "Static analysis of source code, before simulation."],
             ["Synthesisable subset", "The part of Verilog a synthesis tool can turn into "
                                      "hardware."]],
            widths=[1.5, 4.9], size=9, align_center=False)

    w.h2("7.2  Coding-standard checklist")
    w.numbered([
        "One file, one module; the file is named after the module.",
        "`default_nettype none at the top; `resetall at the bottom.",
        "ANSI port headers. Instantiate by name. Prefix instances with u_.",
        "Active-low signals end in _n. Clocks are named clk.",
        "Size every literal.",
        "Combinational: always @(*), =, and a default assignment at the top of the block.",
        "Sequential: always @(posedge clk), <= only.",
        "Every case has a default. Never casex. Never full_case or parallel_case.",
        "One driver per signal. Reset every state-holding register.",
        "Every FSM has a safe default that recovers from an illegal state.",
        "Anything crossing a clock domain goes through a synchroniser; buses use Gray coding or "
        "a handshake.",
        "Lint, then simulate, then synthesise. Read the synthesis log for latches every time.",
    ])

    w.h2("7.3  Troubleshooting")
    w.table(["Symptom", "Almost always means", "Fix"],
            [["Output is x from time zero", "A register was never reset, or a wire has no driver",
              "Reset every register; check port connections"],
             ["Output is x after working", "Two drivers, or reading past the end of a vector",
              "One signal, one driving block"],
             ["'Inferred latch for signal y'", "A branch of always @(*) leaves y unassigned",
              "Default assignment at the top of the block"],
             ["Shift register is one flip-flop", "Blocking = used in a clocked block",
              "Use <= in every always @(posedge clk)"],
             ["Result wraps at the wrong value", "Width truncation on an expression",
              "Make the target one bit wider; run Verilator"],
             ["Signal not found in GTKWave", "$dumpvars scope too narrow, or a stale VCD",
              "$dumpvars(0, tb); and re-run before re-opening"],
             ["Testbench passes, hardware fails", "casex, full_case, or an initial block",
              "Remove all three; reset properly"],
             ["FSM stuck in an unknown state", "No default branch; reset released on a clock edge",
              "default: next = IDLE; release reset between edges"],
             ["Works at one parameter, not another", "A constant sliced to a width too small "
                                                     "to hold it",
              "Compute as an integer; slice at the point of use"],
             ["Design will not fit on the FPGA", "An asynchronous memory read, or a reset on a "
                                                 "large array",
              "Register the read; do not reset the array"],
             ["Timing fails by a large margin", "A long combinational path, or no clock constraint",
              "Constrain the clock; then pipeline the path"]],
            widths=[1.9, 2.3, 2.2], size=9, align_center=False)

    w.h2("7.4  Command card")
    w.table(["Task", "Open-source", "Vivado", "ModelSim"],
            [["Lint", "verilator --lint-only -Wall rtl/*.v", "report_methodology",
              "vlog (warnings)"],
             ["Compile", "iverilog -g2005 -o sim.vvp <files>", "xvlog <files>", "vlog <files>"],
             ["Elaborate", "(part of iverilog)", "xelab -debug typical <top>", "(part of vsim)"],
             ["Run", "vvp sim.vvp", "xsim <snapshot> -runall", "vsim -c work.<top>; run -all"],
             ["Waveforms", "gtkwave dump.vcd", "simulator wave window", "add wave -r /*"],
             ["Synthesise", "yosys -p \"...; synth -top X; stat\"", "synth_design -top X -part P",
              "(not a synthesis tool)"],
             ["Area report", "stat", "report_utilization", "—"],
             ["Timing report", "(none)", "report_timing_summary", "—"],
             ["Find latches", "grep -i latch on the log", "Messages: [Synth 8-327]", "—"]],
            widths=[1.1, 2.2, 1.7, 1.7], size=8.5, align_center=False)

    w.h2("7.5  Where to go next")
    w.bullets([
        [B("Topic 5 — synthesis, constraints and timing closure. "),
         N("Everything you build from here on is written in the language you have just learned; "
           "the difference is that the clock, the area and the power start to have opinions "
           "about it.")],
        [B("The lab. "), N("Topic4_Lab/ contains 22 designs, 5 self-checking testbenches and "
                           "scripts for all three toolchains. The experiments at the end of its "
                           "README are worth more than any additional reading.")],
        [B("Standards. "), N("IEEE 1364-2005 is Verilog; IEEE 1800 is SystemVerilog. You do not "
                             "need to read them cover to cover, but knowing they exist — and "
                             "that your tool's behaviour is defined somewhere — matters when two "
                             "tools disagree.")],
    ])
    w.para([I("End of Topic 4 workbook. Every design, testbench and script referred to here is in "
              "Topic4_Lab/, and every quoted tool output was produced by running the tool on "
              "that code.")])
