// ---------------------------------------------------------------------------
// decoder3to8.v  -  3-to-8 decoder with active-high enable  (Lab L1)
//
// Binary code in, one-hot out. Written with a shift so it is width-independent:
// 1 << a  puts a single 1 at position a.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module decoder3to8 (
    input  wire [2:0] a,
    input  wire       en,
    output wire [7:0] y
);

    assign y = en ? (8'b0000_0001 << a) : 8'b0000_0000;

endmodule

`default_nettype wire
