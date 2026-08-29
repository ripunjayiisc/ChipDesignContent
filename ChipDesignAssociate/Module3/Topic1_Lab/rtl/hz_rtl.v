// RTL versions of the hazard example, to find out what synthesis does with a
// deliberately redundant term.
module hz_rtl_plain (input a, input b, input c, output f);
    assign f = (a & ~b) | (b & c);              // has a static-1 hazard
endmodule

module hz_rtl_fixed (input a, input b, input c, output f);
    assign f = (a & ~b) | (b & c) | (a & c);    // + the consensus term
endmodule
