// ---------------------------------------------------------------------------
// tb_v1_naive.v  -  Lab V1.  A NAIVE testbench. It is not wrong; it is weak.
//
// This is what almost everybody writes first: drive a few values in, read them
// back, print them, look at the transcript, declare victory.
//
// It has all six structural parts of a testbench and it does check its
// results - so it is already better than a testbench that only prints. What it
// lacks is COVERAGE OF THE SPECIFICATION. It never fills the FIFO, never
// empties it past zero, never reads and writes on the same cycle, and never
// wraps the pointers.
//
// Compile it against the golden FIFO and against all four broken ones:
//
//   ./scripts/clinic.sh
//
// It passes on all five. Every stage after this one closes part of that gap.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`ifndef DUT
  `define DUT fifo
`endif
`ifndef DUTNAME
  `define DUTNAME "fifo"
`endif

module tb_v1_naive;

    localparam integer W     = 8;
    localparam integer DEPTH = 8;
    localparam integer CLK   = 10;             // 10 ns period = 100 MHz

    // ---- 1. signals and the device under test -----------------------------
    reg              clk = 1'b0;
    reg              rst_n;
    reg              wr_en, rd_en;
    reg  [W-1:0]     wr_data;
    wire [W-1:0]     rd_data;
    wire             full, empty;
    wire [$clog2(DEPTH):0] count;

    `DUT #(.W(W), .DEPTH(DEPTH)) u_dut (
        .clk(clk), .rst_n(rst_n), .wr_en(wr_en), .wr_data(wr_data),
        .rd_en(rd_en), .rd_data(rd_data),
        .full(full), .empty(empty), .count(count)
    );

    always #(CLK/2) clk = ~clk;

    // ---- 2. one place that decides pass or fail ---------------------------
    integer errors = 0;

    task check(input [W-1:0] got, input [W-1:0] exp, input [255:0] msg);
        begin
            if (got !== exp) begin
                $display("FAIL %0t : %0s  got %h expected %h", $time, msg, got, exp);
                errors = errors + 1;
            end
        end
    endtask

    // ---- 3. stimulus helpers ----------------------------------------------
    task push(input [W-1:0] d);
        begin
            @(posedge clk); #1;
            wr_en = 1'b1; wr_data = d;
            @(posedge clk); #1;
            wr_en = 1'b0;
        end
    endtask

    task pop(output [W-1:0] d);
        begin
            @(posedge clk); #1;
            rd_en = 1'b1;
            d = rd_data;                    // first-word fall-through
            @(posedge clk); #1;
            rd_en = 1'b0;
        end
    endtask

    reg [W-1:0] got;

    // ---- 4. the test ------------------------------------------------------
    initial begin
        $dumpfile("v1.vcd");
        $dumpvars(0, tb_v1_naive);

        rst_n = 1'b0; wr_en = 1'b0; rd_en = 1'b0; wr_data = {W{1'b0}};
        repeat (3) @(posedge clk);
        #1 rst_n = 1'b1;                    // released between edges, never ON one

        push(8'hA1);
        push(8'hB2);
        push(8'hC3);

        pop(got);  check(got, 8'hA1, "first word out");
        pop(got);  check(got, 8'hB2, "second word out");
        pop(got);  check(got, 8'hC3, "third word out");

        repeat (2) @(posedge clk);

        // ---- 5. the verdict ------------------------------------------------
        if (errors == 0)
            $display("PASS - V1 naive testbench on %0s : 3 words in, 3 words out",
                     `DUTNAME);
        else
            $display("FAIL - V1 naive testbench on %0s : %0d errors",
                     `DUTNAME, errors);
        $finish;                            // ---- 6. stop ------------------
    end

    // a watchdog, so a hung DUT fails instead of running forever
    initial begin
        #(CLK * 2000);
        $display("FAIL - V1 timeout on %0s", `DUTNAME);
        $finish;
    end

endmodule
