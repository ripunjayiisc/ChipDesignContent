# -*- coding: utf-8 -*-
"""Module 2 Topic 2 workbook — Theory Parts 2 and 3."""
import _boot
from wbkit import *
from m2t2_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 2
    w.h1("Part 2 · The RTL Design Process and Methodology")

    w.h2("2.1  The flow")

    w.image("design_flow", width=6.9)

    w.para([N("Every arrow points both ways in practice. A timing failure sends you "
              "back to the RTL; a synthesis surprise sends you back to the "
              "micro-architecture; a specification that turns out to be ambiguous "
              "sends you back further than anyone would like.")])

    w.h3("Executed, not described")
    w.para([N("A flow drawn on a slide is a picture of arrows. "), M("make flow"),
            N(" runs the same arrows on a real design and shows what each stage "
              "produces — because a stage that produces no evidence is a stage nobody "
              "can tell you skipped.")])

    w.image("flow_executed", width=6.9)

    w.code([
        "$ make flow",
        "  STAGE 1  SPECIFICATION      4 sentences, written before the RTL",
        "  STAGE 2  LINT               0 issues",
        "  STAGE 3  RTL SIMULATION     18 cycles; wraps at 15, tc correct",
        "  STAGE 4  SYNTHESIS          12 cells",
        "  STAGE 5  GATE SIMULATION    the netlist, same stimulus",
        "  STAGE 6  COMPARE            IDENTICAL on all 18 cycles",
        "  STAGE 7  PROVE              Equivalence PROVEN by induction",
        "",
        "  All seven stages passed."])

    w.callout("Stage 7 is the one worth understanding", [
        [N("Stage 6 says the RTL and the netlist agree on the 18 cycles that were "
           "tested. Stage 7 proves they agree on EVERY input sequence, by induction, "
           "without enumerating any of them.")],
        [N("The script stops at the first stage that fails. That is what makes it a "
           "methodology rather than a diagram.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("2.2  The synthesisable subset")

    w.para([N("\"Verilog is not a programming language\" stays a slogan until you "
              "watch a synthesiser refuse to build something. The lab runs eleven "
              "constructs through Yosys and reports what came out.")])

    w.image("synth_subset", width=6.9)

    w.h3("Three rows worth discussing")
    w.table(["Row", "What happened", "Why it matters"],
            [["a / b  against  a / 4", "371 cells against 0",
              "same operator; the difference is entirely what you divided BY. A "
              "constant power of two is a rename of wires."],
             ["#5 delay in RTL", "synthesised to 1 NOT gate",
              "the delay silently vanished. Silicon cannot wait five time units; the "
              "delay a gate has is set by the library and the layout."],
             ["initial block", "accepted, 10 cells",
              "Yosys targets FPGAs, where the bitstream really does initialise the "
              "flops. An ASIC flow would not — this is how code that works on an FPGA "
              "fails on an ASIC."]],
            widths=[1.6, 1.8, 3.4], size=10.0, bold_cols=(0,), align_center=False)

    w.callout("The habit this table is for", [
        [N("Before you use a construct you are unsure about, synthesise a ten-line "
           "module containing only that construct and read what came out. It takes "
           "two minutes and it is the only way to actually know, as opposed to "
           "remembering what someone told you about a different tool version.")],
    ], color=TEAL)

    w.h2("2.3  The inferred latch")

    w.image("latch_inference", width=6.9)

    w.para([N("When "), M("en"), N(" is 0 the code never says what "), M("y"),
            N(" should be — so the tool must build something that remembers the old "
              "value. That something is a level-sensitive latch, which you did not "
              "ask for and almost certainly do not want.")])

    w.table(["", "A flip-flop", "A latch"],
            [["captures", "on the clock EDGE", "while the enable is HIGH"],
             ["is transparent", "never", "for the whole enable window"],
             ["timing analysis", "one clean check per edge",
              "time-borrowing; much harder to analyse"],
             ["in a scan chain", "standard", "usually needs special handling"],
             ["you asked for it", "yes, by writing posedge", "no — you forgot an else"]],
            widths=[1.5, 2.4, 2.9], size=10.0, bold_cols=(0,), align_center=False)

    w.callout("Why it is worse than an error", [
        [N("It is not an error at all. The tool builds it, mentions it in a log nobody "
           "reads, and hands you a design with a memory element in the middle of what "
           "you thought was combinational logic — which then has its own timing "
           "requirements and quietly complicates your static timing analysis.")],
        [B("The rule is mechanical: "), N("in a combinational block, assign every "
           "output on every path. An if needs an else; a case needs a default. If you "
           "would rather not write them all out, assign a default at the top of the "
           "block and let later assignments override it.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("2.4  When simulation and silicon disagree")

    w.image("sim_synth_mismatch", width=6.9)

    w.para([N("This is the worst bug in the topic, because it is the only one that "
              "cannot be found by testing — the thing you are testing is not the "
              "thing that will be built. The lab drives the RTL and the netlist Yosys "
              "produced from it with identical stimulus:")])

    w.code([
        "$ make mismatch",
        "   change a  (list wakes)     a=1 b=0    RTL y=0    NETLIST y=0",
        "   change b  (list ASLEEP)    a=1 b=1    RTL y=0    NETLIST y=1  <-- DISAGREE",
        "",
        "  disagreements: 1 of 6",
        "  Your testbench was verifying a circuit that does not exist."])

    w.table(["Cause", "What simulation does", "What synthesis does"],
            [["incomplete sensitivity list",
              "the block sleeps; the output goes stale",
              "ignores the list; builds the logic"],
             ["# delays in RTL", "waits the specified time", "ignores them entirely"],
             ["initial block (ASIC)", "sets the value at time zero",
              "ignores it; the flop powers up unknown"],
             ["blocking in a clocked block", "result depends on evaluation order",
              "builds one specific circuit"]],
            widths=[2.1, 2.4, 2.3], size=10.0, bold_cols=(0,), align_center=False)

    w.callout("All four have the same cure", [
        [N("Use "), M("always @*"), N(" and never a hand-written sensitivity list. "
           "No delays in RTL. A real reset instead of an initial block. Non-blocking "
           "in clocked blocks.")],
        [N("Then lint for all four, so that nobody has to remember. "
           "SystemVerilog's "), M("always_comb"),
         N(" goes further and makes the tool check it for you.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("2.5  Seven coding rules, and a tool that checks them")

    w.image("lint_rules", width=6.9)

    w.para([N("Methodology degenerates into a list of good intentions unless something "
              "checks it. Every rule above is one a reviewer would otherwise have to "
              "remember, on every file, for ever — exactly the kind of job people are "
              "bad at and programs are good at. Every real RTL team lints before "
              "simulation, because a lint error costs seconds and the bug it prevents "
              "can cost a silicon revision.")])

    w.h3("Is the linter telling the truth?")
    w.para([N("Rules L005 and L006 claim that a missing "), M("else"),
            N(" or a missing "), M("default"), N(" infers a latch. That is a claim "
              "about what a synthesiser will do, so the synthesiser settles it:")])
    w.code([
        "$ make lintcheck",
        "  file                     linter says    yosys says     verdict",
        "  s03_latch                latch          latch          agree",
        "  s04_incomplete_sens      no latch       no latch       agree",
        "  s14_latch_case           latch          latch          agree",
        "  ... 10 files, 0 disagreements",
        "",
        "  L005 and L006 are not opinions - they predict what gets built."])

    w.image("coding_rules", width=6.9)

    w.para([N("None of these are style preferences. Every one exists because breaking "
              "it produces a design that simulates differently from the way it is "
              "built — and that class of bug survives every test you write.",
              {"b": True})])

    w.h2("2.6  Micro-architecture: the decisions RTL cannot make for you")

    w.image("partitioning", width=6.9)

    w.callout("This is where the engineering is", [
        [N("A synthesiser is better than you are at choosing gates. It is not better "
           "than you are at any of the rows in that table, and it will not warn you "
           "that you chose badly — it will faithfully build what you asked for.")],
        [B("Make these decisions on paper, before the first line of RTL.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("2.7  Writing RTL someone else can use")

    w.image("reuse", width=6.9)

    w.para([N("Module 2's fourth terminal outcome asks for reusable IP by name. "
              "Reuse is not something you add to a design afterwards; it is a set of "
              "decisions taken while writing it. The test is simple: could a "
              "colleague drop this into a different design, next year, without asking "
              "you anything? If the answer needs a conversation, it is not reusable "
              "yet.")])

    w.h2("2.8  Coding style: one function, three ways")

    w.image("mux_styles", width=6.9)

    w.para([N("A four-to-one multiplexer can be written as a conditional expression, "
              "as a case statement, or as an if/else chain. The usual classroom "
              "claim is that the optimiser flattens the difference, so you should "
              "write whichever reads best. Half of that is right.")])

    w.code([
        "$ make mux",
        "  patterns checked : 64        mismatches : 0",
        "  mux4_assign vs mux4_case      EQUIVALENT  (proved, 92 SAT variables)",
        "  mux4_assign vs mux4_if        EQUIVALENT  (proved, 76 SAT variables)",
        "",
        "  mux4_assign                     3 cells     0 flip-flops",
        "  mux4_if                         6 cells     0 flip-flops",
        "  mux4_case                      10 cells     0 flip-flops"])

    w.callout("Equivalent is not the same as identical", [
        [N("The SAT proof answers exactly one question: do these three descriptions "
           "compute the same Boolean function? They do. It says nothing whatever "
           "about area, timing or power — those are separate questions with separate "
           "tools.")],
        [N("The conditional expression hands sel[1] and sel[0] straight to the "
           "multiplexer selects. The case and if/else versions ask the tool to build "
           "equality comparators against 2'b00, 2'b01 and so on, and then to work "
           "out for itself that those comparisons ARE the select bits. On Yosys 0.33 "
           "it gets part of the way.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.para([N("So which do you write? Whichever reads best to the next person — "
              "usually the case statement once there are more than three branches — "
              "and then "), B("measure"), N(", on your own tool, if the block turns "
              "out to be on a critical path. A different synthesiser may well close "
              "the gap. Folklore about what optimisers do is the least reliable kind "
              "of knowledge in this field, and it is cheap to replace with a "
              "measurement.")])

    w.callout("Part 2 self-check", [
        [N("1.  Name the first four stages of the flow, and say what evidence each "
           "produces.")],
        [N("2.  Why lint before simulating rather than after?")],
        [N("3.  What exactly builds a latch?")],
        [N("4.  a / b cost 371 cells and a / 4 cost 0. Explain.")],
        [N("5.  Why is an incomplete sensitivity list worse than a syntax error?")],
        [N("6.  Name three decisions synthesis will not make for you.")],
        [N("7.  Does a formal equivalence proof say anything about area?")],
        [N("8.  Three mux styles gave 3, 6 and 10 cells. Explain why.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()


def build_hdl(w):
    """Part 4 - HDLs. Called after the patterns part, which is Part 3."""
    w.h1("Part 4 · Hardware Description Languages")

    w.h2("4.1  An HDL is not a programming language")

    w.image("what_is_hdl", width=6.9)

    w.para([N("It looks like one, and that resemblance is the single biggest source of "
              "beginner bugs. You are not writing instructions for a machine to "
              "follow; you are writing a "), B("description of a machine"),
            N(", which a tool will then build. The text is a blueprint, not a recipe.")])
    w.para([N("Which is why \"it compiles\" means almost nothing here, and why a "
              "construct can be perfectly legal Verilog and still have no hardware "
              "meaning at all — as the subset table in Part 2 measured.")])

    w.h2("4.2  Everything happens at once")

    w.image("concurrency", width=6.9)

    w.para([N("Write those three "), M("assign"), N(" lines in any order you like and "
              "the circuit is identical, because you did not write a sequence — you "
              "wrote three facts about three pieces of hardware that all exist "
              "together, permanently.")])
    w.para([N("The one place order does matter is inside a single always block using "
              "blocking assignments, where statements do run in order, like software. "
              "That is exactly why mixing "), M("="), N(" and "), M("<="),
            N(" in one block is confusing enough to be a lint rule.")])

    w.h2("4.3  The anatomy of a module")

    w.image("module_anatomy", width=6.9)

    w.callout("The word that confuses everyone: reg", [
        [M("reg"), N(" does NOT mean register. It means \"this signal is assigned "
           "inside a procedural block\". A "), M("reg"), N(" assigned in an "),
         M("always @*"), N(" block becomes pure combinational logic with no storage "
           "whatsoever.")],
        [N("What actually creates a flip-flop is assigning inside "),
         M("always @(posedge clk)"), N(" — nothing else. SystemVerilog renamed "),
         M("reg"), N(" to "), M("logic"), N(" precisely to end this confusion.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("4.4  How a simulator runs an HDL")

    w.image("event_simulation", width=6.9)

    w.para([N("Nothing runs continuously. The simulator jumps from event to event: a "
              "signal changes, everything sensitive to it wakes, they are all "
              "evaluated, non-blocking results are queued, the queue is applied at "
              "once, and the process repeats until nothing more changes — only then "
              "does time advance.")])

    w.callout("Step 3 is why RTL has coding rules at all", [
        [N("The order in which woken blocks are evaluated is genuinely unspecified by "
           "the standard. Two clocked blocks using blocking assignments can see each "
           "other's half-finished work, and which one wins may differ between "
           "simulators, or between runs of the same simulator.")],
        [N("Non-blocking assignment exists to make that impossible: every right-hand "
           "side is read before any left-hand side is updated, so evaluation order "
           "cannot affect the result.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("4.5  Verilog and VHDL")

    w.image("verilog_vhdl", width=6.9)

    w.para([N("None of those differences are about hardware. Both describe registers, "
              "combinational logic and hierarchy; both synthesise to the same gates. "
              "An engineer who understands RTL can read the other one after an "
              "afternoon; an engineer who has only memorised syntax can read "
              "neither.")])

    w.h3("The same designs, in both languages, actually run")
    w.image("two_languages_result", width=6.9)

    w.code([
        "$ make langs",
        "  === Verilog: iverilog ===",
        "    cycle 14  count=1111  tc=1",
        "    cycle 15  count=0000  tc=0",
        "  === VHDL: ghdl ===",
        "    cycle 14  count=1111  tc=1",
        "    cycle 15  count=0000  tc=0",
        "  === diff of the two transcripts ===",
        "  IDENTICAL over all 18 cycles - including the wrap and the terminal count.",
        "",
        "  === the same '101' detector, both languages ===",
        "  IDENTICAL over all 17 cycles, detections included."])

    w.para([N("Not \"they look similar\". The logs were compared line by line by "
              "diff, through two different simulators, and there was nothing to "
              "report.", {"b": True})])

    w.para([N("The state machine is the more interesting of the two, because it is "
              "where the languages genuinely differ. In Verilog the states are "
              "numbers you chose; in VHDL they are a "), B("type"), N(":")])
    w.code([
        "// Verilog",
        "localparam [1:0] S_IDLE = 2'd0, S_1 = 2'd1, S_10 = 2'd2, S_101 = 2'd3;",
        "",
        "-- VHDL",
        "type state_t is (S_IDLE, S_1, S_10, S_101);",
        "signal state, next_state : state_t;"])
    w.para([N("The VHDL version cannot be assigned a value that is not one of those "
              "four — the analyser rejects it — and it also rejects a case statement "
              "that is not exhaustive. The Verilog version will accept "),
            M("state <= 2'd7"), N(" and nobody will complain until silicon. That is "
              "the trade in one sentence: VHDL catches more mistakes at compile time "
              "and costs more keystrokes; Verilog is faster to write and trusts you "
              "more than it should.")])

    w.h2("4.6  Reference cards, and what a testbench is made of")

    w.para([N("The two pages that follow are the whole of the language you need for "
              "this topic — not the whole of Verilog or VHDL, which are both far "
              "larger, but the part that synthesises. Keep them beside you until "
              "you no longer need them.")])

    w.image("verilog_card", width=6.9)
    w.image("vhdl_card", width=6.9)

    w.h3("Verilog to VHDL, line for line")
    w.image("lang_mapping", width=6.9)

    w.h3("The anatomy of a testbench")

    w.image("testbench_anatomy", width=6.9)

    w.para([N("Topic 5 covers verification properly. Six parts are enough to finish "
              "Topic 2, and the fourth is the one people leave out:")])
    w.numbered([
        [B("Clock. "), M("always #5 clk = ~clk;"), N(" — nothing else generates it.")],
        [B("Reset. "), N("Asserted before anything else, and released away from the "
           "sampling edge on purpose.")],
        [B("Stimulus. "), N("Driven on the inactive edge, sampled before the active "
           "one, so the design never sees a value changing at the instant it "
           "samples.")],
        [B("Golden model. "), N("The expected answer, computed from the STIMULUS "
           "and never from the design under test.")],
        [B("Checker. "), N("The line that compares them and counts. This is what "
           "makes a testbench self-checking.")],
        [B("Verdict. "), N("One line a human can read without opening a waveform.")],
    ])

    w.callout("A testbench without a golden model is not a test", [
        [N("If the expected answer comes from the design, the test passes whatever "
           "the design does. Every checker in this lab computes its expectation from "
           "the stimulus — which is the only reason it was able to print "),
         M("blocking version : 6 wrong cycles"), N(" at all.")],
        [N("Eyeballing a waveform is not a checker either. It does not scale past "
           "about ten cycles, and it never runs twice.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("4.7  Which one should you learn?")

    w.image("hdl_choose", width=6.9)

    w.callout("Part 4 self-check", [
        [N("1.  Give the biggest single difference between an HDL and a programming "
           "language.")],
        [N("2.  Does the order of assign statements matter? Why not?")],
        [N("3.  What does reg actually mean, and what actually creates a flip-flop?")],
        [N("4.  Why does the standard leave evaluation order unspecified, and what "
           "saves you from it?")],
        [N("5.  Your colleague only knows VHDL. What can they read of your Verilog, "
           "and what will they need explained?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
