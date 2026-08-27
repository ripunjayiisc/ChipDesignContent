// ---------------------------------------------------------------------------
// mac8.v  -  8x8 multiply-accumulate, ALL IN ONE CYCLE.
//
// This is the design that fails timing, and it fails for the most ordinary
// reason there is: too much logic between two flip-flops. The path is
//
//     a_reg / b_reg  ->  8x8 multiplier  ->  16-bit adder  ->  acc_reg
//
// and a multiplier is deep. Nothing here is badly written; it is simply
// asking for more work per cycle than the clock allows.
//
// mac8_pipe.v is the same function with one register added in the middle.
// Comparing the two is Lab T2.
// ---------------------------------------------------------------------------
`default_nettype none

module mac8 (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        en,
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    output reg  [15:0] acc
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)     acc <= 16'd0;
        else if (en)    acc <= acc + (a * b);
    end
endmodule

`default_nettype wire
