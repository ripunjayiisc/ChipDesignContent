// EVERY rule broken at once, on purpose, so the linter has something to find.
// Do not copy any line of this file.
module s12_bad_style (input clk, input a, input b, input [1:0] sel,
                      output reg y, output reg q, output reg z);

    // L001 + L003 : blocking assignment in a clocked block, mixed with <=
    always @(posedge clk) begin
        q = a & b;          // L001 - should be <=
        z <= a | b;         // L003 - mixed with the line above
    end

    // L004 + L006 : explicit sensitivity list, and a case with no default
    always @(sel or a) begin
        case (sel)
            2'b00: y = a;
            2'b01: y = b;
        endcase                 // L006 - no default, so y latches
    end

endmodule
