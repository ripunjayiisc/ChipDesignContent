// ---------------------------------------------------------------------------
// hz_static1_fix.v   F = A B' + B C + A C
//
// The same function, with the consensus term A C added. When A = 1 and C = 1
// that term is 1 regardless of B, so it holds F up right through the B
// transition and there is no handover to lose.
//
// A C is logically REDUNDANT: the truth table is identical. That is precisely
// why every logic minimiser deletes it, and why a hazard-free circuit costs
// area that a minimiser will try to give back to you.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_static1_fix (input a, input b, input c, output f);

    wire nb, t1, t2, t3;

    not #(4) g_inv (nb, b);
    and #(2) g_t1  (t1, a, nb);    // A B'
    and #(2) g_t2  (t2, b, c);     // B C
    and #(2) g_t3  (t3, a, c);     // A C   <-- the redundant term
    or  #(2) g_or  (f,  t1, t2, t3);

endmodule
