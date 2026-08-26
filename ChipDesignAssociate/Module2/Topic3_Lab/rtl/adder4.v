// ---------------------------------------------------------------------------
// adder4.v  -  4-bit ripple-carry adder  (Module 2, Topic 3, Tutorial T2)
//
// Four full adders chained Cout -> Cin.  Correct and compact, but the carry
// must RIPPLE from bit 0 to bit 3, so the worst-case delay grows linearly
// with the width:   t_adder = (n-1) * t_carry + t_sum
//
// Compare the synthesised delay of this against  assign {cout,sum} = a+b+cin;
// and let the tool choose a carry-lookahead structure instead.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module adder4 (
    input  wire [3:0] a,
    input  wire [3:0] b,
    input  wire       cin,
    output wire [3:0] sum,
    output wire       cout
);

    wire [3:1] c;          // internal carries: c[1] .. c[3]

    full_adder fa0 (.a(a[0]), .b(b[0]), .cin(cin ), .sum(sum[0]), .cout(c[1] ));
    full_adder fa1 (.a(a[1]), .b(b[1]), .cin(c[1]), .sum(sum[1]), .cout(c[2] ));
    full_adder fa2 (.a(a[2]), .b(b[2]), .cin(c[2]), .sum(sum[2]), .cout(c[3] ));
    full_adder fa3 (.a(a[3]), .b(b[3]), .cin(c[3]), .sum(sum[3]), .cout(cout ));

endmodule
