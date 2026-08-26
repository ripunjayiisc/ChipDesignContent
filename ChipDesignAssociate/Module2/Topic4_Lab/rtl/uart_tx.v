// ---------------------------------------------------------------------------
// uart_tx.v  -  UART transmitter, 8 data bits, no parity, 1 stop bit (8N1)
//               (Lab L5 - the capstone design)
//
// Frame, LSB first:   START(0)  D0 D1 D2 D3 D4 D5 D6 D7  STOP(1)
//
// CLKS_PER_BIT = f_clk / baud.  For 50 MHz and 115200 baud that is 434.
// The testbench overrides it with a small number so simulation is quick.
//
// Handshake: assert tx_start for one cycle while tx_data is valid. busy stays
// high until the stop bit has been sent; tx_done pulses for one cycle at the
// very end.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module uart_tx #(
    parameter integer CLKS_PER_BIT = 434
)(
    input  wire       clk,
    input  wire       rst_n,
    input  wire       tx_start,
    input  wire [7:0] tx_data,
    output reg        tx,
    output reg        busy,
    output reg        tx_done
);

    localparam [1:0] IDLE = 2'd0, START = 2'd1, DATA = 2'd2, STOP = 2'd3;

    // See the note in uart_rx.v: compute the limit as an INTEGER, then size it.
    // CLKS_PER_BIT[CW-1:0] would truncate and silently break the baud rate.
    localparam integer CW       = (CLKS_PER_BIT <= 2) ? 1 : $clog2(CLKS_PER_BIT);
    localparam integer FULL_BIT = CLKS_PER_BIT - 1;

    reg [1:0]    state;
    reg [CW-1:0] clk_cnt;
    reg [2:0]    bit_idx;
    reg [7:0]    shifter;

    wire bit_done = (clk_cnt == FULL_BIT[CW-1:0]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state   <= IDLE;
            tx      <= 1'b1;            // the line idles HIGH
            busy    <= 1'b0;
            tx_done <= 1'b0;
            clk_cnt <= {CW{1'b0}};
            bit_idx <= 3'd0;
            shifter <= 8'd0;
        end else begin
            tx_done <= 1'b0;            // default: a one-cycle pulse

            case (state)
                IDLE: begin
                    tx      <= 1'b1;
                    clk_cnt <= {CW{1'b0}};
                    bit_idx <= 3'd0;
                    if (tx_start) begin
                        shifter <= tx_data;
                        busy    <= 1'b1;
                        state   <= START;
                    end else begin
                        busy <= 1'b0;
                    end
                end

                START: begin
                    tx <= 1'b0;                       // start bit
                    if (bit_done) begin
                        clk_cnt <= {CW{1'b0}};
                        state   <= DATA;
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                DATA: begin
                    tx <= shifter[0];                 // LSB first
                    if (bit_done) begin
                        clk_cnt <= {CW{1'b0}};
                        shifter <= {1'b0, shifter[7:1]};
                        if (bit_idx == 3'd7) begin
                            bit_idx <= 3'd0;
                            state   <= STOP;
                        end else begin
                            bit_idx <= bit_idx + 1'b1;
                        end
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                STOP: begin
                    tx <= 1'b1;                       // stop bit
                    if (bit_done) begin
                        clk_cnt <= {CW{1'b0}};
                        tx_done <= 1'b1;
                        busy    <= 1'b0;
                        state   <= IDLE;
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                default: state <= IDLE;               // SAFE FSM
            endcase
        end
    end

endmodule

`default_nettype wire
