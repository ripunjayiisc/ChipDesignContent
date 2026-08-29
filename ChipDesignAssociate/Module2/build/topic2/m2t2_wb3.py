# -*- coding: utf-8 -*-
"""Module 2 Topic 2 workbook — Part 5 tools, Part 6 the fourteen tutorials."""
import _boot
from wbkit import *
from m2t2_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 4
    w.h1("Part 5 · Tools and Installation")

    w.h2("5.1  Which tool answers which question")

    w.image("tool_landscape", width=6.9)

    w.callout("Yosys is the interesting one", [
        [N("It is the only free tool in that list that will both synthesise your RTL "
           "and PROVE that the netlist it produced is equivalent to what you wrote. "
           "That combination is what makes the seven-stage flow in Part 2 runnable on "
           "a laptop.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("5.2  Installing")

    w.image("install_required", width=6.9)

    w.code([
        "sudo apt update",
        "sudo apt install yosys iverilog gtkwave python3",
        "sudo apt install ghdl                   # only for the VHDL comparison",
        "",
        "# verify:",
        "yosys -V && iverilog -V && ghdl --version"],
        caption="Debian, Ubuntu or WSL2")

    w.para([N("On Windows, install WSL2 first ("), M("wsl --install"),
            N(" from an elevated PowerShell) and run the same lines inside it. "
              "Without "), M("ghdl"), N(", every target except "), M("make langs"),
            N(" still works.")])

    w.h3("The vendor tools the syllabus names")
    w.image("install_vendor", width=6.9)

    w.callout("An honest note about the vendor tools", [
        [N("Vivado and ModelSim are not installed in the environment these materials "
           "were built in. Every number quoted in this workbook came from iverilog, "
           "ghdl and yosys, and every one is reproducible with "), M("make"), N(".")],
        [N("The commands shown for Vivado and ModelSim come from the vendor "
           "documentation and are labelled as not executed here. Tutorial N asks you "
           "to run them and record what you get — which is itself a useful exercise "
           "in not trusting a number you did not produce.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("5.3  What the lab does with your RTL")

    w.image("lab_flow", width=6.9)

    w.para([N("Four different questions about one piece of code: does it follow the "
              "rules, does it do what the spec says, what will actually be built from "
              "it, and is that thing still the design you wrote? A methodology is "
              "exactly the discipline of asking all four, every time.")])

    w.page_break()

    # ================================================================ Part 5
    w.h1("Part 6 · Fourteen Guided Tutorials")

    w.callout("Before you start", [
        [N("Install the toolchain and open a terminal in "), M("Topic2_Lab/"),
         N(". Type the commands; do not paste them. The point of a tutorial is the "
           "twenty seconds between typing something and understanding why it did what "
           "it did.")],
        [N("Each tutorial ends with a "), B("Checkpoint"),
         N(" — a specific thing you should be able to show or say. If you cannot, "
           "stop and find out why before moving on.")],
    ], color=NAVY, bar="0E2A47")

    w.image("lab_map", width=6.9)

    # ------------------------------------------------------------------ A
    w.h2("Tutorial A · What RTL means  (1 hour)")

    w.para([N("Open "), M("rtl/transfer.v"), N(" and read the always block as a table "
              "of simultaneous transfers. Then, before running anything, fill in this "
              "table on paper for the first three cycles:")])
    w.code([
        "  cycle   din |    x     y     z   |  acc",
        "  ------------+--------------------+------",
        "    0        5 |    ?     ?     ?  |    ?",
        "    1        0 |    ?     ?     ?  |    ?",
        "    2        0 |    ?     ?     ?  |    ?"])
    w.para([N("Now run "), M("make transfer"), N(" and compare.")])

    w.callout("The row people get wrong", [
        [N("On cycle 0, y is 1 — not 6. The assignment "), M("y <= x + 1"),
         N(" used the OLD value of x, which was still 0 when the edge arrived. The 5 "
           "only reaches x on that same edge, so it cannot reach y until the next "
           "one.")],
        [N("If you predicted 6, you were reading the block as a sequence. Read it as "
           "a table.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.callout("Checkpoint A", [
        [N("You can state the two things an RTL description says, and explain why y "
           "is 1 rather than 6 on cycle 0 without looking it up.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ B
    w.h2("Tutorial B · The abstraction ladder  (2 hours)")

    w.h3("Step 1 — read all four")
    w.para([N("Open the four files in "), M("ladder/"),
            N(" side by side. They are the same full adder. Note how much longer each "
              "one gets as you descend, and note that only the top one says what the "
              "circuit is FOR.")])

    w.h3("Step 2 — run them together")
    w.code([
        "$ make ladder",
        "",
        "   a b cin | golden | behav  dataflow  gate  switch",
        "  ---------+--------+--------------------------------",
        "   0 0  0  |  0_0   |  0_0     0_0     0_0   0_0",
        "   ...",
        "   1 1  1  |  1_1   |  1_1     1_1     1_1   1_1",
        "",
        "  patterns applied : 8 of 8   (exhaustive - every possible input)",
        "  mismatches       : 0",
        "  PASS - all four descriptions are the same circuit."])

    w.h3("Step 3 — synthesise each one and predict first")
    w.para([N("Before running it: which level do you expect to produce the fewest "
              "cells? Most people say gate, on the grounds that it is the most "
              "specific. Write your prediction down, then run the synthesis step and "
              "look at section 1.4 of this workbook.")])

    w.h3("Step 4 — the transistor level")
    w.para([N("Open "), M("ladder/fa_switch.v"), N(". Count the transistors in "),
            M("nand2_sw"), N(": two pmos in parallel pulling up, two nmos in series "
              "pulling down. Work out why an AND needs six transistors and a NAND "
              "needs four — and therefore why CMOS libraries are full of NANDs and "
              "NORs rather than ANDs and ORs.")])

    w.callout("Checkpoint B", [
        [N("All four simulate identically; you predicted which level would synthesise "
           "smallest and can explain the answer; and you can say why dataflow and gate "
           "produced the same netlist.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ C
    w.h2("Tutorial C · Proof, not just testing  (2 hours)")

    w.code([
        "$ make prove",
        "  fa_behav vs fa_dataflow            EQUIVALENT   (proved, 94 SAT variables)",
        "  fa_behav vs fa_gate                EQUIVALENT   (proved, 94 SAT variables)",
        "  fa_dataflow vs fa_gate             EQUIVALENT   (proved, 100 SAT variables)",
        "  fa_behav vs fa_broken              NOT EQUIVALENT"])

    w.h3("Step 1 — understand what was proved")
    w.para([N("Read "), M("scripts/equiv.sh"), N(". It builds a miter, asserts the "
              "outputs always match, and asks a SAT solver to find a counter-example. "
              "\"No model found\" is the solver saying: I could not construct one, and "
              "I looked everywhere.")])

    w.h3("Step 2 — break it yourself")
    w.para([N("Open "), M("ladder/fa_broken.v"), N(". It is missing "), M("(a & cin)"),
            N(" from the carry. Work out on paper which single input pattern that "
              "makes wrong, then remove a "), I("different"),
            N(" term and predict the new failing pattern before you run the check "
              "again.")])

    w.h3("Step 3 — the limit")
    w.para([N("A full adder has 8 input patterns, so exhaustive simulation was "
              "complete. Work out how many patterns a 32-bit adder has, and how long "
              "it would take to simulate them all at a million per second. That number "
              "is why equivalence checking exists.")])

    w.callout("Checkpoint C", [
        [N("You have watched the checker prove three equivalences and catch one real "
           "bug, and you can explain why exhaustive simulation stops being an option "
           "well before a design gets interesting.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ D
    w.h2("Tutorial D · The synthesisable subset  (2 hours)")

    w.para([N("Open each file in "), M("subset/"), N(" and write down, before running "
              "anything, whether you expect it to synthesise and roughly how many "
              "cells you expect. Then:")])
    w.code([
        "$ make subset",
        "  construct              synth    cells  latch   what the tool said",
        "  s03_latch              OK       1      YES     inferred a LATCH: $_DLATCH_P_",
        "  s08_whileloop          REFUSED  -      -       \"only allowed in constant "
        "functions\"",
        "  s10_divide             OK       371    no      a full combinational divider",
        "  s11_shift              OK       0      no      no logic at all - just wires"])

    w.h3("Try these")
    w.bullets([
        [N("Change "), M("s10_divide"), N(" to divide by 8 instead of by b. Predict "
           "the cell count first.")],
        [N("Change it to divide by 3 — a constant, but not a power of two. Predict "
           "again, and explain the result.")],
        [N("Write a twelfth construct of your own that you believe will be refused, "
           "and check.")],
        [N("Add "), M("(* keep *)"), N(" to a signal in s01 and see what changes.")],
    ])

    w.callout("Checkpoint D", [
        [N("You predicted at least eight of the eleven rows correctly, and for the "
           "ones you got wrong you can say what you had assumed and why it was "
           "false.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ E
    w.h2("Tutorial E · Simulation against silicon  (1 hour)")

    w.code([
        "$ make mismatch",
        "   change a  (list wakes)     a=1 b=0    RTL y=0    NETLIST y=0",
        "   change b  (list ASLEEP)    a=1 b=1    RTL y=0    NETLIST y=1  <-- DISAGREE",
        "  disagreements: 1 of 6"])

    w.para([N("Only one of six stimulus steps disagreed. Work out why the other five "
              "did not — this matters, because it is exactly why the bug survives "
              "casual testing.")])

    w.h3("Try these")
    w.bullets([
        [N("Change the sensitivity list to "), M("always @(b)"),
         N(" instead. Which steps disagree now?")],
        [N("Change it to "), M("always @*"), N(". Confirm the disagreement count goes "
           "to zero.")],
        [N("Write the same bug into a clocked block. Does it still mismatch? Why "
           "not?")],
    ])

    w.callout("Checkpoint E", [
        [N("You can explain to someone who has not seen it, in three sentences, why "
           "an incomplete sensitivity list is worse than a syntax error.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ F
    w.h2("Tutorial F · The coding rules  (2 hours)")

    w.code([
        "$ make lint",
        "  --- files written the way the methodology asks: ---",
        "    clean - no rule violations       (x4)",
        "  --- and files that break the rules on purpose: ---",
        "    line 7    L001  blocking (=) in a clocked block - use <=",
        "    line 7    L003  = and <= mixed in one always block",
        "    line 13   L004  explicit sensitivity list - use always @*",
        "    line 14   L006  case with no default - infers a latch",
        "",
        "$ make lintcheck",
        "  10 files  ·  linter and Yosys agree on every one  ·  0 disagreements"])

    w.h3("Step 1 — read the tool")
    w.para([N("Open "), M("tools/rtl_lint.py"), N(". It is a few hundred lines of "
              "regular expressions and you can read all of it. Find the function that "
              "counts blocking and non-blocking assignments and satisfy yourself that "
              "the two counts are disjoint.")])

    w.h3("Step 2 — add a rule")
    w.para([N("Add rule L008 of your own choosing. Candidates worth considering: a "
              "clocked block with more than one clock; a module with no ports; a "
              "case statement over a signal wider than four bits with fewer than "
              "sixteen branches and no default. Write the rule, write a file that "
              "breaks it, and write a file that does not.")])

    w.h3("Step 3 — break the linter")
    w.para([N("Find a file that the linter gets wrong — either a false positive or a "
              "missed violation. This is not hard, because it is regular expressions "
              "and not a parser. Then write down why a regular expression cannot fix "
              "the case you found.")])

    w.callout("Checkpoint F", [
        [N("Your new rule fires on the file that breaks it and stays silent on the "
           "file that does not; and you have found at least one case the linter gets "
           "wrong and can explain why.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ G
    # ------------------------------------------------------------------ G
    w.h2("Tutorial G · Coding style  (1 hour)")

    w.para([N("Open "), M("rtl/mux4_styles.v"), N(". Three modules, one function. "
              "Before running anything, write down which you think will produce the "
              "fewest cells, and why.")])
    w.code([
        "$ make mux",
        "  patterns checked : 64        mismatches : 0",
        "  mux4_assign vs mux4_case      EQUIVALENT  (proved, 92 SAT variables)",
        "  mux4_assign                     3 cells",
        "  mux4_if                         6 cells",
        "  mux4_case                      10 cells"])

    w.h3("Try these")
    w.bullets([
        [N("Write a fourth style — a for loop over the data bits, say — and predict "
           "where it lands before you measure.")],
        [N("Rewrite mux4_case using sel as a bit index (y = d[sel];) and see whether "
           "the tool now matches mux4_assign.")],
        [N("Explain in two sentences why an equivalence proof cannot tell you which "
           "of the three to ship.")],
    ])

    w.callout("Checkpoint G", [
        [N("You can state precisely what a formal equivalence proof does and does "
           "not tell you, and you have measured one case where coding style reached "
           "the netlist.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ H
    w.h2("Tutorial H · The two pitfalls  (2 hours)")

    w.para([N("These two account for most of the bugs a new RTL engineer files. "
              "Neither is illegal; neither produces a warning.")])

    w.h3("Step 1 — blocking assignment in a clocked block")
    w.para([N("Open "), M("pitfalls/shift_nb.v"), N(" and "), M("pitfalls/shift_bl.v"),
            N(". They differ by one character per line. Fill in the table below by "
              "hand for the first six cycles of the stimulus, THEN run the lab.")])
    w.code([
        "$ make pitfalls",
        "  non-blocking version : 0 wrong cycles",
        "  blocking version     : 6 wrong cycles",
        "  shift_nb (non-blocking)         3 cells     3 flip-flops",
        "  shift_bl (blocking)             1 cells     1 flip-flops"])

    w.h3("Step 2 — the inferred latch")
    w.para([N("Synthesise "), M("subset/s03_latch.v"), N(" and "),
            M("subset/s14_latch_case.v"), N(", and confirm the "), M("$_DLATCH_"),
            N(" cell in each. Then fix each one — an else in the first, a default "
              "in the second — and confirm it disappears.")])

    w.h3("Try these")
    w.bullets([
        [N("Explain in two sentences why no tool warned about shift_bl.")],
        [N("Write a combinational block with three outputs where only one is "
           "latched, and predict the cell count before synthesising.")],
        [N("Take one of your own files from Tutorial F and check it for both "
           "pitfalls.")],
    ])

    w.callout("Checkpoint H", [
        [N("You can look at a clocked block and say what it will BUILD rather than "
           "what it appears to say, and you can spot an inferred latch in code "
           "before a tool tells you about it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ I
    w.h2("Tutorial I · State machines  (3 hours)")

    w.para([N("The longest tutorial in the topic, and the most useful. Work through "
              "it in order.")])

    w.h3("Step 1 — read the three-block pattern")
    w.para([N("Open "), M("fsm/seq101_moore.v"), N(". Identify the three blocks and, "
              "for each one, say what would break if you moved a line into a "
              "different block.")])

    w.h3("Step 2 — run both styles against one stream")
    w.code([
        "$ make fsm",
        "  matches in the stream : 5      mismatches vs golden  : 0",
        "  PASS - same language, Moore trails Mealy by one cycle,",
        "         and the one-hot encoding is indistinguishable",
        "  seq101_moore  binary           13 cells     2 flip-flops",
        "  seq101_moore  one-hot          30 cells     4 flip-flops",
        "  seq101_mealy  binary           14 cells     2 flip-flops"])

    w.h3("Step 3 — write one yourself")
    w.para([N("Draw the state diagram for a "), B("'110' detector"), N(" with "
              "overlaps counted, on paper, before writing any code. Then write it "
              "in both styles, extend "), M("fsm/tb_seq101.v"), N(" to drive it, and "
              "confirm the one-cycle offset holds for your machine too.")])

    w.h3("Try these")
    w.bullets([
        [N("Re-encode the Moore machine as gray and measure the cells. Explain the "
           "result.")],
        [N("Delete the default assignment from the next-state block, re-run the "
           "linter and then Yosys, and confirm the two agree about the latch.")],
        [N("Add an illegal state to the Verilog machine by writing state <= 2'd7 in "
           "a debug branch. Then try the equivalent in the VHDL version and record "
           "what the analyser says.")],
    ])

    w.callout("Checkpoint I", [
        [N("You can write a state machine in the three-block form without looking it "
           "up, choose Moore or Mealy for a stated reason, and predict what a change "
           "of encoding will cost.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ J
    w.h2("Tutorial J · A controller with a timer  (2 hours)")

    w.para([N("Open "), M("fsm/traffic.v"), N(". Note that the phase length lives in "
              "a down-counter, not in the state encoding — and that the state "
              "machine asks it exactly one question.")])
    w.code([
        "$ make fsm",
        "  cycles checked      : 40",
        "  property violations : 0",
        "  PASS - mutual exclusion and yellow-before-red both hold",
        "  traffic controller             75 cells    10 flip-flops"])

    w.h3("Step 1 — break it on purpose")
    w.para([N("Remove the yellow phases and re-run. Property P2 should fire, and the "
              "message should name the cycle. If it does not, your property is "
              "written wrongly — which is itself the lesson.")])

    w.h3("Step 2 — extend it")
    w.para([N("Add a pedestrian request input that inserts an all-red phase. Then "
              "add a third property: after a pedestrian request, an all-red phase "
              "occurs within N cycles. Deciding what N should be is part of the "
              "exercise.")])

    w.callout("Checkpoint J", [
        [N("You can write a property that fails when the design is wrong, and you "
           "can explain why a phase timer belongs in the datapath rather than in the "
           "state encoding.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ K
    w.h2("Tutorial K · Datapath and controller  (2 hours)")

    w.para([N("Open "), M("rtl/datapath_ctrl.v"), N(". Three modules: a controller, "
              "a datapath, and a parent that wires them together.")])
    w.code([
        "$ make dpctrl",
        "  golden total : 157      hardware sum : 157",
        "  accum_ctrl   (controller)      10 cells     2 flip-flops",
        "  accum_datapath (datapath)     145 cells    24 flip-flops"])

    w.h3("Step 1 — trace the control bundle")
    w.para([N("The run prints every control signal on every cycle. For each of the "
              "ten cycles, say which state the controller is in and why each signal "
              "has the value it has.")])

    w.h3("Step 2 — move a decision, and see what it costs")
    w.para([N("Move the terminal-count test out of the datapath and into the "
              "controller, so the controller holds the counter itself. It will "
              "work. Then answer: what has the controller become dependent on that "
              "it was not before, and what would now have to change if the sample "
              "count went from 8 bits to 16?")])

    w.h3("Try these")
    w.bullets([
        [N("Widen the datapath to 32-bit samples and confirm the controller needs "
           "no edit at all.")],
        [N("Add a valid/ready handshake on the sample input. Which half changes?")],
    ])

    w.callout("Checkpoint K", [
        [N("Given a block description you can say which signals are control, which "
           "are status and which are data, and justify each placement.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ L
    w.h2("Tutorial L · From a module to an IP  (2 hours)")

    w.code([
        "$ make reuse",
        "  delayline mismatches : 0        prescaler ratio errors : 0",
        "  delayline #(W=8, N) synthesised at four different depths:",
        "    N = 1                           8 cells     8 flip-flops",
        "    N = 2                          16 cells    16 flip-flops",
        "    N = 4                          32 cells    32 flip-flops",
        "    N = 8                          64 cells    64 flip-flops"])

    w.h3("Try these")
    w.bullets([
        [N("Predict the cell count for N = 16 before running it.")],
        [N("Add a bypass so that N = 0 removes the registers entirely and dout comes "
           "straight from din. This is the exercise worth arguing about: a generate "
           "loop with N = 0 builds nothing, so getting it right means understanding "
           "that the parameter is resolved before any hardware exists.")],
        [N("Instantiate counter_n three times to divide by 4096, and check the ratio "
           "in simulation rather than assuming it.")],
        [N("Write the three-line specification a colleague would need to use your "
           "delayline without asking you anything. If it needs a fourth line, the "
           "interface is wrong.")],
    ])

    w.callout("Checkpoint L", [
        [N("You can parameterise a design so one file covers a family, and you can "
           "say precisely which language features survive into the netlist and which "
           "are elaborated away.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("Tutorial M · Two languages  (2 hours)")

    w.para([N("Open "), M("rtl/counter.v"), N(" and "), M("vhdl/counter.vhd"),
            N(" side by side and map every line of one onto the other. Then:")])
    w.code([
        "$ make langs",
        "  IDENTICAL over all 18 cycles - including the wrap and the terminal count.",
        "  IDENTICAL over all 17 cycles, detections included.   (the '101' detector)"])

    w.para([N("Then do the same with "), M("fsm/seq101_moore.v"), N(" and "),
            M("vhdl/seq101_moore.vhd"), N(". The state machine is the more "
              "interesting comparison, because it is where the two languages "
              "genuinely differ rather than merely differing in spelling.")])
    w.code([
        "// Verilog:  the states are NUMBERS you chose",
        "localparam [1:0] S_IDLE = 2'd0, S_1 = 2'd1, S_10 = 2'd2, S_101 = 2'd3;",
        "",
        "-- VHDL:  the states are a TYPE, and nothing else can be assigned",
        "type state_t is (S_IDLE, S_1, S_10, S_101);"])

    w.h3("Try these")
    w.bullets([
        [N("Change the width to 8 in both and re-run. Which file needed more "
           "editing?")],
        [N("Introduce the same bug in both — remove the enable check — and confirm "
           "both fail in the same way.")],
        [N("Write down three things VHDL made you say explicitly that Verilog let you "
           "leave implicit, and say which you prefer and why.")],
    ])

    w.callout("Checkpoint M", [
        [N("You can read the VHDL counter without needing it translated, and name "
           "three concrete differences that are about notation rather than about "
           "hardware.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------------ N
    w.h2("Tutorial N · The flow, end to end, and the vendor tools  (2 hours)")

    w.code([
        "$ make flow",
        "  STAGE 1  SPECIFICATION      4 sentences, written before the RTL",
        "  STAGE 2  LINT               0 issues",
        "  STAGE 3  RTL SIMULATION     18 cycles; wraps at 15, tc correct",
        "  STAGE 4  SYNTHESIS          12 cells",
        "  STAGE 5  GATE SIMULATION    the netlist, same stimulus",
        "  STAGE 6  COMPARE            IDENTICAL on all 18 cycles",
        "  STAGE 7  PROVE              Equivalence PROVEN by induction",
        "  All seven stages passed."])

    w.h3("Step 1 — make each stage fail, one at a time")
    w.para([N("This is the exercise. Introduce a lint violation and watch stage 2 "
              "stop the flow. Break the counter's wrap and watch stage 3 catch it. "
              "Then find a change that passes stages 2 and 3 but fails stage 7 — that "
              "one takes thought, and finding it is the point.")])

    w.h3("Step 2 — add a stage")
    w.para([N("Add a stage 8 of your own. A reasonable candidate: check that the "
              "netlist contains no latches, and fail if it does.")])

    w.callout("Checkpoint N1", [
        [N("You have seen every stage fail at least once, and you have added a stage "
           "that catches something the original seven did not.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h3("Step 3 — the same design in the vendor tools")

    w.image("vivado_flow", width=6.9)

    w.para([N("Run the same counter through Vivado, and the same testbench through "
              "ModelSim. Compare three things with what you already have: the "
              "utilisation report against the Yosys cell count, the ModelSim "
              "transcript against the iverilog one, and the overall runtime.")])

    w.callout("Checkpoint N2", [
        [N("You have run one design through both toolchains and can account for the "
           "differences — and you have noticed which parts of the vendor flow "
           "correspond exactly to steps you already ran for free.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
