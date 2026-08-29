// ---------------------------------------------------------------------------
// LEVEL 4 of 4 : SWITCH (transistor)
//
// The lowest level Verilog can describe: individual MOS transistors, wired
// between supply rails. Each logic gate is built from a pull-up network of
// pmos transistors and a pull-down network of nmos transistors.
//
// You will never write synthesisable design work at this level - this is what
// a standard-cell library contains, written once by the foundry. It is here so
// that you have seen the bottom of the ladder and know what the gate symbols
// in level 3 actually stand for.
//
// Built from CMOS NAND and NOT, because in CMOS a NAND is cheaper than an AND
// (an AND is a NAND followed by an inverter - four transistors plus two).
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

// --- a CMOS inverter: one pmos pulling up, one nmos pulling down -----------
module inv_sw (input a, output y);
    supply1 vdd;
    supply0 gnd;
    pmos p1 (y, vdd, a);           // conducts when a = 0  -> pulls y high
    nmos n1 (y, gnd, a);           // conducts when a = 1  -> pulls y low
endmodule

// --- a CMOS 2-input NAND: pmos in PARALLEL, nmos in SERIES ----------------
module nand2_sw (input a, input b, output y);
    supply1 vdd;
    supply0 gnd;
    wire    mid;
    pmos p1 (y,   vdd, a);         // either pmos on -> y pulled high
    pmos p2 (y,   vdd, b);
    nmos n1 (y,   mid, a);         // BOTH nmos on   -> y pulled low
    nmos n2 (mid, gnd, b);
endmodule

// --- XOR from four NANDs --------------------------------------------------
module xor2_sw (input a, input b, output y);
    wire n1, n2, n3;
    nand2_sw g1 (a,  b,  n1);
    nand2_sw g2 (a,  n1, n2);
    nand2_sw g3 (n1, b,  n3);
    nand2_sw g4 (n2, n3, y);
endmodule

// --- AND = NAND then invert ----------------------------------------------
module and2_sw (input a, input b, output y);
    wire n;
    nand2_sw g1 (a, b, n);
    inv_sw   g2 (n, y);
endmodule

// --- OR = NAND of the two inverted inputs (De Morgan) --------------------
module or2_sw (input a, input b, output y);
    wire na, nb;
    inv_sw   i1 (a,  na);
    inv_sw   i2 (b,  nb);
    nand2_sw g1 (na, nb, y);
endmodule

// --- the full adder, all the way down to transistors ---------------------
module fa_switch (input a, input b, input cin, output sum, output cout);

    wire s1, ab, bc, ac, o1;

    xor2_sw x1 (a,  b,   s1);
    xor2_sw x2 (s1, cin, sum);

    and2_sw n1 (a,  b,   ab);
    and2_sw n2 (b,  cin, bc);
    and2_sw n3 (a,  cin, ac);
    or2_sw  r1 (ab, bc,  o1);
    or2_sw  r2 (o1, ac,  cout);

endmodule
