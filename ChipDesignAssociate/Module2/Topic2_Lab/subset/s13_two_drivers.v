// L007 : one signal driven from two always blocks.
// In simulation the block that happens to run last wins. In synthesis this is
// a multiple-driver error or a short circuit.
module s13_two_drivers (input clk, input a, input b, output reg y);
    always @(posedge clk) y <= a;
    always @(posedge clk) y <= b;      // <-- second driver for y
endmodule
