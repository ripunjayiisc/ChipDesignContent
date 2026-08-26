// ---------------------------------------------------------------------------
// mux4.v  -  parameterised 4:1 multiplexer  (Lab L1)
//
// Note the DEFAULT branch. Without it, sel = 2'bx0 leaves y unassigned and the
// tool infers a latch. With it, this is pure combinational logic.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module mux4 #(
    parameter integer W = 8
)(
    input  wire [W-1:0] d0, d1, d2, d3,
    input  wire [1:0]   sel,
    output reg  [W-1:0] y
);

    always @(*) begin
        y = {W{1'b0}};                 // default first - no latch possible
        case (sel)
            2'b00:   y = d0;
            2'b01:   y = d1;
            2'b10:   y = d2;
            2'b11:   y = d3;
            default: y = {W{1'b0}};
        endcase
    end

endmodule

`default_nettype wire
