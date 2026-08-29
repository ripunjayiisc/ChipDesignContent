// ---------------------------------------------------------------------------
// hz_flat_fix.v   the same function as hz_dynamic.v, done properly
//
// hz_dynamic_fix.v removed the dynamic hazard but left four static ones,
// because those came from a different mechanism: with A=0,C=1 the
// sub-expression s degenerates to a DELAYED COPY of B, and f = s XOR B is
// then B XOR B-delayed, which spikes on every B edge. No redundant product
// term inside s can repair that - it is the multi-level STRUCTURE that is
// wrong, not the cover.
//
// So flatten. The function f = (A B' + B C + A C) XOR B has minterms
// {A'BC', AB'C', AB'C, ABC'}, which is
//
//     f = A B' + B C'
//
// - the same shape as the original example, with C complemented. tools/hazard.py
// reports one static-1 hazard on it and prescribes the consensus term A C'.
// Adding that gives a two-level cover with no hazard of any kind.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_flat_fix (input a, input b, input c, output f);

    wire nb, nc, t1, t2, t3;

    not #(6) g_nb (nb, b);         // still deliberately slow - it no longer matters
    not #(3) g_nc (nc, c);
    and #(2) g_t1 (t1, a, nb);     // A B'
    and #(2) g_t2 (t2, b, nc);     // B C'
    and #(2) g_t3 (t3, a, nc);     // A C'   <-- the consensus term
    or  #(2) g_or (f,  t1, t2, t3);

endmodule
