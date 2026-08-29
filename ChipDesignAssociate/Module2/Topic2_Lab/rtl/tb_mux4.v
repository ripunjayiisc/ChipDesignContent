// Exhaustive: 4 data bits x 2 select bits = 64 input combinations, all of them.
`timescale 1ns/1ps
module tb_mux4;
    reg [3:0] d; reg [1:0] sel;
    wire y1, y2, y3;
    integer i, errors = 0;
    reg exp;

    mux4_assign u1 (.d(d), .sel(sel), .y(y1));
    mux4_case   u2 (.d(d), .sel(sel), .y(y2));
    mux4_if     u3 (.d(d), .sel(sel), .y(y3));

    initial begin
        $display("");
        $display("  === 4:1 mux, three coding styles, all 64 input patterns ===");
        for (i = 0; i < 64; i = i + 1) begin
            {sel, d} = i[5:0];
            #1;
            exp = d[sel];
            if (y1 !== exp || y2 !== exp || y3 !== exp) begin
                errors = errors + 1;
                $display("  MISMATCH sel=%b d=%b -> %b %b %b (exp %b)",
                         sel, d, y1, y2, y3, exp);
            end
        end
        $display("  patterns checked : 64");
        $display("  mismatches       : %0d", errors);
        if (errors == 0)
            $display("  PASS - all three styles compute the same function");
        $display("");
        $finish;
    end
endmodule
