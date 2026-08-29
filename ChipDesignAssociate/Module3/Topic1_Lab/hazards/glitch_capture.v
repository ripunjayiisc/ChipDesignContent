// ---------------------------------------------------------------------------
// glitch_capture.v  -  does a glitch actually matter?
//
// "Synchronous design tolerates glitches" is true, and it is repeated so often
// that people stop noticing the word SYNCHRONOUS. A glitch is harmless only
// where it is sampled by a clock edge after it has settled. Send the same
// glitchy signal somewhere that reacts to EDGES rather than to levels and it
// is not harmless at all.
//
// This module feeds one glitchy signal to three consumers and counts what each
// one does. The glitchy signal is the static-1 hazard from hz_static1.v, driven
// so that the glitch happens far away from any clock edge - the best case for
// the "it settles in time" argument.
//
//   d_path : f is DATA into a normally-clocked flop        (the safe use)
//   c_path : f is the CLOCK of a counter                   (edge-sensitive)
//   r_path : f is the ASYNCHRONOUS RESET of a flop         (edge/level-sensitive)
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module glitch_capture (
    input  a, input b, input c,
    input  clk,
    output reg  d_sampled,      // f, sampled by the clean clock
    output reg [7:0] c_edges,   // times f was used as a clock edge
    output reg  r_flag          // survives only if f never spuriously resets it
);

    wire f;

    // exactly the circuit from hz_static1.v
    wire nb, t1, t2;
    not #(4) g_inv (nb, b);
    and #(2) g_t1  (t1, a, nb);
    and #(2) g_t2  (t2, b, c);
    or  #(2) g_or  (f,  t1, t2);

    // 1. the SAFE use: f is data, sampled long after it has settled
    always @(posedge clk)
        d_sampled <= f;

    // 2. f used as a clock. Every glitch is a clock edge.
    initial c_edges = 0;
    always @(posedge f)
        c_edges <= c_edges + 8'd1;

    // 3. f used as an active-low asynchronous reset. Every downward glitch
    //    clears the flag, whatever the clock is doing.
    initial r_flag = 1'b1;
    always @(posedge clk or negedge f)
        if (!f) r_flag <= 1'b0;
        else    r_flag <= r_flag;

endmodule
