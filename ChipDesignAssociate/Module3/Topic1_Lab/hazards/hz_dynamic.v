// ---------------------------------------------------------------------------
// hz_dynamic.v   a DYNAMIC hazard, and where it comes from
//
// A dynamic hazard is an output that ought to change ONCE but changes three
// or more times. It needs three or more reconverging paths with different
// delays, so it cannot happen in a two-level circuit.
//
// This one is built the way dynamic hazards actually arise in practice: a
// sub-expression that already contains a STATIC hazard is fed into a later
// gate, where the same input reconverges by a faster route.
//
//     s = A B' + B C          <- the static-1 hazard from hz_static1.v
//     F = s XOR B             <- B arrives here directly, well before it has
//                                finished travelling through the inverter
//
// Watch what the detector reports: FIVE glitching transitions, not one. Four
// of them are the inner static hazard passing straight through the XOR, and
// the fifth is that same hazard landing on top of a real output change and
// turning it into a dynamic one. One root cause, five symptoms - which is why
// hz_dynamic_fix.v repairs the sub-expression rather than the output.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module hz_dynamic (input a, input b, input c, output f);

    wire nb, t1, t2, s;

    not #(6) g_inv (nb, b);        // the slow path
    and #(2) g_t1  (t1, a, nb);    // A B'
    and #(2) g_t2  (t2, b, c);     // B C
    or  #(2) g_or  (s,  t1, t2);   // s carries the static-1 hazard
    xor #(2) g_x   (f,  s, b);     // B reconverges here, by a fast route

endmodule
