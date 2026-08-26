# -*- coding: utf-8 -*-
"""Topic 4 deck — 4C: writing RTL for basic digital circuits, verification, tools, labs."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def C(t, **kw):
    d = {"t": t}
    d.update(kw)
    return [d]


def build(d):
    # =============================================== SECTION 4C
    d.section_slide("SUBTOPIC 4C", "Writing RTL Code for Basic Digital Circuits",
                    "Twenty-two designs, five self-checking testbenches, one capstone. "
                    "Everything from here on exists as runnable code.",
                    ["The RTL development flow — specify, code, lint, simulate, synthesise",
                     "A catalogue of the standard blocks and how each is written",
                     "Verification: testbench anatomy, self-checking, scoreboards, randomisation",
                     "Two full designs: a synchronous FIFO and an 8N1 UART",
                     "Two real bugs, found while building this lab, and how they were caught"],
                    accent=VIOLET)

    # ============================================================ flow
    s = d.slide("TOPIC 4C · FLOW", "The Loop You Will Live In")
    y = d.lead(s, TOP, [[
        R("Every RTL block goes round this loop, and the order is not negotiable. ",
          b=True, c=NAVY, s=12.5),
        R("Lint takes one second and catches width bugs; simulation takes a minute and catches "
          "logic bugs; synthesis takes longer and catches structural bugs. Run them cheapest "
          "first.")]], h=594360)
    y = d.image(s, y + 45720, "rtl_flow", 3383280)
    d.card(s, y + G, "The order matters more than the tools",
           [[R("Students who skip lint and go straight to the waveform viewer spend hours "
               "chasing symptoms of a truncation Verilator would have named in one second. "
               "Students who skip synthesis until the end discover their beautiful, "
               "fully-verified design contains forty latches. ", b=True, c=AMBER),
             R("Lint, simulate, synthesise — every time, in that order.")]],
           accent=AMBER, fill=CARD_A, h=960120)

    # ============================================================ catalogue
    s = d.slide("TOPIC 4C · CATALOGUE", "The Standard Blocks — and the Idiom That Builds Each One")
    d.lead(s, TOP, [[
        R("Almost all digital design is assembling these. ", b=True, c=NAVY, s=12.5),
        R("Every row is a real, verified file in Topic4_Lab/rtl/.")]], h=411480)
    d.table(s, 1554480,
            ["Block", "File", "Core idiom", "Lab"],
            [["2:1 / 4:1 multiplexer", "mux2.v  mux4.v", "assign y = sel ? b : a;  /  case", "L1"],
             ["3-to-8 decoder", "decoder3to8.v", "y = 0; if (en) y[sel] = 1'b1;", "L1"],
             ["8-input priority encoder", "priority_encoder8.v", "casez with ? wildcards", "L1"],
             ["8-operation ALU + flags", "alu.v", "defaults + case; {1'b0,a}+{1'b0,b}", "L1"],
             ["7-segment decoder", "seven_seg.v", "case on the nibble, active-low output", "L1"],
             ["N-bit ripple adder", "adder_gen.v", "generate for + full_adder instances", "L1"],
             ["Register with enable", "reg_en.v", "if (!rst_n) ... else if (en) q <= d;", "L2"],
             ["Shift register", "shift_reg.v", "q <= {q[W-2:0], sin};", "L2"],
             ["Up/down counter", "counter.v", "q <= q + 1'b1; with wrap and load", "L2"],
             ["Edge detector", "edge_detect.v", "sig & ~sig_d", "L2"],
             ["CDC synchroniser", "synchroniser.v", "sync <= {sync[0], async_in};", "L2"],
             ["Switch debouncer", "debouncer.v", "counter + stable-for-N-cycles", "L2"],
             ["Clock divider / tick gen", "clk_divider.v", "counter + terminal-count pulse", "L2"]],
            [3017520, 2560320, 4663440, 1005840], rh=246888, bold_cols=(0,), size=9,
            col_colors={0: NAVY})

    # ============================================================ catalogue 2
    s = d.slide("TOPIC 4C · CATALOGUE", "…and the Bigger Blocks")
    d.lead(s, TOP, [[
        R("These are the designs where architecture starts to matter. ", b=True, c=NAVY, s=12.5),
        R("Each is a small system: a controller, a datapath, and a decision about how they "
          "communicate.")]], h=457200)
    y = d.table(s, 1600200,
                ["Block", "File", "Core idiom", "Lab"],
                [["Traffic-light controller", "traffic_fsm.v",
                  "three-block Moore FSM + dwell timer", "L3"],
                 ["Vending machine", "vending_fsm.v",
                  "FSM with a credit datapath and change", "L3"],
                 ["1011 sequence detector", "seq_detect_1011.v",
                  "Moore AND Mealy in one module, overlapping", "L3"],
                 ["Synchronous FIFO", "sync_fifo.v",
                  "dual pointers with an extra MSB; inferred RAM", "L4"],
                 ["Synchronous RAM", "sync_ram.v",
                  "mem[waddr] <= wdata; rdata <= mem[raddr];", "L4"],
                 ["UART transmitter", "uart_tx.v",
                  "FSMD: shift register + bit timer + FSM", "L5"],
                 ["UART receiver", "uart_rx.v",
                  "half-bit alignment, mid-bit sampling, CDC", "L5"]],
                [3017520, 2560320, 4663440, 1005840], rh=283464, bold_cols=(0,), size=9.5,
                col_colors={0: NAVY})
    d.card(s, y + G, "Verified synthesis results — you should be able to predict these",
           [[R("counter (4-bit): 38 cells, 4 FF   ·   traffic_fsm: 52 cells, 12 FF   ·   "
               "uart_tx: 120 cells, 27 FF   ·   uart_rx: 120 cells, 36 FF   ·   "
               "sync_fifo (8×8): 255 cells, 72 FF", b=True, c=NAVY)],
            [R("Before you run the tool on your own design, write down your prediction for the "
               "flip-flop count. Count the bits of state you declared. If the tool disagrees with "
               "you by more than a few, one of you is wrong — and it is worth finding out which.")]],
           accent=GREEN, fill=CARD_G, h=1188720)

    # ============================================================ seven seg / adder
    s = d.slide("TOPIC 4C · TWO SHORT DESIGNS", "A Display Decoder and a Generated Adder")
    y = d.cols(s, TOP, [
        ("seven_seg.v — a lookup table in case form",
         [[R("always @(*) begin", f=MONO_FONT, s=9.5)],
          [R("  seg = 7'b111_1111;      // all off", f=MONO_FONT, s=9.5)],
          [R("  case (nibble)", f=MONO_FONT, s=9.5)],
          [R("    4'h0: seg = 7'b100_0000;", f=MONO_FONT, s=9.5)],
          [R("    4'h1: seg = 7'b111_1001;", f=MONO_FONT, s=9.5)],
          [R("    ...", f=MONO_FONT, s=9.5)],
          [R("    default: seg = 7'b011_1111;  // '-'", f=MONO_FONT, s=9.5)],
          [R("  endcase", f=MONO_FONT, s=9.5)],
          [R("end", f=MONO_FONT, s=9.5)],
          [R("Active-LOW because the display's common anode is tied high — read the board "
             "schematic, not the datasheet's picture.", s=9.5, c=SLATE)]], TEAL, CARD),
        ("adder_gen.v — structure from a loop",
         [[R("genvar i;", f=MONO_FONT, s=9.5)],
          [R("assign c[0] = cin;", f=MONO_FONT, s=9.5)],
          [R("generate", f=MONO_FONT, s=9.5)],
          [R("  for (i=0;i<W;i=i+1) begin: bit_slice", f=MONO_FONT, s=9.5)],
          [R("    full_adder u_fa (.a(a[i]), .b(b[i]),", f=MONO_FONT, s=9.5)],
          [R("      .cin(c[i]), .sum(sum[i]),", f=MONO_FONT, s=9.5)],
          [R("      .cout(c[i+1]));", f=MONO_FONT, s=9.5)],
          [R("  end", f=MONO_FONT, s=9.5)],
          [R("endgenerate", f=MONO_FONT, s=9.5)],
          [R("W full-adder instances chained by the carry. Slow for large W — the carry ripples "
             "— which is exactly the point of the experiment.", s=9.5, c=SLATE)]],
         GREEN, CARD_G)], h=3383280)
    d.card(s, y + G, "Experiment for Lab L1",
           [[R("Synthesise adder_gen at W = 4, 16 and 64 and watch the longest path grow "
               "linearly with W. Then look up carry-lookahead and carry-select adders and ask "
               "why a synthesiser given "),
             R("assign sum = a + b;", f=MONO_FONT, b=True, c=GREEN),
             R(" will usually produce something faster than your hand-written ripple chain. "
               "Lesson: describe intent, let the tool choose the structure — unless you have a "
               "specific reason not to.")]],
           accent=AMBER, fill=CARD_A, h=1051560)

    # =============================================== VERIFICATION
    d.section_slide("TOPIC 4C · VERIFICATION",
                    "Simulating and Verifying the Functionality of RTL Designs",
                    "The syllabus names this as a practical outcome in its own right. "
                    "Untested RTL is not a design; it is a guess.",
                    ["Testbench anatomy — the six parts every testbench has",
                     "Self-checking: never read a waveform to decide if a test passed",
                     "Reference models, scoreboards and randomised stimulus",
                     "Waveform debugging, and the debug ladder to climb when stuck"],
                    accent=AMBER)

    # ============================================================ tb anatomy
    s = d.slide("TOPIC 4C · TESTBENCH", "Anatomy of a Testbench")
    y = d.lead(s, TOP, [[
        R("A testbench is a module with no ports. ", b=True, c=NAVY, s=12.5),
        R("It creates a clock, drives the design, and decides — automatically — whether the "
          "answers were right. It is NOT synthesised, so the whole language is available to you.")]],
        h=548640)
    y = d.image(s, y + 45720, "testbench_anatomy", 3383280)
    d.card(s, y + G, "The rule that separates a testbench from a demo",
           [[R("A testbench must print PASS or FAIL and must be readable by a machine. ",
               b=True, c=RED),
             R("If deciding whether the run was correct requires a human to look at a waveform, "
               "you cannot run it in a regression, you cannot run it overnight, and you will stop "
               "running it entirely within a week.")]],
           accent=RED, fill=CARD_R, h=868680)

    # ============================================================ minimal tb
    s = d.slide("TOPIC 4C · TESTBENCH", "A Complete, Minimal, Self-Checking Testbench")
    y = d.code(s, TOP, [
        "`timescale 1ns / 1ps",
        "module tb_mux2;",
        "  reg  [7:0] a, b;  reg sel;  wire [7:0] y;",
        "  integer errors = 0;",
        "",
        "  mux2 #(.W(8)) u_dut (.a(a), .b(b), .sel(sel), .y(y));      // 1. instantiate",
        "",
        C("  // 2. one place that decides pass or fail", c=CMT),
        "  task check(input [7:0] got, input [7:0] exp, input [255:0] msg);",
        "    if (got !== exp) begin",
        "      $display(\"FAIL %0t: %0s  got %h expected %h\", $time, msg, got, exp);",
        "      errors = errors + 1;",
        "    end",
        "  endtask",
        "",
        "  initial begin",
        "    $dumpfile(\"mux2.vcd\");  $dumpvars(0, tb_mux2);          // 3. waveform dump",
        "    a = 8'hA5; b = 8'h5A;",
        "    sel = 1'b0; #1 check(y, 8'hA5, \"sel=0 should pass a\");   // 4. stimulus + check",
        "    sel = 1'b1; #1 check(y, 8'h5A, \"sel=1 should pass b\");",
        "    if (errors == 0) $display(\"PASS - mux2\");                // 5. verdict",
        "    else             $display(\"FAIL - %0d errors\", errors);",
        "    $finish;                                                 // 6. stop",
        "  end",
        "endmodule",
    ], size=9, title="Everything a testbench needs, in 24 lines")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Note ", s=10.5), R("!==", f=MONO_FONT, b=True, c=GREEN, s=10.5),
        R(" not ", s=10.5), R("!=", f=MONO_FONT, b=True, c=RED, s=10.5),
        R(" — the four-state comparison. With ", s=10.5),
        R("!=", f=MONO_FONT, b=True, c=RED, s=10.5),
        R(", comparing against an x gives x, which is not true, so the check silently passes. "
          "Always use === and !== in a testbench.", s=10.5)]])

    # ============================================================ clock & reset
    s = d.slide("TOPIC 4C · TESTBENCH", "Clock, Reset, and When to Drive and Sample")
    y = d.code(s, TOP, [
        C("// A 100 MHz clock: 10 ns period, so toggle every 5 ns.", c=CMT),
        "localparam integer CLK = 10;",
        "initial clk = 1'b0;",
        "always #(CLK/2) clk = ~clk;",
        "",
        C("// Reset: assert before the first edge, release BETWEEN edges.", c=CMT),
        "initial begin",
        "  rst_n = 1'b0;",
        "  repeat (3) @(posedge clk);",
        "  #(CLK/5) rst_n = 1'b1;      // released just after an edge, not ON one",
        "end",
    ], size=10, title="The clock and reset boilerplate")
    y = d.card(s, y + G, "A bug that cost real time while building this lab",
           [[R("The FSM testbench originally released reset exactly ON a clock edge. ",
               b=True, c=RED),
             R("That is a race: the reset and the clock change at the same instant, so the state "
               "register saw an ambiguous condition and the state stayed x for two cycles. The "
               "sequence detector then found one match instead of two, and the design looked "
               "broken. It was not.")],
            [R("Rule: ", b=True, c=GREEN),
             R("drive stimulus a small delay AFTER the active edge, and sample a small delay "
               "BEFORE the next one. Never change an input at the same instant as the clock.")]],
           accent=RED, fill=CARD_R, h=1188720)
    d.card(s, y + G, "Timescale matters",
           [[R("`timescale 1ns / 1ps", f=MONO_FONT, b=True, c=NAVY),
             R("  means the unit of #1 is a nanosecond and the simulator rounds to a picosecond. "
               "Change the first number and every delay in the file changes meaning. Put the same "
               "timescale in every file, or put it in one included header.")]],
           accent=TEAL, h=822960)

    # ============================================================ scoreboard
    s = d.slide("TOPIC 4C · VERIFICATION", "Reference Models, Scoreboards and Randomisation")
    y = d.lead(s, TOP, [[
        R("Hand-written expected values do not scale past about twenty cases. ",
          b=True, c=NAVY, s=12.5),
        R("Beyond that you need a model that computes the right answer independently, and random "
          "stimulus to reach the corners you would never think of.")]], h=548640)
    y = d.code(s, y + 45720, [
        C("// A scoreboard: an independent model of what should be inside the FIFO.", c=CMT),
        "reg [W-1:0] model [0:DEPTH-1];",
        "integer     mhead, mtail;",
        "function integer mcount; mcount = mtail - mhead; endfunction",
        "",
        "task fifo_push(input [W-1:0] dat);",
        "  begin",
        "    wr_en = 1'b1; wr_data = dat; @(posedge clk); #1 wr_en = 1'b0;",
        "    model[mtail % DEPTH] = dat;  mtail = mtail + 1;      // model, not DUT",
        "  end",
        "endtask",
        "",
        C("// Randomised, but SEEDED -- so a failure reproduces exactly.", c=CMT),
        "for (k = 0; k < 200; k = k + 1) begin",
        "  if (($random(seed) % 2) == 0) begin if (!full) fifo_push($random(seed)); end",
        "  else                          begin if (!empty) fifo_pop(); end",
        "  check1(count === mcount(), \"fifo count disagrees with the scoreboard\");",
        "end",
    ], size=9, title="Topic4_Lab/tb/tb_mem.v (extract)")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("The model must be written from the SPECIFICATION, never by reading the RTL. ",
          s=10.5, b=True, c=RED),
        R("A model derived from the design under test will happily agree with the design's bugs.",
          s=10.5)]])

    # ============================================================ debug
    s = d.slide("TOPIC 4C · DEBUG", "When It Does Not Work — Climb the Ladder")
    y = d.lead(s, TOP, [[
        R("Debugging RTL is not guessing; it is a procedure. ", b=True, c=NAVY, s=12.5),
        R("Work from the cheapest check to the most expensive, and always find the FIRST moment "
          "the design went wrong, never the moment you noticed.")]], h=548640)
    y = d.image(s, y + 45720, "debug_ladder", 3383280)
    d.cols(s, y + G, [
        ("Chasing an x",
         [[R("x is contagious — by the time you see it on your output it may have travelled "
             "through ten signals. In GTKWave, add the suspect signal, find the FIRST edge where "
             "it goes x, then add whatever drives it and repeat. You are looking for the source, "
             "not the symptom.", s=10.5)]], VIOLET, CARD),
        ("Reading a VCD",
         [[R("$dumpvars(0, tb);", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  dumps every signal at every level — start there. ", s=10.5),
           R("$dumpvars(1, tb.u_dut);", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  dumps one level of one instance, for when the file gets too big to open.",
             s=10.5)]], GREEN, CARD_G)], h=1188720)

    # ============================================================ FIFO
    s = d.slide("TOPIC 4C · DESIGN 1", "A Synchronous FIFO — Pointers, and the Extra Bit")
    y = d.lead(s, TOP, [[
        R("A FIFO is a memory plus two pointers. ", b=True, c=NAVY, s=12.5),
        R("The only hard part is telling FULL from EMPTY: in both cases the two pointers are "
          "equal. The classic solution is to give each pointer one extra bit.")]], h=548640)
    y = d.image(s, y + 45720, "fifo_structure", 2743200)
    y = d.code(s, y + G, [
        "reg [AW:0] wr_ptr, rd_ptr;                  // AW+1 bits for a 2**AW-deep FIFO",
        "assign empty = (wr_ptr == rd_ptr);                       // identical, MSB included",
        "assign full  = (wr_ptr[AW] != rd_ptr[AW]) &&             // wrapped a different number",
        "               (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);       //   of times, same position",
        "assign count = wr_ptr - rd_ptr;             // subtraction wraps correctly, for free",
    ], size=9.5, title="Topic4_Lab/rtl/sync_fifo.v — verified 255 cells, 72 FF at 8×8")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Guard the pointers, not the caller: ", s=10.5, b=True, c=NAVY),
        R("wr_en & ~full", f=MONO_FONT, b=True, c=GREEN, s=10.5),
        R(" and ", s=10.5), R("rd_en & ~empty", f=MONO_FONT, b=True, c=GREEN, s=10.5),
        R(". A FIFO that silently corrupts itself when someone writes to it while full is a "
          "system-level bug waiting to happen.", s=10.5)]])

    # ============================================================ UART frame
    s = d.slide("TOPIC 4C · DESIGN 2", "A UART — the 8N1 Frame")
    y = d.lead(s, TOP, [[
        R("The UART is the capstone because it forces every idea in this topic together. ",
          b=True, c=NAVY, s=12.5),
        R("There is no clock on the wire: both ends agree a bit rate in advance and the receiver "
          "recovers timing from the start bit. That is the whole design problem.")]], h=594360)
    y = d.image(s, y + 45720, "uart_frame", 2560320)
    d.cols(s, y + G, [
        ("8N1, and how you count clocks",
         [[R("Idle high · one START bit low · eight DATA bits, LSB first · no parity · one STOP "
             "bit high. Ten bit times per byte.", s=10.5)],
          [R("CLKS_PER_BIT = f_clk / baud", f=MONO_FONT, b=True, c=NAVY, s=10.5)],
          [R("50 MHz / 115200 = 434.03 → 434. The 0.03 error accumulates to 0.3 of a bit over "
             "ten bits: comfortably inside tolerance.", s=10.5)]], TEAL, CARD),
        ("The receiver's one trick",
         [[R("Sample each bit in its MIDDLE, not at its edge. ", b=True, c=GREEN, s=10.5),
           R("On seeing the start bit fall, wait HALF a bit time and re-check the line is still "
             "low — that rejects a glitch. From then on, sample every FULL bit time and you land "
             "in the centre of every bit, with maximum margin against clock mismatch.",
             s=10.5)]], GREEN, CARD_G)], h=1371600)

    # ============================================================ UART rx code
    s = d.slide("TOPIC 4C · DESIGN 2", "The Receiver — an FSMD in Four States")
    y = d.code(s, TOP, [
        "synchroniser #(.STAGES(2)) u_sync (.clk(clk), .rst_n(rst_n),",
        "                                  .async_in(rx), .sync_out(rx_sync));  // CDC first!",
        "case (state)",
        "  IDLE : begin",
        "           clk_cnt <= {CW{1'b0}};  bit_idx <= 3'd0;",
        "           if (!rx_sync) state <= START;              // falling edge seen",
        "         end",
        "  START: if (clk_cnt == HALF_BIT[CW-1:0]) begin",
        "           if (!rx_sync) begin clk_cnt <= {CW{1'b0}}; state <= DATA; end  // genuine",
        "           else                state <= IDLE;                            // glitch",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "  DATA : if (clk_cnt == FULL_BIT[CW-1:0]) begin",
        "           clk_cnt <= {CW{1'b0}};",
        "           shifter <= {rx_sync, shifter[7:1]};        // LSB arrives first",
        "           if (bit_idx == 3'd7) state <= STOP; else bit_idx <= bit_idx + 1'b1;",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "  STOP : if (clk_cnt == FULL_BIT[CW-1:0]) begin",
        "           rx_data <= shifter;  rx_valid <= 1'b1;",
        "           frame_error <= ~rx_sync;                   // stop bit must be high",
        "           state <= IDLE;",
        "         end else clk_cnt <= clk_cnt + 1'b1;",
        "endcase",
    ], size=9, title="Topic4_Lab/rtl/uart_rx.v — verified 120 cells, 36 FF")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Three separate registers hold the state: the FSM state (2 bits), the clock counter "
          "(CW bits) and the bit index (3 bits). Counting those, plus the shifter and outputs, is "
          "how you predict 36 flip-flops before you run the tool.", s=10.5, i=True, c=SLATE)]])

    # ============================================================ UART bug
    s = d.slide("TOPIC 4C · CASE STUDY", "The Bug That Made Some Bytes Work and Others Not", RED)
    y = d.lead(s, TOP, [[
        R("This is a genuine bug found while writing this lab, kept because it is better "
          "teaching material than anything invented. ", b=True, c=NAVY, s=12.5),
        R("Read the symptom first and try to name the cause before turning to the next line.")]],
        h=594360)
    y = d.tiers(s, y + 45720, [
        ("SYMPTOM", "The loopback test passed for 0x00 and 0x55 but failed for 0xFF — which came "
                    "back as 0xF7. One bit, in one pattern. Everything else about the design "
                    "looked correct, and the transmitter was provably fine.", RED),
        ("CAUSE", "The bit-timing limits were written CLKS_PER_BIT[CW-1:0]. The testbench used "
                  "CLKS_PER_BIT = 16 to keep runs short, so CW = $clog2(16) = 4 — and 16 does not "
                  "fit in 4 bits. It truncated to ZERO. HALF_BIT became 0, so the receiver never "
                  "waited half a bit and sampled on bit BOUNDARIES instead of bit centres.",
         AMBER),
        ("WHY SOME BYTES", "Sampling on a boundary gives whichever value wins the race — which "
                           "only matters when adjacent bits DIFFER. 0x00 and 0xFF-with-a-low-start-"
                           "bit differ in different places, so some patterns survived and others "
                           "did not. Intermittent, data-dependent failure: the worst kind.", VIOLET),
        ("FIX", "Compute the limits as integers — localparam integer FULL_BIT = CLKS_PER_BIT - 1; "
                "— and slice them where they are USED. Verified at CLKS_PER_BIT = 16, 27 and 434. "
                "Verilator -Wall is clean on this form and flagged the alternatives.", GREEN),
    ], h=731520, gap=45720)
    d.card(s, y + G, "How it was actually caught, and what would have caught it sooner",
           [[R("It was caught by the loopback testbench, which compares the received byte with "
               "the byte that was sent — in one second, with no waveform. It would have been "
               "caught EARLIER by ", ),
             R("verilator --lint-only -Wall", f=MONO_FONT, b=True, c=GREEN),
             R(", which reports WIDTHTRUNC on exactly that expression. Lint costs a second; this "
               "bug cost an hour.")]],
           accent=TEAL, h=960120)

    # ============================================================ lessons
    s = d.slide("TOPIC 4C · CASE STUDY", "What Those Two Bugs Actually Teach")
    y = d.cols(s, TOP, [
        ("Bug 1 — width truncation in the UART",
         [[R("· A parameter used as an INDEX RANGE is not the same as a parameter used as a "
             "VALUE. Slicing a value that does not fit destroys it silently.", s=10.5)],
          [R("· Test at more than one parameter value. ", b=True, c=NAVY, s=10.5),
           R("At 434 the bug is invisible, because 434 needs 9 bits and CW is 9. Only the short "
             "test value exposed it.", s=10.5)],
          [R("· Verilator would have said WIDTHTRUNC. Lint first, always.", s=10.5, c=GREEN,
             b=True)]], RED, CARD_R),
        ("Bug 2 — state timing in the vending machine",
         [[R("· The credit register was cleared as the FSM ENTERED the DISPENSE state, so the "
             "output logic — which needs the credit to compute change — saw zero.", s=10.5)],
          [R("· The fix is to clear it as the machine LEAVES that state.", s=10.5, b=True,
             c=NAVY)],
          [R("· Lesson: in a Moore machine the outputs are computed FROM the state you are in. "
             "Anything that state's outputs depend on must still be valid while you are in it.",
             s=10.5, c=GREEN, b=True)]], AMBER, CARD_A)], h=2560320)
    d.card(s, y + G, "The meta-lesson worth stating out loud to the class",
           [[R("Both bugs were found by a self-checking testbench, in seconds, and both would "
               "have been nearly impossible to find by looking at waveforms alone. ",
               b=True, c=TEAL),
             R("Neither was a syntax error; both compiled and simulated cleanly. This is what "
               "verification is FOR.")]],
           accent=TEAL, h=868680)

    # =============================================== TOOLS SECTION
    d.section_slide("TOPIC 4 · TOOLS", "Software Tools — Installation and Flow",
                    "The syllabus specifies Vivado Design Suite and ModelSim. The open-source "
                    "chain does the same jobs and runs on any laptop.",
                    ["What each tool does, and which one to reach for first",
                     "Installing the open-source chain — Linux, WSL2, macOS",
                     "Installing and driving Vivado Design Suite",
                     "Installing and driving ModelSim / Questa",
                     "A one-page command reference to keep beside the keyboard"],
                    accent=NAVY)

    # ============================================================ toolchains
    s = d.slide("TOPIC 4 · TOOLS", "Four Jobs, Several Tools for Each")
    y = d.lead(s, TOP, [[
        R("Every flow does the same four jobs. ", b=True, c=NAVY, s=12.5),
        R("Only the command names change. Learn the jobs and moving between vendors becomes a "
          "morning's work rather than a new skill.")]], h=502920)
    y = d.image(s, y + 45720, "toolchains", 3200400)
    d.table(s, y + G,
            ["Job", "Open-source", "Vendor (syllabus)", "What it tells you"],
            [["Lint / static check", "Verilator --lint-only", "Vivado report_methodology",
              "Width bugs, latches, unused signals — in one second"],
             ["Simulate", "Icarus Verilog (iverilog/vvp)", "ModelSim, Questa, Vivado xsim",
              "Does it behave correctly?"],
             ["View waveforms", "GTKWave", "ModelSim wave window, Vivado sim",
              "Where and when it went wrong"],
             ["Synthesise", "Yosys", "Vivado synth_design",
              "What hardware it becomes; area; latch warnings"]],
            [2194560, 2926080, 2926080, 3200400], rh=329184, bold_cols=(0,), size=9.5,
            col_colors={0: NAVY})

    # ============================================================ install OSS
    s = d.slide("TOPIC 4 · INSTALL", "The Open-Source Toolchain — Every Command")
    y = d.code(s, TOP, [
        C("# ---- Ubuntu / Debian / WSL2 -------------------------------------------", c=CMT),
        "sudo apt update",
        "sudo apt install -y iverilog gtkwave verilator yosys graphviz",
        "",
        C("# ---- macOS (Homebrew) --------------------------------------------------", c=CMT),
        "brew install icarus-verilog gtkwave verilator yosys graphviz",
        "",
        C("# ---- Windows -----------------------------------------------------------", c=CMT),
        "#  Best:  install WSL2 (wsl --install in an admin PowerShell), then use",
        "#         the Ubuntu commands above inside it.",
        "#  Or:    download the OSS CAD Suite release for Windows, unzip it, and",
        "#         run its start.bat -- it contains all four tools, already built.",
        "",
        C("# ---- verify the installation -------------------------------------------", c=CMT),
        "iverilog -V | head -1        # Icarus Verilog version 12.0",
        "verilator --version          # Verilator 5.020",
        "yosys -V                     # Yosys 0.33",
        "gtkwave --version",
    ], size=9.5, title="Copy-paste installation")
    d.card(s, y + G, "GTKWave on WSL2",
           [[R("GTKWave is a GUI. On Windows 11, WSLg runs Linux GUI applications with no extra "
               "setup — just type ", ),
             R("gtkwave dump.vcd", f=MONO_FONT, b=True, c=GREEN),
             R(". On Windows 10 you need an X server (VcXsrv) and "),
             R("export DISPLAY=:0", f=MONO_FONT, b=True, c=NAVY),
             R(", or simply install the native Windows GTKWave and open the .vcd file the WSL "
               "side wrote.")]],
           accent=TEAL, h=960120)

    # ============================================================ oss commands
    s = d.slide("TOPIC 4 · TOOLS", "Driving the Open-Source Chain — Four Commands")
    y = d.code(s, TOP, [
        C("# 1. LINT -- one second, run it before anything else", c=CMT),
        "verilator --lint-only -Wall -Wno-DECLFILENAME rtl/*.v",
        "",
        C("# 2. COMPILE + SIMULATE", c=CMT),
        "iverilog -g2005 -Wall -o build/sim.vvp rtl/uart_tx.v rtl/uart_rx.v \\",
        "         rtl/synchroniser.v tb/tb_uart.v",
        "vvp build/sim.vvp                       # prints PASS or FAIL",
        "",
        C("# 3. VIEW WAVEFORMS  (the testbench must call $dumpfile/$dumpvars)", c=CMT),
        "gtkwave uart.vcd &",
        "",
        C("# 4. SYNTHESISE and look for latches", c=CMT),
        "yosys -p \"read_verilog rtl/counter.v; synth -top counter; stat\"",
        "yosys -p \"read_verilog rtl/counter.v; synth -top counter\" 2>&1 | grep -i latch",
        "",
        C("# ... or just use the scripts, which do all of the above for every lab", c=CMT),
        "./scripts/lint.sh   &&  ./scripts/run_all.sh  &&  ./scripts/synth_all.sh",
    ], size=9.5, title="Topic4_Lab — these exact commands were used to verify this material")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Expected output: ", s=10.5, b=True, c=NAVY),
        R("LINT CLEAN", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("  ·  ", s=10.5),
        R("ALL LABS PASSED", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("  ·  ", s=10.5),
        R("ALL DESIGNS SYNTHESISED, NO LATCHES INFERRED", f=MONO_FONT, b=True, c=GREEN, s=10.5)]])

    # ============================================================ vivado install
    s = d.slide("TOPIC 4 · INSTALL", "Vivado Design Suite — Installation")
    y = d.lead(s, TOP, [[
        R("Vivado is the tool named in the syllabus. ", b=True, c=NAVY, s=12.5),
        R("The free ML Standard edition covers every device you will use on a training board. "
          "Budget an afternoon: the download is large and the installer is slow.")]], h=548640)
    y = d.bullets(s, y + 45720, [
        [R("1. Create a free AMD/Xilinx account, then download the ", s=10.5),
         R("Unified Installer", b=True, c=NAVY, s=10.5),
         R(" for Windows or Linux from the AMD downloads page.", s=10.5)],
        [R("2. Run it and choose ", s=10.5),
         R("Vivado → Vivado ML Standard", b=True, c=GREEN, s=10.5),
         R(" (free, no licence file needed).", s=10.5)],
        [R("3. On the device page select ONLY the family your board uses — ", s=10.5),
         R("Artix-7", b=True, c=NAVY, s=10.5),
         R(" for Basys 3 / Arty A7, ", s=10.5), R("Zynq-7000", b=True, c=NAVY, s=10.5),
         R(" for Zybo / PYNQ. Selecting everything costs well over 100 GB.", s=10.5)],
        [R("4. Keep ", s=10.5), R("Vivado Simulator (xsim)", b=True, c=GREEN, s=10.5),
         R(" and, on Windows, the ", s=10.5), R("Cable Drivers", b=True, c=GREEN, s=10.5),
         R(" — without the drivers the board will not be detected.", s=10.5)],
        [R("5. Disk: allow 60–100 GB for one device family. RAM: 8 GB minimum, 16 GB "
           "comfortable.", s=10.5)],
        [R("6. Linux only: run ", s=10.5),
         R("sudo <install>/data/xicom/cable_drivers/lin64/install_script/install_drivers/install_drivers",
           f=MONO_FONT, b=True, c=NAVY, s=9),
         R(" after installation.", s=10.5)],
        [R("7. Verify: ", s=10.5), R("vivado -version", f=MONO_FONT, b=True, c=GREEN, s=10.5),
         R("  (source ", s=10.5), R("settings64.sh", f=MONO_FONT, s=10.5),
         R(" first on Linux).", s=10.5)],
    ], accent=NAVY, step=320040)
    y = d.cols(s, y + G, [
        ("Boards commonly used for this course",
         [[R("Basys 3", b=True, c=NAVY, s=10.5),
           R("  — Artix-7 xc7a35tcpg236-1. Switches, LEDs, four 7-segment digits. Ideal for "
             "L1–L3.", s=10.5)],
          [R("Arty A7 / Nexys A7", b=True, c=NAVY, s=10.5),
           R("  — Artix-7, with a USB-UART bridge, so L5 talks to a terminal on the PC.",
             s=10.5)],
          [R("Zybo / PYNQ-Z2", b=True, c=NAVY, s=10.5),
           R("  — Zynq-7000. More than this topic needs, but the same flow.", s=10.5)]],
         TEAL, CARD),
        ("Installation problems you will meet",
         [[R("· Installer hangs at 'Generating installed device list' — it is not hung, it takes "
             "several minutes.", s=10.5)],
          [R("· Board not detected — the cable drivers were skipped, or on Linux the udev rules "
             "were not installed.", s=10.5)],
          [R("· 'No such part' from a TCL script — the part string does not match your board. "
             "Edit it in vivado_synth.tcl.", s=10.5)]], AMBER, CARD_A),
        ("Plan the lab session around this",
         [[R("Do not spend a scheduled lab hour installing Vivado. Either pre-install it on the "
             "machines, or set the download running at the start of the session and teach the "
             "open-source flow — which installs in under a minute — while it runs. The concepts "
             "are identical, and the students are learning RTL, not an installer.", s=10.5)]],
         RED, CARD_R)], h=2011680)

    # ============================================================ vivado flow
    s = d.slide("TOPIC 4 · VIVADO", "The Vivado Flow — GUI and Batch")
    y = d.image(s, TOP, "vivado_flow", 3017520)
    y = d.code(s, y + G, [
        C("# Batch simulation -- three tools, always in this order", c=CMT),
        "xvlog rtl/uart_tx.v rtl/uart_rx.v rtl/synchroniser.v tb/tb_uart.v   # analyse",
        "xelab -debug typical tb_uart -s tb_uart_sim                          # elaborate",
        "xsim tb_uart_sim -runall                                             # run",
        "",
        C("# Batch synthesis with the provided script", c=CMT),
        "vivado -mode batch -source scripts/vivado_synth.tcl -tclargs uart_tx",
    ], size=9.5, title="Topic4_Lab/scripts/vivado_sim.tcl and vivado_synth.tcl")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("In the GUI the same steps are Create Project → Add Sources → Run Simulation → Run "
          "Synthesis → Open Synthesized Design. Learn the batch commands anyway: they are what "
          "you put in a makefile, and they are what a regression runs.", s=10.5)]])

    # ============================================================ vivado reports
    s = d.slide("TOPIC 4 · VIVADO", "What to Read After Synthesis — Not the Schematic")
    y = d.code(s, TOP, [
        "create_clock -period 20.000 -name clk [get_ports clk]   # 50 MHz, or timing means nothing",
        "synth_design -top uart_tx -part xc7a35tcpg236-1",
        "report_utilization    -file build/vivado/uart_tx_utilization.rpt",
        "report_timing_summary -file build/vivado/uart_tx_timing.rpt",
    ], size=10, title="scripts/vivado_synth.tcl — change the part to match your board")
    y = d.cols(s, y + G, [
        ("Utilisation report",
         [[R("LUTs, flip-flops, block RAMs, DSPs. Compare the flip-flop count with your own "
             "prediction from the source — a large disagreement means the tool built something "
             "you did not intend.", s=10.5)]], TEAL, CARD),
        ("Timing summary",
         [[R("Worst negative slack (WNS). Positive means the design meets the clock you "
             "constrained; negative means it does not, and the number tells you by how much. "
             "Without a create_clock the report is meaningless.", s=10.5)]], GREEN, CARD_G),
        ("Messages tab",
         [[R("Every ", s=10.5), R("[Synth 8-xxx]", f=MONO_FONT, b=True, c=AMBER, s=10.5),
           R(" warning. Read all of them once. Latch inference, width mismatch and unconnected "
             "port warnings all live here.", s=10.5)]], AMBER, CARD_A)], h=1554480)
    d.card(s, y + G, "Honesty note for the trainer",
           [[R("The Vivado and ModelSim scripts in Topic4_Lab are working templates written from "
               "standard, version-stable commands, but they were NOT executed while this material "
               "was prepared — neither tool was installed in the authoring environment. Everything "
               "quoted from Icarus, Verilator and Yosys was really run. Check the vendor scripts "
               "against your installed version before the session; part numbers and menu names "
               "change between releases.")]],
           accent=RED, fill=CARD_R, h=1005840)

    # ============================================================ modelsim
    s = d.slide("TOPIC 4 · MODELSIM", "ModelSim / Questa — Installation and Flow")
    y = d.cols(s, TOP, [
        ("Installing",
         [[R("· ModelSim Intel FPGA Starter Edition is free and needs no licence; it ships with "
             "Intel Quartus Prime Lite. Questa Intel FPGA Starter is its successor — either is "
             "fine for this course.", s=10.5)],
          [R("· Windows: run the installer, accept the default path. Linux: it is 32-bit, so "
             "install the multilib packages ", s=10.5),
           R("lib32z1 lib32ncurses6 libxft2:i386", f=MONO_FONT, b=True, c=NAVY, s=9.5),
           R(" first or vsim will not start.", s=10.5)],
          [R("· Verify with ", s=10.5), R("vsim -version", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R(".", s=10.5)]], TEAL, CARD),
        ("The three commands that matter",
         [[R("vlib work", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("   create the working library", s=10.5)],
          [R("vlog rtl/*.v tb/tb_uart.v", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("   compile into it", s=10.5)],
          [R("vsim -voptargs=+acc work.tb_uart", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("   elaborate and load", s=10.5)],
          [R("run -all", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("   simulate to $finish",
                                                                  s=10.5)],
          [R("+acc keeps signal visibility — without it the optimiser removes the very signals "
             "you want to look at.", s=10.5, i=True, c=SLATE)]], GREEN, CARD_G)], h=2377440)
    y = d.code(s, y + G, [
        "vsim -c -gLAB=L3_fsm -do scripts/modelsim_run.do     # batch, prints PASS/FAIL",
        "vsim    -do scripts/modelsim_run.do                  # GUI, with waveforms added",
    ], size=9.5, title="Topic4_Lab/scripts/modelsim_run.do — covers all five labs")

    # ============================================================ command card
    s = d.slide("TOPIC 4 · REFERENCE", "One-Page Command Card")
    d.lead(s, TOP, [[
        R("Print this and keep it beside the keyboard for the whole module.", b=True, c=NAVY,
          s=12.5)]], h=365760)
    d.table(s, 1508760,
            ["Task", "Open-source", "Vivado", "ModelSim"],
            [["Lint", "verilator --lint-only -Wall rtl/*.v", "report_methodology", "vlog (warnings)"],
             ["Compile", "iverilog -g2005 -o sim.vvp <files>", "xvlog <files>", "vlog <files>"],
             ["Elaborate", "(part of iverilog)", "xelab -debug typical <top>", "(part of vsim)"],
             ["Run", "vvp sim.vvp", "xsim <snapshot> -runall", "vsim -c work.<top>; run -all"],
             ["Waves", "gtkwave dump.vcd", "Vivado sim wave window", "add wave -r /*"],
             ["Synthesise", "yosys -p \"...; synth -top X; stat\"", "synth_design -top X -part P",
              "(not a synthesis tool)"],
             ["Area report", "stat", "report_utilization", "—"],
             ["Timing report", "(none — no timing model)", "report_timing_summary", "—"],
             ["Find latches", "grep -i latch on the log", "Messages: [Synth 8-327]", "—"]],
            [1737360, 3657600, 3200400, 2651760], rh=283464, bold_cols=(0,), size=9,
            col_colors={0: NAVY})

    # =============================================== LABS
    d.section_slide("TOPIC 4 · PRACTICAL", "The Lab Programme",
                    "Mapped to the syllabus practical component: 40 hours of RTL Design and "
                    "Implementation Labs, plus synthesis and timing.",
                    ["L1 combinational · L2 sequential · L3 state machines · L4 memory · "
                     "L5 UART capstone",
                     "Twenty-two designs, five self-checking testbenches, three toolchains",
                     "Deliberately broken examples, so failures can be seen in real tool reports",
                     "Assessment rubric and the common-error table"], accent=GREEN)

    # ============================================================ lab overview
    s = d.slide("TOPIC 4 · LABS", "The Five Labs and Their Hours")
    d.lead(s, TOP, [[
        R("These hours map onto the syllabus practical component. ", b=True, c=NAVY, s=12.5),
        R("Every design listed exists, compiles, simulates to PASS and synthesises with no "
          "inferred latches.")]], h=411480)
    y = d.table(s, 1554480,
                ["Lab", "Hours", "Designs", "Testbench", "What it teaches"],
                [["L1 Combinational", "8",
                  "mux2 mux4 decoder3to8 priority_encoder8 alu seven_seg adder_gen", "tb_comb.v",
                  "assign vs always @(*), defaults, case, generate"],
                 ["L2 Sequential", "8",
                  "reg_en shift_reg counter edge_detect synchroniser debouncer clk_divider",
                  "tb_seq.v", "the clocked templates, <=, clock enables, CDC"],
                 ["L3 State machines", "8", "traffic_fsm vending_fsm seq_detect_1011", "tb_fsm.v",
                  "three-block FSM, safe defaults, Moore vs Mealy"],
                 ["L4 Memory & FIFO", "8", "sync_fifo sync_ram", "tb_mem.v",
                  "memory inference, pointers, scoreboards, $random"],
                 ["L5 UART capstone", "8", "uart_tx uart_rx (+ synchroniser)", "tb_uart.v",
                  "a complete FSMD, loopback, independent decoder"]],
                [1920240, 640080, 3383280, 1188720, 4114800], rh=457200, bold_cols=(0,), size=9,
                col_colors={0: NAVY})
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Forty hours in total, matching the syllabus allocation for RTL Design and "
          "Implementation Labs. The synthesis and timing exercises inside each lab feed the "
          "further 15 h Design Synthesis and 10 h Timing Analysis allocations.", s=10.5, i=True,
        c=SLATE)]])
    d.cols(s, y + 411480, [
        ("What every lab produces",
         [[R("· A clean lint run.   · A simulation transcript ending in PASS.", s=10.5)],
          [R("· A synthesis report with a cell and flip-flop count, and no inferred latches.",
             s=10.5)],
          [R("· Two sentences from the student saying what the design became in hardware.",
             s=10.5)]], GREEN, CARD_G),
        ("Running short of time?",
         [[R("Do not cut L5. ", b=True, c=RED, s=10.5),
           R("The UART is where combinational logic, sequential logic, an FSM, a datapath, a "
             "clock-domain crossing and a self-checking testbench all appear in one design — it "
             "is the only exercise that shows students how the pieces fit. Cut depth in L1 "
             "instead; those designs are the easiest to catch up on alone.", s=10.5)]],
         RED, CARD_R)], h=1417320)

    # ============================================================ lab method
    s = d.slide("TOPIC 4 · LABS", "How to Run a Lab Session")
    y = d.tiers(s, TOP, [
        ("BEFORE", "Students clone Topic4_Lab and run ./scripts/lint.sh and ./scripts/run_all.sh "
                   "unmodified. Everything must print PASS before anyone edits anything — that "
                   "proves the environment works and removes 'it does not build' from the "
                   "session.", NAVY),
        ("READ", "Open one design and one testbench side by side. Ask the room to predict the "
                 "flip-flop count from the source, write the predictions on the board, then run "
                 "the synthesiser and compare. Ten minutes; it changes how they read code.", TEAL),
        ("BREAK", "Introduce a fault deliberately: remove a default, change a <= to =, drop a "
                  "case branch. Re-run lint, simulation and synthesis and see which one catches "
                  "it. This is the single most effective exercise in the whole topic.", AMBER),
        ("BUILD", "The exercise proper — extend or write a design from the workbook. Every "
                  "exercise has a specification, a required interface and an expected testbench "
                  "result, so the student always knows when they are finished.", GREEN),
        ("REPORT", "Submit: source, the simulation transcript showing PASS, the synthesis "
                   "utilisation figures, and two sentences on what the design became in hardware. "
                   "The last item is the one being assessed.", VIOLET),
    ], h=822960, gap=45720)

    # ============================================================ common errors
    s = d.slide("TOPIC 4 · TROUBLESHOOTING", "The Errors Your Students Will Actually Hit")
    d.lead(s, TOP, [[
        R("Nine out of ten support questions in this topic are one of these. ", b=True, c=NAVY,
          s=12.5),
        R("Put this table on the wall of the lab.")]], h=411480)
    d.table(s, 1554480,
            ["Symptom", "Almost always means", "Fix"],
            [["Output is x from time zero", "A register was never reset, or a wire has no driver",
              "Reset every register; check the port connections"],
             ["Output is x after working", "Two drivers, or reading past the end of a vector",
              "One signal, one driving block"],
             ["'Inferred latch for signal y'", "A branch of always @(*) leaves y unassigned",
              "Default assignment at the top of the block"],
             ["Shift register is one flip-flop", "Blocking = used in a clocked block",
              "Use <= in every always @(posedge clk)"],
             ["Result wraps at the wrong value", "Width truncation on an expression",
              "Make the target one bit wider; run Verilator"],
             ["Signal not found in GTKWave", "$dumpvars scope too narrow, or the file is stale",
              "$dumpvars(0, tb); and re-run before re-opening"],
             ["Testbench passes but hardware fails", "casex, full_case, or an initial block",
              "Remove all three; reset properly"],
             ["FSM is stuck in an unknown state", "No default branch; reset released on an edge",
              "default: next = IDLE; release reset between edges"],
             ["Works at one parameter, not another", "A constant sliced to a width that cannot "
              "hold it", "Compute as integer; slice at the point of use"]],
            [3200400, 4023360, 4023360], rh=283464, bold_cols=(0,), size=9,
            col_colors={0: NAVY})

    # ============================================================ assessment
    s = d.slide("TOPIC 4 · ASSESSMENT", "What 'Done' Looks Like")
    y = d.lead(s, TOP, [[
        R("Assess the hardware understanding, not the typing. ", b=True, c=NAVY, s=12.5),
        R("A student who can explain what their code became has learned the topic; one whose "
          "simulation happens to pass may not have.")]], h=548640)
    y = d.table(s, y + 45720,
                ["Level", "Evidence"],
                [["Pass", "Design compiles, lint is clean, the supplied testbench prints PASS, "
                          "and synthesis reports no inferred latches."],
                 ["Good", "All of the above, plus: the student predicted the flip-flop count "
                          "correctly and can point to which lines produced them."],
                 ["Strong", "All of the above, plus: a self-checking testbench of the student's "
                            "own with a reference model, and a sensible explanation of the "
                            "timing report."],
                 ["Excellent", "All of the above, plus: the student found and diagnosed a real "
                               "bug — theirs or a planted one — and can explain which stage of "
                               "the flow should have caught it and why it did not."]],
                [1737360, 9509760], rh=457200, bold_cols=(0,), size=10,
                col_colors={0: NAVY})
    d.card(s, y + G, "One question to ask every student, every session",
           [[R("\"Point at a line and tell me what it became.\" ", b=True, c=TEAL),
             R("If the answer is fluent, they have understood RTL design. If it is 'it assigns "
               "y', go back to the inference map.")]],
           accent=TEAL, h=776224)

    # ============================================================ glossary 1
    s = d.slide("TOPIC 4 · GLOSSARY", "Terms Used in This Topic — 1 of 2")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["RTL", "Register-transfer level — describing what happens to data between clock "
                     "edges, without specifying gates."],
             ["Synthesis", "Translating RTL into a gate-level netlist for a target technology."],
             ["Netlist", "A list of gates and flip-flops and the wires between them — what "
                         "synthesis outputs."],
             ["Inference", "The synthesiser recognising a code pattern and producing the "
                           "corresponding hardware."],
             ["Latch", "Level-sensitive storage. Transparent while enabled. In RTL, almost always "
                       "an accident."],
             ["Flip-flop", "Edge-triggered storage. Captures its input at one clock edge and "
                           "holds it until the next."],
             ["Blocking (=)", "Assignment that takes effect immediately, before the next "
                              "statement. Combinational blocks only."],
             ["Non-blocking (<=)", "Assignment scheduled to take effect at the end of the time "
                                   "step. Clocked blocks only."],
             ["Sensitivity list", "The events that make a procedural block run. @(*) for "
                                  "combinational, @(posedge clk) for clocked."],
             ["Net / variable", "wire is a net, driven continuously; reg is a variable, assigned "
                                "inside a procedural block."],
             ["Four-state logic", "0, 1, x (unknown) and z (high impedance)."],
             ["Elaboration", "Building the design hierarchy and resolving parameters and generate "
                             "blocks, before simulation."]],
            [2377440, 8869680], rh=329184, bold_cols=(0,), size=9.5, col_colors={0: NAVY})

    # ============================================================ glossary 2
    s = d.slide("TOPIC 4 · GLOSSARY", "Terms Used in This Topic — 2 of 2")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["FSM", "Finite state machine — a state register plus next-state and output logic."],
             ["Moore / Mealy", "Outputs from state alone / from state and inputs."],
             ["One-hot", "A state encoding using one flip-flop per state, exactly one of which is "
                         "1."],
             ["FSMD", "Finite state machine with a datapath — a controller plus registers and "
                      "arithmetic it steers."],
             ["Metastability", "A flip-flop's output settling unpredictably after a setup or hold "
                               "violation."],
             ["CDC", "Clock domain crossing — moving a signal between two unrelated clocks."],
             ["Synchroniser", "Two or more chained flip-flops that give metastability time to "
                              "decay."],
             ["Pipelining", "Inserting registers to shorten the longest combinational path, "
                            "raising throughput at the cost of latency."],
             ["Slack / WNS", "Time left over on a timing path; worst negative slack is the worst "
                             "such path in the design."],
             ["Testbench", "A port-less module that instantiates the design, drives it, and "
                           "checks the results automatically."],
             ["Scoreboard", "An independent model of expected behaviour, written from the "
                            "specification, that the testbench compares against."],
             ["VCD", "Value Change Dump — the waveform file format $dumpvars writes and GTKWave "
                     "reads."]],
            [2377440, 8869680], rh=329184, bold_cols=(0,), size=9.5, col_colors={0: NAVY})

    # ============================================================ recap
    s = d.slide("TOPIC 4 · RECAP", "The Ten Things That Matter")
    y = d.bullets(s, TOP, [
        [R("Verilog describes hardware. Sketch the circuit first, then write the code that "
           "describes it.", s=11)],
        [R("reg is not a register. What you assign it with, and in what block, decides the "
           "hardware.", s=11)],
        [R("Three constructs: ", s=11), R("assign", f=MONO_FONT, b=True, c=NAVY, s=11),
         R(", ", s=11), R("always @(*)", f=MONO_FONT, b=True, c=NAVY, s=11), R(", ", s=11),
         R("always @(posedge clk)", f=MONO_FONT, b=True, c=NAVY, s=11),
         R(". Know what each becomes.", s=11)],
        [R("= in combinational blocks, <= in clocked blocks. Never mix them for one variable.",
           s=11)],
        [R("Assign every output on every path, or you get a latch. Default first, then override.",
           s=11)],
        [R("Size every literal. Width truncation is silent, and it is the bug that comes back.",
           s=11)],
        [R("Three-block FSMs, with a safe default that recovers from any illegal state.", s=11)],
        [R("Anything crossing a clock domain goes through two flip-flops — and buses need Gray "
           "coding or a handshake.", s=11)],
        [R("A testbench prints PASS or FAIL. If a human has to read a waveform to decide, it is "
           "not a testbench.", s=11)],
        [R("Lint, then simulate, then synthesise — and read the synthesis log every single time.",
           s=11)],
    ], accent=TEAL, step=329184)
    d.card(s, y + G, "Where this leads",
           [[R("Topic 5 takes this RTL into synthesis proper — constraints, optimisation, and "
               "reading a timing report until it means something. Everything you build from here "
               "on is written in the language you have just learned; the difference is that the "
               "clock, the area and the power start to have opinions about it.")]],
           accent=TEAL, h=822960)

    # ============================================================ close
    d.section_slide("TOPIC 4 · COMPLETE", "RTL Design Using HDL",
                    "Deck · workbook · 22 verified designs · 5 self-checking testbenches · "
                    "3 toolchains.",
                    ["Slides: this deck, for delivery",
                     "Workbook: Module2_Topic4_Tutorial_Practice_Workbook.docx — tutorials, "
                     "exercises and full solutions",
                     "Lab: Topic4_Lab/ — rtl/, tb/, scripts/, all verified end to end",
                     "Next: Module 2 Topic 5 — synthesis, constraints and timing closure"],
                    accent=NAVY)
