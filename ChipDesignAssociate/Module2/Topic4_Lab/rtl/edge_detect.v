// ---------------------------------------------------------------------------
// edge_detect.v  -  rising / falling / any edge detector  (Lab L2)
//
// The whole trick is one register: remember what the signal was LAST cycle and
// compare. This tiny module appears in almost every real design.
//
// The input must already be synchronous to clk. If it comes from outside this
// clock domain, put it through synchroniser.v FIRST.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module edge_detect (
    input  wire clk,
    input  wire rst_n,
    input  wire sig,
    output wire rise,
    output wire fall,
    output wire any
);

    reg sig_d;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) sig_d <= 1'b0;
        else        sig_d <= sig;
    end

    assign rise = sig & ~sig_d;
    assign fall = ~sig & sig_d;
    assign any  = sig ^ sig_d;

endmodule

`default_nettype wire
