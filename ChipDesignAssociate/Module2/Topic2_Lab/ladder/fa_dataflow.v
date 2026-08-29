// ---------------------------------------------------------------------------
// LEVEL 2 of 4 : DATAFLOW
//
// You describe the Boolean EXPRESSION for each output. Still no structure -
// no named gates, no instances - but you have committed to a particular
// Boolean form rather than leaving it to the tool.
//
// Continuous assignments (assign) model combinational logic: the left-hand
// side re-evaluates whenever anything on the right changes.
// ---------------------------------------------------------------------------
module fa_dataflow (input a, input b, input cin, output sum, output cout);

    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (a & cin);

endmodule
