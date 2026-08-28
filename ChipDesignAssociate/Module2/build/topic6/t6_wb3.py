# -*- coding: utf-8 -*-
"""Topic 6 workbook — Part 4 optimisation, Part 5 violations, Part 6 tools."""
import _boot
from wbkit import *
from t6_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 4
    w.h1("Part 4 · Optimisation Techniques")

    w.h2("4.1  The menu, in cost order")

    w.image("fix_setup_menu", width=6.5)

    w.para([N("When a setup path fails, work down this list. The order is not arbitrary: "
              "each step costs more engineering time and more design disruption than the "
              "one above it, and the first two are so cheap that skipping them is never "
              "justified.")])

    w.h2("4.2  Fix 1 — check the constraint before you touch the design")

    w.para([N("Roughly half of all reported violations are not design problems. They are "
              "constraint problems, and the design was fine all along. Spending a week "
              "pipelining a path that a single false-path line would have removed is the "
              "most expensive mistake in this topic.")])

    w.table(["The report says", "Suspect", "Confirm in one minute by"],
            [["a huge violation on a reset path", "a missing false path",
              "reading the startpoint — is it rst_n?"],
             ["every I/O path fails by the same amount", "I/O delay too large",
              "comparing it with the upstream datasheet"],
             ["a path you know is slow fails", "a missing multicycle path",
              "checking whether the capture flop has an enable"],
             ["a path between two clocks fails", "missing set_clock_groups",
              "asking whether the two clocks are related at all"],
             ["WNS is almost exactly −(period)", "an undeclared generated clock",
              "report_clocks — is anything missing?"],
             ["nothing fails and you do not believe it", "unconstrained endpoints",
              "reporting the count; it should be zero"]],
            widths=[2.2, 1.9, 2.7], size=9.0, bold_cols=(0,), align_center=False)

    w.h2("4.3  Fix 2 — let the tool try harder, and the result nobody expects")

    w.para([N("Synthesis has an effort dial. On the open-source flow it is which "
              "technology-mapping mode ABC runs in; in Vivado it is the synthesis "
              "strategy; in an ASIC flow it is compile_ultra versus compile. Turning it up "
              "is free. Here is what it did to a 32-bit adder in the lab:")])

    w.code([
        "# the SAME RTL:   assign {cout, sum} = a_q + b_q;",
        "",
        "$ ABC=abc          make fmax      # default, area-oriented mapping",
        "  longest path 4.615 ns   ->   217 MHz",
        "",
        "$ ABC='abc -fast'  make fmax      # delay-oriented mapping",
        "  longest path 1.939 ns   ->   516 MHz",
        "",
        "# and for comparison, the hand-written structural ripple-carry chain:",
        "  longest path 4.094 ns   ->   244 MHz     (area-oriented mapping)"])

    w.callout("Read the third number again", [
        [N("Under area-oriented mapping the plain "), M("a + b"),
         N(" is SLOWER than the hand-written ripple chain: 4.615 ns against 4.094 ns. "
           "Under delay-oriented mapping it is 2.4× faster than either. Both netlists were "
           "proved equivalent to the RTL over 400 random vectors before those numbers were "
           "quoted.")],
        [B("The lesson: "), N("“describe intent, not structure” is only half the rule. The "
           "other half is “then check what your tool did with it”. The same source file is "
           "a slow design or a fast one depending on one option you may never have set.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("4.4  Fix 3 — restructuring")

    w.image("logic_restructure", width=6.4)

    w.para([N("A chain of N operations has depth N. The same operations arranged as a "
              "balanced tree have depth ⌈log₂ N⌉. For eight additions that is 7 levels "
              "against 3. Synthesis will usually do this for you, because addition is "
              "associative and the tool knows it.")])

    w.callout("What stops the tool doing it", [
        [N("Assign an intermediate result to a named wire that something else also reads, "
           "and that reader pins the structure — the tool can no longer rebalance across "
           "it, because doing so would change the value on that wire.")],
        [B("Practical rule: "), N("if a sum must be fast, do not publish its intermediate "
           "results. Compute the whole expression in one assignment and let the tool "
           "choose the shape.")],
    ], color=TEAL)

    w.h2("4.5  Fix 4 — pipelining")

    w.image("pipelining", width=6.5)

    w.para([N("Cutting a long combinational path with a register is the largest single win "
              "available. The work per cycle halves, so the clock can roughly double; "
              "throughput is unchanged once the pipe is full. What you pay is one extra "
              "cycle of latency, one more bank of registers, and — the part people forget "
              "— the obligation to delay everything that travels alongside the data.")])

    w.code([
        "// BEFORE - the whole 32-bit carry chain in one cycle",
        "always @(posedge clk) {cout, sum} <= a_q + b_q;",
        "",
        "// AFTER - cut at bit 16.",
        "always @(posedge clk) begin",
        "    {cmid_q, sl_q} <= a_q[15:0] + b_q[15:0];   // stage 1",
        "    ah_q <= a_q[31:16];        // <- the easy lines to forget: the upper operands",
        "    bh_q <= b_q[31:16];        //    must be delayed to MEET the carry",
        "",
        "    {cout, sum} <= {ah_q + bh_q + cmid_q, sl_q};   // stage 2",
        "end"],
        caption="rtl/add_ripple_pipe.v")

    w.callout("The classic pipelining bug", [
        [N("You cut the datapath and forget to delay something beside it — an operand, a "
           "valid flag, a write enable, a destination address. The design then meets "
           "timing beautifully and computes the wrong answer, because stage 2 is combining "
           "this cycle's control with last cycle's data.")],
        [N("Every optimisation must be followed by verification. "), M("make verify"),
         N(" runs all three adder netlists against a reference over 500 random vectors for "
           "exactly this reason.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("4.6  Fix 5 — retiming")

    w.image("retiming", width=6.4)

    w.para([N("Retiming moves an existing register across logic rather than adding a new "
              "one. If one stage is 4 ns and the next is 1 ns, moving the register between "
              "them makes both 2.5 ns and the clock can run 1.6× faster. Latency does not "
              "change at all, so nothing beside the datapath needs re-aligning — which "
              "makes it strictly cheaper than pipelining when it is available.")])

    w.table(["", "Pipelining", "Retiming"],
            [["adds a register", "yes", "no"],
             ["changes latency", "yes, by one cycle", "no"],
             ["control signals", "must all be delayed to match", "unchanged"],
             ["how much it can win", "roughly a factor of 2 per cut",
              "only up to the balance of existing stages"],
             ["tool support", "you write it", "Vivado: synth_design -retiming"]],
            widths=[1.7, 2.6, 2.5], size=9.2, bold_cols=(0,), align_center=False)

    w.para([N("A register cannot always move. One with an asynchronous reset, one whose "
              "output drives a port directly, and one that a testbench or a debug probe "
              "observes by name are all usually pinned in place.")])

    w.h2("4.7  Fixes 6 and 7 — architecture, and the clock")

    w.para([N("If the first five have not closed the design, the problem is not in the "
              "implementation. Either the work assigned to one cycle is genuinely too "
              "large — a different adder structure, a different encoding, fewer operations "
              "per cycle — or the frequency target was never achievable in this technology "
              "and should be renegotiated.")])
    w.para([N("Reducing the clock frequency is always available and always last. It works, "
              "immediately and completely, and it means shipping a slower product. Make "
              "that a decision someone takes deliberately, not one that happens because "
              "the deadline arrived.")])

    w.h2("4.8  The measured results, in one table")

    w.image("measured_results", width=6.5)

    w.callout("Part 4 self-check", [
        [N("1.  Why is “check the constraint” the first step and not the third?")],
        [N("2.  The same RTL gave 217 MHz and 516 MHz. What changed, and what did not?")],
        [N("3.  Why can a named intermediate wire make a sum slower?")],
        [N("4.  What must you do to every control signal when you pipeline a datapath?")],
        [N("5.  When is retiming strictly better than pipelining, and when is it "
           "unavailable?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 5
    w.h1("Part 5 · Setup and Hold Violations, and Their Resolution")

    w.h2("5.1  Diagnosing which one you have")

    w.para([N("Every report labels the path type: max (setup) or min (hold). Read that "
              "label first, because the two failures need opposite fixes and applying the "
              "wrong one makes the problem worse rather than merely failing to help.")])

    w.image("setup_vs_hold", width=6.4)

    w.h2("5.2  Setup violations")

    w.table(["Symptom", "Most likely cause", "First thing to try"],
            [["one path fails, the rest are fine", "a genuinely long path",
              "read its incr column"],
             ["one cell has a huge incr", "high fanout or a weak driver",
              "set_max_fanout, or let the tool buffer"],
             ["fifty small cells in one path", "the logic is too deep",
              "restructure, then pipeline"],
             ["everything fails by a similar amount", "the period is too aggressive",
              "sanity-check the target against the technology"],
             ["fails only after place-and-route", "routing delay, not logic",
              "floorplanning; keep the path local"],
             ["fails only at the slow corner", "correct behaviour",
              "that is the corner you sign off at"]],
            widths=[2.2, 2.1, 2.5], size=9.0, bold_cols=(0,), align_center=False)

    w.callout("The number that tells you how much work it is", [
        [N("Express the slack as a fraction of the period. −0.05 ns on a 5 ns period is a "
           "1% problem: a higher effort setting will usually find it. −2.5 ns on the same "
           "period is a 50% problem: no option will close that, and you are looking at "
           "pipelining or a different architecture. Do this arithmetic before you promise "
           "anyone a date.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("5.3  Hold violations")

    w.image("hold_race", width=6.5)

    w.para([N("A hold violation is a race. The launching flop produces its new value, and "
              "that value travels to the capture flop faster than the capture flop's hold "
              "requirement allows. Because both flops are triggered by the SAME edge, the "
              "clock period plays no part in the race at all.")])

    w.code([
        "hold slack  =  arrival 0.164  -  skew 0.300  -  hold 0.035  =  -0.171 ns",
        "",
        "#  measured in the lab:  make hold",
        "#  hold_demo   0.30 ns skew, no logic between the flops   ->  -0.165 ns  VIOLATED",
        "#  hold_fixed  same skew, two delay cells inserted        ->  +0.071 ns  MET"])

    w.callout("Why slowing the clock cannot help", [
        [N("Look at the equation above: the period is not in it. Slow the clock to 1 Hz "
           "and the launch edge and the capture edge are still the same edge, and the new "
           "data still arrives 0.164 ns after it. A hold violation is a functional "
           "failure, not a performance one.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("5.4  Fixing hold")

    w.image("fix_hold", width=6.4)

    w.para([N("The only fix is to make the DATA path slower — to insert delay between the "
              "two flops. That costs area and power and no frequency at all, which is why "
              "hold is always fixable and setup sometimes is not.")])

    w.h3("Who does the fixing")
    w.para([N("Place-and-route, automatically, after layout — because only then does the "
              "real clock skew exist. The tool inserts hold buffers on the paths that need "
              "them. You will almost never do this by hand, and you should be suspicious "
              "of any flow that asks you to.")])

    w.h3("What your RTL can do to make it impossible")
    w.bullets([
        [B("Gating a clock by hand. "), N("An AND gate in the clock path adds skew you "
           "cannot control and the clock-tree synthesiser cannot balance. Use a clock "
           "enable on the flop instead — every FPGA and every standard cell library has "
           "one.")],
        [B("Crossing clock domains without a synchroniser. "), N("No amount of buffering "
           "fixes a genuinely asynchronous crossing; you need two flops in the "
           "destination domain, and the crossing needs a false path or clock group so the "
           "tool stops trying to time it.")],
        [B("Using both clock edges in one path. "), N("Launching on the falling edge and "
           "capturing on the rising edge halves the budget for both checks.")],
    ])

    w.h2("5.5  An honest note on how the lab demonstrates the hold fix")

    w.code([
        "// rtl/hold_fixed.v",
        "// dly_sel is a real input port, tied to zero by the testbench.",
        "assign d0 = q1 ^ dly_sel[0];      // two XOR gates in the data path",
        "assign d1 = d0 ^ dly_sel[1];      // functionally a no-op when dly_sel == 0",
        "",
        "// Why not a chain of buffers marked (* keep *) ?",
        "//   opt_clean removes them. keep_hierarchy combined with -flatten removes",
        "//   them too. Only logic that a real input can influence survives",
        "//   optimisation - so the delay is built from gates fed by a real port."])

    w.callout("What this shows and what it does not", [
        [B("It honestly shows: "), N("that adding delay to the data path converts a hold "
           "violation into a met one, and by exactly how much (−0.165 → +0.071 ns).")],
        [B("It is not a style to copy. "), N("Writing XOR gates into your datapath to fix "
           "hold is not engineering. In a real flow, place-and-route inserts hold buffers "
           "with knowledge of the actual clock tree. This is a teaching device and it is "
           "labelled as one.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("5.6  The diagnosis procedure")

    w.table(["Step", "Do this", "Because"],
            [["1", "Read the unconstrained-endpoint count",
              "a clean report on half a design is worthless"],
             ["2", "Is it setup or hold? Read the path type",
              "the two need opposite fixes"],
             ["3", "Read the startpoint and endpoint by name",
              "the names often identify the problem"],
             ["4", "Ask whether the path is real",
              "half of all violations are constraint bugs"],
             ["5", "Look at the largest incr in the path",
              "one big cell or fifty small ones — different fixes"],
             ["6", "Compare WNS with TNS", "one path, or the whole design?"],
             ["7", "Apply the cheapest fix that could work",
              "and re-run before trying the next"],
             ["8", "Change ONE thing per run", "or you will not know what helped"]],
            widths=[0.6, 3.0, 3.2], size=9.0, bold_cols=(0,), align_center=False)

    w.callout("Step 8 is the one people skip", [
        [N("Under deadline pressure it is tempting to change the period, the effort level "
           "and the RTL all in one run. When the slack moves you will not know which "
           "change did it, and when it moves the wrong way you will not know what to "
           "undo.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("5.7  Timing closure")

    w.image("closure_loop", width=6.4)

    w.para([N("A design is closed when all three of these are true at once. Two out of "
              "three is not closed:")])
    w.numbered([
        [N("WNS ≥ 0 at the slow corner, with realistic uncertainty in the constraint.")],
        [N("Hold slack ≥ 0 at the fast corner.")],
        [N("Zero unconstrained endpoints — the report actually looked at everything.")],
    ])

    w.h2("5.8  Ten ways to get a green report and a broken chip")

    w.table(["#", "The mistake", "What it costs"],
            [["1", "no constraint file at all", "every path unchecked"],
             ["2", "clock declared, I/O not", "every boundary path unchecked"],
             ["3", "a generated clock never declared", "a whole domain unchecked"],
             ["4", "set_false_path used to silence a real path", "a field failure"],
             ["5", "multicycle -setup without the -hold line", "hold violations you created"],
             ["6", "multicycle claimed with no enable in the RTL", "wrong data captured"],
             ["7", "uncertainty reduced to make the report pass", "no margin on silicon"],
             ["8", "signing off setup at the typical corner", "fails on slow silicon"],
             ["9", "ignoring hold because the clock is slow", "fails at every speed"],
             ["10", "never checking the unconstrained count", "all of the above, silently"]],
            widths=[0.4, 3.4, 3.0], size=9.0, bold_cols=(0,), align_center=False)

    w.para([N("Nine of those ten produce a report that says everything is fine. That is "
              "the point of the list.", {"b": True, "c": RED})])

    w.callout("Part 5 self-check", [
        [N("1.  You have a hold violation on a 100 MHz design. Your colleague suggests "
           "dropping to 50 MHz. What do you say?")],
        [N("2.  Why do hold violations appear suddenly after clock-tree synthesis?")],
        [N("3.  Setup slack is −0.05 ns on a 5 ns period. How big a problem is that, and "
           "why does the ratio matter more than the number?")],
        [N("4.  Name three things in RTL that make hold violations harder to fix.")],
        [N("5.  Which of the ten mistakes above would your current project catch?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 6
    w.h1("Part 6 · Tools")

    w.h2("6.1  The landscape")

    w.image("tool_landscape", width=6.5)

    w.para([N("They all compute arrival, required and slack. The differences are the "
              "delay models, the report format and the price. Learn to read one report "
              "and you can read all of them.")])

    w.h2("6.2  Installing what you need")

    w.image("install_required", width=6.4)

    w.code([
        "sudo apt update",
        "sudo apt install yosys iverilog gtkwave python3 python3-matplotlib",
        "",
        "# verify:",
        "yosys -V && iverilog -V && python3 -c \"import matplotlib; print('ok')\""],
        caption="Tier 1 — Debian, Ubuntu or WSL2. This is all 57 of the 62 exercises need.")

    w.para([N("On Windows, install WSL2 first ("), M("wsl --install"),
            N(" from an elevated PowerShell), then run the same lines inside the Ubuntu "
              "shell it gives you. On macOS, "), M("brew install yosys icarus-verilog"),
            N(" covers the first two; matplotlib comes from pip.")])

    w.image("install_optional", width=6.4)

    w.code([
        "# Tier 2 - OpenSTA, a real STA tool with the PrimeTime command set",
        "git clone https://github.com/parallaxsw/OpenSTA",
        "cd OpenSTA && mkdir build && cd build",
        "cmake .. && make -j4 && sudo make install",
        "",
        "# it needs these first:",
        "sudo apt install cmake g++ swig bison flex libeigen3-dev tcl-dev libtcl"])

    w.h3("Vivado, step by step")
    w.table(["Step", "What to do", "Watch out for"],
            [["1", "create a free AMD/Xilinx account",
              "the download will not start without one"],
             ["2", "download the Unified Installer (web installer, ~200 MB)",
              "not the full 40 GB archive"],
             ["3", "choose Vivado ML Edition, then Vivado ML Standard",
              "Standard is the free one; no licence file needed"],
             ["4", "deselect every device family except Artix-7",
              "this cuts 40 GB to about 8 GB"],
             ["5", "on Linux, install the cable drivers afterwards",
              "only needed to program a real board"],
             ["6", "verify with  vivado -version", "then everything runs headless"]],
            widths=[0.6, 3.2, 3.0], size=9.0, bold_cols=(0,), align_center=False)

    w.para([N("You do not need a development board. Every timing exercise here is a "
              "synthesise-and-report exercise; Vivado will target a device it has never "
              "been connected to and give you a real timing report for it.")])

    w.h2("6.3  The open-source flow")

    w.image("lab_flow", width=6.4)

    w.code([
        "make lib      # read the Liberty file and print the cell table",
        "make tiny     # three flops - a report you can check by hand",
        "make sweep    # Fmax against width, for three adder styles",
        "make closure  # the full closure story, with the Fmax curves",
        "make hold     # a hold violation, then the same design fixed",
        "make mcp      # a false violation, then the multicycle path that removes it",
        "make verify   # prove every optimised netlist still computes the right answer",
        "make          # all of the above, ending in 'Topic 6 lab complete'"])

    w.h2("6.4  The same flow in Vivado")

    w.image("vivado_flow", width=6.5)

    w.code([
        "# scripts/vivado_timing.tcl   -   vivado -mode batch -source scripts/vivado_timing.tcl",
        "set part xc7a35tcpg236-1",
        "",
        "read_verilog [glob rtl/*.v]",
        "read_xdc     constraints/vivado.xdc",
        "synth_design -top add32 -part $part -flatten_hierarchy rebuilt",
        "",
        "report_timing_summary -file rpt/post_synth_summary.rpt",
        "report_timing -delay_type max -max_paths 10 -file rpt/post_synth_setup.rpt",
        "report_timing -delay_type min -max_paths 10 -file rpt/post_synth_hold.rpt",
        "",
        "opt_design ; place_design ; route_design",
        "report_timing_summary -file rpt/post_route_summary.rpt",
        "",
        "puts \"WNS = [get_property SLACK [get_timing_paths -delay_type max]]\""])

    w.callout("What to expect from the comparison", [
        [N("The absolute numbers will not match your engine's. They cannot: a 28 nm FPGA "
           "fabric is not the fictional library in lib/cda_edu.lib. What will match is "
           "the structure of the report, which path is critical, and the direction and "
           "rough proportion of every change you make to the constraints.")],
        [N("If you can explain why the numbers differ — pointing at the delay model rather "
           "than shrugging — you have understood this topic.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("6.5  SDC and XDC")

    w.image("sdc_vs_xdc", width=6.4)

    w.code([
        "# constraints/vivado.xdc  -  the timing half is identical to the SDC file",
        "create_clock -name clk -period 5.000 [get_ports clk]",
        "set_input_delay  -clock clk -max 1.20 [get_ports {a[*] b[*]}]",
        "set_output_delay -clock clk -max 1.00 [get_ports {sum[*] cout}]",
        "",
        "# the XDC-only half: physical constraints, which SDC has no concept of",
        "set_property PACKAGE_PIN W5      [get_ports clk]",
        "set_property IOSTANDARD LVCMOS33 [get_ports clk]"])

    w.callout("Part 6 self-check", [
        [N("1.  Which single apt line gives you everything the first 56 exercises need?")],
        [N("2.  What does OpenSTA give you that your own engine does not?")],
        [N("3.  Why does the Vivado installer offer to install 40 GB, and how do you "
           "avoid it?")],
        [N("4.  Name one command that exists in XDC and not in SDC, and say why.")],
        [N("5.  Your engine says 516 MHz and Vivado says 180 MHz on the same RTL. Is "
           "something wrong?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
