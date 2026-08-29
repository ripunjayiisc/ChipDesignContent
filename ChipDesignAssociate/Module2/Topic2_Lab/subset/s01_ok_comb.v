// GOOD - a combinational block written the way RTL methodology asks for.
// @* builds the sensitivity list for you; every branch assigns y; blocking
// assignments (=) are correct inside a combinational block.
module s01_ok_comb (input [1:0] sel, input [3:0] d, output reg y);
    always @* begin
        case (sel)
            2'b00: y = d[0];
            2'b01: y = d[1];
            2'b10: y = d[2];
            default: y = d[3];
        endcase
    end
endmodule
