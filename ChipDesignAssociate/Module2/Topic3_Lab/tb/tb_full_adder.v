// ---------------------------------------------------------------------------
// tb_full_adder.v  -  exhaustive self-checking testbench (all 8 input cases)
//
//   iverilog -g2012 -o fa.out rtl/full_adder.v tb/tb_full_adder.v
//   vvp fa.out
//   gtkwave fa.vcd &
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_full_adder;

    reg  a, b, cin;
    wire sum, cout;
    integer i;
    integer errors = 0;

    full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        $dumpfile("fa.vcd");
        $dumpvars(0, tb_full_adder);

        $display("  a b cin | cout sum | expected");
        $display("  --------+----------+---------");
        for (i = 0; i < 8; i = i + 1) begin
            {a, b, cin} = i[2:0];
            #10;
            $display("  %b %b  %b  |   %b   %b  |    %b",
                     a, b, cin, cout, sum, (a + b + cin));
            if ({cout, sum} !== (a + b + cin)) begin
                $display("  *** FAIL on a=%b b=%b cin=%b", a, b, cin);
                errors = errors + 1;
            end
        end

        if (errors == 0) $display("\nPASS - all 8 cases correct");
        else             $display("\nFAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
