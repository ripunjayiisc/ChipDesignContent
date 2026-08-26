// ---------------------------------------------------------------------------
// broken_latch.v  -  DELIBERATELY WRONG.  Do not copy this style.
//
// This module exists so you can SEE an inferred latch in a synthesis report.
//
//   yosys -p "read_verilog rtl/broken_latch.v; synth -top broken_latch; stat"
//
// Look for  $_DLATCH_  in the cell list.  Then fix it by giving y a default
// value at the top of the always block, re-synthesise, and watch the latch
// disappear.
//
// WHY IT HAPPENS: the always block does not assign y on every path.  Verilog
// says "if you did not assign it, keep the old value", and the only hardware
// that can keep an old value is a storage element - so the tool builds one.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module broken_latch (
    input  wire       enable,
    input  wire [1:0] sel,
    input  wire [3:0] d,
    output reg        y,
    output reg        w
);

    // BUG 1: no else branch
    always @(*) begin
        if (enable) y = d[0];
    end

    // BUG 2: case without a default, and not all cases covered
    always @(*) begin
        case (sel)
            2'b00: w = d[0];
            2'b01: w = d[1];
            2'b10: w = d[2];
            // 2'b11 missing  ->  latch
        endcase
    end

endmodule
