// ---------------------------------------------------------------------------
// pipe_bal.v  -  the same work, with the heavy stage cut in two.
//
// The multiply is split into a partial-product stage and an accumulate stage,
// so no single stage carries all of it. Latency grows by one cycle; the clock
// gets faster. Compare Fmax with pipe_unbal.v.
// ---------------------------------------------------------------------------
module pipe_bal #(parameter W = 8) (
    input                  clk,
    input      [W-1:0]     a,
    input      [W-1:0]     b,
    output reg [2*W-1:0]   y
);
    reg [W-1:0]   s1a, s1b;
    reg [W-1:0]   s2, s2b;
    reg [2*W-1:0] p_lo, p_hi;
    reg [2*W-1:0] s3;

    localparam H = W/2;

    always @(posedge clk) begin
        s1a <= a + b;                                   // stage 1
        s1b <= b;
        s2  <= s1a ^ s1b;                               // stage 2
        s2b <= s1b;
        p_lo <= s2 * s2b[H-1:0];                        // stage 3a - low half
        p_hi <= s2 * s2b[W-1:H];                        // stage 3b - high half
        s3  <= p_lo + (p_hi << H);                      // stage 4 - combine
        y   <= s3 + 1'b1;                               // stage 5
    end
endmodule
