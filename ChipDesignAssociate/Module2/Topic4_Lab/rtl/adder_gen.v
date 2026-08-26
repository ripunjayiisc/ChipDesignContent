// ---------------------------------------------------------------------------
// adder_gen.v  -  N-bit ripple-carry adder built with a generate loop (Lab L1)
//
// Demonstrates generate/genvar: ONE description, any width. Compare the
// synthesis result with  assign {cout,sum} = a + b + cin;  and see which the
// tool prefers when you constrain it for speed.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module full_adder (
    input  wire a, b, cin,
    output wire sum, cout
);
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule


module adder_gen #(
    parameter integer W = 8
)(
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    input  wire         cin,
    output wire [W-1:0] sum,
    output wire         cout
);

    wire [W:0] c;
    assign c[0] = cin;
    assign cout = c[W];

    genvar i;
    generate
        for (i = 0; i < W; i = i + 1) begin : bit_slice
            full_adder u_fa (
                .a   (a[i]),
                .b   (b[i]),
                .cin (c[i]),
                .sum (sum[i]),
                .cout(c[i+1])
            );
        end
    endgenerate

endmodule

`default_nettype wire
