// ---------------------------------------------------------------------------
// uart_rx.v  -  UART receiver, 8N1  (Lab L5)
//
// The one trick that makes a receiver work: sample each bit in its MIDDLE, not
// at its edge. After detecting the falling start bit, wait HALF a bit time,
// check the line is still low (rejecting a glitch), then sample every full bit
// time from there.
//
// rx_valid pulses for one cycle when rx_data is ready.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module uart_rx #(
    parameter integer CLKS_PER_BIT = 434
)(
    input  wire       clk,
    input  wire       rst_n,
    input  wire       rx,
    output reg  [7:0] rx_data,
    output reg        rx_valid,
    output reg        frame_error
);

    localparam [1:0] IDLE = 2'd0, START = 2'd1, DATA = 2'd2, STOP = 2'd3;

    // The counter must hold 0 .. CLKS_PER_BIT-1, so CW = $clog2(CLKS_PER_BIT).
    //
    // WIDTH TRAP: do NOT write CLKS_PER_BIT[CW-1:0]. CLKS_PER_BIT itself does
    // not fit in CW bits - for CLKS_PER_BIT = 16, CW = 4 and 16 truncates to
    // ZERO. Compute the limits as INTEGERS first, then size them.
    localparam integer CW = (CLKS_PER_BIT <= 2) ? 1 : $clog2(CLKS_PER_BIT);

    // the incoming line is asynchronous - synchronise it first
    wire rx_sync;
    synchroniser #(.STAGES(2)) u_sync (
        .clk(clk), .rst_n(rst_n), .async_in(rx), .sync_out(rx_sync)
    );

    reg [1:0]    state;
    reg [CW-1:0] clk_cnt;
    reg [2:0]    bit_idx;
    reg [7:0]    shifter;

    // Declared as INTEGERS, then sliced where they are used. Both values are
    // guaranteed to fit in CW bits by construction, so the slice loses nothing
    // - and this form is clean under Verilator -Wall, which the earlier
    // CLKS_PER_BIT[CW-1:0] was not.
    localparam integer FULL_BIT = CLKS_PER_BIT - 1;
    localparam integer HALF_BIT = (CLKS_PER_BIT / 2) - 1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state       <= IDLE;
            clk_cnt     <= {CW{1'b0}};
            bit_idx     <= 3'd0;
            shifter     <= 8'd0;
            rx_data     <= 8'd0;
            rx_valid    <= 1'b0;
            frame_error <= 1'b0;
        end else begin
            rx_valid    <= 1'b0;        // defaults: one-cycle pulses
            frame_error <= 1'b0;

            case (state)
                IDLE: begin
                    clk_cnt <= {CW{1'b0}};
                    bit_idx <= 3'd0;
                    if (!rx_sync) state <= START;      // falling edge seen
                end

                START: begin
                    if (clk_cnt == HALF_BIT[CW-1:0]) begin
                        if (!rx_sync) begin
                            clk_cnt <= {CW{1'b0}};     // genuine start bit
                            state   <= DATA;
                        end else begin
                            state <= IDLE;             // it was a glitch
                        end
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                DATA: begin
                    if (clk_cnt == FULL_BIT[CW-1:0]) begin
                        clk_cnt <= {CW{1'b0}};
                        shifter <= {rx_sync, shifter[7:1]};   // LSB arrives first
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
                    if (clk_cnt == FULL_BIT[CW-1:0]) begin
                        clk_cnt  <= {CW{1'b0}};
                        rx_data  <= shifter;
                        rx_valid <= 1'b1;
                        // a real stop bit is HIGH; anything else is a framing error
                        frame_error <= ~rx_sync;
                        state    <= IDLE;
                    end else begin
                        clk_cnt <= clk_cnt + 1'b1;
                    end
                end

                default: state <= IDLE;
            endcase
        end
    end

endmodule

`default_nettype wire
