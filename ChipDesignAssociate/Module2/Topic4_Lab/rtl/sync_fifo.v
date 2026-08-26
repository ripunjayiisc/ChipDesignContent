// ---------------------------------------------------------------------------
// sync_fifo.v  -  synchronous FIFO with an extra pointer bit  (Lab L4)
//
// DEPTH must be a power of two.
//
// The classic FIFO bug is that with plain pointers, FULL and EMPTY look
// identical (wr_ptr == rd_ptr in both cases). The fix used here is one EXTRA
// bit on each pointer:
//
//   empty : the pointers match completely
//   full  : the address bits match but the extra bits DIFFER
//
// That costs one flip-flop per pointer and lets you use all DEPTH entries.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module sync_fifo #(
    parameter integer W     = 8,
    parameter integer DEPTH = 8
)(
    input  wire         clk,
    input  wire         rst_n,
    input  wire         wr_en,
    input  wire [W-1:0] wr_data,
    input  wire         rd_en,
    output wire [W-1:0] rd_data,
    output wire         full,
    output wire         empty,
    output wire [$clog2(DEPTH):0] count
);

    localparam integer AW = $clog2(DEPTH);

    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;        // one EXTRA bit each

    wire do_wr = wr_en & ~full;
    wire do_rd = rd_en & ~empty;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin
            mem[wr_ptr[AW-1:0]] <= wr_data;
            wr_ptr <= wr_ptr + 1'b1;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (do_rd) rd_ptr <= rd_ptr + 1'b1;
    end

    // combinational (first-word-fall-through) read
    assign rd_data = mem[rd_ptr[AW-1:0]];

    assign empty = (wr_ptr == rd_ptr);
    assign full  = (wr_ptr[AW] != rd_ptr[AW]) &&
                   (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count = wr_ptr - rd_ptr;

endmodule

`default_nettype wire
