# -*- coding: utf-8 -*-
"""Topic 6 workbook — Part 2: constraints. Part 3: static timing analysis."""
import _boot
from wbkit import *
from t6_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 2
    w.h1("Part 2 · Timing Constraints")

    w.h2("2.1  Why a tool needs to be told anything at all")

    w.para([N("Synthesis is an optimisation problem, and an optimisation problem needs an "
              "objective. Given no objective, a synthesiser will produce something correct "
              "and make no effort to make it fast — and, worse, the timing report it "
              "produces afterwards will be silent, because a report can only report on "
              "checks that were actually performed.")])

    w.image("why_constrain", width=6.4)

    w.callout("The most dangerous artefact in this field", [
        [N("A clean timing report on an unconstrained design. It does not say the design "
           "is fast. It says nothing at all, in a format that looks exactly like good "
           "news. Engineers have shipped chips on the strength of such reports.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("2.2  The four questions every constraint file answers")

    w.image("sdc_map", width=6.4)

    w.para([N("The format is called SDC — Synopsys Design Constraints. It is a set of Tcl "
              "commands, and it is genuinely portable: Synopsys, Cadence, Intel Quartus "
              "and OpenSTA all read it. Xilinx uses XDC, which is SDC plus commands for "
              "physical constraints such as pin placement; the timing half is identical.")])

    w.h2("2.3  create_clock")

    w.image("create_clock_anatomy", width=6.3)

    w.code([
        "create_clock -name sys_clk -period 10.000 -waveform {0.000 5.000} [get_ports clk]",
        "",
        "#  -name       what this clock is called in every report from now on",
        "#  -period     10.0 ns  =  100 MHz. Everything downstream is measured against it.",
        "#  -waveform   rise at 0.0, fall at 5.0 - a 50% duty cycle. Omit it and you get",
        "#              a 50% duty cycle by default.",
        "#  [get_ports] the pin the clock physically enters on"])

    w.h3("Generated clocks")
    w.para([N("If your design divides or multiplies a clock, the result is a new clock and "
              "the tool must be told. Declare it as "), M("create_generated_clock"),
            N(", never as a second "), M("create_clock"),
            N(" — a generated clock keeps its relationship to its source, so paths between "
              "the two domains are still analysed. Two independent create_clock commands "
              "tell the tool the domains are unrelated, which is usually a lie.")])

    w.code([
        "# a divide-by-2 built from a toggling flop",
        "create_generated_clock -name clk_div2 -source [get_ports clk] \\",
        "                       -divide_by 2 [get_pins div_reg/Q]",
        "",
        "# an MMCM/PLL output on an FPGA - the tool usually derives these for you",
        "create_generated_clock -name clk_200 -source [get_pins mmcm/CLKIN1] \\",
        "                       -multiply_by 2 [get_pins mmcm/CLKOUT0]"])

    w.callout("The failure mode to memorise", [
        [N("A register clocked by a signal you never declared as a clock has "),
         B("no timing checks at all"), N(". Not failing checks — no checks. The report is "
           "clean and the domain is completely unanalysed. This is why the "
           "unconstrained-endpoint count matters more than the WNS.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("2.4  Clock uncertainty")
    w.code([
        "set_clock_uncertainty 0.150 -setup [get_clocks sys_clk]   # jitter + unbuilt skew",
        "set_clock_uncertainty 0.050 -hold  [get_clocks sys_clk]   # jitter only",
        "",
        "# uncertainty is SUBTRACTED from the setup budget and ADDED to the hold",
        "# requirement - it makes both checks harder, which is the point"])
    w.para([N("Part 1 covered where the numbers come from. The one thing to add here is "
              "that setup and hold uncertainty are usually different: unmodelled skew "
              "hurts setup at one end of the design and hold at the other, but jitter "
              "affects both, so the setup number is typically larger before layout and "
              "the two converge afterwards.")])

    w.h2("2.5  Input and output delay")

    w.image("io_delay", width=6.4)

    w.para([N("Your chip is not the whole system. Data arriving on a pin left another chip "
              "some time after the shared clock edge, and data leaving on a pin has to "
              "reach the next chip before "), I("its"),
            N(" clock edge. Those two intervals are part of the timing path and the tool "
              "cannot see them.")])

    w.code([
        "# INPUT: the upstream device's clock-to-out, plus the board trace delay.",
        "# 'the data leaves the other chip 3.0 ns after the same edge, so I have",
        "#  period - 3.0 left for my own logic before the next edge.'",
        "set_input_delay  -clock sys_clk -max 3.0 [get_ports {din[*] valid}]",
        "set_input_delay  -clock sys_clk -min 0.5 [get_ports {din[*] valid}]",
        "",
        "# OUTPUT: the downstream device's setup requirement, plus the trace delay.",
        "# 'the next chip needs it 2.5 ns before its edge, so I must be finished early.'",
        "set_output_delay -clock sys_clk -max 2.5 [get_ports {dout[*] ready}]",
        "set_output_delay -clock sys_clk -min 0.2 [get_ports {dout[*] ready}]"],
        caption="constraints/io.sdc")

    w.table(["", "-max", "-min"],
            [["used by", "the setup check", "the hold check"],
             ["means", "the LATEST the data can arrive / must leave",
              "the EARLIEST it can change"],
             ["comes from", "upstream clock-to-out (max) + trace",
              "upstream clock-to-out (min) + trace"],
             ["if you omit it", "setup on that port is unchecked",
              "hold on that port is unchecked"]],
            widths=[1.1, 2.9, 2.8], size=9.2, bold_cols=(0,), align_center=False)

    w.image("io_budget", width=6.3)

    w.callout("The rule of thumb that closes more designs than any other", [
        [B("Register every input and every output. "),
         N("A flop immediately behind each input pin and immediately before each output pin "
           "costs one cycle of latency and makes both boundary paths trivially short. The "
           "entire I/O timing problem disappears and your logic gets the whole period. "
           "Do this unless you have a measured reason not to.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("2.6  Exceptions: false paths")

    w.image("timing_exceptions", width=6.4)

    w.para([N("An exception tells the tool that the default assumption — every path must "
              "complete in one clock cycle — does not apply here. The tool accepts this "
              "without verification. You are making an assertion about your design and "
              "the tool is taking your word for it.")])

    w.h3("The three legitimate uses of set_false_path")
    w.code([
        "# 1. an asynchronous reset: asserted at any time, released synchronously.",
        "#    The assertion edge is not a timed event; the release edge IS.",
        "set_false_path -from [get_ports rst_n]",
        "",
        "# 2. a configuration register written at boot and read only when quiescent",
        "set_false_path -from [get_cells cfg_mode_reg]",
        "",
        "# 3. genuinely unrelated clocks. Use set_clock_groups, not a pile of false paths -",
        "#    it covers both directions and every path between them, now and in future.",
        "set_clock_groups -asynchronous -group [get_clocks sys_clk] \\",
        "                               -group [get_clocks usb_clk]"])

    w.callout("What a false path costs you when it is wrong", [
        [N("It removes the only check that would have caught the bug. The report goes "
           "green. The design ships. The failure appears in the field, at one temperature "
           "and one voltage, on some units and not others — which is the hardest class of "
           "bug there is to reproduce.")],
        [B("The discipline: "), N("every set_false_path line gets a comment on the line "
           "above it saying, in one sentence, why the path cannot matter. If you cannot "
           "write that sentence, you do not have a false path — you have a violation you "
           "have not understood yet.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("2.7  Exceptions: multicycle paths")

    w.image("multicycle_waves", width=6.3)

    w.para([N("Some results are genuinely not needed next cycle. A wide multiplier whose "
              "output is read once every four cycles has four cycles to compute, and "
              "telling the tool to check it in one is asking for a violation that does "
              "not exist.")])

    w.code([
        "set_multicycle_path 4 -setup -from [get_cells a_q*] -to [get_cells acc*]",
        "set_multicycle_path 3 -hold  -from [get_cells a_q*] -to [get_cells acc*]"])

    w.h3("Why the hold number is N−1")
    w.para([N("The -setup line moves the capture edge four cycles later. Left alone, the "
              "hold check would then measure against that same distant edge and demand "
              "that the data stay stable for nearly four cycles — an enormous and entirely "
              "artificial hold requirement that place-and-route would try to satisfy by "
              "inserting hundreds of buffers. The -hold N−1 line moves the hold check back "
              "to one edge after the launch, where it belongs.")])

    w.callout("Forgetting the hold line is a self-inflicted wound", [
        [N("You will not see it immediately: pre-layout there is little skew, so the "
           "absurd hold requirement may still pass. It appears after clock-tree synthesis, "
           "as hundreds of hold violations on a path you had already declared finished.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h3("The part everyone forgets: the hardware must agree")
    w.code([
        "// The SDC exception is a CLAIM about this design. Make the claim true.",
        "reg [1:0] phase;",
        "always @(posedge clk) phase <= phase + 1'b1;",
        "wire tick = (phase == 2'b11);          // one cycle in four",
        "",
        "always @(posedge clk) begin",
        "    if (tick) acc <= a_q + b_q;        // the ENABLE is what makes it legal",
        "end",
        "",
        "// a_q and b_q must ALSO be steady across all four cycles. If they change",
        "// every cycle, the multicycle claim is false and the accumulator will",
        "// sometimes latch a half-computed sum. The report will still be green."],
        caption="rtl/slow_path.v")

    w.table(["", "Without the exception", "With it"],
            [["worst slack", "−1.193 ns", "+0.392 ns"],
             ["what the tool times", "a 32-bit ripple add in one cycle", "across four cycles"],
             ["what you would do next", "pipeline something that never needed it",
              "ship what you already had"]],
            widths=[1.6, 2.8, 2.4], size=9.2, bold_cols=(0,), align_center=False)

    w.h2("2.8  Writing the file, and debugging it")

    w.image("sdc_checklist", width=6.4)

    w.para([N("The order matters because each step depends on the one before. You cannot "
              "constrain an I/O against a clock you have not declared, and you cannot "
              "write a sensible exception before you know which paths exist.")])

    w.h3("A complete file, annotated")
    w.code([
        "# ==================================================== constraints/add32.sdc",
        "# ---- clocks -------------------------------------------------------------",
        "create_clock -name clk -period 5.000 [get_ports clk]",
        "set_clock_uncertainty 0.100 -setup [get_clocks clk]",
        "set_clock_uncertainty 0.030 -hold  [get_clocks clk]",
        "",
        "# ---- boundary -----------------------------------------------------------",
        "set_input_delay  -clock clk -max 1.20 [get_ports {a[*] b[*]}]",
        "set_input_delay  -clock clk -min 0.30 [get_ports {a[*] b[*]}]",
        "set_output_delay -clock clk -max 1.00 [get_ports {sum[*] cout}]",
        "set_output_delay -clock clk -min 0.20 [get_ports {sum[*] cout}]",
        "",
        "# ---- exceptions ---------------------------------------------------------",
        "# cfg_mode is written by software at boot and read only when the core is",
        "# halted; no path from it can be exercised while the clock is running.",
        "set_false_path -from [get_cells cfg_mode_reg]",
        "",
        "# ---- environment --------------------------------------------------------",
        "set_max_fanout 16 [current_design]"])

    w.callout("The last check, on every single run", [
        [N("Report the number of unconstrained endpoints. It should be zero. "
           "A design with WNS +2.0 ns and 400 unconstrained endpoints is in far worse "
           "shape than one with WNS −0.1 ns and none — the first has not been analysed.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 3
    w.h1("Part 3 · How Static Timing Analysis Works")

    w.h2("3.1  Why it is called static")

    w.image("sta_vs_sim", width=6.4)

    w.para([N("Timing simulation applies vectors to a netlist annotated with delays and "
              "watches what happens. It is accurate and it is nearly useless at scale: it "
              "only exercises the paths your vectors happen to reach, it takes hours, and "
              "it is completely silent about the path you forgot to stimulate.")])
    w.para([N("Static timing analysis asks a different question. It never asks what the "
              "data values are — only how long each path is. That is why it needs no "
              "stimulus, why it cannot miss a path, and why it finishes in minutes on a "
              "design that would take a simulator a week.")])
    w.para([N("It buys that with one weakness. A path that can never actually switch — "
              "because two of its inputs are mutually exclusive, say — is still measured "
              "and still reported. Removing those is your job, which is exactly why "),
            M("set_false_path"), N(" exists.")])

    w.h2("3.2  The delay model")

    w.para([N("Before a tool can add up a path it needs a number for each cell. Those "
              "numbers live in a "), B("Liberty"), N(" file — extension .lib — produced by "
              "the foundry from SPICE characterisation of every cell in the library.")])

    w.code([
        "cell (XOR2) {",
        "    area              : 4.0 ;",
        "    cda_intrinsic     : 0.088 ;   /* ns with no load at all               */",
        "    cda_load_factor   : 0.018 ;   /* extra ns per unit of output capacitance */",
        "    cda_input_cap     : 1.5 ;     /* what this cell presents to its driver  */",
        "    pin (A) { direction : input ;  }",
        "    pin (B) { direction : input ;  }",
        "    pin (Y) { direction : output ; function : \"(A^B)\" ; }",
        "}",
        "",
        "cell (DFF) {",
        "    cda_clk_to_q      : 0.145 ;",
        "    cda_setup         : 0.090 ;",
        "    cda_hold          : 0.035 ;",
        "    cda_input_cap     : 1.6 ;",
        "}"],
        caption="lib/cda_edu.lib — the library you write in Tutorial 1")

    w.code([
        "cell delay  =  intrinsic  +  load_factor x (total input capacitance on the output net)"])

    w.callout("How this differs from a real Liberty file", [
        [N("A production .lib holds a two-dimensional table for each arc, indexed by input "
           "transition time (slew) and output load, with 5×5 or 7×7 entries interpolated "
           "at lookup. The arithmetic that follows is identical — arrival, required, slack "
           "— only the lookup is bigger. The simplification here costs you accuracy and "
           "costs you nothing in understanding.")],
    ], color=TEAL)

    w.h2("3.3  The timing graph")

    w.image("timing_graph", width=6.5)

    w.para([N("The netlist becomes a directed graph. Every pin is a node. Every cell "
              "contributes an arc from each input pin to each output pin it affects, "
              "carrying that cell's delay. Every net contributes arcs from its driver to "
              "each of its loads.")])

    w.callout("The arc convention that makes reports readable", [
        [N("Charge the cell's delay on the arc INSIDE the cell — input pin to output pin — "
           "computed with the load on that cell's output net. Charge clock-to-Q at the "
           "flop's Q pin. Give net arcs a delay of zero.")],
        [N("Do it any other way and every line of your report attributes a delay to the "
           "wrong cell. This is the single most common bug when people write their first "
           "analyser, and Tutorial 2 has you get it right deliberately.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("3.4  The two sweeps")

    w.image("arrival_required", width=6.4)

    w.numbered([
        [B("Forward, for arrival time. "), N("Visit the nodes in topological order. At each "
           "node, arrival = max over all incoming arcs of (source arrival + arc delay). "
           "The max is what makes it the setup check; the min, computed at the same time, "
           "is what makes it the hold check.")],
        [B("Backward, for required time. "), N("Start at each endpoint with "
           "required = period − setup − uncertainty + skew, and walk backwards subtracting "
           "arc delays, keeping the minimum at each node.")],
        [B("Subtract. "), N("slack = required − arrival, at every endpoint. The most "
           "negative answer is the WNS.")],
    ])

    w.code([
        "def propagate(self):",
        "    for n in self._order():                     # topological order",
        "        for arc in n.fanin:",
        "            src, dly = arc.src, arc.delay",
        "            n.amax = max(n.amax, src.amax + dly)     # LATEST   -> setup",
        "            n.amin = min(n.amin, src.amin + dly)     # EARLIEST -> hold",
        "",
        "def setup_slack(self, ep):",
        "    required = self.period + self.skew(ep) - ep.cell.setup - self.uncert_setup",
        "    return required - ep.amax",
        "",
        "def hold_slack(self, ep):",
        "    required = self.skew(ep) + ep.cell.hold + self.uncert_hold",
        "    return ep.amin - required"],
        caption="sta/sta.py — the whole algorithm, in fifteen lines")

    w.h3("Why every node carries two numbers")
    w.table(["", "amax (setup)", "amin (hold)"],
            [["propagates", "the latest arrival", "the earliest arrival"],
             ["asks", "did it get there in time?", "did it stay put long enough?"],
             ["compares against", "the NEXT clock edge", "the SAME clock edge"],
             ["uses the period", "yes", "no"],
             ["signed off at", "the slow corner", "the fast corner"]],
            widths=[1.6, 2.6, 2.6], size=9.2, bold_cols=(0,), align_center=False)

    w.h2("3.5  A path computed by hand")

    w.para([N("This is the calculation you must be able to do before you trust any tool. "
              "The design is three flip-flops with one XOR between two of them; the "
              "library is the one above.")])

    w.code([
        "path:   p_reg/Q  ->  u12/A  ->  u12/Y  ->  q_reg/D",
        "",
        "1.  p_reg/Q      DFF clk-to-Q is 0.145. Its output net drives u12/A, whose",
        "                 input capacitance is 1.5. The DFF load_factor is 0.013.",
        "",
        "                     0.145  +  0.013 x 1.5   =   0.1645 ns",
        "",
        "2.  u12 (XOR2)   intrinsic 0.088, load_factor 0.018. Its output net drives",
        "                 q_reg/D, whose input capacitance is 1.6.",
        "",
        "                     0.088  +  0.018 x 1.6   =   0.1168 ns",
        "",
        "3.  arrival at q_reg/D  =  0.1645 + 0.1168  =  0.2813 ns",
        "",
        "4.  required  =  period 1.000  -  setup 0.090  -  uncertainty 0.000",
        "              =  0.910 ns",
        "",
        "5.  slack     =  0.910  -  0.281   =   +0.629 ns          MET"])

    w.callout("Check this against the machine", [
        [M("$ make tiny"), N("   prints the same numbers. If your arithmetic and the "
           "engine ever disagree, one of you has a bug — and finding out which is the most "
           "valuable hour you will spend in this topic.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.h2("3.6  Reading a timing report")

    w.image("report_anatomy", width=6.5)

    w.para([N("Every timing report from every tool contains the same six things, in "
              "roughly the same order. Once you can find all six, PrimeTime, Vivado, "
              "Quartus and your own engine all become the same document with different "
              "formatting.")])

    w.table(["Look at", "If it says", "Then"],
            [["SLACK", "positive", "this path is fine — move to the next"],
             ["SLACK", "negative", "the magnitude tells you how hard the fix is"],
             ["Startpoint", "a port, not a flop", "your input delay is in play"],
             ["largest incr", "one cell dominating", "that cell or its load is the problem"],
             ["largest incr", "fifty small cells",
              "the path is too deep — restructure or pipeline"],
             ["TNS vs WNS", "roughly equal", "one bad path; a local fix"],
             ["TNS vs WNS", "TNS much larger", "systemic; review the target"],
             ["unconstrained", "not zero", "fix that before believing anything else"]],
            widths=[1.2, 1.9, 3.7], size=9.2, bold_cols=(0,), align_center=False)

    w.callout("A habit that makes you fast", [
        [N("Do not read the whole report. Read the slack, then the startpoint and "
           "endpoint names, then the largest incr line. Three numbers will tell you what "
           "class of problem you have in about twenty seconds, and the class determines "
           "the fix.")],
    ], color=TEAL)

    w.h2("3.7  Path groups")

    w.image("path_groups", width=6.5)

    w.para([N("Reports are usually organised by path group, and it is worth checking that "
              "all four appear. Reg-to-reg paths are the ones people look at; in-to-reg "
              "and reg-to-out are the ones that go unconstrained; in-to-out paths are rare "
              "and usually indicate that something should have been registered.")])

    w.h2("3.8  Fmax")

    w.image("fmax_idea", width=6.4)

    w.para([N("Fmax is set by exactly one path. Every other path in the design could be "
              "twice as fast and the number would not move. That is why timing work is "
              "always about one path at a time — and why fixing the critical path often "
              "reveals a second one, almost as bad, immediately behind it.")])

    w.callout("Part 3 self-check", [
        [N("1.  Why does STA need no test vectors?")],
        [N("2.  A node has three incoming arcs. Which arrival time does it keep, and why "
           "does the answer differ for setup and hold?")],
        [N("3.  Where is a cell's delay charged, and computed with which load?")],
        [N("4.  Your report shows WNS +1.2 ns and 260 unconstrained endpoints. What do you "
           "do first?")],
        [N("5.  Compute the slack for the p_reg → q_reg path if the period is 0.5 ns "
           "instead of 1.00 ns.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
