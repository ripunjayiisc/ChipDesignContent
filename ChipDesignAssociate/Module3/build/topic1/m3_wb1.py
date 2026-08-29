# -*- coding: utf-8 -*-
"""Module 3 Topic 1 workbook — front matter, outcomes, Theory 1 and Theory 2."""
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
    r = p.add_run("Module 3 — Topic 1")
    r.font.name = HEADF; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = SLATE
    p.paragraph_format.space_after = Pt(2)
    p = w.d.add_paragraph()
    r = p.add_run("Overview of VLSI STA")
    r.font.name = HEADF; r.font.size = Pt(25); r.font.bold = True; r.font.color.rgb = NAVY
    p.paragraph_format.space_after = Pt(4)
    p = w.d.add_paragraph()
    r = p.add_run("Tutorial & Practice Workbook")
    r.font.name = HEADF; r.font.size = Pt(16); r.font.color.rgb = AMBER
    p.paragraph_format.space_after = Pt(10)
    w.para([N("A self-study companion to the Topic 1 slide deck. It explains every "
              "concept the deck introduces and why it exists, walks you through seven "
              "guided tutorials at the keyboard, and ends with 58 graded exercises and "
              "full worked solutions. Every number quoted here was produced by running "
              "the code in Topic1_Lab/. Nothing in this workbook requires you to look "
              "anything up elsewhere.", {"s": 10.5})])
    w.para([N("NOS: NIE/ELE/N0103  ·  Module 3 “Static Timing Analysis of VLSI "
              "Circuits”, subtopic 1 “Overview of VLSI STA”  ·  Syllabus: introduction "
              "to timing analysis; combinational circuit timing — races and hazards; "
              "sequential circuit timing — setup and hold timing; maximum frequency of "
              "operation; practical examples of setup and hold time violations and "
              "their solution; timing constraints for synthesis; circuit synthesis and "
              "timing analysis.  Module duration: 25 h theory, 35 h practical.",
              {"s": 9, "c": SLATE, "i": True})])

    # ------------------------------------------------- terminal outcomes
    w.h1("Terminal Outcomes")
    w.para([N("After completion of Module 3, the student shall be able to:",
              {"s": 10.5})])
    w.callout("Module 3 terminal outcomes (NOS NIE/ELE/N0103)", [
        [B("1.  "), N("Understand static timing analysis — what a timing path is, how "
                      "arrival, required and slack are computed, and how to read any "
                      "timing report.")],
        [B("2.  "), N("Understand ECO fixes and timing closure for VLSI circuits — how "
                      "to diagnose a violation, choose a fix, and drive a design to a "
                      "state where every check passes at every corner.")],
    ], color=NAVY, bar="0E2A47")

    w.para([N("This subtopic builds outcome 1 and supplies the vocabulary and the "
              "diagnostic habits that outcome 2 depends on: you cannot write an "
              "engineering change order for a violation you cannot classify. "
              "Subtopic 2 covers timing performance; subtopic 3 covers the EDA flow, "
              "the ECO loop and sign-off.", {"s": 10.5})])

    # ------------------------------------------------- learning outcomes
    w.h1("Key Learning Outcomes")
    w.table(["Theory — you will be able to", "Practical — you will be able to"],
            [["Describe the key components of STA: timing paths, "
              "constraints and timing reports",
              "Conduct static timing analysis using industry-standard tools to "
              "analyse timing paths in VLSI circuits"],
             ["Analyse timing issues in combinational circuits, "
              "including races and hazards",
              "Identify and resolve timing issues such as setup and hold time "
              "violations through practical exercises"],
             ["Discuss how timing constraints influence the synthesis process and "
              "timing optimisation",
              "Implement timing constraints in EDA tools and analyse their impact on "
              "circuit timing during synthesis"],
             ["Evaluate timing performance metrics such as maximum frequency of "
              "operation and clock skew",
              "Evaluate the effects of clock skew on a real design"]],
            widths=[3.4, 3.4], size=9.5, align_center=False)

    w.callout("Each outcome is assessed by something you run", [
        [M("make analyse, make glitch, make capture"),
         N("  →  races and hazards in combinational circuits")],
        [M("make synth, make setup"),
         N("  →  constraints, synthesis, and their impact")],
        [M("make hold, make fmax"),
         N("  →  setup, hold, clock skew, maximum frequency")],
        [M("vivado/zynq_sta.tcl"),
         N("  →  STA using an industry-standard tool on a Zynq-7000")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.callout("What's inside", [
        [B("THEORY"), N("")],
        [B("Part 1  "), N("What timing analysis is — why a truth table is not enough, "
                          "the three questions timing asks, and the difference between "
                          "a hazard and a glitch")],
        [B("Part 2  "), N("Races and hazards — the mechanism, the three kinds, the "
                          "function hazard you cannot fix, the adjacency rule, the "
                          "consensus term, where it stops working, and races")],
        [B("Part 3  "), N("Sequential circuit timing — the sampling window, setup and "
                          "hold, maximum frequency of operation derived, and real "
                          "violations with their solutions")],
        [B("Part 4  "), N("Timing constraints for synthesis, and circuit synthesis and "
                          "timing analysis as one loop")],
        [B("PRACTICAL"), N("")],
        [B("Part 5  "), N("Tools and installation — which tool answers which question, "
                          "and one apt line that runs the whole lab")],
        [B("Part 6  "), N("Seven guided tutorials, A to G, at the keyboard")],
        [B("Exercises  "), N("58 graded exercises across seven parts, every one with a "
                             "worked solution")],
        [B("Reference  "), N("The equations, the rules, and the commands, on two "
                             "pages")],
    ], color=NAVY, bar="0E2A47")

    w.callout("How to use this workbook", [
        [N("Read a part, then do its tutorial with a terminal open. Exercises marked "),
         B("[H]"), N(" are hand calculations — do them on paper first. "), B("[C]"),
         N(" need the computer. "), B("[W]"),
         N(" ask you to write something down and defend it.")],
        [N("If a number you measure disagrees with a number printed here, do not "
           "assume the workbook is right. Find out which of you is wrong — that "
           "investigation is worth more than the answer.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 1
    w.h1("Part 1 · What Timing Analysis Is")

    w.h2("1.1  A truth table is a promise about settled values")

    w.para([N("A truth table says: once everything has stopped moving, the output will "
              "be this. Every row, every time. That is what your RTL simulation "
              "checks, and it is a real guarantee — but it is a guarantee about the "
              "destination, not about the journey.")])
    w.para([N("Real gates take real time. Between the moment an input changes and the "
              "moment the output settles, the circuit is in a state the truth table "
              "does not describe. Two things can go wrong there, and neither one is "
              "visible in a zero-delay simulation:")])
    w.numbered([
        [B("The output passes through a wrong value on its way to the right one. "),
         N("This is a "), B("hazard"), N(", and it is the subject of Part 2.")],
        [B("The output arrives after the flip-flop needed it. "),
         N("This is a "), B("setup violation"), N(", and it is the subject of Part 3.")],
    ])

    w.image("hazard_idea", width=6.4)

    w.h2("1.2  The three questions")

    w.table(["The question", "The failure if the answer is no", "Answered by"],
            [["Did the data arrive before the capturing edge needed it?",
              "setup violation — the chip runs, but only slower",
              "static timing analysis"],
             ["Did the data stay put long enough after that edge?",
              "hold violation — the chip does not work at all",
              "static timing analysis"],
             ["Did the output pass through a wrong value on the way?",
              "a hazard — harmless or fatal depending on where the signal goes",
              "simulation with delays"]],
            widths=[2.4, 2.6, 1.6], size=9.2, align_center=False)

    w.callout("The first two are about ONE path. The third is about TWO.", [
        [N("Setup and hold ask how long a path is. A hazard asks what happens when two "
           "paths of different length reconverge on the same output — so no "
           "measurement of any single path can detect one.")],
        [B("This is why static timing analysis is structurally blind to hazards, "
           "and why this topic uses two different tools on the same circuit.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.image("sta_blind_to_hazards", width=6.4)

    w.h2("1.3  Hazard and glitch are not the same word")

    w.table(["", "HAZARD", "GLITCH"],
            [["what it is", "a property of the circuit", "an event in one simulation"],
             ["it means", "there EXISTS an assignment of gate delays for which this "
              "output misbehaves", "on this run, with these delays, the output "
              "actually did misbehave"],
             ["how you find it", "by inspecting the logic — no simulation needed",
              "by simulating with delays, on the transitions you stimulated"],
             ["it is", "either there or not", "may or may not show up"]],
            widths=[1.1, 2.8, 2.9], size=9.2, bold_cols=(0,), align_center=False)

    w.callout("Why the distinction earns its keep", [
        [N("A circuit with a hazard may run for years without glitching, because the "
           "delays happened to fall the right way. Then the process moves, or the "
           "temperature changes, or somebody re-synthesises — and it starts failing "
           "in the field.")],
        [B("You remove hazards, not glitches.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("1.4  Vocabulary")

    w.table(["Term", "One-line definition"],
            [["combinational logic", "output depends only on the present inputs"],
             ["sequential logic", "output depends on inputs and on stored state"],
             ["propagation delay", "how long a gate takes to react to its input"],
             ["timing path", "a route from a start point to an end point, with a delay"],
             ["arrival time", "when the data actually reaches a pin"],
             ["required time", "when it had to be there for the check to pass"],
             ["slack", "required minus arrival; negative means it does not fit"],
             ["setup time", "how long D must be stable before the clock edge"],
             ["hold time", "how long D must stay stable after the clock edge"],
             ["clock-to-Q", "delay from the clock edge until Q is valid"],
             ["clock skew", "the same edge reaching two registers at different instants"],
             ["clock jitter", "cycle-to-cycle variation in the edge position"],
             ["glitch", "a momentary wrong value on an output"],
             ["hazard", "a circuit's potential to glitch, given unlucky delays"],
             ["race", "two signals changing where the order decides the outcome"],
             ["consensus term", "the redundant product term that removes a static "
                                "hazard"],
             ["Fmax", "one divided by the longest path delay"]],
            widths=[1.7, 5.1], size=9.2, bold_cols=(0,), align_center=False)

    w.callout("Part 1 self-check", [
        [N("1.  Which is a property of the circuit — a hazard or a glitch?")],
        [N("2.  Why can no measurement of a single path detect a hazard?")],
        [N("3.  Name the two failures a zero-delay simulation cannot show you.")],
        [N("4.  A circuit has run correctly for two years. Does that prove it has no "
           "hazard?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 2
    w.h1("Part 2 · Combinational Circuit Timing: Races and Hazards")

    w.h2("2.1  The mechanism")

    w.para([N("One input reaches the output by two different routes with different "
              "delays. When that input changes, one route has already reacted and the "
              "other has not, so for a short interval the output is computed from two "
              "inconsistent versions of the same signal.")])

    w.image("hazard_race", width=6.5,
            caption="F = A B' + B C with A = 1 and C = 1, as B falls.")

    w.para([N("Follow the four traces. B falls. The term "), M("B C"),
            N(" switches off almost at once — it is one AND gate away from B. The term "),
            M("A B'"), N(" cannot switch on until B has been through the inverter and "
                         "then an AND gate. For the interval between those two events, "
                         "both terms are 0, and the OR gate has nothing holding its "
                         "output up.")])

    w.h2("2.2  The three kinds, and the one you cannot fix")

    w.image("hazard_kinds", width=6.4)

    w.table(["Kind", "The output should", "It actually", "Can occur in"],
            [["static-1", "stay at 1", "dips to 0", "two-level AND-OR"],
             ["static-0", "stay at 0", "spikes to 1", "two-level OR-AND"],
             ["dynamic", "change once", "changes three or more times",
              "three or more levels"]],
            widths=[1.1, 1.5, 2.0, 2.2], size=9.2, bold_cols=(0,), align_center=False)

    w.h3("The function hazard")
    w.para([N("Everything else in this part assumes "),
            B("one input changes at a time"),
            N(". Let two change at once and a different problem appears. Consider "),
            M("F = A B' + B C"), N(" with A = 1, C = 0, going from B=1 to B=0 and "
                                   "C=0 to C=1 simultaneously:")])
    w.code([
        "    start   A=1 B=1 C=0    ->  F = 0",
        "    end     A=1 B=0 C=1    ->  F = 1",
        "",
        "In between the circuit must pass through either",
        "    A=1 B=1 C=1  (F = 1)   or   A=1 B=0 C=0  (F = 1)",
        "depending which input the wiring happens to deliver first."])
    w.callout("Why no implementation can remove it", [
        [N("The intermediate states are real: the inputs genuinely do pass through "
           "them, because they do not change at exactly the same instant. Every "
           "correct implementation of this function must produce the function's value "
           "in those states. The glitch is in the truth table, not in the gates.")],
        [B("The only remedy is to not change those inputs simultaneously — which, in "
           "a synchronous design, is exactly what a common clock guarantees.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("2.3  The adjacency rule")

    w.callout("The rule, in one sentence", [
        [B("Take two input patterns that differ in exactly ONE variable and both give "
           "F = 1. If no single product term covers both of them, the circuit has a "
           "static-1 logic hazard on that transition.")],
    ], color=NAVY, bar="0E2A47")

    w.code([
        "F = A B' + B C          A=1, C=1, and B changes",
        "",
        "    B=1 :  F = 1, held up by  B C",
        "    B=0 :  F = 1, held up by  A B'",
        "",
        "    Does one term cover BOTH?",
        "        A B'  needs B=0  ->  covers only the second",
        "        B C   needs B=1  ->  covers only the first",
        "    No. So the output is handed from one term to the other."])

    w.para([N("The reasoning behind the rule is worth stating explicitly, because it "
              "is what makes the rule trustworthy. If some term is 1 for "), I("both"),
            N(" patterns, that term does not change during the transition, so it holds "
              "the output up throughout and no assignment of delays can produce a dip. "
              "If no term does, then one term must switch off while another switches "
              "on, and the order in which that happens is decided by delays you do not "
              "control.")])

    w.h3("The same rule on a K-map")
    w.image("hazard_kmap", width=6.4)
    w.para([N("Two 1-cells side by side with no single loop around both. Adjacent 1s "
              "in different loops is exactly \"two patterns one variable apart covered "
              "by no single term\", drawn instead of written.")])

    w.h2("2.4  The consensus term")

    w.image("consensus_fix", width=6.5)

    w.para([N("The fix is to add a product term that covers both patterns. To "
              "construct it: write down every variable the two patterns agree on, at "
              "the value they agree on, and drop the one that changed. For A=1, C=1 "
              "with B changing, that gives "), M("A C"), N(".")])

    w.callout("Redundant is not a criticism — it is the requirement", [
        [N("The consensus term covers no new 1s, so the truth table is identical. "
           "That is not a flaw: a term that changed the function would not be a fix, "
           "it would be a bug. The only way to hold the output up without altering "
           "what the circuit computes is to add cover that is already covered.")],
        [B("And it is also why the fix is fragile: removing redundancy is precisely "
           "what a logic optimiser exists to do. Part 4 measures exactly that.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("2.5  Doing it in code, and checking the rule is right")

    w.code([
        "$ python3 tools/hazard.py \"A B' + B C\"",
        "",
        "  1 static-1 logic hazard(s) found:",
        "",
        "    B changes 1 -> 0   with  A=1, C=1",
        "      before the change, the output is held up by : B C",
        "      after  the change, the output is held up by : A B'",
        "      no single term covers both, so the handover is a race.",
        "      ADD the redundant term:  A C",
        "",
        "  hazard-free cover:",
        "      F = A B'  +  B C  +  A C",
        "",
        "  checking the proposed cover:",
        "    remaining static-1 hazards : 0",
        "    truth table unchanged      : yes"])

    w.para([N("The adjacency rule is a claim about "), B("logic"),
            N(". Whether an output glitches is a fact about "), B("time"),
            N(". Those are different things, so the analyser's self-test checks one "
              "against the other rather than trusting the textbook:")])

    w.code([
        "$ python3 tools/hazard.py --selftest",
        "",
        "D. the combinatorial rule agrees with a delay simulation",
        "   (random functions; the rule and the timeline must never differ)",
        "  static-1 transitions cross-checked           PASS  (got True, want True)",
        "  disagreements between rule and simulation    PASS  (got 0, want 0)",
        "",
        "E. the suggested fix always works, and never changes the function",
        "  fixes that left a hazard behind              PASS  (got 0, want 0)",
        "  fixes that altered the truth table           PASS  (got 0, want 0)",
        "",
        "SELF-TEST PASSED"])

    w.callout("What section D actually proves", [
        [N("It generates hundreds of random covers. For every single-variable "
           "transition between two 1-cells it asks the covering rule, and separately "
           "builds a timeline with randomised per-gate switching times to see whether "
           "an instant exists when every term is off. Over several thousand "
           "transitions the two answers never differed.")],
        [N("Note the word "), B("randomised"),
         N(". An earlier version of that check used one fixed delay profile and "
           "reported a disagreement — because a fixed profile only ever exposes the "
           "glitch in one direction. A hazard is the POSSIBILITY of a dip, so the "
           "check has to search delay assignments, not assume one.")],
    ], color=TEAL)

    w.h2("2.6  Measuring it: the glitch detector")

    w.image("glitch_detector", width=6.4)

    w.para([N("Looking for glitches by eye in a waveform viewer does not scale, does "
              "not go in a regression, and does not tell you when you have finished. "
              "The detector in "), M("hazards/tb_hazard.v"),
            N(" walks every single-variable input transition, counts how many times "
              "the output changes, and compares that with how many times it should:")])
    w.bullets([
        [N("steady value before "), B("=="), N(" steady value after  →  expect "),
         B("0"), N(" changes")],
        [N("steady value before "), B("!="), N(" steady value after  →  expect "),
         B("1"), N(" change")],
        [N("more than expected  →  a glitch, named and counted")],
    ])
    w.para([N("It also records the settled truth table, so that a \"fix\" which "
              "quietly changes the function cannot pass as a fix.")])

    w.h2("2.7  The results, and the surprise in row five")

    w.image("hazard_results", width=6.5)

    w.para([N("Six designs, 24 transitions examined in each. The first three rows "
              "behave exactly as the theory predicts: the textbook cover glitches "
              "once, the consensus term clears it, and the control is clean. Rows four "
              "to six are where it gets interesting.")])

    w.h3("Why hz_dynamic_fix went from 5 glitches to 4, not to 0")
    w.para([N("hz_dynamic feeds the hazardous expression into an XOR where B "
              "reconverges by a faster route. Adding the consensus term inside removed "
              "the dynamic hazard and left four static ones. Those have a different "
              "cause entirely:")])
    w.code([
        "with A=0, C=1 :   s = A B' + B C + A C  =  0 + B + 0  =  B",
        "with A=1, C=0 :   s = A B' + B C + A C  =  B' + 0 + 0 =  B'",
        "",
        "so  f = s XOR b   is computing   B XOR B-delayed,",
        "which spikes on every edge of B, whatever the cover looks like."])
    w.callout("The limit of the technique", [
        [N("That is reconvergent fanout with unequal path delays. No redundant product "
           "term can repair it, because the cover is not what is wrong — the structure "
           "is. hz_flat_fix.v flattens the function to two levels and re-covers it, "
           "and the detector reports CLEAN.")],
        [B("\"Add the consensus term\" cures a two-level logic hazard, and only that. "
           "Knowing the limit of a technique is part of knowing the technique.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("2.8  Does a glitch actually matter?")

    w.image("where_hazards_matter", width=6.5)

    w.para([N("One glitchy signal was fed to three consumers, with the glitch placed "
              "80 ns before any clock edge — the friendliest possible case for the "
              "usual reassurance that synchronous design tolerates glitches. "
              "It is true for the first consumer and false for the other two.")])

    w.callout("The rule, stated properly", [
        [B("A glitch is harmless ONLY where a clock edge samples the signal after it "
           "has settled.")],
        [N("Safe: data into a normally-clocked flip-flop; combinational logic between "
           "two registers in the same clock domain.")],
        [N("Unsafe: logic driving a clock (every glitch is a clock edge); an "
           "asynchronous reset or set; a latch enable, since a latch is transparent "
           "while its enable is high; a handshake crossing into another clock domain.")],
        [N("And everywhere, a cost: every glitch charges and discharges capacitance. "
           "On a wide bus that switches spuriously, glitch power is real and "
           "measurable.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("2.9  Races")

    w.image("races", width=6.4)

    w.para([N("A hazard is about one output taking a wrong value. A "), B("race"),
            N(" is about a state machine landing in the wrong state, because two or "
              "more state variables changed in response to one input change and the "
              "order was not fixed.")])

    w.table(["Name", "What happens", "Is it a bug?"],
            [["Non-critical race", "the variables change in either order and the "
              "machine still reaches the intended state", "no — untidy, but correct"],
             ["Critical race", "the final state depends on which variable changed "
              "first", "yes, and it is delay-dependent"],
             ["Essential hazard", "an input change races its own inverted copy through "
              "the feedback path, so the machine effectively sees the input twice",
              "yes — cured by delay in the feedback, not by logic"]],
            widths=[1.4, 3.4, 2.0], size=9.2, bold_cols=(0,), align_center=False)

    w.image("races_cure", width=6.4)

    w.callout("What synchronous design buys you, and what it does not", [
        [N("All three of those need state to change in response to an input change. "
           "Put a clock in charge and state changes only on an edge, by which time "
           "everything has settled — so an entire class of problem disappears.")],
        [N("What it does not buy you is the boundaries: logic that drives a clock, a "
           "latch enable or an asynchronous reset, and any genuinely asynchronous "
           "interface. There is no clock refereeing those, and hazards there are still "
           "yours to remove.")],
    ], color=NAVY, bar="0E2A47")

    w.callout("Part 2 self-check", [
        [N("1.  State the adjacency rule from memory.")],
        [N("2.  How do you construct the term that fixes a static-1 hazard?")],
        [N("3.  Why can a two-level AND-OR circuit not have a static-0 hazard?")],
        [N("4.  hz_dynamic_fix still glitches four times. Why does the consensus term "
           "not help?")],
        [N("5.  Give three places where a glitch is genuinely dangerous.")],
        [N("6.  What is the difference between a critical and a non-critical race?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
