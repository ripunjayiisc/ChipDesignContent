// ---------------------------------------------------------------------------
// decoder2to4.v  -  2-to-4 decoder with active-high enable
//
// Binary code in, one-hot out.  With en = 0 every output is inactive, which
// is how decoders are cascaded to build larger ones.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module decoder2to4 (
    input  wire [1:0] a,
    input  wire       en,
    output reg  [3:0] d
);

    always @(*) begin
        d = 4'b0000;                    // default: no latch
        if (en) begin
            case (a)
                2'b00: d = 4'b0001;
                2'b01: d = 4'b0010;
                2'b10: d = 4'b0100;
                2'b11: d = 4'b1000;
            endcase
        end
    end

endmodule
