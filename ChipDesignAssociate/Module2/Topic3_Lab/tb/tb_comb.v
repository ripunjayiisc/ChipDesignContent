// ---------------------------------------------------------------------------
// tb_comb.v  -  exhaustive check of the half adder, the 4:1 MUX and the
//               2:4 decoder.
//
//   iverilog -g2012 -o comb.out rtl/half_adder.v rtl/mux4.v \
//            rtl/decoder2to4.v tb/tb_comb.v
//   vvp comb.out
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_comb;

    reg  [3:0] d;
    reg  [1:0] sel;
    reg  [1:0] addr;
    reg        en;
    reg        ha_a, ha_b;
    wire       ha_s, ha_c;
    wire       y;
    wire [3:0] dec;
    integer    i, j;
    integer    errors = 0;

    half_adder   u_ha  (.a(ha_a), .b(ha_b), .sum(ha_s), .cout(ha_c));
    mux4         u_mux (.d(d), .sel(sel), .y(y));
    decoder2to4  u_dec (.a(addr), .en(en), .d(dec));

    initial begin
        $dumpfile("comb.vcd");
        $dumpvars(0, tb_comb);

        // ---- half adder: all 4 rows ----
        for (i = 0; i < 4; i = i + 1) begin
            {ha_a, ha_b} = i[1:0]; #5;
            if ({ha_c, ha_s} !== (ha_a + ha_b)) begin
                $display("FAIL half_adder a=%b b=%b", ha_a, ha_b);
                errors = errors + 1;
            end
        end

        // ---- 4:1 MUX: every data pattern x every select ----
        for (i = 0; i < 16; i = i + 1) begin
            d = i[3:0];
            for (j = 0; j < 4; j = j + 1) begin
                sel = j[1:0]; #5;
                if (y !== d[sel]) begin
                    $display("FAIL mux4 d=%b sel=%b y=%b", d, sel, y);
                    errors = errors + 1;
                end
            end
        end

        // ---- 2:4 decoder: enabled and disabled ----
        en = 1'b1;
        for (i = 0; i < 4; i = i + 1) begin
            addr = i[1:0]; #5;
            if (dec !== (4'b0001 << addr)) begin
                $display("FAIL decoder addr=%b dec=%b", addr, dec);
                errors = errors + 1;
            end
        end
        en = 1'b0; addr = 2'b10; #5;
        if (dec !== 4'b0000) begin
            $display("FAIL decoder should be all-zero when disabled");
            errors = errors + 1;
        end

        if (errors == 0) $display("PASS - half_adder, mux4 and decoder2to4 all correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
