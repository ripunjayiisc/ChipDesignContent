// BAD for ASIC synthesis - an initial block setting state at time zero.
// A simulator can set a variable at time zero. Silicon powers up in whatever
// state the flip-flops happen to settle into, which is why real designs have
// a reset. (FPGA tools DO honour this, because the bitstream initialises the
// flops - which is exactly why code that works on an FPGA can fail on an ASIC.)
module s06_initial (input clk, output reg [3:0] count);
    initial count = 4'd0;
    always @(posedge clk) count <= count + 1'b1;
endmodule
