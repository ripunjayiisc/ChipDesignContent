// ---------------------------------------------------------------------------
// seven_seg.v  -  hex digit to seven-segment decoder, active LOW  (Lab L1)
//
// Segment order is {g,f,e,d,c,b,a}, so bit 0 is segment a.
// Active low because that is how the displays on most FPGA boards are wired:
// a 0 lights the segment.
//
//        aaa
//       f   b
//       f   b
//        ggg
//       e   c
//       e   c
//        ddd
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module seven_seg (
    input  wire [3:0] digit,
    output reg  [6:0] seg_n
);

    always @(*) begin
        case (digit)                   //          gfedcba
            4'h0:    seg_n = 7'b100_0000;
            4'h1:    seg_n = 7'b111_1001;
            4'h2:    seg_n = 7'b010_0100;
            4'h3:    seg_n = 7'b011_0000;
            4'h4:    seg_n = 7'b001_1001;
            4'h5:    seg_n = 7'b001_0010;
            4'h6:    seg_n = 7'b000_0010;
            4'h7:    seg_n = 7'b111_1000;
            4'h8:    seg_n = 7'b000_0000;
            4'h9:    seg_n = 7'b001_0000;
            4'hA:    seg_n = 7'b000_1000;
            4'hB:    seg_n = 7'b000_0011;
            4'hC:    seg_n = 7'b100_0110;
            4'hD:    seg_n = 7'b010_0001;
            4'hE:    seg_n = 7'b000_0110;
            4'hF:    seg_n = 7'b000_1110;
            default: seg_n = 7'b111_1111;   // all segments off
        endcase
    end

endmodule

`default_nettype wire
