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
        [B("Part 1  "), N("What RTL is — what is physically on the chip, what a "
                          "signal is, what a register does, what happens between "
                          "two clock edges, the ladder of abstraction, and only "
                          "then the definition, the two kinds of logic and the "
                          "synchronous discipline")],
        [B("Part 2  "), N("The language you say it in — why an HDL is not a "
                          "programming language, concurrency, the anatomy of a "
                          "module, blocking against non-blocking, event-driven "
                          "simulation, and Verilog against VHDL")],
        [B("Part 3  "), N("The design process and methodology — the abstraction "
                          "ladder demonstrated, proof, the flow, the synthesisable "
                          "subset, inferred latches, the simulate/synthesise "
                          "mismatch, the coding rules and coding style")],
        [B("Part 4  "), N("The patterns every block is built from — datapath and "
                          "controller, the finite state machine, Moore against "
                          "Mealy, state encoding, and parameters, hierarchy and "
                          "generate")],
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

    w.para([N("RTL is an abstraction, and an abstraction is only learnable "
              "once you have seen the thing it abstracts. So this part starts "
              "with the silicon and works upwards. By the time the definition "
              "arrives in section 1.4, every word in it will already mean "
              "something physical.")])

    w.h2("1.1  What is actually on the chip")

    w.image("chip_physical")

    w.para([N("A digital chip is a pattern of four kinds of physical object, "
              "and nothing else:")])
    w.bullets([
        [B("A transistor "), N("is a switch. A voltage on its gate either lets "
           "current flow between its other two terminals, or stops it. It is "
           "perhaps 20 nanometres across, and a modern chip has billions.")],
        [B("A gate "), N("is four to ten transistors wired so that the output "
           "voltage is a Boolean function of the input voltages: NAND, NOR, an "
           "inverter.")],
        [B("A flip-flop "), N("is about twenty transistors wired so that it "
           "remembers one bit, and changes that bit only when a clock edge "
           "arrives.")],
        [B("A block "), N("is thousands of those, wired together to do "
           "something useful: a counter, a filter, a processor.")],
    ])

    w.callout("Keep this in view for the whole topic", [
        [N("Everything you write from here on is a way of TALKING about a "
           "pattern of those four objects. RTL does not replace them and it "
           "does not hide them - it lets you describe them without drawing "
           "each one.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("1.2  A signal is a voltage on a wire")

    w.image("signal_voltage")

    w.para([N("This is the single most useful piece of physical intuition in "
              "the whole course, and it is the one most often skipped.")])

    w.para([N("A 1 is not a number travelling down the wire. A wire is a thin "
              "strip of metal with capacitance, and a 1 means "), B("its "
              "voltage is somewhere in the upper band"), N(" - close enough to "
              "the supply that every gate reading it will agree it is a 1. A 0 "
              "means the voltage is in the lower band. Between the two there "
              "is a forbidden region where a reading gate may decide either "
              "way, and a well-designed circuit never rests there.")])

    w.h3("Why that has consequences")
    w.para([N("Changing a wire from 0 to 1 means "), B("charging a capacitor"),
            N(", and charging a capacitor takes time and energy. That single "
              "fact is where the rest of the course comes from:")])
    w.table(["The physical fact", "What it becomes later"],
            [["a wire takes time to change",
              "propagation delay, and the maximum clock frequency"],
             ["a longer wire takes longer",
              "why placement and routing affect timing at all"],
             ["a gate needs its input settled before it can be trusted",
              "setup time"],
             ["a gate needs its input held briefly after the edge",
              "hold time"],
             ["charging costs energy", "dynamic power, and why clocks are gated"]],
            widths=[3.0, 3.9], size=10.5, bold_cols=(0,), align_center=False)

    w.para([N("None of that appears in an RTL description. All of it is still "
              "true underneath, and Topic 6 and Module 3 are about what "
              "happens when you forget.")])

    w.h2("1.3  What a register physically does")

    w.image("register_physical")

    w.para([N("A flip-flop is not a variable, and it is not memory in the "
              "software sense. It is closer to a "), B("door that the clock "
              "edge opens for an instant"), N(". Its D input can wander as "
              "much as it likes during the cycle; at the rising edge, whatever "
              "value D happens to hold is captured, and Q then presents that "
              "value - flat and unchanging - until the next edge.")])

    w.callout("Why that one property makes design possible", [
        [N("Between two clock edges, nothing that any other block can observe "
           "changes. The whole design moves in discrete steps.")],
        [N("That is what lets you reason about a million-gate chip at all. "
           "Without it you would have to think about every signal at every "
           "instant, and nobody can do that.")],
    ], color=VIOLET, fill="F6F2FC", bar="7A4FBF")

    w.h2("1.4  What happens between two clock edges")

    w.image("clock_cycle_anatomy")

    w.para([N("This is the picture to keep in your head for the rest of the "
              "course. One clock period has four phases:")])

    w.numbered([
        [B("clk to Q. "), N("The edge arrives and the register drives its new "
           "value out. This takes a real, non-zero time, and it is the first "
           "thing that eats into your clock period.")],
        [B("Settling. "), N("The combinational logic between registers "
           "recomputes. While it does, its output is briefly WRONG: signals "
           "arrive down different paths at different times, so the output "
           "glitches, possibly several times.")],
        [B("Stable. "), N("The logic has finished. The value on the wire is "
           "now the correct answer, and it stays there.")],
        [B("Setup. "), N("Just before the next edge the value must ALREADY "
           "have been stable for a short window, or the capturing register may "
           "take the wrong value - or go metastable.")],
    ])

    w.callout("Two things worth taking from this picture", [
        [B("The glitches are harmless. "), N("Nothing looks at that wire until "
           "the next edge, by which time it has settled. Beginners often try "
           "to design them away; there is no need, and in synchronous logic "
           "you cannot.")],
        [B("You never state how long the settling takes. "),
         N("You state what the value must BE by the end of the period. Working "
           "out whether the logic actually fits is the job of synthesis and of "
           "static timing analysis, and that is Topic 6.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("1.5  The ladder of abstraction, and which rung RTL is")

    w.image("abstraction_stack")

    w.para([N("You now know what the hardware is. You could, in principle, "
              "design by drawing it - and for a handful of gates people once "
              "did. The reason nobody does today is arithmetic: a modern block "
              "has millions of gates, and no human can place a million of "
              "anything correctly.")])

    w.para([N("So digital design is organised as a ladder of descriptions. "
              "Each rung says less about the implementation and more about the "
              "intent:")])

    w.table(["Level", "What you say at this level", "What you leave out"],
            [["algorithm", "what the system computes", "all timing"],
             ["RTL", "which registers exist, and what transfers into them",
              "gates, wiring, delays"],
             ["gate", "every gate and every wire", "transistor sizes"],
             ["transistor", "every switch, and its width", "geometry"],
             ["layout", "the actual shapes on the silicon", "nothing"]],
            widths=[1.2, 3.2, 2.5], size=10.5, bold_cols=(0,),
            align_center=False)

    w.callout("The sentence that locates RTL", [
        [B("Above RTL you cannot say WHEN things happen. Below it you cannot "
           "say anything else.")],
        [N("Above RTL - in C, or in an algorithm - there is no clock, so you "
           "cannot express \"this value lands in that register on this edge\". "
           "Below RTL, at gate level, you must specify every gate, and a "
           "human writing a real design that way will not finish.")],
    ], color=NAVY, bar="0E2A47")

    w.para([N("RTL is therefore not a language and not a tool. It is a "),
            B("level of description"), N(" - a rung. Verilog and VHDL are two "
              "notations for writing at that rung, which is why the syllabus "
              "says \"HDLs such as Verilog or VHDL\" and why Part 2 treats the "
              "choice between them as a detail.")])

    w.h2("1.6  RTL, defined")

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
              "at the same instant. That is what "), M("<="), N(" means, and Part 2 "
              "is about why it has to work that way.")])

    w.h3("Watch it happen")
    w.image("rtl_transfer_trace", width=6.9)
    w.para([N("A single 5 is applied on cycle 0 and never again. It lands in x on the "
              "first edge, becomes 6 in y on the second, 12 in z on the third, and "
              "reaches acc on the fourth. Nothing moved in between. That is the entire "
              "timing model of RTL, and it is why RTL is tractable to reason about "
              "where a gate-level netlist is not.")])
    w.h2("1.7  Why anyone designs at this level")

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
    w.h2("1.8  The two kinds of logic, and there is no third")

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

    w.h2("1.9  The synchronous discipline")

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
    w.h2("1.10  The running example")

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
        [N("1.  Name the four kinds of physical object a digital chip is made "
           "of.")],
        [N("2.  What does a 1 on a wire physically mean?")],
        [N("3.  Why does changing a wire from 0 to 1 take time?")],
        [N("4.  What does a flip-flop do at the clock edge, and between "
           "edges?")],
        [N("5.  Name the four phases of one clock period, in order.")],
        [N("6.  Why are the glitches during settling harmless?")],
        [N("7.  Which rung of the abstraction ladder is RTL, and what is on "
           "either side of it?")],
        [N("8.  What two things does an RTL description state?")],
        [N("9.  What are the only two kinds of digital logic?")],
        [N("10. Name three things the synchronous discipline buys you.")],
        [N("11. In counter4, why is there no else on the enable?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
