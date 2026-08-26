// ---------------------------------------------------------------------------
// reg_en.v  -  parameterised register with async reset and clock enable
//              (Lab L2)  -  THE workhorse template. Learn it by heart.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module reg_en #(
    parameter integer W    = 8,
    parameter [W-1:0] INIT = {W{1'b0}}
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire         en,
    input  wire [W-1:0] d,
    output reg  [W-1:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)     q <= INIT;
        else if (en)    q <= d;
    end

endmodule

`default_nettype wire
