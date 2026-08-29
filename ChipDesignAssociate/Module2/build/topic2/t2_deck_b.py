# -*- coding: utf-8 -*-
"""Module 2 Topic 2 deck — Theory 2: the RTL design process and methodology."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 2", "The RTL Design Process and Methodology",
        "Methodology is the hardest thing to teach, because the honest version "
        "is a list of habits and the dishonest version is a list of slogans.",
        ["The design flow, and where this topic sits in it",
         "The synthesisable subset — measured, not asserted",
         "The bug that makes simulation and silicon disagree",
         "Seven coding rules, and a tool that checks them",
         "Micro-architecture: the decisions RTL cannot make for you"],
        accent=VIOLET)

    # ------------------------------------------------------------ the flow
    s = d.slide("2.1 · THE FLOW", "The RTL Design Flow")
    y = d.image(s, TOP - 45720, "design_flow", 4950000)
    d.lead(s, y + G, [[R("Every arrow points both ways in practice: a timing failure "
                         "sends you back to the RTL, a synthesis surprise back to the "
                         "micro-architecture.", s=12.0)]], h=228600)

    s = d.slide("2.1 · THE FLOW", "Executed, Not Described")
    y = d.image(s, TOP - 45720, "flow_executed", 4950000)
    d.lead(s, y + G, [[R("make flow  stops at the first stage that fails. That is what "
                         "makes it a methodology rather than a diagram.", b=True,
                         c=NAVY, s=12.0)]], h=274320)

    # -------------------------------------------------------- the subset
    s = d.slide("2.2 · THE SUBSET", "Which Verilog Actually Synthesises")
    y = d.image(s, TOP - 45720, "synth_subset", 4950000)
    d.lead(s, y + G, [[R("Eleven constructs, run through a real synthesiser. "
                         "The table is measured, not remembered.", s=12.0)]],
           h=228600)

    s = d.slide("2.2 · THE SUBSET", "Three Rows Worth Discussing", accent=AMBER)
    y = d.cols(s, TOP, [
        ("371 cells against 0",
         [[R("a / b  where b is a signal builds a full combinational divider — 371 "
             "cells.")],
          [R("a / 4  builds nothing at all. It is a rename of wires.")],
          [R("Same operator. The difference is entirely what you divided BY.",
             b=True, c=NAVY)]], RED, CARD_R),
        ("#5 vanished silently",
         [[R("A delay is a simulation instruction. Silicon has no way to wait five "
             "time units.")],
          [R("Synthesis ignored it and built the gate. Your simulation and your chip "
             "now behave differently.")]], AMBER, CARD_A),
        ("initial was accepted",
         [[R("Yosys targets FPGAs, where the bitstream really does initialise the "
             "flops.")],
          [R("An ASIC flow would not. This is how code that works on an FPGA fails on "
             "an ASIC.", b=True, c=NAVY)]], VIOLET, CARD)],
        h=2560320)

    d.card(s, y + G, "The habit this table is for",
           [[R("Before you write a construct you are unsure about, synthesise a "
               "ten-line module containing only that construct and read what came "
               "out. It takes two minutes and it is the only way to actually know.")]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------- inferred latch
    s = d.slide("2.3 · THE LATCH", "The Most Common RTL Bug There Is", accent=RED)
    y = d.image(s, TOP - 45720, "latch_inference", 4950000)
    d.lead(s, y + G, [[R("It is not an error. The tool builds it, mentions it in a log "
                         "nobody reads, and hands you the design.", b=True, c=RED,
                         s=12.0)]], h=274320)

    s = d.slide("2.3 · THE LATCH", "Why a Latch In the Middle of Your Logic Hurts")
    y = d.table(s, TOP,
                ["", "A flip-flop", "A latch"],
                [["captures", "on the clock EDGE", "while the enable is HIGH"],
                 ["is transparent", "never", "for the whole enable window"],
                 ["timing analysis", "one clean check per edge",
                  "time-borrowing; much harder to analyse"],
                 ["in a scan chain", "standard", "usually needs special handling"],
                 ["you asked for it", "yes, by writing posedge",
                  "no — you forgot an else"]],
                [2377440, 4297680, 4572000], rh=329184, bold_cols=(0,))

    y = d.card(s, y + G, "So the rule is mechanical",
               [[R("In a combinational block, assign every output on every path. "
                   "An if needs an else; a case needs a default. If you would rather "
                   "not write them out, assign a default value at the top of the block "
                   "and let later assignments override it.")]],
               accent=NAVY, h=1005840)

    d.lead(s, y + G, [[R("Rules L005 and L006 of the linter catch this, and "
                         "make lintcheck confirms the linter agrees with Yosys on "
                         "every file.", s=12.0)]], h=274320)

    # ------------------------------------------------ sim/synth mismatch
    s = d.slide("2.4 · THE WORST BUG", "When Simulation and Silicon Disagree",
                accent=RED)
    y = d.image(s, TOP - 45720, "sim_synth_mismatch", 4950000)
    d.lead(s, y + G, [[R("One disagreement in six — and nothing anywhere reported an "
                         "error.", b=True, c=RED, s=12.0)]], h=228600)

    s = d.slide("2.4 · THE WORST BUG", "Why This Class of Bug Is Special")
    y = d.lead(s, TOP, [[
        R("Most bugs are found by testing. This one cannot be, because ", s=13.0),
        R("the thing you are testing is not the thing that will be built", b=True,
          c=RED, s=13.0),
        R(". Every test you write passes, and the chip still fails.", s=13.0)]],
        h=594360)

    y = d.table(s, y + G,
                ["Cause", "What simulation does", "What synthesis does"],
                [["incomplete sensitivity list",
                  "the block sleeps; the output goes stale",
                  "ignores the list; builds the logic"],
                 ["# delays in RTL", "waits the specified time",
                  "ignores them entirely"],
                 ["initial block (ASIC)", "sets the value at time zero",
                  "ignores it; the flop powers up unknown"],
                 ["blocking in a clocked block",
                  "result depends on evaluation order",
                  "builds one specific circuit"]],
                [3383280, 3931920, 3931920], rh=329184, bold_cols=(0,))

    d.card(s, y + G, "All four have the same cure",
           [[R("Use always @* and never a hand-written sensitivity list. No delays "
               "in RTL. A real reset instead of an initial block. Non-blocking in "
               "clocked blocks. Then lint for all four, so that nobody has to "
               "remember.", b=True, c=GREEN)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------------- rules
    s = d.slide("2.5 · THE RULES", "Seven Rules, Checked By a Tool")
    y = d.image(s, TOP - 45720, "lint_rules", 4950000)
    d.lead(s, y + G, [[R("A linter that cries wolf gets switched off. One that stays "
                         "quiet is worse than none at all.", b=True, c=NAVY,
                         s=12.0)]], h=228600)

    s = d.slide("2.5 · THE RULES", "The Coding Standard, In One Place")
    y = d.image(s, TOP - 45720, "coding_rules", 4950000)
    d.lead(s, y + G, [[R("None of these are style preferences. Every one exists "
                         "because breaking it produces a design that simulates "
                         "differently from the way it is built.", s=12.0)]],
           h=274320)

    # -------------------------------------------------- micro-architecture
    s = d.slide("2.6 · MICRO-ARCHITECTURE", "The Decisions RTL Cannot Make For You")
    y = d.image(s, TOP - 45720, "partitioning", 4950000)
    d.lead(s, y + G, [[R("Make these on paper, before the first line of RTL. "
                         "A synthesiser will faithfully build whatever you chose.",
                         b=True, c=AMBER, s=12.0)]], h=228600)

    s = d.slide("2.7 · REUSE", "Writing RTL That Someone Else Can Use")
    y = d.image(s, TOP - 45720, "reuse", 4300000)
    d.card(s, y + G, "Module 2's fourth terminal outcome asks for this by name",
           [[R("\"Emulate, debug and characterise reusable IPs.\" Reuse is not "
               "something you add to a design afterwards — it is a set of decisions "
               "you take while writing it, and every one of them is listed above.",
               s=12.0)]],
           accent=NAVY, h=822960)

    # ------------------------------------------------------ coding style
    s = d.slide("2.8 · STYLE", "One Function, Three Coding Styles")
    y = d.image(s, TOP - 45720, "mux_styles", 4950000)
    d.lead(s, y + G, [[R("Proved equivalent by SAT — and still three different "
                         "netlists.", b=True, c=RED, s=12.0)]], h=228600)

    s = d.slide("2.8 · STYLE", "What To Take From That")
    y = d.cols(s, TOP, [
        ("EQUIVALENT is not IDENTICAL",
         [[R("A formal equivalence proof answers exactly one question: do these "
             "two descriptions compute the same function?")],
          [R("It says nothing about area, nothing about timing and nothing about "
             "power. Those are separate questions with separate tools.",
             b=True, c=NAVY)]], RED, CARD_R),
        ("MEASURE YOUR OWN TOOL",
         [[R("The claim 'the optimiser flattens the difference' is the most "
             "repeated statement in RTL teaching, and on this toolchain it is "
             "false: 3, 6 and 10 cells.")],
          [R("A different synthesiser may well close the gap. Find out rather "
             "than assume.", b=True, c=NAVY)]], AMBER, CARD_A),
        ("SO WHICH DO YOU WRITE?",
         [[R("Whichever reads best to the next person, which is usually the "
             "case statement for anything with more than three branches.")],
          [R("Then measure, and only reach for the terse form if the block is "
             "actually on a critical path.")]], GREEN, CARD_G)],
        h=2743200)

    d.card(s, y + G, "Why the three differ at all",
           [[R("The conditional expression hands sel[1] and sel[0] straight to the "
               "multiplexer selects. The case and if/else versions ask the tool to "
               "build equality comparators against 2'b00, 2'b01 and so on, and then "
               "to work out for itself that those comparisons ARE the select bits. "
               "It gets part of the way.")]],
           accent=NAVY, h=868680)

    s = d.slide("THEORY 2 · CHECKPOINT", "Nine Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "Name the first four stages of the flow.",
                  "spec, micro-architecture, RTL coding, lint"],
                 ["2", "Why lint before simulating?",
                  "it costs seconds and catches what tests cannot"],
                 ["3", "What builds a latch?",
                  "a combinational block that does not assign on every path"],
                 ["4", "a / b against a / 4 — what did they cost?",
                  "371 cells against 0"],
                 ["5", "Why is an incomplete sensitivity list so dangerous?",
                  "simulation and synthesis then build different circuits"],
                 ["6", "What does # do in synthesisable RTL?",
                  "nothing at all — it is silently ignored"],
                 ["7", "Name three decisions synthesis will not make for you.",
                  "cycle count, register placement, sharing, interface"],
                 ["8", "Does formal equivalence say anything about area?",
                  "no — equivalent is not the same as identical"],
                 ["9", "The three mux styles: how many cells each?",
                  "3, 6 and 10 — style did reach the netlist here"]],
                [548640, 5029200, 5669280], rh=310896, bold_cols=(0,), size=11.0)
    d.lead(s, y + G, [[R("Theory 3 is about the patterns every real block is built "
                         "from.", b=True, c=GREEN, s=12.0)]], h=274320)
