# -*- coding: utf-8 -*-
"""Module 2 Topic 2 deck — front matter, outcomes, Theory 1 (what RTL is)."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.title_slide(
        "MODULE 2 · TOPIC 2",
        "RTL Design Methodology",
        "Basics of register transfer level (RTL) design  ·  Overview of the RTL "
        "design process and methodology  ·  Introduction to hardware description "
        "languages such as Verilog or VHDL",
        ["Theory 1 · What RTL is — the two kinds of logic, the synchronous "
         "discipline, four levels of abstraction",
         "Theory 2 · The methodology — the flow, the synthesisable subset, the "
         "rules, and coding style",
         "Theory 3 · The patterns — datapath and controller, state machines, "
         "parameters and generate",
         "Theory 4 · HDLs — what one is, and Verilog against VHDL",
         "Practical · Labs A–N · 26 hours · 103 exercises · every number measured"])

    # ==================================================== terminal outcomes
    s = d.slide("MODULE 2 · NOS NIE/ELE/N0102", "Terminal Outcomes")
    y = d.image(s, TOP - 45720, "terminal_outcomes", 4389120)
    d.card(s, y + G, "Outcome 2 names this subtopic in the NOS itself",
           [[R("\"Level of abstraction in Verilog programming\" is the phrase. This "
               "session takes one circuit down all four levels, simulates them "
               "together, and proves they are the same — which is the deliverable "
               "the outcome asks for.", s=10.5)]],
           accent=NAVY, h=868680)

    s = d.slide("MODULE 2 · TOPIC 2", "Key Learning Outcomes", accent=GREEN)
    y = d.image(s, TOP - 45720, "learning_outcomes", 4389120)
    d.lead(s, y + G, [[R("Every outcome is assessed by a command you run, not by "
                         "something you recite.", b=True, c=GREEN, s=11)]],
           h=365760)

    s = d.slide("TOPIC 2 · COVERAGE", "Every Syllabus Phrase, and Where It Is Covered")
    y = d.image(s, TOP - 45720, "syllabus_map", 4389120)
    d.card(s, y + G, "On the four notional hours",
           [[R("Four hours is enough to define the terms. It is not enough to make "
               "anyone believe them — and nothing in this subtopic is believed until "
               "it has been seen to happen. Lecture from the summary slides to fit "
               "four hours; run the lab alongside to teach it.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=868680)

    s = d.slide("TOPIC 2 · STRUCTURE", "How This Session Runs")
    y = d.image(s, TOP - 45720, "topic_structure", 4480560)
    d.lead(s, y + G, [[R("RTL is not a language and it is not a tool. It is a way of "
                         "thinking about hardware.", b=True, c=NAVY, s=11)]],
           h=274320)

    # ===================================================== section THEORY 1
    d.section_slide(
        "THEORY 1", "What RTL Is",
        "The name is the definition, and almost everything else in this topic "
        "is a consequence of it.",
        ["Registers, and what transfers into them on each clock edge",
         "Why <= and = are not interchangeable",
         "Four levels of abstraction, one circuit",
         "And what a synthesiser makes of each level"])

    # --------------------------------------------------------- definition
    s = d.slide("1.1 · THE DEFINITION", "Register Transfer Level: the Name Is the "
                                        "Definition")
    y = d.image(s, TOP - 45720, "rtl_definition", 4297680)
    d.card(s, y + G, "Two statements, and nothing else",
           [[R("1.  Which registers exist.    2.  What transfers into each one, on "
               "each clock edge.")],
            [R("How many gates, which gates, how they are wired, how fast they are — "
               "none of that is in the description. You state the transfers; "
               "synthesis works out the circuit.", b=True, c=NAVY)]],
           accent=NAVY, h=868680)

    s = d.slide("1.1 · THE DEFINITION", "Watch One Value Transfer")
    y = d.image(s, TOP - 45720, "rtl_transfer_trace", 4389120)
    d.lead(s, y + G, [[R("A single 5 applied on cycle 0. It reaches x, then y as 6, "
                         "then z as 12, then acc — one register per clock edge, and "
                         "nothing moves in between.", s=10.5)]], h=365760)

    # --------------------------------------------- the two kinds of logic
    s = d.slide("1.2 · THE TWO KINDS", "Combinational and Sequential")
    y = d.image(s, TOP - 45720, "comb_vs_seq", 4754880)
    d.lead(s, y + G, [[R("There is no third kind. Every block in this course is an "
                         "arrangement of these two.", b=True, c=NAVY, s=10.5)]],
           h=274320)

    s = d.slide("1.2 · THE TWO KINDS", "The Same Distinction, In Code")
    y = d.cols(s, TOP, [
        ("COMBINATIONAL",
         [[R("always @(*)  or  assign", b=True, c=TEAL, s=10.5)],
          [R("Blocking assignment. Every output written on every path, or the "
             "tool builds a latch you did not ask for.")],
          [R("No clock appears anywhere in the block.")],
          [R("Checked by: simulation, lint.", b=True, c=NAVY)]], TEAL, CARD),
        ("SEQUENTIAL",
         [[R("always @(posedge clk)", b=True, c=VIOLET, s=10.5)],
          [R("Non-blocking assignment. Reset appears here and only here.")],
          [R("One value remembered per flip-flop, updated on the edge and at no "
             "other time.")],
          [R("Checked by: simulation, lint, and static timing analysis.",
             b=True, c=NAVY)]], VIOLET, CARD)],
        h=2286000)

    d.card(s, y + G, "Why the two are kept in separate always blocks",
           [[R("A block that mixes them has to be read twice — once for what it "
               "computes and once for when. Splitting them means each block has "
               "one job, and the reviewer, the linter and the synthesiser all "
               "agree about which job it is.")]],
           accent=GREEN, fill=CARD_G, h=868680)

    # -------------------------------------------------- synchronous design
    s = d.slide("1.3 · THE DISCIPLINE", "One Clock, One Edge, Everything")
    y = d.image(s, TOP - 45720, "sync_design", 5029200)
    d.lead(s, y + G, [[R("Almost every rule in this topic is a consequence of this "
                         "one decision.", b=True, c=NAVY, s=10.5)]], h=228600)

    s = d.slide("1.3 · THE DISCIPLINE", "What the Discipline Buys You")
    y = d.tiers(s, TOP, [
        ("ANALYSABLE",
         "With one clock and one edge, timing analysis is a finite question: for "
         "every path from a flip-flop to a flip-flop, does the data arrive in "
         "time? Add a gated clock and the question multiplies.", NAVY),
        ("COMPOSABLE",
         "Two blocks written to the same discipline can be wired together "
         "without a conversation. Two blocks written to different disciplines "
         "need one, every time.", TEAL),
        ("REVIEWABLE",
         "A reviewer who knows the discipline can read your block for what it "
         "computes, because the question of WHEN has already been answered the "
         "same way it always is.", VIOLET),
        ("TESTABLE",
         "Scan insertion, the technique that makes a chip testable after "
         "manufacture, assumes edge-triggered flip-flops on one clock. Latches "
         "and gated clocks each need special handling.", GREEN)],
        h=822960)

    d.lead(s, y + G, [[R("You are allowed to break these rules. You are not allowed "
                         "to break them by accident.", b=True, c=AMBER, s=11)]],
           h=274320)

    # ------------------------------------------------------------- why RTL
    s = d.slide("1.4 · WHY", "Why Anyone Designs At This Level")
    y = d.table(s, TOP,
                ["", "Behavioural / algorithmic", "RTL", "Gate netlist"],
                [["you write", "the algorithm", "registers and transfers",
                  "every gate"],
                 ["timing", "none at all", "one clock period per stage",
                  "exact, per gate"],
                 ["synthesisable", "rarely", "yes — this is the target",
                  "yes, but why would you"],
                 ["a 10k-gate design", "unbuildable", "a few hundred lines",
                  "tens of thousands of lines"],
                 ["who writes it", "architects, in C or SystemC", "you",
                  "the synthesiser"]],
                [2194560, 2926080, 3200400, 2926080], rh=329184, bold_cols=(2,))

    y = d.card(s, y + G, "RTL is the level where the trade lands correctly",
               [[R("High enough that a human can write and read a real design; low "
                   "enough that a tool can build it without guessing at your "
                   "intent.")],
                [R("Every industrial digital design in the last thirty years was "
                   "written here. That is not fashion — it is where the abstraction "
                   "pays for itself.", b=True, c=NAVY)]],
               accent=TEAL, h=1005840)

    d.lead(s, y + G, [[R("Above RTL you cannot say when things happen. Below it you "
                         "cannot say anything else.", b=True, c=SLATE, s=10.5)]],
           h=274320)

    # ------------------------------------------------------- blocking
    s = d.slide("1.5 · <= AND =", "The Two Assignment Operators, and Why It Matters")
    y = d.image(s, TOP - 45720, "nonblocking", 4389120)
    d.lead(s, y + G, [[R("Neither one is an error. Both are caught by the linter you "
                         "build in this topic.", b=True, c=RED, s=10.5)]], h=274320)

    s = d.slide("1.5 · <= AND =", "The Swap, Worked Through")
    y = d.code(s, TOP, [
        "// NON-BLOCKING - inside always @(posedge clk)",
        "//   Step 1: read every right-hand side, using the OLD values.",
        "//   Step 2: update every left-hand side, all at the same instant.",
        "",
        "        a <= b;        //  reads old b",
        "        b <= a;        //  reads old a",
        "",
        "        a and b are SWAPPED.  This is what a hardware register does.",
        "",
        "// BLOCKING - inside always @*",
        "//   Each statement finishes before the next one starts.",
        "",
        "        a = b;         //  a is now b",
        "        b = a;         //  a is already b, so this does nothing",
        "",
        "        BOTH end up holding b.  This is what software does."],
        size=9.5)

    d.card(s, y + G, "Why the rule is absolute rather than stylistic",
           [[R("Two clocked blocks using blocking assignments can see each other's "
               "half-updated values, and which one wins depends on the order the "
               "simulator happens to evaluate them in — an order the language "
               "standard deliberately does not fix.")],
            [R("Non-blocking assignment exists precisely to make that race "
               "impossible.", b=True, c=NAVY)]],
           accent=NAVY, h=1097280)

    s = d.slide("1.5 · <= AND =", "And What Each One Actually Builds",
                accent=RED)
    y = d.image(s, TOP - 45720, "blocking_measured", 5029200)
    d.lead(s, y + G, [[R("Three flip-flops against one. Nothing illegal was "
                         "written, so nothing warned.", b=True, c=RED, s=10.5)]],
           h=228600)

    # ---------------------------------------------------------- the ladder
    s = d.slide("1.6 · ABSTRACTION", "Four Levels, One Circuit")
    y = d.image(s, TOP - 45720, "ladder", 4937760)
    d.lead(s, y + G, [[R("All four were simulated together on all 8 input patterns. "
                         "Zero mismatches.", b=True, c=GREEN, s=11)]], h=228600)

    s = d.slide("1.6 · ABSTRACTION", "The Same Adder, Written Four Ways")
    d.code(s, TOP, [
        "// BEHAVIOURAL - you describe the function",
        "always @* {cout, sum} = a + b + cin;",
        "",
        "// DATAFLOW - you describe the Boolean form",
        "assign sum  = a ^ b ^ cin;",
        "assign cout = (a & b) | (b & cin) | (a & cin);",
        "",
        "// GATE - you name every gate and every wire",
        "xor x1 (s1, a, b);      xor x2 (sum, s1, cin);",
        "and a1 (ab, a, b);      and a2 (bc, b, cin);   and a3 (ac, a, cin);",
        "or  o1 (cout, ab, bc, ac);",
        "",
        "// SWITCH - you place individual transistors",
        "pmos p1 (y, vdd, a);    nmos n1 (y, gnd, a);      // one CMOS inverter"],
        size=9.5)

    s = d.slide("1.6 · ABSTRACTION", "And What a Synthesiser Makes of Each")
    y = d.image(s, TOP - 45720, "ladder_synthesis", 4937760)
    d.lead(s, y + G, [[R("The behavioural description produced the SMALLEST circuit — "
                         "and dataflow and gate produced the identical netlist.",
                         b=True, c=AMBER, s=10.5)]], h=228600)

    s = d.slide("1.6 · ABSTRACTION", "The Rule This Gives You", accent=GREEN)
    y = d.card(s, TOP, "Write at the highest level that expresses your intent",
               [[R("Every level you descend takes a decision away from the tool and "
                   "gives it to you — whether or not you wanted it.", b=True,
                   c=NAVY, s=12)]],
               accent=GREEN, fill=CARD_G, h=685800)

    y = d.cols(s, y + G, [
        ("What the tool is better at than you",
         [[R("Choosing a gate mix for a Boolean function.")],
          [R("Balancing a logic tree.")],
          [R("Meeting a timing constraint by restructuring.")],
          [R("Doing all of that again, consistently, at 3 a.m.")]], GREEN, CARD_G),
        ("What you are better at than the tool",
         [[R("How many clock cycles the job should take.")],
          [R("Where the registers go.")],
          [R("What is shared and what is duplicated.")],
          [R("What the interface should look like.")]], AMBER, CARD_A)],
        h=2011680)

    d.lead(s, y + G, [[R("Give the tool the first list. Keep the second one for "
                         "yourself.", b=True, c=NAVY, s=11)]], h=274320)

    # ------------------------------------------------------------- proof
    s = d.slide("1.7 · PROOF", "Simulation Shows. Proof Settles.")
    y = d.image(s, TOP - 45720, "proof_vs_test", 4846320)
    d.lead(s, y + G, [[R("A checker that cannot fail is not evidence of anything — "
                         "which is why the lab includes a deliberately broken adder.",
                         b=True, c=RED, s=10.5)]], h=274320)

    # ------------------------------------------------- the running example
    s = d.slide("1.8 · THE RUNNING EXAMPLE", "One Design, Carried All the Way "
                "Through")
    y = d.image(s, TOP - 45720, "running_example", 4754880)
    d.lead(s, y + G, [[R("Four bits, an asynchronous reset, an enable and a "
                         "terminal count. Small enough to read in one glance, big "
                         "enough to be a real design.", s=10.5)]], h=274320)

    s = d.slide("1.8 · THE RUNNING EXAMPLE", "Read It Line By Line")
    y = d.code(s, TOP, [
        "module counter4 (",
        "    input            clk,",
        "    input            rst_n,      // asynchronous, active LOW",
        "    input            en,",
        "    output reg [3:0] count,",
        "    output           tc          // one cycle high at 15",
        ");",
        "    always @(posedge clk or negedge rst_n) begin",
        "        if (!rst_n)     count <= 4'd0;      // reset wins",
        "        else if (en)    count <= count + 4'd1;",
        "    end                                     // no else: HOLD",
        "",
        "    assign tc = en & (count == 4'd15);",
        "endmodule"], size=10)

    d.card(s, y + G, "Four decisions are visible in fourteen lines",
           [[R("The reset is ASYNCHRONOUS, so it is in the sensitivity list; it is "
               "ACTIVE LOW, so the port is named rst_n and the test is !rst_n. "
               "Reset is tested FIRST, so it wins over the enable. And the missing "
               "else is deliberate — in a CLOCKED block, no assignment means hold, "
               "which is what a flip-flop does anyway.")]],
           accent=NAVY, h=1097280)

    s = d.slide("1.8 · THE RUNNING EXAMPLE", "The Numbers, Worked Out")
    y = d.image(s, TOP - 45720, "numerical_example", 5029200)
    d.lead(s, y + G, [[R("Derive the formula, then measure it. A testbench that only "
                         "ever tries one value of N has told you almost nothing.",
                         b=True, c=NAVY, s=10.5)]], h=274320)

    s = d.slide("THEORY 1 · CHECKPOINT", "Nine Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What two things does an RTL description state?",
                  "which registers exist, and what transfers into them"],
                 ["2", "What does <= mean inside a clocked block?",
                  "read all right-hand sides first, then update together"],
                 ["3", "Name the four levels of abstraction.",
                  "behavioural, dataflow, gate, switch"],
                 ["4", "Which level produced the smallest netlist, and why?",
                  "behavioural — it left the tool free to choose"],
                 ["5", "Why did dataflow and gate give identical netlists?",
                  "writing the Boolean form already fixes the structure"],
                 ["6", "Why prove equivalence instead of simulating?",
                  "exhaustive simulation stops being possible at ~30 inputs"],
                 ["7", "What are the only two kinds of digital logic?",
                  "combinational and sequential — there is no third"],
                 ["8", "Name three things the synchronous discipline buys you.",
                  "analysable timing, composable blocks, testable silicon"],
                 ["9", "In counter4, why is there no else on the enable?",
                  "in a clocked block, no assignment means hold"]],
                [548640, 5029200, 5669280], rh=274320, bold_cols=(0,), size=9.2)
    d.lead(s, y + G, [[R("Theory 2 asks what you are allowed to write, and why the "
                         "rules exist.", b=True, c=GREEN, s=11)]], h=274320)
