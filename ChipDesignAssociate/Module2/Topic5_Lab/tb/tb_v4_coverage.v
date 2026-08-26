// ---------------------------------------------------------------------------
// tb_v4_coverage.v  -  Lab V4.  FUNCTIONAL COVERAGE, and closing it.
//
// V3 asked "did anything break?". V4 asks the question that actually tells you
// whether you are finished: "WHAT DID I ACTUALLY TEST?"
//
// A run that passes proves nothing on its own. If the FIFO never went full,
// then "no bug found near full" is not a result - it is an absence of
// evidence. Functional coverage turns that absence into a number.
//
// SystemVerilog has covergroups for this. Plain Verilog does not, so this
// testbench does it the long way: one counter per interesting situation,
// declared up front as a COVERAGE MODEL, sampled every cycle, and reported at
// the end with a HIT/MISS verdict per bin. That is exactly what a covergroup
// does, and writing it by hand once is the best way to understand what the
// tool is doing for you later.
//
//   vvp v4.vvp +SEED=1 +CYCLES=3000 +WR=55 +RD=45 +TAG=balanced
//
// It also writes build/cov_<TAG>.txt so scripts/coverage.sh can MERGE the bins
// across several runs - which is how coverage is really closed: no single run
// hits everything, and no single run has to.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`ifndef DUT
  `define DUT fifo
`endif

module tb_v4_coverage;

    localparam integer W     = 8;
    localparam integer DEPTH = 8;
    localparam integer CLK   = 10;
    localparam integer NBINS = 12;

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

    // ----------------------------------------------------- THE COVERAGE MODEL
    // Write this list BEFORE you write the stimulus. It is the answer to
    // "what would convince me this FIFO works?", and it is reviewed by a
    // second person exactly like the design is.
    //
    //   0  write accepted                    6  occupancy reached DEPTH (full)
    //   1  read accepted                     7  occupancy reached 0 (empty)
    //   2  simultaneous read and write       8  pointers wrapped at least once
    //   3  idle cycle                        9  write attempted while full
    //   4  simultaneous r+w while EMPTY     10  read attempted while empty
    //   5  simultaneous r+w while FULL      11  a full -> empty -> full round trip
    integer cov [0:NBINS-1];
    reg [8*28-1:0] binname [0:NBINS-1];

    task cov_init;
        integer j;
        begin
            for (j = 0; j < NBINS; j = j + 1) cov[j] = 0;
            binname[0]  = "write accepted";
            binname[1]  = "read accepted";
            binname[2]  = "read+write same cycle";
            binname[3]  = "idle cycle";
            binname[4]  = "read+write while empty";
            binname[5]  = "read+write while full";
            binname[6]  = "reached FULL";
            binname[7]  = "reached EMPTY";
            binname[8]  = "pointers wrapped";
            binname[9]  = "write attempted while full";
            binname[10] = "read attempted while empty";
            binname[11] = "full->empty->full round trip";
        end
    endtask

    // ------------------------------------------------------------ the model
    reg [W-1:0] model [0:DEPTH-1];
    integer     mhead, mtail;
    function [$clog2(DEPTH):0] mcount; input dummy; begin mcount = mtail - mhead; end
    endfunction
    function mempty; input dummy; begin mempty = (mtail == mhead); end endfunction
    function mfull;  input dummy; begin mfull  = ((mtail - mhead) == DEPTH); end endfunction
    function [W-1:0] mfront; input dummy; begin mfront = model[mhead % DEPTH]; end endfunction

    integer errors = 0;
    task expect_true(input cond, input [255:0] msg);
        begin
            if (cond !== 1'b1) begin
                if (errors < 5) $display("  FAIL %0t : %0s", $time, msg);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------------------------ run state
    integer seed = 1, seed0 = 1, cycles = 3000, p_wr = 55, p_rd = 45;
    reg [8*16-1:0] tag = "run";
    integer i, j, fd, hit, was_full, was_empty, seen_full, seen_empty_after_full;
    reg do_w, do_r;
    reg [W-1:0] d;

    initial begin
        $dumpfile("v4.vcd");
        $dumpvars(0, tb_v4_coverage);

        if (!$value$plusargs("SEED=%d",   seed))   seed   = 1;
        if (!$value$plusargs("CYCLES=%d", cycles)) cycles = 3000;
        if (!$value$plusargs("WR=%d",     p_wr))   p_wr   = 55;
        if (!$value$plusargs("RD=%d",     p_rd))   p_rd   = 45;
        if (!$value$plusargs("TAG=%s",    tag))    tag    = "run";
        seed0 = seed;

        cov_init;
        seen_full = 0; seen_empty_after_full = 0;
        rst_n = 1'b0; wr_en = 1'b0; rd_en = 1'b0; wr_data = {W{1'b0}};
        mhead = 0; mtail = 0;
        repeat (3) @(posedge clk);
        #1 rst_n = 1'b1;
        @(posedge clk); #1;

        for (i = 0; i < cycles; i = i + 1) begin
            do_w = (({$random(seed)} % 100) < p_wr);
            do_r = (({$random(seed)} % 100) < p_rd);
            d    = $random(seed);

            was_full  = mfull(0);
            was_empty = mempty(0);

            // ---------------------------------------------- SAMPLE the bins
            if (do_w && !was_full)             cov[0]  = cov[0]  + 1;
            if (do_r && !was_empty)            cov[1]  = cov[1]  + 1;
            if (do_w && do_r)                  cov[2]  = cov[2]  + 1;
            if (!do_w && !do_r)                cov[3]  = cov[3]  + 1;
            if (do_w && do_r && was_empty)     cov[4]  = cov[4]  + 1;
            if (do_w && do_r && was_full)      cov[5]  = cov[5]  + 1;
            if (was_full)                      cov[6]  = cov[6]  + 1;
            if (was_empty)                     cov[7]  = cov[7]  + 1;
            if (do_w && was_full)              cov[9]  = cov[9]  + 1;
            if (do_r && was_empty)             cov[10] = cov[10] + 1;

            // full -> empty -> full is a SEQUENCE, so it needs a little state
            if (was_full)                       seen_full = 1;
            if (seen_full && was_empty)         seen_empty_after_full = 1;
            if (seen_empty_after_full && was_full) begin
                cov[11] = cov[11] + 1;
                seen_full = 1; seen_empty_after_full = 0;
            end

            // ------------------------------------------------- drive a cycle
            @(posedge clk); #1;
            wr_en = do_w; rd_en = do_r; wr_data = d;
            @(posedge clk); #1;
            wr_en = 1'b0; rd_en = 1'b0;

            if (do_w && !was_full)  begin model[mtail % DEPTH] = d; mtail = mtail + 1; end
            if (do_r && !was_empty) mhead = mhead + 1;
            if (mtail >= DEPTH && (mtail % DEPTH) == 0) cov[8] = cov[8] + 1;

            // ------------------------------------------------- and check it
            expect_true(count === mcount(0), "count disagrees with the model");
            expect_true(empty === mempty(0), "empty disagrees with the model");
            expect_true(full  === mfull(0),  "full disagrees with the model");
            if (!mempty(0)) expect_true(rd_data === mfront(0), "rd_data wrong");
        end

        // ------------------------------------------------------- the report
        hit = 0;
        $display("");
        $display("  functional coverage  [%0s]  seed=%0d cycles=%0d wr=%0d rd=%0d",
                 tag, seed0, cycles, p_wr, p_rd);
        $display("  ---------------------------------------------------------------");
        for (j = 0; j < NBINS; j = j + 1) begin
            $display("   %-30s  %8d   %0s", binname[j], cov[j],
                     (cov[j] > 0) ? "HIT" : "MISS  <-- not covered");
            if (cov[j] > 0) hit = hit + 1;
        end
        $display("  ---------------------------------------------------------------");
        $display("  bins covered: %0d of %0d  (%0d%%)", hit, NBINS, (hit*100)/NBINS);

        // machine-readable, so several runs can be merged
        fd = $fopen({"build/cov_", tag, ".txt"}, "w");
        if (fd) begin
            for (j = 0; j < NBINS; j = j + 1)
                $fdisplay(fd, "%0d %0d %0s", j, cov[j], binname[j]);
            $fclose(fd);
        end

        if (errors != 0)
            $display("FAIL - V4 coverage run: %0d functional errors", errors);
        else if (hit == NBINS)
            $display("PASS - V4 coverage run: no errors, ALL %0d bins covered", NBINS);
        else
            $display("PASS-WITH-HOLES - V4 coverage run: no errors, but %0d of %0d bins never happened",
                     NBINS - hit, NBINS);
        $finish;
    end

    initial begin
        #(CLK * 200000);
        $display("FAIL - V4 timeout");
        $finish;
    end

endmodule
