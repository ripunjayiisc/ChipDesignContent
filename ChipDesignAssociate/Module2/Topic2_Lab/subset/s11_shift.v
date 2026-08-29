// GOOD - the cheap version of the same idea.
// Dividing by a constant power of two costs nothing at all: the tool simply
// renames the wires. Compare the cell count with s10_divide.
module s11_shift (input [7:0] a, output [7:0] q);
    assign q = a / 8'd4;        // == a >> 2
endmodule
