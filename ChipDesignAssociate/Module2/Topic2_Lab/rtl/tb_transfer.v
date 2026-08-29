// Watch the data march through the registers, one stage per clock edge.
`timescale 1ns / 1ps

module tb_transfer;
    reg clk = 0, rst;
    reg  [7:0] din;
    wire [7:0] result, r_x, r_y, r_z, r_acc;
    integer c;

    transfer dut (.clk(clk), .rst(rst), .din(din), .result(result),
                  .r_x(r_x), .r_y(r_y), .r_z(r_z), .r_acc(r_acc));

    always #5 clk = ~clk;

    initial begin
        $dumpfile("build/transfer.vcd"); $dumpvars(0, tb_transfer);
        rst = 1; din = 0;
        @(posedge clk); #1; rst = 0;

        $display("");
        $display("  === one value entering a chain of registers ===");
        $display("");
        $display("  A single 5 is applied on cycle 0 and never again. Follow it.");
        $display("");
        $display("  cycle   din |    x     y     z   |  acc");
        $display("  ------------+--------------------+------");

        for (c = 0; c < 7; c = c + 1) begin
            din = (c == 0) ? 8'd5 : 8'd0;
            @(posedge clk); #1;
            $display("    %0d      %3d |  %3d   %3d   %3d  |  %3d",
                     c, din, r_x, r_y, r_z, r_acc);
        end

        $display("");
        $display("  The 5 lands in x on the first edge, becomes 6 in y on the");
        $display("  second, 12 in z on the third, and reaches acc on the fourth.");
        $display("  Nothing moved between edges. That is the whole model.");
        $display("");
        $finish;
    end
endmodule
