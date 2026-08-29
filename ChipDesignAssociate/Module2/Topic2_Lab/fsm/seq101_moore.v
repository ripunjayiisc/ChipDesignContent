// ---------------------------------------------------------------------------
//  seq101_moore.v  -  '101' sequence detector, MOORE style
//
//  Detects the bit pattern 1-0-1 arriving one bit per clock on `din`.
//  Overlapping matches are allowed: the stream 1 0 1 0 1 contains TWO
//  matches (bits 0-2 and bits 2-4), because after a hit we fall back to
//  "we have just seen a 1" rather than to the idle state.
//
//  MOORE: `det` is decoded from the state alone, so it is asserted in the
//  cycle AFTER the final 1 arrives.  One cycle of latency, but the output
//  is a clean function of a registered value.
// ---------------------------------------------------------------------------

module seq101_moore (
    input      clk,
    input      rst_n,
    input      din,
    output     det
);
    localparam [1:0] S_IDLE = 2'd0,   // nothing useful seen yet
                     S_1    = 2'd1,   // seen '1'
                     S_10   = 2'd2,   // seen '10'
                     S_101  = 2'd3;   // seen '101'  <- the accepting state

    reg [1:0] state, next_state;

    // block 1: state register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S_IDLE;
        else        state <= next_state;
    end

    // block 2: next-state logic
    always @(*) begin
        next_state = state;
        case (state)
            S_IDLE : next_state = din ? S_1   : S_IDLE;
            S_1    : next_state = din ? S_1   : S_10;
            S_10   : next_state = din ? S_101 : S_IDLE;
            S_101  : next_state = din ? S_1   : S_10;   // overlap handled here
            default: next_state = S_IDLE;
        endcase
    end

    // block 3: output logic - STATE ONLY.  This is what makes it Moore.
    assign det = (state == S_101);

endmodule
