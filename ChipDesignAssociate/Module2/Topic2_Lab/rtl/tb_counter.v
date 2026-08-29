// Drives the Verilog counter through exactly the stimulus that
// vhdl/tb_counter.vhd drives the VHDL one, and prints the same lines.
`timescale 1ns / 1ps

module tb_counter;
    reg clk = 0, rst, en;
    wire [3:0] count;
    wire tc;
    integer i;

    counter #(.WIDTH(4)) dut (.clk(clk), .rst(rst), .en(en),
                              .count(count), .tc(tc));

    always #5 clk = ~clk;

    initial begin
        rst = 1; en = 0;
        @(posedge clk); #1;
        rst = 0; en = 1;

        for (i = 0; i <= 17; i = i + 1) begin
            @(posedge clk); #1;
            $display("  cycle %0d  count=%b  tc=%b", i, count, tc);
        end
        $display("Verilog run complete");
        $finish;
    end
endmodule
