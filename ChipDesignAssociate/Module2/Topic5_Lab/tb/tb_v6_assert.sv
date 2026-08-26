// ---------------------------------------------------------------------------
// tb_v6_assert.sv  -  Lab V6.  A LAYERED testbench, with assertions.
//
// V3 proved the FIFO's outputs against a model. V6 adds the two things a real
// verification environment has that a flat testbench does not:
//
//   1. LAYERS. The parts that generate stimulus, drive pins, observe pins and
//      decide correctness are separate. Each can be changed without touching
//      the others - which is what makes a testbench survive contact with a
//      second project.
//
//        generator -> driver -> [ DUT ] -> monitor -> scoreboard
//                                  |
//                              assertions
//
//   2. ASSERTIONS. sva/fifo_sva.sv states the specification as properties that
//      are checked on EVERY clock edge and report at the exact cycle the rule
//      broke, not later at the output where the damage became visible.
//
// This file is SystemVerilog and is run by a simulator that supports
// concurrent assertions:
//
//   ./scripts/assert.sh                 (open-source: verilator --binary)
//   ./scripts/modelsim_run.do  LAB=V6   (vendor)
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`ifndef DUT
  `define DUT fifo
`endif
`ifndef DUTNAME
  `define DUTNAME "fifo"
`endif

module tb_v6_assert;

    localparam int W     = 8;
    localparam int DEPTH = 8;
    localparam int CLK   = 10;
    localparam int AW    = $clog2(DEPTH);

    logic              clk = 1'b0;
    logic              rst_n;
    logic              wr_en, rd_en;
    logic [W-1:0]      wr_data;
    logic [W-1:0]      rd_data;
    logic              full, empty;
    logic [AW:0]       count;

    always #(CLK/2) clk = ~clk;

    // ------------------------------------------------------------------ DUT
    `DUT #(.W(W), .DEPTH(DEPTH)) u_dut (
        .clk(clk), .rst_n(rst_n), .wr_en(wr_en), .wr_data(wr_data),
        .rd_en(rd_en), .rd_data(rd_data),
        .full(full), .empty(empty), .count(count));

    // ------------------------------------------------------- the assertions
    // Bound to the same signals, checking the specification continuously.
    fifo_sva #(.DEPTH(DEPTH)) u_sva (
        .clk(clk), .rst_n(rst_n), .wr_en(wr_en), .rd_en(rd_en),
        .full(full), .empty(empty), .count(count));

    // ------------------------------------------------- LAYER 4: scoreboard
    // The only place in the testbench that knows what "correct" means.
    logic [W-1:0] model [DEPTH];
    int           mhead = 0, mtail = 0;
    int           errors = 0, checks = 0;
    int           pushed = 0, popped = 0;

    function automatic logic [AW:0] m_count(); return (AW+1)'(mtail - mhead); endfunction
    function automatic bit  m_empty(); return mtail == mhead;     endfunction
    function automatic bit  m_full();  return (mtail-mhead)==DEPTH; endfunction

    task automatic sb_check(string where);
        checks++;
        if (count !== m_count()) begin
            errors++; $display("  SCOREBOARD %0t %s: count=%0d model=%0d",
                               $time, where, count, m_count());
        end
        if (empty !== m_empty()) begin
            errors++; $display("  SCOREBOARD %0t %s: empty=%0b model=%0b",
                               $time, where, empty, m_empty());
        end
        if (full !== m_full()) begin
            errors++; $display("  SCOREBOARD %0t %s: full=%0b model=%0b",
                               $time, where, full, m_full());
        end
        if (!m_empty() && rd_data !== model[mhead % DEPTH]) begin
            errors++; $display("  SCOREBOARD %0t %s: rd_data=%h model=%h",
                               $time, where, rd_data, model[mhead % DEPTH]);
        end
    endtask

    // ---------------------------------------------------- LAYER 3: monitor
    // Watches the pins and tells the scoreboard what the DUT actually did.
    // It never drives anything and never looks inside the DUT.
    task automatic mon_apply(bit did_wr, bit did_rd, logic [W-1:0] d);
        bit was_full  = m_full();
        bit was_empty = m_empty();
        if (did_wr && !was_full)  begin model[mtail % DEPTH] = d; mtail++; pushed++; end
        if (did_rd && !was_empty) begin mhead++;                          popped++; end
    endtask

    // ----------------------------------------------------- LAYER 2: driver
    // Knows the pin-level protocol and nothing else.
    task automatic drv_cycle(bit do_w, bit do_r, logic [W-1:0] d, string where);
        @(posedge clk); #1;
        wr_en = do_w; rd_en = do_r; wr_data = d;
        @(posedge clk); #1;
        wr_en = 1'b0; rd_en = 1'b0;
        mon_apply(do_w, do_r, d);
        sb_check(where);
    endtask

    // -------------------------------------------------- LAYER 1: generator
    // Decides WHAT to test. Weighted random, plus the corners named explicitly.
    int seed = 1, seed0, cycles = 2000, p_wr = 55, p_rd = 45;

    initial begin
        if (!$value$plusargs("SEED=%d",   seed))   seed   = 1;
        if (!$value$plusargs("CYCLES=%d", cycles)) cycles = 2000;
        if (!$value$plusargs("WR=%d",     p_wr))   p_wr   = 55;
        if (!$value$plusargs("RD=%d",     p_rd))   p_rd   = 45;
        seed0 = seed;
        // SEED THE GENERATOR ONCE. $urandom(seed) RE-SEEDS on every call, so
        // calling it with an argument inside the loop returns the same number
        // for ever - a mistake that silently turns a random test into a single
        // repeated transaction. Seed once, then call $urandom() with no
        // argument.
        void'($urandom(seed0));

        rst_n = 1'b0; wr_en = 1'b0; rd_en = 1'b0; wr_data = '0;
        repeat (3) @(posedge clk);
        #1 rst_n = 1'b1;
        @(posedge clk); #1;

        // directed corners first - cheap, deterministic, and they fail fast
        for (int i = 0; i < DEPTH + 2; i++) drv_cycle(1'b1, 1'b0, 8'h10+i[7:0], "fill");
        for (int i = 0; i < DEPTH + 2; i++) drv_cycle(1'b0, 1'b1, '0,           "drain");
        drv_cycle(1'b1, 1'b1, 8'hAA, "read+write while empty");
        drv_cycle(1'b0, 1'b1, '0,    "drain the one word");

        // then the random body
        for (int i = 0; i < cycles; i++) begin
            bit b_w = (($urandom() % 100) < p_wr);
            bit b_r = (($urandom() % 100) < p_rd);
            drv_cycle(b_w, b_r, W'($urandom()), "random");
        end

        // finally, drain everything the model still holds and prove it comes
        // back in order
        while (!m_empty()) drv_cycle(1'b0, 1'b1, '0, "final drain");

        repeat (2) @(posedge clk);
        $display("  scoreboard: %0d checks, %0d words in, %0d words out",
                 checks, pushed, popped);
        if (errors == 0)
            $display("PASS - V6 layered+assertions on %0s : seed=%0d cycles=%0d",
                     `DUTNAME, seed0, cycles);
        else
            $display("FAIL - V6 layered+assertions on %0s : seed=%0d %0d scoreboard errors",
                     `DUTNAME, seed0, errors);
        $finish;
    end

    initial begin
        #(CLK * 200000);
        $display("FAIL - V6 timeout seed=%0d", seed0);
        $finish;
    end

endmodule
