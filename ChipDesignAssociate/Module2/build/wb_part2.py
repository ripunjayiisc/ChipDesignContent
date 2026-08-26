# -*- coding: utf-8 -*-
"""Workbook Part 2: combinational logic design."""
from wbkit import *
from wb_part1 import B, N, I, M


def build(w):
    w.h1("Part 2 · Combinational Logic Design")
    w.para([N("Combinational logic has no memory: its output is a pure function of its present "
              "inputs. Everything in this part is a pattern you will meet again in Verilog in "
              "Topic 4, and again in a timing report in Topic 6.")])

    # ---------------------------------------------------------- 2.1
    w.h2("2.1  The defining property")
    w.image("comb_vs_seq", 6.5, "Figure 2.1 — the only structural difference is the feedback path")
    w.table(["", "Combinational", "Sequential"],
            [["Output depends on", "present inputs only", "present inputs AND stored state"],
             ["Memory", "none", "yes — in flip-flops or latches"],
             ["Clock", "not needed", "required (in synchronous design)"],
             ["Feedback", "none — the graph is acyclic", "yes, through a storage element"],
             ["Analysed with", "truth tables, K-maps", "state tables, state diagrams"],
             ["Typical blocks", "adder, MUX, decoder, ALU", "register, counter, FSM"]],
            [1.5, 2.4, 2.9], bold_cols=(0,), size=9, align_center=False)
    w.callout("Definitions worth memorising verbatim",
              [[B("Combinational: "), N("the output at any instant depends ONLY on the inputs at "
                                        "that instant, after a bounded settling delay.")],
               [B("Sequential: "), N("the output depends on the present inputs AND on the "
                                     "sequence of past inputs, summarised in a finite amount of "
                                     "stored state.")]],
              color=TEAL)

    # ---------------------------------------------------------- 2.2
    w.h2("2.2  The seven-step design procedure")
    w.image("comb_design_flow", 6.5, "Figure 2.2 — follow this every time")
    w.h3("Worked micro-example")
    w.para([B("Problem: "), N("light a warning LED when at least two of three sensors read high.")])
    w.numbered([
        N("State it: 'W = 1 when two or more of A, B, C are 1.'"),
        N("Name the ports: inputs A, B, C (1 bit each); output W (1 bit)."),
        N("Truth table: W = 1 for ABC = 011, 101, 110, 111 — four of the eight rows."),
        N("Canonical SOP: W = A'BC + AB'C + ABC' + ABC."),
        N("K-map → W = AB + BC + AC. This is the MAJORITY function."),
        N("Circuit: three 2-input ANDs feeding one 3-input OR."),
        N("Verify: simulate all eight input cases against the table."),
    ])
    w.callout("Where the bugs actually are",
              ["Almost every combinational bug is created at step 3. A missing row, a case nobody "
               "thought about, or an input combination the specification never mentioned. When "
               "you cannot enumerate the rows because there are too many, enumerate the "
               "CATEGORIES of behaviour instead, and make sure every input maps into exactly one."],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 2.3
    w.h2("2.3  Adders")
    w.image("adders", 6.5, "Figure 2.3 — half adder and full adder")
    w.h3("Half adder")
    w.para([N("S = A ⊕ B,  C = A · B. It cannot accept a carry IN, so it is only usable for the "
              "least-significant bit.")])
    w.h3("Full adder")
    w.para([N("S = A ⊕ B ⊕ Cin,  Cout = A·B + Cin·(A ⊕ B). Derive Cout from the truth table: "
              "Cout is 1 whenever at least two of the three inputs are 1 — the majority function "
              "again, which is why the two derivations look identical.")])
    w.para([B("Built from two half adders: "), N("the first adds A and B, the second adds that sum "
              "to Cin, and an OR gate combines the two carries. Cout = C₁ + C₂ (the two carries "
              "can never both be 1).")])

    w.h3("Ripple-carry adder")
    w.image("ripple_adder", 6.5, "Figure 2.4 — 4-bit ripple carry, and why it is slow")
    w.para([N("Chain n full adders, Cout to Cin. Minimal area, trivially correct, and its delay "
              "grows LINEARLY with n:")])
    w.callout(None, [[B("t_adder = (n − 1) · t_carry + t_sum")]], color=NAVY, bar="0E2A47")
    w.para([N("The critical path runs from the least-significant inputs, through every carry "
              "stage, to the MOST-significant SUM — not to the final carry-out. Getting that "
              "endpoint right is a classic exam discriminator.")])

    w.h3("Carry-lookahead")
    w.para([N("Define two signals per bit:")])
    w.bullets([
        [B("Generate  Gᵢ = Aᵢ · Bᵢ  "), N("— this bit produces a carry regardless of Cin.")],
        [B("Propagate Pᵢ = Aᵢ ⊕ Bᵢ  "), N("— this bit passes an incoming carry through.")],
    ])
    w.para([N("Then Cᵢ₊₁ = Gᵢ + Pᵢ·Cᵢ. Expanding the recursion removes the dependence on the "
              "previous carry entirely:")])
    w.code(["C1 = G0 + P0.C0",
            "C2 = G1 + P1.G0 + P1.P0.C0",
            "C3 = G2 + P2.G1 + P2.P1.G0 + P2.P1.P0.C0",
            "C4 = G3 + P3.G2 + P3.P2.G1 + P3.P2.P1.G0 + P3.P2.P1.P0.C0"],
           "Carry equations for a 4-bit lookahead block")
    w.para([N("Every carry is now two gate levels from the inputs, so delay grows as log n when "
              "lookahead blocks are themselves cascaded — at the cost of considerably more area "
              "and much higher fan-in. Other schemes you will hear named: carry-select, "
              "carry-skip, and the Brent–Kung and Kogge–Stone parallel-prefix adders.")])
    w.para([B("In RTL you write "), M("assign {cout, sum} = a + b + cin;"),
            N(" and the synthesiser picks a structure to meet your timing constraint. Knowing the "
              "structures is how you understand why the area exploded when you tightened the clock.")])

    w.h3("Subtraction comes free")
    w.para([N("A − B = A + (−B) = A + B' + 1. Feed B through XOR gates controlled by a "),
            M("sub"), N(" signal (XOR with 1 inverts, XOR with 0 passes through) and tie the same "),
            M("sub"), N(" to Cin. One adder now performs both operations — which is exactly the "
                        "ADDER/SUBTRACTOR block in the ALU.")])

    # ---------------------------------------------------------- 2.4
    w.h2("2.4  Multiplexers and de-multiplexers")
    w.image("mux_demux", 6.5, "Figure 2.5 — the data-routing pair")
    w.para([N("A multiplexer is a controllable switch: n select lines choose one of 2ⁿ data inputs. "
              "It is the single most common structure in real hardware, because every "),
            M("if"), N(", every "), M("case"), N(", every shared bus and every function select "
                                                 "becomes a MUX after synthesis.")])
    w.code(["Y = S1'.S0'.I0 + S1'.S0.I1 + S1.S0'.I2 + S1.S0.I3"],
           "4:1 MUX as a sum of products")
    w.h3("The MUX as a universal logic element")
    w.para([N("A 2ⁿ:1 MUX implements ANY function of n variables: wire the truth-table output "
              "column to the data inputs and the variables to the select lines. No minimisation "
              "needed at all.")])
    w.para([B("Halving it. "), N("An n-variable function actually needs only a 2ⁿ⁻¹:1 MUX. Use "
              "n−1 variables as select, then read the truth table in PAIRS of rows: each pair "
              "needs 0, 1, the last variable, or its complement on that data input.")])
    w.callout("This is literally how an FPGA works",
              ["An FPGA logic cell is a small SRAM — typically a 6-input look-up table, which is a "
               "64:1 MUX with programmable data bits — plus a flip-flop. Programming an FPGA means "
               "writing truth tables into those SRAM cells.",
               [B("Consequence for your RTL: "),
                N("on an FPGA a 6-input function and a 2-input function cost the SAME single LUT, "
                  "so splitting logic into tiny pieces buys nothing and can cost you levels of "
                  "delay. On an ASIC the opposite is true. Know your target before you optimise.")]],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")
    w.h3("De-multiplexer")
    w.para([N("The reverse: one input routed to one of 2ⁿ outputs, with all others driven to 0. "
              "A decoder is simply a de-multiplexer with its data input tied to 1.")])

    # ---------------------------------------------------------- 2.5
    w.h2("2.5  Decoders, encoders and priority encoders")
    w.image("decoder_encoder", 6.5, "Figure 2.6 — converting between codes and one-hot lines")
    w.para([B("Decoder: "), N("binary code in, one-hot out. Exactly one output is asserted. Used "
              "for memory chip-select, instruction decode and control-line generation. Real "
              "decoders have an ENABLE pin, which is how several are cascaded — two 2:4 decoders "
              "plus one 1:2 make a 3:8 decoder.")])
    w.para([B("Encoder: "), N("one-hot in, binary code out. A PLAIN encoder assumes exactly one "
              "input is high; if two are, it outputs the OR of their codes, which is simply "
              "wrong.")])
    w.para([B("Priority encoder: "), N("resolves simultaneous inputs by a fixed priority — highest "
              "index wins. A separate VALID output distinguishes 'input 0 is active' (code 00, "
              "V = 1) from 'nothing is active' (code 00, V = 0). Interrupt controllers and bus "
              "arbiters are priority encoders.")])

    # ---------------------------------------------------------- 2.6
    w.h2("2.6  Comparators, parity and other standard cells")
    w.image("comparator_parity", 6.5, "Figure 2.7 — magnitude comparator and parity tree")
    w.h3("Comparator")
    w.numbered([
        [N("1-bit equality: "), M("e = (A ⊕ B)'"), N("  — XNOR IS the equality gate. This is the "
          "single most useful gate identity in the whole topic.")],
        [N("n-bit equality: AND together all n of those XNOR outputs.")],
        [N("Magnitude: work MSB-first. A > B if, at the highest bit position where they differ, "
           "A has a 1. Formally A>B = A₃B₃' + e₃(A₂B₂') + e₃e₂(A₁B₁') + e₃e₂e₁(A₀B₀').")],
    ])
    w.h3("Parity")
    w.para([N("P = D₀ ⊕ D₁ ⊕ … ⊕ Dₙ₋₁ is the EVEN parity bit: it is 1 when the number of 1s in "
              "the data is odd, so that data+parity always has an even number of 1s. The receiver "
              "re-computes it; a mismatch means at least one bit flipped.")])
    w.para([B("Its limit: "), N("parity detects any ODD number of errors and MISSES every even "
              "number. It cannot correct anything. For real protection use Hamming codes or ECC — "
              "the same XOR-tree idea with more check bits, arranged so the syndrome identifies "
              "which bit flipped.")])
    w.h3("Others in every library")
    w.bullets(["Barrel shifter — a MUX per output bit; shifts or rotates by any amount in one cycle.",
               "Binary ↔ Gray converters — G = B ⊕ (B>>1);  B = successive XORs of G from the MSB.",
               "Leading-zero counter / priority encoder — used in floating-point normalisation.",
               "Population count (ones counter) — a tree of adders."])

    # ---------------------------------------------------------- 2.7
    w.h2("2.7  The arithmetic logic unit")
    w.image("alu_block", 6.5, "Figure 2.8 — an ALU is combinational blocks sharing one MUX")
    w.para([N("Structurally trivial: run every operation in parallel on the same operands and let "
              "the opcode select which answer leaves the block. It wastes power computing results "
              "you discard, and it is fast, regular and easy to verify — which usually wins.")])
    w.h3("The status flags")
    w.table(["Flag", "Name", "Computed as", "Meaning"],
            [["Z", "zero", "NOR of every result bit", "the result is exactly zero"],
             ["N", "negative", "the MSB of the result", "sign bit in two's complement"],
             ["C", "carry", "carry out of the MSB", "UNSIGNED overflow / borrow"],
             ["V", "overflow", "Cₙ ⊕ Cₙ₋₁", "SIGNED overflow"]],
            [0.6, 1.1, 2.2, 2.9], bold_cols=(0,), size=9, align_center=False)
    w.callout("C and V are not the same flag",
              [[N("Adding "), M("0111 1111 (+127)"), N(" and "), M("0000 0001 (+1)"),
                N(" gives "), M("1000 0000"), N(", which reads as −128. Carry-out is 0, so C = 0. "
                  "But the carry INTO the sign bit was 1 and the carry OUT was 0, so V = 1.")],
               N("Unsigned code reads C and ignores V. Signed code reads V and ignores C. Reading "
                 "the wrong one is a classic source of silent arithmetic bugs.")],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 2.8
    w.h2("2.8  What limits combinational speed")
    w.image("delay_fanout", 6.5, "Figure 2.9 — propagation delay, fan-in and fan-out")
    w.table(["Term", "Definition"],
            [["Propagation delay t_pd", "time from an input change to the corresponding output "
                                        "change, measured at the 50 % points"],
             ["Contamination delay t_cd", "the MINIMUM delay — how soon the output can start to "
                                          "change; matters for hold checks"],
             ["Fan-in", "number of inputs on one gate"],
             ["Fan-out", "number of gate inputs one output drives"],
             ["Critical path", "the slowest input-to-output route through the block"]],
            [1.8, 4.8], bold_cols=(0,), align_center=False)
    w.para([B("Why fan-out costs time. "), N("Each load adds gate capacitance. Charging more "
              "capacitance through the same driver resistance takes longer, so delay rises "
              "roughly linearly with load: t_pd ≈ t_intrinsic + k·C_load. The fixes are buffering "
              "(inserting repeaters) and upsizing the driver.")])
    w.para([B("Why fan-in costs time. "), N("A static CMOS gate stacks transistors in series, one "
              "per input, so a 6-input NAND is far slower than a balanced tree of 2-input NANDs. "
              "The fix is logic restructuring, which synthesis does automatically — provided you "
              "did not write the expression in a way that forces a chain.")])

    # ---------------------------------------------------------- 2.9
    w.h2("2.9  Hazards and glitches")
    w.image("hazards", 6.5, "Figure 2.10 — correct logic, wrong transient")
    w.para([N("A hazard is a momentary wrong output caused purely by unequal path delays. The "
              "steady-state logic is perfectly correct; only the transient is wrong.")])
    w.table(["Type", "Symptom", "Cause"],
            [["Static-1", "output should stay 1 but dips to 0",
              "two AND terms hand over with a gap"],
             ["Static-0", "output should stay 0 but spikes to 1",
              "the dual situation in POS form"],
             ["Dynamic", "one transition that bounces 0→1→0→1",
              "three or more unequal paths to the output"]],
            [1.1, 2.9, 2.6], bold_cols=(0,), size=9, align_center=False)
    w.h3("Removing a static-1 hazard")
    w.para([N("Take F = A·B' + B·C with A = C = 1 and B falling. The B·C term releases before the "
              "A·B' term arrives, so F dips. On the K-map the two groups are ADJACENT but do not "
              "OVERLAP — that gap is the hazard. Add the consensus term that bridges them:")])
    w.callout(None, [[B("F = A·B' + B·C + A·C")]], color=GREEN, fill="EEF7F1", bar="2A9D5C")
    w.para([N("The A·C term is logically redundant — it changes nothing about the steady-state "
              "function — but it holds F high through the transition. Redundant terms cost area "
              "and are the one case where you deliberately do NOT minimise.")])
    w.callout("Where a glitch is harmless, and where it kills the chip",
              [[B("Harmless: "), N("driving the D input of a flip-flop, provided it settles before "
                                   "the next clock edge. This is the normal case, and it is the "
                                   "main argument for synchronous design.")],
               [B("Fatal: "), N("on a clock line, a reset line, an asynchronous set/clear, a "
                                "memory write-enable, or any signal leaving the chip. NEVER "
                                "generate a clock from combinational logic — use a clock enable "
                                "on the flip-flop instead.")]],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 2.10
    w.h2("2.10  Combinational logic in Verilog")
    w.para([N("Three correct ways, and one way to get it catastrophically wrong.")])
    w.code([
        "// 1. Continuous assignment - always safe, always combinational",
        "assign y = (a & b) | (~a & c);",
        "",
        "// 2. always @(*) with BLOCKING assignments and a DEFAULT",
        "always @(*) begin",
        "    y = 1'b0;                      // default first: kills every latch",
        "    case (sel)",
        "        2'b00: y = i0;",
        "        2'b01: y = i1;",
        "        default: y = 1'b0;",
        "    endcase",
        "end",
        "",
        "// 3. WRONG - incomplete assignment infers a transparent LATCH",
        "always @(*) begin",
        "    if (enable) y = d;             // no else -> 'hold y' -> latch",
        "end",
    ], "Combinational always blocks")
    w.h3("The three rules")
    w.numbered([
        [N("Use "), M("="), N(" (blocking) in combinational blocks. Never "), M("<="), N(".")],
        N("Assign every output on every path. A default assignment at the top of the block is the "
          "easiest way to guarantee this."),
        [N("Use "), M("always @(*)"), N(", never a hand-written sensitivity list — an incomplete "
          "list makes simulation and synthesis disagree.")],
    ])
    w.callout("How to catch an inferred latch",
              [[B("Yosys: "), M("$_DLATCH_"), N(" cells appear in the "), M("stat"),
                N(" report. Commercial tools print 'inferred latch for signal y'.")],
               [B("Treat every such warning as an ERROR. "),
                N("There is no case anywhere in this course where you want an unintended latch. "
                  "The lab includes "), M("rtl/broken_latch.v"),
                N(" specifically so you can see what one looks like in a report.")]],
              color=RED, fill="FDECEF", bar="C01F43")
    w.page_break()
