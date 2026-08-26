// ---------------------------------------------------------------------------
// fifo_bugs.v  -  FOUR BROKEN COPIES of fifo.v, for the Lab V5 debug clinic.
//
// Each variant has exactly ONE realistic bug of the kind that really happens.
// They are all syntactically legal, they all lint clean, they all synthesise,
// and every one of them PASSES a naive "write three words, read three words"
// testbench. That is the point: a testbench is only as good as the properties
// it checks.
//
// DO NOT read the bug descriptions below before attempting the clinic. Run
// your testbench against all four, then come back and mark yourself.
//
//   fifo_b1  full is one entry late   -> accepts a DEPTH+1'th write, and the
//                                        oldest word is silently overwritten
//   fifo_b2  read is not guarded      -> rd_ptr advances even when empty, so
//                                        the FIFO "reads" words that never
//                                        existed and count underflows
//   fifo_b3  count is computed from a separate register that is not updated
//                                        on a simultaneous read+write, so
//                                        count drifts away from reality
//   fifo_b4  the write address drops the wrap bit incorrectly, so the very
//                                        first word after a wrap goes to the
//                                        wrong location and comes back wrong
//   fifo_b5  a write is silently dropped when wr_en and rd_en are asserted
//                                        together while the FIFO is EMPTY -
//                                        a combination no directed test in
//                                        this lab ever produces
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

// ------------------------------------------------------- BUG 1: late full
module fifo_b1 #(parameter integer W = 8, parameter integer DEPTH = 8)(
    input wire clk, rst_n, wr_en, rd_en, input wire [W-1:0] wr_data,
    output wire [W-1:0] rd_data, output wire full, empty,
    output wire [$clog2(DEPTH):0] count);
    localparam integer AW = $clog2(DEPTH);
    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;
    wire do_wr = wr_en & ~full;
    wire do_rd = rd_en & ~empty;
    always @(posedge clk or negedge rst_n)
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin mem[wr_ptr[AW-1:0]] <= wr_data; wr_ptr <= wr_ptr + 1'b1; end
    always @(posedge clk or negedge rst_n)
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (do_rd) rd_ptr <= rd_ptr + 1'b1;
    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign count   = wr_ptr - rd_ptr;
    assign full    = (count > DEPTH[AW:0]);        // BUG: should be ==, not >
endmodule

// ------------------------------------------------------- BUG 2: unguarded read
module fifo_b2 #(parameter integer W = 8, parameter integer DEPTH = 8)(
    input wire clk, rst_n, wr_en, rd_en, input wire [W-1:0] wr_data,
    output wire [W-1:0] rd_data, output wire full, empty,
    output wire [$clog2(DEPTH):0] count);
    localparam integer AW = $clog2(DEPTH);
    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;
    wire do_wr = wr_en & ~full;
    always @(posedge clk or negedge rst_n)
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin mem[wr_ptr[AW-1:0]] <= wr_data; wr_ptr <= wr_ptr + 1'b1; end
    always @(posedge clk or negedge rst_n)
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (rd_en) rd_ptr <= rd_ptr + 1'b1;   // BUG: no & ~empty
    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign full    = (wr_ptr[AW] != rd_ptr[AW]) && (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count   = wr_ptr - rd_ptr;
endmodule

// ------------------------------------------------------- BUG 3: drifting count
module fifo_b3 #(parameter integer W = 8, parameter integer DEPTH = 8)(
    input wire clk, rst_n, wr_en, rd_en, input wire [W-1:0] wr_data,
    output wire [W-1:0] rd_data, output wire full, empty,
    output wire [$clog2(DEPTH):0] count);
    localparam integer AW = $clog2(DEPTH);
    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr, cnt;
    wire do_wr = wr_en & ~full;
    wire do_rd = rd_en & ~empty;
    always @(posedge clk or negedge rst_n)
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin mem[wr_ptr[AW-1:0]] <= wr_data; wr_ptr <= wr_ptr + 1'b1; end
    always @(posedge clk or negedge rst_n)
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (do_rd) rd_ptr <= rd_ptr + 1'b1;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)          cnt <= {(AW+1){1'b0}};
        else if (do_wr)      cnt <= cnt + 1'b1;    // BUG: a simultaneous read+write
        else if (do_rd)      cnt <= cnt - 1'b1;    //      only counts the write
    end
    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign full    = (wr_ptr[AW] != rd_ptr[AW]) && (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count   = cnt;
endmodule

// ------------------------------------------------------- BUG 4: wrong wrap address
module fifo_b4 #(parameter integer W = 8, parameter integer DEPTH = 8)(
    input wire clk, rst_n, wr_en, rd_en, input wire [W-1:0] wr_data,
    output wire [W-1:0] rd_data, output wire full, empty,
    output wire [$clog2(DEPTH):0] count);
    localparam integer AW = $clog2(DEPTH);
    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;
    wire do_wr = wr_en & ~full;
    wire do_rd = rd_en & ~empty;
    // BUG: the write address is clamped instead of wrapped, so once wr_ptr
    // passes DEPTH-1 every further write lands on the last location.
    wire [AW-1:0] waddr = (wr_ptr > DEPTH[AW:0]-1) ? (DEPTH[AW-1:0]-1'b1) : wr_ptr[AW-1:0];
    always @(posedge clk or negedge rst_n)
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin mem[waddr] <= wr_data; wr_ptr <= wr_ptr + 1'b1; end
    always @(posedge clk or negedge rst_n)
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (do_rd) rd_ptr <= rd_ptr + 1'b1;
    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign full    = (wr_ptr[AW] != rd_ptr[AW]) && (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count   = wr_ptr - rd_ptr;
endmodule

// ---------------------------------------- BUG 5: only on a rare input combination
// This one is the reason constrained-random stimulus exists. It is invisible
// to every directed test in tb_v2_selfcheck.v, because that test never
// asserts wr_en and rd_en together while the FIFO is EMPTY. When it happens,
// the write is thrown away and the word is lost for ever.
module fifo_b5 #(parameter integer W = 8, parameter integer DEPTH = 8)(
    input wire clk, rst_n, wr_en, rd_en, input wire [W-1:0] wr_data,
    output wire [W-1:0] rd_data, output wire full, empty,
    output wire [$clog2(DEPTH):0] count);
    localparam integer AW = $clog2(DEPTH);
    reg [W-1:0] mem [0:DEPTH-1];
    reg [AW:0]  wr_ptr, rd_ptr;
    wire do_wr = wr_en & ~full & ~(rd_en & empty);   // BUG: the & ~(rd_en & empty)
    wire do_rd = rd_en & ~empty;
    always @(posedge clk or negedge rst_n)
        if (!rst_n) wr_ptr <= {(AW+1){1'b0}};
        else if (do_wr) begin mem[wr_ptr[AW-1:0]] <= wr_data; wr_ptr <= wr_ptr + 1'b1; end
    always @(posedge clk or negedge rst_n)
        if (!rst_n) rd_ptr <= {(AW+1){1'b0}};
        else if (do_rd) rd_ptr <= rd_ptr + 1'b1;
    assign rd_data = mem[rd_ptr[AW-1:0]];
    assign empty   = (wr_ptr == rd_ptr);
    assign full    = (wr_ptr[AW] != rd_ptr[AW]) && (wr_ptr[AW-1:0] == rd_ptr[AW-1:0]);
    assign count   = wr_ptr - rd_ptr;
endmodule

`default_nettype wire
