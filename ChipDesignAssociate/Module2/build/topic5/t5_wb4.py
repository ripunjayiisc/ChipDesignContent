# -*- coding: utf-8 -*-
"""Topic 5 workbook — Part 5 exercises, Part 6 solutions, Part 7 reference."""
import _boot
from wbkit import *
from t5_wb1 import B, N, I, M


def _paras(body):
    if isinstance(body, (str, tuple)):
        body = [body]
    return [[b] if isinstance(b, tuple) else b for b in body]


def ex(w, n, title, body=None, code=None, size=8.8):
    w.h4("Exercise %d · %s" % (n, title))
    if body:
        for b in _paras(body):
            w.para(b)
    if code:
        w.code(code, size=size)


def sol(w, n, body=None, code=None, size=8.8):
    p = w.d.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Solution %d" % n)
    r.font.name = HEADF; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = GREEN
    if body:
        for b in _paras(body):
            w.para(b)
    if code:
        w.code(code, size=size)


def build_exercises(w):
    w.page_break()
    w.h1("Part 5 · Practice Exercises")
    w.para("Sixty exercises in five blocks. Block B is the one that builds the skill this module "
           "assesses — judging a testbench rather than writing more of it. Full worked solutions "
           "are in Part 6.")
    w.table(["Block", "Exercises", "What it trains"],
            [["A", "1–12", "Concepts — what verification is, and what the terms mean"],
             ["B", "13–26", "Judgement — is this testbench any good, and how do you know?"],
             ["C", "27–38", "Diagnosis — symptom to cause, from real failure messages"],
             ["D", "39–52", "Construction — write the testbench, the model, the coverage"],
             ["E", "53–60", "Tools, regression and closure"]],
            widths=[0.7, 1.1, 4.6], size=9.5, align_center=False)

    # ---------------------------------------------------------- A
    w.h2("Block A · Concepts")
    ex(w, 1, "Verification and validation",
       "State the difference in one sentence each, and give an example of a design that would "
       "pass verification and fail validation.")
    ex(w, 2, "Why not exhaustive",
       "A block has two 16-bit inputs and 40 flip-flops. Explain, with numbers, why exhaustive "
       "testing is not an option, and what you do instead.")
    ex(w, 3, "The cost curve",
       "The same bug is found by a linter, by simulation, and after tape-out. Describe what each "
       "costs, and what that implies about the order in which you run checks.")
    ex(w, 4, "Passing versus proving",
       "A testbench passes on a design you know is broken. What exactly has it told you, and "
       "what has it not?")
    ex(w, 5, "Four checkers",
       "Rank these from weakest to strongest and say why: hard-coded expected values; a human "
       "reading a waveform; assertions; a reference model with a scoreboard.")
    ex(w, 6, "Code versus functional coverage",
       "A testbench reports 100% line and branch coverage. Name three things it might still not "
       "have tested.")
    ex(w, 7, "Coverage holes",
       "Is a coverage hole a bug? What are the three legitimate things you can do about one?")
    ex(w, 8, "Directed and random",
       "For each, say which technique you would reach for FIRST and why: (a) checking reset "
       "empties a FIFO; (b) finding a bug in the interaction of three control signals; (c) "
       "regressing a bug that was fixed last week; (d) closing a coverage hole you have just "
       "identified.")
    ex(w, 9, "Seeds",
       "Why does a random testbench print its seed on every line, including the passing ones?")
    ex(w, 10, "Assertions and scoreboards",
       "Give one bug an assertion catches earlier than a scoreboard, and one it cannot catch at "
       "all. Explain the difference in one sentence.")
    ex(w, 11, "The verification plan",
       "Why must the plan be written before the testbench, and why must somebody other than its "
       "author review it?")
    ex(w, 12, "Sign-off",
       "Coverage is closed, the regression is green, and the team is still finding two "
       "high-severity bugs a week. Are you finished? What does the situation actually tell you?")

    # ---------------------------------------------------------- B
    w.h2("Block B · Judging a testbench")
    w.para("For each: say what the testbench does and does not prove, and what you would add "
           "first.")
    ex(w, 13, "Three words", code=[
        "push(8'hA1); push(8'hB2); push(8'hC3);",
        "pop(got); check(got, 8'hA1);",
        "pop(got); check(got, 8'hB2);",
        "pop(got); check(got, 8'hC3);",
        "$display(\"PASS\");"])
    ex(w, 14, "No verdict", code=[
        "for (i = 0; i < 1000; i = i + 1) begin",
        "  drive($random);",
        "  $display(\"%0t  in=%h  out=%h\", $time, din, dout);",
        "end"])
    ex(w, 15, "The wrong comparison", code=[
        "if (dout != expected) begin errors = errors + 1; end"])
    ex(w, 16, "The model reads the DUT", code=[
        "expected = tb.u_dut.mem[tb.u_dut.rd_ptr[2:0]];",
        "if (rd_data !== expected) errors = errors + 1;"])
    ex(w, 17, "No timeout", code=[
        "initial begin",
        "  reset();",
        "  wait (done);",
        "  $display(\"PASS\");",
        "  $finish;",
        "end"])
    ex(w, 18, "Random without weights", code=[
        "do_w = $random;      // any non-zero 32-bit value is 'true'",
        "do_r = $random;"],
       body="What fraction of cycles asserts each enable, and why is that a problem?")
    ex(w, 19, "Coverage that proves nothing", code=[
        "if (wr_en) cov_write = cov_write + 1;",
        "if (rd_en) cov_read  = cov_read  + 1;",
        "// report: both bins HIT, 100% coverage"],
       body="Two bins, both hit, 100% reported. What is wrong with this coverage model?")
    ex(w, 20, "The assertion that never fires", code=[
        "a_check: assert property (@(posedge clk) disable iff (!rst_n)",
        "    (wr_en && full && rd_en && empty) |=> (count == 0));"],
       body="This assertion has never failed in ten thousand runs. Should you be pleased?")
    ex(w, 21, "The over-eager checker",
       "A colleague's testbench fires an error on the golden design about once every thousand "
       "seeds. They say it is 'probably a race in the checker' and filter the message out of "
       "the log. What is wrong with this, in two respects?")
    ex(w, 22, "One long run",
       "A team runs one random test for twelve hours every night, at a fixed seed. Give three "
       "separate criticisms.")
    ex(w, 23, "Model written from the RTL",
       "A verification engineer writes the reference model by reading the design's source, "
       "because the specification is 'out of date'. What has been lost, and what should happen "
       "instead?")
    ex(w, 24, "The white-box scoreboard",
       "A scoreboard checks the DUT's internal pointer values as well as its outputs. Name one "
       "benefit and two costs.")
    ex(w, 25, "The clinic result",
       "V2 catches 4 of 5 and V3 catches 5 of 5. A student concludes that directed testing is "
       "obsolete. Give two reasons they are wrong.")
    ex(w, 26, "What would you add first?",
       "You inherit a testbench with a reference model, 3000 random cycles, and no coverage, no "
       "assertions and no regression. You have one day. What do you add, in what order, and why?")

    # ---------------------------------------------------------- C
    w.h2("Block C · Diagnosis")
    w.para("Each of these is a real failure message or symptom. Name the most likely cause and "
           "the first thing you would look at.")
    ex(w, 27, "x from time zero", code=[
        "FAIL 0 : rd_data is not the oldest word   got xx expected a1",
        "FAIL 10 : count disagrees with the model  got x  expected 1"])
    ex(w, 28, "Off by one cycle", code=[
        "FAIL 155 : rd_data is not the oldest word  got b2 expected a1",
        "FAIL 165 : rd_data is not the oldest word  got c3 expected b2",
        "  ... and every subsequent cycle is also wrong by exactly one word"])
    ex(w, 29, "Passes on the golden design, fails on one bug only at high WR",
       "Your testbench catches fifo_b1 when +WR=90 but not when +WR=50. What does that tell you "
       "about the bug, and about the testbench?")
    ex(w, 30, "The check that never fires", code=[
        "if (rd_data != model_front()) errors = errors + 1;",
        "// rd_data is x for the whole run; errors stays at 0"])
    ex(w, 31, "Half-width pulse",
       "A one-cycle pulse from the DUT appears half a clock wide in the waveform, and a check on "
       "it fails intermittently. Design bug or testbench bug? How do you tell?")
    ex(w, 32, "Random test drove nine transactions", code=[
        "  scoreboard: 2022 checks, 9 words in, 9 words out",
        "PASS - V6 layered+assertions : seed=7 cycles=2000"],
       body="2000 cycles were requested and it passed. Why is this output alarming?")
    ex(w, 33, "The golden design fails",
       "Your V2 testbench reports FAIL on the correct FIFO, at the first cycle where a read and "
       "a write are asserted together on an empty FIFO. The broken fifo_b5 passes. What is "
       "wrong, and where?")
    ex(w, 34, "The simulation never ends",
       "A test hangs with no output after the reset message. Give three possible causes and how "
       "to distinguish them.")
    ex(w, 35, "Assertion fires during reset", code=[
        "%Error: fifo_sva.sv:48: Assertion failed in a_full_iff_depth: full=x but count=x",
        "       Time: 0"],
       body="What is missing from the property?")
    ex(w, 36, "Coverage says 100%, a bug escaped",
       "A bug in the full→empty→full transition escaped a testbench reporting 100% functional "
       "coverage across 11 bins. What went wrong, and what is the fix?")
    ex(w, 37, "Works in simulation, fails on the board",
       "A design with a signal crossing from a 100 MHz to a 27 MHz clock passes every simulation "
       "and fails intermittently on hardware. Explain, and say what would have caught it.")
    ex(w, 38, "The regression is green but slow",
       "A nightly regression takes nine hours; profiling shows 80% of the time in file I/O. What "
       "is almost certainly happening, and what is the one-line fix?")

    # ---------------------------------------------------------- D
    w.h2("Block D · Construction")
    w.para("Write real code. Each of these should compile and run against Topic5_Lab/rtl/fifo.v "
           "or the DUT named.")
    ex(w, 39, "A minimal self-checking testbench",
       "Write a complete testbench for rtl/fifo.v with all six parts, including a watchdog. It "
       "must print PASS or FAIL and terminate.")
    ex(w, 40, "The reference model",
       "Write the FIFO reference model as an array with head and tail indices, plus mcount, "
       "mempty, mfull and mfront. Then write model_cycle(do_w, do_r, d) correctly — sampling "
       "before applying.")
    ex(w, 41, "The eight corners",
       "Add the eight directed tests T1–T8 from section 2.6. Confirm your testbench now catches "
       "four of the five broken designs.")
    ex(w, 42, "Weighted random",
       "Replace the directed body with weighted random stimulus taking +SEED, +CYCLES, +WR and "
       "+RD from plusargs, and printing the ORIGINAL seed in the verdict.")
    ex(w, 43, "A coverage model",
       "Implement the twelve bins of section 2.9, including bin 11 (the full→empty→full "
       "sequence). Print a HIT/MISS table and a closure verdict.")
    ex(w, 44, "A thirteenth bin",
       "Add a bin for 'a write immediately followed on the next cycle by a read'. Which stimulus "
       "profile hits it most often?")
    ex(w, 45, "Assertions",
       "Write three concurrent assertions for the FIFO that are NOT already in sva/fifo_sva.sv, "
       "and say which line of the specification each encodes.")
    ex(w, 46, "A layered driver",
       "Refactor your testbench into generator / driver / monitor / scoreboard, with the "
       "monitor never driving and the scoreboard never touching a pin.")
    ex(w, 47, "A second DUT",
       "Write a testbench for rtl/fifo.v that also works, unchanged, on a FIFO with a different "
       "DEPTH and W. What did you have to parameterise?")
    ex(w, 48, "Plant a bug",
       "Make a copy of rtl/fifo.v with exactly one realistic bug that your V3 testbench does NOT "
       "catch. Then extend the testbench until it does.")
    ex(w, 49, "A shift-register testbench",
       "Write a self-checking testbench for an 8-bit shift register with enable and synchronous "
       "clear, using a reference model. What is the model, in this case?")
    ex(w, 50, "An FSM testbench",
       "Write a testbench for a traffic-light FSM that checks: every state is entered; no "
       "illegal light combination ever occurs; and the machine recovers from a forced illegal "
       "state. Which of the three needs a white-box hook, and how do you keep it out of the "
       "scoreboard?")
    ex(w, 51, "A protocol checker",
       "Write a standalone checker module for a simple req/ack handshake: req must stay high "
       "until ack; ack must not be asserted without req; and req must fall the cycle after ack. "
       "Bind it to a DUT without editing the DUT.")
    ex(w, 52, "A golden-vector testbench",
       "Write a testbench that reads stimulus and expected results from two hex files, applies "
       "each vector, and writes a mismatch log. Then say what this testbench cannot find.")

    # ---------------------------------------------------------- E
    w.h2("Block E · Tools, regression and closure")
    ex(w, 53, "Reproduce the clinic",
       "Run ./scripts/clinic.sh and reproduce the matrix. Then modify tb_v1_naive.v with the "
       "SMALLEST change that makes it catch at least one bug. What did you change, and why does "
       "it work?")
    ex(w, 54, "A regression of your own",
       "Write a shell script that runs your testbench over 10 seeds and 3 profiles, prints a "
       "table, and exits non-zero if anything fails. It must print the reproduction command for "
       "every failure.")
    ex(w, 55, "Coverage merge",
       "Run the three profiles of ./scripts/coverage.sh separately and merge them by hand from "
       "the build/cov_*.txt files. Confirm you get the same merged total as the script.")
    ex(w, 56, "Assertion triage",
       "Run ./scripts/assert.sh . For each of the five designs, state which assertion fired (or "
       "that none did) and, in one sentence, why that particular property was the one to catch "
       "it.")
    ex(w, 57, "Waveform discipline",
       "Build a GTKWave save file for your own testbench with signals grouped and radixes set. "
       "Commit it. Then hand your VCD and .gtkw to somebody else and time how long it takes them "
       "to find the first failing cycle.")
    ex(w, 58, "Make it fast",
       "Time your regression. Then remove waveform dumping from the regression path and re-time "
       "it. Report both numbers and the ratio.")
    ex(w, 59, "The vendor flow",
       "Run one of the labs under Vivado xsim or ModelSim using the supplied script. Report any "
       "command that needed changing for your installed version — the scripts are templates and "
       "were not executed when this material was written.")
    ex(w, 60, "Write the verification plan",
       "For rtl/fifo.v, write the complete verification plan as a table: one row per rule in the "
       "header comment, with columns for how it is checked, what stimulus reaches it, which "
       "coverage bin proves it, and status. Then compare it with what your testbench actually "
       "does, and list the gaps.")


def build_solutions(w):
    w.page_break()
    w.h1("Part 6 · Worked Solutions")

    w.h2("Block A")
    sol(w, 1, [N("Verification asks whether the design does what the specification says. "
                 "Validation asks whether the specification was the right one."),
               N("Example: a UART verified perfectly against a specification that says 7 data "
                 "bits, when the system it plugs into sends 8. Every test passes; the product "
                 "does not work.")])
    sol(w, 2, "Two 16-bit inputs give 2^32 = 4.3 billion combinations for the combinational part "
              "alone — feasible only if the block is purely combinational and fast to simulate. "
              "Add 40 flip-flops and the reachable state space is up to 2^40 ≈ 10^12 states, "
              "each of which must be visited in every relevant input combination: 10^12 × 4×10^9 "
              "≈ 4×10^21 cases. At a billion per second that is over 100 000 years. Instead: "
              "directed tests at the boundaries, constrained-random for the interior, assertions "
              "for the rules, and coverage to measure what was reached.")
    sol(w, 3, "Lint: one second, with a file and line. Simulation: a minute, plus reading a "
              "waveform. After tape-out: a mask respin — months and a large amount of money, "
              "with parts already at customers. Implication: run the checks in cost order, and "
              "never skip a cheap one because you are in a hurry. A bug a linter would have "
              "named should never reach a waveform viewer.")
    sol(w, 4, "It has told you that the testbench does not distinguish this design from a "
              "correct one. It has told you nothing whatever about the design. In Topic5_Lab, "
              "V1 passes on all five broken FIFOs — which measures V1, not the FIFOs.")
    sol(w, 5, [N("Weakest to strongest: a human reading a waveform (cannot run unattended, so it "
                 "is not a check at all); hard-coded expected values (scales to about twenty "
                 "cases, and the values acquire their own bugs); a reference model with a "
                 "scoreboard (checks every cycle, scales to millions); assertions (check every "
                 "cycle of EVERY test, for ever, and report at the cycle the rule broke)."),
               N("The ordering is about scale and about when the failure is reported, not about "
                 "how clever each one is.")])
    sol(w, 6, "(1) Behaviour there is no code for — a missing else, an unhandled case, a feature "
              "not implemented. (2) Whether any output was actually CHECKED: a testbench that "
              "runs every line and compares nothing reports 100%. (3) Situations, as opposed to "
              "lines: the FIFO may never have been full while a write was attempted, even though "
              "every line of the full logic executed.")
    sol(w, 7, "No — a hole means the situation never occurred during testing, which is a gap in "
              "evidence rather than a defect. Three legitimate responses: write stimulus that "
              "reaches it; waive it in writing with a reason (typically that it is impossible by "
              "construction); or change the coverage model because the bin was wrong. What you "
              "may not do is leave it unexplained.")
    sol(w, 8, None, code=[
        "(a) reset empties a FIFO        DIRECTED  - one named case, cheap, unambiguous",
        "(b) three interacting signals   RANDOM    - the combinations are what you cannot list",
        "(c) regressing a fixed bug      DIRECTED  - you want that exact case, every time",
        "(d) closing a known hole        DIRECTED  - you know precisely what must happen"])
    sol(w, 9, "Because a failure is useless unless it can be reproduced, and because you cannot "
              "know in advance which line will fail. Printing it only on failure means the "
              "passing runs cannot be re-examined later — and 'it passed last week' is a claim "
              "somebody will eventually want to check.")
    sol(w, 10, [N("Catches earlier: any rule about the control interface — for example "
                  "fifo_b3's count drifting on a simultaneous read and write, which "
                  "a_step_both reports at 545 ns by name, while a scoreboard would report a "
                  "count mismatch some cycles later."),
                N("Cannot catch: fifo_b4, which corrupts DATA while keeping count, full and "
                  "empty perfectly correct. No property in sva/fifo_sva.sv describes the data, "
                  "so nothing fires and the scoreboard is what catches it."),
                B("Assertions catch what you described; scoreboards catch what you compared.")])
    sol(w, 11, "Written first, it tells you what to build and the gaps are visible while they "
               "are cheap. Written afterwards, it documents what you happened to build. It must "
               "be reviewed by somebody else because the author of a plan cannot see what the "
               "plan omits — that is what an omission is.")
    sol(w, 12, "No. A flat bug-discovery rate is one of the sign-off criteria, and yours is not "
               "flat. Coverage being closed while serious bugs keep arriving means the coverage "
               "MODEL is missing a category of behaviour — it is measuring the wrong thing, "
               "accurately. The action is to find out what the escaping bugs have in common and "
               "add bins for it, not to keep running the same regression.")

    w.h2("Block B")
    sol(w, 13, "Proves: three words go in and come out in order, from an empty FIFO. Does not "
               "prove: anything at a boundary — it never fills, never empties past zero, never "
               "reads and writes on the same cycle, never wraps. Add first: fill to full and "
               "drain to empty, with a reference model so every cycle is checked. That single "
               "change takes it from 0 of 5 to 4 of 5 in the lab.")
    sol(w, 14, "It proves nothing at all: there is no verdict. It is a demonstration, not a "
               "test. Add an error counter, a check task, and a PASS/FAIL line. Until then it "
               "cannot be put in a regression, which means in practice it will be run once and "
               "never again.")
    sol(w, 15, [N("It uses "), M("!="), N(" instead of "), M("!=="),
                 N(". If dout is x, the comparison evaluates to x, which is not true, so the "
                   "check silently passes. A design that outputs x for the whole run reports "
                   "zero errors."),
                N("Fix: use === and !== in every testbench comparison.")])
    sol(w, 16, "The 'model' is reading the DUT's own memory and pointer, so it agrees with the "
               "DUT by construction and can never disagree with it. It will not detect any "
               "addressing bug, because it uses the same address. Fix: an independent model, "
               "written from the specification, that never looks inside the DUT.")
    sol(w, 17, "No timeout. If done never asserts, the test hangs for ever, and in a regression "
               "it hangs everything behind it. Add a watchdog: a second initial block that "
               "prints FAIL and calls $finish after a generous delay. A hung DUT must FAIL, not "
               "stall.")
    sol(w, 18, [N("$random returns a 32-bit value, and any non-zero value is 'true', so each "
                  "enable is asserted about 4 294 967 295 times out of 4 294 967 296 — that is, "
                  "essentially always. Both enables are high on essentially every cycle, so the "
                  "FIFO does read+write for ever and never fills or empties."),
                N("Fix: reduce to a range and compare, as in the lab: "),
                M("({$random(seed)} % 100) < p_wr")])
    sol(w, 19, "The bins record that a write happened and a read happened. They say nothing "
               "about the OCCUPANCY at the time, which is where the bugs are: read+write while "
               "empty, write while full, the wrap. Two hit bins reporting '100%' is worse than "
               "no coverage, because it is believed. Fix: bins for situations (state × "
               "operation), which is exactly what a covergroup CROSS expresses.")
    sol(w, 20, [N("No. Read the antecedent: "), M("wr_en && full && rd_en && empty"),
                 N(" requires full and empty to be true at the same time, which never happens. "
                   "The property is VACUOUSLY true — it has never actually been evaluated, so it "
                   "has proved nothing."),
                N("This is why assertion coverage exists: every assertion must be shown to have "
                  "been hit at least once. An assertion that never fires may be protecting you, "
                  "or may be dead code.")])
    sol(w, 21, [N("First: an intermittent failure on the golden design is either a real design "
                  "bug that only shows in rare orderings, or a real testbench bug. Both matter, "
                  "and 'probably a race' is a hypothesis, not a diagnosis — the seed makes it "
                  "reproducible, so it can be investigated properly."),
                N("Second, and worse: filtering the message trains the team to ignore that "
                  "checker. From then on it is not a checker. A checker that fires on correct "
                  "hardware must be fixed or removed, never muted.")])
    sol(w, 22, "(1) A fixed seed means twelve hours of the SAME stimulus every night — one "
               "sample, repeated, not twelve hours of coverage. (2) One long run does not "
               "parallelise; twelve one-hour runs at different seeds cover far more and finish "
               "sooner. (3) A twelve-hour turnaround means a bug introduced in the morning is "
               "found the following day at the earliest, and nobody will run it before "
               "committing.")
    sol(w, 23, "The independence has been lost: a model derived from the design agrees with the "
               "design's bugs, so the scoreboard can only detect the testbench's own mistakes. "
               "What should happen: fix the specification. If the spec is out of date, that is a "
               "project problem to be escalated, not a problem to be worked around by the "
               "verification engineer — and writing the model is often exactly the exercise that "
               "exposes what the spec fails to say.")
    sol(w, 24, "Benefit: when a check fails you can see immediately which internal signal is "
               "wrong, which shortens debugging. Costs: (1) the testbench now depends on the "
               "design's internal structure, so any refactor breaks it and nobody can tell "
               "whether the design broke too; (2) it can mask bugs, because a model that reads "
               "the DUT's own state agrees with it by construction. Use white-box hooks for "
               "debugging and coverage, never for the primary scoreboard comparison.")
    sol(w, 25, "(1) The four bugs V2 caught were caught by DIRECTED boundary tests, and it "
               "caught them immediately and deterministically — the random test found the same "
               "four less directly. (2) A random test cannot be relied on to reach a specific "
               "named case; once you know a case matters, you write it directly so it is hit on "
               "every run, at every seed, for ever. Directed and random are instruments for "
               "different jobs.")
    sol(w, 26, [N("In this order:"),
                N("1. ASSERTIONS on the control interface — a few hours, they check every cycle "
                  "of every existing test, and they report at the cycle the rule breaks."),
                N("2. COVERAGE — otherwise you have no idea whether the 3000 cycles reach "
                  "anything interesting, and you cannot tell your manager anything true."),
                N("3. A REGRESSION over several seeds and profiles — cheap to script, and it "
                  "turns one sample into evidence."),
                N("Assertions first because they are the highest value per hour and they improve "
                  "every test that already exists.")])

    w.h2("Block C")
    sol(w, 27, "x from time zero means the DUT was never reset, or the reset is not reaching it. "
               "Look first at the reset path: polarity (rst_n is active LOW), whether the "
               "testbench asserts it before the first edge, and whether the port is connected — "
               "a misspelt port name creates a silent undriven wire unless `default_nettype none "
               "is in force.")
    sol(w, 28, "Every word is late by exactly one, and consistently. That is not a data bug; it "
               "is an alignment bug — either the model popped one word too early, or the "
               "testbench sampled rd_data after advancing the model instead of before. Look at "
               "the testbench first: consistent, uniform off-by-one is almost always the checker "
               "and almost never the design.")
    sol(w, 29, "The bug only manifests near FULL, so it needs the write-heavy profile to be "
               "reached at all. That tells you two things: the bug is at the full boundary "
               "(fifo_b1's full flag is one entry late), and your testbench has a COVERAGE hole "
               "at +WR=50 — it is not reaching full often enough. Add a directed fill-to-full "
               "test so the case is hit at every profile and every seed.")
    sol(w, 30, [N("Same fault as exercise 15: "), M("!="), N(" instead of "), M("!=="),
                 N(". rd_data is x, so (x != anything) is x, which is not true, so errors never "
                   "increments and the run reports PASS while the design outputs nothing but x."),
                N("The deeper lesson: the FIRST thing a testbench should check is that its "
                  "outputs are not x. Add an $isunknown assertion or an explicit check.")])
    sol(w, 31, "Testbench bug, almost certainly. A DUT clocked on posedge can only change its "
               "outputs at a posedge, so a half-cycle-wide pulse means the STIMULUS changed "
               "mid-cycle. How to tell: look at the input in the waveform — if it changes at a "
               "time that is not just after a posedge, the driver is at fault. This exact bug "
               "occurred in the Topic 4 edge-detector lab.")
    sol(w, 32, [N("2000 cycles were driven but only 9 words moved, which means the random "
                  "decisions were not random — the same do_w/do_r pair was produced every "
                  "cycle."),
                N("Cause: "), M("$urandom(seed)"),
                N(" called inside the loop. In SystemVerilog that RE-SEEDS the generator every "
                  "call, so it returns the same number for ever. Seed once with "),
                M("void'($urandom(seed0));"), N(" then call "), M("$urandom()"),
                N(" with no argument. This happened while writing Lab V6."),
                B("A random test that is silently not random is worse than none, because it is "
                  "believed.")])
    sol(w, 33, [N("The reference model is wrong, not the FIFO. The model applies the write and "
                  "then tests its own updated state to decide whether to pop:"),
                N("on a simultaneous read and write to an empty FIFO it pushes, sees itself no "
                  "longer empty, and pops the word straight back out — reporting 0 where the "
                  "hardware correctly has 1. fifo_b5 really does drop that write, so it agrees "
                  "with the broken model and 'passes'."),
                N("Fix: sample full and empty ONCE, before applying either operation.")],
        code=["was_full  = mfull();",
              "was_empty = mempty();",
              "if (do_w && !was_full)  push(d);",
              "if (do_r && !was_empty) pop();"])
    sol(w, 34, "(1) No $finish and the stimulus has ended — the simulation is idle but alive; "
               "check whether time is still advancing. (2) A wait loop with no delay, so time "
               "cannot advance at all; the process is spinning. (3) The DUT never asserts the "
               "condition being waited on — a real functional bug. Distinguish them by printing "
               "$time periodically, or by checking whether the VCD keeps growing: if time is "
               "advancing it is (1) or (3); if not, it is (2).")
    sol(w, 35, [N("The "), M("disable iff (!rst_n)"),
                 N(" clause is missing, or rst_n is itself x at time 0 so the disable condition "
                   "cannot be evaluated. During reset nothing is guaranteed and every property "
                   "must be switched off."),
                N("If rst_n is x at time 0, initialise it in the testbench before the first "
                  "edge — that is part 1 of the six parts.")])
    sol(w, 36, "The coverage model had no bin for the SEQUENCE. Bins 0–10 in the lab are all "
               "instantaneous conditions; bin 11, 'full → empty → full', is a sequence over time "
               "and needs a small state machine to detect. A model made only of instantaneous "
               "bins reports 100% while never having exercised any interesting ordering. Fix: "
               "add sequence bins — in SystemVerilog, cover properties or transition bins.")
    sol(w, 37, "The simulator has no model of metastability: it resolves every flip-flop to a "
               "clean 0 or 1, so a missing or inadequate synchroniser simulates identically to a "
               "correct one. On hardware the receiving flip-flop occasionally goes metastable "
               "and resolves unpredictably. What would have caught it: a structural CDC checker, "
               "or review — two flip-flops for a single-bit level, Gray coding or a handshake "
               "for a bus. Not simulation.")
    sol(w, 38, [N("Waveform dumping. 80% of the time in file I/O with a green regression means "
                  "every run is writing a VCD nobody will ever look at."),
                N("Fix: remove the $dumpvars from the regression path (guard it with a plusarg "
                  "or an `ifdef) and re-run only the failing seed with dumping switched on. "
                  "Expect the run time to fall by several times.")])

    w.h2("Block D")
    sol(w, 39, "See Topic5_Lab/tb/tb_v1_naive.v for a complete worked version. The six parts: "
               "clock and reset; push/pop tasks; (no model at this stage); a check task with an "
               "error counter; $dumpfile/$dumpvars; a PASS/FAIL line, $finish, and a separate "
               "watchdog initial block. The commonest omissions in student answers are the "
               "watchdog and releasing reset between edges rather than on one.")
    sol(w, 40, None, code=[
        "reg [W-1:0] model [0:DEPTH-1];",
        "integer     mhead, mtail;",
        "function [$clog2(DEPTH):0] mcount; input d; mcount = mtail - mhead;        endfunction",
        "function mempty; input d; mempty = (mtail == mhead);                       endfunction",
        "function mfull;  input d; mfull  = ((mtail - mhead) == DEPTH);             endfunction",
        "function [W-1:0] mfront; input d; mfront = model[mhead % DEPTH];           endfunction",
        "",
        "task model_cycle(input do_w, input do_r, input [W-1:0] dat);",
        "  reg was_full, was_empty;",
        "  begin",
        "    was_full  = mfull(0);          // SAMPLE BOTH FIRST - this is the whole point",
        "    was_empty = mempty(0);",
        "    if (do_w && !was_full)  begin model[mtail % DEPTH] = dat; mtail = mtail + 1; end",
        "    if (do_r && !was_empty) mhead = mhead + 1;",
        "  end",
        "endtask"])
    sol(w, 41, "See tb_v2_selfcheck.v. The eight tests are: post-reset state; fill to full; "
               "write while full; drain to empty; read while empty; simultaneous read+write held "
               "half full; enough cycles to wrap; final drain. Verified result: 4 of 5 bugs "
               "caught, golden design passes. The one that escapes is fifo_b5, because no "
               "directed test asserts read and write together while EMPTY.")
    sol(w, 42, None, code=[
        "integer seed = 1, seed0 = 1, cycles = 3000, p_wr = 55, p_rd = 45;",
        "if (!$value$plusargs(\"SEED=%d\",   seed))   seed   = 1;",
        "seed0 = seed;                      // $random UPDATES seed - keep the original",
        "if (!$value$plusargs(\"CYCLES=%d\", cycles)) cycles = 3000;",
        "if (!$value$plusargs(\"WR=%d\",     p_wr))   p_wr   = 55;",
        "if (!$value$plusargs(\"RD=%d\",     p_rd))   p_rd   = 45;",
        "",
        "do_w = (({$random(seed)} % 100) < p_wr);",
        "do_r = (({$random(seed)} % 100) < p_rd);",
        "",
        "$display(\"PASS - seed=%0d cycles=%0d wr=%0d rd=%0d\", seed0, cycles, p_wr, p_rd);"])
    sol(w, 43, "See tb_v4_coverage.v. Bin 11 needs two flags: seen_full, set whenever the FIFO "
               "is full; and seen_empty_after_full, set when it is empty and seen_full is "
               "already set. When both are set and it goes full again, increment bin 11 and "
               "reset seen_empty_after_full. Everything else is a one-line condition sampled "
               "each cycle.")
    sol(w, 44, [N("The bin is a two-cycle sequence, so it needs one flag:"),
                N("The read-heavy profile hits it most often, because after a write the FIFO is "
                  "non-empty and a read is very likely on the next cycle. The write-heavy "
                  "profile hits it least.")],
        code=["reg wrote_last;",
              "if (wrote_last && do_r && !was_empty) cov[12] = cov[12] + 1;",
              "wrote_last <= (do_w && !was_full);"])
    sol(w, 45, None, code=[
        "// 1. \"rd_data is only meaningful while empty=0\" - it must never be x then",
        "a_rd_known: assert property (@(posedge clk) disable iff (!rst_n)",
        "    !empty |-> !$isunknown(rd_data));",
        "",
        "// 2. \"a write while full is IGNORED\" - occupancy must not change",
        "a_wr_at_full: assert property (@(posedge clk) disable iff (!rst_n)",
        "    (wr_en && full && !(rd_en && !empty)) |=> (count == $past(count)));",
        "",
        "// 3. \"reset empties the FIFO\" - checked on the cycle after reset releases",
        "a_reset_empty: assert property (@(posedge clk)",
        "    $rose(rst_n) |=> (count == 0 && empty));"])
    sol(w, 46, "See tb_v6_assert.sv. The test of a correct refactoring is mechanical: the "
               "monitor contains no assignment to any DUT input, and the scoreboard contains no "
               "reference to any DUT signal other than the outputs the monitor passed it. If "
               "either is untrue, the layers are not actually separate.")
    sol(w, 47, "W and DEPTH as localparams driving everything: the signal declarations, the "
               "model array size, the loop bounds in the fill and drain tests, the count "
               "comparison width ($clog2(DEPTH)+1 bits), and the coverage bin for 'reached "
               "full'. The commonest thing students forget is the count width — an 8-deep FIFO "
               "needs 4 bits, and hard-coding [3:0] breaks silently at DEPTH=16.")
    sol(w, 48, [N("Any bug outside what the testbench checks will do. Examples that survive a "
                  "V3-class testbench:"),
                N("· rd_data is correct but glitches for one delta before settling — the "
                  "testbench samples after #1 and never sees it."),
                N("· the FIFO works correctly for the first 2^AW wraps and then fails — the test "
                  "never runs long enough."),
                N("· an output is correct but takes an extra cycle to become valid when the FIFO "
                  "goes from empty to non-empty — if the testbench never checks that transition "
                  "specifically."),
                N("Each is closed by adding the corresponding check and coverage bin, which is "
                  "the point of the exercise.")])
    sol(w, 49, "The model is a simple shadow register: on each enabled clock, shadow <= "
               "{shadow[W-2:0], sin}; on clear, shadow <= 0. It is almost the same as the design, "
               "which is fine here — the specification for a shift register genuinely is that "
               "expression. The value of the testbench is in the CONTROL: that clear beats "
               "enable, that a disabled cycle changes nothing, and that reset dominates both.")
    sol(w, 50, [N("Entering every state and recovering from an illegal state both need to see "
                  "the state register, which is internal. Keep it out of the scoreboard by "
                  "separating the roles:"),
                N("· The SCOREBOARD checks only the outputs — the light patterns and their "
                  "durations — against a model built from the specification."),
                N("· COVERAGE may look at the internal state, because coverage measures what "
                  "happened rather than deciding correctness. A hierarchical reference is "
                  "acceptable there."),
                N("· Forcing an illegal state is a deliberate white-box test in its own file, "
                  "clearly labelled, and it checks only that the machine returns to a legal "
                  "state — which is an output-visible property.")])
    sol(w, 51, None, code=[
        "module reqack_checker (input wire clk, rst_n, req, ack);",
        "  a_req_stable: assert property (@(posedge clk) disable iff (!rst_n)",
        "      (req && !ack) |=> req)          else $error(\"req dropped before ack\");",
        "  a_no_lone_ack: assert property (@(posedge clk) disable iff (!rst_n)",
        "      ack |-> req)                    else $error(\"ack without req\");",
        "  a_req_falls:  assert property (@(posedge clk) disable iff (!rst_n)",
        "      (req && ack) |=> !req)          else $error(\"req did not fall after ack\");",
        "  c_handshake:  cover property (@(posedge clk) disable iff (!rst_n) req && ack);",
        "endmodule",
        "",
        "// bound alongside the DUT in the testbench, without editing the DUT:",
        "reqack_checker u_chk (.clk(clk), .rst_n(rst_n), .req(req), .ack(ack));"])
    sol(w, 52, [N("See section 2.12 for the code. What it CANNOT find:"),
                N("· any bug outside the fixed stimulus in the file — it cannot reach a corner "
                  "nobody generated;"),
                N("· a divergence between the file and the current specification, because "
                  "nothing checks that the golden file is still right;"),
                N("· which RULE was broken — a mismatch names a vector number, not a property.")])

    w.h2("Block E")
    sol(w, 53, [N("The smallest effective change is to fill the FIFO past DEPTH and read it back. "
                  "Adding this before the existing checks catches fifo_b1 and fifo_b4:")],
        code=["for (i = 0; i < DEPTH + 1; i = i + 1) push(8'h10 + i[7:0]);",
              "for (i = 0; i < DEPTH;     i = i + 1) begin",
              "  pop(got);  check(got, 8'h10 + i[7:0], \"filled then drained\");",
              "end",
              "",
              "// It works because both bugs are at the FULL boundary, and V1 never went there."])
    sol(w, 54, "See scripts/regress.sh for a worked version. The essentials: loop over profiles "
               "and seeds; capture the output; grep for ^PASS; print one line per run including "
               "the seed; accumulate a failure list; print the reproduction command; exit 1 if "
               "anything failed. The exit code is what makes it usable from a CI system.")
    sol(w, 55, [N("Each run writes build/cov_<TAG>.txt with one line per bin: index, count, "
                  "name. Merging is a sum per index:")],
        code=["awk '{ c[$1] += $2 } END { for (i=0;i<12;i++) print i, c[i] }' build/cov_*.txt",
              "",
              "# Verified merged result across the three profiles: 12 of 12 bins covered."])
    sol(w, 56, None, code=[
        "fifo_b1  a_full_iff_depth  205 ns   full and count disagree - the flag is the bug",
        "fifo_b2  a_count_range     425 ns   count underflowed past DEPTH - a range violation",
        "fifo_b3  a_step_both       545 ns   a simultaneous r+w changed the occupancy",
        "fifo_b4  (none)            456 ns   the CONTROL interface stays correct; only DATA",
        "                                    is corrupted, and no property describes the data",
        "fifo_b5  a_step_up         465 ns   a write did not increase count by exactly one"])
    sol(w, 57, "The point of the exercise is the timing. A colleague given a raw VCD typically "
               "takes several minutes to assemble a useful view; given a .gtkw they are looking "
               "at the right signals in seconds. That difference, multiplied by every person who "
               "ever debugs the block, is why the save file is committed.")
    sol(w, 58, "Expect a large ratio — commonly 3× to 10× on a design of this size, and more on "
               "a bigger one, because dumping writes a line of text for every signal change. The "
               "exact number is what you should report; the lesson is that a regression should "
               "dump nothing by default.")
    sol(w, 59, "Answers will vary by release. Things that commonly need adjusting: the exact "
               "form of the -d / +define+ argument for a string macro; whether -sv is required "
               "for the SystemVerilog files; the name of the simulation snapshot; and, in "
               "ModelSim, the multilib packages needed on a 64-bit Linux host. Record what you "
               "changed — that record is worth more to the next class than the script itself.")
    sol(w, 60, [N("The plan has one row per rule in the header comment of rtl/fifo.v — the "
                  "two-part bullets about writes and reads split into an 'accepted' row and an "
                  "'ignored' row. A correct answer looks like this (abridged):")],
        code=[
        "RULE                          CHECKED BY              STIMULUS      BIN          ",
        "write accepted when !full     scoreboard, every cyc   random        write accepted",
        "write while full ignored      a_full_iff_depth + sb   write-heavy   wr while full ",
        "read accepted when !empty     scoreboard, every cyc   random        read accepted ",
        "read while empty ignored      a_count_range + sb      read-heavy    rd while empty",
        "rd_data is the oldest word    scoreboard              random        (implicit)    ",
        "count is 0..DEPTH             a_count_range           all           reached full  ",
        "empty<=>0, full<=>DEPTH       a_empty_iff_zero etc    all           reached empty ",
        "order preserved, none lost    scoreboard + drain      all           wrapped       ",
        "reset empties the FIFO        directed T1             directed      post-reset    ",
        "",
        "// The commonest GAP students find in their own testbench: nothing explicitly",
        "// checks 'no word is duplicated'. The drain at the end of V3 does check it,",
        "// but only if the model is drained to exactly empty and compared word by word."])


def build_reference(w):
    w.page_break()
    w.h1("Part 7 · Reference")

    w.h2("7.1  Glossary")
    w.table(["Term", "Meaning"],
            [["Verification", "establishing that a design does what its specification says."],
             ["Validation", "establishing that the specification was the right one."],
             ["DUT", "device under test — the design the testbench instantiates."],
             ["Testbench", "a port-less module that instantiates the DUT, drives it, and decides "
                           "automatically whether the results were correct."],
             ["Self-checking", "the testbench forms its own verdict; no human reads a waveform."],
             ["Reference model", "an independent implementation of the specification, written "
                                 "from the spec, used to compute expected results."],
             ["Golden model / vectors", "a trusted external reference — a C model, or a file of "
                                        "expected outputs."],
             ["Scoreboard", "the component that compares DUT behaviour against the model."],
             ["Driver", "the layer that knows the pin-level protocol."],
             ["Monitor", "the layer that observes the pins and drives nothing."],
             ["Generator / sequencer", "the layer that decides which scenarios to run."],
             ["Directed test", "a test whose case and expected result you wrote by hand."],
             ["Constrained-random", "stimulus generated by weighted or solver-driven random "
                                    "choice within constraints you specify."],
             ["Seed", "the number that makes a random run reproducible."],
             ["Regression", "the full set of tests, run automatically after every change."],
             ["Code coverage", "which lines, branches, conditions and toggles the tests reached."],
             ["Functional coverage", "which specification-level situations the tests reached."],
             ["Coverage bin", "one counted situation in a functional coverage model."],
             ["Cross", "coverage of a combination of two or more coverpoints."],
             ["Coverage hole", "a bin nothing ever hit — a gap in evidence, not a failure."],
             ["Coverage closure", "every bin hit, or every remaining hole waived in writing."],
             ["Assertion", "a rule stated in the design's language and checked every clock edge."],
             ["Cover property", "the same syntax used to RECORD that a situation occurred."],
             ["Vacuous pass", "an assertion whose antecedent never became true, so it proved "
                              "nothing."],
             ["Immediate assertion", "a check inside procedural code, evaluated when reached."],
             ["Concurrent assertion", "a property checked on a clock, continuously."],
             ["SVA", "SystemVerilog Assertions."],
             ["UVM", "Universal Verification Methodology — a SystemVerilog class library that "
                     "standardises the testbench layers."],
             ["Formal verification", "proving a property for all input sequences, or producing "
                                     "a counter-example."],
             ["CDC", "clock domain crossing — and a class of bug simulation cannot find."],
             ["Metastability", "a flip-flop settling unpredictably after a setup or hold "
                               "violation. Not modelled by any simulator."],
             ["Event queue", "the simulator's ordered list of scheduled events."],
             ["Stratified regions", "Active, Inactive, NBA and Monitor — the ordering within one "
                                    "simulation time step."],
             ["VCD / FST / WLF / FSDB", "waveform file formats — plain, compressed, and "
                                        "vendor-native."],
             ["Watchdog", "a timeout that turns a hung simulation into a FAIL."]],
            widths=[1.7, 4.7], size=9, align_center=False)

    w.h2("7.2  Testbench checklist")
    w.numbered([
        "Does it have all six parts, including the verdict AND a watchdog?",
        "Does it print a PASS or FAIL line a machine can grep for?",
        "Does it compare with === and !==, never == and !=?",
        "Is reset asserted before the first edge and released BETWEEN edges?",
        "Is every input driven a small delay AFTER the active edge?",
        "Are expected values computed by a model written from the SPECIFICATION?",
        "Does the model sample its state once, before applying any operation?",
        "Does the scoreboard avoid every hierarchical reference into the DUT?",
        "Are the boundary cases present: full, empty, write-while-full, read-while-empty, "
        "simultaneous read and write, and a wrap?",
        "Is the stimulus seeded, and is the ORIGINAL seed printed on every result line?",
        "Is there a coverage model, and does the run report HIT/MISS per bin?",
        "Are there assertions for the control interface, and has each one been hit at least "
        "once?",
        "Does it run in a regression across several seeds and profiles?",
        "Does the regression dump no waveforms by default?",
        "Would it FAIL if the design were wrong? Name a change it would not catch.",
    ])

    w.h2("7.3  Troubleshooting")
    w.table(["Symptom", "Almost always means", "Fix"],
            [["Everything is x from time 0", "reset never asserted, or a misspelt DUT port",
              "check reset polarity; `default_nettype none"],
             ["A check passes when the value is x", "== used instead of ===",
              "use === and !== in every check"],
             ["The design looks one cycle late", "sampled before the NBA update landed",
              "sample after the NEXT edge, or use $strobe"],
             ["A pulse is half a cycle wide", "stimulus driven ON the clock edge",
              "drive at #1 after the edge, never on it"],
             ["Random test drove 9 transactions", "$urandom(seed) called inside the loop",
              "seed once with void'($urandom(s)), then $urandom()"],
             ["Both enables high on every cycle", "raw $random used as a boolean",
              "({$random(seed)} % 100) < weight"],
             ["The CORRECT design fails", "the reference model is wrong",
              "sample full/empty once, before applying either operation"],
             ["Simulation never ends", "no $finish, or a wait loop with no delay",
              "add $finish and a watchdog; put @(posedge clk) in the loop"],
             ["The waveform has no signals", "$dumpvars scope too narrow, or a stale VCD",
              "$dumpvars(0, tb); and re-run before re-opening"],
             ["An assertion fires at time 0", "no disable iff (!rst_n), or rst_n is x",
              "add the disable clause; initialise rst_n"],
             ["An assertion has never fired", "it may be vacuous",
              "check assertion coverage; look at the antecedent"],
             ["Coverage 100% but bugs escape", "the model has no SEQUENCE bins",
              "add bins for orderings, not just states"],
             ["Regression takes all night", "waveform dumping on every run",
              "dump nothing; re-run the failing seed with dumping on"]],
            widths=[2.0, 2.2, 2.2], size=9, align_center=False)

    w.h2("7.4  Command card")
    w.table(["Task", "Open-source", "Vivado", "ModelSim / Questa"],
            [["Lint", "verilator --lint-only -Wall rtl/*.v", "report_methodology",
              "vlog (warnings)"],
             ["Compile", "iverilog -g2005 -o sim.vvp <files>", "xvlog <files>", "vlog <files>"],
             ["Compile SV", "verilator --binary --timing --assert", "xvlog -sv", "vlog -sv"],
             ["Define a macro", "-DDUT=fifo_b1", "-d DUT=fifo_b1", "+define+DUT=fifo_b1"],
             ["Plusarg", "vvp sim.vvp +SEED=1", "xsim s -testplusarg SEED=1", "vsim +SEED=1"],
             ["Run", "vvp sim.vvp", "xsim <snap> -runall", "vsim -c work.<top>; run -all"],
             ["Waveforms", "gtkwave dump.vcd", "wave window", "add wave -r /*"],
             ["Assertions", "--assert (subset)", "full SVA", "full SVA, -assertdebug"],
             ["Coverage", "--coverage", "-cover, report_coverage", "vlog -cover bcesx"],
             ["Merge coverage", "awk over cov_*.txt", "report_coverage", "vcover merge"]],
            widths=[1.1, 2.2, 1.6, 1.8], size=8.5, align_center=False)

    w.h2("7.5  The lab in one page")
    w.code([
        "cd Topic5_Lab",
        "make lint          # one second - always first",
        "make run           # every lab against the golden FIFO: all PASS",
        "make clinic        # the V1/V2/V3 x six-designs matrix. The point of Topic 5.",
        "make cover         # coverage across three profiles, merged",
        "make assert        # assertions vs scoreboard on every broken design",
        "make regress       # multi-seed regression",
        "make waves         # run V3 and open GTKWave with the saved view",
    ], caption="Everything, from a clean checkout")
    w.table(["", "fifo", "b1", "b2", "b3", "b4", "b5", "caught"],
            [["V1 naive directed", "pass", "pass", "pass", "pass", "pass", "pass", "0 / 5"],
             ["V2 model + corners", "pass", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT", "pass",
              "4 / 5"],
             ["V3 constrained-random", "pass", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT", "CAUGHT",
              "5 / 5"]],
            widths=[1.7, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], size=8.5)

    w.h2("7.6  Where this leads")
    w.bullets([
        [B("Topic 6 — timing constraints and analysis. "),
         N("The verification skills here do not stop being needed: every timing fix is a design "
           "change, and every design change has to be re-verified. That is what the regression "
           "is for.")],
        [B("The lab. "), N("Topic5_Lab/ contains one DUT, five planted bugs, six testbenches and "
                           "scripts for three toolchains. The experiments at the end of its "
                           "README are worth more than any additional reading.")],
        [B("Standards. "), N("IEEE 1800 defines SystemVerilog including assertions, constraints "
                             "and covergroups. You do not need to read it end to end, but "
                             "knowing your tool's behaviour is defined somewhere matters when "
                             "two tools disagree.")],
    ])
    w.para([I("End of Topic 5 workbook. Every design, testbench and script referred to here is "
              "in Topic5_Lab/, and every quoted tool output was produced by running the tool on "
              "that code.")])
