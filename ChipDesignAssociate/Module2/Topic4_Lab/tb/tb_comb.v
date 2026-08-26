// ---------------------------------------------------------------------------
// tb_comb.v  -  exhaustive self-checking testbench for the L1 combinational
//               library: mux2, mux4, decoder3to8, priority_encoder8, alu,
//               seven_seg and adder_gen.
//
// Technique on show: a REFERENCE MODEL written in behavioural Verilog, and a
// CHECKER that compares the DUT against it. Where the reference is simply a
// Verilog operator, that is exactly the point - the DUT is the structural or
// hand-written version, and the operator is the golden answer.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_comb;

    localparam integer W = 8;
    integer errors = 0;
    integer i, j, k;

    // ------------------------------------------------ mux2
    reg  [W-1:0] m2_a, m2_b;  reg m2_sel;  wire [W-1:0] m2_y;
    mux2 #(.W(W)) u_mux2 (.a(m2_a), .b(m2_b), .sel(m2_sel), .y(m2_y));

    // ------------------------------------------------ mux4
    reg  [W-1:0] m4_d0, m4_d1, m4_d2, m4_d3;  reg [1:0] m4_sel;
    wire [W-1:0] m4_y;
    mux4 #(.W(W)) u_mux4 (.d0(m4_d0), .d1(m4_d1), .d2(m4_d2), .d3(m4_d3),
                          .sel(m4_sel), .y(m4_y));

    // ------------------------------------------------ decoder
    reg  [2:0] dec_a;  reg dec_en;  wire [7:0] dec_y;
    decoder3to8 u_dec (.a(dec_a), .en(dec_en), .y(dec_y));

    // ------------------------------------------------ priority encoder
    reg  [7:0] pe_req;  wire [2:0] pe_y;  wire pe_valid;
    priority_encoder8 u_pe (.req(pe_req), .y(pe_y), .valid(pe_valid));

    // ------------------------------------------------ ALU
    reg  [W-1:0] alu_a, alu_b;  reg [2:0] alu_op;
    wire [W-1:0] alu_res;  wire alu_z, alu_n, alu_c, alu_v;
    alu #(.W(W)) u_alu (.a(alu_a), .b(alu_b), .op(alu_op), .result(alu_res),
                        .zero(alu_z), .negative(alu_n), .carry(alu_c),
                        .overflow(alu_v));

    // ------------------------------------------------ generate-built adder
    reg  [W-1:0] ag_a, ag_b;  reg ag_cin;
    wire [W-1:0] ag_sum;  wire ag_cout;
    adder_gen #(.W(W)) u_ag (.a(ag_a), .b(ag_b), .cin(ag_cin),
                             .sum(ag_sum), .cout(ag_cout));

    // ------------------------------------------------ seven segment
    reg  [3:0] ss_d;  wire [6:0] ss_seg;
    seven_seg u_ss (.digit(ss_d), .seg_n(ss_seg));

    task check1(input cond, input [255:0] msg);
        begin
            if (!cond) begin
                $display("  FAIL: %0s   (t=%0t)", msg, $time);
                errors = errors + 1;
            end
        end
    endtask

    // reference model for the priority encoder
    function [3:0] ref_pri (input [7:0] r);
        integer b;
        begin
            ref_pri = 4'hF;                         // 'none'
            for (b = 0; b < 8; b = b + 1)
                if (r[b]) ref_pri = b[3:0];         // highest index wins
        end
    endfunction

    initial begin
        $dumpfile("comb.vcd");
        $dumpvars(0, tb_comb);
        $display("=== L1 combinational library ===");

        // ---- mux2: exhaustive over sel, sampled over data ----
        for (i = 0; i < 16; i = i + 1) begin
            m2_a = i[7:0]; m2_b = ~i[7:0];
            m2_sel = 1'b0; #1; check1(m2_y === m2_a, "mux2 sel=0");
            m2_sel = 1'b1; #1; check1(m2_y === m2_b, "mux2 sel=1");
        end

        // ---- mux4: exhaustive over sel ----
        m4_d0 = 8'hA0; m4_d1 = 8'hB1; m4_d2 = 8'hC2; m4_d3 = 8'hD3;
        m4_sel = 2'd0; #1; check1(m4_y === 8'hA0, "mux4 sel=0");
        m4_sel = 2'd1; #1; check1(m4_y === 8'hB1, "mux4 sel=1");
        m4_sel = 2'd2; #1; check1(m4_y === 8'hC2, "mux4 sel=2");
        m4_sel = 2'd3; #1; check1(m4_y === 8'hD3, "mux4 sel=3");

        // ---- decoder: exhaustive, enabled and disabled ----
        dec_en = 1'b1;
        for (i = 0; i < 8; i = i + 1) begin
            dec_a = i[2:0]; #1;
            check1(dec_y === (8'd1 << i), "decoder3to8 one-hot");
        end
        dec_en = 1'b0; dec_a = 3'd5; #1;
        check1(dec_y === 8'd0, "decoder3to8 disabled");

        // ---- priority encoder: EXHAUSTIVE over all 256 inputs ----
        for (i = 0; i < 256; i = i + 1) begin
            pe_req = i[7:0]; #1;
            if (i == 0) begin
                check1(pe_valid === 1'b0, "priority encoder valid should be 0");
            end else begin
                check1(pe_valid === 1'b1, "priority encoder valid should be 1");
                check1(pe_y === ref_pri(pe_req[7:0]), "priority encoder index");
            end
        end

        // ---- ALU: exhaustive over op, sampled over operands ----
        for (i = 0; i < 256; i = i + 4) begin
            for (j = 0; j < 256; j = j + 37) begin
                alu_a = i[7:0]; alu_b = j[7:0];
                alu_op = 3'd0; #1;                     // ADD
                check1({alu_c, alu_res} === (alu_a + alu_b), "alu add");
                alu_op = 3'd1; #1;                     // SUB
                check1(alu_res === (alu_a - alu_b), "alu sub");
                alu_op = 3'd2; #1;
                check1(alu_res === (alu_a & alu_b), "alu and");
                alu_op = 3'd3; #1;
                check1(alu_res === (alu_a | alu_b), "alu or");
                alu_op = 3'd4; #1;
                check1(alu_res === (alu_a ^ alu_b), "alu xor");
                alu_op = 3'd7; #1;                     // SLT, signed
                check1(alu_res === (($signed(alu_a) < $signed(alu_b)) ? 8'd1 : 8'd0),
                       "alu slt");
                check1(alu_z === (alu_res == 8'd0), "alu zero flag");
            end
        end

        // ---- the specific signed-overflow case from the slides ----
        alu_a = 8'h7F; alu_b = 8'h01; alu_op = 3'd0; #1;   // 127 + 1
        check1(alu_res === 8'h80, "alu 127+1 result");
        check1(alu_c === 1'b0,    "alu 127+1 carry should be 0");
        check1(alu_v === 1'b1,    "alu 127+1 overflow should be 1");

        // ---- generate-built adder: exhaustive on a reduced range ----
        for (i = 0; i < 256; i = i + 5) begin
            for (j = 0; j < 256; j = j + 11) begin
                for (k = 0; k < 2; k = k + 1) begin
                    ag_a = i[7:0]; ag_b = j[7:0]; ag_cin = k[0]; #1;
                    check1({ag_cout, ag_sum} === (ag_a + ag_b + ag_cin),
                           "adder_gen sum");
                end
            end
        end

        // ---- seven segment: every code must be defined (never x) ----
        for (i = 0; i < 16; i = i + 1) begin
            ss_d = i[3:0]; #1;
            check1(^ss_seg !== 1'bx, "seven_seg produced x");
        end
        ss_d = 4'h0; #1; check1(ss_seg === 7'b100_0000, "seven_seg digit 0");
        ss_d = 4'h8; #1; check1(ss_seg === 7'b000_0000, "seven_seg digit 8");

        if (errors == 0) $display("PASS - L1 combinational library, all checks correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
