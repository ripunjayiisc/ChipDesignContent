// ---------------------------------------------------------------------------
// dff.v  -  D flip-flop with ASYNCHRONOUS active-low reset
//           (Module 2, Topic 3, Tutorial T3)
//
// The reset appears in the sensitivity list, so it takes effect immediately -
// even with no clock running.  This is the reference template for every
// sequential element in this course.
//
// Note the non-blocking assignment (<=).  In a clocked block it is mandatory:
// it makes every flip-flop sample its input BEFORE any of them update.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module dff (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 1'b0;
        else        q <= d;
    end

endmodule
