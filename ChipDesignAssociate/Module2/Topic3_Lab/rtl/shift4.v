// ---------------------------------------------------------------------------
// shift4.v  -  4-bit serial-in / parallel-out shift register
//              (Module 2, Topic 3, Tutorial T3)
//
// One clock edge moves every bit one position up.  sin enters at bit 0 and
// appears at q[3] exactly four clock cycles later.
//
// EXPERIMENT: change  <=  to  =  and re-synthesise.  The blocking version
// collapses to a SINGLE flip-flop, because q[1] is updated before q[2] reads
// it - and simulation and hardware then disagree.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module shift4 (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       sin,
    output reg  [3:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 4'b0000;
        else        q <= {q[2:0], sin};
    end

endmodule
