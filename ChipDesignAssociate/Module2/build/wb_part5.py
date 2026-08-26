# -*- coding: utf-8 -*-
"""Workbook Part 5: practice exercises;  Part 6: solutions;  Part 7: reference."""
from wbkit import *
from wb_part1 import B, N, I, M

# ---------------------------------------------------------------------------
# Every exercise is (id, section, question-lines, solution-lines).
# Question and solution live together so they can never drift apart.
# ---------------------------------------------------------------------------
EX = [
    # ---------------- Section A : Boolean algebra and gates ----------------
    ("E1", "A", ["Convert to binary, hex and BCD:  (a) 45   (b) 200   (c) 255."],
     ["(a) 45  = 0010 1101 = 0x2D ; BCD 0100 0101",
      "(b) 200 = 1100 1000 = 0xC8 ; BCD 0010 0000 0000",
      "(c) 255 = 1111 1111 = 0xFF ; BCD 0010 0101 0101"]),

    ("E2", "A", ["Write −37 and −1 in 8-bit two's complement, and state the range an 8-bit "
                 "two's-complement number can represent."],
     ["+37 = 0010 0101 ; invert -> 1101 1010 ; +1 -> 1101 1011 = -37",
      "+1  = 0000 0001 ; invert -> 1111 1110 ; +1 -> 1111 1111 = -1",
      "Range: -128 ... +127  (that is -2^7 ... +2^7 - 1).  Note the asymmetry:",
      "there is one more negative value than positive, because 0 uses a positive code."]),

    ("E3", "A", ["Add 0111 1111 and 0000 0001 as 8-bit two's-complement numbers. State the "
                 "values of C and V and explain the difference."],
     ["0111 1111 (+127) + 0000 0001 (+1) = 1000 0000, which reads as -128.",
      "Carry out of the MSB = 0, so C = 0.",
      "Carry INTO the sign bit = 1, carry OUT of it = 0, so V = Cn XOR Cn-1 = 1.",
      "C flags UNSIGNED overflow; V flags SIGNED overflow. Here the unsigned",
      "interpretation (127 + 1 = 128) is perfectly correct, so C is 0; the signed",
      "interpretation is wrong, so V is 1. They are different questions."]),

    ("E4", "A", ["Prove  A + A'·B = A + B  by perfect induction, then again algebraically."],
     ["Truth table (columns A+A'B and A+B):",
      "  A B | A'B | A+A'B | A+B",
      "  0 0 |  0  |   0   |  0",
      "  0 1 |  1  |   1   |  1",
      "  1 0 |  0  |   1   |  1",
      "  1 1 |  0  |   1   |  1     -> identical on all four rows.",
      "",
      "Algebraically:  A + A'B = (A + A')(A + B)   [distributive, second form]",
      "                        = 1 . (A + B)       [complement]",
      "                        = A + B             [identity]"]),

    ("E5", "A", ["Prove De Morgan's second theorem (A + B)' = A'·B' by perfect induction, and "
                 "state the n-variable generalisation."],
     ["  A B | A+B | (A+B)' | A' B' | A'.B'",
      "  0 0 |  0  |   1    | 1  1  |   1",
      "  0 1 |  1  |   0    | 1  0  |   0",
      "  1 0 |  1  |   0    | 0  1  |   0",
      "  1 1 |  1  |   0    | 0  0  |   0     -> columns 4 and 6 match.",
      "",
      "Generalisation:  (A + B + C + ...)' = A' . B' . C' . ...",
      "and dually       (A . B . C . ...)' = A' + B' + C' + ..."]),

    ("E6", "A", ["Simplify  F = A·B·C + A·B·C' + A·B'·C + A'·B·C  and name the resulting function."],
     ["F = AB(C + C') + AB'C + A'BC        group the first two terms",
      "  = AB + AB'C + A'BC                complement and identity",
      "  = A(B + B'C) + A'BC               factor A",
      "  = A(B + C) + A'BC                 simplification law B + B'C = B + C",
      "  = AB + AC + A'BC",
      "  = B(A + A'C) + AC                 factor B",
      "  = B(A + C) + AC                   simplification law again",
      "  = AB + BC + AC",
      "",
      "F = AB + BC + AC  -- the MAJORITY function: 1 when two or more inputs are 1.",
      "Cost: 12 literals and 4 AND gates before, 6 literals and 3 AND gates after."]),

    ("E7", "A", ["Why is NAND universal but AND is not? Give the construction for NOT, AND and OR "
                 "from NAND."],
     ["A gate is universal if every Boolean function can be built from it alone. Every",
      "function has an SOP form, which needs NOT, AND and OR - so it is enough to build",
      "those three.",
      "",
      "  NOT A   = A NAND A",
      "  A AND B = (A NAND B) NAND (A NAND B)",
      "  A OR B  = (A NAND A) NAND (B NAND B)      [De Morgan]",
      "",
      "AND is NOT universal because no combination of AND gates can ever produce a 1",
      "from all-1 inputs turned into 0 - formally, AND is monotone: raising any input",
      "from 0 to 1 can never lower the output. NOT is not monotone, so NOT cannot be",
      "built from AND alone. The same argument rules out OR."]),

    ("E8", "A", ["Minimise F(A,B,C,D) = Σm(0,2,5,7,8,10,13,15) with a K-map."],
     ["Plot the 1s. Two groups of four cover everything:",
      "  * m5, m7, m13, m15  -> B = 1, D = 1 with A and C free   ->  B.D",
      "  * m0, m2, m8, m10   -> B = 0, D = 0 with A and C free   ->  B'.D'",
      "",
      "F = B.D + B'.D'  =  (B XOR D)'  =  B XNOR D",
      "",
      "Two literals. The function is simply 'B equals D' - a 1-bit comparator."]),

    ("E9", "A", ["Minimise F(A,B,C,D) = Σm(1,3,7,11,15) + d(0,2,5) and state which prime "
                 "implicants are essential."],
     ["Ones: 1,3,7,11,15.  Don't-cares: 0,2,5.",
      "",
      "Group 1: m3,m7,m11,m15 -> C.D  (C=1, D=1, A and B free).  Covers 3,7,11,15.",
      "Group 2: m0,m1,m2,m3 (uses X at 0 and 2) -> A'.B'  Covers 1 and 3.",
      "",
      "F = C.D + A'.B'",
      "",
      "Essential prime implicants: BOTH.",
      "  * m11 and m15 are covered only by C.D, so C.D is essential.",
      "  * m1 is covered only by A'B' (m1 is not in C.D since C=0 there), so A'B' is",
      "    essential too.",
      "The don't-cares were used to enlarge A'B' from a pair to a group of four; they",
      "were never covered for their own sake."]),

    ("E10", "A", ["A function has V_OL = 0.4 V, V_IL = 0.8 V, V_IH = 2.0 V, V_OH = 2.4 V. "
                  "Compute both noise margins and say which is the weaker."],
     ["NM_L = V_IL - V_OL = 0.8 - 0.4 = 0.4 V",
      "NM_H = V_OH - V_IH = 2.4 - 2.0 = 0.4 V",
      "",
      "They are equal here, so neither is weaker - the family is balanced. In a real",
      "library they are rarely equal, and the SMALLER one determines how much noise the",
      "signal can actually tolerate."]),

    ("E11", "A", ["Write the canonical SOP and POS for the 3-input function that is 1 exactly "
                  "when an odd number of inputs is 1."],
     ["This is 3-input XOR (odd parity). Y = 1 for ABC = 001, 010, 100, 111.",
      "",
      "SOP: Y = Sm(1,2,4,7) = A'B'C + A'BC' + AB'C' + ABC",
      "POS: Y = PM(0,3,5,6) = (A+B+C)(A+B'+C')(A'+B+C')(A'+B'+C)",
      "",
      "Minimal form: Y = A XOR B XOR C - which no K-map will find, because XOR is a",
      "checkerboard on the map and has NO adjacent pairs. This is a standing limitation",
      "of two-level minimisation."]),

    ("E12", "A", ["Explain duality, and give the dual of  A + A'·B = A + B."],
     ["Duality: swap every AND with every OR and every 0 with every 1. If the original",
      "statement is a Boolean identity, so is the result.",
      "",
      "Dual of  A + A'.B = A + B   is   A . (A' + B) = A . B",
      "",
      "Note that duality is NOT the same as complementation: it transforms one true",
      "identity into another true identity, it does not compute the inverse function."]),

    # ---------------- Section B : Combinational logic ----------------
    ("E13", "B", ["Derive the full-adder equations from its truth table and show that Cout is the "
                  "majority function."],
     ["S    = 1 on rows with an ODD number of 1s -> S = A XOR B XOR Cin",
      "Cout = 1 on rows with TWO OR MORE 1s      -> Cout = AB + A.Cin + B.Cin",
      "",
      "That last expression IS the majority function of three inputs. It can also be",
      "written Cout = A.B + Cin.(A XOR B), which shares the XOR already computed for S",
      "and therefore costs fewer gates - which is why libraries use that form."]),

    ("E14", "B", ["A 4-bit ripple-carry adder has t_carry = 90 ps and t_sum = 120 ps. Find the "
                  "worst-case delay, then repeat for 16 and 32 bits."],
     ["The critical path runs from A0/B0 through every carry to the LAST SUM:",
      "  t_adder = (n-1) . t_carry + t_sum",
      "",
      "  n =  4 :  3 x 90 + 120 =  390 ps",
      "  n = 16 : 15 x 90 + 120 = 1470 ps",
      "  n = 32 : 31 x 90 + 120 = 2910 ps",
      "",
      "Delay is linear in n, so achievable frequency is roughly inverse-linear. This is",
      "exactly the calculation that forces a move to carry-lookahead or to pipelining."]),

    ("E15", "B", ["The adder of E14 sits between two registers with t_cq = 60 ps and "
                  "t_setup = 50 ps. Find f_max for n = 4 and for n = 32."],
     ["T_clk >= t_cq + t_adder + t_setup",
      "",
      "  n =  4 : 60 +  390 + 50 =  500 ps  ->  f_max = 2.00 GHz",
      "  n = 32 : 60 + 2910 + 50 = 3020 ps  ->  f_max =  331 MHz",
      "",
      "An eightfold increase in width costs a sixfold drop in frequency."]),

    ("E16", "B", ["Define generate and propagate, and write C3 for a carry-lookahead adder."],
     ["G_i = A_i . B_i          this bit GENERATES a carry regardless of C_in",
      "P_i = A_i XOR B_i        this bit PROPAGATES an incoming carry",
      "",
      "Recursively  C_{i+1} = G_i + P_i . C_i.  Expanding:",
      "",
      "  C3 = G2 + P2.G1 + P2.P1.G0 + P2.P1.P0.C0",
      "",
      "Every carry is now two gate levels from the inputs, so delay grows as log n when",
      "lookahead blocks are cascaded - at the cost of much more area and higher fan-in."]),

    ("E17", "B", ["Implement F(A,B,C) = Σm(1,2,4,7) with (a) an 8:1 MUX and (b) a 4:1 MUX."],
     ["(a) 8:1 MUX. Use A,B,C as S2,S1,S0 and tie the data inputs to the truth-table",
      "    output column:  I0=0 I1=1 I2=1 I3=0 I4=1 I5=0 I6=0 I7=1.",
      "",
      "(b) 4:1 MUX. Use A,B as S1,S0 and read the table in PAIRS of rows:",
      "      AB=00 : C=0 -> 0, C=1 -> 1   =>  I0 = C",
      "      AB=01 : C=0 -> 1, C=1 -> 0   =>  I1 = C'",
      "      AB=10 : C=0 -> 1, C=1 -> 0   =>  I2 = C'",
      "      AB=11 : C=0 -> 0, C=1 -> 1   =>  I3 = C",
      "",
      "In general an n-variable function needs only a 2^(n-1):1 MUX. This function is",
      "3-input XOR, which is why the pattern alternates."]),

    ("E18", "B", ["Why is a plain 4:2 encoder broken, and what does the V output of a priority "
                  "encoder add?"],
     ["A plain encoder assumes EXACTLY ONE input is high. If I1 and I2 are both high it",
      "outputs the bitwise OR of their codes (01 | 10 = 11), which is the code for I3 -",
      "an input that is not even active. The answer is not just imprecise, it is wrong.",
      "",
      "A PRIORITY encoder resolves the ambiguity by a fixed rule (highest index wins).",
      "",
      "V (valid) is needed because the all-zero input and 'input 0 active' both produce",
      "the code 00. V = 0 means 'nothing is active'; V = 1 with code 00 means 'input 0'."]),

    ("E19", "B", ["Design a 1-bit equality comparator and extend it to 4 bits. How would you add "
                  "a greater-than output?"],
     ["1-bit:  e = (A XOR B)'  = A XNOR B.   XNOR IS the equality gate.",
      "4-bit:  EQ = e3 . e2 . e1 . e0        AND all four bit-equalities together.",
      "",
      "Greater-than works MSB-first: A > B if, at the highest bit where they differ, A",
      "has the 1.",
      "  GT = A3.B3' + e3.(A2.B2') + e3.e2.(A1.B1') + e3.e2.e1.(A0.B0')",
      "",
      "and LT = (GT + EQ)'. In Verilog you simply write A > B and let synthesis build",
      "this - but you must recognise the structure in the timing report."]),

    ("E20", "B", ["Name the three kinds of hazard, and remove the static-1 hazard from "
                  "F = A·B' + B·C."],
     ["Static-1 : the output should stay 1 but momentarily dips to 0.",
      "Static-0 : the output should stay 0 but momentarily spikes to 1.",
      "Dynamic  : one intended transition that bounces, e.g. 0->1->0->1.",
      "",
      "With A = C = 1 and B falling 1->0: the B.C term releases before the A.B' term",
      "arrives, so F dips. On the K-map the two groups are adjacent but do not overlap.",
      "Add the consensus term that bridges them:",
      "",
      "    F = A.B' + B.C + A.C",
      "",
      "A.C is logically redundant but holds F high through the transition. This is the",
      "one case where you deliberately do NOT minimise."]),

    ("E21", "B", ["Where is a glitch harmless and where is it fatal? Give two of each."],
     ["HARMLESS (it settles before the next clock edge):",
      "  * driving the D input of a flip-flop",
      "  * driving a purely combinational output that is itself registered downstream",
      "",
      "FATAL:",
      "  * on a clock line - the receiving flip-flops see extra edges",
      "  * on an asynchronous reset or set - the design resets spuriously",
      "  * on a memory write-enable - random corruption",
      "  * on any signal leaving the chip",
      "",
      "This is the core argument for synchronous design: it makes the whole class of",
      "harmless glitches genuinely harmless."]),

    ("E22", "B", ["Explain why a 6-input NAND is slower than a tree of 2-input NANDs, and why "
                  "adding loads slows a driver."],
     ["FAN-IN: a static CMOS NAND stacks its NMOS transistors in SERIES, one per input.",
      "Six in series means roughly six times the pull-down resistance, so the output",
      "discharges far more slowly. A balanced tree of 2-input gates has more gates but",
      "a much shorter series stack per gate.",
      "",
      "FAN-OUT: each load adds gate capacitance. Delay is roughly",
      "    t_pd = t_intrinsic + k . C_load",
      "so doubling the loads roughly doubles the load-dependent part. The fixes are",
      "buffering (repeaters) and upsizing the driver - both of which synthesis does",
      "automatically, provided the timing constraint tells it to."]),

    ("E23", "B", ["What hardware does this infer, and why is it a bug?"],
     ["    always @(*) begin",
      "        if (enable) y = d;",
      "    end",
      "",
      "It infers a transparent D LATCH. When enable is 0 the block assigns nothing to y,",
      "so Verilog says 'keep the old value' - and the only hardware that can keep an old",
      "value is a storage element.",
      "",
      "It is a bug because (a) you did not intend a storage element, (b) a latch is",
      "level-sensitive and very hard to time, and (c) static timing analysis will now",
      "report paths you never designed. Fix it with a default:",
      "",
      "    always @(*) begin",
      "        y = 1'b0;",
      "        if (enable) y = d;",
      "    end"]),

    ("E24", "B", ["Distinguish the C and V flags of an ALU and give an example where they differ."],
     ["C = carry out of the MSB. It is the correct overflow indicator for UNSIGNED",
      "    arithmetic.",
      "V = Cn XOR Cn-1. It is the correct overflow indicator for SIGNED arithmetic.",
      "",
      "Example (8-bit): 0111 1111 + 0000 0001 = 1000 0000.",
      "  Unsigned: 127 + 1 = 128, which fits in 8 bits. C = 0. Correct.",
      "  Signed:   +127 + 1 gave -128. V = 1. Wrong.",
      "",
      "Counter-example the other way: 1111 1111 + 0000 0001 = 0000 0000.",
      "  Unsigned: 255 + 1 = 256 does not fit. C = 1.",
      "  Signed:   -1 + 1 = 0, perfectly correct. V = 0."]),

    # ---------------- Section C : Sequential logic ----------------
    ("E25", "C", ["State three differences between a latch and a flip-flop, and say which you "
                  "should infer in RTL."],
     ["1. A latch is LEVEL-sensitive (transparent while its enable is asserted); a",
      "   flip-flop is EDGE-triggered (samples at one instant).",
      "2. A latch's output can change many times per clock cycle; a flip-flop's changes",
      "   at most once per edge.",
      "3. A latch is roughly half the area; a flip-flop is two latches internally.",
      "",
      "Infer FLIP-FLOPS. An unintended latch is always a bug; timing analysis of latches",
      "requires time-borrowing analysis that most flows do not do by default."]),

    ("E26", "C", ["Why is S = R = 1 forbidden on an SR latch? What happens on release?"],
     ["With both inputs asserted, both NOR outputs are forced to 0, so Q and Q' are no",
      "longer complements - the latch's defining invariant is broken.",
      "",
      "On simultaneous release both gates begin to rise together and the cross-coupled",
      "loop must settle into one of its two stable states. Which one it picks depends on",
      "picosecond-level differences in transistor strength and wire delay, so the result",
      "is genuinely unpredictable and not reproducible between chips - a RACE."]),

    ("E27", "C", ["Explain how a master-slave structure produces edge-triggering."],
     ["Two D latches in series driven by OPPOSITE clock phases.",
      "  clk = 0 : master transparent (tracks D), slave opaque (holds old Q).",
      "  clk 0->1: master freezes, capturing whatever D was; slave opens and copies it.",
      "  clk = 1 : master opaque, slave transparent but its input is now frozen.",
      "",
      "Because the two latches are NEVER transparent at the same time, data cannot race",
      "through both in one clock phase. The output therefore changes exactly once per",
      "rising edge - which is the definition of edge-triggered."]),

    ("E28", "C", ["Give the characteristic equation of each of the D, T, JK and SR flip-flops."],
     ["  D  :  Q+ = D",
      "  T  :  Q+ = T XOR Q",
      "  JK :  Q+ = J.Q' + K'.Q",
      "  SR :  Q+ = S + R'.Q       valid only while S.R = 0",
      "",
      "Useful conversions:  D = T XOR Q  (D-FF used as a T-FF)",
      "                     T = D XOR Q  (T-FF used as a D-FF)"]),

    ("E29", "C", ["Define setup and hold time. Why can slowing the clock fix one but not the other?"],
     ["t_setup: the data must be STABLE for this long BEFORE the active clock edge.",
      "t_hold : the data must REMAIN stable for this long AFTER the active clock edge.",
      "",
      "Setup is a MAX-DELAY check: T_clk >= t_cq + t_logic,max + t_setup. Lengthening",
      "T_clk directly increases the left-hand side, so slowing the clock fixes it.",
      "",
      "Hold is a MIN-DELAY check: t_cq + t_logic,min >= t_hold. T_clk does not appear",
      "at all. It is a RACE between two paths launched by the SAME edge, so it is broken",
      "at any frequency, including DC. The only fix is to ADD delay to the short path."]),

    ("E30", "C", ["Given t_cq = 60 ps, t_logic = 240 ps, t_setup = 50 ps, find T_clk(min) and f_max."],
     ["T_clk(min) = t_cq + t_logic + t_setup = 60 + 240 + 50 = 350 ps",
      "f_max      = 1 / 350 ps = 2.857 GHz  ~= 2.86 GHz",
      "",
      "If the design must run at 2.0 GHz (T = 500 ps), the setup slack is",
      "  500 - 350 = +150 ps  ->  PASS with margin."]),

    ("E31", "C", ["Repeat E30 including a clock skew of 25 ps (capture clock LATE) and 15 ps of "
                  "jitter. Then perform the hold check with t_hold = 40 ps and t_logic,min = 30 ps."],
     ["SETUP  (a late capture clock HELPS setup, so skew is subtracted):",
      "  T_req = t_cq + t_logic,max + t_setup + t_jitter - t_skew",
      "        = 60 + 240 + 50 + 15 - 25 = 340 ps   ->  f_max = 2.94 GHz",
      "",
      "HOLD   (a late capture clock HURTS hold, so skew is added to the requirement):",
      "  t_cq + t_logic,min >= t_hold + t_skew",
      "  60   + 30          >= 40     + 25",
      "  90                 >= 65     ->  hold slack = +25 ps, PASS",
      "",
      "Note the OPPOSITE SIGNS of t_skew in the two checks. Getting that wrong makes",
      "both answers wrong, and it is the single most common exam error on this topic."]),

    ("E32", "C", ["What is metastability, and why does a two-flop synchroniser work? Why can you "
                  "not simply synchronise each bit of a bus?"],
     ["Metastability: if data changes inside the setup/hold window, the flip-flop's",
      "output can hover at an invalid intermediate voltage for an unbounded time before",
      "resolving randomly to 0 or 1. It cannot be prevented, only made unlikely.",
      "",
      "A two-flop synchroniser gives the first flip-flop a full clock period to resolve",
      "before the second samples it. Because resolution time appears in an EXPONENT",
      "  MTBF = e^(t_r/tau) / (T0 . f_clk . f_data)",
      "one extra stage typically moves MTBF from seconds to millions of years.",
      "",
      "A BUS cannot be synchronised bit by bit: different bits will resolve on different",
      "cycles, so you can read a value that never existed on the source side (e.g. 0111",
      "-> 1000 read as 1111). Use a Gray-coded pointer (only one bit changes per step),",
      "a request/acknowledge handshake, or an asynchronous FIFO."]),

    ("E33", "C", ["Distinguish clock skew from jitter. Give one cause and one remedy for each."],
     ["SKEW is a FIXED difference in edge arrival time between different flip-flops.",
      "  Cause  : unequal clock-tree wire length and load.",
      "  Remedy : clock-tree synthesis (CTS) inserts buffers to balance every branch.",
      "",
      "JITTER is a RANDOM cycle-to-cycle variation in edge arrival on the SAME line.",
      "  Cause  : PLL noise, supply droop, crosstalk, temperature.",
      "  Remedy : it cannot be designed out - it is budgeted as clock uncertainty in the",
      "           SDC constraints and paid for out of every clock period."]),

    ("E34", "C", ["Design a 4-bit SIPO shift register. How many cycles until the first bit "
                  "appears at q[3]? Name three real uses."],
     ["always @(posedge clk or negedge rst_n)",
      "    if (!rst_n) q <= 4'b0000;",
      "    else        q <= {q[2:0], sin};",
      "",
      "Four clock cycles: the bit enters at q[0] on cycle 1 and reaches q[3] on cycle 4.",
      "",
      "Uses: (1) deserialising SPI/UART/JTAG data; (2) pipeline delay balancing; (3) the",
      "two-flop synchroniser IS a 2-bit shift register; (4) scan chains for manufacturing",
      "test; (5) with an XOR tap, an LFSR for pseudo-random generation or CRC."]),

    ("E35", "C", ["Why should you never write a ripple counter in RTL?"],
     ["A ripple counter clocks each stage from the previous stage's OUTPUT. That has",
      "three consequences:",
      "  1. Every stage adds one t_cq of skew, so an n-bit counter can read out a WRONG",
      "     intermediate value for up to n . t_cq after every edge.",
      "  2. It creates a new clock domain out of a DATA signal. Static timing analysis",
      "     cannot analyse it without special constraints, and usually just gives up.",
      "  3. Any glitch on a stage output becomes a spurious clock edge downstream.",
      "",
      "Always use one clock and an enable instead."]),

    ("E36", "C", ["Design a mod-10 synchronous counter. Give the state table and the next-state "
                  "equations for D flip-flops."],
     ["States 0000..1001; from 1001 the next state is 0000. Codes 1010..1111 are",
      "unreachable and treated as don't-cares.",
      "",
      "Since D = Q+ for a D flip-flop, the D column IS the next-state column. K-mapping",
      "each bit gives:",
      "",
      "  D0 = Q0'",
      "  D1 = Q1 XOR (Q0 . Q3')",
      "  D2 = Q2 XOR (Q1 . Q0)",
      "  D3 = Q3 XOR (Q3.Q0 + Q2.Q1.Q0)",
      "",
      "Check at count 9 (1001): D0 = 0; D1 = 0 XOR (1.0) = 0; D2 = 0 XOR 0 = 0;",
      "D3 = 1 XOR (1.1 + 0) = 0. Next state 0000. Correct.",
      "",
      "In RTL you would simply write:",
      "  if (cnt == 4'd9) cnt <= 4'd0; else cnt <= cnt + 1'b1;"]),

    ("E37", "C", ["Compare Moore and Mealy machines on five points, and say which you should "
                  "default to."],
     ["                    Moore                        Mealy",
      "  Output is         f(state)                     f(state, input)",
      "  Changes           just after a clock edge      the moment the input changes",
      "  Glitches          none (straight off FFs)      possible (combinational)",
      "  State count       usually more                 usually fewer",
      "  Reacts            one cycle later              same cycle",
      "",
      "Default to MOORE. Its outputs are registered, so they are glitch-free and",
      "trivially timeable. Use Mealy only when you need the one-cycle-earlier response,",
      "and then register the output before it leaves the block."]),

    ("E38", "C", ["Draw the Moore state diagram for a NON-overlapping '1011' detector and say how "
                  "it differs from the overlapping one."],
     ["States S0..S4 exactly as before, except for the transitions OUT of the accepting",
      "state S4. In the NON-overlapping machine a detection consumes the pattern, so:",
      "",
      "  overlapping    : S4 --1--> S1    S4 --0--> S2",
      "  non-overlapping: S4 --1--> S0    S4 --0--> S0",
      "",
      "On the stream 1011011 the overlapping machine fires TWICE (it reuses the trailing",
      "'11'); the non-overlapping machine fires ONCE."]),

    ("E39", "C", ["Give the state table for the overlapping 1011 Moore detector with the encoding "
                  "S0=000 … S4=100, and derive Z."],
     ["  Present   Q2Q1Q0   Next(X=0)   Next(X=1)   Z",
      "  S0        000      S0  000     S1  001     0",
      "  S1        001      S2  010     S1  001     0",
      "  S2        010      S0  000     S3  011     0",
      "  S3        011      S2  010     S4  100     0",
      "  S4        100      S2  010     S1  001     1",
      "",
      "Z = Q2, because S4 is the only state whose code has Q2 = 1. Choosing the encoding",
      "so that the output falls out for free is worth doing deliberately.",
      "",
      "Next-state equations (codes 101-111 as don't-cares):",
      "  D2 = Q1 . Q0 . X",
      "  D1 = X' . (Q2 + Q0) + Q1 . Q0' . X",
      "  D0 = X . (Q1 . Q0)'"]),

    ("E40", "C", ["Compare binary, Gray and one-hot encoding for a 9-state FSM. Which would you "
                  "choose on an FPGA and on an ASIC?"],
     ["9 states:",
      "  binary  : ceil(log2 9) = 4 flip-flops, most next-state logic",
      "  Gray    : 4 flip-flops, similar logic, but only one bit toggles per step",
      "  one-hot : 9 flip-flops, next-state logic only one level deep",
      "",
      "FPGA -> one-hot. Flip-flops are abundant and effectively free; LUT DEPTH is what",
      "limits your clock, and one-hot next-state logic is shallow.",
      "",
      "ASIC with many states -> binary, to keep register area down.",
      "Low-power or a signal crossing clock domains -> Gray, because only one bit",
      "changes per transition (less switching energy, and safe to sample)."]),

    ("E41", "C", ["Name five ways an FSM fails in silicon and give the prevention for each."],
     ["1. Unreachable/illegal states  - 5 states in 3 bits leaves codes 101-111 in the",
      "   hardware. A glitch or SEU lands you there.  Fix: a `default` branch returning",
      "   to a safe state.",
      "2. Deadlock - a group of states with no path back.  Fix: prove reachability from",
      "   every state to the start state.",
      "3. Incomplete transitions - a state with no arc for some input; in RTL this",
      "   becomes an inferred latch.  Fix: default assignment at the top of the block.",
      "4. Unregistered Mealy output driving a clock enable or a write strobe.  Fix:",
      "   register the output, or use Moore.",
      "5. An asynchronous input fed straight into the FSM.  Fix: two-flop synchroniser",
      "   on EVERY asynchronous input."]),

    ("E42", "C", ["Explain why the code below builds ONE flip-flop rather than two."],
     ["    always @(posedge clk) begin",
      "        q1 = d;",
      "        q2 = q1;",
      "    end",
      "",
      "Blocking assignments execute in order, like software. q1 takes the value of d",
      "IMMEDIATELY, so the next line assigns that same value to q2. Both registers get d,",
      "so the optimiser merges them - one flip-flop, not a two-stage shift register.",
      "",
      "Worse, the simulation result depends on the order the simulator happens to",
      "evaluate always blocks, so simulation and synthesis can disagree.",
      "",
      "Fix: use non-blocking <= in every clocked block. Then both right-hand sides are",
      "sampled first and both registers update together, which is exactly what real",
      "flip-flops do on a clock edge."]),

    ("E43", "C", ["When would you choose an asynchronous reset, and what is a reset synchroniser?"],
     ["Choose ASYNCHRONOUS reset when the design must be forced to a known state with NO",
      "clock running - which includes every power-up, before the PLL has locked.",
      "",
      "The danger is the RELEASE: an asynchronous de-assertion can violate the",
      "flip-flop's recovery and removal times (the reset-pin equivalents of setup and",
      "hold), which can itself put the flip-flop into a metastable state.",
      "",
      "A RESET SYNCHRONISER solves both: two flip-flops clocked by the destination clock,",
      "with their asynchronous reset pins tied to the raw reset. The output asserts the",
      "instant the raw signal drops (works with no clock) but releases cleanly on a",
      "clock edge. Assert asynchronously, de-assert synchronously."]),

    ("E44", "C", ["Sketch the FSMD architecture and identify what crosses each way."],
     ["  +---------------+  control signals  +---------------+",
      "  |  CONTROLLER   | ----------------> |   DATAPATH    |",
      "  |   (an FSM)    |                   | registers,    |",
      "  |               | <---------------- | ALU, MUXes    |",
      "  +---------------+   status flags    +---------------+",
      "",
      "Controller -> datapath: load, shift, select, enable, opcode.",
      "Datapath -> controller: zero, negative, carry, overflow, done, terminal count.",
      "",
      "The controller decides WHEN; the datapath decides WHAT. Every processor, DMA",
      "engine, UART and SPI controller has exactly this shape."]),

    ("E45", "C", ["A design has a 100 MHz clock and a 30 MHz asynchronous input that changes on "
                  "every one of its own edges. Using tau = 50 ps, T0 = 20 ps, estimate the MTBF "
                  "of a single flip-flop given 5 ns of resolution time, then for a two-flop "
                  "synchroniser giving 10 ns."],
     ["MTBF = e^(t_r/tau) / (T0 . f_clk . f_data)",
      "",
      "Denominator = 20e-12 x 100e6 x 30e6 = 6.0e4  (per second)",
      "",
      "One stage, t_r = 5 ns:   e^(5000/50)  = e^100  ~= 2.7e43",
      "                         MTBF = 2.7e43 / 6.0e4 = 4.5e38 s",
      "",
      "Two stages, t_r = 10 ns: e^(10000/50) = e^200 ~= 7.2e86",
      "                         MTBF = 7.2e86 / 6.0e4 = 1.2e82 s",
      "",
      "Both look enormous because tau is generous here; the POINT is the ratio. Doubling",
      "the resolution time SQUARED the MTBF, because t_r sits in an exponent. That is",
      "why one extra flip-flop is such a cheap and effective fix - and why using a",
      "realistic (much larger) tau for a fast process can make a single stage genuinely",
      "unsafe."]),

    ("E46", "C", ["You inherit an RTL block whose synthesis report shows 4 200 cells for a "
                  "function you believe needs about 40 gates, plus 12 $_DLATCH_ cells. List, in "
                  "order, what you would check."],
     ["1. The 12 latches first - they are a definite bug and often the root cause.",
      "   Find every combinational always block and check that each output is assigned",
      "   on EVERY path. Add default assignments at the top of each block.",
      "2. Check bus widths. A missing width on a parameter or a literal (e.g. writing 1",
      "   where you meant 1'b1 in a wide expression) can silently create 32-bit logic.",
      "3. Check for accidental multipliers or dividers. A single `*` or `/` in RTL can",
      "   become thousands of gates. Look for `%` too.",
      "4. Check loop bounds in generate/for constructs - an off-by-one or a parameter",
      "   that did not get overridden can replicate logic hundreds of times.",
      "5. Check that don't-care conditions were actually declared. Logic minimised",
      "   without them can be several times larger.",
      "6. Only then look at the timing constraint. An over-tight clock makes the tool",
      "   duplicate and upsize logic aggressively; relax it and re-run to see how much",
      "   of the area is timing-driven rather than functional."]),
]

SECTIONS = {
    "A": "Section A · Boolean algebra and logic gates",
    "B": "Section B · Combinational logic",
    "C": "Section C · Sequential logic and state machines",
}


def build_exercises(w):
    w.h1("Part 5 · Practice Exercises")
    w.para([N("Attempt every exercise before opening Part 6. An exercise whose answer you have "
              "already read teaches you nothing. Show your working — in an examination the method "
              "carries most of the marks.")])
    for key in ("A", "B", "C"):
        w.h2(SECTIONS[key])
        for eid, sec, q, _ in EX:
            if sec != key:
                continue
            p = w.d.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(7)
            r = p.add_run(eid + ".  ")
            r.font.bold = True; r.font.color.rgb = TEAL; r.font.size = Pt(10.5)
            for line in q:
                rr = p.add_run(line)
                rr.font.size = Pt(10.5); rr.font.color.rgb = BODY
    w.page_break()


def build_solutions(w):
    w.h1("Part 6 · Worked Solutions")
    w.para([N("Full solutions to every exercise in Part 5. Where a numerical answer is asked for, "
              "the method is shown line by line — copy the method, not the number.")])
    for key in ("A", "B", "C"):
        w.h2(SECTIONS[key])
        for eid, sec, q, a in EX:
            if sec != key:
                continue
            p = w.d.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(8)
            r = p.add_run(eid + ".  ")
            r.font.bold = True; r.font.color.rgb = TEAL; r.font.size = Pt(10.5)
            rr = p.add_run(" ".join(q))
            rr.font.size = Pt(10); rr.font.italic = True; rr.font.color.rgb = SLATE
            w.code(a, size=8.6)
    w.page_break()


def build_reference(w):
    w.h1("Part 7 · Reference")

    w.h2("7.1  Formula sheet")
    w.code([
        "BOOLEAN",
        "  A + 0 = A          A . 1 = A            identity",
        "  A + 1 = 1          A . 0 = 0            null",
        "  A + A = A          A . A = A            idempotent",
        "  A + A' = 1         A . A' = 0           complement",
        "  A + A.B = A        A . (A+B) = A        absorption",
        "  A + A'.B = A + B   A . (A'+B) = A.B     simplification",
        "  (A+B)' = A'.B'     (A.B)' = A'+B'       De Morgan",
        "  AB + A'C + BC = AB + A'C                consensus",
        "",
        "ARITHMETIC",
        "  half adder :  S = A XOR B                C = A.B",
        "  full adder :  S = A XOR B XOR Cin        Cout = A.B + Cin.(A XOR B)",
        "  ripple adder delay :  t = (n-1).t_carry + t_sum",
        "  lookahead  :  G = A.B ,  P = A XOR B ,  C(i+1) = G + P.C(i)",
        "  two's complement : negate = invert all bits, then add 1",
        "  n-bit signed range : -2^(n-1) ... +2^(n-1) - 1",
        "  signed overflow V = Cn XOR C(n-1)",
        "",
        "TIMING",
        "  setup :  T_clk >= t_cq + t_logic,max + t_setup + t_jitter - t_skew",
        "  hold  :  t_cq + t_logic,min >= t_hold + t_skew",
        "  slack :  available - required   (positive = met)",
        "  f_max :  1 / T_clk(min)",
        "  MTBF  :  e^(t_r/tau) / (T0 . f_clk . f_data)",
        "",
        "FLIP-FLOPS",
        "  D  : Q+ = D                T  : Q+ = T XOR Q",
        "  JK : Q+ = J.Q' + K'.Q      SR : Q+ = S + R'.Q   (SR != 11)",
        "  D from T : D = T XOR Q     T from D : T = D XOR Q",
        "",
        "ENCODING (n states)",
        "  binary / Gray : ceil(log2 n) flip-flops     one-hot : n flip-flops",
    ], "Everything you should be able to reproduce from memory")

    w.h2("7.2  Glossary")
    terms = [
        ("Absorption", "A + A·B = A. One of the two laws that make K-map grouping work."),
        ("Canonical form", "SOP or POS written directly from the truth table; unique but rarely minimal."),
        ("Contamination delay", "The minimum delay through a gate — how soon its output can start to change. Used in hold checks."),
        ("Critical path", "The slowest input-to-output route through a block; it sets the maximum frequency."),
        ("CDC", "Clock-domain crossing. Any signal passing between two unrelated clocks; must be synchronised."),
        ("Don't-care (X)", "An input combination that cannot occur or whose output is never read. Free optimisation."),
        ("Duality", "Swap AND↔OR and 0↔1; a true Boolean identity stays true."),
        ("Essential prime implicant", "The only prime implicant covering some particular minterm; must appear in every minimal cover."),
        ("Excitation table", "Tells you which flip-flop inputs produce a required state transition. Used to DESIGN."),
        ("Fan-in / fan-out", "Number of inputs on a gate / number of loads driven by one output."),
        ("FSMD", "Finite state machine with datapath — a controller FSM plus a datapath, exchanging control signals and status flags."),
        ("Gate equivalent (GE)", "Area unit: the area of one 2-input NAND cell in that technology."),
        ("Gray code", "An ordering in which successive values differ in exactly one bit."),
        ("Hazard", "A transient wrong output caused by unequal path delays; the steady-state logic is still correct."),
        ("Huffman model", "The canonical picture of a sequential circuit: combinational logic plus a state register in a feedback loop."),
        ("Implicant", "Any product term covering only 1s of the function."),
        ("Jitter", "Random cycle-to-cycle variation in clock-edge arrival."),
        ("Latch", "Level-sensitive storage: transparent for as long as its enable is asserted."),
        ("LFSR", "Linear-feedback shift register: a shift register with XOR feedback, producing a pseudo-random sequence."),
        ("Literal", "A variable or its complement. A and A′ are two literals."),
        ("Mealy machine", "Output depends on state AND input; fewer states, reacts immediately, can glitch."),
        ("Metastability", "An invalid intermediate flip-flop output after a setup/hold violation; resolves at random after an unbounded time."),
        ("Minterm / maxterm", "The AND term true for exactly one row / the OR term false for exactly one row."),
        ("Moore machine", "Output depends on state only; glitch-free, reacts one cycle later."),
        ("MTBF", "Mean time between failures — the standard measure of synchroniser reliability."),
        ("Noise margin", "How much interference a signal can absorb and still be read correctly."),
        ("One-hot", "A state encoding using one flip-flop per state, exactly one of which is 1."),
        ("Prime implicant", "An implicant that cannot be combined into any larger group."),
        ("Propagation delay t_pd", "Time from an input change to the corresponding output change, at the 50 % points."),
        ("Recovery / removal", "Setup and hold, but for the reset pin: how long before/after the clock edge reset must be de-asserted."),
        ("Restoring logic", "The property that every gate outputs a clean full-swing level, so noise never accumulates."),
        ("Safe FSM", "One whose default branch returns any illegal state code to a known good state."),
        ("Setup / hold time", "How long data must be stable before / after the active clock edge."),
        ("Skew", "Fixed difference in clock-edge arrival time between flip-flops; caused by the clock tree."),
        ("Slack", "Available time minus required time. Positive means met; negative is a violation."),
        ("SOP / POS", "Sum of products / product of sums."),
        ("Synchroniser", "Two or three cascaded flip-flops that reduce metastable failure to a negligible rate."),
        ("State", "An equivalence class of input histories — everything the circuit needs to remember."),
        ("Universal gate", "NAND or NOR — enough on its own to build any Boolean function."),
    ]
    for t, d in terms:
        w.para([B(t + " — "), N(d)], size=10, space_after=3)

    w.h2("7.3  Where to go next")
    w.bullets([
        [B("Topic 4 — RTL Design Using HDL (6 h). "),
         N("Every construct there maps onto something here: truth tables become assign and "
           "always @(*); MUXes become case; flip-flops become always @(posedge clk); state "
           "diagrams become the three-block template.")],
        [B("Topic 5 — RTL Simulation and Verification (6 h). "),
         N("The self-checking testbenches from Part 4 grow into coverage-driven verification.")],
        [B("Topic 6 — Timing Constraints and Analysis (4 h). "),
         N("The setup and hold arithmetic in §3.6 done automatically over every path, from SDC "
           "constraints.")],
    ])
    w.h3("Classic references, if you want to read further")
    w.bullets([
        "M. Morris Mano & Michael Ciletti, Digital Design — the standard undergraduate text for "
        "Boolean algebra, K-maps and FSM design.",
        "Neil Weste & David Harris, CMOS VLSI Design — for the transistor-level costs quoted in §1.4.",
        "David Harris & Sarah Harris, Digital Design and Computer Architecture — the clearest "
        "treatment of timing, metastability and the FSMD architecture.",
        "Clifford Cummings' SNUG papers on non-blocking assignments and clock-domain crossing — "
        "freely available, and still the definitive practical guidance.",
    ])
    w.para([N("End of the Module 2 · Topic 3 workbook.  Next: Topic 4 — RTL Design Using HDL.",
              {"b": True, "c": NAVY})], space_after=0)
