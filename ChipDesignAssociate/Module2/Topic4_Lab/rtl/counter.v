// ---------------------------------------------------------------------------
// counter.v  -  parameterised up/down counter with load, enable and a
//               terminal-count output  (Lab L2)
//
// MAX is the highest value the counter reaches; it wraps to 0 after MAX when
// counting up, and to MAX after 0 when counting down. Set MAX = 2**W-1 for a
// plain binary counter, or MAX = 9 for a BCD decade counter.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module counter #(
    parameter integer W   = 4,
    parameter integer MAX = 15
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire         en,
    input  wire         up,          // 1 = count up, 0 = count down
    input  wire         load,
    input  wire [W-1:0] din,
    output reg  [W-1:0] q,
    output wire         tc           // terminal count
);

    assign tc = en & (up ? (q == MAX[W-1:0]) : (q == {W{1'b0}}));

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)      q <= {W{1'b0}};
        else if (load)   q <= din;
        else if (en) begin
            if (up)      q <= (q == MAX[W-1:0]) ? {W{1'b0}}   : q + 1'b1;
            else         q <= (q == {W{1'b0}})  ? MAX[W-1:0]  : q - 1'b1;
        end
    end

endmodule

`default_nettype wire
