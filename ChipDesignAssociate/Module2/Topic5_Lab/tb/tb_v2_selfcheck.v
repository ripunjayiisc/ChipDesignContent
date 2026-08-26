// ---------------------------------------------------------------------------
// tb_v2_selfcheck.v  -  Lab V2.  Directed tests against a REFERENCE MODEL.
//
// The step up from V1 is not "more test cases". It is that the expected value
// is now computed by an independent model of the specification instead of
// being typed in by hand. Once you have a model you can check EVERY cycle,
// not just the ones you remembered to write an expectation for.
//
// The model here is a plain Verilog array with a head and a tail index. It is
// written from the interface contract at the top of rtl/fifo.v and it never
// looks at anything inside the DUT.
//
// This stage also adds the boundary cases V1 never reached: filling to full,
// draining to empty, writing while full and reading while empty.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`ifndef DUT
  `define DUT fifo
`endif
`ifndef DUTNAME
  `define DUTNAME "fifo"
`endif

module tb_v2_selfcheck;

    localparam integer W     = 8;
    localparam integer DEPTH = 8;
    localparam integer CLK   = 10;

    reg  clk = 1'b0, rst_n, wr_en, rd_en;
    reg  [W-1:0] wr_data;
    wire [W-1:0] rd_data;
    wire full, empty;
    wire [$clog2(DEPTH):0] count;

    `DUT #(.W(W), .DEPTH(DEPTH)) u_dut (
        .clk(clk), .rst_n(rst_n), .wr_en(wr_en), .wr_data(wr_data),
        .rd_en(rd_en), .rd_data(rd_data),
        .full(full), .empty(empty), .count(count));

    always #(CLK/2) clk = ~clk;

    // ---------------------------------------------------------- the verdict
    integer errors = 0;
    reg [255:0] first_msg, first_where;

    // Two separate strings, never concatenated: a Verilog string is a fixed
    // width vector, so joining two 256 bit strings and passing the result to a
    // 256 bit argument silently throws half of it away.
    task expect_true(input cond, input [255:0] msg, input [255:0] where);
        begin
            if (cond !== 1'b1) begin
                if (errors == 0) begin first_msg = msg; first_where = where; end
                if (errors < 8)
                    $display("  FAIL %0t : %0s   (during: %0s)", $time, msg, where);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------- the reference model (SPEC)
    // An independent queue. Nothing here reads any DUT signal.
    reg [W-1:0] model [0:DEPTH-1];
    integer     mhead, mtail;                       // mtail - mhead = occupancy

    function [$clog2(DEPTH):0] mcount; input dummy; begin mcount = mtail - mhead; end
    endfunction
    function mempty; input dummy; begin mempty = (mtail == mhead); end endfunction
    function mfull;  input dummy; begin mfull  = ((mtail - mhead) == DEPTH); end endfunction

    task model_reset; begin mhead = 0; mtail = 0; end endtask

    // Apply one bus cycle to the model. The hardware decides BOTH do_wr and
    // do_rd from the state as it was BEFORE the clock edge, so the model must
    // sample full and empty once, up front, and use those samples for both
    // decisions. Applying the push first and then testing empty for the pop
    // is a real and easy mistake: on a simultaneous read and write to an EMPTY
    // FIFO the model would push, observe itself no longer empty, and pop again
    // - reporting an occupancy of 0 where the hardware has 1.
    task model_cycle(input do_w, input do_r, input [W-1:0] d);
        reg was_full, was_empty;
        begin
            was_full  = mfull(0);
            was_empty = mempty(0);
            if (do_w && !was_full)  begin model[mtail % DEPTH] = d; mtail = mtail + 1; end
            if (do_r && !was_empty) mhead = mhead + 1;
        end
    endtask
    function [W-1:0] model_front; input dummy; begin model_front = model[mhead % DEPTH]; end
    endfunction

    // --------------------------------------------- compare DUT against model
    // Called after every clock edge the test drives.
    task compare(input [255:0] where);
        begin
            expect_true(count   === mcount(0),      "count disagrees with the model", where);
            expect_true(empty   === mempty(0),      "empty disagrees with the model", where);
            expect_true(full    === mfull(0),       "full disagrees with the model",  where);
            if (!mempty(0))
                expect_true(rd_data === model_front(0),
                            "rd_data is not the oldest word", where);
        end
    endtask

    // ------------------------------------------------------ stimulus drivers
    // One bus cycle. Drives wr_en/rd_en for exactly one clock, updates the
    // model with the SAME operation, then compares.
    task cycle(input do_w, input do_r, input [W-1:0] d, input [255:0] where);
        begin
            @(posedge clk); #1;
            wr_en = do_w; rd_en = do_r; wr_data = d;
            @(posedge clk); #1;
            wr_en = 1'b0; rd_en = 1'b0;
            model_cycle(do_w, do_r, d);
            compare(where);
        end
    endtask

    integer i;
    reg [W-1:0] d;

    initial begin
        $dumpfile("v2.vcd");
        $dumpvars(0, tb_v2_selfcheck);

        rst_n = 1'b0; wr_en = 1'b0; rd_en = 1'b0; wr_data = {W{1'b0}};
        model_reset;
        repeat (3) @(posedge clk);
        #1 rst_n = 1'b1;
        @(posedge clk); #1;

        // ---- T1 : state immediately after reset ---------------------------
        compare("after reset");

        // ---- T2 : fill to exactly full ------------------------------------
        for (i = 0; i < DEPTH; i = i + 1)
            cycle(1'b1, 1'b0, 8'h10 + i[7:0], "filling");
        expect_true(full === 1'b1,  "FIFO did not go full after DEPTH writes", "T2");
        expect_true(empty === 1'b0, "FIFO says empty while full", "T2");

        // ---- T3 : write while full must be ignored ------------------------
        cycle(1'b1, 1'b0, 8'hEE, "write while full");
        expect_true(count === DEPTH[$clog2(DEPTH):0],
                    "a write while full changed the occupancy", "T3");

        // ---- T4 : drain to exactly empty ----------------------------------
        for (i = 0; i < DEPTH; i = i + 1)
            cycle(1'b0, 1'b1, 8'h00, "draining");
        expect_true(empty === 1'b1, "FIFO did not go empty after DEPTH reads", "T4");
        expect_true(full  === 1'b0, "FIFO says full while empty", "T4");

        // ---- T5 : read while empty must be ignored ------------------------
        cycle(1'b0, 1'b1, 8'h00, "read while empty");
        expect_true(count === 0, "a read while empty changed the occupancy", "T5");

        // ---- T6 : simultaneous read and write, held half full --------------
        for (i = 0; i < DEPTH/2; i = i + 1)
            cycle(1'b1, 1'b0, 8'h40 + i[7:0], "half fill");
        for (i = 0; i < 12; i = i + 1)
            cycle(1'b1, 1'b1, 8'h80 + i[7:0], "read+write same cycle");

        // ---- T7 : keep going long enough to WRAP the pointers -------------
        for (i = 0; i < DEPTH * 3; i = i + 1)
            cycle(1'b1, 1'b1, 8'hC0 + i[7:0], "wrapping");

        // ---- T8 : drain what is left --------------------------------------
        while (!mempty(0))
            cycle(1'b0, 1'b1, 8'h00, "final drain");
        expect_true(empty === 1'b1, "FIFO not empty at the end of the test", "T8");

        repeat (2) @(posedge clk);
        if (errors == 0)
            $display("PASS - V2 self-checking on %0s : model agrees every cycle",
                     `DUTNAME);
        else
            $display("FAIL - V2 self-checking on %0s : %0d errors, first was \"%0s\" during %0s",
                     `DUTNAME, errors, first_msg, first_where);
        $finish;
    end

    initial begin
        #(CLK * 5000);
        $display("FAIL - V2 timeout on %0s", `DUTNAME);
        $finish;
    end

endmodule
