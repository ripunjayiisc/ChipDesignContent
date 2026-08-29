// ---------------------------------------------------------------------------
// hz_none.v   F = A B + A C   -  a control, with no static-1 hazard anywhere
//
// Included so that a clean run of the detector proves the detector is capable
// of saying "no glitch". A test that only ever reports failures is not a test.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_none (input a, input b, input c, output f);

    wire t1, t2;

    and #(2) g_t1 (t1, a, b);
    and #(2) g_t2 (t2, a, c);
    or  #(2) g_or (f,  t1, t2);

endmodule
