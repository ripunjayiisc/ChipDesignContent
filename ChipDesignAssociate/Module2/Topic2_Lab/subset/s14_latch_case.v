// A latch inferred from a case with no default - the same bug as s03, but
// wearing a different hat. Kept separate so the Yosys cross-check has two
// independent latch cases to confirm.
module s14_latch_case (input [1:0] sel, input [3:0] d, output reg y);
    always @* begin
        case (sel)
            2'b00: y = d[0];
            2'b01: y = d[1];
            2'b10: y = d[2];
        endcase
    end
endmodule
