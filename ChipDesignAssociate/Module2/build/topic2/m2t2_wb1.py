# -*- coding: utf-8 -*-
"""Module 2 Topic 2 workbook — front matter, outcomes, Theory Part 1."""
import _boot
from wbkit import *


def B(t, d=None, **kw):
    kw.update(d or {}); kw["b"] = True; return (t, kw)


def N(t, d=None, **kw):
    kw.update(d or {}); return (t, kw)


def I(t, d=None, **kw):
    kw.update(d or {}); kw["i"] = True; return (t, kw)


def M(t, d=None, **kw):
    kw.update(d or {}); kw["f"] = MONOF; return (t, kw)


def build(w):
    # ------------------------------------------------------------ cover
    w.para([N("CHIP DESIGN ASSOCIATE  ·  O-LEVEL ‘CHIP DESIGN’",
              {"b": True, "s": 12.0, "c": TEAL})], space_after=2)
    p = w.d.add_paragraph()
    r = p.add_run("Module 2 — Topic 2")
    r.font.name = HEADF; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = SLATE
    p.paragraph_format.space_after = Pt(2)
    p = w.d.add_paragraph()
    r = p.add_run("RTL Design Methodology")
    r.font.name = HEADF; r.font.size = Pt(25); r.font.bold = True; r.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(4)
    p = w.d.add_paragraph()
    r = p.add_run("Tutorial & Practice Workbook")
    r.font.name = HEADF; r.font.size = Pt(16); r.font.color.rgb = AMBER
    p.paragraph_format.space_after = Pt(10)
    w.para([N("A self-study companion to the Topic 2 slide deck. It explains every "
              "concept the deck introduces and why it exists, walks you through nine "
              "guided tutorials at the keyboard, and ends with 103 graded exercises "
              "and full worked solutions. Every number quoted here was produced by "
              "running the code in Topic2_Lab/. Nothing in this workbook requires you "
              "to look anything up elsewhere.", {"s": 11.5})])
    w.para([N("NOS: NIE/ELE/N0102  ·  Module 2 “Verilog RTL coding for Synthesis”, "
              "subtopic 2 “RTL Design Methodology”  ·  Syllabus: basics of register "
              "transfer level (RTL) design; overview of RTL design process and "
              "methodology; introduction to hardware description languages (HDLs) "
              "such as Verilog or VHDL.  Module duration: 25 h theory, 35 h "
              "practical, of which RTL Design and Implementation Labs are 40 h.",
              {"s": 9, "c": SLATE, "i": True})])

    # ------------------------------------------------- terminal outcomes
    w.h1("Terminal Outcomes")
    w.para([N("After successful completion of Module 2, the student shall be able to:",
              {"s": 11.5})])
    w.callout("Module 2 terminal outcomes (NOS NIE/ELE/N0102)", [
        [B("1.  "), N("Understand the design cycle of VLSI.")],
        [B("2.  "), N("Understand Verilog programming syntax, "),
         B("level of abstraction in Verilog programming"),
         N(", and testbench simulation.")],
        [B("3.  "), N("Design and develop IPs for VLSI using Verilog.")],
        [B("4.  "), N("Emulate, debug and characterise reusable IPs.")],
    ], color=NAVY, bar="0E2A47")

    w.para([N("Outcome 2 names this subtopic in the NOS itself. \"Level of "
              "abstraction\" is not a phrase this workbook invented to organise the "
              "material — it is the deliverable. Part 1 takes one circuit down all "
              "four levels of abstraction Verilog offers, simulates them together, "
              "and proves they are the same circuit.", {"s": 11.5})])
    w.para([N("Outcome 3 begins with knowing what is synthesisable and what is not, "
              "which is Part 2. Outcome 4 asks for reusable IP, and reuse is a set of "
              "decisions you take while writing, not a property you add afterwards — "
              "also Part 2.", {"s": 11.5})])

    # ------------------------------------------------- learning outcomes
    w.h1("Key Learning Outcomes")
    w.table(["Theory — you will be able to", "Practical — you will be able to"],
            [["Explain what register transfer level means, and the timing model it "
              "implies",
              "Write RTL code for basic digital circuits"],
             ["Describe the levels of abstraction available in an HDL, and choose "
              "between them with a reason",
              "Validate RTL designs through simulation using testbenches"],
             ["Explain how the synthesisable subset and the coding rules shape the "
              "RTL you are allowed to write",
              "Apply a coding standard and check it mechanically rather than by "
              "review"],
             ["Compare Verilog and VHDL, and read either",
              "Synthesise a design and read what the tool actually built"]],
            widths=[3.4, 3.4], size=10.5, align_center=False)

    w.callout("Each outcome is assessed by a command you run", [
        [M("make transfer, make ladder"), N("   →  what RTL means, and abstraction")],
        [M("make prove, make mux"), N("        →  equivalence, and what it does NOT "
           "tell you")],
        [M("make subset, make mismatch"),
         N("  →  the synthesisable subset, and its traps")],
        [M("make pitfalls"), N("             →  the latch and the blocking trap, "
           "measured")],
        [M("make lint, make lintcheck"), N("   →  the coding standard, mechanised")],
        [M("make fsm"), N("                  →  state machines, both styles, both "
           "encodings")],
        [M("make dpctrl"), N("               →  datapath and controller")],
        [M("make reuse"), N("                →  parameters, hierarchy and generate")],
        [M("make langs"), N("                →  Verilog or VHDL, on two designs")],
        [M("make flow"), N("                 →  the whole methodology, end to end")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.callout("What's inside", [
        [B("THEORY"), N("")],
        [B("Part 1  "), N("What RTL is — the two kinds of logic, the synchronous "
                          "discipline, registers and transfers, blocking against "
                          "non-blocking, four levels of abstraction, proof, and the "
                          "running example")],
        [B("Part 2  "), N("The design process and methodology — the flow, the "
                          "synthesisable subset, inferred latches, the "
                          "simulate/synthesise mismatch, seven coding rules, "
                          "micro-architecture, reuse and coding style")],
        [B("Part 3  "), N("The patterns every block is built from — datapath and "
                          "controller, the finite state machine, Moore against "
                          "Mealy, state encoding, and parameters, hierarchy and "
                          "generate")],
        [B("Part 4  "), N("HDLs — why an HDL is not a programming language, "
                          "concurrency, the anatomy of a module, event-driven "
                          "simulation, Verilog against VHDL, reference cards, and "
                          "what a testbench is made of")],
        [B("PRACTICAL"), N("")],
        [B("Part 5  "), N("Tools and installation")],
        [B("Part 6  "), N("Fourteen guided tutorials, A to N, at the keyboard")],
        [B("Exercises  "), N("103 graded exercises with worked solutions")],
        [B("Reference  "), N("The rules, the subset, and the commands, on two pages")],
    ], color=NAVY, bar="0E2A47")

    w.callout("How to use this workbook", [
        [N("Read a part, then do its tutorial with a terminal open. Exercises marked "),
         B("[H]"), N(" are hand work — do them on paper first. "), B("[C]"),
         N(" need the computer. "), B("[W]"),
         N(" ask you to write something you could defend in a design review.")],
        [B("Predict before you measure. "),
         N("Almost every exercise here is worth more if you write down what you "
           "expect first. Being wrong and knowing why is the point of a lab; running "
           "a command and copying the output is not.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 1
    w.h1("Part 1 · What RTL Is")

    w.h2("1.1  The name is the definition")

    w.para([N("A register transfer level description says two things, and nothing "
              "else:")])
    w.numbered([
        [B("Which registers exist.")],
        [B("What transfers into each one, on each clock edge.")],
    ])
    w.para([N("Everything between the registers — the adder, the comparison, the "
              "multiplexer — is combinational logic that has one clock period to "
              "settle. You never say how long it takes or which gates it uses. "
              "You say what value lands in which register on the next edge.")])

    w.image("rtl_definition", width=6.9)

    w.code([
        "always @(posedge clk) begin",
        "    x   <= din;                 // input          -> x",
        "    y   <= x + 8'd1;            // x, plus logic  -> y",
        "    z   <= y << 1;              // y, plus logic  -> z",
        "    acc <= acc + z;             // acc and z      -> acc",
        "end"],
        caption="rtl/transfer.v — read this as a table of simultaneous transfers")

    w.para([N("Read that block as a "), B("table"), N(", not as a sequence. All four "
              "assignments read the OLD values of x, y, z and acc, and all four land "
              "at the same instant. That is what "), M("<="), N(" means, and section "
              "1.5 is about why it has to work that way.")])

    w.h3("Watch it happen")
    w.image("rtl_transfer_trace", width=6.9)
    w.para([N("A single 5 is applied on cycle 0 and never again. It lands in x on the "
              "first edge, becomes 6 in y on the second, 12 in z on the third, and "
              "reaches acc on the fourth. Nothing moved in between. That is the entire "
              "timing model of RTL, and it is why RTL is tractable to reason about "
              "where a gate-level netlist is not.")])

    w.h2("1.2  The two kinds of logic, and there is no third")

    w.image("comb_vs_seq", width=6.9)

    w.para([N("Every digital block ever built is some arrangement of two kinds of "
              "logic. Learning to see which one you are looking at is the first "
              "skill this topic asks for, because almost every rule that follows "
              "applies to one and not the other.")])

    w.h3("Combinational")
    w.para([N("The output is a function of the inputs "), B("right now"),
            N(". No clock, no memory, no history. Change an input and the output "
              "follows after a propagation delay, and that is the whole story.")])
    w.code([
        "assign y = a & b;                 // continuous assignment",
        "",
        "always @(*) begin                 // or a combinational always block",
        "    y = a & b;                    // BLOCKING assignment",
        "end"])
    w.para([N("The thing that goes wrong here is the "), B("inferred latch"),
            N(" — a path through the block on which some output is never assigned, "
              "so the tool has to build something that remembers. Section 2.3 is "
              "about that, and it is the single most common RTL bug there is.")])

    w.h3("Sequential")
    w.para([N("The output depends on the inputs "), B("and on the past"),
            N(". A flip-flop samples its input at one instant — the clock edge — and "
              "holds that value until the next edge, whatever the input does in "
              "between.")])
    w.code([
        "always @(posedge clk or negedge rst_n) begin",
        "    if (!rst_n) q <= 1'b0;        // reset appears HERE and nowhere else",
        "    else        q <= d;           // NON-BLOCKING assignment",
        "end"])
    w.para([N("The things that go wrong here are timing failures: the data arrives "
              "too late for the edge (a setup violation) or changes too soon after "
              "it (a hold violation). Neither is visible in an RTL simulation, which "
              "is why static timing analysis exists — and why it is Topic 6.")])

    w.callout("The whole of RTL design, in one sentence", [
        [N("Deciding what goes in the registers, and what happens between them.")],
        [N("That is not a slogan. It is literally what the letters R, T and L stand "
           "for, and if you can answer those two questions about a block you can "
           "write it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("1.3  The synchronous discipline")

    w.image("sync_design", width=6.9)

    w.para([N("Almost every rule in this topic — and most of the rules in Topics 5 "
              "and 6 — is a consequence of one decision: "), B("one clock, one edge, "
              "everything"), N(". It is worth stating the discipline explicitly, "
              "because a design that has drifted out of it fails in ways that are "
              "very hard to diagnose.")])

    w.table(["The rule", "What it means", "Why"],
            [["one clock edge", "every register samples at the same instant",
              "so 'now' means the same thing everywhere"],
             ["one reset policy", "sync or async, active high or low — pick one",
              "so nobody has to look it up per module"],
             ["no logic on the clock", "no gated clocks, no ripple clocks",
              "so timing analysis has one thing to analyse"],
             ["no latches", "assign every output on every path",
              "so timing is edge-to-edge, not level-dependent"],
             ["registered outputs", "a block's outputs come out of flip-flops",
              "so a slow path never crosses two blocks"]],
            widths=[1.5, 2.6, 2.7], size=10.0, bold_cols=(0,), align_center=False)

    w.h3("What the discipline buys you")
    w.bullets([
        [B("Analysable. "), N("With one clock and one edge, timing analysis is a "
           "finite question: for every path from a flip-flop to a flip-flop, does "
           "the data arrive in time? Add a gated clock and the question multiplies.")],
        [B("Composable. "), N("Two blocks written to the same discipline can be "
           "wired together without a conversation. Two blocks written to different "
           "disciplines need one, every time.")],
        [B("Reviewable. "), N("A reviewer can read your block for what it computes, "
           "because the question of WHEN has already been answered the same way it "
           "always is.")],
        [B("Testable. "), N("Scan insertion — the technique that makes a chip "
           "testable after manufacture — assumes edge-triggered flip-flops on one "
           "clock. Latches and gated clocks each need special handling.")],
    ])

    w.callout("You are allowed to break these rules", [
        [N("Clock gating and multiple clock domains are real techniques, used in "
           "every serious design. What makes them safe is that they are "),
         B("deliberate"), N(": chosen, reviewed, constrained and documented.")],
        [N("What is not safe is a design that drifted out of the discipline because "
           "nobody noticed. You are not allowed to break these rules by accident.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("1.4  Why anyone designs at this level")

    w.table(["", "Behavioural", "RTL", "Gate netlist"],
            [["you write", "the algorithm", "registers and transfers", "every gate"],
             ["timing", "none at all", "one clock period per stage",
              "exact, per gate"],
             ["synthesisable", "rarely", "yes — this is the target",
              "yes, but why would you"],
             ["a 10k-gate design", "unbuildable", "a few hundred lines",
              "tens of thousands of lines"],
             ["who writes it", "architects, in C or SystemC", "you",
              "the synthesiser"]],
            widths=[1.3, 1.8, 2.0, 1.7], size=10.0, bold_cols=(0,), align_center=False)

    w.callout("RTL is where the trade lands correctly", [
        [N("High enough that a human can write and read a real design; low enough "
           "that a tool can build it without guessing at your intent.")],
        [N("Above RTL you cannot say WHEN things happen. Below it you cannot say "
           "anything else. Every industrial digital design of the last thirty years "
           "was written at this level, and that is not fashion — it is where the "
           "abstraction pays for itself.")],
    ], color=TEAL)

    w.h2("1.5  Blocking and non-blocking assignment")

    w.image("nonblocking", width=6.9)

    w.h3("The swap, worked through")
    w.code([
        "// NON-BLOCKING - inside always @(posedge clk)",
        "//   Step 1: read every right-hand side, using the OLD values.",
        "//   Step 2: update every left-hand side, all at the same instant.",
        "",
        "        a <= b;        //  reads old b",
        "        b <= a;        //  reads old a",
        "",
        "        a and b are SWAPPED. This is what a hardware register does.",
        "",
        "// BLOCKING - inside always @*",
        "//   Each statement finishes before the next one starts.",
        "",
        "        a = b;         //  a is now b",
        "        b = a;         //  a is already b, so this does nothing",
        "",
        "        BOTH end up holding b. This is what software does."])

    w.callout("Why the rule is absolute rather than stylistic", [
        [N("Two clocked blocks using blocking assignments can see each other's "
           "half-updated values, and which one wins depends on the order the "
           "simulator happens to evaluate them in — an order the language standard "
           "deliberately does not fix.")],
        [B("Non-blocking assignment exists precisely to make that race impossible. "),
         N("It is not a convention; it is the mechanism.")],
    ], color=NAVY, bar="0E2A47")

    w.para([N("The mirror-image rule matters too. Non-blocking assignment inside a "
              "combinational block is legal, and it makes the block behave like a "
              "register in simulation while synthesis builds plain logic — so the "
              "simulation and the silicon disagree. Rules L001 and L002 of the linter "
              "in this lab catch both directions.")])

    w.h3("And what each one actually builds")

    w.image("blocking_measured", width=6.9)

    w.para([N("The argument above is about semantics. Here is the same argument as a "
              "measurement. Two files, identical apart from one character per line:")])

    w.code([
        "// shift_nb.v - the intended 3-stage shift register",
        "always @(posedge clk) begin",
        "    q[0] <= din;   q[1] <= q[0];   q[2] <= q[1];",
        "end",
        "",
        "// shift_bl.v - the same three lines with =",
        "always @(posedge clk) begin",
        "    q[0] = din;    q[1] = q[0];    q[2] = q[1];",
        "end"])

    w.code([
        "$ make pitfalls",
        "  non-blocking version : 0 wrong cycles",
        "  blocking version     : 6 wrong cycles",
        "",
        "  shift_nb (non-blocking)         3 cells     3 flip-flops",
        "  shift_bl (blocking)             1 cells     1 flip-flops"])

    w.callout("Three flip-flops against one", [
        [N("The blocking version did not build a slower shift register, or a buggy "
           "one. It built a "), B("different circuit"), N(" — din races all the way "
           "to q[2] in a single clock cycle, because q[0] already holds the new "
           "value when line two reads it.")],
        [N("It compiled. It simulated. It synthesised. No tool issued a single "
           "warning, because nothing illegal was written. This is exactly the class "
           "of bug a methodology rule exists to prevent, and rule L001 catches it in "
           "about a millisecond.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("1.6  Four levels of abstraction")

    w.image("ladder", width=6.9)

    w.para([N("Verilog can describe hardware at four levels. The lab writes the same "
              "full adder at all four and simulates them together:")])

    w.code([
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
        "pmos p1 (y, vdd, a);    nmos n1 (y, gnd, a);      // one CMOS inverter"])

    w.para([N("All four were driven with all eight input patterns — exhaustive, since "
              "a full adder has only three inputs — and compared against plain "
              "arithmetic. Zero mismatches. "),
            B("The level of abstraction changed what was written, not what it does.")])

    w.h3("And what a synthesiser makes of each")
    w.image("ladder_synthesis", width=6.9)

    w.callout("Two results worth stopping on", [
        [B("The behavioural description produced the SMALLEST circuit "),
         N("— five cells against six. It left the tool free to choose the Boolean "
           "form, and the tool found a better one than the textbook expression.")],
        [B("Dataflow and gate produced the IDENTICAL netlist. "),
         N("Once you have written the Boolean expression you have already committed "
           "to the structure; naming the gates adds nothing but typing.")],
        [N("And the switch-level description was refused outright. Transistor "
           "primitives are for library cells, not for synthesis.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.callout("The rule this gives you", [
        [B("Write at the highest level that expresses your intent."),
         N(" Every level you descend takes a decision away from the tool and gives "
           "it to you — whether or not you wanted it.")],
        [N("The tool is better than you are at choosing a gate mix, balancing a logic "
           "tree, and doing it again consistently at 3 a.m. It is not better than you "
           "are at deciding how many cycles the job takes, where the registers go, "
           "what is shared, or what the interface looks like. Give it the first list; "
           "keep the second.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("1.7  Simulation shows; proof settles")

    w.image("proof_vs_test", width=6.9)

    w.para([N("Eight patterns was exhaustive for a full adder. It stops being possible "
              "at about thirty inputs, and real designs have thousands — so the lab "
              "makes the same claim a different way. An "), B("equivalence check"),
            N(" builds a miter: both designs fed the same inputs, their outputs "
              "compared, and an assertion that the comparison always holds. A SAT "
              "solver then tries to find any input pattern that breaks it.")])

    w.code([
        "$ make prove",
        "  fa_behav vs fa_dataflow            EQUIVALENT   (proved, 94 SAT variables)",
        "  fa_behav vs fa_gate                EQUIVALENT   (proved, 94 SAT variables)",
        "  fa_dataflow vs fa_gate             EQUIVALENT   (proved, 100 SAT variables)",
        "",
        "  and the same checker, on a full adder with one term missing:",
        "  fa_behav vs fa_broken              NOT EQUIVALENT"])

    w.callout("That last line is the important one", [
        [M("fa_broken.v"), N(" has one term missing from the carry, so it is wrong for "
           "exactly one input pattern in eight. A random test could easily miss it. "
           "The solver cannot.")],
        [B("A checker that cannot fail is not evidence of anything. "),
         N("You have to watch it catch a real bug before you can trust it on a design "
           "you cannot check by hand.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("1.8  The running example")

    w.image("running_example", width=6.9)

    w.para([N("One design is carried through the rest of this workbook: a four-bit "
              "counter with an asynchronous reset, an enable and a terminal-count "
              "output. It is small enough to hold in your head and real enough to "
              "have every decision a real design has.")])

    w.code([
        "module counter4 (",
        "    input            clk,",
        "    input            rst_n,      // asynchronous, active LOW",
        "    input            en,",
        "    output reg [3:0] count,",
        "    output           tc          // one cycle high at 15",
        ");",
        "    always @(posedge clk or negedge rst_n) begin",
        "        if (!rst_n)     count <= 4'd0;",
        "        else if (en)    count <= count + 4'd1;",
        "    end",
        "",
        "    assign tc = en & (count == 4'd15);",
        "endmodule"],
        caption="rtl/counter4.v")

    w.h3("Four decisions are visible in fourteen lines")
    w.bullets([
        [B("The reset is asynchronous. "), N("That is why negedge rst_n is in the "
           "sensitivity list. A synchronous reset would not be — it would just be "
           "the first test inside the block.")],
        [B("The reset is active low. "), N("That is why the port is named rst_n and "
           "the test is !rst_n. Naming the polarity in the signal name is a "
           "convention worth keeping: it makes a wrong connection visible in the "
           "instantiation.")],
        [B("Reset is tested first. "), N("It therefore wins over the enable. Written "
           "the other way round, a reset arriving while en was low would be "
           "ignored.")],
        [B("There is no else on the enable. "), N("This is deliberate, and it is the "
           "one case where a missing else is correct: in a CLOCKED block, no "
           "assignment means hold, which is exactly what a flip-flop does. The same "
           "omission in a combinational block would build a latch.")],
    ])

    w.h3("The numbers, worked out")

    w.image("numerical_example", width=6.9)

    w.para([N("Run the arithmetic before you run the simulator. At 100 MHz the clock "
              "period is 10 ns, the counter has 2"), N("\u2074"), N(" = 16 states, so "
              "one full cycle takes 160 ns and "), M("tc"), N(" pulses at 6.25 MHz "
              "for exactly one clock period. Every one of those numbers is "
              "predictable from the source without running anything, and being able "
              "to do that is most of what design review is.")])

    w.callout("Where the running example goes next", [
        [B("Part 3 "), N("turns its controller into a state machine, and reuses the "
           "counter as the timer inside the traffic-light controller.")],
        [B("Part 3 again "), N("parameterises it as counter_n and instantiates it "
           "twice to build a prescaler.")],
        [B("Tutorial N "), N("runs it through the whole front end: spec, lint, "
           "simulation, synthesis, gate-level simulation, comparison and formal "
           "proof.")],
    ], color=TEAL)

    w.callout("Part 1 self-check", [
        [N("1.  What two things does an RTL description state?")],
        [N("2.  What are the only two kinds of digital logic?")],
        [N("3.  Name three things the synchronous discipline buys you.")],
        [N("4.  Explain what happens to a and b in a<=b; b<=a; and in a=b; b=a;")],
        [N("5.  How many flip-flops did the blocking shift register build, and why?")],
        [N("6.  Name the four levels of abstraction, highest first.")],
        [N("7.  Which level produced the smallest netlist, and why?")],
        [N("8.  Why did dataflow and gate produce identical netlists?")],
        [N("9.  Why does the lab include a deliberately broken full adder?")],
        [N("10. In counter4, why is there no else on the enable?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
