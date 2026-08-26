// ---------------------------------------------------------------------------
// bcd_counter.v  -  mod-10 (BCD) synchronous up-counter with enable
//                   (Module 2, Topic 3, Tutorial T3, Practical Example 5)
//
// Counts 0,1,...,9,0,1,...   All four flip-flops share ONE clock, so every
// bit changes on the same edge - unlike a ripple counter.
//
// The gate-level equivalent derived in the slides is:
//     D0 = Q0'
//     D1 = Q1 XOR (Q0 . Q3')
//     D2 = Q2 XOR (Q1 . Q0)
//     D3 = Q3 XOR (Q3.Q0 + Q2.Q1.Q0)
// Synthesis derives exactly this from the code below.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module bcd_counter (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    output reg  [3:0] cnt
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)             cnt <= 4'd0;
        else if (en) begin
            if (cnt == 4'd9)    cnt <= 4'd0;      // the ONLY special case
            else                cnt <= cnt + 4'd1;
        end
    end

endmodule
