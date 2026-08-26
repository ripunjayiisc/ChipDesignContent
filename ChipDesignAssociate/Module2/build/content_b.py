# -*- coding: utf-8 -*-
"""Topic 3 deck — rest of 3A (gates, laws, K-maps) and all of 3B (combinational)."""
from deckkit import *
from content_a import R, G


def build(d):
    # ================================================================ gates
    s = d.slide("TOPIC 3A · THE GATES", "The Seven Logic Gates — Symbol, Expression, Truth Table")
    y = d.lead(s, TOP, [[
        R("A logic gate is a physical circuit (in CMOS, a handful of transistors) that computes one "
          "Boolean operator. ", b=True, c=NAVY, s=12.5),
        R("Learn to read these symbols instantly — schematics, synthesis reports and datasheets all "
          "assume you can.")]], h=502920)
    y = d.image(s, y + 45720, "gate_gallery", 3657600)
    d.card(s, y + 91440, "Transistor cost — why NAND and NOR are the cheapest gates in CMOS",
           [[R("In static CMOS, an inverter costs 2 transistors, a 2-input NAND or NOR costs 4, but a "
               "2-input AND or OR costs 6 ", ),
             R("(they are built as NAND/NOR followed by an inverter)", i=True, c=SLATE),
             R(". XOR costs 8–12. This is why standard-cell libraries are dominated by NAND/NOR/inverter "
               "cells and why synthesis output rarely contains a literal AND gate.")]],
           accent=AMBER, fill=CARD_A, h=868680)

    # ================================================================ universal gates
    s = d.slide("TOPIC 3A · UNIVERSALITY", "Universal Gates — NAND and NOR Can Build Anything", AMBER)
    y = d.lead(s, TOP, [[
        R("A gate is UNIVERSAL if any Boolean function can be built from copies of it alone. ",
          b=True, c=NAVY, s=12.5),
        R("NAND and NOR are the only two-input gates with this property (AND, OR and XOR are not — none "
          "of them can produce a NOT). The proof is constructive: build NOT, AND and OR from it, and "
          "since every function has an SOP form, you are done.")]], h=594360)
    y = d.image(s, y + 45720, "universal_nand", 3200400)
    y = d.cols(s, y + 91440, [
        ("Why it matters in manufacturing",
         [[R("One well-characterised cell can be tiled everywhere, so the foundry optimises, "
             "models and yields a small library instead of a large one.", s=10.5)]], AMBER, CARD_A),
        ("Why it matters in design",
         [[R("Synthesis 'technology maps' your logic onto whatever cells the library actually has — "
             "so your AND gate may well appear as two NANDs in the netlist.", s=10.5)]], TEAL, CARD)],
        h=1005840)

    # ================================================================ laws
    s = d.slide("TOPIC 3A · LAWS", "Boolean Axioms, Laws and Theorems")
    y = d.lead(s, TOP, [[
        R("Every one of these can be proved with a truth table, and every one is a legal, "
          "behaviour-preserving circuit transformation. ", b=True, c=NAVY, s=12.5),
        R("Synthesis tools apply them thousands of times per second; you apply them by hand to check "
          "the tool and to simplify before you write the code.")]], h=502920)
    rows = [["Identity", "A + 0 = A", "A · 1 = A"],
            ["Null / Dominance", "A + 1 = 1", "A · 0 = 0"],
            ["Idempotent", "A + A = A", "A · A = A"],
            ["Complement", "A + A' = 1", "A · A' = 0"],
            ["Involution", "(A')' = A", "—"],
            ["Commutative", "A + B = B + A", "A · B = B · A"],
            ["Associative", "A + (B + C) = (A + B) + C", "A · (B · C) = (A · B) · C"],
            ["Distributive", "A · (B + C) = A·B + A·C", "A + (B · C) = (A+B) · (A+C)"],
            ["Absorption", "A + A·B = A", "A · (A + B) = A"],
            ["Simplification", "A + A'·B = A + B", "A · (A' + B) = A · B"],
            ["Consensus", "AB + A'C + BC = AB + A'C", "(A+B)(A'+C)(B+C) = (A+B)(A'+C)"]]
    y = d.table(s, y + G, ["Law", "OR form", "AND form"], rows,
                [2286000, 4480560, 4480560], rh=274320, bold_cols=(0,),
                col_colors={0: TEAL, 1: NAVY, 2: NAVY}, size=10)
    d.card(s, y + G, "Two ideas that make the table half as long",
           [[R("Duality. ", b=True, c=AMBER),
             R("Swap every AND ↔ OR and every 0 ↔ 1 and a true statement stays true — which is why the "
               "two columns above are mirror images. You only have to memorise one column.")],
            [R("Why the second distributive law surprises people. ", b=True, c=AMBER),
             R("A + B·C = (A+B)(A+C) has no counterpart in ordinary arithmetic. Verify it on all 8 rows "
               "once and you will trust it forever.")]],
           accent=AMBER, fill=CARD_A, h=1188720)

    # ================================================================ De Morgan
    s = d.slide("TOPIC 3A · DE MORGAN", "De Morgan's Theorems — The Most-Used Identity in RTL", RED)
    y = d.lead(s, TOP, [[
        R("Break the bar, change the operator. ", b=True, c=NAVY, s=12.5),
        R("These two identities let you push inversions through a network, convert any AND-OR structure "
          "into an all-NAND structure, and read active-low signals correctly. In practice this is the "
          "theorem you will use most often at a whiteboard.")]], h=548640)
    y = d.image(s, y + 45720, "demorgan", 2926080)
    y = d.card(s, y + 91440, "Proof by perfect induction (exhaustive truth table)",
               [[R("A=0 B=0 → (A·B)' = 1, A'+B' = 1+1 = 1  ✓        "
                   "A=0 B=1 → (A·B)' = 1, A'+B' = 1+0 = 1  ✓", s=10.5, f=MONO_FONT)],
                [R("A=1 B=0 → (A·B)' = 1, A'+B' = 0+1 = 1  ✓        "
                   "A=1 B=1 → (A·B)' = 0, A'+B' = 0+0 = 0  ✓", s=10.5, f=MONO_FONT)],
                [R("All four rows agree, so the two expressions are the same function. "
                   "The theorem generalises to n variables: (ABC…)' = A'+B'+C'+…", s=10.5, i=True, c=SLATE)]],
               accent=TEAL, h=1005840)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Active-low reading: ", b=True, c=RED, s=11),
        R("a signal named  rst_n  asserted low means 'reset when rst_n = 0'. "
          "De Morgan is how you convert a spec written in active-low language into positive logic without errors.",
          s=11)]])

    # ================================================================ tiered 3A
    s = d.slide("TOPIC 3A · TIERED DEPTH", "Understanding Boolean Algebra at Four Levels")
    y = d.lead(s, TOP, [[
        R("The same idea, deepened. Use the level that matches your audience — and make sure you can "
          "climb all four.", s=12)]], h=365760)
    d.tiers(s, y + G, [
        ("BASIC", "Circuits work with just two values, 0 and 1. Three operations — AND, OR and NOT — "
                  "combine them, and a truth table lists what comes out for every possible input.", TEAL),
        ("INTERMEDIATE", "Boolean algebra is a formal algebra with its own laws. Those laws let you rewrite "
                         "an expression into an equivalent one that needs fewer gates — which is exactly "
                         "what minimisation means.", TEAL),
        ("ADVANCED", "Any function has canonical SOP and POS forms derived directly from its truth table. "
                     "Minimisation (K-map, Quine–McCluskey, Espresso) finds a cover of prime implicants "
                     "that is cheapest under a chosen cost model — literals, gates, or area.", AMBER),
        ("INDUSTRY", "Nobody minimises by hand at scale. Synthesis uses BDDs, AIGs and SAT-based "
                     "rewriting (ABC) against a real standard-cell library, optimising area, timing and "
                     "power together. Your job is to write clean RTL, set correct constraints, and read "
                     "the report critically.", GREEN)],
        h=914400, gap=68580)

    # ================================================================ worked example 1
    s = d.slide("TOPIC 3A · PRACTICAL EXAMPLE 1", "Worked: Algebraic Simplification, Step by Step", GREEN)
    y = d.lead(s, TOP, [[
        R("Problem. ", b=True, c=NAVY, s=12.5),
        R("Simplify  F = A·B·C + A·B·C' + A·B'·C + A'·B·C  and state how many gates you saved.", s=12.5)]],
        h=411480)
    y = d.code(s, y + G, [
        "F = ABC + ABC' + AB'C + A'BC",
        "",
        "  = AB(C + C')  + AB'C + A'BC        group terms 1 and 2  (distributive)",
        "  = AB(1)       + AB'C + A'BC        complement:  C + C' = 1",
        "  = AB          + AB'C + A'BC        identity:    X · 1  = X",
        "",
        "  = A(B + B'C)  + A'BC               factor A out of terms 1 and 2",
        "  = A(B + C)    + A'BC               simplification:  B + B'C = B + C",
        "  = AB + AC     + A'BC               expand",
        "",
        "  = AB + A'BC   + AC                 reorder",
        "  = B(A + A'C)  + AC                 factor B",
        "  = B(A + C)    + AC                 simplification again",
        "  = AB + BC     + AC",
        "",
        "F = AB + BC + AC        ←  the 'majority' function: 1 when ≥ 2 inputs are 1",
    ], size=10, title="Each line names the law that justifies it — never skip that column",
        accent=GREEN)
    d.cols(s, y + G, [
        ("Cost before", [[R("4 AND gates (3-input)", s=10.5)], [R("1 OR gate (4-input)", s=10.5)],
                         [R("3 inverters · 12 literals", b=True, c=RED, s=10.5)]], RED, CARD_R),
        ("Cost after", [[R("3 AND gates (2-input)", s=10.5)], [R("1 OR gate (3-input)", s=10.5)],
                        [R("0 inverters · 6 literals", b=True, c=GREEN, s=10.5)]], GREEN, CARD_G),
        ("Sanity check", [[R("Build the truth table for both forms and compare all 8 rows. "
                             "Never trust an algebraic simplification you have not checked.",
                             s=10.5)]], AMBER, CARD_A)], h=1051560)

    # ================================================================ canonical forms
    s = d.slide("TOPIC 3A · CANONICAL FORMS", "SOP and POS — Reading Algebra Straight Off a Truth Table")
    y = d.lead(s, TOP, [[
        R("Given any truth table you can write down two exact expressions immediately, with no thinking "
          "required. ", b=True, c=NAVY, s=12.5),
        R("They are called canonical because they are unique. They are also usually far from minimal — "
          "which is what the next two slides fix.")]], h=502920)
    y = d.image(s, y + 45720, "sop_pos", 3383280)
    d.cols(s, y + 91440, [
        ("Minterm  mᵢ", [[R("The AND term that is 1 for exactly ONE input combination. "
                            "Write the variable plain if its bit is 1, complemented if 0.", s=10.5)]],
         GREEN, CARD_G),
        ("Maxterm  Mᵢ", [[R("The OR term that is 0 for exactly ONE input combination — the complement "
                            "rule is reversed.", s=10.5)]], AMBER, CARD_A),
        ("Relationship", [[R("Mᵢ = (mᵢ)'.  A function's SOP minterm list and POS maxterm list are "
                             "complementary sets of the same 2ⁿ indices.", s=10.5)]], TEAL, CARD)],
        h=1005840)

    # ================================================================ K-map method
    s = d.slide("TOPIC 3A · MINIMISATION", "Karnaugh Maps — Minimisation You Can Do by Eye")
    y = d.lead(s, TOP, [[
        R("A K-map is a truth table redrawn so that physically adjacent cells differ in exactly one "
          "variable. ", b=True, c=NAVY, s=12.5),
        R("That turns the algebraic law  X·Y + X·Y' = X  into a visual one: any group of adjacent 1s "
          "collapses into a single, shorter product term. Practical up to 4 variables (5–6 with effort).")]],
        h=548640)
    y = d.image(s, y + 45720, "kmap_method", 3840480)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Vocabulary: ", b=True, c=NAVY, s=11),
        R("an ", s=11), R("implicant", b=True, c=TEAL, s=11), R(" is any legal group; a ", s=11),
        R("prime implicant", b=True, c=TEAL, s=11),
        R(" is one that cannot be made larger; an ", s=11),
        R("essential prime implicant", b=True, c=AMBER, s=11),
        R(" is the only group covering some particular 1 — it must appear in every minimal solution.", s=11)]])

    # ================================================================ K-map worked
    s = d.slide("TOPIC 3A · WORKED EXAMPLE", "A 4-Variable K-Map with Don't-Cares", GREEN)
    y = d.lead(s, TOP, [[
        R("Don't-cares (X) are input combinations that can never occur, or whose output nobody reads. ",
          b=True, c=NAVY, s=12.5),
        R("You may assign each one 0 or 1 — whichever makes your groups bigger. They are free "
          "optimisation, and forgetting to declare them is a common source of oversized logic.")]], h=548640)
    y = d.image(s, y + 45720, "kmap_worked", 3337560)
    d.card(s, y + 91440, "The procedure, in the order you should always follow it",
           [[R("1. Fill the map from the truth table.   2. Circle every ESSENTIAL prime implicant first.   "
               "3. Cover the remaining 1s with the fewest, largest groups.   "
               "4. Read each group as a product term: keep the variables that stay constant, drop those "
               "that change.   5. OR the terms together.   6. Verify against the original truth table.")]],
           accent=TEAL, h=1051560)

    # ================================================================ gate cost
    s = d.slide("TOPIC 3A · PRACTICAL EXAMPLE 2", "Numerical: What Minimisation Buys You in Silicon", GREEN)
    y = d.image(s, TOP, "gate_cost", 3383280)
    y = d.card(s, y + 91440, "Work it through with real numbers",
               [[R("Assume a 28 nm library where 1 gate-equivalent (GE) ≈ 0.5 µm² and a 2-input gate "
                   "switching at 500 MHz burns ≈ 0.6 µW.")],
                [R("Before: ", b=True, c=RED),
                 R("12 GE → 6.0 µm², ≈ 7.2 µW.        "),
                 R("After: ", b=True, c=GREEN),
                 R("5 GE → 2.5 µm², ≈ 3.0 µW.        "),
                 R("Saving: 58 % area and power.", b=True, c=NAVY)],
                [R("Now multiply by 200 000 instances of this block on a real SoC: 0.7 mm² of die and "
                   "0.84 W of dynamic power. That is the difference between a product that ships and one "
                   "that does not.", i=True, c=SLATE)]],
               accent=GREEN, fill=CARD_G, h=1234440)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Numbers are illustrative, chosen to show the method — always use your own library's datasheet. ",
          s=10.5, i=True, c=SLATE)]])

    # ================================================================ beyond k-maps
    s = d.slide("TOPIC 3A · SCALING UP", "Beyond K-Maps — What Real Tools Do")
    y = d.lead(s, TOP, [[
        R("K-maps stop working past about 5 variables, and real blocks have hundreds of inputs. ",
          b=True, c=NAVY, s=12.5),
        R("The algorithms below do the same job systematically. You will not implement them, but you "
          "must know their names and limits because they appear in every synthesis log.")]], h=548640)
    y = d.table(s, y + G, ["Method", "How it works", "Scales to", "Where you meet it"],
                [["Karnaugh map", "visual grouping on a Gray-coded grid", "≤ 5–6 vars", "exams, whiteboards, intuition"],
                 ["Quine–McCluskey", "tabular; finds ALL prime implicants, then solves a covering problem",
                  "≤ ~15 vars", "the exact algorithm K-maps approximate"],
                 ["Espresso", "heuristic expand / reduce / irredundant loop — near-optimal, very fast",
                  "hundreds", "classic two-level logic minimiser"],
                 ["ABC / AIG rewriting", "multi-level: And-Inverter Graphs, cut rewriting, SAT sweeping",
                  "millions", "inside Yosys and every commercial tool"],
                 ["BDD", "canonical decision-diagram form of the function", "varies wildly",
                  "equivalence checking, formal verification"]],
                [2011680, 4023360, 1554480, 3657600], rh=457200, bold_cols=(0,),
                col_colors={0: TEAL}, size=10)
    d.card(s, y + G, "So why learn K-maps at all?",
           [[R("Because you must be able to read what the tool produced and decide whether it is right. "
               "A synthesis report showing 4 000 gates for a function you know needs 40 means your RTL is "
               "wrong — an unintended latch, a runaway loop, or a missing don't-care. "
               "Minimisation intuition is your only defence against silently accepting bad hardware.")]],
           accent=AMBER, fill=CARD_A, h=1188720)

    # =============================================== SECTION 3B divider
    d.section_slide("SUBTOPIC 3B", "Combinational Logic Design",
                    "Circuits with no memory — the output is a pure function of the inputs, right now.",
                    ["The defining property, and the seven-step design procedure",
                     "The standard building blocks: adders, MUX, decoders, comparators, ALUs",
                     "What limits them: propagation delay, fan-in, fan-out and hazards",
                     "How they are written in Verilog — and the inferred-latch trap"], accent=TEAL)

    # ================================================================ comb vs seq
    s = d.slide("TOPIC 3B · DEFINITION", "Combinational vs Sequential — The Only Real Difference")
    y = d.lead(s, TOP, [[
        R("One structural feature separates the two families: ", b=True, c=NAVY, s=12.5),
        R("a feedback path through a storage element. Everything else — that sequential circuits have "
          "memory, need a clock, and are analysed with state diagrams — follows from that one fact.")]],
        h=502920)
    y = d.image(s, y + 45720, "comb_vs_seq", 3657600)
    d.card(s, y + 91440, "The formal definitions, worth memorising verbatim",
           [[R("Combinational: ", b=True, c=TEAL),
             R("the output at any instant depends ONLY on the inputs at that instant "
               "(after a bounded settling delay).  ")],
            [R("Sequential: ", b=True, c=AMBER),
             R("the output depends on the present inputs AND on the sequence of past inputs, "
               "summarised in a finite amount of stored STATE.")]],
           accent=TEAL, h=822960)

    # ================================================================ design procedure
    s = d.slide("TOPIC 3B · PROCEDURE", "The Seven-Step Combinational Design Procedure")
    y = d.lead(s, TOP, [[
        R("Follow this every time, even when the answer looks obvious. ", b=True, c=NAVY, s=12.5),
        R("Most combinational bugs come from an incomplete truth table at step 3 — a missing row, or a "
          "case nobody thought about.")]], h=457200)
    y = d.image(s, y + G, "comb_design_flow", 3200400)
    d.cols(s, y + 91440, [
        ("Worked micro-example — steps 1 to 3",
         [[R("1. 'Light a warning LED when at least two of three sensors read high.'", s=10.5)],
          [R("2. Inputs A, B, C (1 bit each); output W (1 bit).", s=10.5)],
          [R("3. Truth table: W = 1 for ABC = 011, 101, 110, 111 — four of the eight rows.", s=10.5)]],
         TEAL, CARD),
        ("Steps 4 to 7",
         [[R("4. W = A'BC + AB'C + ABC' + ABC   (canonical SOP)", s=10.5)],
          [R("5. K-map → W = AB + BC + AC   — the majority function again.", s=10.5)],
          [R("6. Three 2-input ANDs into one 3-input OR.   7. Simulate all 8 input cases.", s=10.5)]],
         GREEN, CARD_G)], h=1234440)

    # ================================================================ tiered 3B
    s = d.slide("TOPIC 3B · TIERED DEPTH", "Understanding Combinational Logic at Four Levels")
    y = d.lead(s, TOP, [[
        R("The same idea at four depths — pick the one that fits the room.", s=12)]], h=365760)
    d.tiers(s, y + G, [
        ("BASIC", "A circuit with no memory. Change the inputs and, after a short delay, the outputs "
                  "follow. Ask it the same question twice and you always get the same answer.", TEAL),
        ("INTERMEDIATE", "Built entirely from gates in an acyclic network. Fully described by a truth "
                         "table. Standard blocks — adders, multiplexers, decoders, comparators — are "
                         "reusable, well-understood patterns.", TEAL),
        ("ADVANCED", "Its speed is set by the critical path: the slowest input-to-output route, measured "
                     "as a sum of gate delays plus wire RC. Multiple unequal paths to one output create "
                     "hazards (glitches) even when the logic is correct.", AMBER),
        ("INDUSTRY", "Written as `assign` or `always @(*)` in RTL and left to synthesis, which restructures, "
                     "resizes, buffers and technology-maps it against a timing constraint. Arithmetic is "
                     "usually mapped to hand-tuned carry-lookahead or Wallace-tree macros, not to your "
                     "literal gates.", GREEN)],
        h=914400, gap=68580)

    # ================================================================ adders
    s = d.slide("TOPIC 3B · ARITHMETIC", "Half Adder and Full Adder")
    y = d.lead(s, TOP, [[
        R("Binary addition is the most-used combinational function on any chip. ", b=True, c=NAVY, s=12.5),
        R("It is built from one tiny cell — the full adder — repeated once per bit. Derive it once and "
          "you understand every adder, subtractor, multiplier and ALU that follows.")]], h=502920)
    y = d.image(s, y + 45720, "adders", 3840480)
    d.card(s, y + 91440, "Subtraction comes free",
           [[R("A − B  =  A + (−B)  =  A + B' + 1. Feed B through XOR gates controlled by a  sub  signal "
               "(XOR with 1 inverts, XOR with 0 passes through) and tie that same  sub  to Cᵢₙ. "
               "One adder now does both operations — this is exactly the ADDER / SUBTRACTOR block "
               "in the ALU slide.")]],
           accent=AMBER, fill=CARD_A, h=776224)

    # ================================================================ ripple adder
    s = d.slide("TOPIC 3B · THE CARRY PROBLEM", "4-Bit Ripple-Carry Adder — Correct but Slow", RED)
    y = d.lead(s, TOP, [[
        R("Chain n full adders and you have an n-bit adder. ", b=True, c=NAVY, s=12.5),
        R("It is minimal in area and trivially correct — and its delay grows linearly with n, which makes "
          "it the classic critical path in any first-attempt design.")]], h=502920)
    y = d.image(s, y + 45720, "ripple_adder", 3200400)
    d.cols(s, y + 91440, [
        ("Generate and Propagate",
         [[R("Gᵢ = AᵢBᵢ  — this bit generates a carry regardless of Cᵢₙ.", s=10.5)],
          [R("Pᵢ = Aᵢ ⊕ Bᵢ — this bit propagates an incoming carry.", s=10.5)],
          [R("Cᵢ₊₁ = Gᵢ + PᵢCᵢ", s=10.5, b=True, c=NAVY)]], TEAL, CARD),
        ("Carry-lookahead",
         [[R("Expand the recursion so every carry is a function of G/P only:", s=10.5)],
          [R("C₂ = G₁ + P₁G₀ + P₁P₀C₀ …", s=10.5, f=MONO_FONT)],
          [R("Delay ∝ log n instead of n — at the cost of much more area.", s=10.5)]], GREEN, CARD_G),
        ("Others you will meet",
         [[R("Carry-select, carry-skip, Brent–Kung, Kogge–Stone prefix adders.", s=10.5)],
          [R("Synthesis picks one for you from a `+` in Verilog, guided by your timing constraint.",
             s=10.5)]], AMBER, CARD_A)], h=1417320)

    # ================================================================ practical example 3
    s = d.slide("TOPIC 3B · PRACTICAL EXAMPLE 3", "Numerical: Critical Path and fₘₐₓ of a Ripple Adder", GREEN)
    y = d.card(s, TOP, "Given",
               [[R("A 4-bit ripple-carry adder built from full adders in a library where: "
                   "carry-in to carry-out delay t_c = 90 ps, carry-in to sum delay t_s = 120 ps, "
                   "and the input operands are driven by registers with t_cq = 60 ps into registers "
                   "needing t_setup = 50 ps.")]],
               accent=TEAL, h=822960)
    y = d.code(s, y + G, [
        "Step 1  Identify the critical path.",
        "        It runs A0/B0 -> C1 -> C2 -> C3 -> S3  (the last SUM, not the last carry).",
        "",
        "Step 2  Count the stages on that path.",
        "        3 carry hops (FA0, FA1, FA2)  +  1 final sum (FA3)",
        "        t_adder = 3 x t_c + t_s = 3 x 90 + 120 = 270 + 120 = 390 ps",
        "",
        "Step 3  Add the register overhead to get the clock period.",
        "        T_clk >= t_cq + t_adder + t_setup",
        "               = 60 + 390 + 50 = 500 ps",
        "",
        "Step 4  f_max = 1 / T_clk = 1 / 500 ps = 2.0 GHz",
        "",
        "Step 5  Generalise to n bits:  t_adder = (n-1) x t_c + t_s",
        "        n = 32  ->  31 x 90 + 120 = 2910 ps  ->  T_clk = 3020 ps  ->  f_max = 331 MHz",
    ], size=10, title="Answer the question in five steps — always state the path first", accent=GREEN)
    d.card(s, y + G, "The lesson",
           [[R("The 4-bit adder runs at 2 GHz; the same design at 32 bits collapses to 331 MHz. "),
             R("Delay is linear in n, so frequency is roughly inverse-linear. ", b=True, c=RED),
             R("This is precisely the calculation that forces a designer to move from ripple-carry to "
               "carry-lookahead, or to pipeline the adder across two clock cycles.")]],
           accent=RED, fill=CARD_R, h=868680)

    # ================================================================ mux
    s = d.slide("TOPIC 3B · DATA ROUTING", "Multiplexers and De-multiplexers")
    y = d.lead(s, TOP, [[
        R("A multiplexer is a controllable switch: n select lines choose one of 2ⁿ data inputs to appear "
          "at the output. ", b=True, c=NAVY, s=12.5),
        R("It is the single most common structure in real hardware — every  if,  every  case,  every "
          "shared bus and every ALU function select becomes a MUX after synthesis.")]], h=548640)
    y = d.image(s, y + 45720, "mux_demux", 3383280)
    d.cols(s, y + 91440, [
        ("In Verilog, all of these are MUXes",
         [[R("assign y = sel ? a : b;", s=10, f=MONO_FONT)],
          [R("if (sel) y = a; else y = b;", s=10, f=MONO_FONT)],
          [R("case (sel) 2'b00: y = i0; ...", s=10, f=MONO_FONT)]], TEAL, CARD),
        ("Why the size matters",
         [[R("A 2ⁿ:1 MUX on an m-bit bus costs roughly 2ⁿ × m AND-OR pairs. A careless 16-way case on a "
             "32-bit bus is 512 gates — and its delay grows with the number of select levels.", s=10.5)]],
         AMBER, CARD_A)], h=1097280)

    # ================================================================ mux universal
    s = d.slide("TOPIC 3B · A USEFUL TRICK", "The Multiplexer as a Universal Logic Element")
    y = d.lead(s, TOP, [[
        R("A 2ⁿ:1 MUX can implement ANY function of n variables ", b=True, c=NAVY, s=12.5),
        R("— just wire the truth-table output column to the data inputs and the variables to the select "
          "lines. This is not a curiosity: it is exactly how an FPGA look-up table (LUT) works.")]], h=548640)
    y = d.cols(s, y + G, [
        ("The construction",
         [[R("Target: F(A,B,C) = Σm(1,3,5,6).", s=10.5)],
          [R("Use an 8:1 MUX with S₂S₁S₀ = A,B,C.", s=10.5)],
          [R("Tie I₁ = I₃ = I₅ = I₆ = 1 and every other data input to 0.", s=10.5)],
          [R("Done — no minimisation needed at all.", b=True, c=GREEN, s=10.5)]], TEAL, CARD),
        ("Halving the MUX",
         [[R("A 4:1 MUX also suffices: use A,B as select and feed each data input with one of "
             "0, 1, C or C'.", s=10.5)],
          [R("Read pairs of truth-table rows: 00 → C, 01 → C, 10 → C, 11 → C'.", s=10.5)],
          [R("In general an n-variable function needs only a 2ⁿ⁻¹:1 MUX.", s=10.5)]], GREEN, CARD_G),
        ("Why FPGAs are built this way",
         [[R("An FPGA logic cell is a small SRAM (typically a 6-input LUT = a 64:1 MUX with "
             "programmable data bits) plus a flip-flop.", s=10.5)],
          [R("Programming an FPGA literally means writing truth tables into those SRAM cells.",
             s=10.5, b=True, c=AMBER)]], AMBER, CARD_A)], h=2194560)
    d.card(s, y + 137160, "Consequence for your RTL",
           [[R("On an FPGA, a 6-input function and a 2-input function cost the SAME single LUT. "
               "Deliberately splitting logic into tiny pieces therefore buys you nothing and can cost "
               "you levels of delay. On an ASIC the opposite is true. "),
             R("Know your target before you optimise.", b=True, c=NAVY)]],
           accent=TEAL, h=960120)

    # ================================================================ decoders
    s = d.slide("TOPIC 3B · CODE CONVERSION", "Decoders, Encoders and Priority Encoders")
    y = d.lead(s, TOP, [[
        R("A decoder turns a compact binary code into one-hot select lines; an encoder does the reverse. ",
          b=True, c=NAVY, s=12.5),
        R("Address decode, instruction decode, chip-select generation and interrupt arbitration are all "
          "this one pattern.")]], h=502920)
    y = d.image(s, y + 45720, "decoder_encoder", 3566160)
    d.cols(s, y + 91440, [
        ("Enable inputs", [[R("Real decoders have an EN pin: when EN = 0 every output is inactive. "
                              "This is how several decoders are cascaded to build a larger one "
                              "(two 2:4 + one 1:2 = a 3:8 decoder).", s=10.5)]], TEAL, CARD),
        ("Why plain encoders are broken",
         [[R("A plain 4:2 encoder assumes exactly one input is high. If two are, it outputs the OR of "
             "their codes — a value that is simply wrong. A PRIORITY encoder resolves this, and the "
             "V (valid) output distinguishes 'input 0 active' from 'nothing active'.", s=10.5)]],
         RED, CARD_R)], h=1005840)

    # ================================================================ comparators / parity
    s = d.slide("TOPIC 3B · MORE BLOCKS", "Comparators, Parity and Other Standard Cells")
    y = d.image(s, TOP, "comparator_parity", 3383280)
    y = d.cols(s, y + 91440, [
        ("Comparator — building it up",
         [[R("1-bit equal:  e = (A ⊕ B)'", s=10.5, f=MONO_FONT)],
          [R("n-bit equal:  AND all n of those", s=10.5, f=MONO_FONT)],
          [R("Greater-than works MSB-first: A > B if the highest bit where they differ has A = 1. "
             "In Verilog this is just `A > B` and synthesis builds the ripple for you.", s=10.5)]],
         TEAL, CARD),
        ("Parity — one XOR tree",
         [[R("Even parity bit P = XOR of all data bits.", s=10.5)],
          [R("Detects ANY odd number of bit flips, but cannot correct and misses even ones. "
             "For real protection use Hamming or ECC — the same XOR-tree idea, more bits.", s=10.5)]],
         GREEN, CARD_G),
        ("Also in every library",
         [[R("· Barrel shifter (a MUX per output bit)", s=10.5)],
          [R("· Priority arbiter", s=10.5)],
          [R("· Binary ↔ Gray converter", s=10.5)],
          [R("· Leading-zero counter", s=10.5)]], AMBER, CARD_A)], h=1737360)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Trainer note: ", b=True, c=SLATE, s=10.5),
        R("ask the class to derive the 1-bit equality gate before you show it — XNOR-as-equality is the "
          "single most useful gate identity in this whole topic.", s=10.5, i=True)]])

    # ================================================================ ALU
    s = d.slide("TOPIC 3B · PUTTING BLOCKS TOGETHER", "An Arithmetic Logic Unit Is Just a MUX of Blocks")
    y = d.lead(s, TOP, [[
        R("An ALU looks intimidating and is structurally trivial: ", b=True, c=NAVY, s=12.5),
        R("run every operation in parallel on the same operands and use the opcode to select which "
          "answer leaves the block. It wastes power computing results you throw away — and it is fast, "
          "regular and easy to verify, which usually wins.")]], h=548640)
    y = d.image(s, y + 45720, "alu_block", 3200400)
    d.card(s, y + 91440, "The status flags — and the mistake everyone makes with V",
           [[R("Z ", b=True, c=RED), R("= result is all zeros (a NOR of every result bit).    "),
             R("N ", b=True, c=RED), R("= MSB of the result (the sign bit in two's complement).    "),
             R("C ", b=True, c=RED), R("= carry out of the MSB — meaningful for UNSIGNED overflow.")],
            [R("V ", b=True, c=RED),
             R("= SIGNED overflow, and it is NOT the same as C. V = Cₙ ⊕ Cₙ₋₁ : the carry INTO the sign "
               "bit differs from the carry OUT of it. Adding two positives and getting a negative is the "
               "classic case.")]],
           accent=RED, fill=CARD_R, h=1280160)

    # ================================================================ hazards
    s = d.slide("TOPIC 3B · HAZARDS", "Glitches — When Correct Logic Produces a Wrong Pulse", RED)
    y = d.lead(s, TOP, [[
        R("A hazard is a momentary wrong output caused purely by unequal path delays. ",
          b=True, c=NAVY, s=12.5),
        R("The steady-state logic is perfectly correct; the transient is not. Understanding this is what "
          "makes the case for synchronous design.")]], h=502920)
    y = d.image(s, y + 45720, "hazards", 3337560)
    d.card(s, y + 91440, "Where a glitch is harmless — and where it kills the chip",
           [[R("Harmless: ", b=True, c=GREEN),
             R("feeding the D input of a flip-flop, provided it settles before the next clock edge. "
               "This is the normal case and why we design synchronously.")],
            [R("Fatal: ", b=True, c=RED),
             R("on a clock line, a reset line, an asynchronous set/clear, a write-enable to memory, or "
               "any signal leaving the chip. Never generate a clock from combinational logic.")]],
           accent=RED, fill=CARD_R, h=1097280)

    # ================================================================ delay / fanout
    s = d.slide("TOPIC 3B · WHAT LIMITS SPEED", "Propagation Delay, Fan-In and Fan-Out")
    y = d.image(s, TOP, "delay_fanout", 3383280)
    y = d.cols(s, y + 91440, [
        ("Terms",
         [[R("t_pd ", b=True, c=NAVY, s=10.5), R("propagation delay of one gate", s=10.5)],
          [R("Fan-in ", b=True, c=NAVY, s=10.5), R("inputs on one gate", s=10.5)],
          [R("Fan-out ", b=True, c=NAVY, s=10.5), R("loads driven by one output", s=10.5)],
          [R("Critical path ", b=True, c=NAVY, s=10.5), R("slowest route through the block", s=10.5)]],
         TEAL, CARD),
        ("Why fan-out costs time",
         [[R("Each load adds gate capacitance. Charging more capacitance through the same driver "
             "resistance takes longer — delay rises roughly linearly with load.", s=10.5)],
          [R("Fix: insert buffers, or size the driver up.", s=10.5, b=True, c=GREEN)]], AMBER, CARD_A),
        ("Why fan-in costs time",
         [[R("A CMOS gate stacks transistors in series per input, so a 6-input NAND is far slower than "
             "a tree of 2-input NANDs.", s=10.5)],
          [R("Fix: let synthesis restructure — or write balanced expressions yourself.",
             s=10.5, b=True, c=GREEN)]], GREEN, CARD_G)], h=1600200)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Static timing analysis (STA), covered in Topic 6, is nothing more than this arithmetic done "
          "automatically over every path in the design.", s=10.5, i=True, c=SLATE)]])

    # ================================================================ verilog comb
    s = d.slide("TOPIC 3B · IN VERILOG", "Writing Combinational Logic — and the Inferred-Latch Trap", RED)
    y = d.lead(s, TOP, [[
        R("Three ways to write pure combinational logic, and one way to get it catastrophically wrong.",
          b=True, c=NAVY, s=12.5)]], h=365760)
    y = d.code(s, y + G, [
        "// 1. Continuous assignment - always safe, always combinational",
        "assign y = (a & b) | (~a & c);",
        "",
        "// 2. always @(*) with BLOCKING assignments (=) and a DEFAULT",
        "always @(*) begin",
        "    y = 1'b0;                 // <-- default first: kills every latch",
        "    case (sel)",
        "        2'b00: y = i0;",
        "        2'b01: y = i1;",
        "        default: y = 1'b0;",
        "    endcase",
        "end",
        "",
        "// 3. WRONG - incomplete assignment infers a transparent LATCH",
        "always @(*) begin",
        "    if (enable) y = d;        // no else -> 'hold y' -> latch",
        "end",
    ], size=8.6, title="Combinational always blocks: blocking assignments, complete assignment",
        accent=RED)
    d.cols(s, y + G, [
        ("The three rules",
         [[R("1. Use  =  (blocking) in combinational blocks, never  <=.", s=10.5)],
          [R("2. Assign every output on every path — a default at the top is the easiest way.", s=10.5)],
          [R("3. Use  always @(*)  never a hand-written sensitivity list.", s=10.5)]], TEAL, CARD),
        ("How to catch it",
         [[R("Yosys prints:  $_DLATCH_  cells in the statistics.", s=10.5, f=MONO_FONT)],
          [R("Commercial tools warn 'inferred latch for signal y'.", s=10.5)],
          [R("Treat every such warning as an ERROR. There is no case in this course where you want an "
             "unintended latch.", s=10.5, b=True, c=RED)]], RED, CARD_R)], h=1280160)
