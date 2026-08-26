# -*- coding: utf-8 -*-
"""Topic 5 workbook — Part 3: simulation and debugging; Part 4: tools and tutorials."""
import _boot
from wbkit import *
from t5_wb1 import B, N, I, M


def build(w):
    w.page_break()
    w.h1("Part 3 · Simulation and Debugging")
    w.para("You cannot debug a tool you do not understand. Part 3 explains what a simulator "
           "actually does, what a waveform file really is, and how to find a bug by procedure "
           "rather than by staring.")

    # ---------------------------------------------------------- 3.1
    w.h2("3.1  The event-driven engine")
    w.image("sim_engine", 6.4, "Events ordered by time, not instructions in sequence.")
    w.para("A digital simulator does not step through your code. It maintains a queue of "
           "scheduled EVENTS ordered by simulation time. At each time it wakes only the blocks "
           "sensitive to what changed, runs them to completion, and then advances to the next "
           "scheduled time.")
    w.bullets([
        "Nothing is evaluated unless one of its inputs changed, which is why a design that is "
        "mostly idle costs almost nothing to simulate — and why a clock that never stops is "
        "expensive.",
        "Simulation time is not wall-clock time. A million cycles may take a second or an hour, "
        "depending entirely on how much of the design is switching.",
        "Time advances only when there is nothing left to do at the current time. That is why a "
        "loop with no delay hangs: the simulator is not stuck, it is doing exactly what you "
        "wrote.",
    ])
    w.code([
        "while (!done) ;              // NEVER lets time advance, so done can never change",
        "while (!done) @(posedge clk);// correct: yields, so the rest of the design can run",
    ], caption="The commonest way to hang a simulation")

    # ---------------------------------------------------------- 3.2
    w.h2("3.2  Inside one time step")
    w.image("event_regions", 6.4, "The stratified event queue.")
    w.table(["Region", "What happens there"],
            [["Active", "blocking assignments (=); every non-blocking right-hand side is "
                        "EVALUATED; continuous assignments; $display"],
             ["Inactive", "anything scheduled with #0 — avoid using this"],
             ["NBA", "non-blocking assignments are APPLIED to their left-hand sides"],
             ["Monitor", "$monitor and $strobe — after everything has settled"]],
            widths=[1.2, 5.2], size=9.5, align_center=False)
    w.para("Every clocked block samples its inputs in ACTIVE, using values from before the edge; "
           "every register updates later, in NBA. So no clocked block can see another block's "
           "new value on the same edge — exactly like real flip-flops, and the reason "
           "non-blocking assignment models them correctly.")
    w.callout("The practical consequence you will meet first",
              [[M("$display"), N(" runs in ACTIVE, so at a clock edge it prints the value from "
                                 "BEFORE the edge. "), M("$strobe"),
                N(" runs in MONITOR, after every non-blocking update has landed, so it prints "
                  "the settled value. If a printout disagrees with the waveform by exactly one "
                  "cycle, this is why — and the fix is usually to use $strobe, not to change the "
                  "design.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 3.3
    w.h2("3.3  Analyse, elaborate, run")
    w.image("compile_elab_run", 6.4, "The same three steps in every tool.")
    w.table(["Step", "Errors that appear here", "What it means you did"],
            [["Analyse", "syntax errors, undeclared names, bad literals",
              "a typing mistake — file and line are given"],
             ["Elaborate", "missing modules, port mismatches, parameter problems, "
                           "multiple drivers", "a wiring or hierarchy mistake"],
             ["Run", "wrong values, x propagation, timeouts", "a logic mistake — yours or the "
                                                              "testbench's"]],
            widths=[1.1, 2.9, 2.4], size=9.5, align_center=False)
    w.para("Knowing which step failed tells you which kind of mistake you made, which is often "
           "half the diagnosis.")

    # ---------------------------------------------------------- 3.4
    w.h2("3.4  Waveforms")
    w.image("vcd_flow", 6.4, "Your testbench asks for a change-log; a separate program draws it.")
    w.table(["Format", "Written by", "Note"],
            [["VCD", "any simulator, via $dumpvars", "plain text, universal, and very large"],
             ["FST", "Icarus (-fst), GTKWave", "compressed VCD — much smaller and faster"],
             ["WLF", "ModelSim / Questa", "native, fast, read by their own viewer"],
             ["FSDB", "commercial (Verdi)", "the industry standard on large projects"]],
            widths=[1.1, 2.3, 3.0], size=9.5, align_center=False)
    w.code([
        "$dumpfile(\"v3.vcd\");",
        "$dumpvars(0, tb);            // level 0 = EVERYTHING below tb. Start here.",
        "$dumpvars(1, tb.u_dut);      // one level of one instance, when the file gets too big",
    ], caption="Controlling what is dumped")
    w.callout("Dumping is usually the most expensive thing your simulation does",
              ["A regression dumps nothing and re-runs only the failing seed with dumping "
               "switched on. That one habit often takes a nightly regression down to minutes."],
              color=AMBER, fill="FFF7EC", bar="C77514")
    w.h3("Reading a viewer properly")
    w.image("gtkwave_tour", 6.4, "The same picture, every time, from a saved view.")
    w.numbered([
        "GROUP AND ORDER the signals: stimulus at the top, DUT outputs next, internals last. A "
        "jumbled list hides the answer in plain sight.",
        "SET THE RADIX. A counter in binary is unreadable; in hex the pattern is obvious. "
        "Right-click the signal to change it.",
        "USE THE MARKER. Put it on the FIRST wrong cycle named in the transcript, then walk "
        "backwards signal by signal.",
        "SAVE THE VIEW. File → Write Save File writes a .gtkw recording which signals are shown, "
        "in what order, at what radix, with which dividers. Commit it next to the testbench.",
    ])
    w.code([
        "gtkwave v3.vcd wave/v3_fifo.gtkw",
    ], caption="Everyone then sees the same picture")

    # ---------------------------------------------------------- 3.5
    w.h2("3.5  A debugging procedure")
    w.image("debug_method", 6.4, "Two searches, and a ladder run in cost order.")
    w.h3("Bisect in time")
    w.para("Find the FIRST cycle where reality and the model disagree — never the cycle where "
           "you noticed. A wrong output is usually many cycles downstream of its cause, and "
           "every minute spent looking at the output is a minute not spent looking at the cause. "
           "This is why the testbenches in this lab compare every cycle and report the cycle "
           "number of the first failure.")
    w.h3("Bisect in space")
    w.para("Walk backwards from the wrong signal to whatever drives it, and repeat, until you "
           "reach the first signal that was wrong on its own account.")
    w.h3("The ladder")
    w.numbered([
        "Read the error message. It names the file and the line.",
        "Run the linter. One second, and it may name the problem outright.",
        "Read your own diff. What changed since it last worked?",
        "Add $display at the point of failure, printing the INPUTS as well as the output.",
        "Open the waveform at the first failing cycle — not at the end.",
        "Walk backwards to the first signal that was wrong.",
        "Synthesise. A latch or a surprising flip-flop count explains a whole class of symptoms "
        "that look like logic bugs.",
        "Reduce. Cut the test down to the smallest case that still fails; that case is usually "
        "the explanation.",
    ])

    # ---------------------------------------------------------- 3.6
    w.h2("3.6  Chasing an x")
    w.image("x_chase", 6.2, "The signal where you noticed it is almost never the cause.")
    w.para("An x is the simulator saying \"I cannot determine this\". It spreads through every "
           "expression it touches, so by the time you see it on an output it may have travelled "
           "through ten signals.")
    w.table(["Cause", "Typical origin"],
            [["A register that was never reset", "a missing reset branch, or no reset at all"],
             ["A wire nothing drives", "a typo in a port connection — the classic"],
             ["A wire TWO things drive", "a signal assigned in two always blocks"],
             ["Reading past the end of a vector or array", "an index that is one too large"],
             ["Arithmetic on a value that was already x", "x is contagious"]],
            widths=[2.6, 3.8], size=9.5, align_center=False)
    w.callout("Two habits that between them remove most x hunts",
              [[M("`default_nettype none"), N(" at the top of every file turns a misspelt port "
                  "connection from a silent undriven wire into a compile error naming the "
                  "line.")],
               [N("In the testbench, always compare with "), M("==="), N(" and "), M("!=="),
                N(". With "), M("!="), N(" an x compares as x, which is not true, so the check "
                  "silently passes and the bug escapes.")]],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 3.7
    w.h2("3.7  Symptom to cause")
    w.image("failure_signatures", 6.4, "Worth printing and putting on the wall of the lab.")

    # ---------------------------------------------------------- 3.8
    w.h2("3.8  Simulation performance")
    w.para("A regression that takes all night is run once a week; a regression that takes five "
           "minutes is run on every commit. Simulation speed is therefore a verification-quality "
           "issue, not a convenience.")
    w.table(["What costs time", "Why", "What to do"],
            [["Waveform dumping", "every signal change becomes a line of text",
              "dump nothing in a regression; re-run the failing seed with dumping on"],
             ["Dumping the whole hierarchy", "$dumpvars(0, tb) includes every instance",
              "$dumpvars(1, tb.u_dut) once you know where to look"],
             ["A clock that never stops", "every edge wakes every clocked block",
              "stop the clock when idle, if the design allows it"],
             ["Very fine timescale", "1 ps precision means more scheduling work",
              "1ns/1ps is plenty for RTL; you are not doing SPICE"],
             ["$display in a hot loop", "formatting and I/O are slow",
              "print on events, not on cycles"],
             ["One very long random run", "it does not parallelise, and one seed is one sample",
              "many shorter runs at different seeds"]],
            widths=[1.9, 2.3, 2.2], size=9, align_center=False)
    w.para("Verilator compiles the design to C++ and is often 10–100× faster than an interpreted "
           "simulator, which is why it is used for long random regressions even on projects "
           "whose sign-off simulator is a vendor tool.")

    # ============================================================ PART 4
    w.page_break()
    w.h1("Part 4 · Tools and Guided Tutorials")
    w.image("tool_matrix", 6.4, "The verification jobs, and the tool that does each one.")
    w.callout("Honesty note",
              [[N("Every result quoted in this workbook was produced by the open-source column "
                  "— Icarus Verilog 12.0 and Verilator 5.020 — on the code in Topic5_Lab. The "),
                B("Vivado and ModelSim scripts in the lab are working templates that were NOT "
                  "executed"),
                N(", because neither tool is installed in the environment this material was "
                  "written in. The commands are standard and version-stable; check them against "
                  "your installed release before the session.")]],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 4.1
    w.h2("4.1  Installing the open-source flow")
    w.image("install_map", 6.4, "Four tools, one command.")
    w.code([
        "# ---- Ubuntu / Debian / WSL2 ------------------------------------------------",
        "sudo apt update",
        "sudo apt install -y iverilog gtkwave verilator yosys graphviz",
        "",
        "# ---- macOS (Homebrew) ------------------------------------------------------",
        "brew install icarus-verilog verilator gtkwave yosys graphviz",
        "",
        "# ---- Windows ---------------------------------------------------------------",
        "#  Best:  wsl --install  in an administrator PowerShell, then the Ubuntu line.",
        "#  Or:    download the OSS CAD Suite, unzip it, run start.bat.",
        "",
        "# ---- verify ----------------------------------------------------------------",
        "iverilog -V | head -1        # Icarus Verilog version 12.0",
        "verilator --version          # Verilator 5.020",
        "gtkwave --version",
    ], caption="Copy-paste installation")
    w.para("GTKWave is a GUI. On Windows 11, WSLg runs Linux GUIs with no extra setup. On "
           "Windows 10 you need an X server such as VcXsrv plus export DISPLAY=:0, or you can "
           "install the native Windows GTKWave and open the .vcd the WSL side wrote — the file "
           "system is shared.")

    # ---------------------------------------------------------- 4.2
    w.h2("4.2  Vivado xsim")
    w.code([
        "xvlog -d DUT=fifo_b1 -d DUTNAME=\\\"fifo_b1\\\" \\",
        "      rtl/fifo.v rtl/fifo_bugs.v tb/tb_v3_random.v      # analyse",
        "xelab -debug typical tb_v3_random -s tb_v3_random_sim    # elaborate",
        "xsim tb_v3_random_sim -runall -testplusarg SEED=1        # run",
        "",
        "# or with the provided script:",
        "vivado -mode batch -source scripts/vivado_sim.tcl -tclargs V3 fifo_b1",
    ], caption="Topic5_Lab/scripts/vivado_sim.tcl")
    w.bullets([
        [M("-d NAME=value"), N(" passes a `define, exactly like "), M("-D"),
         N(" does to iverilog.")],
        [M("-testplusarg SEED=1"), N(" passes a plusarg, so the same seed gives the same run as "
                                     "under Icarus.")],
        [M("-debug typical"), N(" keeps signal visibility for the wave window.")],
        [B("xsim supports the FULL SystemVerilog assertion language"),
         N(", including the ranged delay forms (a |-> ##[1:3] b) that the open-source flow "
           "cannot handle.")],
    ])

    # ---------------------------------------------------------- 4.3
    w.h2("4.3  ModelSim / Questa")
    w.code([
        "vlib work",
        "vmap work work",
        "vlog -sv +define+DUT=fifo_b3 rtl/*.v sva/fifo_sva.sv tb/tb_v6_assert.sv",
        "vsim -voptargs=+acc -assertdebug +SEED=7 work.tb_v6_assert",
        "assertion fail -action break -r /*        # stop on the first assertion failure",
        "run -all",
        "",
        "# or with the provided script:",
        "vsim -c -gLAB=V6 -gDUT=fifo_b3 -do scripts/modelsim_run.do",
    ], caption="Topic5_Lab/scripts/modelsim_run.do")
    w.bullets([
        [M("-voptargs=+acc"), N(" keeps signal visibility — without it the optimiser removes the "
                                "very signals you want to look at.")],
        [M("-assertdebug"), N(" reports every assertion pass and failure, not only failures.")],
        [N("Compile with "), M("vlog -cover bcesx"), N(" to enable code coverage, then "),
         M("coverage report -details -file build/coverage.txt"), N(".")],
        [N("Merge coverage across a regression with "), M("vcover merge"), N(".")],
    ])

    # ============================================================ TUTORIALS
    w.page_break()
    w.h1("Guided Tutorials V-T1 – V-T7")
    w.para("Seven tutorials, at the keyboard, in order. Each ends with something you can see. "
           "About five hours in total, and they are the bridge between reading Parts 1–3 and "
           "attempting the exercises.")

    w.h2("V-T1 · Run the clinic before you understand it  (20 min)")
    w.para("Goal: see the result that the rest of the topic explains.")
    w.numbered([
        "cd Topic5_Lab and run ./scripts/lint.sh . It reports LINT CLEAN — including all five "
        "broken designs. Read the note it prints.",
        "Run ./scripts/run_all.sh . Every lab passes on the golden FIFO.",
        "Run ./scripts/clinic.sh . Read the matrix carefully. Write down, before reading any "
        "further, why you think V1 catches nothing.",
        "Open rtl/fifo.v and read only the header comment. List every rule it states — there are "
        "eight. That list is the verification plan.",
        "Now open tb/tb_v1_naive.v and mark which of the eight rules it actually tests. The "
        "answer is one and a half.",
    ])

    w.h2("V-T2 · Build V1 yourself  (35 min)")
    w.para("Goal: write a complete testbench from nothing, and meet all six parts.")
    w.numbered([
        "Start a new file tb/my_v1.v. Do not copy tb_v1_naive.v — write it.",
        "Declare the signals, instantiate the FIFO, and generate a 100 MHz clock.",
        "Write the reset sequence. Release reset BETWEEN clock edges, not on one.",
        "Write push() and pop() tasks that drive at #1 after the edge.",
        "Write a check() task that increments an error counter and prints the time, the value "
        "and the expectation.",
        "Add $dumpfile and $dumpvars, a PASS/FAIL verdict, $finish, and a watchdog.",
        "Compile and run it against the golden FIFO. Then run it against fifo_b1 through "
        "fifo_b5. Record which it catches.",
        "Compare your file with tb_v1_naive.v. The differences are worth ten minutes of "
        "discussion.",
    ])

    w.h2("V-T3 · Add a model and the corners  (45 min)")
    w.para("Goal: turn a weak testbench into one that catches four bugs out of five.")
    w.numbered([
        "Copy your V1 into tb/my_v2.v.",
        "Add the reference model: an array, mhead, mtail, and the four functions mcount, mempty, "
        "mfull and mfront.",
        "Write model_cycle(do_w, do_r, d). Sample full and empty ONCE at the top, before "
        "applying either operation. If you skip this you will reproduce the bug described in "
        "section 2.5 — try it deliberately, once, and watch the golden FIFO fail.",
        "Write compare(): check count, empty, full, and (when not empty) rd_data, against the "
        "model.",
        "Replace your ad-hoc stimulus with a cycle(do_w, do_r, d) task that drives, advances the "
        "model, and compares.",
        "Add the eight directed tests T1–T8 from section 2.6.",
        "Run against all six designs. You should now catch four. Which one still escapes, and "
        "why?",
    ])

    w.h2("V-T4 · Constrained-random, seeds and a regression  (40 min)")
    w.para("Goal: catch the fifth bug, and make the result reproducible.")
    w.numbered([
        "Copy your V2 into tb/my_v3.v.",
        "Replace the directed body with a loop that decides do_w and do_r from $random with "
        "configurable weights, read from +WR and +RD plusargs.",
        "Read the seed from +SEED and SAVE IT into seed0 before the loop. Print seed0, not seed, "
        "in the verdict.",
        "Run it against fifo_b5. It should now fail. Note the cycle number of the first error.",
        "Run the same seed again and confirm the failure is identical. Change the seed and "
        "confirm it is different.",
        "Run ./scripts/regress.sh 6 to see a full multi-seed, multi-profile regression.",
        "Deliberately break the seeding — call $random with no argument — and observe that runs "
        "are no longer reproducible. Put it back.",
    ])

    w.h2("V-T5 · Coverage, and closing it  (40 min)")
    w.para("Goal: measure what your test actually reached, and make the number move.")
    w.numbered([
        "Run ./scripts/coverage.sh and read all three profile reports plus the merged one.",
        "Run vvp build/cov.vvp +WR=95 +RD=5 +TAG=extreme . Which bins go MISS, and why?",
        "Copy tb_v4_coverage.v and add a thirteenth bin: \"three consecutive idle cycles\". "
        "Does anything hit it? If not, what stimulus would?",
        "Add a fourteenth bin that is IMPOSSIBLE by construction — for example \"full and empty "
        "at the same time\". Confirm it stays at zero, and write the one-line waiver you would "
        "put in the verification plan.",
        "Take the write-heavy profile and add directed stimulus at the end of the run that "
        "closes its three holes. Confirm it reaches 12 of 12 on its own.",
    ])

    w.h2("V-T6 · Assertions  (45 min)")
    w.para("Goal: state the specification as properties, and see one fire.")
    w.numbered([
        "Read sva/fifo_sva.sv. For each property, say in one sentence which line of the FIFO's "
        "header comment it encodes.",
        "Run ./scripts/assert.sh . Note which assertion caught which bug, and at what time.",
        "Comment out a_step_both and re-run. fifo_b3 drops from \"caught by an assertion\" to "
        "\"caught by the scoreboard only\" — later, and with a much less useful message. Put it "
        "back.",
        "Add a new property: rd_data must never be x while empty is low. Run it against all six "
        "designs.",
        "Now try to write an assertion that would catch fifo_b4. It is harder than the others — "
        "explain why in two sentences. (Hint: what would the property have to remember?)",
        "Add a cover property for \"a write immediately followed by a read\". Confirm from the "
        "run that it was actually hit.",
    ])

    w.h2("V-T7 · The debug clinic  (60 min)")
    w.para("Goal: diagnose a bug you did not plant, from symptoms, using the procedure.")
    w.numbered([
        "Have somebody else pick one of the five broken FIFOs without telling you which.",
        "Run your V3 against it. Note the FIRST failing cycle and the message.",
        "Predict, from the message alone, what kind of bug it is. Write the prediction down "
        "before opening anything.",
        "Re-run with dumping on and open the VCD at that cycle, not at the end.",
        "Add the signals in the right order: stimulus, then outputs, then the DUT's internal "
        "pointers. Walk backwards to the first signal that is wrong.",
        "Name the bug and the line. Then open rtl/fifo_bugs.v and check.",
        "Finally: write a bug of your own that your testbench does NOT catch, hand it to your "
        "neighbour, and see whether theirs does.",
    ])
    w.callout("Step 7 is the point of the whole topic",
              ["Writing a bug that survives a good testbench forces you to think about what the "
               "testbench does not check — which is exactly the skill a verification plan is "
               "supposed to produce."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")
