# -*- coding: utf-8 -*-
"""Module 3 Topic 1 workbook — Part 5 tools, Part 6 the seven tutorials."""
import _boot
from wbkit import *
from m3_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 5
    w.h1("Part 5 · Tools and Installation")

    w.h2("5.1  Which tool answers which question")

    w.image("tool_landscape", width=6.5)

    w.callout("The pairing that matters in this topic", [
        [N("A static analyser for setup and hold, and a delay-annotated simulator for "
           "hazards. Neither substitutes for the other, and a flow with only one of "
           "them has a blind spot you will not notice until silicon.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("5.2  Installing the free toolchain")

    w.image("install_required", width=6.4)

    w.code([
        "sudo apt update",
        "sudo apt install yosys iverilog gtkwave python3 python3-matplotlib",
        "",
        "# verify - the third command is the real test:",
        "yosys -V && iverilog -V && python3 tools/hazard.py --selftest"],
        caption="Debian, Ubuntu or WSL2. This is all 53 of the 58 exercises need.")

    w.para([N("On Windows, install WSL2 first ("), M("wsl --install"),
            N(" from an elevated PowerShell), then run the same lines inside the "
              "Ubuntu shell it gives you. On macOS, "),
            M("brew install yosys icarus-verilog"),
            N(" covers the first two.")])

    w.h2("5.3  The vendor tools the syllabus names")

    w.image("install_vendor", width=6.4)

    w.para([N("The syllabus lists a ZynQ7000 SoC evaluation board, Vivado, and a JTAG "
              "cable. Only Vivado is needed for the lab work, and only for tutorial G. "
              "The board and the cable matter when you want to "), I("run"),
            N(" a design; timing analysis is a synthesise-and-report activity, and "
              "Vivado will happily target a Zynq-7000 it has never been connected to.")])

    w.callout("An honest note about tutorial G", [
        [M("vivado/zynq_sta.tcl"), N(" has NOT been executed in the environment these "
           "materials were built in — Vivado is not installable there. It is written "
           "against the documented command set and is the one file in this lab whose "
           "output is not reproduced in the README. Run it and record what you get; "
           "that is part of the exercise.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("5.4  The lab flow")

    w.image("lab_flow", width=6.4)

    w.code([
        "make analyse    # find hazards in a two-level cover, and prove the fix",
        "make glitch     # gate-level simulation: watch the glitch, and watch it go",
        "make capture    # what a glitch does to a flop as data / clock / reset",
        "make synth      # what synthesis does to a hazard fix (it deletes it)",
        "make fmax       # Fmax of an unbalanced pipeline, and of a balanced one",
        "make setup      # a real setup violation at 400 MHz, and its fix",
        "make hold       # a hold violation, and why the clock period cannot help",
        "make            # all of the above"])

    w.page_break()

    # ================================================================ Part 6
    w.h1("Part 6 · Seven Guided Tutorials")

    w.callout("Before you start", [
        [N("Install the toolchain from Part 5 and open a terminal in "),
         M("Topic1_Lab/"), N(". Type the commands; do not paste them. The point of a "
                             "tutorial is the twenty seconds between typing something "
                             "and understanding why it did what it did.")],
        [N("Each tutorial ends with a "), B("Checkpoint"),
         N(" — a specific thing you should be able to see or say. If you cannot, stop "
           "and find out why before moving on.")],
    ], color=NAVY, bar="0E2A47")

    w.image("lab_map", width=6.5)

    # ------------------------------------------------------------------ A
    w.h2("Tutorial A · Hazards on paper  (2 hours)")

    w.para([N("Before any tool touches this, do it by hand. The rule is short enough "
              "to hold in your head, and holding it in your head is the point.")])

    w.h3("Step 1 — draw the map")
    w.para([N("Draw the K-map for "), M("F = A B' + B C"),
            N(" with A down the side and B C across the top. Fill in the four 1-cells. "
              "Draw the loop for each product term.")])

    w.h3("Step 2 — find the adjacency")
    w.para([N("Look for two 1-cells that are neighbours but sit in different loops. "
              "There is exactly one such pair. Write down which two cells, and which "
              "variable differs between them.")])

    w.h3("Step 3 — derive the fix")
    w.para([N("Write down every variable the two cells agree on, at the value they "
              "agree on. Drop the one that changed. That product is the term to add.")])

    w.h3("Step 4 — prove it did not change anything")
    w.para([N("Write out both truth tables, eight rows each, and check them row by "
              "row. If they differ anywhere, you have not written the consensus term "
              "— you have written a bug.")])

    w.callout("Checkpoint A", [
        [N("You can state the adjacency rule without looking, derive "), M("A C"),
         N(" from the two cells, and show that F is unchanged on all eight rows.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ B
    w.h2("Tutorial B · Build the analyser  (2 hours)")

    w.h3("Step 1 — see what it does")
    w.code([
        "$ python3 tools/hazard.py \"A B' + B C\"",
        "",
        "  1 static-1 logic hazard(s) found:",
        "    B changes 1 -> 0   with  A=1, C=1",
        "      ADD the redundant term:  A C",
        "",
        "  checking the proposed cover:",
        "    remaining static-1 hazards : 0",
        "    truth table unchanged      : yes"])

    w.h3("Step 2 — read the core of it")
    w.para([N("Open "), M("tools/hazard.py"), N(" and find "), M("static1_hazards()"),
            N(". It is the adjacency rule, transcribed:")])
    w.code([
        "for vec in every input vector:",
        "    if F(vec) != 1: continue",
        "    for each variable i:",
        "        other = vec with bit i flipped",
        "        if F(other) != 1: continue",
        "        spanning = [t for t in terms if t covers vec and t covers other]",
        "        if not spanning:",
        "            report a hazard, and prescribe the shared literals as the fix"])

    w.h3("Step 3 — run the self-test and read section D")
    w.code([
        "$ python3 tools/hazard.py --selftest",
        "",
        "D. the combinatorial rule agrees with a delay simulation",
        "  static-1 transitions cross-checked           PASS",
        "  disagreements between rule and simulation    PASS  (got 0, want 0)",
        "",
        "SELF-TEST PASSED"])

    w.para([N("Section D is the part worth studying. "), M("can_glitch()"),
            N(" builds a timeline with randomised per-term switching times and looks "
              "for an instant when every term is off. It never refers to the covering "
              "rule, so the two are genuinely independent — and over several thousand "
              "transitions on random functions they never disagreed.")])

    w.h3("Step 4 — try to break it")
    w.para([N("Feed it functions of your own. A single product term. A function whose "
              "minimal cover is already hazard-free. "), M("A B + A B'"),
            N(" — which is just F = A written badly, and which does have a hazard. "
              "Predict each answer before you run it.")])

    w.callout("Checkpoint B", [
        [N("The self-test prints PASSED, and you can explain in your own words what "
           "section D proves and why a single fixed delay profile would not have "
           "proved it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ C
    w.h2("Tutorial C · Gate-level glitches  (2 hours)")

    w.h3("Step 1 — predict, then measure")
    w.para([N("From the analyser's output you know the hazard is on B falling with "
              "A = 1 and C = 1 — that is the input pattern 111 going to 101. "
              "Write that prediction down. Then:")])
    w.code([
        "$ make glitch",
        "",
        "  === glitch detector: hz_static1 ===",
        "  ABC 111 -> 101  (B changed)   f: 1 -> 1   changes=2 expected=0"
        "    STATIC GLITCH",
        "",
        "  transitions examined : 24",
        "  transitions glitching: 1",
        "  RESULT: 1 GLITCH(ES), worst had 2 surplus change(s)",
        "  TRUTH(ABC=000..111) = 10111000"])

    w.para([N("One glitch, on exactly the transition the analyser named, out of 24 "
              "examined. A logic rule predicted a physical measurement.")])

    w.h3("Step 2 — apply the fix and re-measure")
    w.para([N("hz_static1_fix reports CLEAN, with the same truth signature "),
            M("10111000"), N(". Same function, no glitch.")])

    w.h3("Step 3 — the multi-level case")
    w.para([N("Now hz_dynamic, which feeds the hazardous expression into an XOR where "
              "B reconverges by a faster route:")])
    w.table(["design", "detector result"],
            [["hz_dynamic", "5 glitches — 4 static, 1 dynamic"],
             ["hz_dynamic_fix", "4 glitches — the dynamic one is gone"],
             ["hz_flat_fix", "CLEAN"]],
            widths=[2.2, 4.2], size=9.5, bold_cols=(0,), align_center=False)

    w.h3("Step 4 — work out why the fix only got half way")
    w.para([N("This is the exercise, not a demonstration. Substitute A=0 and C=1 into "),
            M("s = A B' + B C + A C"), N(" and see what s becomes. Then work out what "),
            M("f = s XOR b"), N(" is computing. Write your answer down before reading "
                                "section 2.7 of this workbook again.")])

    w.callout("Checkpoint C", [
        [N("You predicted the glitching transition before simulating and were right; "
           "and you can explain why the four surviving glitches in hz_dynamic_fix are "
           "not a cover problem.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ D
    w.h2("Tutorial D · Does it matter?  (1 hour)")

    w.code([
        "$ make capture",
        "",
        "  1. f as DATA, sampled by the clean clock",
        "       final d_sampled = 1        <- correct, glitch never seen",
        "  2. f as a CLOCK",
        "       edges at power-up      = 1   (legitimate: f settled x -> 1)",
        "       edges after that       = 4   <- should be 0",
        "  3. f as an ASYNCHRONOUS RESET",
        "       r_flag = 0                  <- should be 1; a glitch reset it"])

    w.para([N("Four glitches produced four spurious clock edges and cleared a flag "
              "that nothing should have cleared. The glitch was placed 80 ns before "
              "any clock edge, which is the friendliest possible case for the usual "
              "reassurance.")])

    w.h3("Try these")
    w.bullets([
        [N("Move the B transitions to 5 ns before the clock edge instead of 20 ns "
           "after it. Does the DATA column still hold? At what point does it stop "
           "holding?")],
        [N("Replace the asynchronous reset with a synchronous one and re-measure.")],
        [N("List three signals in a design you have written yourself that are "
           "edge-sensitive or level-sensitive rather than clock-sampled.")],
    ])

    w.callout("Checkpoint D", [
        [N("You can state the rule as \"a glitch is harmless only where a clock edge "
           "samples it after it has settled\" — and name at least three places in a "
           "real design where that condition does not hold.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ E
    w.h2("Tutorial E · What synthesis does about it  (1 hour)")

    w.code([
        "$ make synth",
        "",
        "  RTL written                      cells  gates",
        "  f = a&~b | b&c                       1  {'$_MUX_': 1}",
        "  f = a&~b | b&c | a&c   (fixed)       1  {'$_MUX_': 1}",
        "",
        "  The two netlists are IDENTICAL. The consensus term was deleted."])

    w.h3("Try these")
    w.bullets([
        [N("Add a "), M("(* keep *)"), N(" attribute to the consensus term's wire and "
           "re-run. Does it survive? Does the netlist still contain a MUX?")],
        [N("Write the glitch detector against the post-synthesis netlist rather than "
           "the RTL. What does it report?")],
        [N("Explain, in writing, why the tool chose a multiplexer. Check your answer "
           "by writing out the truth table of "), M("B ? C : A"), N(".")],
    ])

    w.callout("Checkpoint E", [
        [N("You can say where hazard-freedom has to be verified, and why verifying it "
           "on the RTL proves nothing at all.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ F
    w.h2("Tutorial F · Setup, hold and Fmax  (2 hours)")

    w.code([
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
        "",
        "  skew 0.25 ns     WNS : -0.119 ns   VIOLATED",
        "  skew 0.10 ns     WNS : +0.031 ns   MET"])

    w.h3("Try these")
    w.bullets([
        [N("Before running "), M("make setup"),
         N(", compute −0.322 ns as a percentage of the 2.5 ns period and predict which "
           "class of fix will be needed. Then check the table in section 3.5.")],
        [N("Run the hold analysis at 4000 ns. Predict the answer first.")],
        [N("Find the skew value at which hold_demo is exactly on the boundary. "
           "What does that tell you about the margin you have?")],
        [N("Remove "), M("set_input_delay"), N(" from pipe.sdc and re-run. The WNS "
           "improves. Explain to a manager, in two sentences, why that is bad news.")],
    ])

    w.callout("Checkpoint F", [
        [N("You have reproduced all six numbers, and you can explain why the hold "
           "slack did not move across a hundred-fold change in clock frequency.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ G
    w.h2("Tutorial G · The same design on a Zynq-7000  (2 hours)")

    w.image("vivado_zynq", width=6.5)

    w.code([
        "$ vivado -mode batch -source vivado/zynq_sta.tcl",
        "",
        "# then compare, in vivado/rpt/ :",
        "#   post_synth_summary.rpt   against  ./scripts/sta.sh pipe_bal",
        "#   post_route_summary.rpt   against  post_synth_summary.rpt"])

    w.table(["What to compare", "Expect", "Why"],
            [["absolute WNS", "different", "a Zynq LUT is not lib/cda_edu.lib"],
             ["which path is critical", "the same", "the design's structure is the same"],
             ["post-synth vs post-route setup", "post-route is worse",
              "synthesis estimated the wiring; routing measured it"],
             ["post-route hold", "a number that did not exist before",
              "only now is there a real clock tree"]],
            widths=[2.2, 1.8, 2.8], size=9.2, bold_cols=(0,), align_center=False)

    w.h3("The deliverable")
    w.para([N("One page: what matched between your engine and Vivado, what did not, "
              "and why. An answer that says \"different tools give different answers\" "
              "is not an answer. An answer that says \"the numbers differ because an "
              "Artix-class LUT delay is around 0.1 ns where our XOR2 is 0.088 ns, and "
              "because routing adds delay our model has none of\" is.")])

    w.callout("Checkpoint G", [
        [N("You have run the same design through two toolchains and can account for "
           "the difference in terms of the delay model, rather than dismissing it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
