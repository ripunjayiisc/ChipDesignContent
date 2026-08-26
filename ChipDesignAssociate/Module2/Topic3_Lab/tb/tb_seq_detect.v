// ---------------------------------------------------------------------------
// tb_seq_detect.v  -  drives the SAME bit stream into the Moore and the Mealy
//                     '1011' detectors so the one-cycle offset is visible.
//
//   iverilog -g2012 -o fsm.out rtl/seq_detect_1011.v \
//            rtl/seq_detect_1011_mealy.v tb/tb_seq_detect.v
//   vvp fsm.out
//   gtkwave fsm.vcd &
//
// Stream: 1 0 1 1 0 1 1 0    ->  the pattern 1011 completes TWICE
//         (bits 1-4, and again at bits 4-7 because overlapping is allowed)
//
// TESTBENCH DISCIPLINE worth copying:
//   * reset is released BETWEEN clock edges, never on one - releasing it on
//     an edge is a race, and the state register stays X for several cycles.
//   * stimulus changes just AFTER a rising edge, so it is stable long before
//     the next one (this is what t_setup means in a real design).
//   * the Moore output is sampled just after the edge (it is registered);
//     the Mealy output is sampled at the falling edge, mid-cycle, where it
//     is settled and unambiguous.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_seq_detect;

    reg  clk   = 1'b0;
    reg  rst_n = 1'b0;
    reg  x     = 1'b0;
    wire z_moore, z_mealy;

    integer i;
    integer moore_hits = 0;
    integer mealy_hits = 0;
    integer errors     = 0;

    localparam integer NBITS = 8;
    reg [NBITS-1:0] stream = 8'b1011_0110;      // driven MSB first

    always #5 clk = ~clk;                       // 100 MHz

    seq_detect_1011       u_moore (.clk(clk), .rst_n(rst_n), .x(x), .z(z_moore));
    seq_detect_1011_mealy u_mealy (.clk(clk), .rst_n(rst_n), .x(x), .z(z_mealy));

    // Moore output is registered: sample 1 ns after each rising edge.
    always @(posedge clk) if (rst_n) begin
        #1 if (z_moore) moore_hits = moore_hits + 1;
    end

    // Mealy output is combinational: sample mid-cycle, at the falling edge.
    always @(negedge clk) if (rst_n && z_mealy) mealy_hits = mealy_hits + 1;

    initial begin
        $dumpfile("fsm.vcd");
        $dumpvars(0, tb_seq_detect);

        #12 rst_n = 1'b1;                       // release between edges

        @(posedge clk);
        for (i = NBITS - 1; i >= 0; i = i - 1) begin
            #2 x = stream[i];                   // stable well before the next edge
            @(posedge clk);
        end
        #2 x = 1'b0;
        repeat (3) @(posedge clk);
        #2;

        $display("stream            = %b  (driven MSB first)", stream);
        $display("Moore  Z pulses   = %0d   (expected 2)", moore_hits);
        $display("Mealy  Z pulses   = %0d   (expected 2)", mealy_hits);

        if (moore_hits != 2) begin
            $display("  *** FAIL - Moore detector"); errors = errors + 1;
        end
        if (mealy_hits != 2) begin
            $display("  *** FAIL - Mealy detector"); errors = errors + 1;
        end

        if (errors == 0)
            $display("\nPASS - both detectors found exactly two overlapping matches");
        else
            $display("\nFAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
