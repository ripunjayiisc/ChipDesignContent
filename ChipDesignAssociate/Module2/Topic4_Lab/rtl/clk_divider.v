// ---------------------------------------------------------------------------
// clk_divider.v  -  a TICK generator, not a clock generator  (Lab L2)
//
// This is the RIGHT way to run something slowly. It produces a one-cycle-wide
// ENABLE pulse every DIV cycles, and every flip-flop in the design keeps using
// the SAME clk.
//
// The WRONG way is to divide the clock and use the divided signal as a clock.
// That creates a second clock domain out of combinational logic, breaks static
// timing analysis, and is one of the fastest ways to make a design that works
// in simulation and fails in silicon.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module clk_divider #(
    parameter integer DIV = 50_000        // 50 MHz -> 1 kHz
)(
    input  wire clk,
    input  wire rst_n,
    output reg  tick
);

    localparam integer CW = (DIV <= 2) ? 1 : $clog2(DIV);
    reg [CW-1:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt  <= {CW{1'b0}};
            tick <= 1'b0;
        end else if (cnt == DIV[CW-1:0] - 1'b1) begin
            cnt  <= {CW{1'b0}};
            tick <= 1'b1;                 // exactly one clk cycle wide
        end else begin
            cnt  <= cnt + 1'b1;
            tick <= 1'b0;
        end
    end

endmodule

`default_nettype wire
