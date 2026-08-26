// ---------------------------------------------------------------------------
// alu.v  -  parameterised arithmetic logic unit  (Lab L1)
//
// Eight operations selected by a 3-bit opcode, with the four standard flags.
//
//   Z  result is zero          - a reduction NOR of every result bit
//   N  result is negative      - the MSB, in two's complement
//   C  carry / borrow out      - UNSIGNED overflow
//   V  signed overflow         - Cn XOR Cn-1, and NOT the same as C
//
// The width-(W+1) sum is the standard trick for capturing the carry out.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module alu #(
    parameter integer W = 8
)(
    input  wire [W-1:0] a,
    input  wire [W-1:0] b,
    input  wire [2:0]   op,
    output reg  [W-1:0] result,
    output wire         zero,
    output wire         negative,
    output reg          carry,
    output reg          overflow
);

    localparam [2:0] OP_ADD = 3'd0,
                     OP_SUB = 3'd1,
                     OP_AND = 3'd2,
                     OP_OR  = 3'd3,
                     OP_XOR = 3'd4,
                     OP_SLL = 3'd5,
                     OP_SRL = 3'd6,
                     OP_SLT = 3'd7;    // set-on-less-than, SIGNED

    wire [W:0] sum_ext  = {1'b0, a} + {1'b0, b};
    wire [W:0] diff_ext = {1'b0, a} - {1'b0, b};

    always @(*) begin
        result   = {W{1'b0}};          // defaults - no latch
        carry    = 1'b0;
        overflow = 1'b0;
        case (op)
            OP_ADD: begin
                result   = sum_ext[W-1:0];
                carry    = sum_ext[W];
                // signed overflow: operands agree in sign, result disagrees
                overflow = (a[W-1] == b[W-1]) && (result[W-1] != a[W-1]);
            end
            OP_SUB: begin
                result   = diff_ext[W-1:0];
                carry    = diff_ext[W];        // borrow
                overflow = (a[W-1] != b[W-1]) && (result[W-1] != a[W-1]);
            end
            OP_AND: result = a & b;
            OP_OR : result = a | b;
            OP_XOR: result = a ^ b;
            OP_SLL: result = a << b[$clog2(W)-1:0];
            OP_SRL: result = a >> b[$clog2(W)-1:0];
            OP_SLT: result = ($signed(a) < $signed(b)) ? {{(W-1){1'b0}}, 1'b1}
                                                      : {W{1'b0}};
            default: begin
                result   = {W{1'b0}};
                carry    = 1'b0;
                overflow = 1'b0;
            end
        endcase
    end

    assign zero     = ~|result;        // reduction NOR
    assign negative = result[W-1];

endmodule

`default_nettype wire
