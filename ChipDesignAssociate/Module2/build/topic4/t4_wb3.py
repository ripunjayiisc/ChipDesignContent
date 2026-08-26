# -*- coding: utf-8 -*-
"""Topic 4 workbook — Part 3: writing RTL for basic circuits, and verification."""
import _boot
from wbkit import *
from t4_wb1 import B, N, I, M


def build(w):
    w.page_break()
    w.h1("Part 3 · Writing RTL for Basic Digital Circuits")
    w.para("Parts 1 and 2 were the language and the craft. Part 3 is the practice: a catalogue of "
           "the standard blocks, a working method for verifying them, and two complete designs "
           "built end to end. Every file named here exists in Topic4_Lab and has been compiled, "
           "linted, simulated and synthesised.")

    # ---------------------------------------------------------- 3.1
    w.h2("3.1  The development loop")
    w.image("rtl_flow", 6.4, "Cheapest check first, every time.")
    w.numbered([
        "SPECIFY. Write down, in words, what the block does: its interface, its reset state, its "
        "throughput, its latency. If you cannot write it down you cannot design it.",
        "SKETCH. Draw the registers and the logic between them. Ten minutes here saves an "
        "afternoon later.",
        "CODE. Write the RTL from the sketch, following the coding standard in 1.18.",
        "LINT. One second. Catches width truncation, latches, unused and undriven signals.",
        "SIMULATE. A minute. Catches logic bugs. The testbench must print PASS or FAIL.",
        "SYNTHESISE. Longer. Catches structural bugs: latches, unexpected flip-flop counts, "
        "designs that cannot be built.",
        "READ THE LOG. Every time. The synthesis log is where the tool tells you your design does "
        "not mean what you thought.",
    ])
    w.callout("The order matters more than the tools",
              ["Students who skip lint and go straight to the waveform viewer spend hours chasing "
               "symptoms of a truncation that Verilator names in one second. Students who leave "
               "synthesis until the end discover their beautiful, fully-verified design contains "
               "forty latches and cannot meet timing. Lint, simulate, synthesise — always in that "
               "order."],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 3.2
    w.h2("3.2  The design catalogue")
    w.table(["Block", "File", "Core idiom", "Lab"],
            [["2:1 / 4:1 multiplexer", "mux2.v  mux4.v", "assign y = sel ? b : a;  /  case", "L1"],
             ["3-to-8 decoder", "decoder3to8.v", "y = 0; if (en) y[sel] = 1'b1;", "L1"],
             ["8-input priority encoder", "priority_encoder8.v", "casez with ? wildcards", "L1"],
             ["8-operation ALU with flags", "alu.v", "defaults + case; {1'b0,a}+{1'b0,b}", "L1"],
             ["7-segment decoder", "seven_seg.v", "case on the nibble, active-low output", "L1"],
             ["N-bit ripple adder", "adder_gen.v", "generate for + full_adder instances", "L1"],
             ["Register with enable", "reg_en.v", "if (!rst_n) ... else if (en) q <= d;", "L2"],
             ["Shift register", "shift_reg.v", "q <= {q[W-2:0], sin};", "L2"],
             ["Up/down counter", "counter.v", "q <= q + 1'b1; with wrap and load", "L2"],
             ["Edge detector", "edge_detect.v", "sig & ~sig_d", "L2"],
             ["CDC synchroniser", "synchroniser.v", "sync <= {sync[0], async_in};", "L2"],
             ["Switch debouncer", "debouncer.v", "counter + stable-for-N-cycles", "L2"],
             ["Clock divider / tick", "clk_divider.v", "counter + terminal-count pulse", "L2"],
             ["Traffic-light controller", "traffic_fsm.v", "three-block Moore FSM + timer", "L3"],
             ["Vending machine", "vending_fsm.v", "FSM with a credit datapath", "L3"],
             ["1011 sequence detector", "seq_detect_1011.v", "Moore AND Mealy, overlapping", "L3"],
             ["Synchronous FIFO", "sync_fifo.v", "dual pointers with an extra MSB", "L4"],
             ["Synchronous RAM", "sync_ram.v", "registered read infers block RAM", "L4"],
             ["UART transmitter", "uart_tx.v", "FSMD: shifter + bit timer + FSM", "L5"],
             ["UART receiver", "uart_rx.v", "half-bit alignment, mid-bit sampling", "L5"],
             ["Deliberately broken", "broken_examples.v", "latch, blocking, truncation", "all"]],
            widths=[1.9, 1.7, 2.4, 0.5], size=8.5, align_center=False)
    w.h3("Verified synthesis results")
    w.table(["Design", "Cells", "Flip-flops"],
            [["counter (4-bit, mod-10)", "38", "4"],
             ["traffic_fsm", "52", "12"],
             ["uart_tx", "120", "27"],
             ["uart_rx", "120", "36"],
             ["sync_fifo (8 × 8)", "255", "72"]],
            widths=[2.6, 1.2, 1.4], size=9.5)
    w.para("Before you run the tool on your own design, write down your prediction for the "
           "flip-flop count by counting the bits of state you declared. If the tool disagrees with "
           "you by more than a few, one of you is wrong, and it is worth finding out which.")

    # ---------------------------------------------------------- 3.3
    w.h2("3.3  Verification — the method")
    w.image("testbench_anatomy", 6.4, "The six parts every testbench has.")
    w.para("A testbench is a module with no ports. It creates a clock, drives the design, and "
           "decides — automatically — whether the answers were right. It is never synthesised, so "
           "the whole language is available to you.")
    w.callout("The rule that separates a testbench from a demonstration",
              [[B("A testbench must print PASS or FAIL, and its verdict must be readable by a "
                  "machine."),
                N("  If deciding whether a run was correct requires a human to look at a "
                  "waveform, you cannot put it in a regression, you cannot run it overnight, and "
                  "you will stop running it entirely within a week.")]],
              color=RED, fill="FDECEF", bar="C01F43")
    w.code([
        "`timescale 1ns / 1ps",
        "module tb_mux2;",
        "  reg  [7:0] a, b;  reg sel;  wire [7:0] y;",
        "  integer errors = 0;",
        "",
        "  mux2 #(.W(8)) u_dut (.a(a), .b(b), .sel(sel), .y(y));       // 1. instantiate",
        "",
        "  // 2. ONE place that decides pass or fail",
        "  task check(input [7:0] got, input [7:0] exp, input [255:0] msg);",
        "    if (got !== exp) begin",
        "      $display(\"FAIL %0t: %0s  got %h expected %h\", $time, msg, got, exp);",
        "      errors = errors + 1;",
        "    end",
        "  endtask",
        "",
        "  initial begin",
        "    $dumpfile(\"mux2.vcd\");  $dumpvars(0, tb_mux2);           // 3. waveform dump",
        "    a = 8'hA5; b = 8'h5A;",
        "    sel = 1'b0; #1 check(y, 8'hA5, \"sel=0 should pass a\");    // 4. stimulus + check",
        "    sel = 1'b1; #1 check(y, 8'h5A, \"sel=1 should pass b\");",
        "    if (errors == 0) $display(\"PASS - mux2\");                 // 5. verdict",
        "    else             $display(\"FAIL - %0d errors\", errors);",
        "    $finish;                                                  // 6. stop",
        "  end",
        "endmodule",
    ], caption="Everything a testbench needs, in 24 lines")
    w.para([N("Note "), M("!=="), N(" and not "), M("!="),
            N(". With the two-state operator, comparing against an x gives x, which is not true, "
              "so the check silently passes and the bug escapes. Always use "), M("==="),
            N(" and "), M("!=="), N(" in a testbench.")])

    w.h3("Clock and reset")
    w.code([
        "// A 100 MHz clock: 10 ns period, so toggle every 5 ns.",
        "localparam integer CLK = 10;",
        "initial clk = 1'b0;",
        "always #(CLK/2) clk = ~clk;",
        "",
        "// Reset: assert before the first edge, release BETWEEN edges.",
        "initial begin",
        "  rst_n = 1'b0;",
        "  repeat (3) @(posedge clk);",
        "  #(CLK/5) rst_n = 1'b1;      // released just AFTER an edge, never ON one",
        "end",
    ], caption="Clock and reset boilerplate")
    w.callout("A bug that cost real time while building this lab", [
        [N("The FSM testbench originally released reset exactly ON a clock edge. That is a race: "
           "reset and clock change at the same instant, the state register saw an ambiguous "
           "condition, and the state stayed x for two cycles. The sequence detector then found "
           "one match instead of two and the design looked broken. It was not.")],
        [B("Drive stimulus a small delay AFTER the active edge; sample a small delay BEFORE the "
           "next one. Never change an input at the same instant as the clock.")],
    ], color=RED, fill="FDECEF", bar="C01F43")

    w.h3("Reference models, scoreboards and randomisation")
    w.para("Hand-written expected values do not scale past about twenty cases. Beyond that you "
           "need a model that computes the right answer independently, and random stimulus to "
           "reach the corners you would never think of.")
    w.code([
        "// A scoreboard: an independent model of what should be inside the FIFO.",
        "reg [W-1:0] model [0:DEPTH-1];",
        "integer     mhead, mtail;",
        "function integer mcount; mcount = mtail - mhead; endfunction",
        "",
        "task fifo_push(input [W-1:0] dat);",
        "  begin",
        "    wr_en = 1'b1; wr_data = dat; @(posedge clk); #1 wr_en = 1'b0;",
        "    model[mtail % DEPTH] = dat;  mtail = mtail + 1;         // model, not DUT",
        "  end",
        "endtask",
        "",
        "// Randomised, but SEEDED -- so a failure reproduces exactly.",
        "for (k = 0; k < 200; k = k + 1) begin",
        "  if (($random(seed) % 2) == 0) begin if (!full)  fifo_push($random(seed)); end",
        "  else                          begin if (!empty) fifo_pop(); end",
        "  check1(count === mcount(), \"fifo count disagrees with the scoreboard\");",
        "end",
    ], caption="Topic4_Lab/tb/tb_mem.v")
    w.callout("Write the model from the specification, never from the RTL",
              ["A reference model derived by reading the design under test will happily agree "
               "with the design's bugs. If the same person must write both, write the model "
               "FIRST, from the specification, before looking at the implementation again."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h3("Coverage — what did you actually test?")
    w.para("A testbench that passes tells you nothing unless you know what it exercised. Even "
           "without formal coverage tools, keep a short list beside each testbench:")
    w.bullets([
        "Every state of every FSM entered at least once, and every transition taken.",
        "Every branch of every case taken, including the default.",
        "Boundaries: empty and full for a FIFO; 0 and MAX for a counter; the first and last bit "
        "of a frame.",
        "Back-to-back operations with no idle cycle between them.",
        "Reset asserted in the middle of an operation, not only at time zero.",
        "At least two different parameter values, if the module is parameterised — this is what "
        "caught the UART bug.",
    ])

    w.h3("Debugging")
    w.image("debug_ladder", 6.2, "Climb from the cheapest check to the most expensive.")
    w.numbered([
        "Read the error message. It usually names the file and line.",
        "Run lint. Verilator will name width and latch problems in one second.",
        "Read your own diff. What changed since it last worked?",
        "Add $display at the point of failure and print the inputs as well as the output.",
        "Open the waveform. Find the FIRST cycle where reality diverges from expectation — not "
        "the cycle where you noticed.",
        "Walk backwards from that signal to whatever drives it, and repeat.",
        "Synthesise. A latch or a surprising flip-flop count explains a whole class of symptoms "
        "that look like logic bugs.",
        "Reduce. Cut the testbench down to the smallest case that still fails. That case is "
        "usually the explanation.",
    ])
    w.para([M("$dumpvars(0, tb);"), N(" dumps every signal at every level — start there. "),
            M("$dumpvars(1, tb.u_dut);"),
            N(" dumps one level of one instance, for when the VCD gets too large to open.")])

    # ---------------------------------------------------------- 3.4
    w.h2("3.4  Design study 1 — a synchronous FIFO")
    w.image("fifo_structure", 5.8, "A memory and two pointers.")
    w.para("A FIFO is a memory plus a write pointer and a read pointer. The only genuinely hard "
           "part is distinguishing FULL from EMPTY, because in both cases the two pointers are at "
           "the same position. The classic solution is to give each pointer one extra bit.")
    w.code([
        "localparam integer AW = $clog2(DEPTH);",
        "reg [W-1:0] mem [0:DEPTH-1];",
        "reg [AW:0]  wr_ptr, rd_ptr;              // ONE EXTRA BIT each",
        "",
        "wire do_wr = wr_en & ~full;              // guard the pointers, not the caller",
        "wire do_rd = rd_en & ~empty;",
        "",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n) wr_ptr <= {(AW+1){1'b0}};",
        "  else if (do_wr) begin",
        "    mem[wr_ptr[AW-1:0]] <= wr_data;",
        "    wr_ptr <= wr_ptr + 1'b1;",
        "  end",
        "end",
        "",
        "assign rd_data = mem[rd_ptr[AW-1:0]];    // first-word-fall-through read",
        "assign empty   = (wr_ptr == rd_ptr);                     // identical, MSB included",
        "assign full    = (wr_ptr[AW] != rd_ptr[AW]) &&           // wrapped a different number",
        "                 (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);     //   of times, same position",
        "assign count   = wr_ptr - rd_ptr;        // subtraction wraps correctly, for free",
    ], caption="Topic4_Lab/rtl/sync_fifo.v — verified 255 cells, 72 FF at 8 × 8")
    w.bullets([
        "The extra MSB records how many times each pointer has wrapped. Equal in every bit means "
        "empty; equal in the address bits but different in the MSB means the writer is exactly one "
        "lap ahead — full.",
        "Guard inside the FIFO, not at the caller. A FIFO that silently corrupts itself when "
        "someone writes to it while full is a system-level bug waiting to happen.",
        "count is a plain subtraction of the extended pointers; the wraparound takes care of "
        "itself, and no separate counter register is needed.",
        "An ASYNCHRONOUS FIFO — two clock domains — needs Gray-coded pointers and synchronisers "
        "on each side. Same structure, considerably more care. That is a Topic 5 subject.",
    ])

    # ---------------------------------------------------------- 3.5
    w.h2("3.5  Design study 2 — a UART")
    w.image("uart_frame", 5.8, "8N1: idle high, start low, eight data bits LSB first, stop high.")
    w.para("The UART is the capstone because it forces every idea in this topic together: "
           "combinational logic, sequential logic, an FSM, a datapath, a clock-domain crossing "
           "and a self-checking testbench. There is no clock on the wire — both ends agree a bit "
           "rate in advance and the receiver recovers timing from the start bit. That is the whole "
           "design problem.")
    w.h3("Bit timing")
    w.para([M("CLKS_PER_BIT = f_clk / baud"), N(".  At 50 MHz and 115 200 baud that is 434.03, "
              "so 434. The 0.03 error accumulates to 0.3 of a bit over the ten bits of a frame, "
              "comfortably inside the tolerance a mid-bit sample gives you.")])
    w.h3("The transmitter")
    w.para("A shift register, a bit counter and a four-state FSM. On a start request it loads the "
           "byte, drives the start bit low for one bit time, shifts out eight bits LSB first, then "
           "drives the stop bit high. Verified: 120 cells, 27 flip-flops.")
    w.h3("The receiver — and its one trick")
    w.code([
        "// The incoming line is asynchronous. Synchronise it FIRST.",
        "synchroniser #(.STAGES(2)) u_sync (.clk(clk), .rst_n(rst_n),",
        "                                  .async_in(rx), .sync_out(rx_sync));",
        "",
        "case (state)",
        "  IDLE : begin",
        "           clk_cnt <= {CW{1'b0}};  bit_idx <= 3'd0;",
        "           if (!rx_sync) state <= START;                  // falling edge seen",
        "         end",
        "  START: if (clk_cnt == HALF_BIT[CW-1:0]) begin",
        "           if (!rx_sync) begin clk_cnt <= {CW{1'b0}}; state <= DATA; end  // genuine",
        "           else                state <= IDLE;                            // glitch",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "  DATA : if (clk_cnt == FULL_BIT[CW-1:0]) begin",
        "           clk_cnt <= {CW{1'b0}};",
        "           shifter <= {rx_sync, shifter[7:1]};            // LSB arrives first",
        "           if (bit_idx == 3'd7) state <= STOP;",
        "           else                 bit_idx <= bit_idx + 1'b1;",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "  STOP : if (clk_cnt == FULL_BIT[CW-1:0]) begin",
        "           rx_data     <= shifter;",
        "           rx_valid    <= 1'b1;",
        "           frame_error <= ~rx_sync;                       // stop bit must be high",
        "           state       <= IDLE;",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "endcase",
    ], caption="Topic4_Lab/rtl/uart_rx.v — verified 120 cells, 36 FF")
    w.callout("Sample in the middle, not at the edge",
              ["On seeing the start bit fall, wait HALF a bit time and re-check that the line is "
               "still low — that rejects a glitch. From then on, sample every FULL bit time and "
               "you land in the centre of every bit, with the maximum possible margin against a "
               "mismatch between the two ends' clocks."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")
    w.para("Three separate registers hold the state: the FSM state (2 bits), the clock counter "
           "(CW bits) and the bit index (3 bits). Counting those, plus the shifter and the "
           "outputs, is how you predict 36 flip-flops before you run the tool.")

    # ---------------------------------------------------------- 3.6
    w.h2("3.6  Two real bugs, and what they teach")
    w.h3("Bug 1 — width truncation in the UART")
    w.table(["Stage", "Detail"],
            [["Symptom", "The loopback test passed for 0x00 and 0x55 but failed for 0xFF, which "
                         "came back as 0xF7. One bit, in one pattern. The transmitter was "
                         "provably correct."],
             ["Cause", "The bit-timing limits were written CLKS_PER_BIT[CW-1:0]. The testbench "
                       "used CLKS_PER_BIT = 16 to keep runs short, so CW = $clog2(16) = 4 — and "
                       "16 does not fit in 4 bits. It truncated to ZERO. HALF_BIT became 0, so "
                       "the receiver never waited half a bit and sampled on bit BOUNDARIES."],
             ["Why some bytes", "Sampling on a boundary gives whichever value wins the race, "
                                "which only matters when adjacent bits DIFFER. Some patterns "
                                "survived and others did not: an intermittent, data-dependent "
                                "failure."],
             ["Fix", "Compute the limits as integers — localparam integer FULL_BIT = "
                     "CLKS_PER_BIT - 1; — and slice them where they are USED. Verified at "
                     "CLKS_PER_BIT = 16, 27 and 434, and clean under Verilator -Wall."]],
            widths=[1.1, 5.3], size=9, align_center=False)
    w.bullets([
        "A parameter used as an INDEX RANGE is not the same thing as a parameter used as a VALUE. "
        "Slicing a value that does not fit destroys it silently.",
        "Test at more than one parameter value. At 434 the bug is invisible, because 434 needs "
        "9 bits and CW is 9. Only the short test value exposed it.",
        [B("Verilator would have reported WIDTHTRUNC on that expression. Lint first, always.")],
    ])
    w.h3("Bug 2 — state timing in the vending machine")
    w.para("The credit register was cleared as the FSM ENTERED the DISPENSE state, so the output "
           "logic — which needs the credit to compute the change — saw zero. The fix is to clear "
           "it as the machine LEAVES that state:")
    w.code([
        "// WRONG -- cleared on entering DISPENSE, so the output logic sees 0",
        "if (next == DISPENSE || next == REFUND) cred <= 6'd0;",
        "",
        "// RIGHT -- cleared on leaving, so the outputs are valid while the state is active",
        "if (state == DISPENSE || state == REFUND) cred <= 6'd0;",
    ], caption="Topic4_Lab/rtl/vending_fsm.v")
    w.para("The lesson generalises: in a Moore machine the outputs are computed FROM the state you "
           "are currently in. Anything those outputs depend on must still be valid for the whole "
           "time you are in that state.")
    w.callout("The meta-lesson",
              ["Both bugs were found by a self-checking testbench, in seconds, and both would "
               "have been nearly impossible to find by staring at waveforms. Neither was a syntax "
               "error; both compiled and simulated cleanly. This is what verification is FOR — "
               "not to prove that code compiles, but to prove that it means what you intended."],
              color=TEAL)
