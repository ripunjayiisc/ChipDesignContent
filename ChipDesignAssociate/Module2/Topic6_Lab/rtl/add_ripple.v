// ---------------------------------------------------------------------------
// add_ripple.v  -  a W-bit ripple-carry adder, registered in and out.
//
// The carry has to travel through every bit position in turn, so the longest
// path grows LINEARLY with W. That makes this the clearest possible subject
// for timing analysis: you can predict the answer before you run the tool, and
// then watch the tool agree with you.
//
//     path = a_reg/b_reg -> FA[0] -> FA[1] -> ... -> FA[W-1] -> sum_reg
//
// Lab T1 sweeps W and plots Fmax. Lab T2 pipelines it. Lab T3 replaces the
// whole thing with "assign {cout,sum} = a + b" and compares - the tool then
// chooses the adder structure itself, and chooses better.
// ---------------------------------------------------------------------------
`default_nettype none

module add_ripple #(
    parameter integer W = 32
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    output reg  [W-1:0] sum,
    output reg          cout
);
    reg  [W-1:0] a_q, b_q;
    wire [W:0]   c;
    wire [W-1:0] s;

    assign c[0] = 1'b0;

    genvar i;
    generate
        for (i = 0; i < W; i = i + 1) begin : bit_slice
            // one full adder, written structurally so the carry chain is real
            assign s[i]   = a_q[i] ^ b_q[i] ^ c[i];
            assign c[i+1] = (a_q[i] & b_q[i]) | (c[i] & (a_q[i] ^ b_q[i]));
        end
    endgenerate

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a_q <= {W{1'b0}};  b_q <= {W{1'b0}};
            sum <= {W{1'b0}};  cout <= 1'b0;
        end else begin
            a_q  <= a;
            b_q  <= b;
            sum  <= s;
            cout <= c[W];
        end
    end
endmodule

`default_nettype wire
