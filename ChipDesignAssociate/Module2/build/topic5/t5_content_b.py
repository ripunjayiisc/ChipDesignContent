# -*- coding: utf-8 -*-
"""Topic 5 deck — 5b: test benches and testbench development."""
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
    # =============================================== SECTION 5B
    d.section_slide("SUBTOPIC 5B", "Introduction to Test Benches and Testbench Development",
                    "Built up in six stages, each one measured against five broken designs.",
                    ["The six parts every testbench has, and the DUT under test",
                     "Clock, reset, and when to drive and when to sample",
                     "Reference models and scoreboards",
                     "Constrained-random stimulus, seeds and regressions",
                     "Functional coverage, and closing it",
                     "Assertions, and a layered testbench environment"],
                    accent=GREEN)

    # ============================================================ the DUT
    s = d.slide("TOPIC 5B · THE DUT", "One Design, Six Testbenches — Meet the FIFO")
    y = d.lead(s, TOP, [[
        R("Everything in 5b is built against a single device under test. ", b=True, c=NAVY,
          s=12.5),
        R("A small synchronous FIFO — big enough to have interesting corners, small enough to "
          "hold in your head. Its header comment IS the specification your testbench checks.")]],
        h=594360)
    y = d.code(s, y + 45720, [
        C("//  * A write is accepted when wr_en=1 and full=0. A write while FULL is IGNORED", c=CMT),
        C("//    and must not corrupt anything.", c=CMT),
        C("//  * A read is accepted when rd_en=1 and empty=0. A read while EMPTY is IGNORED.", c=CMT),
        C("//  * rd_data shows the OLDEST unread word at all times (first-word fall-through).", c=CMT),
        C("//  * count is the number of words stored, 0..DEPTH.", c=CMT),
        C("//  * empty <=> count==0.   full <=> count==DEPTH.", c=CMT),
        C("//  * Words come out in the ORDER they went in. None is lost or duplicated.", c=CMT),
        C("//  * Asynchronous active-low reset empties the FIFO.", c=CMT),
    ], size=10, title="Topic5_Lab/rtl/fifo.v — the interface contract")
    d.cols(s, y + G, [
        ("Every line of that comment becomes a check",
         [[R("There are eight bullets. A finished testbench has a check for each one, and a "
             "coverage bin proving the situation actually arose. That mapping — spec bullet to "
             "check to bin — is the whole verification plan.", s=10.5)]], TEAL, CARD),
        ("And five broken copies",
         [[R("Topic5_Lab/rtl/fifo_bugs.v", f=MONO_FONT, b=True, c=RED, s=10.5),
           R("  holds five variants with one realistic bug each. They all lint clean, all "
             "synthesise, and all pass a naive testbench. Do not read the bug list before "
             "attempting the clinic.", s=10.5)]], RED, CARD_R)], h=1234440)

    # ============================================================ anatomy
    s = d.slide("TOPIC 5B · ANATOMY", "The Six Parts of Every Testbench")
    y = d.lead(s, TOP, [[
        R("A testbench is a module with no ports. ", b=True, c=NAVY, s=12.5),
        R("It is never synthesised, so the entire language is available — and every testbench "
          "you will ever write has these six parts, whatever the design.")]], h=548640)
    y = d.image(s, y + 45720, "tb_anatomy", 3474720)
    d.card(s, y + G, "Missing part 6 is the commonest omission",
           [[R("A testbench that never calls "), R("$finish", f=MONO_FONT, b=True, c=NAVY),
             R(" runs until somebody kills it, which in a regression means the whole run hangs. "
               "Add a watchdog too: a second initial block that prints FAIL and finishes after "
               "a generous timeout, so a hung DUT FAILS rather than stalling the regression.")]],
           accent=AMBER, fill=CARD_A, h=960120)

    # ============================================================ V1
    s = d.slide("TOPIC 5B · LAB V1", "The Testbench Everybody Writes First")
    y = d.code(s, TOP, [
        "module tb_v1_naive;",
        "  fifo #(.W(8), .DEPTH(8)) u_dut (.clk(clk), .rst_n(rst_n), ...);   // 1. instantiate",
        "",
        C("  // 2. ONE place that decides pass or fail", c=CMT),
        "  task check(input [7:0] got, input [7:0] exp, input [255:0] msg);",
        "    if (got !== exp) begin",
        "      $display(\"FAIL %0t : %0s  got %h expected %h\", $time, msg, got, exp);",
        "      errors = errors + 1;",
        "    end",
        "  endtask",
        "",
        "  initial begin",
        "    $dumpfile(\"v1.vcd\");  $dumpvars(0, tb_v1_naive);          // 3. waveform dump",
        "    rst_n = 1'b0; repeat (3) @(posedge clk); #1 rst_n = 1'b1;  // reset, released",
        "                                                              //   BETWEEN edges",
        "    push(8'hA1); push(8'hB2); push(8'hC3);                    // 4. stimulus",
        "    pop(got); check(got, 8'hA1, \"first word out\");            //    and checks",
        "    pop(got); check(got, 8'hB2, \"second word out\");",
        "    pop(got); check(got, 8'hC3, \"third word out\");",
        "",
        "    if (errors == 0) $display(\"PASS - 3 words in, 3 words out\");  // 5. verdict",
        "    $finish;                                                       // 6. stop",
        "  end",
        "endmodule",
    ], size=9, title="Topic5_Lab/tb/tb_v1_naive.v — all six parts, and it does check its results")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("This is not a bad testbench. It has every structural part, and it decides pass or "
          "fail without a human. It is still worth ", s=10.5),
        R("nothing", b=True, i=True, c=RED, s=10.5),
        R(" — and the next slide says why.", s=10.5)]])

    # ============================================================ V1 result
    s = d.slide("TOPIC 5B · LAB V1", "…and It Passes on Every Broken Design", RED)
    y = d.lead(s, TOP, [[
        R("Run that testbench against the golden FIFO and against all five broken ones. ",
          b=True, c=NAVY, s=12.5),
        R("This is real output.")]], h=457200)
    y = d.code(s, y + 45720, [
        C("$ ./scripts/clinic.sh", c=TEAL),
        "",
        "  V1 naive directed      pass      pass      pass      pass      pass      pass",
        "                         fifo      fifo_b1   fifo_b2   fifo_b3   fifo_b4   fifo_b5",
        "",
        "  V1 : 0 of 5 bugs caught, golden design passes (no false alarm)",
    ], size=10, accent=RED, title="Verified output")
    y = d.card(s, y + G, "Why it misses everything",
           [[R("It never fills the FIFO. It never empties it past zero. It never asserts read "
               "and write on the same cycle. It never wraps the pointers. It never attempts a "
               "write while full or a read while empty.")],
            [R("Three words in and three words out exercises the one path where a broken FIFO "
               "and a correct FIFO behave identically. ", b=True, c=RED),
             R("The bugs are all at the boundaries — which is where bugs generally are.")]],
           accent=RED, fill=CARD_R, h=1188720)
    d.card(s, y + G, "The lesson to state explicitly",
           [[R("Coverage of the SPECIFICATION, not volume of stimulus, is what makes a "
               "testbench worth having.", b=True, c=NAVY)]],
           accent=NAVY, h=685800)

    # ============================================================ timing
    s = d.slide("TOPIC 5B · TIMING", "When to Drive and When to Sample")
    y = d.lead(s, TOP, [[
        R("More 'the design is broken' reports come from this than from any other cause. ",
          b=True, c=NAVY, s=12.5),
        R("If you change an input at the same instant as the clock edge, you have created a "
          "race — and which value the DUT sees is not defined.")]], h=594360)
    y = d.image(s, y + 45720, "stimulus_timing", 3383280)
    d.card(s, y + G, "Two real examples from these labs",
           [[R("Topic 4: ", b=True, c=AMBER),
             R("an edge-detector test failed because the stimulus changed mid-cycle, so the "
               "pulse was half a cycle wide and the check sampled at the wrong moment.")],
            [R("Topic 4: ", b=True, c=AMBER),
             R("an FSM testbench released reset exactly ON a clock edge; the state register saw "
               "an ambiguous condition and stayed x for two cycles, and the sequence detector "
               "found one match instead of two. Neither design was broken.")]],
           accent=AMBER, fill=CARD_A, h=1051560)

    # ============================================================ ref model
    s = d.slide("TOPIC 5B · REFERENCE MODEL", "The Step That Changes Everything")
    y = d.lead(s, TOP, [[
        R("Hand-written expected values do not scale past about twenty cases. ", b=True,
          c=NAVY, s=12.5),
        R("A reference model is a second, independent implementation of the specification — "
          "usually far simpler than the RTL, because it need not be efficient or synthesisable.")]],
        h=594360)
    y = d.image(s, y + 45720, "refmodel", 3291840)
    y = d.code(s, y + G, [
        C("// The FIFO's model: an array and two indices. That is all it needs to be.", c=CMT),
        "reg [W-1:0] model [0:DEPTH-1];",
        "integer     mhead, mtail;             // mtail - mhead is the occupancy",
        "function [$clog2(DEPTH):0] mcount; input dummy; mcount = mtail - mhead; endfunction",
    ], size=9.5, title="Topic5_Lab/tb/tb_v2_selfcheck.v")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Once the model exists you can compare EVERY cycle — count, empty, full and the "
          "output word — instead of only at the points where you happened to write a check.",
          s=10.5, i=True, c=SLATE)]])

    # ============================================================ model bug
    s = d.slide("TOPIC 5B · CASE STUDY", "A Real Bug — in the Reference Model", RED)
    y = d.lead(s, TOP, [[
        R("The model is code, and code has bugs. ", b=True, c=NAVY, s=12.5),
        R("This one was found while writing this lab, and it is the most instructive failure in "
          "the whole topic: the CORRECT FIFO failed, and a BROKEN one passed.")]], h=594360)
    y = d.image(s, y + 45720, "model_order_bug", 3566160)
    d.card(s, y + G, "The general rule this teaches",
           [[R("A model must make its decisions from the same state the hardware does. ",
               b=True, c=GREEN),
             R("Hardware evaluates every enable from the state that existed BEFORE the clock "
               "edge, all at once. A model that applies one operation and then tests its own "
               "updated state is modelling something the hardware never does. Sample first; "
               "then apply.")]],
           accent=GREEN, fill=CARD_G, h=960120)

    # ============================================================ V2 result
    s = d.slide("TOPIC 5B · LAB V2", "Model Plus Corners — 4 of 5")
    y = d.lead(s, TOP, [[
        R("V2 adds two things to V1: the reference model, and the boundary cases. ",
          b=True, c=NAVY, s=12.5),
        R("It is not a longer test — it is a better-chosen one.")]], h=502920)
    y = d.code(s, y + 45720, [
        "T1  state immediately after reset",
        "T2  fill to exactly full            -> full must assert, empty must not",
        "T3  a write WHILE FULL              -> must be ignored, occupancy unchanged",
        "T4  drain to exactly empty          -> empty must assert, full must not",
        "T5  a read WHILE EMPTY              -> must be ignored, occupancy unchanged",
        "T6  read and write on the SAME cycle, held half full",
        "T7  keep going long enough to WRAP the pointers",
        "T8  final drain, and the FIFO must end empty",
    ], size=10, title="The eight directed tests in tb_v2_selfcheck.v")
    y = d.code(s, y + G, [
        C("$ ./scripts/clinic.sh", c=TEAL),
        "  V2 model + corners     pass     CAUGHT   CAUGHT   CAUGHT   CAUGHT   pass",
        "  V2 : 4 of 5 bugs caught, golden design passes (no false alarm)",
    ], size=10, accent=GREEN)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Four bugs, from eight well-chosen directed tests and a model. Nothing exotic — just "
          "the boundaries, checked against something that knows the right answer.", s=10.5,
          i=True, c=SLATE)]])

    # ============================================================ random
    s = d.slide("TOPIC 5B · RANDOM", "The Constraints ARE the Test")
    y = d.lead(s, TOP, [[
        R("Constrained-random does not mean 'random'. ", b=True, c=NAVY, s=12.5),
        R("You still decide what the test does — you just express it as weights and let the "
          "generator produce the sequences. Change the weights and you are testing a different "
          "part of the design.")]], h=594360)
    y = d.image(s, y + 45720, "random_weights", 3474720)
    d.code(s, y + G, [
        "do_w = (({$random(seed)} % 100) < p_wr);      // p_wr and p_rd are the CONSTRAINTS",
        "do_r = (({$random(seed)} % 100) < p_rd);",
        "d    = $random(seed);",
    ], size=9.5, title="Topic5_Lab/tb/tb_v3_random.v — three lines of generator")

    # ============================================================ seeds
    s = d.slide("TOPIC 5B · SEEDS", "Reproducibility Is What Makes Random Usable")
    y = d.lead(s, TOP, [[
        R("A random failure you cannot reproduce is not a bug report — it is a rumour. ",
          b=True, c=NAVY, s=12.5),
        R("The seed makes every run deterministic, so any failure can be replayed exactly, with "
          "waveforms this time.")]], h=548640)
    y = d.image(s, y + 45720, "seed_repro", 2560320)
    y = d.code(s, y + G, [
        C("$ ./scripts/regress.sh 4        # 4 seeds x 3 profiles", c=TEAL),
        "  profile        seed     cycles   result",
        "  balanced       1        3000     pass",
        "  balanced       2        3000     pass",
        "  write-heavy    1        3000     pass",
        "  read-heavy     1        3000     pass",
        "  ...",
        "  12 passed, 0 failed",
        "  REGRESSION CLEAN",
    ], size=9, title="Verified output")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Two traps: ", s=10.5, b=True, c=RED),
        R("$random(seed)", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" UPDATES seed in place, so save the original before the loop if you want to print "
          "it; and in SystemVerilog ", s=10.5),
        R("$urandom(seed)", f=MONO_FONT, b=True, c=RED, s=10.5),
        R(" RE-SEEDS on every call — seed once, then call ", s=10.5),
        R("$urandom()", f=MONO_FONT, b=True, c=GREEN, s=10.5), R(" with no argument.", s=10.5)]])

    # ============================================================ V3 result
    s = d.slide("TOPIC 5B · LAB V3", "Constrained-Random — 5 of 5")
    y = d.code(s, TOP, [
        C("$ ./scripts/clinic.sh", c=TEAL),
        "",
        "  testbench               fifo      fifo_b1   fifo_b2   fifo_b3   fifo_b4   fifo_b5",
        "  ---------------------------------------------------------------------------------",
        "  V1 naive directed       pass      pass      pass      pass      pass      pass",
        "  V2 model + corners      pass      CAUGHT    CAUGHT    CAUGHT    CAUGHT    pass",
        "  V3 constrained-random   pass      CAUGHT    CAUGHT    CAUGHT    CAUGHT    CAUGHT",
        "",
        "  V1 : 0 of 5 bugs caught, golden design passes (no false alarm)",
        "  V2 : 4 of 5 bugs caught, golden design passes (no false alarm)",
        "  V3 : 5 of 5 bugs caught, golden design passes (no false alarm)",
    ], size=10, title="The full clinic result — verified")
    y = d.card(s, y + G, "What the fifth bug was, and why only random found it",
           [[R("fifo_b5", f=MONO_FONT, b=True, c=RED),
             R(" drops a write when wr_en and rd_en are asserted together while the FIFO is "
               "EMPTY. That is a legal, sensible combination — and no directed test in V2 ever "
               "produces it, because nobody thinks to write \"read and write at once, from an "
               "empty FIFO\" as a test case.")],
            [R("The random generator produced it ten times in three thousand cycles without "
               "being asked. ", b=True, c=GREEN),
             R("That is the entire argument for constrained-random stimulus.")]],
           accent=GREEN, fill=CARD_G, h=1188720)
    d.card(s, y + G, "And note the first column",
           [[R("Every testbench passes on the golden design. A checker that fires on correct "
               "hardware is worse than no checker — the team learns to ignore it.")]],
           accent=NAVY, h=685800)

    # ============================================================ coverage model
    s = d.slide("TOPIC 5B · COVERAGE", "Writing a Coverage Model by Hand")
    y = d.lead(s, TOP, [[
        R("SystemVerilog has covergroups. Plain Verilog does not — so you write one counter per "
          "interesting situation. ", b=True, c=NAVY, s=12.5),
        R("Doing it by hand once is the best way to understand what the tool does for you "
          "later.")]], h=594360)
    y = d.code(s, y + 45720, [
        C("// THE COVERAGE MODEL. Write this list BEFORE the stimulus.", c=CMT),
        "//   0  write accepted            6  occupancy reached DEPTH (full)",
        "//   1  read accepted             7  occupancy reached 0 (empty)",
        "//   2  read+write same cycle     8  pointers wrapped at least once",
        "//   3  idle cycle                9  write attempted while full",
        "//   4  read+write while EMPTY   10  read attempted while empty",
        "//   5  read+write while FULL    11  a full -> empty -> full round trip",
        "",
        "if (do_w && !was_full)         cov[0] = cov[0] + 1;      // sample, every cycle",
        "if (do_w && do_r && was_empty) cov[4] = cov[4] + 1;",
    ], size=9.5, title="Topic5_Lab/tb/tb_v4_coverage.v")
    d.card(s, y + G, "Bin 11 is the one worth pointing at",
           [[R("\"full → empty → full\" is not a state; it is a SEQUENCE over time, and it "
               "needs a little state machine in the testbench to detect. Real coverage models "
               "are full of these — 'a request followed by a retry', 'back-to-back bursts', "
               "'reset in the middle of a transfer'. They are also where the interesting bugs "
               "live.")]],
           accent=TEAL, h=960120)

    # ============================================================ coverage result
    s = d.slide("TOPIC 5B · LAB V4", "Coverage Holes, and Closing Them")
    y = d.lead(s, TOP, [[
        R("Here is the result that surprises students: a run can PASS and still prove almost "
          "nothing. ", b=True, c=NAVY, s=12.5),
        R("The write-heavy profile passes cleanly — and never reaches empty at all.")]],
        h=548640)
    y = d.image(s, y + 45720, "cov_bins", 3566160)
    d.card(s, y + G, "This is what closure looks like in practice",
           [[R("No single profile closes coverage, and none has to. Each run contributes what "
               "it reached, the results are MERGED across the regression, and what is still "
               "missing is the specification for the next test you write. "),
             R("./scripts/coverage.sh", f=MONO_FONT, b=True, c=GREEN),
             R(" does exactly this and prints COVERAGE CLOSED.")]],
           accent=GREEN, fill=CARD_G, h=960120)

    # ============================================================ assertions
    s = d.slide("TOPIC 5B · ASSERTIONS", "Stating the Rule Instead of Checking the Output")
    y = d.lead(s, TOP, [[
        R("A scoreboard checks the outputs at the points you compare them. ", b=True, c=NAVY,
          s=12.5),
        R("An assertion states a RULE, and the simulator checks it on every clock edge of every "
          "test, for ever — and reports at the exact cycle and the exact line where it broke.")]],
        h=594360)
    y = d.image(s, y + 45720, "assertion_anatomy", 3200400)
    d.cols(s, y + G, [
        ("assert versus cover",
         [[R("assert property", f=MONO_FONT, b=True, c=VIOLET, s=10.5),
           R("  — this must ALWAYS be true; fail loudly if not.", s=10.5)],
          [R("cover property", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  — this is not a rule, just RECORD whether it ever happened. That is functional "
             "coverage, expressed in the same language.", s=10.5)]], VIOLET, CARD),
        ("Where to put them",
         [[R("In a separate module bound to the DUT's signals — as in "),
           R("sva/fifo_sva.sv", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(". The design source stays clean, the assertions can be maintained by the "
             "verification engineer, and they can be switched off for synthesis without "
             "touching the RTL.", s=10.5)]], GREEN, CARD_G)], h=1325880)

    # ============================================================ SVA code
    s = d.slide("TOPIC 5B · ASSERTIONS", "The FIFO's Specification, Written as Properties")
    y = d.code(s, TOP, [
        C("// 1. count and the flags must always agree", c=CMT),
        "a_empty_iff_zero: assert property (@(posedge clk) disable iff (!rst_n)",
        "    empty == (count == 0))       else $error(\"empty=%0b but count=%0d\", empty, count);",
        "",
        "a_full_iff_depth: assert property (@(posedge clk) disable iff (!rst_n)",
        "    full == (count == DEPTH_C))  else $error(\"full=%0b but count=%0d\", full, count);",
        "",
        C("// 2. occupancy may only move by one per cycle, in the right direction", c=CMT),
        "a_step_up:   assert property (@(posedge clk) disable iff (!rst_n)",
        "    (wr_en && !full && !(rd_en && !empty)) |=> (count == $past(count) + 1));",
        "",
        "a_step_both: assert property (@(posedge clk) disable iff (!rst_n)",
        "    (wr_en && !full && rd_en && !empty)    |=> (count == $past(count)));",
        "",
        C("// 3. COVER: not checks. They record that the interesting situations HAPPENED.", c=CMT),
        "c_both_empty: cover property (@(posedge clk) disable iff (!rst_n)",
        "    wr_en && rd_en && empty);",
    ], size=9, title="Topic5_Lab/sva/fifo_sva.sv — lint-clean under Verilator 5.020")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Read the property names aloud and they are the specification: "
          "\"empty if and only if count is zero\", \"a write steps the count up by one\". "
          "That readability is the point — an assertion nobody can read is an assertion nobody "
          "will maintain.", s=10.5, i=True, c=SLATE)]])

    # ============================================================ assert result
    s = d.slide("TOPIC 5B · LAB V6", "Which Caught Which — and the One That Slipped Through")
    y = d.lead(s, TOP, [[
        R("Assertions and scoreboards are not alternatives. ", b=True, c=NAVY, s=12.5),
        R("Here is the measured proof, from the same five broken FIFOs.")]], h=502920)
    y = d.image(s, y + 45720, "assert_vs_scoreboard", 3566160)
    d.card(s, y + G, "Read the fourth row to the class twice",
           [[R("Four bugs are caught by a NAMED assertion, at the exact cycle, with a message "
               "that says which rule broke. One is not caught by any assertion — because these "
               "assertions describe the CONTROL interface and that bug corrupts DATA. "),
             R("Assertions catch what you described; scoreboards catch what you compared.",
               b=True, c=AMBER),
             R(" You need both, and neither is a substitute for the other.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ============================================================ layered
    s = d.slide("TOPIC 5B · ARCHITECTURE", "A Layered Testbench")
    y = d.lead(s, TOP, [[
        R("A flat testbench works for one design. ", b=True, c=NAVY, s=12.5),
        R("A layered one survives contact with the second, because the part that decides WHAT "
          "to test is separate from the part that knows HOW to wiggle the pins.")]], h=548640)
    y = d.image(s, y + 45720, "tb_layers", 3383280)
    d.table(s, y + G,
            ["Layer", "Knows about", "Does NOT know about"],
            [["Generator", "the test intent — what scenarios matter", "pins, timing, the DUT"],
             ["Driver", "the pin-level protocol and its timing", "why this transaction was chosen"],
             ["Monitor", "how to observe the pins", "how to drive anything"],
             ["Scoreboard", "what 'correct' means", "pins, timing, protocol"]],
            [2011680, 4754880, 4480560], rh=283464, bold_cols=(0,), size=10)

    # ============================================================ V6
    s = d.slide("TOPIC 5B · LAB V6", "The Capstone Testbench")
    y = d.code(s, TOP, [
        C("// LAYER 3: monitor -- watches the pins and tells the scoreboard what happened.", c=CMT),
        "task automatic mon_apply(bit did_wr, bit did_rd, logic [W-1:0] dat);",
        "  bit was_full  = m_full();          // sample BOTH before applying either",
        "  bit was_empty = m_empty();",
        "  if (did_wr && !was_full)  begin model[mtail % DEPTH] = dat; mtail++; end",
        "  if (did_rd && !was_empty) begin mhead++;                          end",
        "endtask",
        "",
        C("// LAYER 2: driver -- knows the pin protocol and nothing else.", c=CMT),
        "task automatic drv_cycle(bit do_w, bit do_r, logic [W-1:0] dat, string where);",
        "  @(posedge clk); #1;  wr_en = do_w; rd_en = do_r; wr_data = dat;",
        "  @(posedge clk); #1;  wr_en = 1'b0; rd_en = 1'b0;",
        "  mon_apply(do_w, do_r, dat);",
        "  sb_check(where);",
        "endtask",
        "",
        C("// LAYER 1: generator -- corners first (cheap, deterministic), then random.", c=CMT),
        "for (int i = 0; i < DEPTH + 2; i++) drv_cycle(1'b1, 1'b0, 8'h10+i[7:0], \"fill\");",
        "drv_cycle(1'b1, 1'b1, 8'hAA, \"read+write while empty\");",
        "for (int i = 0; i < cycles; i++) begin",
        "  bit b_w = (($urandom() % 100) < p_wr);      // seeded ONCE, before the loop",
        "  bit b_r = (($urandom() % 100) < p_rd);",
        "  drv_cycle(b_w, b_r, W'($urandom()), \"random\");",
        "end",
    ], size=8.5, title="Topic5_Lab/tb/tb_v6_assert.sv — verified: 2027 checks, 895 words in, 895 out")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Directed corners first, then the random body. The corners fail fast and cheaply; "
          "the random body finds what the corners did not.", s=10.5, i=True, c=SLATE)]])

    # ============================================================ 5B checkpoint
    s = d.slide("TOPIC 5B · CHECKPOINT", "Build It Yourself — Eight Tasks")
    d.lead(s, TOP, [[
        R("These are the tasks that make the difference between reading about verification and "
          "being able to do it. ", b=True, c=NAVY, s=12.5),
        R("Full solutions in workbook section T5-B.")]], h=457200)
    y = d.cols(s, 1600200, [
        ("Tasks 1–4",
         [[R("1. Add a ninth directed test to V2 that V2 currently lacks. What does it check?",
             s=10.5)],
          [R("2. Change V3's weights so the FIFO spends most of its time empty. Which coverage "
             "bins go MISS?", s=10.5)],
          [R("3. Break the golden FIFO with a one-character change. Which stage catches it — "
             "V1, V2 or V3?", s=10.5)],
          [R("4. Write a bug that V3 misses. What kind of bug is it, and what would catch it?",
             s=10.5)]], TEAL, CARD),
        ("Tasks 5–8",
         [[R("5. Add a coverage bin for \"three consecutive idle cycles\". Does anything hit "
             "it?", s=10.5)],
          [R("6. Add an assertion that would have caught fifo_b4. Why is it harder than the "
             "others?", s=10.5)],
          [R("7. Comment out a_step_both and re-run assert.sh. What changes about fifo_b3's "
             "diagnosis?", s=10.5)],
          [R("8. Run the same seed twice and diff the transcripts. Then change the seed. "
             "Explain both results.", s=10.5)]], GREEN, CARD_G)], h=2103120)
    d.card(s, y + G, "Task 4 is the one that teaches the most",
           [[R("Writing a bug that survives a good testbench forces you to think about what the "
               "testbench does NOT check — which is exactly the skill a verification plan is "
               "supposed to produce.")]],
           accent=AMBER, fill=CARD_A, h=776224)
