# -*- coding: utf-8 -*-
"""Module 2 Topic 2 workbook — Part 3: the patterns every block is built from."""
import _boot
from wbkit import *
from m2t2_wb1 import B, N, I, M


def build(w):
    w.h1("Part 3 · The Patterns Every Block Is Built From")

    w.para([N("Parts 1 and 2 were about what RTL is and what you are allowed to "
              "write. This part is about what real designs are actually made of. "
              "Three structures account for almost all synthesisable RTL, and once "
              "you can recognise them most designs stop looking unfamiliar.")])

    # ================================================ datapath + controller
    w.h2("3.1  Datapath and controller")

    w.image("datapath_controller", width=6.4)

    w.para([N("A UART, a cache controller, a DMA engine, a GPU shader core — "
              "different sizes, the same two halves.")])

    w.bullets([
        [B("The datapath "), N("holds and transforms data: registers, adders, "
           "multiplexers, counters. It is wide, it is most of the area, and it makes "
           "no decisions at all.")],
        [B("The controller "), N("is a finite state machine that decides WHEN each "
           "datapath element loads, clears or holds. It is narrow, it is a handful "
           "of gates, and it contains all of the behaviour.")],
    ])

    w.para([N("They talk over two thin bundles of wires: "), B("control"),
            N(" signals downward, "), B("status"), N(" signals upward. That is the "
              "entire interface.")])

    w.h3("The worked example: accumulate N samples")

    w.para([N("Assert "), M("start"), N(" with the sample count on "), M("n"),
            N("; feed one sample per clock on "), M("data"), N("; "), M("done"),
            N(" pulses when the sum is valid. The controller is three states.")])

    w.code([
        "// ---- the CONTROLLER decides.  Narrow.  No data passes through it.",
        "always @(*) begin",
        "    acc_clr = 0; acc_en = 0; cnt_ld = 0; cnt_dec = 0; done = 0;",
        "    case (state)",
        "        S_IDLE : if (start)     begin acc_clr = 1; cnt_ld  = 1; end",
        "        S_RUN  : if (!cnt_done) begin acc_en  = 1; cnt_dec = 1; end",
        "        S_DONE :                      done    = 1;",
        "        default: ;",
        "    endcase",
        "end",
        "",
        "// ---- the DATAPATH holds and transforms.  Wide.  It decides nothing.",
        "always @(posedge clk or negedge rst_n) begin",
        "    if      (!rst_n)  sum <= 0;",
        "    else if (acc_clr) sum <= 0;",
        "    else if (acc_en)  sum <= sum + data;",
        "end"],
        caption="rtl/datapath_ctrl.v, abridged")

    w.code([
        "$ make dpctrl",
        "  cycle  data  | clr en ld dec done |  sum",
        "      0     0  |  1  0  1  0   0   |     0",
        "      1    10  |  0  1  0  1   0   |     0",
        "      2    20  |  0  1  0  1   0   |    10",
        "      ...",
        "      7     0  |  0  0  0  0   0   |   157",
        "      8     0  |  0  0  0  0   1   |   157",
        "",
        "  golden total : 157      hardware sum : 157",
        "  PASS - controller sequenced the datapath correctly"])

    w.h3("What the split costs, measured")

    w.table(["module", "cells", "flip-flops", "what it contains"],
            [["accum_ctrl", "10", "2", "three states, five control outputs"],
             ["accum_datapath", "145", "24",
              "a 16-bit accumulator and an 8-bit down-counter"],
             ["accum_top", "156", "26", "both, plus the wires between them"]],
            widths=[1.5, 0.8, 1.0, 3.5], size=9.0, bold_cols=(0,),
            align_center=False)

    w.callout("Six per cent of the cells, one hundred per cent of the behaviour", [
        [N("That ratio is the whole argument for the split. Over the life of a "
           "design you will re-time, widen and pipeline the expensive half many "
           "times — and each time, the half that decides what happens stays exactly "
           "as it was.")],
        [N("It also means the part that is hardest to get right is the part small "
           "enough to read in one sitting. A ten-cell controller can be reviewed "
           "line by line; a 145-cell datapath cannot, and does not need to be.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h3("Which signals go where")
    w.table(["Signal", "Direction", "Why it belongs there"],
            [["acc_clr, acc_en", "control, down",
              "the controller decides when to clear and accumulate"],
             ["cnt_ld, cnt_dec", "control, down",
              "the controller decides when to load and decrement"],
             ["cnt_done", "status, up",
              "the datapath knows the count; the controller only asks"],
             ["sum", "data, out",
              "never crosses into the controller — it does not need it"],
             ["start, done", "handshake",
              "the block's interface, not an internal signal"]],
            widths=[1.5, 1.4, 3.9], size=9.0, bold_cols=(0,), align_center=False)

    w.para([N("The row worth arguing about is "), M("cnt_done"), N(". It would be "
              "possible for the controller to hold the counter itself and test it "
              "directly. Do that and the controller becomes width-dependent: change "
              "the maximum sample count and you edit the state machine. Keeping the "
              "counter in the datapath and passing up a single "), B("status bit"),
            N(" means the controller never changes at all.")])

    # ============================================================== the FSM
    w.h2("3.2  The finite state machine")

    w.image("fsm_pattern", width=6.4)

    w.para([N("A state machine is the standard way to write anything that has to "
              "happen in a sequence. Almost every RTL group writes them in the same "
              "three blocks, and the reason is not tradition.")])

    w.h3("Block 1 — the state register")
    w.code([
        "always @(posedge clk or negedge rst_n) begin",
        "    if (!rst_n) state <= S_IDLE;",
        "    else        state <= next_state;",
        "end"])
    w.para([N("Sequential. Non-blocking assignment. This is the only sequential "
              "logic in the machine, so it is the only place a clock or a reset "
              "appears — which makes it the only block whose timing you have to "
              "think about.")])

    w.h3("Block 2 — the next-state logic")
    w.code([
        "always @(*) begin",
        "    next_state = state;              // <-- THE DEFAULT ASSIGNMENT",
        "    case (state)",
        "        S_IDLE : if (din) next_state = S_1;",
        "        S_1    : if (din) next_state = S_1;   else next_state = S_10;",
        "        ...",
        "        default:          next_state = S_IDLE;",
        "    endcase",
        "end"])
    w.para([N("Combinational. Blocking assignment. A pure function of the current "
              "state and the inputs, with no notion of time in it at all.")])

    w.h3("Block 3 — the output logic")
    w.code([
        "assign det = (state == S_101);       // Moore: state only",
        "",
        "// or, when several outputs are decoded:",
        "always @(*) begin",
        "    main_light = RED;  side_light = RED;      // defaults again",
        "    case (state)",
        "        S_MAIN_GREEN : begin main_light = GREEN; side_light = RED; end",
        "        ...",
        "    endcase",
        "end"])

    w.callout("The default assignment is the whole trick", [
        [N("Look again at blocks 2 and 3. Not one of those if statements has an "
           "else, and not one of them needs one — the output was already written, "
           "unconditionally, on the first line of the block. No path through either "
           "block leaves anything unassigned, so no latch can be inferred, whatever "
           "the case statement leaves out.")],
        [N("This is the recommended way to write a next-state or output block, and "
           "it is why the lab linter had to learn to recognise it. A naive latch "
           "rule flags every one of those if statements; Yosys builds a latch in "
           "none of them. "), M("make lintcheck"), N(" puts the two opinions side by "
           "side on sixteen designs, and a linter that cries wolf gets switched off "
           "— which makes it worse than no linter at all.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h3("Why not one block?")

    w.para([N("You can write a working state machine in a single clocked block, "
              "with the case statement inside it. Nothing about it is illegal, and "
              "for a very small machine it is shorter. Here is what you give up:")])

    w.table(["", "one block", "three blocks"],
            [["works?", "yes", "yes"],
             ["where is the reset?", "mixed in with the logic",
              "block 1, and nowhere else"],
             ["where is the clock?", "wrapped around everything",
              "block 1, and nowhere else"],
             ["outputs are", "registered, always",
              "your choice — Moore or Mealy"],
             ["reviewing a change", "you re-read the timing every time",
              "blocks 2 and 3 have no timing to re-read"],
             ["adding a state", "one place, easy to miss a branch",
              "two places, both of them a case statement"]],
            widths=[1.6, 2.5, 2.7], size=9.0, bold_cols=(0,), align_center=False)

    w.para([N("One block is not wrong. Three blocks are easier to be right in, and "
              "over a project that is the same thing.")])

    # ======================================================== Moore / Mealy
    w.h2("3.3  Moore and Mealy")

    w.image("moore_mealy", width=6.4)

    w.para([N("There is exactly one structural difference between the two: whether "
              "the output logic is allowed to see the input. Everything else follows "
              "from it.")])

    w.h3("The same detector, twice")

    w.para([N("Both machines below detect the pattern 1-0-1 arriving one bit per "
              "clock, counting overlaps — so the stream 1 0 1 0 1 contains two "
              "matches, not one.")])

    w.image("seq101_moore_states", width=6.4)
    w.image("seq101_mealy_states", width=6.4)

    w.code([
        "// MOORE - the output is decoded from the state alone",
        "assign det = (state == S_101);",
        "",
        "// MEALY - the output depends on the state AND the current input",
        "assign det = (state == S_10) && din;"])

    w.h3("The difference, measured")

    w.image("moore_mealy_timing", width=6.4)

    w.code([
        "$ make fsm",
        "  cycle  din   mealy exp   moore exp",
        "     3    1     1   1     0   0   <- match",
        "     4    1     0   0     1   1",
        "     6    1     1   1     0   0   <- match",
        "     7    0     0   0     1   1",
        "",
        "  matches in the stream : 5      mismatches vs golden  : 0",
        "  PASS - same language, Moore trails Mealy by one cycle"])

    w.para([N("The golden model is computed from the stimulus stream itself, not "
              "from either machine — so a bug in one of them appears as a mismatch "
              "rather than as two machines confidently agreeing on the wrong "
              "answer.")])

    w.table(["", "Moore", "Mealy"],
            [["output depends on", "state only", "state and input"],
             ["output appears", "one cycle after the input", "the same cycle"],
             ["output glitches", "no — decoded from registers",
              "yes — inherits the input's glitches"],
             ["states needed", "usually one more", "usually one fewer"],
             ["measured here", "13 cells, 2 flip-flops", "14 cells, 2 flip-flops"]],
            widths=[1.6, 2.5, 2.7], size=9.0, bold_cols=(0,), align_center=False)

    w.callout("Choosing between them", [
        [B("Moore "), N("when the output leaves the block, drives other logic, or "
           "is timing critical. It comes out of a decode of registered bits, so it "
           "is clean, predictable and easy to constrain.")],
        [B("Mealy "), N("when the cycle genuinely matters — a handshake that must be "
           "answered immediately, or a pipeline where one more cycle of latency "
           "costs throughput you cannot spare.")],
        [B("Either way, register it at the boundary. "),
         N("A Mealy output leaving your block hands the next designer a "
           "combinational path they did not ask for. Put a flip-flop on it — which "
           "turns it back into Moore.")],
    ], color=NAVY, bar="0E2A47")

    w.para([N("One piece of folklore is worth discarding here. “Mealy needs "
              "fewer states” is true and almost never the reason to pick it. "
              "In this example it saved one flip-flop's worth of nothing — both "
              "machines needed two — and cost one cell more. The real trade is the "
              "cycle against the glitch-free output, and that is a system question, "
              "not a coding one.")])

    # ============================================================ encoding
    w.h2("3.4  State encoding")

    w.image("state_encoding", width=6.4)

    w.para([N("The state names are just numbers you chose. Choosing them differently "
              "gives the same behaviour and different hardware.")])

    w.code([
        "// binary                          // one-hot",
        "localparam [1:0] S_IDLE = 2'b00,    localparam [3:0] S_IDLE = 4'b0001,",
        "                 S_1    = 2'b01,                     S_1    = 4'b0010,",
        "                 S_10   = 2'b10,                     S_10   = 4'b0100,",
        "                 S_101  = 2'b11;                     S_101  = 4'b1000;"])

    w.table(["encoding", "flops", "cells", "the property", "where it wins"],
            [["binary", "2", "13", "fewest flip-flops",
              "ASIC, many states, area-critical"],
             ["one-hot", "4", "30", "decode is one wire",
              "FPGA, speed-critical, few states"],
             ["gray", "2", "—", "one bit changes per transition",
              "the state crosses a clock domain"]],
            widths=[1.0, 0.7, 0.7, 1.9, 2.5], size=8.8, bold_cols=(0,),
            align_center=False)

    w.callout("Read the measurement before repeating the folklore", [
        [N("On this generic gate library one-hot came out BIGGER, not smaller: four "
           "states need four flip-flops instead of two, and the next-state logic has "
           "to drive four bits instead of two. Thirty cells against thirteen.")],
        [N("One-hot is still usually right on an FPGA, where a flip-flop beside each "
           "lookup table is effectively free and the win is the short decode path — "
           "and it grows more attractive as the number of states rises, because "
           "binary decode logic grows faster than the extra registers do. Both "
           "statements are true. Neither is a rule. Measure your own target.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    # =============================================== a controller + a timer
    w.h2("3.5  A controller with a timer, and how to check it")

    w.image("traffic_states", width=6.4)

    w.para([N("A traffic-light controller for a two-road junction, with a car sensor "
              "on the minor road. The main road stays green until a car appears, "
              "then the sequence runs main-yellow, side-green, side-yellow and back. "
              "Green lasts six cycles and yellow two.")])

    w.callout("Where the timer lives, and why it is not a state", [
        [N("A six-cycle green phase does not mean six states, and a six-hundred-"
           "cycle one certainly does not. The count lives in a "), B("down-counter"),
         N(" — a datapath element — and the state machine only ever asks it one "
           "question: are you at zero yet?")],
        [N("That is section 3.1 again, in the smallest design in this topic. "
           "Measured: 75 cells and 10 flip-flops, of which 2 are the state and 8 are "
           "the timer.")],
    ], color=VIOLET, fill="F6F2FC", bar="7A4FBF")

    w.h3("Checking a property instead of reading a waveform")

    w.para([N("A traffic-light controller has safety requirements that are easy to "
              "state and tedious to check by eye. Write them once as code and the "
              "simulator checks them on every cycle of every run:")])

    w.code([
        "// P1 : the two roads are never green at the same time",
        "if (main_light == GREEN && side_light == GREEN) begin",
        "    $display(\"*** P1 VIOLATED at cycle %0d\", cycles);",
        "    errors = errors + 1;",
        "end",
        "",
        "// P2 : a green never goes straight to red - yellow comes first",
        "if (prev_main == GREEN && main_light == RED) begin",
        "    $display(\"*** P2 VIOLATED at cycle %0d\", cycles);",
        "    errors = errors + 1;",
        "end"])

    w.code([
        "$ make fsm",
        "  cycles checked      : 40",
        "  property violations : 0",
        "  PASS - mutual exclusion and yellow-before-red both hold"])

    w.para([N("This is the cheap half of formal verification, available in any "
              "simulator, in about ten lines. It scales to runs far longer than "
              "anyone would page through by hand, and — unlike a waveform you "
              "inspected once — it keeps working after you change the design. The "
              "expensive half, proving the property holds for "), B("every possible"),
            N(" input rather than the ones you tried, is what "), M("make prove"),
            N(" does with a SAT solver.")])

    # ============================================================== reuse
    w.h2("3.6  From a module to an IP")

    w.image("hierarchy_generate", width=6.4)

    w.para([N("Module 2's terminal outcomes ask you to design and develop IPs, and "
              "to characterise "), B("reusable"), N(" ones. Reusable means one source "
              "file that covers a family of widths and depths — not fourteen copies "
              "with the numbers edited. Three language features do all the work, and "
              "none of them exists in the hardware.")])

    w.table(["Feature", "What it is", "When it disappears"],
            [["parameter", "a compile-time constant the instantiator can override",
              "elaboration"],
             ["hierarchy", "a module instantiated inside another module",
              "flattening, if the tool flattens at all"],
             ["generate", "a compile-time loop that builds N copies of a structure",
              "elaboration"]],
            widths=[1.2, 3.8, 1.8], size=9.0, bold_cols=(0,), align_center=False)

    w.code([
        "module delayline #(parameter W = 8, parameter N = 4)",
        "                 (input clk, rst, en, input [W-1:0] din,",
        "                  output [W-1:0] dout);",
        "",
        "    wire [W-1:0] tap [0:N];        // one more element than stages",
        "    assign tap[0] = din;",
        "",
        "    genvar k;",
        "    generate",
        "        for (k = 0; k < N; k = k + 1) begin : stage",
        "            preg #(.W(W)) u_reg (.clk(clk), .rst(rst), .en(en),",
        "                                 .d(tap[k]), .q(tap[k+1]));",
        "        end",
        "    endgenerate",
        "",
        "    assign dout = tap[N];",
        "endmodule"],
        caption="rtl/reuse.v")

    w.code([
        "$ make reuse",
        "  delayline #(W=8, N) synthesised at four different depths:",
        "    N = 1                           8 cells     8 flip-flops",
        "    N = 2                          16 cells    16 flip-flops",
        "    N = 4                          32 cells    32 flip-flops",
        "    N = 8                          64 cells    64 flip-flops"])

    w.callout("The for loop is not a loop", [
        [N("It is an instruction to the "), B("elaborator"), N(": make N instances of "
           "preg and wire stage k's output to stage k+1's input. After elaboration "
           "there are N registers and no loop anywhere in the design. The measured "
           "table is the proof: eight flip-flops per stage, exactly N stages, "
           "linear.")],
        [N("The same run instantiates one parameterised counter twice, at different "
           "widths, to build a prescaler — and checks that it divides by exactly 16. "
           "That is all “hierarchy” means: a wire between two instances.")],
    ], color=TEAL)

    w.callout("Part 3 self-check", [
        [N("1.  What are the two halves of almost every block, and what crosses "
           "between them?")],
        [N("2.  Why keep the sample counter in the datapath rather than the "
           "controller?")],
        [N("3.  Name the three blocks of a state machine and say what each one is "
           "for.")],
        [N("4.  Why does a default assignment at the top of a block prevent a "
           "latch?")],
        [N("5.  What does the output logic read in a Moore machine? In a Mealy "
           "machine?")],
        [N("6.  How much later does a Moore output appear, and why is that ever "
           "acceptable?")],
        [N("7.  Did one-hot encoding cost more or less than binary here, and why?")],
        [N("8.  Why is the traffic light's phase timer not implemented as states?")],
        [N("9.  Write the property that says two roads are never both green.")],
        [N("10. Does a generate loop appear anywhere in the netlist?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
