// ---------------------------------------------------------------------------
// seq_detect_1011.v  -  the Topic 3 FSM, rewritten here as a Topic 4 exercise
//
// Identical behaviour to the Topic 3 version; kept in this lab so you can
// compare the two topics' treatment of the same problem side by side.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module seq_detect_1011 (
    input  wire clk,
    input  wire rst_n,
    input  wire x,
    output reg  z
);

    localparam [2:0] S0 = 3'd0, S1 = 3'd1, S2 = 3'd2, S3 = 3'd3, S4 = 3'd4;
    reg [2:0] state, next;

    always @(posedge clk or negedge rst_n)
        if (!rst_n) state <= S0;
        else        state <= next;

    always @(*) begin
        next = state;
        case (state)
            S0:      next = x ? S1 : S0;
            S1:      next = x ? S1 : S2;
            S2:      next = x ? S3 : S0;
            S3:      next = x ? S4 : S2;
            S4:      next = x ? S1 : S2;
            default: next = S0;
        endcase
    end

    always @(*) z = (state == S4);

endmodule

`default_nettype wire
