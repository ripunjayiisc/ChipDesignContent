// GOOD - a for loop with constant bounds.
// This is not a loop in hardware. The tool UNROLLS it at compile time into
// eight parallel XOR gates. Loops with bounds the tool can compute are a
// normal and idiomatic part of synthesisable RTL.
module s07_forloop (input [7:0] d, output reg parity);
    integer i;
    always @* begin
        parity = 1'b0;
        for (i = 0; i < 8; i = i + 1)
            parity = parity ^ d[i];
    end
endmodule
