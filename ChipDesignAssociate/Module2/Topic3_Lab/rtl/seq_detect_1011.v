// ---------------------------------------------------------------------------
// seq_detect_1011.v  -  Moore FSM: overlapping '1011' sequence detector
//                       (Module 2, Topic 3, Tutorial T4)
//
// One serial bit arrives on x per clock.  z goes high for one cycle after the
// last four bits received were 1,0,1,1.  Sequences may OVERLAP, so the stream
//     1 0 1 1 0 1 1
// contains TWO occurrences.
//
// State meaning - each state records how much of the pattern has matched:
//     S0  nothing yet      S1  seen '1'      S2  seen '10'
//     S3  seen '101'       S4  seen '1011'  (this is the accepting state)
//
// Written in the standard THREE-BLOCK style:
//     block 1  state register     - sequential, non-blocking
//     block 2  next-state logic   - combinational, blocking, with a default
//     block 3  output logic       - combinational, Moore (state only)
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module seq_detect_1011 (
    input  wire clk,
    input  wire rst_n,
    input  wire x,
    output reg  z
);

    localparam S0 = 3'd0,
               S1 = 3'd1,
               S2 = 3'd2,
               S3 = 3'd3,
               S4 = 3'd4;

    reg [2:0] state, next;

    // ---- BLOCK 1 : state register --------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S0;
        else        state <= next;
    end

    // ---- BLOCK 2 : next-state logic ------------------------------------
    always @(*) begin
        next = state;                       // default => no inferred latch
        case (state)
            S0:      next = x ? S1 : S0;
            S1:      next = x ? S1 : S2;
            S2:      next = x ? S3 : S0;
            S3:      next = x ? S4 : S2;
            S4:      next = x ? S1 : S2;    // overlapping: reuse the suffix
            default: next = S0;             // SAFE FSM: recover from 5,6,7
        endcase
    end

    // ---- BLOCK 3 : output logic (Moore) --------------------------------
    always @(*) z = (state == S4);

endmodule
