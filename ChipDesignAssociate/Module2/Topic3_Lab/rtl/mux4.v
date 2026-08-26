// ---------------------------------------------------------------------------
// mux4.v  -  4-to-1 multiplexer, three equivalent styles
//
// All three synthesise to the same hardware.  Style 3 is the one you should
// normally write; note the DEFAULT assignment, which is what makes it
// impossible for the tool to infer a latch.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module mux4 (
    input  wire [3:0] d,
    input  wire [1:0] sel,
    output reg        y
);

    // Style 1 (continuous assign):  assign y = d[sel];
    // Style 2 (nested ternary)   :  assign y = sel[1] ? (sel[0] ? d[3] : d[2])
    //                                                 : (sel[0] ? d[1] : d[0]);
    // Style 3 (case) - preferred:
    always @(*) begin
        y = 1'b0;                       // default: no latch can be inferred
        case (sel)
            2'b00: y = d[0];
            2'b01: y = d[1];
            2'b10: y = d[2];
            2'b11: y = d[3];
        endcase
    end

endmodule
