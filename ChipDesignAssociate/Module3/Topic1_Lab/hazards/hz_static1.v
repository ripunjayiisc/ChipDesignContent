// ---------------------------------------------------------------------------
// hz_static1.v   F = A B' + B C     -  the textbook static-1 hazard
//
// Built from gate primitives with explicit delays, because a hazard is a
// TIMING phenomenon: it does not exist in the truth table and it does not
// exist in a zero-delay simulation. The delays below are what make it visible.
//
// The trap is the transition B: 1 -> 0 while A = 1 and C = 1.
//   before:  B=1, so the term (B C) is holding F up.        F = 1
//   after :  B=0, so the term (A B') is holding F up.       F = 1
// The handover is a race. (B C) switches off as soon as B falls, but (A B')
// cannot switch on until B has been through the inverter. For the few
// nanoseconds in between, BOTH terms are off and F dips to 0.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_static1 (input a, input b, input c, output f);

    wire nb, t1, t2;

    not #(4) g_inv (nb, b);        // the slow path - this is what causes it
    and #(2) g_t1  (t1, a, nb);    // A B'
    and #(2) g_t2  (t2, b, c);     // B C
    or  #(2) g_or  (f,  t1, t2);

endmodule
