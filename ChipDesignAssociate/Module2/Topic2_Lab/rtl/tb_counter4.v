// Self-checking testbench for the running example. It does not print a
// waveform and hope you look at it - it checks every cycle against a model
// and reports a count of mismatches.
`timescale 1ns / 1ps

module tb_counter4;
    reg clk = 0, rst_n, en;
    wire [3:0] count;
    wire tc;
    reg  [3:0] model;
    integer i, errors;

    counter4 dut (.clk(clk), .rst_n(rst_n), .en(en), .count(count), .tc(tc));
    always #5 clk = ~clk;

    initial begin
        $dumpfile("build/counter4.vcd"); $dumpvars(0, tb_counter4);
        errors = 0;
        rst_n = 0; en = 0; model = 0;
        @(posedge clk); #1;
        rst_n = 1; en = 1;

        $display("");
        $display("  === the running example: 4-bit counter ===");
        $display("");
        for (i = 0; i < 20; i = i + 1) begin
            @(posedge clk); #1;
            model = model + 4'd1;
            if (count !== model) begin
                errors = errors + 1;
                $display("  cycle %0d  count=%b  EXPECTED %b   MISMATCH",
                         i, count, model);
            end
            if (count == 4'd15 && tc !== 1'b1) begin
                errors = errors + 1;
                $display("  cycle %0d  count=1111 but tc=%b   tc is wrong", i, tc);
            end
            if (i < 3 || i > 13)
                $display("  cycle %2d   count=%b   tc=%b", i, count, tc);
            else if (i == 3)
                $display("      ...");
        end

        // hold: with en low the count must not move
        en = 0;
        @(posedge clk); #1;
        if (count !== model) begin
            errors = errors + 1;
            $display("  count moved while en was low   MISMATCH");
        end else
            $display("  en held low          count=%b   held correctly", count);

        $display("");
        $display("  cycles checked : 21   mismatches : %0d", errors);
        $display("  %s", (errors == 0) ? "PASS - counts, wraps, flags and holds correctly"
                                       : "FAIL");
        $display("");
        $finish;
    end
endmodule
