// ---------------------------------------------------------------------------
//  seq101_mealy.v  -  '101' sequence detector, MEALY style
//
//  Same language, same overlapping rule, one fewer state and one cycle less
//  latency.  `det` is a function of the state AND the current input, so it
//  rises in the SAME cycle as the final 1.
//
//  The price: `det` is combinational from `din`.  It inherits whatever
//  glitches and timing `din` has, and it eats into the setup budget of
//  whatever it feeds.  That trade - one cycle of latency against a clean
//  registered output - is the entire Moore-versus-Mealy decision.
// ---------------------------------------------------------------------------

module seq101_mealy (
    input      clk,
    input      rst_n,
    input      din,
    output     det
);
    localparam [1:0] S_IDLE = 2'd0,   // nothing useful seen
                     S_1    = 2'd1,   // seen '1'
                     S_10   = 2'd2;   // seen '10'   <- no accepting state needed

    reg [1:0] state, next_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S_IDLE;
        else        state <= next_state;
    end

    always @(*) begin
        next_state = state;
        case (state)
            S_IDLE : next_state = din ? S_1 : S_IDLE;
            S_1    : next_state = din ? S_1 : S_10;
            S_10   : next_state = din ? S_1 : S_IDLE;   // the hit also re-arms
            default: next_state = S_IDLE;
        endcase
    end

    // output logic - STATE **AND** INPUT.  This is what makes it Mealy.
    assign det = (state == S_10) && din;

endmodule
