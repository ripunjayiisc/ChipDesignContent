// ---------------------------------------------------------------------------
// mac8_pipe.v  -  the same multiply-accumulate, cut into two stages.
//
//     stage 1 :  a_reg / b_reg  ->  8x8 multiplier  ->  prod_reg
//     stage 2 :  prod_reg       ->  16-bit adder    ->  acc_reg
//
// The function is identical; the RESULT now appears one cycle later. That is
// the whole trade: pipelining buys frequency and pays with latency.
//
// The valid bit is pipelined ALONGSIDE the data. Forgetting to do that is the
// classic pipelining bug: results arrive correctly but are flagged one or two
// cycles too early.
// ---------------------------------------------------------------------------
`default_nettype none

module mac8_pipe (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        en,
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    output reg  [15:0] acc,
    output reg         acc_valid
);
    reg [15:0] prod;
    reg        prod_valid;

    // ---- stage 1 : the multiply -------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prod       <= 16'd0;
            prod_valid <= 1'b0;
        end else begin
            prod       <= a * b;
            prod_valid <= en;          // the control travels with the data
        end
    end

    // ---- stage 2 : the accumulate -----------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            acc       <= 16'd0;
            acc_valid <= 1'b0;
        end else begin
            if (prod_valid) acc <= acc + prod;
            acc_valid <= prod_valid;
        end
    end
endmodule

`default_nettype wire
