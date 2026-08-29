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
              {"b": True, "s": 11, "c": TEAL})], space_after=2)
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
              "guided tutorials at the keyboard, and ends with 60 graded exercises "
              "and full worked solutions. Every number quoted here was produced by "
              "running the code in Topic2_Lab/. Nothing in this workbook requires you "
              "to look anything up elsewhere.", {"s": 10.5})])
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
              {"s": 10.5})])
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
              "and proves they are the same circuit.", {"s": 10.5})])
    w.para([N("Outcome 3 begins with knowing what is synthesisable and what is not, "
              "which is Part 2. Outcome 4 asks for reusable IP, and reuse is a set of "
              "decisions you take while writing, not a property you add afterwards — "
              "also Part 2.", {"s": 10.5})])

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
            widths=[3.4, 3.4], size=9.5, align_center=False)

    w.callout("Each outcome is assessed by a command you run", [
        [M("make transfer, make ladder"), N("   →  what RTL means, and abstraction")],
        [M("make prove"), N("            →  equivalence, and why testing runs out")],
        [M("make subset, make mismatch"),
         N("  →  the synthesisable subset, and its traps")],
        [M("make lint, make lintcheck"), N("   →  the coding standard, mechanised")],
        [M("make langs"), N("            →  Verilog or VHDL")],
        [M("make flow"), N("             →  the whole methodology, end to end")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.callout("What's inside", [
        [B("THEORY"), N("")],
        [B("Part 1  "), N("What RTL is — registers and transfers, blocking against "
                          "non-blocking, four levels of abstraction, and proof")],
        [B("Part 2  "), N("The design process and methodology — the flow, the "
                          "synthesisable subset, inferred latches, the "
                          "simulate/synthesise mismatch, seven coding rules, "
                          "micro-architecture and reuse")],
        [B("Part 3  "), N("HDLs — why an HDL is not a programming language, "
                          "concurrency, the anatomy of a module, event-driven "
                          "simulation, and Verilog against VHDL")],
        [B("PRACTICAL"), N("")],
        [B("Part 4  "), N("Tools and installation")],
        [B("Part 5  "), N("Nine guided tutorials, A to I, at the keyboard")],
        [B("Exercises  "), N("60 graded exercises with worked solutions")],
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

    w.image("rtl_definition", width=6.4)

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
              "1.3 is about why it has to work that way.")])

    w.h3("Watch it happen")
    w.image("rtl_transfer_trace", width=6.4)
    w.para([N("A single 5 is applied on cycle 0 and never again. It lands in x on the "
              "first edge, becomes 6 in y on the second, 12 in z on the third, and "
              "reaches acc on the fourth. Nothing moved in between. That is the entire "
              "timing model of RTL, and it is why RTL is tractable to reason about "
              "where a gate-level netlist is not.")])

    w.h2("1.2  Why anyone designs at this level")

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
            widths=[1.3, 1.8, 2.0, 1.7], size=9.0, bold_cols=(0,), align_center=False)

    w.callout("RTL is where the trade lands correctly", [
        [N("High enough that a human can write and read a real design; low enough "
           "that a tool can build it without guessing at your intent.")],
        [N("Above RTL you cannot say WHEN things happen. Below it you cannot say "
           "anything else. Every industrial digital design of the last thirty years "
           "was written at this level, and that is not fashion — it is where the "
           "abstraction pays for itself.")],
    ], color=TEAL)

    w.h2("1.3  Blocking and non-blocking assignment")

    w.image("nonblocking", width=6.4)

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

    w.h2("1.4  Four levels of abstraction")

    w.image("ladder", width=6.5)

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
    w.image("ladder_synthesis", width=6.4)

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

    w.h2("1.5  Simulation shows; proof settles")

    w.image("proof_vs_test", width=6.4)

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

    w.callout("Part 1 self-check", [
        [N("1.  What two things does an RTL description state?")],
        [N("2.  Explain what happens to a and b in a<=b; b<=a; and in a=b; b=a;")],
        [N("3.  Name the four levels of abstraction, highest first.")],
        [N("4.  Which level produced the smallest netlist, and why?")],
        [N("5.  Why did dataflow and gate produce identical netlists?")],
        [N("6.  Why does the lab include a deliberately broken full adder?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
