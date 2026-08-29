# -*- coding: utf-8 -*-
"""Module 2 Topic 2 workbook — 60 exercises, worked solutions, reference card."""
import _boot
from wbkit import *
from m2t2_wb1 import B, N, I, M

EX = [
    # ------------------------------------------------- A · what RTL means
    ("A1", "H", "State the two things, and only the two things, that an RTL "
     "description says.",
     "Which registers exist, and what transfers into each of them on each clock "
     "edge. Everything else - gate count, gate choice, wiring, speed - is left to "
     "synthesis."),
    ("A2", "H", "In rtl/transfer.v, why is y equal to 1 rather than 6 on cycle 0?",
     "y <= x + 1 reads the OLD value of x, which was still 0 when the edge arrived. "
     "The 5 reaches x on that same edge, so it cannot reach y until the next one. "
     "Reading the block as a sequence rather than a table is what produces the wrong "
     "answer."),
    ("A3", "H", "How many clock edges does the 5 take to reach acc, and why?",
     "Four. One per register in the chain x, y, z, acc - each transfer happens on its "
     "own edge, and nothing moves in between."),
    ("A4", "C", "Run make transfer. Add a fifth register after acc and predict the "
     "new latency before re-running.",
     "Five edges. Each register added to a chain adds exactly one cycle of latency, "
     "which is the trade pipelining makes."),
    ("A5", "W", "Explain, to someone who writes software, why the four assignments in "
     "that always block are not four steps.",
     "They are four wires into four registers, all loaded by the same clock edge. The "
     "semicolons separate declarations of what is connected to what, not instructions "
     "to be performed in turn."),
    ("A6", "W", "Why is RTL the level at which industrial design is done, rather than "
     "behavioural or gate level?",
     "Above RTL you cannot say when things happen, so the tool has to invent a "
     "schedule; below it you cannot say anything else, so a human cannot write or "
     "read a real design. RTL is where a human can express intent AND a tool can "
     "build it without guessing."),

    # ------------------------------------------------------- B · the ladder
    ("B1", "H", "Name the four levels of abstraction, highest first, and say in one "
     "phrase what you specify at each.",
     "Behavioural - the function. Dataflow - the Boolean form. Gate - every gate and "
     "wire. Switch - individual transistors."),
    ("B2", "C", "Run make ladder. How many patterns were applied, and why is that "
     "number significant?",
     "Eight, which is exhaustive: a full adder has three inputs, so 2^3 = 8 covers "
     "every possible case. There is nothing left untested."),
    ("B3", "H", "Before running the synthesis step, predict which level will produce "
     "the fewest cells. Then check.",
     "Most people predict gate, reasoning that it is most specific. The answer is "
     "behavioural, with 5 cells against 6, because it left the tool free to choose "
     "the Boolean form and the tool found a better one."),
    ("B4", "W", "Why did dataflow and gate produce the identical netlist?",
     "Writing the Boolean expression already commits to a structure. Naming the gates "
     "afterwards adds no information the tool did not already have, so it produces the "
     "same result from both."),
    ("B5", "H", "Count the transistors in nand2_sw. Why does a CMOS AND cost more "
     "than a CMOS NAND?",
     "Four - two pmos in parallel, two nmos in series. An AND is a NAND followed by "
     "an inverter, so it costs six. This is why standard-cell libraries are full of "
     "NANDs and NORs."),
    ("B6", "C", "Why did the switch-level description fail to synthesise?",
     "Transistor primitives have no gate-level meaning a synthesiser can map. They "
     "are what a library cell is BUILT from, not something you hand to a tool that "
     "builds from library cells."),
    ("B7", "W", "State the rule about choosing an abstraction level, and the reason "
     "for it.",
     "Write at the highest level that expresses your intent, because every level you "
     "descend takes a decision away from the tool and gives it to you - whether or not "
     "you wanted it."),
    ("B8", "W", "Name two things the tool is better at than you, and two things you "
     "are better at than the tool.",
     "Tool: choosing a gate mix, balancing a logic tree, meeting a constraint by "
     "restructuring, doing it consistently. You: how many cycles the job takes, where "
     "registers go, what is shared, what the interface looks like."),
    ("B9", "C", "Write a 4-bit adder at behavioural and gate level, synthesise both, "
     "and compare cell counts.",
     "The behavioural version should be no larger and usually smaller. If yours is "
     "larger, look at whether your gate-level version accidentally shares logic the "
     "tool could not."),

    # -------------------------------------------------------- C · proof
    ("C1", "H", "What is a miter, and what question does the SAT solver answer?",
     "Both designs fed the same inputs, their outputs compared, and an assertion that "
     "the comparison always holds. The solver is asked to find an input pattern that "
     "breaks the assertion; failing to find one proves none exists."),
    ("C2", "C", "Run make prove. Why does the run end with a NOT EQUIVALENT line?",
     "Because fa_broken.v is deliberately wrong. A checker that only ever reports "
     "success is not evidence of anything - you have to see it catch a real bug."),
    ("C3", "H", "fa_broken is missing (a & cin) from the carry. Which single input "
     "pattern does that make wrong?",
     "a=1, b=0, cin=1. There the correct carry is 1 and the broken expression gives "
     "0. Every other pattern is unaffected - one in eight."),
    ("C4", "C", "Remove a different term instead and predict the failing pattern "
     "before running the checker.",
     "Removing (a & b) fails at a=1, b=1, cin=0. Removing (b & cin) fails at a=0, "
     "b=1, cin=1. In each case it is the pattern where that term is the only one "
     "asserting the carry."),
    ("C5", "H", "A 32-bit adder has 65 inputs. How many patterns is exhaustive "
     "simulation, and how long at a million per second?",
     "2^65, about 3.7e19. At a million per second that is roughly 1.2 million years. "
     "This is the number that makes equivalence checking necessary rather than "
     "merely nice."),
    ("C6", "W", "Simulation and equivalence checking answer different questions. "
     "State each precisely.",
     "Simulation: does this design produce the right output on the patterns I applied? "
     "Equivalence checking: do these two designs produce the same output on every "
     "possible input? Neither replaces the other - you still need simulation to know "
     "the SPEC is met."),
    ("C7", "C", "The counter's equivalence proof used induction rather than a single "
     "SAT call. Why?",
     "The counter has state. Combinational equivalence compares outputs for one input "
     "vector; a sequential design needs an argument that holds across all reachable "
     "states, which is what induction over the state elements provides."),

    # ------------------------------------------------------- D · the subset
    ("D1", "C", "Run make subset. Which two constructs were refused, and in the "
     "tool's own words?",
     "The data-dependent while loop (\"While loops are only allowed in constant "
     "functions!\") and real (\"syntax error, unexpected TOK_REAL\")."),
    ("D2", "W", "Why can a synthesiser not build a while loop whose trip count "
     "depends on data?",
     "It must produce a fixed amount of hardware. It cannot build 'however many "
     "iterations this value happens to need'. Doing that in hardware means a state "
     "machine taking several cycles - a design decision you must make explicitly."),
    ("D3", "H", "s07_forloop has a for loop and synthesised fine. What is the "
     "difference?",
     "Its bounds are constants, so the tool unrolls it at compile time into seven "
     "parallel XOR gates. It is not a loop in hardware at all."),
    ("D4", "C", "a / b cost 371 cells and a / 4 cost 0. Explain both numbers.",
     "Dividing by a signal requires a full combinational divider. Dividing by a "
     "constant power of two is a right shift, which is a renaming of wires and costs "
     "no logic whatsoever."),
    ("D5", "C", "Change s10 to divide by 3. Predict the cell count first.",
     "Larger than 0 and much smaller than 371: division by a constant becomes a "
     "multiply-and-shift, which is real logic but far cheaper than a general divider."),
    ("D6", "H", "What happened to the #5 delay in s05, and why is that dangerous?",
     "It was ignored; the module synthesised to one NOT gate. Dangerous because the "
     "simulation you signed off waited 5 ns and the silicon will not, so the two "
     "behave differently."),
    ("D7", "W", "s06_initial synthesised successfully. Why is that a trap rather than "
     "good news?",
     "Yosys targets FPGAs, where the bitstream really does initialise flip-flops. An "
     "ASIC flow ignores initial blocks and the flops power up unknown. Code that works "
     "on an FPGA can therefore fail on an ASIC, with no warning at either end."),
    ("D8", "C", "Write a construct you believe will be refused and check it.",
     "Candidates: file I/O ($fopen), hierarchical references across modules, "
     "unbounded recursion in a function, four-state logic used arithmetically. Record "
     "what the tool actually said, not what you expected."),
    ("D9", "W", "Give the two-minute procedure for deciding whether a construct is "
     "synthesisable.",
     "Write a ten-line module containing only that construct, synthesise it, and read "
     "the output. Do not rely on memory or on advice about a different tool version."),
    ("D10", "H", "Which row in the table is the most dangerous, and why?",
     "The incomplete sensitivity list. Every other row either fails loudly or produces "
     "something you can see in the cell count. That one produces a working netlist "
     "that does not match the simulation you tested."),

    # ------------------------------------------------ E · sim vs silicon
    ("E1", "C", "Run make mismatch. How many of the six steps disagreed?",
     "One. That is the whole problem: five of six steps agreed, so casual testing "
     "finds nothing."),
    ("E2", "H", "Why did the other five steps agree?",
     "The RTL block only re-evaluates when a changes. On the steps where a changed, "
     "it recomputed and matched; on the steps where b changed while the result "
     "happened to be unaffected, both gave the same answer anyway."),
    ("E3", "C", "Change the list to always @(b) and predict which steps now disagree.",
     "The mirror image: the block now sleeps through changes of a. Run it and confirm "
     "your prediction before reading the output."),
    ("E4", "C", "Change it to always @* and confirm the disagreement count is zero.",
     "It is. @* builds the sensitivity list from what the block actually reads, and "
     "keeps it correct every time the block is edited."),
    ("E5", "W", "Explain in three sentences why this bug is worse than a syntax "
     "error.",
     "A syntax error stops you immediately and costs a minute. This produces a design "
     "where the simulation and the silicon compute different things, so every test you "
     "write passes and the chip still fails. The bug is found in the lab, on hardware, "
     "months later."),

    # --------------------------------------------------- F · coding rules
    ("F1", "H", "State rules L001 and L002 and the reason for each.",
     "L001: no blocking assignment in a clocked block, because two such blocks can "
     "see each other's half-updated values in an order the standard does not fix. "
     "L002: no non-blocking assignment in a combinational block, because it simulates "
     "like a register while synthesis builds logic."),
    ("F2", "C", "Run make lint on the good files and the bad files. How many rules "
     "fired, and on which lines?",
     "The four good files are clean. s12_bad_style trips L001, L003, L004 and L006; "
     "s13 trips L007; s03 trips L005; s04 trips L004."),
    ("F3", "C", "Run make lintcheck. What is it comparing, and why is that comparison "
     "worth making?",
     "The linter's L005/L006 latch prediction against whether Yosys actually put a "
     "$_DLATCH_ in the netlist. It turns two rules from opinions into predictions that "
     "have been checked on ten files."),
    ("F4", "H", "Why does the linter count blocking and non-blocking assignments with "
     "two separate patterns rather than subtracting one from the other?",
     "The blocking pattern already excludes <=, >=, != and ==, so the two counts are "
     "disjoint. Subtracting would cancel real detections - which is a bug this tool "
     "had until the self-test caught it."),
    ("F5", "C", "Add a rule L008 of your own, with a file that breaks it and a file "
     "that does not.",
     "Any defensible rule is acceptable. It must fire on the bad file, stay silent on "
     "the good one, and you must be able to say what bug it prevents."),
    ("F6", "C", "Find a file the linter gets wrong.",
     "Not hard - it is regular expressions. Nested if/else across many lines, "
     "generate blocks, and unusual formatting will all fool it. The point is to know "
     "the limits of your own tool."),
    ("F7", "W", "Why can a regular expression not decide the latch question in "
     "general?",
     "Deciding whether every path through a block assigns a signal requires "
     "understanding the block's control flow, which needs a parser and an analysis of "
     "reachability. Regexes match text, not structure."),
    ("F8", "W", "Why lint before simulating rather than after?",
     "Linting costs seconds and catches a class of bug that simulation structurally "
     "cannot - the ones where the simulation itself is testing the wrong circuit."),
    ("F9", "H", "A colleague says the coding rules are style preferences. Respond.",
     "Every one of the seven exists because breaking it produces a design that "
     "simulates differently from the way it is built. That is not taste; it is a "
     "correctness property, and the lintcheck target demonstrates two of them."),
    ("F10", "W", "What does 'a fix you cannot explain is not a fix' mean here?",
     "Silencing a lint message by rearranging code until the tool stops complaining "
     "does not remove the hazard. If you cannot say which bug the rule prevents and "
     "why your change prevents it too, you have moved the problem rather than solved "
     "it."),

    # ------------------------------------------------- G · two languages
    ("G1", "C", "Run make langs. What exactly was compared, and by what?",
     "The Verilog transcript from iverilog and the VHDL transcript from ghdl, "
     "compared line by line by diff. Identical over all 18 cycles."),
    ("G2", "H", "Name three things VHDL made explicit that Verilog left implicit.",
     "Library and package declarations; the separation of entity from architecture; "
     "type conversions between unsigned and std_logic_vector. Verilog would have let "
     "you add 1 to anything."),
    ("G3", "C", "Change the width to 8 in both files. Which needed more editing?",
     "Neither, if both were parameterised properly - which is the point of the "
     "exercise. If yours needed more editing in one language, that file was not as "
     "reusable as it looked."),
    ("G4", "W", "Your colleague only knows VHDL. What can they read of your Verilog?",
     "Almost all of it: the clocked process, the reset, the enable, the vector, the "
     "wrap. What will need explaining is notation - blocking against non-blocking, "
     "what reg means, and case sensitivity."),
    ("G5", "W", "Which language should someone starting today learn?",
     "The concepts first; the notation follows in an afternoon. In practice, whichever "
     "one the team uses - and expect to read the other. Large projects routinely mix "
     "them in one flow."),

    # ------------------------------------------------------- H · the flow
    ("H1", "C", "Run make flow. What evidence does each of the seven stages produce?",
     "Spec: four sentences. Lint: 0 issues. RTL sim: 18 cycles with the wrap checked. "
     "Synthesis: 12 cells. Gate sim: 18 cycles. Compare: identical. Prove: "
     "equivalence by induction."),
    ("H2", "C", "Introduce a lint violation and confirm the flow stops at stage 2.",
     "It should. A methodology in which a failing stage does not stop the flow is a "
     "checklist people tick, not a set of gates."),
    ("H3", "C", "Break the counter's wrap and see which stage catches it.",
     "Stage 3, the RTL simulation, because the spec said it must wrap and the "
     "transcript is checked against that."),
    ("H4", "C", "Find a change that passes stages 2 and 3 but fails stage 7.",
     "Anything that is functionally correct on the stimulus applied but not "
     "equivalent in general - for example a reset that is asynchronous in the RTL and "
     "synchronous in the netlist, or a wrap condition that differs only in a state "
     "the 18-cycle test never reaches."),
    ("H5", "W", "Stage 6 and stage 7 both compare the RTL with the netlist. What is "
     "the difference?",
     "Stage 6 compares them on the 18 cycles that were tested. Stage 7 proves they "
     "agree on every input sequence, by induction, without enumerating any."),
    ("H6", "C", "Add a stage 8 that fails if the netlist contains any latch.",
     "Grep the JSON for DLATCH, or count $_DLATCH_ cells and exit non-zero if the "
     "count is not zero. This is a real check that real teams run."),
    ("H7", "W", "Why is 'a stage that produces no evidence' a problem?",
     "Because nobody can tell whether it was run. A methodology is auditable only if "
     "each stage leaves something behind that a reviewer can look at."),
    ("H8", "W", "Which stage would you add next, and why?",
     "Reasonable answers: code coverage on the RTL simulation; a check that every "
     "output is driven; a constraint check; a second synthesis with different options "
     "to detect fragility. Any answer that names the bug the stage would catch."),
]


def build_exercises(w):
    w.h1("Exercises")

    w.callout("How to read the tags", [
        [B("[H] "), N("hand work - do it on paper before you touch a keyboard.  "),
         B("[C] "), N("computer - run it and record what you see.  "),
         B("[W] "), N("write it down - a paragraph you could defend in a design "
                      "review.")],
        [B("Predict before you measure. "),
         N("Almost every [C] exercise here is worth more if you write down what you "
           "expect first. Running the command and copying the output teaches very "
           "little.")],
    ], color=NAVY, bar="0E2A47")

    heads = {
        "A": ("Part A · What RTL means", "6 exercises · 1 hour"),
        "B": ("Part B · The abstraction ladder", "9 exercises · 2 hours"),
        "C": ("Part C · Proof, not just testing", "7 exercises · 2 hours"),
        "D": ("Part D · The synthesisable subset", "10 exercises · 2 hours"),
        "E": ("Part E · Simulation against silicon", "5 exercises · 1 hour"),
        "F": ("Part F · The coding rules", "10 exercises · 2 hours"),
        "G": ("Part G · Two languages", "5 exercises · 1 hour"),
        "H": ("Part H · The flow, end to end", "8 exercises · 2 hours"),
    }
    cur = None
    for eid, tag, q, _ in EX:
        if eid[0] != cur:
            cur = eid[0]
            h, sub = heads[cur]
            w.h2(h)
            w.para([I(sub, {"s": 9.5, "c": SLATE})], space_after=4)
        w.para([B("%s  [%s]  " % (eid, tag), {"c": TEAL}), N(q, {"s": 10.2})],
               space_after=5)

    w.page_break()


def build_solutions(w):
    w.h1("Worked Solutions")
    w.para([N("Every answer below was checked against the lab. Where a number is "
              "quoted it came from a real run; where a judgement is asked for, the "
              "solution gives the reasoning that earns the marks rather than a single "
              "word.", {"s": 10.2, "i": True})])

    cur = None
    for eid, tag, q, a in EX:
        if eid[0] != cur:
            cur = eid[0]
            w.h2("Part %s" % cur)
        w.para([B("%s  " % eid, {"c": TEAL}), I(q, {"s": 9.6, "c": SLATE})],
               space_after=2)
        w.para([N(a, {"s": 10.2})], space_after=8)

    w.page_break()


def build_reference(w):
    w.h1("Reference Card")

    w.h2("What RTL is")
    w.code([
        "An RTL description states TWO things and nothing else:",
        "    1. which registers exist",
        "    2. what transfers into each one, on each clock edge",
        "",
        "Everything between the registers is combinational logic with one clock",
        "period to settle. You never say how long it takes or which gates it uses."])

    w.h2("The two assignment operators")
    w.code([
        "<=   NON-BLOCKING   in CLOCKED blocks",
        "     read every right-hand side first (old values), then update all",
        "     left-hand sides at the same instant.   a<=b; b<=a;  SWAPS them.",
        "",
        "=    BLOCKING       in COMBINATIONAL blocks",
        "     each statement completes before the next starts, like software.",
        "                                            a=b;  b=a;   does NOT swap."])

    w.h2("The four levels of abstraction")
    w.table(["Level", "You specify", "Synthesises?", "Cells (full adder)"],
            [["behavioural", "the function", "yes", "5"],
             ["dataflow", "the Boolean form", "yes", "6"],
             ["gate", "every gate and wire", "yes", "6 (identical netlist)"],
             ["switch", "individual transistors", "no", "refused"]],
            widths=[1.4, 2.2, 1.3, 1.9], size=9.2, bold_cols=(0,),
            align_center=False)
    w.para([N("Write at the highest level that expresses your intent. Every level you "
              "descend takes a decision away from the tool and gives it to you.",
              {"b": True, "s": 10})])

    w.h2("The seven coding rules")
    w.table(["Rule", "What it catches"],
            [["L001", "blocking (=) in a clocked block - use <="],
             ["L002", "non-blocking (<=) in a combinational block - use ="],
             ["L003", "= and <= mixed in one always block"],
             ["L004", "explicit sensitivity list - use always @*"],
             ["L005", "if with no else in a combinational block - infers a latch"],
             ["L006", "case with no default - infers a latch"],
             ["L007", "signal driven from more than one always block"]],
            widths=[0.9, 5.9], size=9.2, bold_cols=(0,), align_center=False)

    w.h2("The synthesisable subset, at a glance")
    w.code([
        "ALWAYS FINE      always @*  ·  always @(posedge clk)  ·  assign",
        "                 for loops with constant bounds  ·  case with default",
        "                 parameters and localparams  ·  module instantiation",
        "",
        "NEVER            # delays  ·  real  ·  data-dependent while loops",
        "                 file I/O  ·  most system tasks",
        "",
        "TRAPS            initial      accepted by FPGA tools, ignored by ASIC flows",
        "                 if/case with no else/default   silently builds a LATCH",
        "                 always @(a)  synthesis ignores the list; simulation does not",
        "                 a / b        371 cells.  a / 4 is 0 cells."])

    w.h2("Commands")
    w.code([
        "make transfer   what register transfer level literally means",
        "make ladder     one adder at four levels, all simulated together",
        "make prove      formal proof that those levels are the same circuit",
        "make subset     which constructs synthesise, and what they cost",
        "make mismatch   RTL and its own netlist, disagreeing",
        "make lint       the seven rules, checked",
        "make lintcheck  and cross-checked against what Yosys builds",
        "make langs      the same design in Verilog and VHDL, both run",
        "make flow       the whole methodology: spec to formal proof",
        "",
        "python3 tools/rtl_lint.py <file.v> ...",
        "./scripts/equiv.sh fileA.v topA fileB.v topB"])

    w.callout("The three sentences to leave with", [
        [B("1.  "), N("RTL says which registers exist and what transfers into them. "
                      "Everything else is the tool's problem.")],
        [B("2.  "), N("Write at the highest level that expresses your intent - and "
                      "then check what the tool did with it.")],
        [B("3.  "), N("The dangerous bugs are the ones where the simulation and the "
                      "silicon are not the same circuit. Every coding rule in this "
                      "topic exists to prevent one of them.")],
    ], color=RED, fill="FDECEF", bar="D6224A")
