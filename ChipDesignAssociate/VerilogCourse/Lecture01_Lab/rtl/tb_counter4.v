// tb_counter4 - stimulus for counter4, and a self-check.
//
// A test bench is NOT hardware. It is a program that drives the hardware and
// watches what comes out, so it may use delays, loops and $display freely.
`timescale 1ns/1ps
module tb_counter4;
    reg        clk = 1'b0;
    reg        rst = 1'b1;
    wire [3:0] q;
    integer    errors = 0;
    integer    i;
    reg  [3:0] expected;

    counter4 dut (.clk(clk), .rst(rst), .q(q));

    always #5 clk = ~clk;          // a 100 MHz clock: 10 ns period

    initial begin
        $dumpfile("out/counter4.vcd");
        $dumpvars(0, tb_counter4);

        // The rising edge at t=5 ns happens while rst is still high, so the
        // register is cleared there. We release reset on the falling edge at
        // t=10 ns, which means the NEXT rising edge (t=15 ns) is already the
        // first counting edge - hence expected starts at 1, not 0.
        @(negedge clk);
        if (q !== 4'd0) begin
            $display("MISMATCH after reset: q=%0d expected=0", q);
            errors = errors + 1;
        end
        rst      = 1'b0;
        expected = 4'd1;

        for (i = 0; i < 20; i = i + 1) begin
            @(negedge clk);
            if (q !== expected) begin
                $display("MISMATCH at step %0d: q=%0d expected=%0d",
                         i, q, expected);
                errors = errors + 1;
            end
            expected = expected + 4'd1;
        end

        if (errors == 0)
            $display("PASS  counter4 counted 0..15 and wrapped correctly");
        else
            $display("FAIL  %0d mismatches", errors);
        $finish;
    end
endmodule
