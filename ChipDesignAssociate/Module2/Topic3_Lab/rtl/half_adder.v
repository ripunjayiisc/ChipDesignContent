// ---------------------------------------------------------------------------
// half_adder.v  -  1-bit half adder  (Module 2, Topic 3, Tutorial T1/T2)
//
//   S = A XOR B        C = A AND B
//
// Note the limitation: there is no carry INPUT, so a half adder can only ever
// be used for the least-significant bit of a multi-bit adder.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module half_adder (
    input  wire a,
    input  wire b,
    output wire sum,
    output wire cout
);

    assign sum  = a ^ b;
    assign cout = a & b;

endmodule
