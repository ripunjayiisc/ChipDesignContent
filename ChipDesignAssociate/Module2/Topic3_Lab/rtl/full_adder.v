// ---------------------------------------------------------------------------
// full_adder.v  -  1-bit full adder  (Module 2, Topic 3, Tutorial T2)
//
//   S    = A XOR B XOR Cin
//   Cout = AB + Cin(A XOR B)
//
// Pure combinational logic: no clock, no state, no feedback.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module full_adder (
    input  wire a,
    input  wire b,
    input  wire cin,
    output wire sum,
    output wire cout
);

    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));

endmodule
