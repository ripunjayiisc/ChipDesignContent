// ---------------------------------------------------------------------------
// priority_encoder8.v  -  8-to-3 priority encoder with a valid output (Lab L1)
//
// This is the ONE place where if/else-if is the right choice: the branches are
// deliberately NOT mutually exclusive, and the priority is the specification.
//
// valid distinguishes 'input 0 is active' (y=000, valid=1) from
// 'nothing is active' (y=000, valid=0).
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module priority_encoder8 (
    input  wire [7:0] req,
    output reg  [2:0] y,
    output wire       valid
);

    assign valid = |req;               // reduction OR: 1 if ANY bit is set

    always @(*) begin
        y = 3'd0;                      // default - no latch
        if      (req[7]) y = 3'd7;
        else if (req[6]) y = 3'd6;
        else if (req[5]) y = 3'd5;
        else if (req[4]) y = 3'd4;
        else if (req[3]) y = 3'd3;
        else if (req[2]) y = 3'd2;
        else if (req[1]) y = 3'd1;
        else if (req[0]) y = 3'd0;
    end

endmodule

`default_nettype wire
