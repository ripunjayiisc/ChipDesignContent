// ---------------------------------------------------------------------------
// fa_broken.v  -  a full adder with ONE term missing from the carry.
//
// This file exists so that the equivalence check has something to fail on. A
// checker that only ever reports EQUIVALENT is not evidence of anything; you
// have to see it catch a real bug before you can trust it on a design you
// cannot check by hand.
//
// The bug: cout should be (a&b) | (b&cin) | (a&cin). The last term is missing,
// so this is wrong ONLY when a=1, cin=1, b=0 - one input pattern in eight. A
// random test could easily miss it. The solver cannot.
// ---------------------------------------------------------------------------
module fa_broken (input a, input b, input cin, output sum, output cout);

    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin);      // <-- (a & cin) omitted

endmodule
