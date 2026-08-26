// ---------------------------------------------------------------------------
// synchroniser.v  -  N-stage clock-domain-crossing synchroniser  (Lab L2)
//
// Every signal entering this clock domain from outside it MUST pass through
// one of these. Two stages is the universal minimum; three for very high
// clock rates or safety-critical paths.
//
// This works for a SINGLE BIT ONLY. A multi-bit bus needs a Gray-coded
// pointer, a handshake, or an asynchronous FIFO - synchronising each bit
// separately lets different bits resolve on different cycles, so you can read
// a value that never existed.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module synchroniser #(
    parameter integer STAGES = 2
)(
    input  wire clk,
    input  wire rst_n,
    input  wire async_in,
    output wire sync_out
);

    reg [STAGES-1:0] sync_ff;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) sync_ff <= {STAGES{1'b0}};
        else        sync_ff <= {sync_ff[STAGES-2:0], async_in};
    end

    assign sync_out = sync_ff[STAGES-1];

endmodule

`default_nettype wire
