// ---------------------------------------------------------------------------
// debouncer.v  -  mechanical switch debouncer  (Lab L2)
//
// A real push-button bounces for 1-10 ms. This module only accepts a new level
// once the input has been STABLE for STABLE_COUNT clock cycles.
//
// Default: 50 MHz clock, 20 ms => 1_000_000 cycles. For simulation, override
// STABLE_COUNT with something small (say 8) or the testbench runs forever.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module debouncer #(
    parameter integer STABLE_COUNT = 1_000_000
)(
    input  wire clk,
    input  wire rst_n,
    input  wire noisy_in,
    output reg  clean_out
);

    localparam integer CW = (STABLE_COUNT <= 1) ? 1 : $clog2(STABLE_COUNT);

    wire sync_in;
    synchroniser #(.STAGES(2)) u_sync (
        .clk(clk), .rst_n(rst_n), .async_in(noisy_in), .sync_out(sync_in)
    );

    reg [CW-1:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt       <= {CW{1'b0}};
            clean_out <= 1'b0;
        end else if (sync_in != clean_out) begin
            // input differs from the accepted level - count how long it holds
            if (cnt == STABLE_COUNT[CW-1:0] - 1'b1) begin
                clean_out <= sync_in;              // stable long enough: accept
                cnt       <= {CW{1'b0}};
            end else begin
                cnt <= cnt + 1'b1;
            end
        end else begin
            cnt <= {CW{1'b0}};                     // agrees again: restart
        end
    end

endmodule

`default_nettype wire
