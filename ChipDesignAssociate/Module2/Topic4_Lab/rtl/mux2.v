// ---------------------------------------------------------------------------
// mux2.v  -  parameterised 2:1 multiplexer  (Lab L1)
//
// Three equivalent styles are shown in the workbook; this is the one to use.
// The ternary operator IS a multiplexer - the commonest construct in all RTL.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module mux2 #(
    parameter integer W = 8
)(
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    input  wire         sel,
    output wire [W-1:0] y
);

    assign y = sel ? b : a;

endmodule

`default_nettype wire
