# -*- coding: utf-8 -*-
"""Module 2 Topic 2 deck - Theory 2: the language you say it in."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 2", "The Language You Say It In",
        "Theory 1 was about the hardware. This section is about how you "
        "write it down - and the first thing to unlearn is that this is "
        "programming.",
        ["Why an HDL is not a programming language",
         "Everything happens at once",
         "The parts of a module, and the word reg that confuses everyone",
         "<= and =, and why the clock edge forces the difference",
         "How a simulator runs an HDL",
         "Verilog and VHDL as reference cards, and both actually run"],
        accent=TEAL)

    s = d.slide("2.1 · NOT A PROGRAM", "An HDL Is Not a Programming Language")
    y = d.image(s, TOP - 45720, "what_is_hdl", 4950000)
    d.lead(s, y + G, [[R("You are not writing instructions for a machine to follow. "
                         "You are writing a description of a machine.", b=True,
                         c=NAVY, s=12.0)]], h=274320)

    s = d.slide("2.2 · CONCURRENCY", "Everything Happens At Once")
    y = d.image(s, TOP - 45720, "concurrency", 4950000)
    d.lead(s, y + G, [[R("Write those three assign lines in any order you like — the "
                         "circuit is identical.", s=12.0)]], h=274320)

    s = d.slide("2.3 · ANATOMY", "The Parts of a Verilog Module")
    y = d.image(s, TOP - 45720, "module_anatomy", 4950000)
    d.lead(s, y + G, [[R("reg does not mean register. What creates a flip-flop is "
                         "assigning inside always @(posedge clk) — nothing else.",
                         b=True, c=AMBER, s=12.0)]], h=228600)

    # --------------------------------------- the two assignment operators
    s = d.slide("2.4 · <= AND =", "Where This Rule Comes From", accent=VIOLET)
    y = d.card(s, TOP, "Go back to the clock edge in Theory 1",
               [[R("Every flip-flop in the design captures at the SAME instant. "
                   "None of them can see what any other one is about to become "
                   "— they all see the values that were on the wires just "
                   "before the edge.", s=12.5)],
                [R("Non-blocking assignment is how you write that down. It is "
                   "not a style convention; it is the notation for physical "
                   "simultaneity.", b=True, c=VIOLET, s=12.5)]],
               accent=VIOLET, h=1371600)

    y = d.cols(s, y + G, [
        ("THE HARDWARE",
         [[R("All registers sample at once, from the values already settled "
             "on their inputs.", s=12.0)]], VIOLET, CARD),
        ("THE NOTATION",
         [[R("<= reads every right-hand side first, then updates every "
             "left-hand side together.", s=12.0)]], NAVY, CARD),
        ("GET IT WRONG",
         [[R("= makes each line finish before the next starts, so a later "
             "line sees a value that does not exist yet.", s=12.0)]], RED,
         CARD_R)],
        h=1554480)

    d.lead(s, y + G, [[R("The operator is a consequence of the physics, not a "
                         "preference.", b=True, c=NAVY, s=12.0)]], h=274320)

    s = d.slide("2.4 · <= AND =", "The Two Assignment Operators, and Why It Matters")
    y = d.image(s, TOP - 45720, "nonblocking", 4950000)
    d.lead(s, y + G, [[R("The mirror-image mistake matters too: <= in a "
                         "combinational block simulates like a register while "
                         "synthesis builds plain logic.", s=12.0)]], h=274320)

    s = d.slide("2.4 · <= AND =", "The Swap, Worked Through")
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
        size=11.2)

    d.card(s, y + G, "Why the rule is absolute rather than stylistic",
           [[R("Two clocked blocks using blocking assignments can see each other's "
               "half-updated values, and which one wins depends on the order the "
               "simulator happens to evaluate them in — an order the language "
               "standard deliberately does not fix.")],
            [R("Non-blocking assignment exists precisely to make that race "
               "impossible.", b=True, c=NAVY)]],
           accent=NAVY, h=1097280)

    s = d.slide("2.4 · <= AND =", "And What Each One Actually Builds",
                accent=RED)
    y = d.image(s, TOP - 45720, "blocking_measured", 4950000)
    d.lead(s, y + G, [[R("Three flip-flops against one. Nothing illegal was "
                         "written, so nothing warned.", b=True, c=RED, s=12.0)]],
           h=228600)

    s = d.slide("2.5 · SIMULATION", "How a Simulator Runs an HDL")
    y = d.image(s, TOP - 45720, "event_simulation", 4950000)
    d.lead(s, y + G, [[R("The order blocks are evaluated in is genuinely unspecified. "
                         "That is why non-blocking assignment exists.", s=12.0)]],
           h=228600)

    # --------------------------------------------------- reference cards
    s = d.slide("2.6 · REFERENCE", "Verilog On One Page")
    y = d.image(s, TOP - 45720, "verilog_card", 4950000)
    d.lead(s, y + G, [[R("Not the whole language — the part that synthesises, "
                         "which is much smaller.", s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "Verilog: Blocks and Operators")
    y = d.image(s, TOP - 45720, "verilog_card2", 4950000)
    d.lead(s, y + G, [[R("Three kinds of block, and the operators you will "
                         "actually use.", s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "VHDL On One Page")
    y = d.image(s, TOP - 45720, "vhdl_card", 4950000)
    d.lead(s, y + G, [[R("Everything on this page has an exact counterpart on the "
                         "previous one.", s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "VHDL: Types, and What They Catch")
    y = d.image(s, TOP - 45720, "vhdl_card2", 4950000)
    d.lead(s, y + G, [[R("The type system is the real difference between the two "
                         "languages.", s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "Verilog to VHDL, Line For Line  (1 of 2)")
    y = d.image(s, TOP - 45720, "lang_mapping", 4950000)
    d.lead(s, y + G, [[R("Learn one and you can read the other in an afternoon. "
                         "These two tables are the afternoon.", b=True, c=NAVY,
                         s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "Verilog to VHDL, Line For Line  (2 of 2)")
    y = d.image(s, TOP - 45720, "lang_mapping2", 4950000)
    d.lead(s, y + G, [[R("Nothing in this topic depends on which one you use.",
                         s=12.0)]], h=228600)

    s = d.slide("2.6 · REFERENCE", "What a Testbench Is Made Of")
    y = d.image(s, TOP - 45720, "testbench_anatomy", 4950000)
    d.lead(s, y + G, [[R("Topic 5 covers verification properly. These six parts are "
                         "the minimum you need to finish Topic 2.", s=12.0)]],
           h=228600)

    s = d.slide("2.7 · TWO LANGUAGES", "Verilog and VHDL, Side By Side")
    y = d.image(s, TOP - 45720, "verilog_vhdl", 4950000)
    d.lead(s, y + G, [[R("None of those differences are about hardware. Both describe "
                         "registers, logic and hierarchy; both synthesise to the same "
                         "gates.", s=12.0)]], h=228600)

    s = d.slide("2.7 · TWO LANGUAGES", "Both Designs, In Both Languages, Actually "
                "Run")
    y = d.image(s, TOP - 45720, "two_languages_result", 4250000)
    d.card(s, y + G, "Not \"they look similar\"",
           [[R("Both transcripts were compared line by line by diff, and there was "
               "nothing to report. The state machine is the interesting one: VHDL "
               "gives the states a real enumerated TYPE, so an illegal state will "
               "not compile. Verilog gives them numbers.", s=12.0)]],
           accent=GREEN, fill=CARD_G, h=868680)

    s = d.slide("2.8 · WHICH ONE", "Which HDL Should You Learn?")
    y = d.image(s, TOP - 45720, "hdl_choose", 4950000)
    d.lead(s, y + G, [[R("Learn the concepts. The notation follows in an afternoon.",
                         b=True, c=GREEN, s=12.0)]], h=228600)

    s = d.slide("THEORY 2 · CHECKPOINT", "Seven Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "Name the biggest difference between an HDL and a program.",
                  "everything in an HDL runs all the time, concurrently"],
                 ["2", "Does the order of assign statements matter?",
                  "no — they describe hardware that exists together"],
                 ["3", "What does reg actually mean?",
                  "assigned in a procedural block; NOT a flip-flop"],
                 ["4", "Why is the evaluation order unspecified?",
                  "the standard leaves it free; <= makes it not matter"],
                 ["5", "Verilog or VHDL?",
                  "either — the concepts are identical, and the lab proves it"],
                 ["6", "What does VHDL catch that Verilog does not?",
                  "illegal states, non-exhaustive cases, width mismatches"],
                 ["7", "Where must a testbench's expected answer come from?",
                  "the stimulus — never from the design under test"]],
                [548640, 5029200, 5669280], rh=310896, bold_cols=(0,), size=11.2)

