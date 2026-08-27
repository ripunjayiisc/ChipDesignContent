// ---------------------------------------------------------------------------
// fifo.v  -  synchronous FIFO.  THE DEVICE UNDER TEST for Labs V1-V6.
//
// This is the golden, correct version. Four deliberately broken variants live
// in fifo_bugs.v; the whole point of Topic 5 is to build a testbench good
// enough to catch every one of them.
//
// Interface contract (this IS the specification - your testbench checks it):
//
//   * A write is accepted on a rising clk when wr_en=1 and full=0.
//     A write attempted while full is IGNORED and must not corrupt anything.
//   * A read is accepted on a rising clk when rd_en=1 and empty=0.
//     A read attempted while empty is IGNORED.
//   * rd_data shows the OLDEST unread word at all times (first-word
//     fall-through). It is only meaningful while empty=0.
//   * count is the number of words currently stored, 0..DEPTH.
//   * empty <=> count==0.   full <=> count==DEPTH.
//   * Words come out in the order they went in. No word is lost or duplicated.
//   * Asynchronous active-low reset empties the FIFO.
//
// DEPTH must be a power of two.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module fifo #(
    parameter integer W     = 8,
    parameter integer DEPTH = 8
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    wr_en,
    input  wire [W-1:0]            wr_data,
    input  wire                    rd_en,
    output wire [W-1:0]            rd_data,
    output wire                    full,
    output wire                    empty,
    output wire [$clog2(DEPTH):0]  count
);

    localparam integer AW = $clog2(DEPTH);

    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;          // one EXTRA bit each - see the workbook

    wire do_wr = wr_en & ~full;          // guard INSIDE the FIFO, not at the caller
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

    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign full    = (wr_ptr[AW] != rd_ptr[AW]) &&
                     (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count   = wr_ptr - rd_ptr;

endmodule

`default_nettype wire
