// ---------------------------------------------------------------------------
// slow_path.v  -  a long path that only has to be right every FOURTH cycle.
//
// A 2-bit counter makes 'tick' high one cycle in four. The wide ripple add is
// only ever captured on a tick, so the logic genuinely has four clock periods
// to settle - but the timing analyser cannot know that. It sees a register,
// some logic, and another register, and it assumes one period. It will report
// a violation that is not real.
//
// The fix is not to change the design. It is to TELL the tool the truth:
//
//     set_multicycle_path 4 -from a_q_reg -to acc_reg
//
// This is the single most useful optimisation in the whole topic, because it
// costs nothing: no extra area, no extra latency, no RTL change. It is also
// the most dangerous, because if the claim is false the chip fails and no
// simulation will ever show it. A multicycle constraint is a PROMISE about the
// design, and somebody must check it.
// ---------------------------------------------------------------------------
`default_nettype none

module slow_path #(
    parameter integer W = 32
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    output reg  [W-1:0] acc,
    output wire         tick
);
    reg [1:0]   phase;
    reg [W-1:0] a_q, b_q;

    assign tick = (phase == 2'b11);

    wire [W:0]   c;
    wire [W-1:0] s;
    assign c[0] = 1'b0;

    genvar i;
    generate
        for (i = 0; i < W; i = i + 1) begin : bit_slice
            assign s[i]   = a_q[i] ^ b_q[i] ^ c[i];
            assign c[i+1] = (a_q[i] & b_q[i]) | (c[i] & (a_q[i] ^ b_q[i]));
        end
    endgenerate

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase <= 2'b00;
            a_q   <= {W{1'b0}};
            b_q   <= {W{1'b0}};
            acc   <= {W{1'b0}};
        end else begin
            phase <= phase + 2'b01;
            if (tick) begin              // operands change only on a tick ...
                a_q <= a;
                b_q <= b;
                acc <= s;                // ... and so is the result captured
            end
        end
    end
endmodule

`default_nettype wire
