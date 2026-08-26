// ---------------------------------------------------------------------------
// tb_mem.v  -  self-checking testbench for sync_fifo and sync_ram  (Lab L4)
//
// Techniques on show:
//   * a SCOREBOARD - an independent queue in the testbench that models what
//     the FIFO should contain, compared against what it actually returns
//   * RANDOMISED stimulus with $random, seeded so the run is repeatable
//   * boundary testing: fill to full, drain to empty, and try to over-run both
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_mem;

    localparam integer W     = 8;
    localparam integer DEPTH = 8;

    reg clk = 1'b0, rst_n = 1'b0;
    integer errors = 0;
    integer i;
    integer seed = 32'd12345;

    always #5 clk = ~clk;

    task check1(input cond, input [255:0] msg);
        begin
            if (!cond) begin
                $display("  FAIL: %0s   (t=%0t)", msg, $time);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------------ FIFO
    reg           wr_en, rd_en;
    reg  [W-1:0]  wr_data;
    wire [W-1:0]  rd_data;
    wire          full, empty;
    wire [$clog2(DEPTH):0] count;

    sync_fifo #(.W(W), .DEPTH(DEPTH)) u_fifo (
        .clk(clk), .rst_n(rst_n), .wr_en(wr_en), .wr_data(wr_data),
        .rd_en(rd_en), .rd_data(rd_data), .full(full), .empty(empty),
        .count(count));

    // ---- the scoreboard: an independent model of what should be inside ----
    reg [W-1:0] model [0:1023];
    integer     mhead = 0, mtail = 0;
    function integer mcount; begin mcount = mtail - mhead; end endfunction

    // ------------------------------------------------ RAM
    reg          ram_we;
    reg  [7:0]   ram_addr;
    reg  [W-1:0] ram_din;
    wire [W-1:0] ram_q;
    sync_ram #(.W(W), .DEPTH(256)) u_ram (
        .clk(clk), .we(ram_we), .addr(ram_addr), .din(ram_din), .q(ram_q));

    task fifo_push(input [W-1:0] d);
        begin
            @(posedge clk); #1 wr_data = d; wr_en = 1'b1;
            @(posedge clk); #1 wr_en = 1'b0;
            model[mtail] = d; mtail = mtail + 1;
        end
    endtask

    task fifo_pop;
        begin
            @(negedge clk);                       // rd_data is valid now
            check1(rd_data === model[mhead], "fifo returned the wrong word");
            @(posedge clk); #1 rd_en = 1'b1;
            @(posedge clk); #1 rd_en = 1'b0;
            mhead = mhead + 1;
        end
    endtask

    initial begin
        $dumpfile("mem.vcd");
        $dumpvars(0, tb_mem);
        $display("=== L4 FIFO and RAM ===");

        wr_en = 0; rd_en = 0; wr_data = 0;
        ram_we = 0; ram_addr = 0; ram_din = 0;

        #12 rst_n = 1'b1;
        #1;
        check1(empty === 1'b1, "fifo not empty after reset");
        check1(full  === 1'b0, "fifo full after reset");
        check1(count === 0,    "fifo count not 0 after reset");

        // ---------------- fill it right to the top ----------------
        for (i = 0; i < DEPTH; i = i + 1) begin
            check1(full === 1'b0, "fifo went full too early");
            fifo_push(i[W-1:0] + 8'h10);
        end
        #1;
        check1(full  === 1'b1, "fifo did not go full at DEPTH entries");
        check1(empty === 1'b0, "fifo says empty while full");
        check1(count === DEPTH, "fifo count wrong when full");

        // a write while full must be IGNORED, not corrupt anything
        @(posedge clk); #1 wr_data = 8'hFF; wr_en = 1'b1;
        @(posedge clk); #1 wr_en = 1'b0;
        #1 check1(count === DEPTH, "fifo accepted a write while full");

        // ---------------- drain it completely ----------------
        for (i = 0; i < DEPTH; i = i + 1) begin
            check1(empty === 1'b0, "fifo went empty too early");
            fifo_pop;
        end
        #1;
        check1(empty === 1'b1, "fifo did not go empty after draining");
        check1(count === 0,    "fifo count wrong when empty");

        // a read while empty must be ignored
        @(posedge clk); #1 rd_en = 1'b1;
        @(posedge clk); #1 rd_en = 1'b0;
        #1 check1(count === 0, "fifo accepted a read while empty");

        // ---------------- randomised push/pop against the scoreboard ------
        for (i = 0; i < 200; i = i + 1) begin
            if (($random(seed) % 2) == 0) begin
                if (!full) fifo_push($random(seed));
            end else begin
                if (!empty) fifo_pop;
            end
            check1(count === mcount(), "fifo count disagrees with the scoreboard");
        end

        // ---------------- RAM: write then read back ----------------
        for (i = 0; i < 16; i = i + 1) begin
            @(posedge clk); #1;
            ram_we = 1'b1; ram_addr = i[7:0]; ram_din = (i * 7) & 8'hFF;
        end
        @(posedge clk); #1 ram_we = 1'b0;
        for (i = 0; i < 16; i = i + 1) begin
            @(posedge clk); #1 ram_addr = i[7:0];
            @(posedge clk); #1;                    // registered read: 1 cycle
            check1(ram_q === ((i * 7) & 8'hFF), "ram read-back mismatch");
        end

        if (errors == 0) $display("PASS - L4 FIFO and RAM, all checks correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
