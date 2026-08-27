# -*- coding: utf-8 -*-
"""Topic 6 workbook — Part 7: seven guided tutorials at the keyboard."""
import _boot
from wbkit import *
from t6_wb1 import B, N, I, M


def build(w):
    w.h1("Part 7 · Seven Guided Tutorials")

    w.callout("Before you start", [
        [N("Install tier 1 (Part 6.2) and open a terminal in "), M("Topic6_Lab/"),
         N(". Type the commands; do not copy and paste them. The point of a tutorial is "
           "the twenty seconds between typing something and understanding why it did what "
           "it did.")],
        [N("Each tutorial ends with a "), B("Checkpoint"),
         N(" — a specific output you should see. If you do not see it, stop and find out "
           "why before moving on. The tutorials build on each other.")],
    ], color=NAVY, bar="0E2A47")

    w.image("lab_map", width=6.5)

    # ------------------------------------------------------------ T1
    w.h2("Tutorial 1 · The delay model  (2 hours)")

    w.para([N("You cannot analyse timing without numbers for each cell, and you cannot "
              "trust an analysis whose numbers you have never seen. So the first thing you "
              "build is the library.")])

    w.h3("Step 1 — look at what a Liberty file is")
    w.code([
        "$ cd Topic6_Lab",
        "$ head -40 lib/cda_edu.lib"])

    w.para([N("It is a nested, brace-delimited format. Each "), M("cell (NAME) { ... }"),
            N(" block describes one standard cell. Real foundry libraries use the same "
              "syntax and run to tens of megabytes; this one is 191 lines and describes "
              "14 cells.")])

    w.h3("Step 2 — read the model")
    w.code([
        "cell (XOR2) {",
        "    area              : 4.0 ;",
        "    cda_intrinsic     : 0.088 ;   /* ns, unloaded                          */",
        "    cda_load_factor   : 0.018 ;   /* ns per unit of capacitance on Y       */",
        "    cda_input_cap     : 1.5 ;     /* what this cell presents to its driver */",
        "    pin (Y) { direction : output ; function : \"(A^B)\" ; }",
        "}"])
    w.para([N("The delay of any cell is "), M("intrinsic + load_factor × output_load"),
            N(", where the output load is the sum of the input capacitances of everything "
              "the cell drives. Three numbers per cell; that is the entire model.")])

    w.h3("Step 3 — run the reader")
    w.code([
        "$ make lib",
        "",
        "14 cells read from cda_edu.lib",
        "",
        "cell      type  intrinsic   load/ld    clk->Q     setup    cap",
        "------------------------------------------------------------------",
        "AND2      comb      0.053     0.012         -         -   1.20",
        "DFF       FF        0.000     0.013     0.145     0.090   1.60",
        "INV       comb      0.021     0.012         -         -   1.00",
        "XOR2      comb      0.088     0.018         -         -   1.50",
        "...  (14 rows)"])

    w.h3("Step 4 — do the arithmetic yourself")
    w.para([N("An INV drives two XOR2 inputs. What is its delay?")])
    w.code([
        "load  =  1.5 + 1.5  =  3.0",
        "delay =  0.021  +  0.012 x 3.0   =   0.057 ns"])
    w.para([N("Now the same INV driving eight XOR2 inputs: load 12.0, delay 0.165 ns — "
              "nearly three times as slow. That is fanout, and it is why "),
            M("set_max_fanout"), N(" exists.")])

    w.callout("Checkpoint 1", [
        [M("make lib"), N(" prints a 14-row table. You can state, for any cell in it, what "
           "its delay would be driving three DFF inputs — and check your answer against "
           "the formula.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T2
    w.h2("Tutorial 2 · The timing graph  (3 hours)")

    w.h3("Step 1 — look at the design")
    w.code([
        "$ cat rtl/tiny.v",
        "",
        "module tiny (input clk, input din, output q);",
        "    reg p, r, qq;",
        "    always @(posedge clk) begin",
        "        p  <= din;",
        "        r  <= din;",
        "        qq <= p ^ r;      // one XOR between two flops - hand-checkable",
        "    end",
        "    assign q = qq;",
        "endmodule"])

    w.h3("Step 2 — synthesise it and look at the netlist")
    w.code([
        "$ ./scripts/synth.sh tiny",
        "$ python3 -c \"import json;d=json.load(open('build/tiny.json'));\\",
        "  print(list(d['modules']['tiny']['cells'].keys()))\"",
        "",
        "['$auto$ff.cc:266:slice$89', '$abc$95$auto$blifparse.cc:...$97', ...]"])

    w.callout("Yosys names are unreadable, and that is a real problem", [
        [N("A report full of "), M("$abc$95$auto$blifparse.cc:492:parse_blif$97/Y"),
         N(" is a report nobody reads. The engine has a "), M("short()"),
         N(" function that turns those into "), M("u97/Y"),
         N(", and recovers register names from the JSON "), M("netnames"),
         N(" section so a flop appears as "), M("q_reg"), N(" rather than a hash. "
           "Making a tool's output legible is not cosmetic work — an unreadable report "
           "does not get read, and a report that does not get read finds no bugs.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h3("Step 3 — build the graph, and get the arcs right")
    w.image("timing_graph", width=6.3)
    w.para([N("One node per pin. For each cell, one arc from every input pin to every "
              "output pin, carrying the cell's delay computed with the load on that output "
              "net. For each net, arcs from the driver to every load, carrying zero. For a "
              "flip-flop, the clock-to-Q delay is charged at the Q pin.")])

    w.h3("Step 4 — draw it on paper first")
    w.para([N("Before running anything, draw the graph for tiny.v by hand. Three flops, "
              "one XOR, one output port. Count the nodes; count the arcs. Then run the "
              "engine and compare.")])
    w.code([
        "$ python3 sta/sta.py build/tiny.json tiny -p 1.0 --paths 1"])

    w.callout("Checkpoint 2", [
        [N("Your hand-drawn graph and the engine's agree on the number of nodes and the "
           "number of arcs, and you can point at the arc that carries the XOR's delay and "
           "say which net's load was used to compute it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T3
    w.h2("Tutorial 3 · Arrival, required, slack  (4 hours)")

    w.para([N("This is the tutorial the whole topic exists for. When you finish it you "
              "will have written a static timing analyser, and no vendor's timing report "
              "will ever be a black box again.")])

    w.h3("Step 1 — the forward sweep")
    w.code([
        "def propagate(self):",
        "    for n in self._order():                     # topological order",
        "        for arc in n.fanin:",
        "            src, dly = arc.src, arc.delay",
        "            n.amax = max(n.amax, src.amax + dly)     # LATEST   -> setup",
        "            n.amin = min(n.amin, src.amin + dly)     # EARLIEST -> hold"])
    w.para([N("Two numbers per node, not one. Keep only the max and your hold analysis is "
              "silently wrong.")])

    w.h3("Step 2 — the checks")
    w.code([
        "def setup_slack(self, ep):",
        "    required = self.period + self.skew(ep) - ep.cell.setup - self.uncert_setup",
        "    return required - ep.amax",
        "",
        "def hold_slack(self, ep):",
        "    required = self.skew(ep) + ep.cell.hold + self.uncert_hold",
        "    return ep.amin - required"])

    w.h3("Step 3 — compute the answer on paper, before you run it")
    w.code([
        "path:   p_reg/Q  ->  u97/B  ->  u97/Y  ->  q_reg/D",
        "",
        "1.  p_reg/Q     0.145 + 0.013 x 1.5  =  0.164     (DFF clk->Q, driving XOR2 A=1.5)",
        "2.  u97/Y       0.088 + 0.018 x 1.6  =  0.117     (XOR2, driving DFF D=1.6)",
        "",
        "    arrival at q_reg/D  =  0.164 + 0.117  =  0.281 ns",
        "",
        "3.  required  =  period 1.000 - setup 0.090  =  0.910 ns",
        "4.  slack     =  0.910 - 0.281               =  +0.629 ns    MET"])

    w.h3("Step 4 — now run it")
    w.code([
        "$ make tiny",
        "",
        "  ==========================================================================",
        "  SETUP TIMING REPORT   design=tiny   clock clk period=1.000 ns (1000.0 MHz)",
        "  ==========================================================================",
        "",
        "  Path 1   endpoint q_reg/D  (DFF)",
        "           startpoint p_reg",
        "         incr   arrival   pin",
        "        0.000     0.000   clock edge at p_reg",
        "        0.164     0.164   p_reg/Q                    (DFF)",
        "        0.000     0.164   u97/B                      (XOR2)",
        "        0.117     0.281   u97/Y                      (XOR2)",
        "        0.000     0.281   q_reg/D                    (DFF)",
        "                  0.910   required (period - setup)",
        "                  0.629   SLACK   MET",
        "",
        "  --------------------------------------------------------------------------",
        "  endpoints analysed : 2",
        "  UNCONSTRAINED      : 2 endpoint(s) not checked - no input/output",
        "                       delay was set for them. Unchecked is not passed.",
        "  WNS (worst slack)  : +0.629 ns   MET",
        "  TNS (total neg)    : +0.000 ns over 0 failing endpoint(s)",
        "  longest path       : 0.371 ns",
        "  Fmax               : 2693.2 MHz",
        "  --------------------------------------------------------------------------"])

    w.callout("Notice the UNCONSTRAINED line", [
        [N("Two endpoints were not checked, because no input or output delay was set for "
           "them. The report says so, in as many words. Most commercial reports say the "
           "same thing but bury it in a summary section, which is why so many engineers "
           "have never noticed it.")],
        [B("“Unchecked is not passed” "), N("is the single most useful sentence in this "
           "workbook.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.callout("Checkpoint 3", [
        [N("Your paper arithmetic and the engine agree to three decimal places, and you "
           "can explain every line of the report — including which library number "
           "produced each incr value.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T4
    w.h2("Tutorial 4 · Constraints  (4 hours)")

    w.para([N("Now change constraints and watch the report move. Do them one at a time and "
              "write down the prediction before each run.")])

    w.table(["Change", "Predict, then measure"],
            [["period 1.0 → 0.5 ns", "slack falls by 0.5; the path does not change"],
             ["period 1.0 → 0.35 ns", "slack goes negative; the same path is now critical"],
             ["add set_clock_uncertainty 0.15 -setup", "every setup slack drops by 0.15"],
             ["add set_input_delay for the first time",
              "new paths appear that were not there before; unconstrained count falls"],
             ["remove it again", "unconstrained count rises AND the WNS improves"],
             ["set_clock_skew 0.30 on the capture register",
              "setup slack improves; hold slack collapses"],
             ["set_false_path on the critical path", "the WNS jumps to the next-worst path"]],
            widths=[2.6, 4.2], size=9.2, bold_cols=(0,), align_center=False)

    w.code([
        "$ python3 sta/sta.py build/tiny.json tiny -p 0.5",
        "$ python3 sta/sta.py build/tiny.json tiny -p 0.35",
        "$ python3 sta/sta.py build/add32.json add32 -c constraints/add32.sdc",
        "$ python3 sta/sta.py build/hold_demo.json hold_demo \\",
        "      -c constraints/hold_skew.sdc --hold"])

    w.callout("The two runs that teach the most", [
        [B("Removing the input delay "), N("makes the WNS better and the analysis worse. "
           "Removing a check always improves the number.")],
        [B("Adding a false path on the critical path "), N("does the same thing, more "
           "dramatically. Write down, in your own words, why an engineer under deadline "
           "pressure might do this and how you would catch it in review.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.callout("Checkpoint 4", [
        [N("You predicted the direction and rough size of every change above before "
           "running it, and you were right at least five times out of seven. Where you "
           "were wrong, you know why.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T5
    w.h2("Tutorial 5 · Setup closure  (5 hours)")

    w.h3("Step 1 — the Fmax sweep")
    w.code([
        "$ make sweep",
        "",
        "=== Fmax vs width: hand-written carry chain ===",
        "  W           cells  longest(ns)  Fmax(MHz)     ns/bit",
        "  -------------------------------------------------------",
        "  4              30        0.773     1293.7     0.1933",
        "  8              62        1.247      801.9     0.1559",
        "  16            126        2.196      455.4     0.1373",
        "  32            254        4.094      244.3     0.1279",
        "  64            510        7.889      126.8     0.1233",
        "",
        "=== Fmax vs width: a + b, delay-driven mapping ===",
        "  W           cells  longest(ns)  Fmax(MHz)     ns/bit",
        "  -------------------------------------------------------",
        "  4              33        0.831     1203.4     0.2077",
        "  8              74        1.183      845.3     0.1479",
        "  16            159        1.547      646.4     0.0967",
        "  32            332        1.939      515.7     0.0606",
        "  64            681        2.318      431.4     0.0362"])

    w.para([N("The ns/bit column is the interesting one. For the hand-written chain it "
              "converges on a constant — the delay is linear in width, because a "
              "ripple-carry adder is a chain. For the tool's version it keeps falling — "
              "the tool built something with logarithmic depth, a carry-lookahead or "
              "carry-select structure, from a source file that never mentioned one.")])

    w.h3("Step 2 — the closure table")
    w.code([
        "$ make closure",
        "",
        "  design                  cells   area-mapped        cells   delay-mapped",
        "                                longest    Fmax               longest    Fmax",
        "  ----------------------------------------------------------------------------",
        "  add_ripple                254     4.094     244      254     5.258     190",
        "  add_ripple_pipe           303     2.315     432      303     2.906     344",
        "  add_fast                  268     4.615     217      332     1.939     516"])

    w.callout("Three things in that table are worth an argument", [
        [B("1. "), N("add_fast under area mapping (4.615 ns) is SLOWER than the "
           "hand-written ripple chain (4.094 ns). The idiomatic code lost.")],
        [B("2. "), N("add_fast under delay mapping (1.939 ns) is 2.4× faster than itself. "
           "The RTL did not change; one option did.")],
        [B("3. "), N("add_ripple gets WORSE under delay mapping (5.258 ns). The mapper has "
           "nothing left to decide — the structure is already fixed by the source — so the "
           "extra effort only shuffles the same slow chain.")],
    ], color=NAVY, bar="0E2A47")

    w.h3("Step 3 — verify before you believe any of it")
    w.code([
        "$ make verify",
        "",
        "PASS - all three adders agree with the reference over 500 vectors"])
    w.para([N("An optimisation you have not verified is not an optimisation. This is not "
              "ceremony: the pipelined version is genuinely easy to get wrong, and the "
              "testbench compares it against a reference delayed by the correct number of "
              "cycles for each design.")])

    w.h3("Step 4 — break it deliberately")
    w.para([N("Open "), M("rtl/add_ripple_pipe.v"), N(" and delete the two lines that "
              "delay the upper operands ("), M("ah_q <= a_q[31:16];"),
            N(" and its partner). Re-run "), M("make sweep"),
            N(" — the timing is unchanged, possibly better. Now run "), M("make verify"),
            N(" — it fails. This is the classic pipelining bug and you should meet it "
              "under controlled conditions before you meet it at work.")])

    w.callout("Checkpoint 5", [
        [N("You can explain, without looking, why the ripple chain's ns/bit is constant "
           "and the tool's is falling; you have reproduced the 2.4× speed-up; and you have "
           "broken the pipeline and watched verify catch it.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T6
    w.h2("Tutorial 6 · Hold violations and exceptions  (4 hours)")

    w.h3("Step 1 — create a hold violation")
    w.code([
        "$ cat constraints/hold_skew.sdc",
        "create_clock -period 3.0",
        "set_clock_skew 0.30 -regs dout_reg      # the capture clock arrives 0.30 ns late",
        "",
        "$ make hold",
        "  WNS (worst slack)  : -0.165 ns   VIOLATED     (hold_demo, 0.30 ns skew)",
        "  WNS (worst slack)  : +0.071 ns   MET          (hold_fixed, same skew)"])

    w.para([N("Two flops, nothing between them, and 0.30 ns of skew on the capture clock. "
              "The new data arrives 0.164 ns after the launch edge; the capture flop needs "
              "the old value for 0.035 ns after ITS edge, which is 0.300 ns later. The "
              "data lost the race by 0.171 ns.")])

    w.h3("Step 2 — change the period and watch nothing happen")
    w.code([
        "$ python3 sta/sta.py build/hold_demo.json hold_demo -p 3.0  --hold",
        "$ python3 sta/sta.py build/hold_demo.json hold_demo -p 30.0 --hold",
        "$ python3 sta/sta.py build/hold_demo.json hold_demo -p 300.0 --hold",
        "",
        "# the hold slack is -0.165 ns in all three runs."])
    w.para([N("A hundred-fold reduction in clock frequency and the violation is exactly "
              "the same size. If you needed one demonstration of why hold is different "
              "from setup, this is it.")])

    w.h3("Step 3 — the multicycle path")
    w.code([
        "$ make mcp",
        "",
        "=== a long path captured one cycle in four, at 3 ns ===",
        "  --- without the multicycle promise ---",
        "  WNS (worst slack)  : -1.193 ns   VIOLATED",
        "  TNS (total neg)    : -6.555 ns over 11 failing endpoint(s)",
        "  --- with set_multicycle_path 4 ---",
        "  WNS (worst slack)  : +0.392 ns   MET",
        "  TNS (total neg)    : +0.000 ns over 0 failing endpoint(s)"])

    w.para([N("Eleven failing endpoints became zero, and no RTL changed. The design was "
              "always correct; the analysis was wrong, because nobody had told the tool "
              "that the accumulator is only enabled one cycle in four.")])

    w.h3("Step 4 — make the promise false")
    w.para([N("Open "), M("rtl/slow_path.v"), N(" and remove the "), M("if (tick)"),
            N(" enable, so the accumulator loads every cycle. The multicycle constraint is "
              "now a lie. Re-run "), M("make mcp"),
            N(" — the report is still green, because the tool believed you. Write down "
              "what would happen in silicon.")])

    w.callout("Checkpoint 6", [
        [N("You have produced a hold violation, shown that the clock period does not "
           "affect it, fixed it with added delay, removed 11 false violations with one SDC "
           "line, and then made that line a lie and watched the report stay green.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ------------------------------------------------------------ T7
    w.h2("Tutorial 7 · The same design in an industrial tool  (3 hours)")

    w.para([N("Requires tier 3 (Vivado) or tier 2 (OpenSTA) from Part 6.2. If you have "
              "neither, read this tutorial anyway — the comparison is the point, and the "
              "outputs are reproduced below.")])

    w.h3("Step 1 — Vivado, headless")
    w.code([
        "$ vivado -mode batch -source scripts/vivado_timing.tcl",
        "$ grep -A4 'Design Timing Summary' rpt/post_synth_summary.rpt"])

    w.h3("Step 2 — compare against your engine")
    w.table(["What to compare", "Expect", "Why"],
            [["absolute WNS", "different", "a real FPGA fabric is not cda_edu.lib"],
             ["which path is critical", "the same", "the structure of the design is the "
              "same"],
             ["effect of halving the period", "the same shift", "slack is linear in period"],
             ["effect of the multicycle path", "the same direction",
              "the exception means the same thing everywhere"],
             ["report layout", "the same six things", "every STA tool reports the same "
              "things"]],
            widths=[2.3, 1.7, 2.8], size=9.2, bold_cols=(0,), align_center=False)

    w.h3("Step 3 — OpenSTA on the same netlist")
    w.code([
        "$ sta",
        "% read_liberty  lib/cda_edu.lib",
        "% read_verilog  build/add32_netlist.v",
        "% link_design   add32",
        "% read_sdc      constraints/add32.sdc",
        "% report_checks -path_delay max -digits 3"])
    w.para([N("OpenSTA uses the PrimeTime command set, so what you learn here transfers "
              "directly to the tool most ASIC teams sign off with. It will not read "),
            M("cda_edu.lib"), N(" — that file uses custom "), M("cda_*"),
            N(" attributes, which are convenient for a teaching analyser and are not part "
              "of the Liberty standard. Generate the standards-compliant view first:")])
    w.code([
        "$ make stdlib",
        "  wrote lib/cda_edu_std.lib  -  14 cells, 753 lines",
        "  braces balanced        : yes",
        "  required groups        : all present",
        "  delay numbers match    : yes, every cell",
        "  PASS - structurally sound and numerically identical to cda_edu.lib.",
        "",
        "# then read THAT file in OpenSTA:",
        "% read_liberty lib/cda_edu_std.lib"])
    w.para([N("The generated file expresses the same straight-line delay model as a 2×5 "
              "lookup table — the smallest form every Liberty reader accepts — with "
              "correct unateness on every input pin and proper setup/hold constraint "
              "groups on the flip-flops. The delay numbers are identical, so an OpenSTA "
              "report and a sta.py report on the same netlist can be compared cell by "
              "cell.")])
    w.callout("What make stdlib does and does not prove", [
        [N("The self-check verifies that the file is brace-balanced, that every cell "
           "carries the groups a Liberty reader requires, and that every delay number "
           "matches cda_edu.lib exactly. It cannot prove OpenSTA will accept it — only "
           "OpenSTA can do that, and it is not installed in every environment. "
           "If you have it, confirm with "),
         M("sta -no_splash -exit -x 'read_liberty lib/cda_edu_std.lib'"), N(".")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h3("Step 4 — write the comparison")
    w.para([N("One page. What matched, what did not, and why. This is the deliverable that "
              "shows you understood the topic rather than memorised a procedure. An "
              "answer that says “the numbers were different” is not an answer; an answer "
              "that says “the numbers were different because the FPGA's LUT delay is 0.12 "
              "ns where our XOR2 is 0.088, and routing adds delay our model has none of” "
              "is.")])

    w.callout("Checkpoint 7", [
        [N("You have run the same design through two tools, and you can account for the "
           "difference between them in terms of the delay model rather than dismissing it "
           "as “different tools give different answers”.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
