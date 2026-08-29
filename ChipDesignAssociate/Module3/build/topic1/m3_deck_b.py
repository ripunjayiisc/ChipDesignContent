# -*- coding: utf-8 -*-
"""Module 3 Topic 1 deck — Theory 2: combinational circuit timing, races and
hazards."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 2", "Combinational Circuit Timing: Races and Hazards",
        "The part of this subtopic that Module 2 never covered, and the part "
        "that static timing analysis is structurally unable to see.",
        ["What a hazard is, and why it is a property of the circuit",
         "Static-1, static-0, dynamic — and the function hazard you cannot fix",
         "Finding them: the adjacency rule, on a K-map and in code",
         "Removing them: the consensus term, and where it stops working",
         "Races, and why synchronous design mostly makes them go away"],
        accent=RED)

    # ------------------------------------------------------------- the idea
    s = d.slide("2.1 · THE IDEA", "A Wrong Value On the Way To the Right One",
                accent=RED)
    y = d.image(s, TOP - 45720, "hazard_idea", 4389120)
    d.lead(s, y + G, [[R("Two paths from one input, different delays, one output. "
                         "That is the entire mechanism.", b=True, c=NAVY, s=11)]],
           h=365760)

    # ------------------------------------------------------------ the kinds
    s = d.slide("2.2 · THE KINDS", "Three Kinds of Hazard, and One You Cannot Remove")
    y = d.image(s, TOP - 45720, "hazard_kinds", 4389120)
    d.lead(s, y + G, [[R("Logic hazards come from your implementation and can be "
                         "removed. A function hazard belongs to the truth table "
                         "itself.", s=10.5)]], h=365760)

    # -------------------------------------------------------- function hazard
    s = d.slide("2.3 · FUNCTION HAZARDS", "The One No Implementation Can Fix",
                accent=AMBER)
    y = d.lead(s, TOP, [[
        R("Everything else in this section assumes ", s=12.5),
        R("one input changes at a time", b=True, c=NAVY, s=12.5),
        R(". Let two change at once and a new problem appears that no amount of "
          "redundant logic will touch.", s=12.5)]], h=594360)

    y = d.code(s, y + G, [
        "F = A B' + B C        with A = 1, C = 0",
        "",
        "    start   A=1 B=1 C=0    ->  F = 0",
        "    end     A=1 B=0 C=1    ->  F = 1",
        "",
        "Two inputs changed. In between, the circuit necessarily passes through",
        "either A=1 B=1 C=1  (F = 1)  or  A=1 B=0 C=0  (F = 1),",
        "depending which input the wiring happens to deliver first.",
        "",
        "Both intermediate states give F = 1. The output is SUPPOSED to end at 1,",
        "so here it is harmless - but change the example and it need not be."],
        title="two inputs changing at once", size=9.5)

    y = d.cols(s, y + G, [
        ("Why it cannot be fixed",
         [[R("The glitch is in the FUNCTION, not the gates. Every correct "
             "implementation must pass through one of those intermediate states, "
             "because the inputs really do go through them.")]], RED, CARD_R),
        ("What to do instead",
         [[R("Do not change those inputs simultaneously — which, in a synchronous "
             "design, is exactly what a common clock guarantees.")],
          [R("This is one more reason the clocked discipline is worth its cost.")]],
         GREEN, CARD_G)],
        h=1554480)

    d.lead(s, y + G, [[R("From here on: one input at a time, and every hazard we "
                         "discuss is a LOGIC hazard.", b=True, c=NAVY, s=10.5)]],
           h=274320)

    # ------------------------------------------------------------- the race
    s = d.slide("2.4 · THE MECHANISM", "The Race, In Time")
    y = d.image(s, TOP - 45720, "hazard_race", 4846320)
    d.lead(s, y + G, [[R("B C switches off as soon as B falls. A B' cannot switch on "
                         "until B has been through the inverter. In between, nothing "
                         "is holding F up.", s=10.5)]], h=274320)

    # ------------------------------------------------------------ the rule
    s = d.slide("2.5 · THE RULE", "How To Find One Without Simulating Anything")
    y = d.card(s, TOP, "The adjacency rule, in one sentence",
               [[R("Take two input patterns that differ in exactly ONE variable and "
                   "both give F = 1. If no single product term covers both of them, "
                   "the circuit has a static-1 logic hazard on that transition.",
                   b=True, c=NAVY, s=12)]],
               accent=NAVY, h=822960)

    y = d.code(s, y + G, [
        "F = A B' + B C          A=1, C=1, and B changes",
        "",
        "    B=1 :  F = 1, held up by  B C",
        "    B=0 :  F = 1, held up by  A B'",
        "",
        "    Does one term cover BOTH?",
        "        A B'  needs B=0  ->  covers only the second",
        "        B C   needs B=1  ->  covers only the first",
        "    No. So the output is handed from one term to the other, and whether",
        "    it dips depends on which gate wins."],
        size=9.5)

    d.card(s, y + G, "Why this is the right test",
           [[R("If some term is 1 for both patterns, that term does not change at all "
               "during the transition — so it holds the output up throughout and no "
               "delay assignment can produce a dip. If no term does, then one must "
               "switch off while another switches on, and the order is decided by "
               "delays you do not control.")]],
           accent=TEAL, h=1005840)

    # ------------------------------------------------------------- the K-map
    s = d.slide("2.6 · ON A K-MAP", "Adjacent 1s In Different Loops")
    y = d.image(s, TOP - 45720, "hazard_kmap", 4663440)
    d.lead(s, y + G, [[R("Two 1-cells side by side with no single loop around both. "
                         "That is the same test, drawn.", b=True, c=NAVY, s=10.5)]],
           h=274320)

    # ---------------------------------------------------------- the fix
    s = d.slide("2.7 · THE FIX", "The Consensus Term")
    y = d.image(s, TOP - 45720, "consensus_fix", 4846320)
    d.lead(s, y + G, [[R("A term that covers no new 1s, changes nothing in the truth "
                         "table, and holds the output up through the handover.",
                         s=10.5)]], h=274320)

    # ----------------------------------------------- redundancy is the point
    s = d.slide("2.7 · THE FIX", "Redundant Is Not a Criticism — It Is the Requirement")
    y = d.lead(s, TOP, [[
        R("The consensus term is ", s=12.5),
        R("logically redundant by construction", b=True, c=NAVY, s=12.5),
        R(". Delete it and the truth table is identical. That is not a flaw in the "
          "fix — it is what makes the fix safe, and it is also what makes it fragile.",
          s=12.5)]], h=594360)

    y = d.cols(s, y + G, [
        ("Why redundancy is required",
         [[R("A term that changed the function would not be a fix, it would be a bug.")],
          [R("The only way to hold the output up without altering what the circuit "
             "computes is to add cover that is already covered.")]], GREEN, CARD_G),
        ("Why it will not survive",
         [[R("Removing redundancy is precisely what a logic optimiser exists to do.")],
          [R("Write the consensus term in RTL and synthesis will delete it — measured "
             "in Theory 4 of this session.", b=True, c=RED)]], RED, CARD_R)],
        h=1737360)

    d.card(s, y + G, "How to find the term, every time",
           [[R("Take the two input patterns. Write down every variable they agree on, "
               "at the value they agree on. Drop the one that changed. That product is "
               "the term to add — and tools/hazard.py prescribes it automatically.")]],
           accent=TEAL, h=822960)

    # ------------------------------------------------------ the analyser
    s = d.slide("2.8 · THE ANALYSER", "Doing It In Code")
    y = d.code(s, TOP, [
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
        "    truth table unchanged      : yes"],
        size=9.5)

    d.card(s, y + G, "It checks its own answer, and that matters",
           [[R("A tool that proposes a fix without verifying it is a tool that will "
               "eventually propose a wrong one. This one re-runs the analysis on the "
               "patched cover and re-derives the truth table before it prints.")]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ------------------------------------------------------- the self-test
    s = d.slide("2.8 · THE ANALYSER", "How We Know the Rule Is Actually Right",
                accent=GREEN)
    y = d.lead(s, TOP, [[
        R("The adjacency rule is a claim about ", s=12),
        R("logic", b=True, c=NAVY, s=12),
        R(". Whether an output glitches is a fact about ", s=12),
        R("time", b=True, c=RED, s=12),
        R(". Those are different things, so the analyser's self-test checks one "
          "against the other.", s=12)]], h=594360)

    y = d.code(s, y + G, [
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
        "SELF-TEST PASSED"],
        size=9.5)

    d.card(s, y + G, "What that test actually does",
           [[R("It generates hundreds of random covers. For every single-variable "
               "transition it asks the covering rule, and separately builds a timeline "
               "with randomised per-gate delays to see whether a dip is possible. "
               "Over several thousand transitions the two answers never differed.")],
            [R("That is the difference between believing a textbook rule and having "
               "checked it.", b=True, c=GREEN)]],
           accent=GREEN, fill=CARD_G, h=1188720)

    # ---------------------------------------------------------- the detector
    s = d.slide("2.9 · MEASURING", "Finding Glitches By Counting, Not By Squinting")
    y = d.image(s, TOP - 45720, "glitch_detector", 4846320)
    d.lead(s, y + G, [[R("A waveform viewer does not scale, does not go in a "
                         "regression, and does not tell you when you have fixed "
                         "something.", s=10.5)]], h=274320)

    # ------------------------------------------------------------ results
    s = d.slide("2.10 · RESULTS", "Six Designs, One Detector, and a Surprise")
    y = d.image(s, TOP - 45720, "hazard_results", 4846320)
    d.lead(s, y + G, [[R("Read row five before the next slide.", b=True, c=AMBER,
                         s=11)]], h=228600)

    # ------------------------------------------------------- where it stops
    s = d.slide("2.11 · THE LIMIT", "Where \"Add the Consensus Term\" Stops Working",
                accent=RED)
    y = d.lead(s, TOP, [[
        R("hz_dynamic feeds the hazardous expression into an XOR where B reconverges. "
          "The detector reports five glitching transitions. Adding the consensus term "
          "removes ", s=11.5),
        R("one", b=True, c=RED, s=11.5),
        R(" of them.", s=11.5)]], h=502920)

    y = d.table(s, y + G,
                ["design", "glitching transitions", "what changed"],
                [["hz_dynamic", "5  (4 static, 1 dynamic)", "the starting point"],
                 ["hz_dynamic_fix", "4  (4 static)", "consensus term added inside"],
                 ["hz_flat_fix", "0", "flattened to two levels, then re-covered"]],
                [3383280, 3931920, 3931920], rh=320040, bold_cols=(0, 1))

    y = d.card(s, y + G, "Why the four survivors do not respond to a redundant term",
               [[R("With A=0, C=1 the inner expression collapses to a delayed copy of "
                   "B. The circuit is then computing B XOR B-delayed, which spikes on "
                   "every edge no matter what.")],
                [R("That is reconvergent fanout with unequal path delays. The cover is "
                   "not what is wrong — the STRUCTURE is, and only restructuring fixes "
                   "it.", b=True, c=RED)]],
               accent=RED, fill=CARD_R, h=1097280)

    d.lead(s, y + G, [[R("The consensus term cures a two-level logic hazard, and only "
                         "that. Know the limit of your tool.", b=True, c=NAVY,
                         s=10.5)]], h=274320)

    # ---------------------------------------------------------- does it matter
    s = d.slide("2.12 · DOES IT MATTER?", "One Glitchy Signal, Three Consumers")
    y = d.image(s, TOP - 45720, "where_hazards_matter", 4846320)
    d.lead(s, y + G, [[R("The glitch was placed 80 ns before any clock edge — the "
                         "friendliest possible case for the usual reassurance.",
                         s=10.5)]], h=274320)

    s = d.slide("2.12 · DOES IT MATTER?", "The Rule, Stated Properly")
    y = d.card(s, TOP, "Not \"glitches do not matter in synchronous design\"",
               [[R("A glitch is harmless ONLY where a clock edge samples the signal "
                   "after it has settled.", b=True, c=NAVY, s=12)]],
               accent=NAVY, h=685800)

    y = d.cols(s, y + G, [
        ("Safe: level-sampled by a clock",
         [[R("Data into a normally-clocked flip-flop.")],
          [R("Combinational logic between two registers in the same domain.")],
          [R("Here the clock is the referee, and the glitch has a whole cycle to go "
             "away.")]], GREEN, CARD_G),
        ("Unsafe: anything edge-sensitive",
         [[R("Logic driving a CLOCK — every glitch is a clock edge.")],
          [R("An ASYNCHRONOUS reset or set — no clock referees it.")],
          [R("A LATCH enable — the latch is transparent while it is high.")],
          [R("A handshake crossing into another clock domain.")]], RED, CARD_R)],
        h=2011680)

    d.card(s, y + G, "And one cost that applies everywhere",
           [[R("Every glitch charges and discharges capacitance. On a wide bus that "
               "switches spuriously, glitch power is real and measurable — a reason to "
               "care about hazards even where they are functionally harmless.")]],
           accent=AMBER, fill=CARD_A, h=868680)

    # ------------------------------------------------------------- races
    s = d.slide("2.13 · RACES", "When Two State Variables Change At Once")
    y = d.image(s, TOP - 45720, "races", 4937760)
    d.lead(s, y + G, [[R("A hazard is about one output taking a wrong value. A race is "
                         "about a machine landing in the wrong STATE.", s=10.5)]],
           h=228600)

    s = d.slide("2.13 · RACES", "Critical, Non-Critical, and the Essential Hazard")
    y = d.table(s, TOP,
                ["Name", "What happens", "Is it a bug?"],
                [["Non-critical race", "the state variables change in either order and "
                  "the machine still lands in the intended state", "no — untidy, but "
                  "correct"],
                 ["Critical race", "the final state depends on which variable changed "
                  "first", "yes — and it is delay-dependent"],
                 ["Essential hazard", "an input change races its own inverted copy "
                  "through the feedback path, and the machine sees the input twice",
                  "yes — cured by delay in the feedback, not by logic"]],
                [2377440, 5486400, 3383280], rh=457200, bold_cols=(0,))

    d.card(s, y + G, "Why these are asynchronous problems",
           [[R("All three need state to change in response to an INPUT change. Put a "
               "clock in charge and state changes only on an edge, by which time "
               "everything has settled — which is why an entire class of problem "
               "disappears the moment you adopt synchronous discipline.")]],
           accent=NAVY, h=1005840)

    s = d.slide("2.14 · THE CURE", "What Synchronous Design Buys You, and What It "
                                   "Does Not")
    y = d.image(s, TOP - 45720, "races_cure", 4663440)
    d.lead(s, y + G, [[R("It buys you almost everything in this section — except at "
                         "the boundaries, where there is no clock to referee.",
                         b=True, c=AMBER, s=10.5)]], h=274320)

    # ------------------------------------------------------- checkpoint
    s = d.slide("THEORY 2 · CHECKPOINT", "Ten Questions Before We Move On",
                accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "Hazard or glitch — which is a property of the circuit?",
                  "the hazard; the glitch is one event in one run"],
                 ["2", "Which hazard can a two-level AND-OR circuit have?",
                  "static-1 only"],
                 ["3", "How many levels does a dynamic hazard need?", "three or more"],
                 ["4", "What is a function hazard?",
                  "two inputs change at once and the function itself demands a glitch"],
                 ["5", "State the adjacency rule.",
                  "two 1-cells one variable apart, covered by no single term"],
                 ["6", "How do you build the fixing term?",
                  "the literals both patterns agree on, minus the one that changed"],
                 ["7", "Why will synthesis delete it?", "it is redundant, by design"],
                 ["8", "When does the consensus term NOT help?",
                  "reconvergent fanout — a structural problem, not a cover one"],
                 ["9", "Where is a glitch genuinely dangerous?",
                  "clocks, async resets, latch enables, domain crossings"],
                 ["10", "Why can STA not find any of this?",
                  "it measures one path; a hazard needs two"]],
                [548640, 5303520, 5394960], rh=283464, bold_cols=(0,), size=9.5)
    d.lead(s, y + G, [[R("If question 8 or 10 is fuzzy, say so now — Theory 3 assumes "
                         "both.", b=True, c=GREEN, s=10.5)]], h=274320)
