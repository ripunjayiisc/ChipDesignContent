# -*- coding: utf-8 -*-
"""Topic 5 deck — 5c: simulation and debugging, tools, labs, close."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def C(t, **kw):
    d = {"t": t}
    d.update(kw)
    return [d]


def build(d):
    # =============================================== SECTION 5C
    d.section_slide("SUBTOPIC 5C", "Simulation and Debugging of RTL Designs",
                    "How the simulator actually works, and what to do when the answer is wrong.",
                    ["The event-driven engine, and what happens inside one time step",
                     "Analyse, elaborate, run — the same three steps in every tool",
                     "Waveforms: dumping, reading, and saving a view",
                     "A debugging procedure: bisect in time, bisect in space, chase the x",
                     "Symptom-to-cause, and how to make simulation fast enough to live with"],
                    accent=VIOLET)

    # ============================================================ engine
    s = d.slide("TOPIC 5C · THE ENGINE", "A Simulator Runs Events, Not Instructions")
    y = d.lead(s, TOP, [[
        R("A digital simulator does not step through your code. ", b=True, c=NAVY, s=12.5),
        R("It keeps a queue of scheduled EVENTS ordered by time, and at each time it wakes only "
          "the blocks sensitive to what changed. Understanding that explains almost every "
          "surprising thing a simulation does.")]], h=594360)
    y = d.image(s, y + 45720, "sim_engine", 3383280)
    d.cols(s, y + G, [
        ("Why simulation time is not wall-clock time",
         [[R("A million simulated clock cycles may take a second or an hour, depending entirely "
             "on how much of the design is switching. Time in the simulator advances only when "
             "there is nothing left to do at the current time.", s=10.5)]], TEAL, CARD),
        ("Why a loop with no delay hangs",
         [[R("while (!done) ;", f=MONO_FONT, b=True, c=RED, s=10.5),
           R("  in a testbench never lets simulation time advance, so ", s=10.5),
           R("done", f=MONO_FONT, s=10.5),
           R(" can never change. The simulator is not stuck — it is doing exactly what you "
             "wrote. Every wait loop needs an @ or a #.", s=10.5)]], RED, CARD_R)], h=1188720)

    # ============================================================ regions
    s = d.slide("TOPIC 5C · ONE TIME STEP", "The Stratified Event Queue")
    y = d.lead(s, TOP, [[
        R("Several events can be scheduled at the SAME simulation time. ", b=True, c=NAVY,
          s=12.5),
        R("The standard defines regions that are processed in order, and that ordering is what "
          "makes non-blocking assignment model a flip-flop correctly.")]], h=548640)
    y = d.image(s, y + 45720, "event_regions", 3383280)
    d.card(s, y + G, "The practical consequence you will meet first",
           [[R("$display", f=MONO_FONT, b=True, c=NAVY),
             R(" runs in the ACTIVE region, so at a clock edge it prints the value from BEFORE "
               "the edge. "), R("$strobe", f=MONO_FONT, b=True, c=GREEN),
             R(" runs in the MONITOR region, after every non-blocking update has landed, so it "
               "prints the settled value. If a printout disagrees with the waveform by exactly "
               "one cycle, this is why.")]],
           accent=AMBER, fill=CARD_A, h=960120)

    # ============================================================ three steps
    s = d.slide("TOPIC 5C · THE FLOW", "Analyse, Elaborate, Run")
    y = d.lead(s, TOP, [[
        R("Every simulator you will ever use does the same three things. ", b=True, c=NAVY,
          s=12.5),
        R("Only the command names change — which is why moving between Icarus, xsim and "
          "ModelSim is a morning's work rather than a new skill.")]], h=548640)
    y = d.image(s, y + 45720, "compile_elab_run", 3657600)
    d.card(s, y + G, "Where each kind of error appears",
           [[R("ANALYSE ", b=True, c=TEAL),
             R("reports syntax errors and undeclared names — file and line.   "),
             R("ELABORATE ", b=True, c=VIOLET),
             R("reports missing modules, port mismatches and parameter problems.   "),
             R("RUN ", b=True, c=GREEN),
             R("is where your logic is finally wrong. Knowing which step failed tells you which "
               "kind of mistake you made.")]],
           accent=TEAL, h=868680)

    # ============================================================ vcd
    s = d.slide("TOPIC 5C · WAVEFORMS", "How a Waveform Gets Onto Your Screen")
    y = d.lead(s, TOP, [[
        R("The simulator does not draw waveforms. ", b=True, c=NAVY, s=12.5),
        R("Your testbench asks it to write a change-log file, and a separate program draws that. "
          "Knowing this explains why dumping is optional, why it is slow, and why the file can "
          "be enormous.")]], h=594360)
    y = d.image(s, y + 45720, "vcd_flow", 3200400)
    d.table(s, y + G,
            ["Format", "Written by", "Note"],
            [["VCD", "any simulator; $dumpvars", "plain text, universal, large"],
             ["FST", "Icarus (-fst), GTKWave", "compressed VCD; much smaller and faster"],
             ["WLF", "ModelSim / Questa", "native, fast, read by their own viewer"],
             ["FSDB", "commercial (Verdi)", "the industry standard on large projects"]],
            [2011680, 4023360, 5212080], rh=283464, bold_cols=(0,), size=10)

    # ============================================================ gtkwave
    s = d.slide("TOPIC 5C · WAVEFORMS", "Reading a Waveform Viewer Properly")
    y = d.lead(s, TOP, [[
        R("Most students open a viewer, drag in every signal, and stare. ", b=True, c=NAVY,
          s=12.5),
        R("Four habits turn it from a wall of lines into an instrument.")]], h=502920)
    y = d.image(s, y + 45720, "gtkwave_tour", 3474720, w=MW)
    d.cols(s, y + G, [
        ("Group and order",
         [[R("Stimulus at the top, DUT outputs next, internals last. A jumbled list hides the "
             "answer in plain sight.", s=9.5)]], TEAL, CARD),
        ("Set the radix",
         [[R("A counter in binary is unreadable; in hex the pattern is obvious. Right-click the "
             "signal to change it.", s=9.5)]], VIOLET, CARD),
        ("Use the marker",
         [[R("Put it on the FIRST wrong cycle named in the transcript, then walk backwards, "
             "signal by signal.", s=9.5)]], AMBER, CARD_A),
        ("Save the view",
         [[R("File → Write Save File writes a .gtkw. Commit it, open with "), 
           R("gtkwave v3.vcd wave/v3_fifo.gtkw", f=MONO_FONT, b=True, c=GREEN, s=8.6),
           R(" and everyone sees the SAME picture.", s=9.5)]], GREEN, CARD_G)], h=1188720)

    # ============================================================ debug
    s = d.slide("TOPIC 5C · DEBUGGING", "A Procedure, Not a Talent")
    y = d.lead(s, TOP, [[
        R("Fast debuggers are not more clever — they are more systematic. ", b=True, c=NAVY,
          s=12.5),
        R("Two searches, and a ladder of checks run in cost order.")]], h=502920)
    y = d.image(s, y + 45720, "debug_method", 3749040)
    d.card(s, y + G, "The single most important habit",
           [[R("Find the FIRST moment things went wrong, never the moment you noticed. ",
               b=True, c=RED),
             R("A wrong output is usually many cycles downstream of the cause, and every cycle "
               "you spend looking at the output is a cycle not spent looking at the cause.")]],
           accent=RED, fill=CARD_R, h=822960)

    # ============================================================ x chase
    s = d.slide("TOPIC 5C · DEBUGGING", "Chasing an x")
    y = d.lead(s, TOP, [[
        R("An x is the simulator saying \"I cannot determine this\". ", b=True, c=NAVY, s=12.5),
        R("It spreads through every expression it touches, so by the time you see it on an "
          "output it may have travelled through ten signals.")]], h=548640)
    y = d.image(s, y + 45720, "x_chase", 3383280)
    d.cols(s, y + G, [
        ("The five usual causes",
         [[R("1. A register that was never reset.   2. A wire nothing drives — often a typo in "
             "a port connection.   3. A wire TWO things drive.", s=10.5)],
          [R("4. Reading past the end of a vector or an array.   5. Arithmetic on a value that "
             "was already x.", s=10.5)]], RED, CARD_R),
        ("And one prevention",
         [[R("`default_nettype none", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R(" at the top of every file turns a misspelt port connection from a silent undriven "
             "wire into a compile error naming the line. It costs one line and removes an entire "
             "category of x.", s=10.5)]], GREEN, CARD_G)], h=1234440)

    # ============================================================ signatures
    s = d.slide("TOPIC 5C · TROUBLESHOOTING", "Symptom to Cause")
    y = d.lead(s, TOP, [[
        R("Most failures have a signature. ", b=True, c=NAVY, s=12.5),
        R("Recognising it is most of the debugging — and this table is worth printing and "
          "putting on the wall of the lab.")]], h=502920)
    d.image(s, y + 45720, "failure_signatures", 4297680)

    # ============================================================ speed
    s = d.slide("TOPIC 5C · SPEED", "Making Simulation Fast Enough to Live With")
    y = d.lead(s, TOP, [[
        R("A regression that takes all night gets run once a week; a regression that takes five "
          "minutes gets run on every commit. ", b=True, c=NAVY, s=12.5),
        R("Simulation speed is therefore a verification-quality issue, not a convenience.")]],
        h=594360)
    y = d.table(s, y + 45720,
                ["What costs time", "Why", "What to do about it"],
                [["Waveform dumping", "every signal change becomes a line of text",
                  "dump nothing in a regression; re-run the failing seed with dumping on"],
                 ["Dumping the whole hierarchy", "$dumpvars(0, tb) includes every instance",
                  "$dumpvars(1, tb.u_dut) once you know where to look"],
                 ["A clock that never stops", "every edge wakes every clocked block",
                  "stop the clock when the test is idle, if the design allows it"],
                 ["Very fine timescale", "1ps precision means more scheduling work",
                  "1ns/1ps is plenty for RTL; you are not doing SPICE"],
                 ["$display in a hot loop", "formatting and I/O are slow",
                  "print on events, not on cycles"],
                 ["Long random runs at one seed", "one long run is not better than many short ones",
                  "many shorter runs, different seeds — and they parallelise"]],
                [2926080, 3840480, 4480560], rh=329184, bold_cols=(0,), size=9.5)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Verilator compiles the design to C++ and is often 10–100× faster than an "
          "interpreted simulator — which is why it is used for long random regressions even "
          "on projects whose sign-off simulator is a vendor tool.", s=10.5, i=True, c=SLATE)]])

    # =============================================== TOOLS
    d.section_slide("TOPIC 5 · TOOLS", "Software Tools — Installation and Flow",
                    "The syllabus specifies Vivado Design Suite and ModelSim. The open-source "
                    "chain does the same jobs and installs in a minute.",
                    ["What each tool does, and which one to reach for",
                     "Installing the open-source verification flow",
                     "Driving Vivado xsim and ModelSim / Questa",
                     "Regression scripting, and what a CI loop looks like"],
                    accent=NAVY)

    # ============================================================ tool matrix
    s = d.slide("TOPIC 5 · TOOLS", "The Verification Jobs, and the Tool for Each")
    y = d.lead(s, TOP, [[
        R("Four jobs — lint, simulate, view, measure. ", b=True, c=NAVY, s=12.5),
        R("Every flow does all four; only the command names change.")]], h=457200)
    y = d.image(s, y + 45720, "tool_matrix", 3657600)
    d.card(s, y + G, "Honesty note for the trainer",
           [[R("Every result quoted in this deck was produced by the open-source column — "
               "Icarus Verilog 12.0 and Verilator 5.020 — on the code in Topic5_Lab. The Vivado "
               "and ModelSim scripts in the lab are working templates written from standard, "
               "version-stable commands, but they were NOT executed, because neither tool is "
               "installed in the authoring environment. Check them against your release before "
               "the session.")]],
           accent=RED, fill=CARD_R, h=1005840)

    # ============================================================ install
    s = d.slide("TOPIC 5 · INSTALL", "The Open-Source Verification Flow")
    y = d.image(s, TOP, "install_map", 3383280)
    y = d.code(s, y + G, [
        C("# ---- Ubuntu / Debian / WSL2 -------------------------------------------", c=CMT),
        "sudo apt update && sudo apt install -y iverilog gtkwave verilator yosys graphviz",
        "",
        C("# ---- verify ------------------------------------------------------------", c=CMT),
        "iverilog -V | head -1     # Icarus Verilog version 12.0",
        "verilator --version       # Verilator 5.020",
        "gtkwave --version",
    ], size=9.5, title="Copy-paste installation")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("macOS: ", s=10.5, b=True, c=NAVY),
        R("brew install icarus-verilog verilator gtkwave", f=MONO_FONT, s=10.5),
        R("     Windows: run the Ubuntu line inside WSL2 (", s=10.5),
        R("wsl --install", f=MONO_FONT, s=10.5),
        R(" in an admin PowerShell), or unzip the OSS CAD Suite.", s=10.5)]])

    # ============================================================ vendor
    s = d.slide("TOPIC 5 · VENDOR TOOLS", "Vivado xsim and ModelSim / Questa")
    y = d.cols(s, TOP, [
        ("Vivado simulator (xsim)",
         [[R("xvlog -d DUT=fifo_b1 rtl/*.v tb/tb_v3_random.v", f=MONO_FONT, s=9.5)],
          [R("xelab -debug typical tb_v3_random -s sim", f=MONO_FONT, s=9.5)],
          [R("xsim sim -runall -testplusarg SEED=1", f=MONO_FONT, s=9.5)],
          [R("", s=9)],
          [R("· ", s=10.5), R("-d NAME=value", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" passes a `define, exactly like -D to iverilog.", s=10.5)],
          [R("· ", s=10.5), R("-testplusarg", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" passes a plusarg, so the SAME seed gives the same run as under Icarus.", s=10.5)],
          [R("· Supports the FULL SystemVerilog assertion language, including the ranged delay "
             "forms the open-source flow cannot handle.", s=10.5, c=GREEN, b=True)]],
         TEAL, CARD),
        ("ModelSim / Questa",
         [[R("vlib work", f=MONO_FONT, s=9.5)],
          [R("vlog -sv +define+DUT=fifo_b1 rtl/*.v sva/*.sv tb/*.sv", f=MONO_FONT, s=9.5)],
          [R("vsim -voptargs=+acc -assertdebug +SEED=7 work.tb_v6_assert", f=MONO_FONT, s=9.5)],
          [R("assertion fail -action break -r /*", f=MONO_FONT, s=9.5)],
          [R("run -all", f=MONO_FONT, s=9.5)],
          [R("· ", s=10.5), R("+acc", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" keeps signal visibility — without it the optimiser removes the very signals you "
             "want to see.", s=10.5)],
          [R("· ", s=10.5), R("-assertdebug", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" reports every assertion pass and failure, and can break on the first failure.",
             s=10.5)]], GREEN, CARD_G)], h=3017520)
    d.card(s, y + G, "Both flows are scripted in the lab",
           [[R("scripts/vivado_sim.tcl", f=MONO_FONT, b=True, c=NAVY),
             R(" takes a lab and a DUT as arguments; "),
             R("scripts/modelsim_run.do", f=MONO_FONT, b=True, c=NAVY),
             R(" takes them as -g parameters. Both cover all six labs and all six designs, so "
               "the clinic can be reproduced on the vendor tools exactly as it is on the "
               "open-source ones.")]],
           accent=TEAL, h=960120)

    # ============================================================ regression
    s = d.slide("TOPIC 5 · REGRESSION", "What Turns Random Stimulus Into Evidence")
    y = d.lead(s, TOP, [[
        R("A single random run is one sample. ", b=True, c=NAVY, s=12.5),
        R("A regression — many seeds, several profiles, run automatically after every change — "
          "is what makes it evidence.")]], h=502920)
    y = d.image(s, y + 45720, "regression_loop", 3383280)
    y = d.code(s, y + G, [
        C("$ ./scripts/regress.sh 4", c=TEAL),
        "  regression on fifo : 4 seeds x 3 profiles",
        "  ...",
        "  12 passed, 0 failed",
        "  REGRESSION CLEAN",
    ], size=9.5)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("When a run fails, the script prints the exact command that reproduces it. That one "
          "line is the difference between a bug report somebody can act on and one they cannot.",
          s=10.5, i=True, c=SLATE)]])

    # =============================================== LABS
    d.section_slide("TOPIC 5 · PRACTICAL", "The Lab Programme",
                    "Six labs, thirty-four hours, inside the syllabus practical component: "
                    "simulating and verifying the functionality of RTL designs.",
                    ["V1 naive · V2 model + corners · V3 random · V4 coverage · "
                     "V5 clinic · V6 layered + assertions",
                     "One DUT, five planted bugs, and a measured catch rate for every stage",
                     "Scripts for the open-source chain, Vivado and ModelSim",
                     "Assessment rubric and the troubleshooting table"], accent=GREEN)

    # ============================================================ lab table
    s = d.slide("TOPIC 5 · LABS", "The Six Labs")
    d.lead(s, TOP, [[
        R("Every lab builds on the one before, against the same device under test. ",
          b=True, c=NAVY, s=12.5),
        R("Nothing is thrown away; the testbench grows.")]], h=411480)
    y = d.table(s, 1554480,
                ["Lab", "h", "What you build", "What it teaches"],
                [["V1 naive", "3", "a directed testbench with all six parts",
                  "structure, a verdict, and why passing is not proving"],
                 ["V2 model", "6", "a reference model and the boundary cases",
                  "expected values come from the spec, not from you"],
                 ["V3 random", "6", "weighted constrained-random, seeded",
                  "reproducibility, and the corner nobody writes"],
                 ["V4 coverage", "6", "a coverage model, sampled and merged",
                  "what did I actually test, and when do I stop"],
                 ["V5 clinic", "5", "diagnosis of five unknown bugs",
                  "bisection, x-chasing, reading a waveform properly"],
                 ["V6 capstone", "8", "a layered environment with assertions",
                  "separation of concerns; assertions vs scoreboards"]],
                [1920240, 548640, 3840480, 4937760], rh=365760, bold_cols=(0,), size=9.5,
                col_colors={0: NAVY})
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Thirty-four hours, from the syllabus practical bullet \"simulating and verifying "
          "the functionality of RTL designs\".", s=10.5, i=True, c=SLATE)]])
    y = d.cols(s, y + 274320, [
        ("What every lab produces",
         [[R("· A lint run that is clean.", s=10.5)],
          [R("· A simulation transcript ending in a machine-readable PASS or FAIL.", s=10.5)],
          [R("· From V4 on, a coverage report with a closure verdict.", s=10.5)],
          [R("· One sentence from the student on what their testbench would NOT catch.",
             s=10.5)]], GREEN, CARD_G),
        ("Running short of time?",
         [[R("Do not cut V5, the clinic. ", b=True, c=RED, s=10.5),
           R("It is the only exercise where students meet a bug they did not plant, with no "
             "hint about what it is — which is the actual job. Shorten V1 instead: the naive "
             "testbench can be read rather than typed, provided the room still watches it pass "
             "on all five broken designs.", s=10.5)]], RED, CARD_R)], h=1234440)
    d.card(s, y + G, "Worth ten minutes of the session",
           [[R("Have every student plant ONE bug in a copy of the golden FIFO and hand it to a "
               "neighbour, whose testbench must catch it and name it.")]],
           accent=TEAL, h=594360)

    # ============================================================ running a session
    s = d.slide("TOPIC 5 · LABS", "How to Run the Session")
    y = d.tiers(s, TOP, [
        ("OPEN WITH THE CLINIC",
         "Do not begin with theory. Run ./scripts/clinic.sh live, in front of the room, before "
         "explaining anything. The table — 0 of 5, 4 of 5, 5 of 5 — does the persuading, and "
         "everything afterwards is the explanation of why.", RED),
        ("READ THE SPEC FIRST",
         "Have the class read the header comment of rtl/fifo.v and list, on the board, every "
         "rule it states. That list IS the verification plan. Only then look at a testbench.",
         NAVY),
        ("BUILD, DO NOT COPY",
         "V1 and V2 are typed from scratch, not copied. The supplied versions are for comparing "
         "against afterwards. The point is the decisions, and you only meet them by making them.",
         TEAL),
        ("BREAK IT ON PURPOSE",
         "Every student plants one bug in a copy of the golden FIFO and hands it to a "
         "neighbour, whose testbench must catch it. This single exercise teaches more about "
         "verification than any lecture, and the room enjoys it.", AMBER),
        ("CLOSE WITH COVERAGE",
         "Finish on ./scripts/coverage.sh. Passing tests feel like the end; the coverage report "
         "showing three MISSes is what teaches that they are not.", GREEN),
    ], h=822960, gap=45720)

    # ============================================================ common errors
    s = d.slide("TOPIC 5 · TROUBLESHOOTING", "What Your Students Will Hit")
    d.lead(s, TOP, [[
        R("Testbench problems, not design problems. ", b=True, c=NAVY, s=12.5),
        R("Nine out of ten support questions in this topic are one of these.")]], h=411480)
    d.table(s, 1554480,
            ["Symptom", "Almost always means", "Fix"],
            [["Everything is x from time 0", "reset never asserted, or the DUT port is misspelt",
              "check reset polarity; `default_nettype none"],
             ["The check passes when the value is x", "== used instead of ===",
              "use === and !== in every testbench check"],
             ["The design looks one cycle late", "sampled before the NBA update landed",
              "sample after the NEXT edge, or use $strobe"],
             ["A pulse is half a cycle wide", "stimulus driven ON the clock edge",
              "drive at #1 after the edge, never on it"],
             ["Random test passes but drove 9 transactions", "$urandom(seed) called in the loop",
              "seed once with void'($urandom(s)), then $urandom()"],
             ["The correct design fails", "the reference model is wrong",
              "sample full/empty once, before applying either operation"],
             ["Simulation never ends", "no $finish, or a wait loop with no delay",
              "add $finish and a watchdog timeout"],
             ["The waveform has no signals", "$dumpvars scope too narrow, or a stale VCD",
              "$dumpvars(0, tb); and re-run before re-opening"],
             ["Coverage is 100% but bugs escape", "the coverage model is too coarse",
              "add bins for SEQUENCES, not just states"]],
            [3200400, 4023360, 4023360], rh=283464, bold_cols=(0,), size=9,
            col_colors={0: NAVY})

    # ============================================================ assessment
    s = d.slide("TOPIC 5 · ASSESSMENT", "What 'Done' Looks Like")
    y = d.lead(s, TOP, [[
        R("Assess the testbench, not the design. ", b=True, c=NAVY, s=12.5),
        R("Give every student the same correct FIFO and the same five broken ones, and grade "
          "them on what their own testbench catches.")]], h=548640)
    y = d.table(s, y + 45720,
                ["Level", "Evidence"],
                [["Pass", "The testbench is self-checking, prints PASS or FAIL, terminates, and "
                          "catches at least three of the five planted bugs."],
                 ["Good", "All of the above, plus: it catches all five, and the student can say "
                          "which check caught each one and why."],
                 ["Strong", "All of the above, plus: a coverage model with a closure verdict, "
                            "and a regression over several seeds and profiles."],
                 ["Excellent", "All of the above, plus: assertions bound to the DUT, and the "
                               "student can explain a bug that assertions cannot catch and why "
                               "the scoreboard is needed too."]],
                [1737360, 9509760], rh=457200, bold_cols=(0,), size=10,
                col_colors={0: NAVY})
    d.card(s, y + G, "One question to ask every student",
           [[R("\"Show me a change to the design that your testbench would NOT catch.\" ",
               b=True, c=TEAL),
             R("If they can answer immediately, they understand verification. If they cannot, "
               "they have been testing rather than verifying.")]],
           accent=TEAL, h=776224)

    # ============================================================ glossary
    s = d.slide("TOPIC 5 · GLOSSARY", "Terms Used in This Topic")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["Verification", "establishing that a design does what its specification says."],
             ["Validation", "establishing that the specification was the right one. A different "
                            "question, usually answered by somebody else."],
             ["DUT", "device under test — the design the testbench instantiates."],
             ["Testbench", "a port-less module that instantiates the DUT, drives it, and decides "
                           "automatically whether the results were correct."],
             ["Self-checking", "the testbench forms its own verdict; no human reads a waveform "
                               "to decide."],
             ["Reference model", "an independent implementation of the specification, written "
                                 "from the spec, used to compute expected results."],
             ["Scoreboard", "the component that compares DUT behaviour against the model."],
             ["Directed test", "a test whose case and expected result you wrote by hand."],
             ["Constrained-random", "stimulus generated by weighted random choice within "
                                    "constraints you specify."],
             ["Seed", "the number that makes a random run reproducible."],
             ["Regression", "the full set of tests, run automatically after every change."],
             ["Code coverage", "which lines, branches, conditions and toggles the tests reached."],
             ["Functional coverage", "which SPECIFICATION-level situations the tests reached. "
                                     "Written by you."],
             ["Coverage hole", "a bin nothing ever hit — a gap in testing, not a failure."],
             ["Assertion", "a rule stated in the design's own language and checked on every "
                           "clock edge."],
             ["Cover property", "the same syntax used to RECORD that a situation occurred, "
                                "rather than to require it."],
             ["VCD / FST / WLF", "waveform file formats — plain, compressed, and vendor-native."]],
            [2377440, 8869680], rh=274320, bold_cols=(0,), size=9, col_colors={0: NAVY})

    # ============================================================ recap
    s = d.slide("TOPIC 5 · RECAP", "The Ten Things That Matter")
    y = d.bullets(s, TOP, [
        [R("A testbench is finished when it would FAIL if the design were wrong — not when it "
           "passes.", s=11)],
        [R("Every testbench has six parts, and the one people omit is the verdict and the "
           "watchdog.", s=11)],
        [R("Drive stimulus just AFTER the clock edge; sample just before the next one. Never on "
           "the edge.", s=11)],
        [R("Expected values come from an independent model of the SPECIFICATION, never from the "
           "RTL.", s=11)],
        [R("A model must sample the state ONCE, before applying any operation — exactly as the "
           "hardware does.", s=11)],
        [R("Constrained-random finds the corner nobody writes a directed test for. Seed it, and "
           "print the seed.", s=11)],
        [R("Coverage is what turns \"it passed\" into \"here is what was tested\". Merge it "
           "across the regression.", s=11)],
        [R("Assertions catch a broken rule at the cycle it breaks; scoreboards catch what no "
           "assertion describes.", s=11)],
        [R("Debug by procedure: first wrong cycle, then walk backwards. Never start at the "
           "output.", s=11)],
        [R("Lint, then simulate, then measure. Run the regression on every commit, or it will "
           "stop working.", s=11)],
    ], accent=TEAL, step=329184)
    d.card(s, y + G, "Where this leads",
           [[R("Topic 6 takes these verified designs into timing — constraints, setup and hold "
               "analysis, and closure. The verification skills here do not stop being needed: "
               "every timing fix is a design change, and every design change has to be "
               "re-verified. That is what the regression is for.")]],
           accent=TEAL, h=822960)

    # ============================================================ close
    d.section_slide("TOPIC 5 · COMPLETE", "RTL Simulation and Verification",
                    "Deck · workbook · one DUT · five planted bugs · six testbenches · "
                    "three toolchains.",
                    ["Slides: this deck, for delivery",
                     "Workbook: Module2_Topic5_Tutorial_Practice_Workbook.docx — tutorials, "
                     "exercises and full solutions",
                     "Lab: Topic5_Lab/ — rtl/, tb/, sva/, scripts/, all verified end to end",
                     "Next: Module 2 Topic 6 — timing constraints and analysis"],
                    accent=NAVY)
