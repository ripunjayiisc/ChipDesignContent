// ---------------------------------------------------------------------------
// tb_adder4.v  -  exhaustive testbench for the 4-bit ripple adder
//                 (all 16 x 16 x 2 = 512 input combinations)
//
//   iverilog -g2012 -o a4.out rtl/full_adder.v rtl/adder4.v tb/tb_adder4.v
//   vvp a4.out
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_adder4;

    reg  [3:0] a, b;
    reg        cin;
    wire [3:0] sum;
    wire       cout;
    integer i, j, k;
    integer errors = 0;

    adder4 dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        $dumpfile("a4.vcd");
        $dumpvars(0, tb_adder4);

        for (i = 0; i < 16; i = i + 1)
        for (j = 0; j < 16; j = j + 1)
        for (k = 0; k < 2;  k = k + 1) begin
            a = i[3:0]; b = j[3:0]; cin = k[0];
            #5;
            if ({cout, sum} !== (a + b + cin)) begin
                $display("FAIL  %0d + %0d + %0d  ->  %0d (expected %0d)",
                         a, b, cin, {cout, sum}, a + b + cin);
                errors = errors + 1;
            end
        end

        if (errors == 0) $display("PASS - all 512 combinations correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
