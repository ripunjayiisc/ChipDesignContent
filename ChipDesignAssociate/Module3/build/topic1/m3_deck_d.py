# -*- coding: utf-8 -*-
"""Module 3 Topic 1 deck — Theory 4 (constraints and synthesis) and the
practical component."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ===================================================== section THEORY 4
    d.section_slide(
        "THEORY 4", "Timing Constraints for Synthesis",
        "A constraint file is not a report setting. It is the objective the "
        "optimiser is trying to meet — and it decides what circuit you get.",
        ["What constraints actually do to synthesis",
         "The minimum honest constraint set",
         "What synthesis does to a hazard fix (it deletes it)",
         "Circuit synthesis and timing analysis as one loop"],
        accent=VIOLET)

    s = d.slide("4.1 · THE INPUT", "Constraints Are an Input to Synthesis")
    y = d.image(s, TOP - 45720, "constraints_drive_synthesis", 4937760)
    d.lead(s, y + G, [[R("The same RTL becomes a different circuit depending on what "
                         "you asked for.", b=True, c=NAVY, s=10.5)]], h=228600)

    s = d.slide("4.2 · THE MINIMUM", "The Minimum Honest Constraint Set, In Order")
    y = d.image(s, TOP - 45720, "sdc_minimum", 4846320)
    d.lead(s, y + G, [[R("Module 2 Topic 6 develops each of these in full. Here the "
                         "point is what synthesis does once you have written them.",
                         s=10.5)]], h=274320)

    s = d.slide("4.2 · THE MINIMUM", "A Complete File For the Lab Design")
    y = d.code(s, TOP, [
        "# ==================================================== constraints/pipe.sdc",
        "# ---- clock ------------------------------------------------------------",
        "# 400 MHz. pipe_unbal cannot make this; pipe_bal can. That is the experiment.",
        "create_clock -period 2.500",
        "",
        "# jitter, plus a placeholder for the clock-tree skew that does not exist yet",
        "set_clock_uncertainty 0.080 -setup",
        "set_clock_uncertainty 0.020 -hold",
        "",
        "# ---- boundary ---------------------------------------------------------",
        "# Without these two lines every path touching a port is UNCONSTRAINED,",
        "# and the analyser says so. Run without them once and read the warning.",
        "set_input_delay  0.40 -clock clk",
        "set_output_delay 0.35 -clock clk"],
        size=9.5)

    d.card(s, y + G, "The line to check on every single run",
           [[R("The count of unconstrained endpoints. It must be zero. A design with "
               "WNS +2.0 ns and four hundred unconstrained endpoints is in far worse "
               "shape than one with WNS −0.1 ns and none — the first has not been "
               "analysed at all.", b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=822960)

    # -------------------------------------------- synthesis deletes the fix
    s = d.slide("4.3 · THE COLLISION", "Synthesis Deletes Your Hazard Fix. Every Time.",
                accent=RED)
    y = d.image(s, TOP - 45720, "synth_deletes_fix", 4937760)
    d.lead(s, y + G, [[R("Both RTL versions produced the identical netlist: one "
                         "multiplexer.", b=True, c=RED, s=10.5)]], h=228600)

    s = d.slide("4.3 · THE COLLISION", "Why This Is the Most Important Slide In the "
                                       "Session")
    y = d.lead(s, TOP, [[
        R("Theory 2 taught you to add a redundant term to remove a hazard. Theory 4 "
          "has just shown that a synthesiser deletes it. Those two facts have to be "
          "reconciled, and the reconciliation is the practical skill.", s=12)]],
        h=594360)

    y = d.cols(s, y + G, [
        ("What NOT to conclude",
         [[R("\"Hazard analysis is pointless because the tool undoes it.\"")],
          [R("\"Just write the RTL and trust synthesis.\"")],
          [R("Both are wrong, and the second one ships broken asynchronous "
             "interfaces.")]], RED, CARD_R),
        ("What to conclude",
         [[R("Hazard-freedom is a property of the NETLIST, not of your source.")],
          [R("So it has to be protected structurally, and then verified on the "
             "netlist.")],
          [R("And on the vast majority of nets — everything sampled by a clock — you "
             "do not need it at all.", b=True, c=NAVY)]], GREEN, CARD_G)],
        h=1920240)

    d.card(s, y + G, "How to protect it, when you genuinely need it",
           [[R("A dont_touch or keep attribute on the net or cell  ·  instantiate the "
               "library cell directly  ·  put it in a module the tool is told not to "
               "flatten  ·  and then re-run the glitch detector on the post-synthesis "
               "netlist, not on the RTL.")]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ------------------------------------------------ synthesis and analysis
    s = d.slide("4.4 · THE LOOP", "Circuit Synthesis and Timing Analysis")
    y = d.image(s, TOP - 45720, "synth_to_sta", 4846320)
    d.lead(s, y + G, [[R("You leave the loop once, when all three conditions hold "
                         "together. Two out of three is not closure.", b=True,
                         c=GREEN, s=10.5)]], h=274320)

    s = d.slide("4.5 · THE TRADE", "Everything In This Topic Is a Trade")
    y = d.image(s, TOP - 45720, "area_speed", 4846320)
    d.lead(s, y + G, [[R("There is no free row in that table, and a design that pays "
                         "nothing gets nothing.", b=True, c=NAVY, s=10.5)]], h=274320)

    s = d.slide("THEORY 4 · CHECKPOINT", "Six Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What does a constraint file do to synthesis?",
                  "it is the objective the optimiser tries to meet"],
                 ["2", "What happens with no constraints at all?",
                  "the tool optimises for area; you get small and slow"],
                 ["3", "What happens with an impossible period?",
                  "it burns area and runtime and still fails"],
                 ["4", "What did synthesis do to the consensus term?",
                  "deleted it — both versions gave one identical MUX"],
                 ["5", "So where does hazard-freedom have to be checked?",
                  "on the netlist, never on the RTL"],
                 ["6", "When do you leave the synthesis/analysis loop?",
                  "setup met, hold met, zero unconstrained endpoints"]],
                [548640, 5029200, 5669280], rh=283464, bold_cols=(0,), size=9.5)
    d.lead(s, y + G, [[R("That is the theory. The rest of the session is at the "
                         "keyboard.", b=True, c=GREEN, s=11)]], h=274320)

    # ==================================================== PRACTICAL section
    d.section_slide(
        "PRACTICAL", "Labs A–G",
        "12 hours, 58 graded exercises, and not one number in this deck that you "
        "cannot reproduce yourself.",
        ["Which tool answers which question, and how to install them",
         "Labs A–C: hazards, on paper, in code, and in simulation",
         "Labs D–E: does it matter, and what synthesis does about it",
         "Labs F–G: setup, hold, Fmax — then the same design on a Zynq-7000"],
        accent=GREEN)

    s = d.slide("PRACTICAL · TOOLS", "Which Tool Answers Which Question")
    y = d.image(s, TOP - 45720, "tool_landscape", 4937760)
    d.lead(s, y + G, [[R("A static analyser for setup and hold, a delay-annotated "
                         "simulator for hazards. Neither substitutes for the other.",
                         s=10.5)]], h=228600)

    s = d.slide("PRACTICAL · INSTALL", "One apt Line, and the Whole Lab Runs",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "install_required", 3474720)
    y = d.code(s, y + G, [
        "sudo apt update",
        "sudo apt install yosys iverilog gtkwave python3 python3-matplotlib",
        "yosys -V && iverilog -V && python3 tools/hazard.py --selftest"],
        title="Debian / Ubuntu / WSL2 — copy this", size=10)
    d.lead(s, y + G, [[R("On Windows: wsl --install first, then the same three lines "
                         "inside it.", s=10.5)]], h=228600)

    s = d.slide("PRACTICAL · INSTALL", "The Vendor Tools the Syllabus Names")
    y = d.image(s, TOP - 45720, "install_vendor", 4846320)
    d.lead(s, y + G, [[R("Needed for lab G only. Labs A–F — 53 of the 58 exercises — "
                         "run on the free toolchain alone.", b=True, c=GREEN,
                         s=10.5)]], h=274320)

    s = d.slide("PRACTICAL · THE FLOW", "One Circuit, Two Toolchains")
    y = d.image(s, TOP - 45720, "lab_flow", 4937760)
    d.lead(s, y + G, [[R("You write the hazard analyser here; you wrote the timing "
                         "engine in Module 2. Nothing in the chain is a black box.",
                         s=10.5)]], h=228600)

    s = d.slide("PRACTICAL · MAP", "Seven Parts, Twelve Hours")
    y = d.image(s, TOP - 45720, "lab_map", 5029200)
    d.lead(s, y + G, [[R("Parts A–C build the understanding and the tool. D–E connect "
                         "it to design decisions. F–G are the timing half.", s=10.5)]],
           h=228600)

    # ------------------------------------------------------------ labs A-C
    s = d.slide("LABS A–C", "Hazards: On Paper, In Code, In Simulation")
    y = d.cols(s, TOP, [
        ("A · on paper (2 h)",
         [[R("Draw the K-map for F = A B' + B C.")],
          [R("Find the adjacent 1s that share no loop.")],
          [R("Derive the consensus term by hand.")],
          [R("Deliverable: the term, and a sentence saying why it works.")]],
         TEAL, CARD),
        ("B · in code (2 h)",
         [[R("Write the adjacency test in tools/hazard.py.")],
          [R("Make the self-test pass, including the cross-check against a delay "
             "timeline.")],
          [R("Deliverable: PASSED, and an explanation of what section D of it "
             "proves.")]], NAVY, CARD),
        ("C · in simulation (2 h)",
         [[R("Build the glitch detector.")],
          [R("Predict the glitching transition BEFORE running it.")],
          [R("Then the dynamic case, and its two different fixes.")],
          [R("Deliverable: the six-row results table, explained.")]], VIOLET, CARD)],
        h=3200400)

    d.card(s, y + G, "The exercise that teaches the most is C",
           [[R("Predict which of the 24 transitions will glitch, from the analyser's "
               "output, before you simulate. When the prediction matches, you have "
               "connected a piece of logic reasoning to a physical measurement — "
               "which is the whole of this subtopic.")]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------------ labs D-E
    s = d.slide("LABS D–E", "Does It Matter, and What Synthesis Does About It")
    y = d.code(s, TOP, [
        "$ make capture",
        "  f as DATA, sampled by the clean clock   -> correct",
        "  f as a CLOCK        edges after power-up = 4   <- should be 0",
        "  f as an ASYNC RESET r_flag = 0                 <- should be 1",
        "",
        "$ make synth",
        "  f = a&~b | b&c                   1 cell   {'$_MUX_': 1}",
        "  f = a&~b | b&c | a&c  (fixed)    1 cell   {'$_MUX_': 1}",
        "  The two netlists are IDENTICAL. The consensus term was deleted."],
        title="both results, measured", size=9.5)

    y = d.table(s, y + G,
                ["Exercise", "Task"],
                [["D.1", "Move the glitch to 5 ns before the clock edge. Does the DATA "
                         "column still hold?"],
                 ["D.2", "Replace the async reset with a synchronous one. Re-measure."],
                 ["D.3", "Name three signals in a design you have written that are "
                         "edge-sensitive."],
                 ["E.1", "Add a keep attribute to the consensus term. Does it survive?"],
                 ["E.2", "Re-run the glitch detector on the post-synthesis netlist."],
                 ["E.3", "Explain in writing why the tool chose a MUX."]],
                [1188720, 10058400], rh=283464, bold_cols=(0,))

    # ------------------------------------------------------------ labs F-G
    s = d.slide("LABS F–G", "Setup, Hold, Fmax — Then an Industrial Tool")
    y = d.code(s, TOP, [
        "$ make fmax",
        "  pipe_unbal     Fmax : 364.7 MHz",
        "  pipe_bal       Fmax : 473.2 MHz",
        "",
        "$ make setup                             # target 400 MHz",
        "  pipe_unbal     WNS : -0.322 ns   VIOLATED",
        "  pipe_bal       WNS : +0.307 ns   MET",
        "",
        "$ make hold",
        "  period    4.0 ns   WNS : -0.119 ns   VIOLATED",
        "  period   40.0 ns   WNS : -0.119 ns   VIOLATED",
        "  period  400.0 ns   WNS : -0.119 ns   VIOLATED",
        "  skew 0.25 -> 0.10  WNS : -0.119 -> +0.031 ns   MET"],
        size=9.5)

    d.card(s, y + G, "Lab G: the same design on a Zynq-7000",
           [[R("vivado -mode batch -source vivado/zynq_sta.tcl, targeting "
               "xc7z020clg400-1. The absolute numbers will differ — a Zynq LUT is not "
               "the teaching library. What must match is the shape of the report, "
               "which path is critical, and the direction of every constraint change.")]],
           accent=NAVY, h=1005840)

    s = d.slide("LABS · ASSESSMENT", "How the 58 Exercises Are Weighted")
    y = d.image(s, TOP - 45720, "assessment", 4846320)
    d.lead(s, y + G, [[R("A fix you cannot explain is not a fix.", b=True, c=RED,
                         s=11)]], h=274320)

    # ------------------------------------------------------ honest limits
    s = d.slide("PRACTICAL · LIMITS", "What This Lab Does Not Show You", accent=AMBER)
    d.bullets(s, TOP, [
        "The gate delays are teaching-sized. A real inverter is not 4 ns; the "
        "mechanism is real, the timescale is not.",
        "The delay numbers in the Liberty file are invented, not any vendor's. They "
        "are chosen to be checkable by hand.",
        "sta/sta.py is a teaching analyser: straight-line delays, no slew "
        "propagation, no wire RC, one corner at a time.",
        "The hazard analyser handles two-level covers. Multi-level hazard analysis is "
        "a much harder problem, and hz_dynamic shows you why.",
        "vivado/zynq_sta.tcl has NOT been executed in the environment these materials "
        "were built in — Vivado is not installable there. It is the one file whose "
        "output is not reproduced in the README.",
        "Nothing here covers on-chip variation, crosstalk, or signal integrity. Those "
        "belong to sign-off, in subtopic 3."],
        accent=AMBER, size=11, step=457200)

    # -------------------------------------------------------------- summary
    s = d.slide("SUMMARY", "Topic 1 In Ten Lines", accent=GREEN)
    d.bullets(s, TOP, [
        "A truth table promises settled values. It says nothing about the journey.",
        "A hazard is the circuit's potential to glitch; a glitch is one event in one "
        "run.",
        "Two 1-cells one variable apart, covered by no single term, is a static-1 "
        "hazard.",
        "The fix is the term made of the literals they agree on — redundant, by "
        "design.",
        "That fix cures two-level logic hazards and nothing else. Structure needs "
        "restructuring.",
        "A glitch is harmless only where a clock edge samples it after it settles.",
        "Static timing analysis cannot see any of this: it measures one path, not two.",
        "The clock period is in the setup equation and nowhere in the hold equation.",
        "Fmax is set by one stage; moving work took 364.7 MHz to 473.2 MHz.",
        "And synthesis will delete your hazard fix, so verify on the netlist."],
        accent=GREEN, size=12, step=384048)

    s = d.slide("CLOSE", "What To Do Next", accent=TEAL)
    y = d.image(s, TOP - 45720, "what_you_can_do", 4023360)
    d.card(s, y + G, "Coming next in Module 3",
           [[R("Subtopic 2 takes the optimisation techniques further — pipelining, "
               "retiming, open- and closed-loop timing, block-level versus chip-level. "
               "Subtopic 3 is the EDA flow end to end: post-route analysis, ECO, and "
               "sign-off.", s=10.5)]],
           accent=NAVY, h=822960)
