// ---------------------------------------------------------------------------
// shift_reg.v  -  universal shift register  (Lab L2)
//
//   mode 00  hold          mode 01  shift right (sin enters at the MSB)
//   mode 10  shift left    mode 11  parallel load
//
// One always block, one case, four behaviours - and no latch, because every
// branch assigns q and there is a default.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module shift_reg #(
    parameter integer W = 8
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire [1:0]   mode,
    input  wire         sin,
    input  wire [W-1:0] din,
    output reg  [W-1:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= {W{1'b0}};
        else begin
            case (mode)
                2'b00:   q <= q;                    // hold
                2'b01:   q <= {sin, q[W-1:1]};      // shift right
                2'b10:   q <= {q[W-2:0], sin};      // shift left
                2'b11:   q <= din;                  // parallel load
                default: q <= q;
            endcase
        end
    end

endmodule

`default_nettype wire
