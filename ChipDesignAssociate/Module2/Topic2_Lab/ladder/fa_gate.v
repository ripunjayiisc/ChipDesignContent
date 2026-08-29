// ---------------------------------------------------------------------------
// LEVEL 3 of 4 : GATE (structural)
//
// You name every gate and every wire between them. This is a netlist written
// by hand - exactly the form a synthesiser PRODUCES, and almost never the form
// a human should write.
//
// Note what you have given up: the tool can no longer choose a different
// Boolean form or a different gate mix, because you have already chosen.
// ---------------------------------------------------------------------------
module fa_gate (input a, input b, input cin, output sum, output cout);

    wire ab, s1, s1c, bc, ac;

    xor  x1 (s1,   a, b);          // s1  = a ^ b
    xor  x2 (sum,  s1, cin);       // sum = a ^ b ^ cin

    and  a1 (ab,   a, b);
    and  a2 (bc,   b, cin);
    and  a3 (ac,   a, cin);
    or   o1 (cout, ab, bc, ac);

endmodule
