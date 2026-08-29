# -*- coding: utf-8 -*-
"""Module 2 Topic 2 deck — Theory 3 (HDLs) and the practical component."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 4", "Introduction to Hardware Description Languages",
        "The syllabus says \"HDLs such as Verilog or VHDL\". The word doing "
        "the work is OR.",
        ["Why an HDL is not a programming language",
         "Everything happens at once",
         "The parts of a module, and the word reg that confuses everyone",
         "Verilog and VHDL as reference cards, and a line-for-line mapping",
         "The anatomy of a testbench that checks itself",
         "Both languages actually run, and their transcripts diffed"],
        accent=TEAL)

    s = d.slide("4.1 · NOT A PROGRAM", "An HDL Is Not a Programming Language")
    y = d.image(s, TOP - 45720, "what_is_hdl", 4950000)
    d.lead(s, y + G, [[R("You are not writing instructions for a machine to follow. "
                         "You are writing a description of a machine.", b=True,
                         c=NAVY, s=12.0)]], h=274320)

    s = d.slide("4.2 · CONCURRENCY", "Everything Happens At Once")
    y = d.image(s, TOP - 45720, "concurrency", 4950000)
    d.lead(s, y + G, [[R("Write those three assign lines in any order you like — the "
                         "circuit is identical.", s=12.0)]], h=274320)

    s = d.slide("4.3 · ANATOMY", "The Parts of a Verilog Module")
    y = d.image(s, TOP - 45720, "module_anatomy", 4950000)
    d.lead(s, y + G, [[R("reg does not mean register. What creates a flip-flop is "
                         "assigning inside always @(posedge clk) — nothing else.",
                         b=True, c=AMBER, s=12.0)]], h=228600)

    s = d.slide("4.4 · SIMULATION", "How a Simulator Runs an HDL")
    y = d.image(s, TOP - 45720, "event_simulation", 4950000)
    d.lead(s, y + G, [[R("The order blocks are evaluated in is genuinely unspecified. "
                         "That is why non-blocking assignment exists.", s=12.0)]],
           h=228600)

    # --------------------------------------------------- reference cards
    s = d.slide("4.5 · REFERENCE", "Verilog On One Page")
    y = d.image(s, TOP - 45720, "verilog_card", 4950000)
    d.lead(s, y + G, [[R("Not the whole language — the part that synthesises, "
                         "which is much smaller.", s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "Verilog: Blocks and Operators")
    y = d.image(s, TOP - 45720, "verilog_card2", 4950000)
    d.lead(s, y + G, [[R("Three kinds of block, and the operators you will "
                         "actually use.", s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "VHDL On One Page")
    y = d.image(s, TOP - 45720, "vhdl_card", 4950000)
    d.lead(s, y + G, [[R("Everything on this page has an exact counterpart on the "
                         "previous one.", s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "VHDL: Types, and What They Catch")
    y = d.image(s, TOP - 45720, "vhdl_card2", 4950000)
    d.lead(s, y + G, [[R("The type system is the real difference between the two "
                         "languages.", s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "Verilog to VHDL, Line For Line  (1 of 2)")
    y = d.image(s, TOP - 45720, "lang_mapping", 4950000)
    d.lead(s, y + G, [[R("Learn one and you can read the other in an afternoon. "
                         "These two tables are the afternoon.", b=True, c=NAVY,
                         s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "Verilog to VHDL, Line For Line  (2 of 2)")
    y = d.image(s, TOP - 45720, "lang_mapping2", 4950000)
    d.lead(s, y + G, [[R("Nothing in this topic depends on which one you use.",
                         s=12.0)]], h=228600)

    s = d.slide("4.5 · REFERENCE", "What a Testbench Is Made Of")
    y = d.image(s, TOP - 45720, "testbench_anatomy", 4950000)
    d.lead(s, y + G, [[R("Topic 5 covers verification properly. These six parts are "
                         "the minimum you need to finish Topic 2.", s=12.0)]],
           h=228600)

    s = d.slide("4.6 · TWO LANGUAGES", "Verilog and VHDL, Side By Side")
    y = d.image(s, TOP - 45720, "verilog_vhdl", 4950000)
    d.lead(s, y + G, [[R("None of those differences are about hardware. Both describe "
                         "registers, logic and hierarchy; both synthesise to the same "
                         "gates.", s=12.0)]], h=228600)

    s = d.slide("4.6 · TWO LANGUAGES", "Both Designs, In Both Languages, Actually "
                "Run")
    y = d.image(s, TOP - 45720, "two_languages_result", 4250000)
    d.card(s, y + G, "Not \"they look similar\"",
           [[R("Both transcripts were compared line by line by diff, and there was "
               "nothing to report. The state machine is the interesting one: VHDL "
               "gives the states a real enumerated TYPE, so an illegal state will "
               "not compile. Verilog gives them numbers.", s=12.0)]],
           accent=GREEN, fill=CARD_G, h=868680)

    s = d.slide("4.7 · WHICH ONE", "Which HDL Should You Learn?")
    y = d.image(s, TOP - 45720, "hdl_choose", 4950000)
    d.lead(s, y + G, [[R("Learn the concepts. The notation follows in an afternoon.",
                         b=True, c=GREEN, s=12.0)]], h=228600)

    s = d.slide("THEORY 4 · CHECKPOINT", "Seven Questions", accent=GREEN)
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

    # ==================================================== PRACTICAL section
    d.section_slide(
        "PRACTICAL", "Labs A–N",
        "26 hours, 103 graded exercises, and not one number in this deck that "
        "you cannot reproduce yourself.",
        ["Which tool answers which question, and how to install them",
         "Labs A–D: what RTL means, the ladder, proof, and the subset",
         "Labs E–H: the mismatch, the coding rules, style, and the two pitfalls",
         "Labs I–L: state machines, a controller with a timer, datapath and "
         "controller, and reuse",
         "Labs M–N: two languages, the whole flow, and the vendor tools"],
        accent=GREEN)

    s = d.slide("PRACTICAL · TOOLS", "The Tools, and What Each One Is For")
    y = d.image(s, TOP - 45720, "tool_landscape", 4950000)
    d.lead(s, y + G, [[R("Yosys is the interesting one: the only free tool here that "
                         "both synthesises your RTL and PROVES the netlist matches it.",
                         s=12.0)]], h=228600)

    s = d.slide("PRACTICAL · INSTALL", "Two apt Lines, and the Whole Lab Runs",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "install_required", 4950000)
    d.lead(s, y + G, [[R("No licence, no account, no download manager. Two lines "
                         "and the whole lab runs.", b=True, c=GREEN, s=12.0)]],
           h=228600)

    s = d.slide("PRACTICAL · INSTALL", "The Vendor Tools the Syllabus Names")
    y = d.image(s, TOP - 45720, "install_vendor", 4950000)
    d.lead(s, y + G, [[R("They add a real device library and a flow you will meet at "
                         "work. They add nothing to the concepts.", s=12.0)]],
           h=274320)

    s = d.slide("PRACTICAL · THE FLOW", "Four Questions About One Piece of Code")
    y = d.image(s, TOP - 45720, "lab_flow", 4950000)
    d.lead(s, y + G, [[R("Does it follow the rules? Does it do what the spec says? "
                         "What will be built? Is that still your design?", s=12.0)]],
           h=274320)

    s = d.slide("PRACTICAL · MAP", "Fourteen Parts, Twenty-Six Hours")
    y = d.image(s, TOP - 45720, "lab_map", 4950000)
    d.lead(s, y + G, [[R("A–D build the mental model, E–H the methodology, I–L the "
                         "patterns every block is built from, M–N the connection to "
                         "other languages and real tools.", s=11.5)]], h=182880)

    # ------------------------------------------------------------ labs A-C
    s = d.slide("LABS A–C", "What RTL Means, the Ladder, and Proof")
    y = d.cols(s, TOP, [
        ("A · what RTL means (1 h)",
         [[R("Run make transfer. Follow a single 5 through four registers.")],
          [R("Predict the value in each register on each cycle BEFORE running it.")],
          [R("Deliverable: the table, and why y is 1 on cycle 0.")]], TEAL, CARD),
        ("B · the ladder (2 h)",
         [[R("Write the same full adder at all four levels.")],
          [R("Run make ladder — all four together, exhaustively.")],
          [R("Then synthesise each and compare cell counts.")],
          [R("Deliverable: why behavioural won.")]], NAVY, CARD),
        ("C · proof (2 h)",
         [[R("Run make prove. Three pairs proved equivalent.")],
          [R("Then break the adder yourself and watch the checker catch it.")],
          [R("Deliverable: why 8 patterns was enough here and will not be next "
             "time.")]], VIOLET, CARD)],
        h=3017520)

    d.card(s, y + G, "The exercise that teaches the most is C",
           [[R("Delete a different term from fa_broken.v and predict which input "
               "pattern the solver will find. Getting that prediction right means you "
               "understand both the circuit and the tool.")]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------------ labs D-F
    s = d.slide("LABS D–F", "The Subset, the Mismatch, and the Rules")
    y = d.code(s, TOP, [
        "$ make subset",
        "  s03_latch            OK       1     YES     inferred a LATCH: $_DLATCH_P_",
        "  s08_whileloop        REFUSED  -     -       \"only allowed in constant "
        "functions\"",
        "  s10_divide           OK       371   no      a full combinational divider",
        "  s11_shift            OK       0     no      no logic at all - just wires",
        "",
        "$ make mismatch",
        "  change b (list ASLEEP)   a=1 b=1   RTL y=0   NETLIST y=1  <-- THEY DISAGREE",
        "",
        "$ make lintcheck",
        "  10 files  ·  linter and Yosys agree on every one  ·  0 disagreements"],
        size=11.0)

    y = d.table(s, y + G,
                ["Exercise", "Task"],
                [["D.1", "Predict the cell count for each construct before running "
                         "make subset"],
                 ["D.2", "Add a twelfth construct of your own and predict the result"],
                 ["E.1", "Explain the mismatch to someone who has not seen it, in "
                         "three sentences"],
                 ["F.1", "Add rule L008 to the linter — your choice — and justify it"],
                 ["F.2", "Find a file the linter gets wrong, and say why regexes "
                         "cannot fix it"]],
                [1188720, 10058400], rh=310896, bold_cols=(0,))

    # ------------------------------------------------------------ labs G-H
    s = d.slide("LABS G–H", "Coding Style, and the Two Pitfalls")
    y = d.code(s, TOP, [
        "$ make mux",
        "  mux4_assign vs mux4_case      EQUIVALENT  (proved, 92 SAT variables)",
        "  mux4_assign                     3 cells     0 flip-flops",
        "  mux4_if                         6 cells     0 flip-flops",
        "  mux4_case                      10 cells     0 flip-flops",
        "",
        "$ make pitfalls",
        "  non-blocking version : 0 wrong cycles",
        "  blocking version     : 6 wrong cycles",
        "  shift_nb (non-blocking)         3 cells     3 flip-flops",
        "  shift_bl (blocking)             1 cells     1 flip-flops",
        "  s03_latch   (missing else)      1 cells     *** 1 LATCH INFERRED ***"],
        size=11.0)

    d.table(s, y + G,
            ["Exercise", "Task"],
            [["G.1", "Predict the three cell counts before you run make mux"],
             ["G.2", "Write a fourth style of your own and predict where it lands"],
             ["H.1", "Predict q_bl for the first six cycles, then run it"],
             ["H.2", "Explain in two sentences why no tool warned about shift_bl"],
             ["H.3", "Add an else to s03_latch and confirm the latch disappears"]],
            [1188720, 10058400], rh=310896, bold_cols=(0,))

    # ------------------------------------------------------------ labs I-K
    s = d.slide("LABS I–K", "State Machines, a Timer, and a Datapath")
    y = d.code(s, TOP, [
        "$ make fsm",
        "  matches in the stream : 5      mismatches vs golden  : 0",
        "  PASS - same language, Moore trails Mealy by one cycle,",
        "         and the one-hot encoding is indistinguishable",
        "  seq101_moore  binary           13 cells     2 flip-flops",
        "  seq101_moore  one-hot          30 cells     4 flip-flops",
        "  cycles checked : 40   property violations : 0        (traffic light)",
        "",
        "$ make dpctrl",
        "  golden total : 157   hardware sum : 157",
        "  accum_ctrl   (controller)      10 cells     2 flip-flops",
        "  accum_datapath (datapath)     145 cells    24 flip-flops"],
        size=11.0)

    d.table(s, y + G,
            ["Exercise", "Task"],
            [["I.1", "Draw the state diagram for '110' before you write any code"],
             ["I.2", "Write it in both styles and confirm the one-cycle offset"],
             ["I.3", "Re-encode the Moore machine as gray and measure the cells"],
             ["J.1", "Add a pedestrian request input and a third property to check"],
             ["K.1", "Move the terminal-count test into the controller. What "
                     "breaks, and why is it worse?"]],
            [1188720, 10058400], rh=310896, bold_cols=(0,))

    # -------------------------------------------------------------- lab L
    s = d.slide("LAB L", "From a Module to an IP")
    y = d.code(s, TOP, [
        "$ make reuse",
        "  delayline mismatches : 0        prescaler ratio errors : 0",
        "",
        "  delayline #(W=8, N) synthesised at four different depths:",
        "    N = 1                           8 cells     8 flip-flops",
        "    N = 2                          16 cells    16 flip-flops",
        "    N = 4                          32 cells    32 flip-flops",
        "    N = 8                          64 cells    64 flip-flops"],
        size=11.2)

    y = d.table(s, y + G,
                ["Exercise", "Task"],
                [["L.1", "Predict the cell count for N = 16 before running it"],
                 ["L.2", "Add a bypass parameter that removes the registers "
                         "entirely when N = 0"],
                 ["L.3", "Instantiate counter_n three times to divide by 4096, and "
                         "check the ratio"]],
                [1188720, 10058400], rh=310896, bold_cols=(0,))

    d.card(s, y + G, "L.2 is the one worth arguing about",
           [[R("A generate loop with N = 0 builds nothing, so dout must come "
               "straight from din. Getting that right means understanding that "
               "the parameter is resolved before any hardware exists — which is "
               "the whole point of the lab.")]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ------------------------------------------------------------ labs M-N
    s = d.slide("LABS M–N", "Two Languages, the Whole Flow, and the Vendor Tools")
    y = d.code(s, TOP, [
        "$ make langs",
        "  === Verilog: iverilog ===        === VHDL: ghdl ===",
        "  IDENTICAL over all 18 cycles - including the wrap and the terminal count.",
        "  IDENTICAL over all 17 cycles, detections included.   (the '101' detector)",
        "",
        "$ make flow",
        "  STAGE 2  LINT              0 issues",
        "  STAGE 4  SYNTHESIS         12 cells",
        "  STAGE 6  COMPARE           IDENTICAL on all 18 cycles",
        "  STAGE 7  PROVE             Equivalence PROVEN by induction",
        "",
        "  All seven stages passed."],
        size=11.2)

    d.card(s, y + G, "Lab N: the same design in Vivado",
           [[R("Read the design, synthesise for a real part, report utilisation, "
               "write the netlist for gate-level simulation. Vivado is not installed "
               "in the environment these materials were built in, so lab N is the one "
               "whose output is not reproduced here — run it and record what you "
               "get.", s=12.0)]],
           accent=AMBER, fill=CARD_A, h=1005840)

    s = d.slide("PRACTICAL · VENDOR", "The Same Flow in Vivado and ModelSim")
    y = d.image(s, TOP - 45720, "vivado_flow", 4950000)
    d.lead(s, y + G, [[R("Stated plainly on the slide: these commands were not run "
                         "here. Every number in this deck came from the free "
                         "toolchain.", b=True, c=AMBER, s=12.0)]], h=228600)

    s = d.slide("LABS · ASSESSMENT", "How the 103 Exercises Are Weighted")
    y = d.image(s, TOP - 45720, "assessment", 4950000)
    d.lead(s, y + G, [[R("Predict, then measure. Being wrong and knowing why is the "
                         "whole point of a lab.", b=True, c=RED, s=12.0)]],
           h=228600)

    # ------------------------------------------------------ honest limits
    s = d.slide("PRACTICAL · LIMITS", "What This Lab Does Not Show You", accent=AMBER)
    d.bullets(s, TOP, [
        "rtl_lint.py is regular expressions, not a Verilog parser. It reads code the "
        "way a careful reviewer skims it and can be fooled by unusual formatting.",
        "The cell counts come from Yosys' generic library, not a foundry library. "
        "They compare designs against each other; they are not area figures.",
        "fa_switch.v is a functional transistor model. There are no threshold "
        "voltages and no capacitances — SPICE is the tool for that.",
        "Yosys accepts initial blocks because it targets FPGAs. An ASIC flow would "
        "not, and that difference is a genuine trap.",
        "Vivado and ModelSim were not run. Every measured number here came from "
        "iverilog, ghdl and yosys, and is reproducible with make.",
        "Nothing here covers verification methodology beyond a directed testbench "
        "and a handful of assertions — that is Topic 5, a large subject on its own.",
        "The state machines here are small and single-clock. Clock-domain crossing, "
        "reset synchronisers and safe-state recovery are all real, and all later."],
        accent=AMBER, size=12.0, step=457200)

    # -------------------------------------------------------------- summary
    s = d.slide("SUMMARY", "Topic 2 In Fourteen Lines", accent=GREEN)
    d.bullets(s, TOP, [
        "RTL says which registers exist and what transfers into them. Nothing else.",
        "There are two kinds of logic, combinational and sequential, and no third.",
        "<= reads every right-hand side first, then updates together. = does not — "
        "and the blocking version built 1 flip-flop where 3 were meant.",
        "Four levels of abstraction describe the same circuit — proved, not assumed.",
        "Write at the highest level that says what you mean: behavioural gave 5 "
        "cells against 6.",
        "Not all legal Verilog is synthesisable, and a / b cost 371 cells against 0.",
        "A combinational block that does not assign on every path builds a latch; "
        "a default assignment at the top of the block prevents it.",
        "An incomplete sensitivity list makes simulation and silicon disagree "
        "silently.",
        "Equivalent is not identical: three mux styles, 3, 6 and 10 cells.",
        "Almost every block is a datapath and a controller. Here: 145 cells "
        "against 10.",
        "Write state machines in three blocks — register, next state, output.",
        "Moore trails Mealy by exactly one cycle, and one-hot was BIGGER here.",
        "parameter, hierarchy and generate are elaborated away before synthesis.",
        "Verilog and VHDL produced identical transcripts, on both designs."],
        accent=GREEN, size=12.0, step=310896)

    s = d.slide("CLOSE", "What To Do Next", accent=TEAL)
    y = d.image(s, TOP - 45720, "what_you_can_do", 4300000)
    d.card(s, y + G, "Coming next in Module 2",
           [[R("Topic 3 covers the digital logic this all rests on. Topic 4 writes "
               "much more RTL. Topic 5 is verification — how you know it works. "
               "Topic 6 is timing — whether it is fast enough.", s=12.0)]],
           accent=NAVY, h=822960)
