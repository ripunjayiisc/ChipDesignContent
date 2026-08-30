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
        ["Theory 1 · What RTL is — from the transistor up: what a signal is, "
         "what a register does, and where RTL sits on the ladder of abstraction",
         "Theory 2 · The language you say it in — an HDL is not a program",
         "Theory 3 · The methodology — the flow, the synthesisable subset, the "
         "rules, and what the tool actually builds",
         "Theory 4 · The patterns — datapath and controller, state machines, "
         "parameters and generate",
         "Practical · Labs A–N · 26 hours · 103 exercises · every number measured"])

    # ==================================================== terminal outcomes
    s = d.slide("MODULE 2 · NOS NIE/ELE/N0102", "Terminal Outcomes")
    y = d.image(s, TOP - 45720, "terminal_outcomes", 4250000)
    d.card(s, y + G, "Outcome 2 names this subtopic in the NOS itself",
           [[R("\"Level of abstraction in Verilog programming\" is the phrase. This "
               "session takes one circuit down all four levels, simulates them "
               "together, and proves they are the same — which is the deliverable "
               "the outcome asks for.", s=12.0)]],
           accent=NAVY, h=868680)

    s = d.slide("MODULE 2 · TOPIC 2", "Key Learning Outcomes", accent=GREEN)
    y = d.image(s, TOP - 45720, "learning_outcomes", 4950000)
    d.lead(s, y + G, [[R("Every outcome is assessed by a command you run, not by "
                         "something you recite.", b=True, c=GREEN, s=12.0)]],
           h=365760)

    s = d.slide("MODULE 2 · TOPIC 2", "Which Command Assesses Which Outcome",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "outcomes_commands", 4950000)
    d.lead(s, y + G, [[R("Run the right-hand column and you have evidence for the "
                         "left-hand one.", s=12.0)]], h=228600)

    s = d.slide("TOPIC 2 · COVERAGE", "Every Syllabus Phrase, and Where It Is Covered")
    y = d.image(s, TOP - 45720, "syllabus_map", 4250000)
    d.card(s, y + G, "On the four notional hours",
           [[R("Four hours is enough to define the terms. It is not enough to make "
               "anyone believe them — and nothing in this subtopic is believed until "
               "it has been seen to happen. Lecture from the summary slides to fit "
               "four hours; run the lab alongside to teach it.", s=12.0)]],
           accent=AMBER, fill=CARD_A, h=868680)

    s = d.slide("TOPIC 2 · STRUCTURE", "How This Session Runs")
    y = d.image(s, TOP - 45720, "topic_structure", 4950000)
    d.lead(s, y + G, [[R("RTL is not a language and it is not a tool. It is a way of "
                         "thinking about hardware.", b=True, c=NAVY, s=12.0)]],
           h=274320)

    # ===================================================== section THEORY 1
    d.section_slide(
        "THEORY 1", "What RTL Is",
        "RTL is an abstraction, and an abstraction only means something once "
        "you have seen the thing it abstracts. So this section starts with "
        "the silicon and works upwards.",
        ["What is physically on the chip, and what a signal physically is",
         "What a register does, and what happens between two clock edges",
         "The ladder of abstraction, and which rung RTL is",
         "Only then: the definition, and what follows from it",
         "The two kinds of logic, and the synchronous discipline"])

    # ------------------------------------------------- the physical picture
    s = d.slide("1.1 · THE PHYSICAL PICTURE", "What Is Actually On the Chip")
    y = d.image(s, TOP - 45720, "chip_physical", 4950000)
    d.lead(s, y + G, [[R("Start here, not with a definition. Everything later "
                         "in this topic is a way of talking about these four "
                         "things.", s=12.0)]], h=228600)

    s = d.slide("1.1 · THE PHYSICAL PICTURE", "A Signal Is a Voltage on a Wire")
    y = d.image(s, TOP - 45720, "signal_voltage", 4114800)
    d.card(s, y + G, "Why this matters for everything that follows",
           [[R("A wire is a small capacitor, and driving it from 0 to 1 means "
               "charging it. Propagation delay, setup time, hold time and "
               "maximum clock frequency are all consequences of that one "
               "physical fact.", s=12.0)]],
           accent=RED, fill=CARD_R, h=1005840)

    # ------------------------------------------------------- the register
    s = d.slide("1.2 · THE REGISTER", "What a Register Physically Does")
    y = d.image(s, TOP - 45720, "register_physical", 4950000)
    d.lead(s, y + G, [[R("A flip-flop is not a variable. It is a door the "
                         "clock edge opens for an instant.", b=True, c=VIOLET,
                         s=12.0)]], h=228600)

    s = d.slide("1.2 · THE REGISTER", "What Happens Between Two Clock Edges",
                accent=NAVY)
    y = d.image(s, TOP - 45720, "clock_cycle_anatomy", 4950000)
    d.lead(s, y + G, [[R("Memorise this picture. Almost every rule in Topics 2, "
                         "5 and 6 is a statement about some part of it.",
                         b=True, c=NAVY, s=12.0)]], h=228600)

    s = d.slide("1.2 · THE REGISTER", "Reading That Picture")
    y = d.tiers(s, TOP, [
        ("clk → Q",
         "The edge arrives and the register drives its new value out. This "
         "takes a real, non-zero time, and it is the first thing that eats "
         "into your clock period.", VIOLET),
        ("SETTLING",
         "The combinational logic between registers now recomputes. While it "
         "does, its output is briefly WRONG — signals arrive down different "
         "paths at different times and the output glitches. This is normal "
         "and harmless, because nothing is looking.", AMBER),
        ("STABLE",
         "The logic has finished. The value on the wire is now the correct "
         "answer, and it stays there.", GREEN),
        ("SETUP",
         "Just before the next edge, the value must ALREADY have been stable "
         "for a short window, or the register may capture the wrong thing. "
         "Miss it and you have a setup violation.", RED)],
        h=822960)

    d.lead(s, y + G, [[R("Everything you write in RTL has to fit in that gap. "
                         "You never say how long it takes — you say what the "
                         "answer must be by the end of it.", b=True, c=NAVY,
                         s=12.0)]], h=274320)

    # ------------------------------------------------------- the ladder
    s = d.slide("1.3 · ABSTRACTION", "The Ladder, and Which Rung RTL Is")
    y = d.image(s, TOP - 45720, "abstraction_stack", 4950000)
    d.lead(s, y + G, [[R("RTL is not a language and not a tool. It is a LEVEL "
                         "of description — one rung on this ladder.", b=True,
                         c=NAVY, s=12.0)]], h=228600)

    s = d.slide("1.3 · ABSTRACTION", "Why Anyone Designs At This Level")
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
                [2194560, 2926080, 3200400, 2926080], rh=310896, bold_cols=(2,))

    y = d.card(s, y + G, "RTL is the level where the trade lands correctly",
               [[R("High enough that a human can write and read a real design; "
                   "low enough that a tool can build it without guessing at "
                   "your intent.", s=12.0)],
                [R("Every industrial digital design in the last thirty years "
                   "was written here. That is not fashion — it is where the "
                   "abstraction pays for itself.", b=True, c=NAVY, s=12.0)]],
               accent=TEAL, h=1188720)

    # ----------------------------------------------------- RTL, defined
    s = d.slide("1.4 · RTL, DEFINED", "Now the Definition Means Something")
    y = d.image(s, TOP - 45720, "rtl_definition", 4250000)
    d.card(s, y + G, "Read it against the physical picture",
           [[R("\"Which registers exist\" means: which of those edge-triggered "
               "doors are in the design. \"What transfers into them\" means: "
               "what the logic between them must have settled to before the "
               "next edge arrives. Nothing else — not the gates, not the "
               "wiring, not the delay — is yours to state.", s=12.0)]],
           accent=NAVY, h=1005840)

    s = d.slide("1.4 · RTL, DEFINED", "Watch One Value Transfer")
    y = d.image(s, TOP - 45720, "rtl_transfer_trace", 4950000)
    d.lead(s, y + G, [[R("One register per clock edge, and nothing moving in "
                         "between. That is the whole timing model.", s=12.0)]],
           h=228600)

    # --------------------------------------------- the two kinds of logic
    s = d.slide("1.5 · THE TWO KINDS", "Combinational and Sequential")
    y = d.image(s, TOP - 45720, "comb_vs_seq", 4950000)
    d.lead(s, y + G, [[R("There is no third kind. Every block in this course "
                         "is an arrangement of these two.", b=True, c=NAVY,
                         s=12.0)]], h=274320)

    s = d.slide("1.5 · THE TWO KINDS", "Side By Side")
    y = d.image(s, TOP - 45720, "comb_vs_seq_table", 4950000)
    d.lead(s, y + G, [[R("Each row is a rule you will use every day. Learn "
                         "which column you are in before you write a line.",
                         s=12.0)]], h=228600)

    # -------------------------------------------------- synchronous design
    s = d.slide("1.6 · THE DISCIPLINE", "One Clock, One Edge, Everything")
    y = d.image(s, TOP - 45720, "sync_design", 4950000)
    d.lead(s, y + G, [[R("Almost every rule in this topic is a consequence of "
                         "this one decision.", b=True, c=NAVY, s=12.0)]],
           h=228600)

    s = d.slide("1.6 · THE DISCIPLINE", "What the Discipline Buys You")
    y = d.tiers(s, TOP, [
        ("ANALYSABLE",
         "With one clock and one edge, timing analysis is a finite question: "
         "for every path from a flip-flop to a flip-flop, does the data "
         "arrive in time? Add a gated clock and the question multiplies.",
         NAVY),
        ("COMPOSABLE",
         "Two blocks written to the same discipline can be wired together "
         "without a conversation. Two blocks written to different disciplines "
         "need one, every time.", TEAL),
        ("REVIEWABLE",
         "A reviewer can read your block for what it computes, because the "
         "question of WHEN has already been answered the same way it always "
         "is.", VIOLET),
        ("TESTABLE",
         "Scan insertion, the technique that makes a chip testable after "
         "manufacture, assumes edge-triggered flip-flops on one clock. "
         "Latches and gated clocks each need special handling.", GREEN)],
        h=822960)

    d.lead(s, y + G, [[R("You are allowed to break these rules. You are not "
                         "allowed to break them by accident.", b=True, c=AMBER,
                         s=12.0)]], h=274320)

    # ------------------------------------------------ the designer's view
    s = d.slide("1.7 · THE DESIGNER'S VIEW", "What You Decide, What the Tool "
                "Decides")
    y = d.image(s, TOP - 45720, "designer_view", 4950000)
    d.lead(s, y + G, [[R("This split IS the abstraction. Learning RTL is "
                         "learning where the line falls.", b=True, c=NAVY,
                         s=12.0)]], h=228600)

    # ------------------------------------------------- the running example
    s = d.slide("1.8 · THE RUNNING EXAMPLE", "One Design, Carried All the Way "
                "Through")
    y = d.image(s, TOP - 45720, "running_example", 4950000)
    d.lead(s, y + G, [[R("Four bits, an asynchronous reset, an enable and a "
                         "terminal count. Small enough to read in one glance, big "
                         "enough to be a real design.", s=12.0)]], h=274320)

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
        "endmodule"], size=11.5)

    d.card(s, y + G, "Four decisions are visible in fourteen lines",
           [[R("The reset is ASYNCHRONOUS, so it is in the sensitivity list; it is "
               "ACTIVE LOW, so the port is named rst_n and the test is !rst_n. "
               "Reset is tested FIRST, so it wins over the enable. And the missing "
               "else is deliberate — in a CLOCKED block, no assignment means hold, "
               "which is what a flip-flop does anyway.")]],
           accent=NAVY, h=1097280)

    s = d.slide("1.8 · THE RUNNING EXAMPLE", "The Numbers, Worked Out")
    y = d.image(s, TOP - 45720, "numerical_example", 4950000)
    d.lead(s, y + G, [[R("Derive the formula, then measure it. A testbench that only "
                         "ever tries one value of N has told you almost nothing.",
                         b=True, c=NAVY, s=12.0)]], h=274320)

    s = d.slide("THEORY 1 · CHECKPOINT", "Ten Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What is physically on the chip?",
                  "transistors, wired into gates, flip-flops and blocks"],
                 ["2", "What does a 1 on a wire physically mean?",
                  "a voltage in the upper band, not a number"],
                 ["3", "Why does changing a wire take time?",
                  "the wire is a capacitor and has to be charged"],
                 ["4", "What does a flip-flop do at the clock edge?",
                  "captures D, then holds it until the next edge"],
                 ["5", "Name the four phases of one clock period.",
                  "clk-to-Q, settling, stable, setup window"],
                 ["6", "Why are glitches during settling harmless?",
                  "nothing samples until the next edge"],
                 ["7", "Which rung of the abstraction ladder is RTL?",
                  "below the algorithm, above the gate netlist"],
                 ["8", "What two things does an RTL description state?",
                  "which registers exist, and what transfers into them"],
                 ["9", "What are the only two kinds of digital logic?",
                  "combinational and sequential — there is no third"],
                 ["10", "Name three things you decide that the tool does not.",
                  "the registers, the cycle count, the interface"]],
                [548640, 5029200, 5669280], rh=274320, bold_cols=(0,), size=11.0)
    d.lead(s, y + G, [[R("Theory 2 is the notation you write all of that down "
                         "in.", b=True, c=GREEN, s=12.5)]], h=274320)
