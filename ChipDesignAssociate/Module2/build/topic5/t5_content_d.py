# -*- coding: utf-8 -*-
"""Topic 5 deck — 5b continued: advanced testbench development."""
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
    # ============================================================ tasks/fork
    s = d.slide("TOPIC 5B · MECHANICS", "Tasks, Functions and Concurrency in a Testbench")
    y = d.lead(s, TOP, [[
        R("A testbench is not synthesised, so the whole language is available — including "
          "everything Topic 4 told you never to use in design code. ", b=True, c=NAVY, s=12.5),
        R("Delays, while loops, file I/O, hierarchical references: all legal, all useful here.")]],
        h=502920)
    y = d.code(s, y + 45720, [
        C("// A TASK may consume time. This is how you package a bus transaction.", c=CMT),
        "task automatic push(input [W-1:0] dat);",
        "  begin",
        "    @(posedge clk); #1;  wr_en = 1'b1; wr_data = dat;",
        "    @(posedge clk); #1;  wr_en = 1'b0;",
        "  end",
        "endtask",
        "",
        C("// FORK/JOIN runs several stimulus threads at once - a writer and a reader,", c=CMT),
        C("// independent of each other, exactly as two masters on a bus would be.", c=CMT),
        "fork",
        "  begin : writer  repeat (100) push($random(seed));      end",
        "  begin : reader  repeat (100) pop();                    end",
        "join",
        "",
        C("// join_any + disable fork is the standard TIMEOUT idiom in SystemVerilog.", c=CMT),
    ], size=9, title="The testbench-only constructs you will actually use")
    d.cols(s, y + G, [
        ("automatic matters",
         [[R("task automatic", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  gives each call its own copy of the arguments and locals. Without it, two "
             "concurrent calls from a fork share one set — and corrupt each other in a way that "
             "looks like a DUT bug.", s=10.5)]], GREEN, CARD_G),
        ("A watchdog is not optional",
         [[R("Every testbench needs a second initial block that prints FAIL and calls $finish "
             "after a generous timeout. Without one, a hung DUT stalls the whole regression "
             "instead of failing it — and a regression that hangs is a regression nobody runs.",
             s=10.5)]], RED, CARD_R)], h=1188720)

    # ============================================================ file io
    s = d.slide("TOPIC 5B · FILE I/O", "Golden Vectors — When the Answer Comes From Elsewhere")
    y = d.lead(s, TOP, [[
        R("Sometimes the reference is not a model you write but a file somebody else produced ",
          b=True, c=NAVY, s=12.5),
        R("— a C reference implementation, a MATLAB run, the output of the previous chip. The "
          "testbench then reads stimulus and expected results from files.")]], h=502920)
    y = d.code(s, y + 45720, [
        "reg [7:0] stim   [0:1023];",
        "reg [7:0] golden [0:1023];",
        "integer   i, fd, errors;",
        "",
        "initial begin",
        "  $readmemh(\"vectors/stim.hex\",   stim);      // one hex value per line",
        "  $readmemh(\"vectors/golden.hex\", golden);",
        "  fd = $fopen(\"build/mismatch.log\", \"w\");     // and write our own report",
        "  for (i = 0; i < 1024; i = i + 1) begin",
        "    apply(stim[i]);",
        "    if (dut_out !== golden[i]) begin",
        "      $fdisplay(fd, \"%0d  sent %h  got %h  expected %h\", i, stim[i], dut_out, golden[i]);",
        "      errors = errors + 1;",
        "    end",
        "  end",
        "  $fclose(fd);",
        "end",
    ], size=9, title="$readmemh, $fopen, $fdisplay, $fclose")
    d.cols(s, y + G, [
        ("When golden vectors are the right answer",
         [[R("· A published standard with official test vectors (AES, CRC, a codec).", s=10.5)],
          [R("· A bit-exact C or MATLAB reference that already exists and is trusted.", s=10.5)],
          [R("· Regression against the PREVIOUS revision of the same block.", s=10.5)]],
         GREEN, CARD_G),
        ("And when they are not",
         [[R("· They fix the stimulus, so they cannot find the corner nobody generated.", s=10.5)],
          [R("· They rot: the file and the specification drift apart and nobody notices.",
             s=10.5)],
          [R("· A mismatch tells you WHICH vector failed, not which rule was broken.", s=10.5)]],
         AMBER, CARD_A)], h=1234440)

    # ============================================================ reusable tb
    s = d.slide("TOPIC 5B · REUSE", "A Testbench That Survives the Next Project")
    y = d.lead(s, TOP, [[
        R("The testbenches in this lab are parameterised the same way the design is. ",
          b=True, c=NAVY, s=12.5),
        R("Change W or DEPTH in one place and everything — stimulus, model, coverage bins — "
          "follows. That is not tidiness; it is what makes the testbench reusable at all.")]],
        h=594360)
    y = d.code(s, y + 45720, [
        C("// The DUT is selected by a `define, so ONE testbench runs against SIX designs.", c=CMT),
        "`ifndef DUT",
        "  `define DUT fifo",
        "`endif",
        "",
        "`DUT #(.W(W), .DEPTH(DEPTH)) u_dut ( .clk(clk), .rst_n(rst_n), ... );",
        "",
        C("// and on the command line:", c=CMT),
        "iverilog -DDUT=fifo_b3 -DDUTNAME=\\\"fifo_b3\\\" rtl/*.v tb/tb_v3_random.v",
        "xvlog    -d DUT=fifo_b3 ...                     # Vivado",
        "vlog     +define+DUT=fifo_b3 ...                # ModelSim",
    ], size=9.5, title="How the clinic runs one testbench against six designs")
    d.card(s, y + G, "Three habits that make a testbench outlive its design",
           [[R("1. Parameterise everything the DUT parameterises, and derive nothing by hand.")],
            [R("2. Keep the layers separate — a new DUT usually needs a new DRIVER only, and the "
               "generator, monitor and scoreboard survive unchanged.")],
            [R("3. Never reach inside the DUT from the scoreboard. A white-box check is fine for "
               "debugging and fatal for reuse: the moment the design is refactored, the "
               "testbench breaks and nobody can tell whether the design did too.")]],
           accent=TEAL, h=1234440)

    # ============================================================ DUT kinds
    s = d.slide("TOPIC 5B · BY DESIGN TYPE", "What to Check, for Each Kind of Block")
    d.lead(s, TOP, [[
        R("The six parts of a testbench are always the same. ", b=True, c=NAVY, s=12.5),
        R("What changes is what you check, and where the bugs hide.")]], h=411480)
    d.table(s, 1554480,
            ["Kind of DUT", "The checks that matter", "Where the bugs actually are"],
            [["Combinational", "exhaustive if the input space is small; otherwise random + a "
                               "reference function", "boundaries, sign, and width truncation"],
             ["Registered / pipelined", "output correct AND arriving at the right cycle; "
                                        "valid delayed with the data",
              "latency, and control not pipelined with the data"],
             ["Counter / timer", "wrap, load, enable priority, terminal count",
              "off-by-one at the wrap, and at the reload"],
             ["FSM", "every state entered, every arc taken, illegal states recovered from",
              "the arcs nobody drew, and the missing default"],
             ["Memory / FIFO", "order, occupancy, full, empty, simultaneous access",
              "the boundaries: full, empty, and both at once"],
             ["Protocol / bus", "handshake rules as assertions; a checker independent of the DUT",
              "the rule the other end violates, not the one you do"],
             ["CDC", "not by simulation alone — structural CDC checks and a Gray/handshake review",
              "multi-bit buses crossing without a handshake"]],
            [2377440, 4754880, 4114800], rh=411480, bold_cols=(0,), size=9,
            col_colors={0: NAVY})

    # ============================================================ SV features
    s = d.slide("TOPIC 5B · SYSTEMVERILOG", "What SystemVerilog Adds for Verification")
    y = d.lead(s, TOP, [[
        R("Verilog-2005 is enough to build everything in this lab, and doing it by hand once is "
          "worth the effort. ", b=True, c=NAVY, s=12.5),
        R("SystemVerilog then gives you the same things as language features — and you will "
          "meet them in every professional environment.")]], h=594360)
    y = d.table(s, y + 45720,
                ["SystemVerilog feature", "What it replaces in this lab", "Support"],
                [["logic", "the wire / reg decision", "everywhere"],
                 ["always_comb / always_ff", "always @(*) and the latch you inferred by mistake",
                  "everywhere"],
                 ["assert / cover property", "hand-written checks scattered through the code",
                  "vendor: full; open-source: a subset"],
                 ["covergroup / coverpoint / bins", "the twelve integer counters in Lab V4",
                  "vendor tools"],
                 ["rand / randc + constraint blocks", "the weighted $random in Lab V3",
                  "vendor tools"],
                 ["classes, mailboxes, semaphores", "the layers written as tasks in Lab V6",
                  "vendor tools"],
                 ["interface / modport", "the long port lists in every instantiation",
                  "vendor tools"],
                 ["queues, dynamic arrays, associative arrays",
                  "the fixed model array and its indices", "vendor tools"]],
                [3383280, 5486400, 2377440], rh=283464, bold_cols=(0,), size=9.5)
    d.card(s, y + G, "Why this lab is written in Verilog-2005",
           [[R("Because you learn what a covergroup IS by writing twelve counters once, and "
               "what a constraint IS by writing the weights yourself. ", b=True, c=NAVY),
             R("And because it then runs on every tool on every machine, including the ones your "
               "students have at home. Move to SystemVerilog as soon as your tool flow allows — "
               "but move to it understanding what it is doing for you.")]],
           accent=TEAL, h=960120)

    # ============================================================ SV random
    s = d.slide("TOPIC 5B · SYSTEMVERILOG", "Constraints, Written as Constraints")
    y = d.lead(s, TOP, [[
        R("In Verilog you weight a coin and hope. ", b=True, c=NAVY, s=12.5),
        R("In SystemVerilog you state the rules and a constraint solver generates values that "
          "satisfy them — which is a considerably more powerful thing.")]], h=548640)
    y = d.code(s, y + 45720, [
        "class fifo_txn;",
        "  rand bit        do_wr;",
        "  rand bit        do_rd;",
        "  rand bit [7:0]  data;",
        "",
        C("  // weights, expressed directly", c=CMT),
        "  constraint c_mix   { do_wr dist { 1 := 55, 0 := 45 };",
        "                       do_rd dist { 1 := 45, 0 := 55 }; }",
        "",
        C("  // and rules the generator must respect", c=CMT),
        "  constraint c_burst { (do_wr && do_rd) -> data inside {[8'h80:8'hFF]}; }",
        "endclass",
        "",
        "fifo_txn t = new();",
        "repeat (2000) begin",
        "  if (!t.randomize()) $fatal(1, \"constraints are unsatisfiable\");",
        "  drv_cycle(t.do_wr, t.do_rd, t.data);",
        "end",
    ], size=8.4, title="The same generator as Lab V3, expressed declaratively")
    d.cols(s, y + G, [
        ("What the solver buys you",
         [[R("· Constraints compose: add one and the others still hold.", s=10.5)],
          [R("· ", s=10.5), R("randomize() with { ... }", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R("  adds a temporary constraint at one call site — a directed test written as a "
             "narrowing of the random one.", s=10.5)]], GREEN, CARD_G),
        ("And the trap",
         [[R("An over-constrained set has no solution and ", s=10.5),
           R("randomize()", f=MONO_FONT, b=True, c=RED, s=10.5),
           R(" returns 0. If you ignore the return value the test silently drives the same "
             "unrandomised value for ever — and passes. Always check it, and always $fatal on "
             "failure.", s=10.5)]], RED, CARD_R)], h=1188720)

    # ============================================================ covergroups
    s = d.slide("TOPIC 5B · SYSTEMVERILOG", "Covergroups — the Same Twelve Bins, Declared")
    y = d.code(s, TOP, [
        "covergroup cg_fifo @(posedge clk);",
        "  cp_op : coverpoint {wr_en, rd_en} {",
        "            bins idle  = {2'b00};",
        "            bins wr    = {2'b10};",
        "            bins rd    = {2'b01};",
        "            bins both  = {2'b11};",
        "          }",
        "  cp_occ: coverpoint count {",
        "            bins empty = {0};",
        "            bins mid   = {[1:DEPTH-1]};",
        "            bins full  = {DEPTH};",
        "          }",
        C("  // the CROSS is where the real value is: read+write WHILE empty, and", c=CMT),
        C("  // read+write WHILE full, are cells of this cross - and both were bugs.", c=CMT),
        "  x_op_occ: cross cp_op, cp_occ;",
        "endgroup",
        "",
        "cg_fifo cg = new();          // sampled automatically on every posedge clk",
    ], size=8.4, title="Lab V4's coverage model, as a SystemVerilog covergroup")
    y = d.card(s, y + G, "The cross is the point",
           [[R("cp_op has 4 bins and cp_occ has 3, so the cross has 12 cells — and two of them, "
               "\"both while empty\" and \"both while full\", are exactly where two of the "
               "five planted bugs live. "),
             R("A cross says \"this situation, in that state\" in one line", b=True, c=GREEN),
             R(" — the combination hand-written counters make tedious, and that people skip.")]],
           accent=GREEN, fill=CARD_G, h=914400)
    d.card(s, y + G, "Coverage is reported and merged by the tool",
           [[R("vsim -coverage ; coverage report -details", f=MONO_FONT, b=True, c=NAVY),
             R("   and merged across a regression with "),
             R("vcover merge", f=MONO_FONT, b=True, c=NAVY),
             R(". That is the vendor equivalent of the awk merge in scripts/coverage.sh.")]],
           accent=TEAL, h=776224)

    # ============================================================ UVM
    s = d.slide("TOPIC 5B · UVM", "What UVM Is, and When It Is Worth It")
    y = d.lead(s, TOP, [[
        R("The Universal Verification Methodology is a SystemVerilog class library that "
          "standardises exactly the layers in Lab V6. ", b=True, c=NAVY, s=12.5),
        R("It is what most professional verification environments are built from — and it is "
          "considerable overhead for a small block.")]], h=594360)
    y = d.table(s, y + 45720,
                ["Lab V6 calls it", "UVM calls it", "What UVM adds"],
                [["generator", "uvm_sequence / uvm_sequencer",
                  "reusable, layered, randomisable sequences"],
                 ["driver", "uvm_driver", "a standard handshake with the sequencer"],
                 ["monitor", "uvm_monitor", "publishes transactions to any number of subscribers"],
                 ["scoreboard", "uvm_scoreboard", "standard comparison and reporting"],
                 ["(the whole thing)", "uvm_env / uvm_agent",
                  "a package you can instantiate twice, or reuse on the next project"],
                 ["$display", "uvm_info / uvm_error with verbosity", "filterable, gradable reporting"],
                 ["(nothing)", "the factory and config_db",
                  "swap a component or a setting without editing the environment"]],
                [3017520, 3931920, 4297680], rh=283464, bold_cols=(0,), size=9.5)
    d.cols(s, y + G, [
        ("Worth it when",
         [[R("· The block has a real protocol interface that other blocks also use.", s=10.5)],
          [R("· Several people work on the environment at once.", s=10.5)],
          [R("· The environment will be reused across projects, or at chip level.", s=10.5)]],
         GREEN, CARD_G),
        ("Not worth it when",
         [[R("· The block is a FIFO, and Lab V6 already verifies it in 160 lines.", s=10.5)],
          [R("· Nobody on the team has used UVM before and the schedule is four weeks.", s=10.5)],
          [R("· Your simulator licence does not include the class library.", s=10.5)]],
         AMBER, CARD_A)], h=1188720)

    # ============================================================ formal
    s = d.slide("TOPIC 5B · FORMAL", "Formal Verification — Proof Instead of Sampling")
    y = d.lead(s, TOP, [[
        R("Simulation samples the state space. Formal tools SEARCH it. ", b=True, c=NAVY,
          s=12.5),
        R("Given the same assertions you already wrote, a formal engine tries to prove no input "
          "sequence can ever violate them — or produces a counter-example waveform that does.")]],
        h=594360)
    y = d.tiers(s, y + 45720, [
        ("WHAT YOU GET", "For a property that is PROVEN, no amount of simulation adds anything: "
                         "it holds for every input sequence, for ever. For one that fails, you "
                         "get the shortest counter-example — usually far easier to understand "
                         "than a random failure at cycle 40 000.", GREEN),
        ("WHAT IT COSTS", "The state space can explode. Formal works beautifully on control "
                          "logic — FIFOs, arbiters, protocol adapters, CDC handshakes — and "
                          "poorly on wide datapaths such as multipliers, where the engine runs "
                          "out of memory rather than returning an answer.", AMBER),
        ("THE OVERLAP", "The assertions in sva/fifo_sva.sv are already formal properties. That "
                        "is the practical point: writing assertions for simulation costs you "
                        "nothing extra and gives you a formal testbench for free if you later "
                        "get access to a tool.", TEAL),
        ("WHERE IT IS USED", "Almost universally for connectivity checks, register maps, "
                             "clock-domain crossings, arbiters and cache coherence — and almost "
                             "never as a replacement for simulation at the system level.",
         VIOLET),
    ], h=822960, gap=45720)

    # ============================================================ CDC
    s = d.slide("TOPIC 5B · CDC", "Why Simulation Alone Cannot Verify a Clock Crossing", RED)
    y = d.lead(s, TOP, [[
        R("This is the most important limitation to state out loud. ", b=True, c=NAVY, s=12.5),
        R("A simulator has no model of metastability. It resolves every flip-flop to a clean 0 "
          "or 1, so a design with a genuinely broken clock crossing simulates perfectly and "
          "fails intermittently in the lab.")]], h=594360)
    y = d.cols(s, y + 45720, [
        ("What simulation WILL catch",
         [[R("· Functional errors in the handshake protocol itself.", s=10.5)],
          [R("· Data being sampled before it was stable, if you model the delay.", s=10.5)],
          [R("· A Gray-code pointer that is not actually Gray.", s=10.5)],
          [R("· With randomised clock phases, some — not all — sampling races.", s=10.5)]],
         TEAL, CARD),
        ("What it will NOT catch",
         [[R("· Metastability. There is no such value in the simulator.", s=10.5, b=True,
             c=RED)],
          [R("· A missing synchroniser: two flip-flops or none simulate identically.", s=10.5,
             b=True, c=RED)],
          [R("· A multi-bit bus crossing without a handshake — in simulation all the bits "
             "arrive together, which is exactly what does not happen on silicon.", s=10.5,
             b=True, c=RED)]], RED, CARD_R)], h=1554480)
    d.card(s, y + G, "So CDC is verified structurally, not dynamically",
           [[R("Every professional flow runs a dedicated CDC checker that reads the netlist, "
               "identifies every path between unrelated clocks, and demands a recognised "
               "synchroniser structure on each one. Review the crossings by eye as well: "),
             R("two flip-flops for a single-bit level, Gray coding or a handshake for a bus, "
               "and never bit-by-bit synchronisation of a vector.", b=True, c=GREEN)]],
           accent=GREEN, fill=CARD_G, h=960120)

    # ============================================================ metrics
    s = d.slide("TOPIC 5B · METRICS", "How a Project Decides Verification Is Finished")
    y = d.lead(s, TOP, [[
        R("\"We ran all the tests and they passed\" is not a sign-off criterion. ", b=True,
          c=NAVY, s=12.5),
        R("These are — and every one of them is a number somebody outside the team can read.")]],
        h=548640)
    y = d.table(s, y + 45720,
                ["Metric", "What it means", "Typical sign-off bar"],
                [["Functional coverage", "spec-level situations reached", "100% of the plan, "
                  "or every hole waived in writing"],
                 ["Code coverage", "lines, branches, conditions, toggles exercised",
                  "95–100%, with the rest explained"],
                 ["Assertion coverage", "each assertion actually evaluated, not vacuously true",
                  "every assertion hit at least once"],
                 ["Regression pass rate", "seeds passing over the last N runs",
                  "100%, sustained, not 'usually'"],
                 ["Bug discovery rate", "new bugs found per week",
                  "flattened, and staying flat"],
                 ["Bug severity trend", "are the new ones getting less serious?",
                  "no high-severity bugs for N weeks"]],
                [2926080, 4297680, 4023360], rh=329184, bold_cols=(0,), size=9.5)
    d.card(s, y + G, "The bug-rate curve is the one experienced teams watch",
           [[R("If you are still finding serious bugs at the same rate as last month, you are "
               "not near the end however good the coverage number looks. If the rate has "
               "flattened AND coverage is closed AND the regression is green, you have as much "
               "evidence as this method can give you.")]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ============================================================ mid checkpoint
    s = d.slide("TOPIC 5B · CHECKPOINT", "Six Questions on the Advanced Material")
    d.lead(s, TOP, [[
        R("Discussion questions — there is no code to type. ", b=True, c=NAVY, s=12.5),
        R("Answers in workbook section T5-B.")]], h=411480)
    y = d.cols(s, 1554480, [
        ("Questions 1–3",
         [[R("1. Your testbench uses golden vectors from a trusted C model and every vector "
             "passes. Name two classes of bug this cannot find.", s=10.5)],
          [R("2. Why does a scoreboard that reads the DUT's internal pointers make the "
             "testbench worse, even though it makes debugging easier?", s=10.5)],
          [R("3. A cross of a 4-bin and a 3-bin coverpoint has 12 cells, and two of them are "
             "impossible by construction. What do you do about them?", s=10.5)]], TEAL, CARD),
        ("Questions 4–6",
         [[R("4. randomize() returns 0 and the test still passes. Explain how, and what you "
             "should have written.", s=10.5)],
          [R("5. A design with no synchroniser at all simulates perfectly. Why, and what "
             "actually catches it?", s=10.5)],
          [R("6. Coverage is 100% and the regression is green, but the team is still finding "
             "two serious bugs a week. Are you finished? What does that tell you?", s=10.5)]],
         GREEN, CARD_G)], h=2286000)
    d.card(s, y + G, "Question 6 is the one to spend time on",
           [[R("It is the difference between measuring what you tested and knowing whether the "
               "measurement was the right one. A closed coverage model that misses a whole "
               "category of behaviour reports 100% and means nothing — which is why the "
               "verification plan is reviewed by somebody other than its author.")]],
           accent=AMBER, fill=CARD_A, h=776224)
