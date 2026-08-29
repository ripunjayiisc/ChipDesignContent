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
        "THEORY 3", "Introduction to Hardware Description Languages",
        "The syllabus says \"HDLs such as Verilog or VHDL\". The word doing "
        "the work is OR.",
        ["Why an HDL is not a programming language",
         "Everything happens at once",
         "The parts of a module, and the word reg that confuses everyone",
         "Verilog and VHDL, side by side and both actually run"],
        accent=NAVY)

    s = d.slide("3.1 · NOT A PROGRAM", "An HDL Is Not a Programming Language")
    y = d.image(s, TOP - 45720, "what_is_hdl", 4846320)
    d.lead(s, y + G, [[R("You are not writing instructions for a machine to follow. "
                         "You are writing a description of a machine.", b=True,
                         c=NAVY, s=11)]], h=274320)

    s = d.slide("3.2 · CONCURRENCY", "Everything Happens At Once")
    y = d.image(s, TOP - 45720, "concurrency", 4846320)
    d.lead(s, y + G, [[R("Write those three assign lines in any order you like — the "
                         "circuit is identical.", s=10.5)]], h=274320)

    s = d.slide("3.3 · ANATOMY", "The Parts of a Verilog Module")
    y = d.image(s, TOP - 45720, "module_anatomy", 4937760)
    d.lead(s, y + G, [[R("reg does not mean register. What creates a flip-flop is "
                         "assigning inside always @(posedge clk) — nothing else.",
                         b=True, c=AMBER, s=10.5)]], h=228600)

    s = d.slide("3.4 · SIMULATION", "How a Simulator Runs an HDL")
    y = d.image(s, TOP - 45720, "event_simulation", 4937760)
    d.lead(s, y + G, [[R("The order blocks are evaluated in is genuinely unspecified. "
                         "That is why non-blocking assignment exists.", s=10.5)]],
           h=228600)

    s = d.slide("3.5 · TWO LANGUAGES", "Verilog and VHDL, Side By Side")
    y = d.image(s, TOP - 45720, "verilog_vhdl", 5029200)
    d.lead(s, y + G, [[R("None of those differences are about hardware. Both describe "
                         "registers, logic and hierarchy; both synthesise to the same "
                         "gates.", s=10.5)]], h=228600)

    s = d.slide("3.5 · TWO LANGUAGES", "The Same Counter, In Both, Actually Run")
    y = d.image(s, TOP - 45720, "two_languages_result", 4297680)
    d.card(s, y + G, "Not \"they look similar\"",
           [[R("The two transcripts were compared line by line by diff, and there was "
               "nothing to report — 18 cycles, two languages, two different "
               "simulators, one design.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=685800)

    s = d.slide("3.6 · WHICH ONE", "Which HDL Should You Learn?")
    y = d.image(s, TOP - 45720, "hdl_choose", 4937760)
    d.lead(s, y + G, [[R("Learn the concepts. The notation follows in an afternoon.",
                         b=True, c=GREEN, s=11)]], h=228600)

    s = d.slide("THEORY 3 · CHECKPOINT", "Five Questions", accent=GREEN)
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
                  "either — the concepts are identical, and the lab proves it"]],
                [548640, 5029200, 5669280], rh=283464, bold_cols=(0,), size=9.5)

    # ==================================================== PRACTICAL section
    d.section_slide(
        "PRACTICAL", "Labs A–I",
        "14 hours, 60 graded exercises, and not one number in this deck that "
        "you cannot reproduce yourself.",
        ["Which tool answers which question, and how to install them",
         "Labs A–C: what RTL means, the ladder, and proof",
         "Labs D–F: the subset, the mismatch, and the coding rules",
         "Labs G–I: two languages, the whole flow, and the vendor tools"],
        accent=GREEN)

    s = d.slide("PRACTICAL · TOOLS", "The Tools, and What Each One Is For")
    y = d.image(s, TOP - 45720, "tool_landscape", 5029200)
    d.lead(s, y + G, [[R("Yosys is the interesting one: the only free tool here that "
                         "both synthesises your RTL and PROVES the netlist matches it.",
                         s=10.5)]], h=228600)

    s = d.slide("PRACTICAL · INSTALL", "Two apt Lines, and the Whole Lab Runs",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "install_required", 3474720)
    y = d.code(s, y + G, [
        "sudo apt install yosys iverilog gtkwave python3",
        "sudo apt install ghdl                    # only for the VHDL comparison",
        "yosys -V && iverilog -V && ghdl --version"],
        title="Debian / Ubuntu / WSL2", size=10)
    d.lead(s, y + G, [[R("Without ghdl everything except  make langs  still runs.",
                         s=10.5)]], h=228600)

    s = d.slide("PRACTICAL · INSTALL", "The Vendor Tools the Syllabus Names")
    y = d.image(s, TOP - 45720, "install_vendor", 4846320)
    d.lead(s, y + G, [[R("They add a real device library and a flow you will meet at "
                         "work. They add nothing to the concepts.", s=10.5)]],
           h=274320)

    s = d.slide("PRACTICAL · THE FLOW", "Four Questions About One Piece of Code")
    y = d.image(s, TOP - 45720, "lab_flow", 4846320)
    d.lead(s, y + G, [[R("Does it follow the rules? Does it do what the spec says? "
                         "What will be built? Is that still your design?", s=10.5)]],
           h=274320)

    s = d.slide("PRACTICAL · MAP", "Nine Parts, Fourteen Hours")
    y = d.image(s, TOP - 45720, "lab_map", 5120640)
    d.lead(s, y + G, [[R("Parts A–C build the mental model, D–F the methodology, "
                         "G–I the connection to other languages and real tools.",
                         s=10.5)]], h=182880)

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
        size=9.2)

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
                [1188720, 10058400], rh=283464, bold_cols=(0,))

    # ------------------------------------------------------------ labs G-I
    s = d.slide("LABS G–I", "Two Languages, the Whole Flow, and the Vendor Tools")
    y = d.code(s, TOP, [
        "$ make langs",
        "  === Verilog: iverilog ===        === VHDL: ghdl ===",
        "  IDENTICAL over all 18 cycles - including the wrap and the terminal count.",
        "",
        "$ make flow",
        "  STAGE 2  LINT              0 issues",
        "  STAGE 4  SYNTHESIS         12 cells",
        "  STAGE 6  COMPARE           IDENTICAL on all 18 cycles",
        "  STAGE 7  PROVE             Equivalence PROVEN by induction",
        "",
        "  All seven stages passed."],
        size=9.5)

    d.card(s, y + G, "Lab I: the same design in Vivado",
           [[R("Read the design, synthesise for a real part, report utilisation, "
               "write the netlist for gate-level simulation. Vivado is not installed "
               "in the environment these materials were built in, so lab I is the one "
               "whose output is not reproduced here — run it and record what you "
               "get.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=1005840)

    s = d.slide("PRACTICAL · VENDOR", "The Same Flow in Vivado and ModelSim")
    y = d.image(s, TOP - 45720, "vivado_flow", 4937760)
    d.lead(s, y + G, [[R("Stated plainly on the slide: these commands were not run "
                         "here. Every number in this deck came from the free "
                         "toolchain.", b=True, c=AMBER, s=10.5)]], h=228600)

    s = d.slide("LABS · ASSESSMENT", "How the 60 Exercises Are Weighted")
    y = d.image(s, TOP - 45720, "assessment", 4937760)
    d.lead(s, y + G, [[R("Predict, then measure. Being wrong and knowing why is the "
                         "whole point of a lab.", b=True, c=RED, s=10.5)]],
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
        "Nothing here covers verification methodology beyond a directed testbench — "
        "that is Topic 5, and it is a large subject on its own."],
        accent=AMBER, size=11, step=457200)

    # -------------------------------------------------------------- summary
    s = d.slide("SUMMARY", "Topic 2 In Ten Lines", accent=GREEN)
    d.bullets(s, TOP, [
        "RTL says which registers exist and what transfers into them. Nothing else.",
        "<= reads every right-hand side first, then updates together. = does not.",
        "Four levels of abstraction describe the same circuit — proved, not assumed.",
        "The behavioural description produced the smallest netlist: 5 cells against 6.",
        "Write at the highest level that says what you mean.",
        "Not all legal Verilog is synthesisable, and a / b cost 371 cells against 0.",
        "A combinational block that does not assign on every path builds a latch.",
        "An incomplete sensitivity list makes simulation and silicon disagree "
        "silently.",
        "Seven coding rules, checked by a tool, and cross-checked against Yosys.",
        "Verilog and VHDL produced identical transcripts over 18 cycles."],
        accent=GREEN, size=12, step=384048)

    s = d.slide("CLOSE", "What To Do Next", accent=TEAL)
    y = d.image(s, TOP - 45720, "what_you_can_do", 4114800)
    d.card(s, y + G, "Coming next in Module 2",
           [[R("Topic 3 covers the digital logic this all rests on. Topic 4 writes "
               "much more RTL. Topic 5 is verification — how you know it works. "
               "Topic 6 is timing — whether it is fast enough.", s=10.5)]],
           accent=NAVY, h=822960)
