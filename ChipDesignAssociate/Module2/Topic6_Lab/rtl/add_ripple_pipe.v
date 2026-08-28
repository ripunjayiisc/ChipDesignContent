// ---------------------------------------------------------------------------
// add_ripple_pipe.v  -  the same ripple adder, cut in half by a register.
//
// Stage 1 adds the low half and registers the carry out of bit W/2-1.
// Stage 2 adds the high half, starting from that registered carry.
//
// The longest path is now half as long, so the clock can be roughly twice as
// fast. The answer arrives one cycle later than before - that is the price,
// and it is almost always worth paying.
//
// NOTE the low half of the sum must be DELAYED by one cycle so that it comes
// out alongside the high half. Forgetting that is the classic pipelining bug:
// half the answer arrives a cycle early.
// ---------------------------------------------------------------------------
`default_nettype none

module add_ripple_pipe #(
    parameter integer W = 32
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    output reg  [W-1:0] sum,
    output reg          cout
);
    localparam integer H = W / 2;

    reg  [W-1:0] a_q, b_q;
    wire [H:0]   cl;
    wire [H-1:0] sl;

    assign cl[0] = 1'b0;
    genvar i;
    generate
        for (i = 0; i < H; i = i + 1) begin : lo
            assign sl[i]   = a_q[i] ^ b_q[i] ^ cl[i];
            assign cl[i+1] = (a_q[i] & b_q[i]) | (cl[i] & (a_q[i] ^ b_q[i]));
        end
    endgenerate

    // ---- the pipeline register, in the middle of the carry chain ----------
    reg  [H-1:0] sl_q;        // the low sum, delayed to stay with the high half
    reg          cmid_q;      // the carry crossing the cut
    reg  [H-1:0] ah_q, bh_q;  // the high operands, delayed to meet the carry

    wire [H:0]   ch;
    wire [H-1:0] sh;
    assign ch[0] = cmid_q;
    generate
        for (i = 0; i < H; i = i + 1) begin : hi
            assign sh[i]   = ah_q[i] ^ bh_q[i] ^ ch[i];
            assign ch[i+1] = (ah_q[i] & bh_q[i]) | (ch[i] & (ah_q[i] ^ bh_q[i]));
        end
    endgenerate

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_q <= {W{1'b0}};  b_q <= {W{1'b0}};
            sl_q <= {H{1'b0}}; cmid_q <= 1'b0;
            ah_q <= {H{1'b0}}; bh_q <= {H{1'b0}};
            sum <= {W{1'b0}};  cout <= 1'b0;
        end else begin
            a_q    <= a;
            b_q    <= b;
            sl_q   <= sl;              // stage 1 result, held for stage 2
            cmid_q <= cl[H];           // the carry across the cut
            ah_q   <= a_q[W-1:H];      // operands travel with the carry
            bh_q   <= b_q[W-1:H];
            sum    <= {sh, sl_q};      // both halves, aligned
            cout   <= ch[H];
        end
    end
endmodule

`default_nettype wire
