// LEGAL but expensive - division by a variable.
// This synthesises. It builds a full combinational divider, which is one of
// the largest and slowest things you can accidentally ask for. Dividing by a
// CONSTANT POWER OF TWO is free (it is a wire shift); dividing by a variable
// is not. Count the cells and see.
module s10_divide (input [7:0] a, input [7:0] b, output [7:0] q);
    assign q = a / b;
endmodule
