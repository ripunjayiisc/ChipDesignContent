// BAD for synthesis - a floating-point type.
// `real` is an IEEE-754 double inside the simulator. There is no such thing
// in a standard-cell library. Floating point in hardware means instantiating
// an FPU, which is a large block you choose deliberately.
module s09_real (input [7:0] d, output reg [7:0] y);
    real scale;
    always @* begin
        scale = 1.5;
        y = d * scale;
    end
endmodule
