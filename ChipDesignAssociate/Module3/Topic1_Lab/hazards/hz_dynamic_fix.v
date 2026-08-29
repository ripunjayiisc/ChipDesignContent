// ---------------------------------------------------------------------------
// hz_dynamic_fix.v   the same circuit with the ROOT CAUSE removed
//
// Identical to hz_dynamic.v except for one added gate: the consensus term A C
// in the sub-expression s. That is the same one-line fix as hz_static1_fix.v.
//
// This removes the DYNAMIC hazard. It does NOT remove the four static ones,
// and that is the point of this file: 5 glitches becomes 4, not 0.
//
// The four survivors have a different cause. With A=0,C=1 the fixed
// sub-expression collapses to s = B, and with A=1,C=0 it collapses to s = B'.
// Either way s is a DELAYED copy of B, so f = s XOR B computes B XOR B-delayed
// and spikes on every B edge. That is reconvergent fanout with unequal path
// delays. No redundant product term inside s can cure it, because the cover is
// not what is wrong - the structure is.
//
// The lesson: "add the consensus term" is the cure for a two-level logic
// hazard, and only for that. See hz_flat_fix.v for the structural repair.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_dynamic_fix (input a, input b, input c, output f);

    wire nb, t1, t2, t3, s;

    not #(6) g_inv (nb, b);
    and #(2) g_t1  (t1, a, nb);    // A B'
    and #(2) g_t2  (t2, b, c);     // B C
    and #(2) g_t3  (t3, a, c);     // A C   <-- the redundant term
    or  #(2) g_or  (s,  t1, t2, t3);
    xor #(2) g_x   (f,  s, b);

endmodule
