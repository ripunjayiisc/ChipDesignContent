# -*- coding: utf-8 -*-
"""Topic 5 workbook — Part 2: testbench development."""
import _boot
from wbkit import *
from t5_wb1 import B, N, I, M


def build(w):
    w.page_break()
    w.h1("Part 2 · Testbench Development")
    w.para("Part 1 was the argument. Part 2 is the craft: how a testbench is actually built, in "
           "six stages, each measured against the same five broken designs.")

    # ---------------------------------------------------------- 2.1
    w.h2("2.1  The device under test")
    w.para([N("Everything in this part is built against one design: the small synchronous FIFO "
              "in "), M("Topic5_Lab/rtl/fifo.v"),
            N(". Its header comment is the specification, and every bullet in it becomes a "
              "check.")])
    w.code([
        "//  * A write is accepted on a rising clk when wr_en=1 and full=0.",
        "//    A write attempted while full is IGNORED and must not corrupt anything.",
        "//  * A read is accepted on a rising clk when rd_en=1 and empty=0.",
        "//    A read attempted while empty is IGNORED.",
        "//  * rd_data shows the OLDEST unread word at all times (first-word fall-through).",
        "//    It is only meaningful while empty=0.",
        "//  * count is the number of words currently stored, 0..DEPTH.",
        "//  * empty <=> count==0.   full <=> count==DEPTH.",
        "//  * Words come out in the order they went in. No word is lost or duplicated.",
        "//  * Asynchronous active-low reset empties the FIFO.",
    ], caption="The interface contract — this IS the verification plan")
    w.para("Eight rules. A finished testbench has a check for each, and a coverage bin proving "
           "the situation actually arose. That mapping — rule to check to bin — is what a "
           "verification plan is.")
    w.h3("And five broken copies")
    w.table(["Variant", "The bug", "Realistic because"],
            [["fifo_b1", "full asserts one entry late, so a DEPTH+1'th write is accepted and "
                         "the oldest word is overwritten", "> instead of == in a comparison"],
             ["fifo_b2", "the read is not guarded, so rd_ptr advances even when empty and count "
                         "underflows", "a missing & ~empty on one signal"],
             ["fifo_b3", "count comes from a separate register that is not updated on a "
                         "simultaneous read and write", "an else-if chain that looked complete"],
             ["fifo_b4", "the write address is clamped instead of wrapped, so words after a "
                         "wrap go to the wrong place", "a conditional written for the wrong "
                                                       "boundary"],
             ["fifo_b5", "a write is dropped when wr_en and rd_en are asserted together while "
                         "EMPTY", "an over-eager guard added to fix something else"]],
            widths=[0.9, 3.2, 2.3], size=9, align_center=False)
    w.para([B("Do not read that table before attempting the clinic."),
            N("  All five lint clean, all five synthesise, and all five pass a naive testbench.")])

    # ---------------------------------------------------------- 2.2
    w.h2("2.2  The six parts")
    w.image("tb_anatomy", 6.4, "Every testbench has these, whatever the design.")
    w.numbered([
        "CLOCK AND RESET. A free-running clock, and a reset asserted before the first edge and "
        "released between edges.",
        "STIMULUS. Tasks that drive the pins according to the interface protocol.",
        "REFERENCE MODEL. An independent computation of what should happen.",
        "CHECKS. One place that compares, counts errors and reports.",
        "WAVEFORM DUMP. $dumpfile and $dumpvars, so a failure can be looked at.",
        "VERDICT AND STOP. A PASS or FAIL line and a $finish — plus a watchdog.",
    ])
    w.callout("Part 6 is the one people omit",
              [[N("A testbench that never calls "), M("$finish"),
                N(" runs until somebody kills it, which in a regression means the whole run "
                  "hangs. Add a watchdog too — a second initial block that prints FAIL and "
                  "finishes after a generous timeout — so a hung DUT FAILS rather than stalling "
                  "everything behind it.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")
    w.code([
        "initial begin                        // the watchdog: every testbench needs one",
        "  #(CLK * 5000);",
        "  $display(\"FAIL - timeout on %0s\", `DUTNAME);",
        "  $finish;",
        "end",
    ], caption="Five lines that turn a hang into a failure")

    # ---------------------------------------------------------- 2.3
    w.h2("2.3  Lab V1 — the testbench everybody writes first")
    w.para("V1 has all six parts and it does form its own verdict, so it is already better than "
           "a testbench that only prints values. It writes three words, reads three words, "
           "checks them, and prints PASS.")
    w.code([
        "push(8'hA1);  push(8'hB2);  push(8'hC3);",
        "pop(got);  check(got, 8'hA1, \"first word out\");",
        "pop(got);  check(got, 8'hB2, \"second word out\");",
        "pop(got);  check(got, 8'hC3, \"third word out\");",
        "if (errors == 0) $display(\"PASS - 3 words in, 3 words out\");",
    ], caption="Topic5_Lab/tb/tb_v1_naive.v — the whole test")
    w.code([
        "$ ./scripts/clinic.sh",
        "",
        "  V1 naive directed      pass      pass      pass      pass      pass      pass",
        "                         fifo      fifo_b1   fifo_b2   fifo_b3   fifo_b4   fifo_b5",
        "  V1 : 0 of 5 bugs caught, golden design passes (no false alarm)",
    ], caption="Verified output")
    w.para("It misses every bug, and the reason is not that it is short. It never fills the "
           "FIFO, never empties it past zero, never asserts read and write on the same cycle, "
           "never wraps the pointers, and never attempts a write while full or a read while "
           "empty. Three words in and three words out exercises the one path where a broken FIFO "
           "and a correct one behave identically.")
    w.callout("State the lesson explicitly",
              ["Coverage of the SPECIFICATION, not volume of stimulus, is what makes a testbench "
               "worth having. V1 could run three million words instead of three and still catch "
               "nothing."],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 2.4
    w.h2("2.4  Clock, reset and stimulus timing")
    w.image("stimulus_timing", 6.2, "The commonest testbench bug, and the rule that prevents it.")
    w.code([
        "localparam integer CLK = 10;         // 10 ns period = 100 MHz",
        "reg clk = 1'b0;",
        "always #(CLK/2) clk = ~clk;",
        "",
        "initial begin",
        "  rst_n = 1'b0;",
        "  repeat (3) @(posedge clk);",
        "  #1 rst_n = 1'b1;                   // released just AFTER an edge, never ON one",
        "end",
        "",
        "// and every driver follows the same discipline:",
        "task push(input [W-1:0] dat);",
        "  begin",
        "    @(posedge clk); #1;  wr_en = 1'b1; wr_data = dat;   // DRIVE after the edge",
        "    @(posedge clk); #1;  wr_en = 1'b0;                  // SAMPLE after the next one",
        "  end",
        "endtask",
    ], caption="Clock, reset, and a driver task")
    w.para("If you change an input at the same instant as the clock edge you have created a "
           "race, and which value the DUT sees is not defined — it depends on the order the "
           "simulator happens to process the two events. The design is not broken; the testbench "
           "is.")
    w.callout("Two real examples from these labs", [
        [B("Topic 4, edge detector. "), N("The stimulus changed mid-cycle, so the pulse under "
           "test was half a cycle wide and the check sampled at the wrong moment. The design was "
           "correct.")],
        [B("Topic 4, FSM. "), N("Reset was released exactly ON a clock edge. The state register "
           "saw an ambiguous condition and stayed x for two cycles, and the sequence detector "
           "reported one match instead of two. The design was correct.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 2.5
    w.h2("2.5  The reference model")
    w.image("refmodel", 6.2, "A second implementation of the specification.")
    w.para("Hand-written expected values do not scale past about twenty cases. A reference model "
           "is a second, independent implementation of the specification — usually far simpler "
           "than the RTL, because it need not be efficient, parallel or synthesisable.")
    w.code([
        "reg [W-1:0] model [0:DEPTH-1];",
        "integer     mhead, mtail;                       // mtail - mhead is the occupancy",
        "",
        "function [$clog2(DEPTH):0] mcount; input dummy; mcount = mtail - mhead; endfunction",
        "function mempty; input dummy; mempty = (mtail == mhead);        endfunction",
        "function mfull;  input dummy; mfull  = ((mtail-mhead) == DEPTH); endfunction",
        "function [W-1:0] mfront; input dummy; mfront = model[mhead % DEPTH]; endfunction",
    ], caption="The FIFO's model — an array and two indices")
    w.para("Once the model exists you can compare EVERY cycle — count, empty, full and the "
           "output word — instead of only at the points where you happened to write a check.")
    w.callout("Two rules", [
        [B("1. Write it from the SPECIFICATION, never by reading the RTL."),
         N("  A model derived from the design agrees with the design's bugs. If the same person "
           "must write both, write the model first.")],
        [B("2. It never looks inside the DUT."),
         N("  Only at the same inputs, and its own state. A white-box check is fine while "
           "debugging and fatal for reuse: the moment the design is refactored the testbench "
           "breaks, and nobody can tell whether the design did too.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h3("A real bug — in the model")
    w.image("model_order_bug", 6.4, "The correct FIFO failed, and a broken one passed.")
    w.para("This was found while writing this lab, and it is the most instructive failure in the "
           "topic. The model applied the write, then tested its own updated state to decide "
           "whether to apply the read:")
    w.code([
        "// WRONG",
        "if (do_w && !mfull())  push(d);      // model now holds one word",
        "if (do_r && !mempty()) pop();        // ... so mempty() is FALSE, and it pops again",
        "",
        "// RIGHT",
        "was_full  = mfull();                 // sample BOTH, once, before applying either",
        "was_empty = mempty();",
        "if (do_w && !was_full)  push(d);",
        "if (do_r && !was_empty) pop();",
    ], caption="Topic5_Lab/tb/tb_v2_selfcheck.v — task model_cycle")
    w.para("On a simultaneous read and write to an EMPTY FIFO, the wrong version pushes, "
           "observes itself no longer empty, and pops the word straight back out — reporting an "
           "occupancy of 0 where the hardware correctly has 1. The golden FIFO \"failed\"; "
           "fifo_b5, which really does drop that write, \"passed\".")
    w.callout("The general rule",
              ["Hardware evaluates every enable from the state that existed BEFORE the clock "
               "edge, all at once. A model that applies one operation and then tests its own "
               "updated state is modelling something the hardware never does. Sample first; "
               "then apply."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 2.6
    w.h2("2.6  Lab V2 — the model plus the corners")
    w.para("V2 is not a longer test than V1; it is a better-chosen one. Eight directed tests, "
           "every one of them at a boundary, each compared against the model on every cycle.")
    w.table(["Test", "What it does", "What it proves"],
            [["T1", "check the state immediately after reset", "reset really empties the FIFO"],
             ["T2", "fill to exactly full", "full asserts at DEPTH, and not before"],
             ["T3", "a write WHILE FULL", "it is ignored, and nothing is corrupted"],
             ["T4", "drain to exactly empty", "empty asserts at 0, and not before"],
             ["T5", "a read WHILE EMPTY", "it is ignored, and count does not underflow"],
             ["T6", "read and write on the same cycle, held half full",
              "occupancy is unchanged and the data is right"],
             ["T7", "keep going long enough to WRAP the pointers",
              "the addressing is correct past the end of the array"],
             ["T8", "final drain", "everything that went in comes out, in order"]],
            widths=[0.6, 2.9, 2.9], size=9, align_center=False)
    w.code([
        "  V2 model + corners     pass     CAUGHT   CAUGHT   CAUGHT   CAUGHT   pass",
        "  V2 : 4 of 5 bugs caught, golden design passes (no false alarm)",
    ], caption="Verified output")

    # ---------------------------------------------------------- 2.7
    w.h2("2.7  Constrained-random stimulus")
    w.image("random_weights", 6.4, "The weights are the test.")
    w.code([
        "do_w = (({$random(seed)} % 100) < p_wr);      // p_wr and p_rd are the CONSTRAINTS",
        "do_r = (({$random(seed)} % 100) < p_rd);",
        "d    = $random(seed);",
    ], caption="Topic5_Lab/tb/tb_v3_random.v — the whole generator")
    w.para("Constrained-random does not mean unconstrained. You still decide what the test does; "
           "you express it as weights rather than as a list of cases, and the generator produces "
           "the sequences. Change the weights and you are testing a different part of the "
           "design:")
    w.table(["Profile", "Weights", "Where the occupancy lives", "What it never reaches"],
            [["write-heavy", "+WR=90 +RD=10", "at FULL", "empty; 3 of 12 bins MISS"],
             ["read-heavy", "+WR=10 +RD=90", "at EMPTY", "full; 4 of 12 bins MISS"],
             ["balanced", "+WR=50 +RD=50", "the whole range", "nothing — all 12 bins HIT"]],
            widths=[1.3, 1.6, 1.9, 1.8], size=9.5, align_center=False)
    w.h3("Seeds")
    w.image("seed_repro", 6.0, "The seed is what makes a random failure debuggable.")
    w.para("A random failure you cannot reproduce is not a bug report; it is a rumour. The seed "
           "makes every run deterministic, so a failure can be replayed exactly — with waveforms "
           "this time. Print it on every line, pass or fail.")
    w.callout("Two traps with random number generation", [
        [M("$random(seed)"), N(" in Verilog UPDATES seed in place. If you print "), M("seed"),
         N(" at the end of the run you will print the final internal state, not the seed you "
           "were given. Save the original into "), M("seed0"), N(" before the loop.")],
        [M("$urandom(seed)"), N(" in SystemVerilog "), B("re-seeds on every call"),
         N(", so calling it with an argument inside a loop returns the same number for ever. "
           "This happened while writing Lab V6: the run reported PASS and had driven 9 "
           "transactions instead of 895. Seed once with "), M("void'($urandom(seed0));"),
         N(", then call "), M("$urandom()"), N(" with no argument.")],
        [B("A random test that is silently not random is worse than no random test, because it "
           "is believed.")],
    ], color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 2.8
    w.h2("2.8  Lab V3, and the fifth bug")
    w.code([
        "  V3 constrained-random  pass     CAUGHT   CAUGHT   CAUGHT   CAUGHT   CAUGHT",
        "  V3 : 5 of 5 bugs caught, golden design passes (no false alarm)",
    ], caption="Verified output")
    w.para([M("fifo_b5"), N(" drops a write when wr_en and rd_en are asserted together while the "
              "FIFO is EMPTY. That is a legal, sensible combination — and no directed test in V2 "
              "ever produces it, because nobody thinks to write \"read and write at once, from "
              "an empty FIFO\" as a test case. The random generator produced it ten times in "
              "three thousand cycles without being asked. That is the entire argument for "
              "constrained-random stimulus.")])
    w.h3("Regressions")
    w.para("One random run is one sample. A regression — many seeds, several profiles, run "
           "automatically after every change — is what makes it evidence.")
    w.code([
        "$ ./scripts/regress.sh 4        # 4 seeds x 3 profiles",
        "",
        "  profile        seed     cycles   result",
        "  balanced       1        3000     pass",
        "  balanced       2        3000     pass",
        "  write-heavy    1        3000     pass",
        "  ...",
        "  12 passed, 0 failed",
        "  REGRESSION CLEAN",
    ], caption="Verified output")
    w.para("When a run fails, the script prints the exact command that reproduces it. That one "
           "line is the difference between a bug report somebody can act on and one they cannot.")

    # ---------------------------------------------------------- 2.9
    w.h2("2.9  Functional coverage by hand")
    w.image("cov_bins", 6.4, "Twelve bins, three profiles, and the merge that closes them.")
    w.para("SystemVerilog has covergroups. Plain Verilog does not, so Lab V4 does it the long "
           "way: one counter per interesting situation, declared up front as a coverage model, "
           "sampled every cycle, and reported at the end with a HIT/MISS verdict per bin.")
    w.code([
        "//   0  write accepted            6  occupancy reached DEPTH (full)",
        "//   1  read accepted             7  occupancy reached 0 (empty)",
        "//   2  read+write same cycle     8  pointers wrapped at least once",
        "//   3  idle cycle                9  write attempted while full",
        "//   4  read+write while EMPTY   10  read attempted while empty",
        "//   5  read+write while FULL    11  a full -> empty -> full round trip",
        "",
        "if (do_w && !was_full)          cov[0]  = cov[0]  + 1;",
        "if (do_w && do_r && was_empty)  cov[4]  = cov[4]  + 1;",
        "if (was_full)                   cov[6]  = cov[6]  + 1;",
        "",
        "// bin 11 is a SEQUENCE, so it needs a little state machine of its own:",
        "if (was_full)                            seen_full = 1;",
        "if (seen_full && was_empty)              seen_empty_after_full = 1;",
        "if (seen_empty_after_full && was_full) begin",
        "  cov[11] = cov[11] + 1;  seen_full = 1;  seen_empty_after_full = 0;",
        "end",
    ], caption="Topic5_Lab/tb/tb_v4_coverage.v")
    w.para("Bin 11 is the one worth studying. \"full → empty → full\" is not a state; it is a "
           "sequence over time. Real coverage models are full of these — \"a request followed by "
           "a retry\", \"back-to-back bursts\", \"reset in the middle of a transfer\" — and they "
           "are where the interesting bugs live.")
    w.h3("Closure is across the regression, not within one run")
    w.code([
        "$ ./scripts/coverage.sh",
        "",
        "  --- profile writeheavy (wr=90 rd=10) ---   bins covered:  9 of 12  (75%)",
        "  --- profile readheavy  (wr=10 rd=90) ---   bins covered:  8 of 12  (66%)",
        "  --- profile balanced   (wr=50 rd=50) ---   bins covered: 12 of 12  (100%)",
        "",
        "  merged: 12 of 12 bins covered (100%)",
        "  COVERAGE CLOSED",
    ], caption="Verified output")
    w.para("No single profile closes coverage, and none has to. Each run contributes what it "
           "reached, the results are merged, and what is still missing is the specification for "
           "the next test somebody writes.")

    # ---------------------------------------------------------- 2.10
    w.h2("2.10  Assertions")
    w.image("assertion_anatomy", 6.4, "Anatomy of a concurrent assertion.")
    w.para("A scoreboard checks outputs at the points you compare them. An assertion states a "
           "RULE, and the simulator checks it on every clock edge of every test, reporting at "
           "the exact cycle and the exact line where it broke.")
    w.table(["Element", "Means"],
            [["a_step_up:", "a name — it appears in the failure message and in coverage reports"],
             ["assert property", "this must always hold; report if it does not"],
             ["cover property", "not a rule — just RECORD whether this ever happened"],
             ["@(posedge clk)", "the sampling clock; assertions are synchronous"],
             ["disable iff (!rst_n)", "switched off during reset, where nothing is guaranteed"],
             ["|->", "implication, same cycle"],
             ["|=>", "implication, one cycle later — where a registered value shows the change"],
             ["$past(x)", "the value of x one clock ago — how you express \"changed by\""],
             ["$isunknown(x)", "true if any bit of x is x or z"],
             ["$onehot / $onehot0", "exactly one bit set / at most one bit set"]],
            widths=[1.8, 4.6], size=9.5, align_center=False)
    w.code([
        "a_empty_iff_zero: assert property (@(posedge clk) disable iff (!rst_n)",
        "    empty == (count == 0))",
        "    else $error(\"empty=%0b but count=%0d\", empty, count);",
        "",
        "a_step_up: assert property (@(posedge clk) disable iff (!rst_n)",
        "    (wr_en && !full && !(rd_en && !empty)) |=> (count == $past(count) + 1))",
        "    else $error(\"a write did not increase count by exactly one\");",
        "",
        "c_both_empty: cover property (@(posedge clk) disable iff (!rst_n)",
        "    wr_en && rd_en && empty);",
    ], caption="Topic5_Lab/sva/fifo_sva.sv")
    w.para("Read the property names aloud and they are the specification: \"empty if and only if "
           "count is zero\", \"a write steps the count up by one\". That readability is the "
           "point — an assertion nobody can read is an assertion nobody will maintain.")
    w.h3("Where to put them")
    w.para([N("In a separate module bound to the DUT's signals, as in "), M("sva/fifo_sva.sv"),
            N(". The design source stays clean, the assertions can be owned by the verification "
              "engineer, and they can be excluded from synthesis without touching the RTL.")])
    w.h3("Assertions and scoreboards catch different things")
    w.image("assert_vs_scoreboard", 6.4, "Real output from ./scripts/assert.sh")
    w.para([B("Read the fourth row carefully."), N("  Four of the five bugs are caught by a "
            "named assertion, at the exact cycle. One is not caught by any assertion at all — "
            "because the assertions in this file describe the CONTROL interface (count, full, "
            "empty) and fifo_b4 keeps all of those perfectly correct while corrupting the DATA. "
            "No property is violated, so nothing fires, and the scoreboard is what catches it.")])
    w.callout("So they are not alternatives",
              ["Assertions catch what you described. Scoreboards catch what you compared. A "
               "serious environment has both, and neither is a substitute for the other."],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 2.11
    w.h2("2.11  A layered environment")
    w.image("tb_layers", 6.4, "Each part replaceable on its own.")
    w.table(["Layer", "Knows about", "Does NOT know about"],
            [["Generator", "the test intent — which scenarios matter", "pins, timing, the DUT"],
             ["Driver", "the pin-level protocol and its timing",
              "why this transaction was chosen"],
             ["Monitor", "how to observe the pins", "how to drive anything"],
             ["Scoreboard", "what \"correct\" means", "pins, timing, protocol"],
             ["Assertions", "the rules, continuously", "the test that is running"]],
            widths=[1.3, 2.7, 2.4], size=9.5, align_center=False)
    w.para("A flat testbench works for one design. A layered one survives the second, because a "
           "new DUT usually needs a new driver only — the generator, monitor and scoreboard "
           "survive unchanged.")
    w.code([
        "// LAYER 3: monitor -- watches the pins and tells the scoreboard what happened.",
        "task automatic mon_apply(bit did_wr, bit did_rd, logic [W-1:0] dat);",
        "  bit was_full  = m_full();          // sample BOTH before applying either",
        "  bit was_empty = m_empty();",
        "  if (did_wr && !was_full)  begin model[mtail % DEPTH] = dat; mtail++; end",
        "  if (did_rd && !was_empty) begin mhead++;                          end",
        "endtask",
        "",
        "// LAYER 2: driver -- knows the pin protocol and nothing else.",
        "task automatic drv_cycle(bit do_w, bit do_r, logic [W-1:0] dat, string where);",
        "  @(posedge clk); #1;  wr_en = do_w; rd_en = do_r; wr_data = dat;",
        "  @(posedge clk); #1;  wr_en = 1'b0; rd_en = 1'b0;",
        "  mon_apply(do_w, do_r, dat);",
        "  sb_check(where);",
        "endtask",
    ], caption="Topic5_Lab/tb/tb_v6_assert.sv — verified: 2027 checks, 895 words in, 895 out")

    # ---------------------------------------------------------- 2.12
    w.h2("2.12  Testbench mechanics you will need")
    w.h3("Tasks, functions and fork/join")
    w.code([
        "task automatic push(input [W-1:0] dat);   // automatic: each call gets its own copy",
        "  begin",
        "    @(posedge clk); #1;  wr_en = 1'b1; wr_data = dat;",
        "    @(posedge clk); #1;  wr_en = 1'b0;",
        "  end",
        "endtask",
        "",
        "fork                                       // two independent stimulus threads",
        "  begin : writer  repeat (100) push($random(seed)); end",
        "  begin : reader  repeat (100) pop();               end",
        "join",
        "",
        "fork                                       // the standard timeout idiom (SystemVerilog)",
        "  begin wait (done);              end",
        "  begin #(CLK*10000); timeout = 1; end",
        "join_any  disable fork;",
    ], caption="Testbench-only constructs")
    w.para([B("automatic matters."), N("  Without it, two concurrent calls from a fork share one "
            "set of arguments and locals and corrupt each other — in a way that looks exactly "
            "like a DUT bug.")])
    w.h3("File I/O and golden vectors")
    w.code([
        "$readmemh(\"vectors/stim.hex\",   stim);      // one hex value per line",
        "$readmemh(\"vectors/golden.hex\", golden);",
        "fd = $fopen(\"build/mismatch.log\", \"w\");",
        "$fdisplay(fd, \"%0d  sent %h  got %h  expected %h\", i, stim[i], dut_out, golden[i]);",
        "$fclose(fd);",
    ], caption="When the reference is a file somebody else produced")
    w.table(["Golden vectors are right when", "and wrong when"],
            [["a published standard supplies official test vectors (AES, CRC, a codec)",
              "they fix the stimulus, so they cannot find the corner nobody generated"],
             ["a trusted bit-exact C or MATLAB reference already exists",
              "they rot — the file and the specification drift apart and nobody notices"],
             ["you are regressing against the previous revision of the same block",
              "a mismatch says WHICH vector failed, not which rule was broken"]],
            widths=[3.2, 3.2], size=9, align_center=False)

    # ---------------------------------------------------------- 2.13
    w.h2("2.13  What to check, by kind of design")
    w.table(["Kind of DUT", "The checks that matter", "Where the bugs actually are"],
            [["Combinational", "exhaustive if the input space is small; otherwise random against "
                               "a reference function", "boundaries, sign, width truncation"],
             ["Registered / pipelined", "output correct AND arriving at the right cycle; valid "
                                        "delayed with the data",
              "latency, and control not pipelined alongside the data"],
             ["Counter / timer", "wrap, load, enable priority, terminal count",
              "off-by-one at the wrap and at the reload"],
             ["FSM", "every state entered, every arc taken, illegal states recovered from",
              "the arcs nobody drew, and the missing default"],
             ["Memory / FIFO", "order, occupancy, full, empty, simultaneous access",
              "the boundaries — full, empty, and both at once"],
             ["Protocol / bus", "handshake rules as assertions, plus a checker independent of "
                                "the DUT", "the rule the OTHER end violates"],
             ["Clock crossing", "not by simulation alone — structural CDC checks and review",
              "multi-bit buses crossing without a handshake"]],
            widths=[1.4, 2.8, 2.2], size=9, align_center=False)

    # ---------------------------------------------------------- 2.14
    w.h2("2.14  SystemVerilog for verification")
    w.para("Verilog-2005 is enough to build everything in this lab, and doing it by hand once is "
           "worth the effort — you learn what a covergroup IS by writing twelve counters. "
           "SystemVerilog then provides the same things as language features, and you will meet "
           "them in every professional environment.")
    w.table(["Feature", "What it replaces here", "Tool support"],
            [["logic", "the wire / reg decision", "everywhere"],
             ["always_comb / always_ff", "always @(*), and the latch you inferred by accident",
              "everywhere"],
             ["assert / cover property", "hand-written checks scattered through the code",
              "vendor: full; open-source: a subset"],
             ["covergroup / coverpoint / cross", "the twelve integer counters of Lab V4",
              "vendor tools"],
             ["rand / randc + constraint", "the weighted $random of Lab V3", "vendor tools"],
             ["classes, mailboxes, semaphores", "the layers written as tasks in Lab V6",
              "vendor tools"],
             ["interface / modport", "the long port lists in every instantiation", "vendor tools"],
             ["queues and associative arrays", "the fixed model array and its indices",
              "vendor tools"]],
            widths=[2.0, 3.0, 1.4], size=9, align_center=False)
    w.h3("Constraints, written as constraints")
    w.code([
        "class fifo_txn;",
        "  rand bit       do_wr, do_rd;",
        "  rand bit [7:0] data;",
        "  constraint c_mix   { do_wr dist { 1 := 55, 0 := 45 };",
        "                       do_rd dist { 1 := 45, 0 := 55 }; }",
        "  constraint c_burst { (do_wr && do_rd) -> data inside {[8'h80:8'hFF]}; }",
        "endclass",
        "",
        "fifo_txn t = new();",
        "repeat (2000) begin",
        "  if (!t.randomize()) $fatal(1, \"constraints are unsatisfiable\");",
        "  drv_cycle(t.do_wr, t.do_rd, t.data);",
        "end",
    ], caption="The Lab V3 generator, expressed declaratively")
    w.callout("Always check what randomize() returns",
              [[N("An over-constrained set has no solution and "), M("randomize()"),
                N(" returns 0. If you ignore the return value the test silently drives the same "
                  "unrandomised value for ever — and passes. Check it, and "), M("$fatal"),
                N(" on failure.")]],
              color=RED, fill="FDECEF", bar="C01F43")
    w.h3("Covergroups, and the cross")
    w.code([
        "covergroup cg_fifo @(posedge clk);",
        "  cp_op : coverpoint {wr_en, rd_en} {",
        "            bins idle = {2'b00};  bins wr = {2'b10};",
        "            bins rd   = {2'b01};  bins both = {2'b11}; }",
        "  cp_occ: coverpoint count {",
        "            bins empty = {0};  bins mid = {[1:DEPTH-1]};  bins full = {DEPTH}; }",
        "  x_op_occ: cross cp_op, cp_occ;      // 12 cells - and two of them were bugs",
        "endgroup",
        "cg_fifo cg = new();",
    ], caption="Lab V4's coverage model, as a covergroup")
    w.para("The cross is the point. cp_op has 4 bins and cp_occ has 3, so the cross has 12 "
           "cells — and two of those cells, \"both while empty\" and \"both while full\", are "
           "exactly where two of the five planted bugs live. A cross says \"this situation, in "
           "that state\" in one line, which is precisely the combination that hand-written "
           "counters make tedious and that people therefore skip.")

    # ---------------------------------------------------------- 2.15
    w.h2("2.15  UVM, formal and CDC — what they are, and when")
    w.h3("UVM")
    w.para("The Universal Verification Methodology is a SystemVerilog class library that "
           "standardises exactly the layers of Lab V6.")
    w.table(["Lab V6 calls it", "UVM calls it", "What UVM adds"],
            [["generator", "uvm_sequence / uvm_sequencer", "reusable, layered, randomisable "
              "sequences"],
             ["driver", "uvm_driver", "a standard handshake with the sequencer"],
             ["monitor", "uvm_monitor", "publishes transactions to any number of subscribers"],
             ["scoreboard", "uvm_scoreboard", "standard comparison and reporting"],
             ["the whole thing", "uvm_env / uvm_agent", "a package you can instantiate twice, "
              "or reuse next project"],
             ["$display", "uvm_info / uvm_error with verbosity", "filterable, gradable reporting"],
             ["(nothing)", "the factory and config_db",
              "swap a component or a setting without editing the environment"]],
            widths=[1.7, 2.2, 2.5], size=9, align_center=False)
    w.para("Worth it when the block has a real protocol interface other blocks share, when "
           "several people work on the environment at once, or when it will be reused at chip "
           "level. Not worth it when the block is a FIFO and Lab V6 verifies it in 160 lines.")
    w.h3("Formal verification")
    w.para("Simulation samples the state space; formal tools search it. Given the assertions you "
           "already wrote, a formal engine tries to prove no input sequence can violate them — "
           "or produces the shortest counter-example that does.")
    w.bullets([
        "A PROVEN property holds for every input sequence, for ever. No amount of simulation "
        "adds to that.",
        "A counter-example from a formal tool is usually far easier to understand than a random "
        "failure at cycle 40 000.",
        "It works beautifully on control logic — FIFOs, arbiters, protocol adapters, CDC "
        "handshakes — and poorly on wide datapaths such as multipliers, where the engine runs "
        "out of memory instead of returning an answer.",
        "The practical point: writing assertions for simulation costs nothing extra and gives "
        "you a formal testbench for free if you later get a tool.",
    ])
    w.h3("Clock domain crossings")
    w.callout("Simulation alone cannot verify a clock crossing",
              [[N("A simulator has no model of metastability. It resolves every flip-flop to a "
                  "clean 0 or 1, so a design with a genuinely broken crossing simulates "
                  "perfectly and fails intermittently in the lab.")],
               [B("Two flip-flops and none simulate identically."),
                N("  A multi-bit bus crossing without a handshake simulates with all bits "
                  "arriving together, which is exactly what does not happen on silicon.")],
               [N("CDC is therefore verified STRUCTURALLY: a dedicated checker reads the netlist, "
                  "finds every path between unrelated clocks, and demands a recognised "
                  "synchroniser on each. Review the crossings by eye as well.")]],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 2.16
    w.h2("2.16  Making a testbench reusable")
    w.code([
        "`ifndef DUT",
        "  `define DUT fifo",
        "`endif",
        "`DUT #(.W(W), .DEPTH(DEPTH)) u_dut ( .clk(clk), .rst_n(rst_n), ... );",
        "",
        "iverilog -DDUT=fifo_b3 -DDUTNAME=\\\"fifo_b3\\\" rtl/*.v tb/tb_v3_random.v",
        "xvlog    -d DUT=fifo_b3 ...                     # Vivado",
        "vlog     +define+DUT=fifo_b3 ...                # ModelSim",
    ], caption="How one testbench runs against six designs")
    w.numbered([
        "Parameterise everything the DUT parameterises, and derive nothing by hand.",
        "Keep the layers separate — a new DUT usually needs a new driver only.",
        "Never reach inside the DUT from the scoreboard.",
        "Select the DUT with a `define, so the same testbench can be pointed at a broken copy "
        "for a clinic, or at a second implementation for an equivalence check.",
    ])
