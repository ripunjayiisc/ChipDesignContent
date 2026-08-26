// ---------------------------------------------------------------------------
// seq_detect_1011_onehot.v  -  identical behaviour to seq_detect_1011.v, but
//                              with the state register explicitly one-hot
//                              encoded.  (Module 2, Topic 3, Tutorial T4)
//
// The ONLY difference is the (* fsm_encoding = "one-hot" *) attribute.  Run
// both through Yosys and compare:
//
//     binary  (seq_detect_1011.v)         3 flip-flops, more next-state logic
//     one-hot (this file)                 5 flip-flops, less next-state logic
//
// On an FPGA the one-hot version is usually faster and costs nothing extra,
// because flip-flops are abundant and LUT depth is what limits the clock.
// On an ASIC the binary version is usually smaller.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module seq_detect_1011_onehot (
    input  wire clk,
    input  wire rst_n,
    input  wire x,
    output reg  z
);

    localparam S0 = 3'd0, S1 = 3'd1, S2 = 3'd2, S3 = 3'd3, S4 = 3'd4;

    (* fsm_encoding = "one-hot" *) reg [2:0] state;
    reg [2:0] next;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S0;
        else        state <= next;
    end

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
