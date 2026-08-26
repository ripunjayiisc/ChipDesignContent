// ---------------------------------------------------------------------------
// seq_detect_1011_mealy.v  -  Mealy version of the same detector
//
// Only FOUR states are needed, and z asserts one cycle EARLIER than the Moore
// version, because the output logic can see x directly.
//
// The price: z is combinational, so it can glitch.  Never drive a clock
// enable, a memory write or an off-chip pin from it without registering it
// first - at which point you are back to Moore timing anyway.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module seq_detect_1011_mealy (
    input  wire clk,
    input  wire rst_n,
    input  wire x,
    output reg  z
);

    localparam S0 = 2'd0,   // nothing yet
               S1 = 2'd1,   // seen '1'
               S2 = 2'd2,   // seen '10'
               S3 = 2'd3;   // seen '101'

    reg [1:0] state, next;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S0;
        else        state <= next;
    end

    always @(*) begin
        next = state;
        z    = 1'b0;                        // default both => no latch
        case (state)
            S0:      next = x ? S1 : S0;
            S1:      next = x ? S1 : S2;
            S2:      next = x ? S3 : S0;
            S3: begin
                     next = x ? S1 : S2;
                     z    = x;              // output on the TRANSITION
                 end
            default: next = S0;
        endcase
    end

endmodule
