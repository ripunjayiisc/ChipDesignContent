// ---------------------------------------------------------------------------
// add_fast.v  -  the same adder, described as INTENT rather than structure.
//
// One line. The synthesiser is now free to choose the adder architecture, and
// it chooses better than a hand-written ripple chain: a carry-lookahead or
// carry-select tree whose depth grows with log(W) rather than with W.
//
// Comparing this with add_ripple.v at the same W is Lab T3, and it is the most
// useful single measurement in this topic.
// ---------------------------------------------------------------------------
`default_nettype none

module add_fast #(
    parameter integer W = 32
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    output reg  [W-1:0] sum,
    output reg          cout
);
    reg [W-1:0] a_q, b_q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_q <= {W{1'b0}};  b_q <= {W{1'b0}};
            sum <= {W{1'b0}};  cout <= 1'b0;
        end else begin
            a_q          <= a;
            b_q          <= b;
            {cout, sum}  <= a_q + b_q;
        end
    end
endmodule

`default_nettype wire
