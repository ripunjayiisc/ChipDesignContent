// ---------------------------------------------------------------------------
// tb_v3_random.v  -  Lab V3.  CONSTRAINED-RANDOM stimulus with a seed.
//
// V2 checks the corners you thought of. V3 exists for the corners you did not.
// It drives wr_en and rd_en from a weighted random source, compares against the
// same reference model every cycle, and prints the SEED with every result so a
// failure can be reproduced exactly.
//
//   vvp v3.vvp +SEED=12345 +CYCLES=4000 +WR=60 +RD=45
//
//   +SEED    seed for $random. Same seed -> identical run, always.
//   +CYCLES  how many bus cycles to drive (default 3000)
//   +WR      percentage chance of asserting wr_en on a cycle (default 55)
//   +RD      percentage chance of asserting rd_en on a cycle (default 45)
//
// The weights are the "constraints". Setting WR well above RD keeps the FIFO
// near full; setting RD above WR keeps it near empty; equal weights spend most
// of the run in the middle, which is exactly where the interesting corner
// cases are NOT. Run all three profiles - scripts/regress.sh does.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`ifndef DUT
  `define DUT fifo
`endif
`ifndef DUTNAME
  `define DUTNAME "fifo"
`endif

module tb_v3_random;

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

    // ------------------------------------------------------- run parameters
    integer seed   = 1;
    integer seed0  = 1;                   // the seed AS GIVEN - $random mutates seed
    integer cycles = 3000;
    integer p_wr   = 55;
    integer p_rd   = 45;

    // -------------------------------------------------------- the reference
    reg [W-1:0] model [0:DEPTH-1];
    integer     mhead, mtail;
    function [$clog2(DEPTH):0] mcount; input dummy; begin mcount = mtail - mhead; end
    endfunction
    function mempty; input dummy; begin mempty = (mtail == mhead); end endfunction
    function mfull;  input dummy; begin mfull  = ((mtail - mhead) == DEPTH); end endfunction
    function [W-1:0] model_front; input dummy; begin model_front = model[mhead % DEPTH]; end
    endfunction

    // ------------------------------------------------------------- checking
    integer errors = 0;
    integer first_cycle = -1;
    reg [255:0] first_msg;

    task expect_true(input cond, input [255:0] msg, input integer cyc);
        begin
            if (cond !== 1'b1) begin
                if (errors == 0) begin first_msg = msg; first_cycle = cyc; end
                if (errors < 5)
                    $display("  FAIL %0t cycle %0d : %0s", $time, cyc, msg);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------------------------ coverage
    // Plain-Verilog functional coverage: a counter per interesting situation.
    // This is what a SystemVerilog covergroup does, written by hand.
    integer cov_wr_only, cov_rd_only, cov_both, cov_idle;
    integer cov_wr_full, cov_rd_empty, cov_both_empty, cov_both_full;
    integer cov_hit_full, cov_hit_empty, cov_wrapped;

    integer i, k;
    reg do_w, do_r, was_full, was_empty;
    reg [W-1:0] d;
    reg [$clog2(DEPTH):0] prev_count;

    initial begin
        $dumpfile("v3.vcd");
        $dumpvars(0, tb_v3_random);

        if (!$value$plusargs("SEED=%d",   seed))   seed   = 1;
        seed0 = seed;                     // remember it: $random updates seed in place
        if (!$value$plusargs("CYCLES=%d", cycles)) cycles = 3000;
        if (!$value$plusargs("WR=%d",     p_wr))   p_wr   = 55;
        if (!$value$plusargs("RD=%d",     p_rd))   p_rd   = 45;

        cov_wr_only=0; cov_rd_only=0; cov_both=0; cov_idle=0;
        cov_wr_full=0; cov_rd_empty=0; cov_both_empty=0; cov_both_full=0;
        cov_hit_full=0; cov_hit_empty=0; cov_wrapped=0;

        rst_n = 1'b0; wr_en = 1'b0; rd_en = 1'b0; wr_data = {W{1'b0}};
        mhead = 0; mtail = 0;
        repeat (3) @(posedge clk);
        #1 rst_n = 1'b1;
        @(posedge clk); #1;

        for (i = 0; i < cycles; i = i + 1) begin
            // ---- constrained-random decision for this cycle ---------------
            do_w = (({$random(seed)} % 100) < p_wr);
            do_r = (({$random(seed)} % 100) < p_rd);
            d    = $random(seed);

            // ---- record what situation we are about to exercise -----------
            if      ( do_w && !do_r) cov_wr_only = cov_wr_only + 1;
            else if (!do_w &&  do_r) cov_rd_only = cov_rd_only + 1;
            else if ( do_w &&  do_r) cov_both    = cov_both    + 1;
            else                     cov_idle    = cov_idle    + 1;
            if (do_w && full)             cov_wr_full    = cov_wr_full    + 1;
            if (do_r && empty)           cov_rd_empty   = cov_rd_empty   + 1;
            if (do_w && do_r && empty)   cov_both_empty = cov_both_empty + 1;
            if (do_w && do_r && full)    cov_both_full  = cov_both_full  + 1;
            if (full)                    cov_hit_full   = cov_hit_full   + 1;
            if (empty)                   cov_hit_empty  = cov_hit_empty  + 1;

            // ---- drive one bus cycle --------------------------------------
            prev_count = count;
            @(posedge clk); #1;
            wr_en = do_w; rd_en = do_r; wr_data = d;
            @(posedge clk); #1;
            wr_en = 1'b0; rd_en = 1'b0;

            // ---- advance the model with the SAME operation ----------------
            // Sample full/empty ONCE, before either is applied - the hardware
            // decides both from the state that existed before the edge.
            was_full  = mfull(0);
            was_empty = mempty(0);
            if (do_w && !was_full)  begin model[mtail % DEPTH] = d; mtail = mtail + 1; end
            if (do_r && !was_empty) mhead = mhead + 1;
            if (mtail >= DEPTH && (mtail % DEPTH) == 0) cov_wrapped = cov_wrapped + 1;

            // ---- compare, every single cycle ------------------------------
            expect_true(count === mcount(0), "count disagrees with the model",   i);
            expect_true(empty === mempty(0), "empty disagrees with the model",   i);
            expect_true(full  === mfull(0),  "full disagrees with the model",    i);
            if (!mempty(0))
                expect_true(rd_data === model_front(0),
                            "rd_data is not the oldest word", i);
        end

        // ---- drain and confirm every word that went in comes out ----------
        k = 0;
        while (!mempty(0) && k < DEPTH + 2) begin
            expect_true(rd_data === model_front(0), "drain: wrong word", cycles + k);
            @(posedge clk); #1; rd_en = 1'b1;
            @(posedge clk); #1; rd_en = 1'b0;
            mhead = mhead + 1;
            k = k + 1;
        end
        expect_true(empty === 1'b1, "FIFO not empty after draining the model", cycles);

        $display("  coverage: wr_only=%0d rd_only=%0d both=%0d idle=%0d",
                 cov_wr_only, cov_rd_only, cov_both, cov_idle);
        $display("  coverage: cycles_full=%0d cycles_empty=%0d wraps=%0d",
                 cov_hit_full, cov_hit_empty, cov_wrapped);
        $display("  coverage: wr_while_full=%0d rd_while_empty=%0d both_while_empty=%0d both_while_full=%0d",
                 cov_wr_full, cov_rd_empty, cov_both_empty, cov_both_full);

        if (errors == 0)
            $display("PASS - V3 random on %0s : seed=%0d cycles=%0d wr=%0d rd=%0d",
                     `DUTNAME, seed0, cycles, p_wr, p_rd);
        else
            $display("FAIL - V3 random on %0s : seed=%0d %0d errors, first at cycle %0d \"%0s\"",
                     `DUTNAME, seed0, errors, first_cycle, first_msg);
        $finish;
    end

    initial begin
        #(CLK * 200000);
        $display("FAIL - V3 timeout on %0s seed=%0d", `DUTNAME, seed0);
        $finish;
    end

endmodule
