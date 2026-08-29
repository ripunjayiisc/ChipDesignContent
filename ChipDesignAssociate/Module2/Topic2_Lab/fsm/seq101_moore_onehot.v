// ---------------------------------------------------------------------------
//  seq101_moore_onehot.v  -  the SAME Moore machine, ONE-HOT encoded.
//
//  Line for line identical to seq101_moore.v except that the four states are
//  numbered 0001, 0010, 0100, 1000 instead of 00, 01, 10, 11.  Nothing about
//  the behaviour changes; only the number of flip-flops and the shape of the
//  decode logic do.
//
//  ENCODING is a real design decision:
//     binary    fewest flip-flops, more decode logic per output
//     one-hot   one flip-flop per state, but every decode is a single wire,
//               so the combinational paths are short - the usual choice on
//               FPGAs, where flip-flops are free and routing is not
//     gray      one bit changes per legal transition; useful when the state
//               crosses a clock domain
//
//  scripts/fsm.sh synthesises both and prints the two cell counts, so you can
//  see the trade rather than take it on faith.
// ---------------------------------------------------------------------------

module seq101_moore_onehot (
    input      clk,
    input      rst_n,
    input      din,
    output     det
);
    localparam [3:0] S_IDLE = 4'b0001,
                     S_1    = 4'b0010,
                     S_10   = 4'b0100,
                     S_101  = 4'b1000;

    reg [3:0] state, next_state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S_IDLE;
        else        state <= next_state;
    end

    always @(*) begin
        next_state = state;
        case (state)
            S_IDLE : next_state = din ? S_1   : S_IDLE;
            S_1    : next_state = din ? S_1   : S_10;
            S_10   : next_state = din ? S_101 : S_IDLE;
            S_101  : next_state = din ? S_1   : S_10;
            default: next_state = S_IDLE;      // recovers from an illegal code
        endcase
    end

    assign det = (state == S_101);

endmodule
