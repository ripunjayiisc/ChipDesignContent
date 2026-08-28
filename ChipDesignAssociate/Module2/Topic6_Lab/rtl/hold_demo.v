// ---------------------------------------------------------------------------
// hold_demo.v  -  two flip-flops with NOTHING between them.
//
// This is the shape every hold violation has. There is no logic on the path,
// so the data arrives at the second flop almost immediately after the clock
// edge - about one clock-to-Q later. If the clock reaches the second flop
// LATER than the first (positive skew), the new data can arrive before the
// old data has been safely captured, and the second flop samples the wrong
// value.
//
// A hold violation is not fixed by slowing the clock down. It is a race
// between two things that both happen at the same edge, so the period does
// not appear in the arithmetic at all. That surprises people, and it is the
// single most important fact about hold.
// ---------------------------------------------------------------------------
`default_nettype none

module hold_demo (
    input  wire clk,
    input  wire rst_n,
    input  wire din,
    output reg  dout
);
    reg q1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q1   <= 1'b0;
            dout <= 1'b0;
        end else begin
            q1   <= din;
            dout <= q1;        // no logic at all on this path
        end
    end
endmodule

`default_nettype wire
