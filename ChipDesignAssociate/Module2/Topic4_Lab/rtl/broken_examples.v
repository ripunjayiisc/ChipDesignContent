// ---------------------------------------------------------------------------
// broken_examples.v  -  DELIBERATELY WRONG. Never copy any of this.
//
// These modules exist so you can SEE each failure in a real tool report
// instead of only reading about it. Synthesise them and look:
//
//   yosys -p "read_verilog rtl/broken_examples.v; synth -top bad_latch; stat"
//
// Then fix each one and watch the report change. That exercise teaches more
// than any amount of reading.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

// BUG 1 - incomplete assignment infers a transparent latch
module bad_latch (
    input  wire       enable,
    input  wire [1:0] sel,
    input  wire [3:0] d,
    output reg        y,
    output reg        w
);
    always @(*) begin
        if (enable) y = d[0];          // no else -> LATCH
    end
    always @(*) begin
        case (sel)
            2'b00: w = d[0];
            2'b01: w = d[1];
            2'b10: w = d[2];           // 2'b11 missing, no default -> LATCH
        endcase
    end
endmodule


// BUG 2 - blocking assignment in a clocked block collapses a shift register
module bad_blocking (
    input  wire clk,
    input  wire d,
    output reg  q1,
    output reg  q2
);
    always @(posedge clk) begin
        q1 = d;                        // should be <=
        q2 = q1;                       // q2 gets d, not the old q1
    end
endmodule


// BUG 3 - truncation, because the result is not wide enough
module bad_width (
    input  wire [3:0] a,
    input  wire [3:0] b,
    output wire [3:0] sum             // should be [4:0] to hold the carry
);
    assign sum = a + b;               // 9 + 8 = 17, truncated to 1
endmodule
