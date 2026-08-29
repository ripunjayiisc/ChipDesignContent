// ---------------------------------------------------------------------------
// pipe_unbal.v  -  a four-stage pipeline whose stages are badly unbalanced.
//
// Fmax is set by ONE stage: the slowest. Everything else in the design could
// be free and the clock would not go up. This module makes that concrete by
// giving stage 3 far more logic than the others.
//
//   stage 1   one add                        - light
//   stage 2   one xor                        - very light
//   stage 3   a 16-bit multiply              - heavy, and it sets Fmax
//   stage 4   one add                        - light
// ---------------------------------------------------------------------------
module pipe_unbal #(parameter W = 8) (
    input                  clk,
    input      [W-1:0]     a,
    input      [W-1:0]     b,
    output reg [2*W-1:0]   y
);
    reg [W-1:0]   s1a, s1b;
    reg [W-1:0]   s2;
    reg [2*W-1:0] s3;

    always @(posedge clk) begin
        s1a <= a + b;                 // stage 1
        s1b <= b;
        s2  <= s1a ^ s1b;             // stage 2
        s3  <= s2 * s1b;              // stage 3  <- the heavy one
        y   <= s3 + 1'b1;             // stage 4
    end
endmodule
