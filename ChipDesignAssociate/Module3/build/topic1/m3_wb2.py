# -*- coding: utf-8 -*-
"""Module 3 Topic 1 workbook — Theory 3 and Theory 4."""
import _boot
from wbkit import *
from m3_wb1 import B, N, I, M


def build(w):
    # ================================================================ Part 3
    w.h1("Part 3 · Sequential Circuit Timing")

    w.h2("3.1  The sampling window")

    w.para([N("Once a clock is in charge, the question stops being \"did it glitch?\" "
              "and becomes \"had it finished glitching by the time the edge "
              "arrived?\". That question is setup and hold.")])

    w.image("setup_hold", width=6.4)

    w.para([N("A flip-flop is a pair of cross-coupled latches. For it to settle into a "
              "definite state, D must be still for a short interval around the clock "
              "edge — before it and after it. Change D inside that window and the flop "
              "may take an unbounded time to settle, or settle to the wrong value. "
              "That is "), B("metastability"), N(", and it is what these checks exist "
              "to prevent.")])

    w.table(["Name", "What it requires", "Typical value"],
            [["setup time", "D stable BEFORE the clock edge", "0.02 – 0.2 ns"],
             ["hold time", "D stable AFTER the clock edge",
              "0.00 – 0.1 ns, sometimes negative"],
             ["clock-to-Q", "how long after the edge before Q is valid",
              "0.05 – 0.3 ns"]],
            widths=[1.5, 3.3, 2.0], size=9.5, bold_cols=(0,), align_center=False)

    w.callout("A negative hold time is not a typo", [
        [N("Inside the cell, the clock takes a little time to reach the input latch. "
           "If that internal delay exceeds the latch's own requirement, D may change "
           "slightly before the external clock edge and still be captured correctly. "
           "A negative hold time is free margin — it makes hold violations harder to "
           "create.")],
    ], color=TEAL)

    w.h2("3.2  The four terms, and one asymmetry")

    w.table(["Term", "What it is", "Who sets it"],
            [["clock-to-Q", "delay from the launching edge until Q is valid",
              "the library cell"],
             ["logic delay", "every gate and wire between the two flops",
              "your design, and synthesis"],
             ["setup time", "how early the capturing flop needs the data",
              "the library cell"],
             ["clock skew", "difference in clock arrival between the two flops",
              "the clock tree, after layout"],
             ["uncertainty", "jitter, plus skew not yet modelled",
              "you, in the constraint file"]],
            widths=[1.3, 3.4, 2.1], size=9.2, bold_cols=(0,), align_center=False)

    w.code([
        "setup:   t_cq + t_logic   <=   T + t_skew - t_setup - t_unc",
        "hold:    t_cq + t_logic   >=   t_skew + t_hold + t_unc",
        "",
        "#  The clock period T is in the first line and NOWHERE in the second.",
        "#  Everything surprising about hold follows from that one asymmetry."])

    w.callout("The sign on skew", [
        [N("A capture clock that arrives LATE gives the data more time, so it helps "
           "setup — and it eats hold margin by exactly the same amount. Every "
           "clock-tree decision trades one against the other, which is why skew is "
           "sometimes added deliberately (\"useful skew\") and why doing so is never "
           "free.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("3.3  Maximum frequency of operation")

    w.image("fmax_derivation", width=6.4)

    w.para([N("Fmax is not a number you look up; it is the setup inequality "
              "rearranged. Start from the requirement that the data must arrive before "
              "the next edge needs it, solve for the period, and invert.")])

    w.h3("Worked, with real numbers")
    w.code([
        "A path in the teaching library:",
        "",
        "    clock-to-Q (DFF)                       0.145 ns",
        "    logic: one XOR2 driving a flop D pin   0.117 ns",
        "    setup time (DFF)                       0.090 ns",
        "    uncertainty                            0.000 ns",
        "    skew                                   0.000 ns",
        "                                        -----------",
        "    minimum period                         0.352 ns",
        "",
        "    Fmax = 1 / 0.352 ns  =  2841 MHz",
        "",
        "Add 0.15 ns of uncertainty and the same path gives 1992 MHz.",
        "The circuit did not change. Your honesty about the clock did."])

    w.callout("An Fmax figure without its assumptions is marketing", [
        [N("Always ask three things: which PVT corner, how much uncertainty, and "
           "post-synthesis or post-route? The same netlist will produce numbers a "
           "factor of two apart depending on the answers.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("3.4  Fmax is set by one stage")

    w.image("fmax_one_stage", width=6.5)

    w.para([N("Every other path in the design could be twice as fast and the number "
              "would not move. In the lab, "), M("pipe_unbal"),
            N(" puts a 16-bit multiply in one stage and three light stages around it. "
              "Splitting that one stage in two took Fmax from 364.7 MHz to 473.2 MHz "
              "— a factor of 1.30, from moving work rather than from making anything "
              "faster.")])

    w.table(["", "What you gain", "What you pay"],
            [["pipelining", "a shorter longest path, so a faster clock; throughput "
              "unchanged once the pipe is full",
              "one more cycle of latency; one more register bank; every control signal "
              "beside the data must be delayed to match"]],
            widths=[1.2, 2.7, 2.9], size=9.2, bold_cols=(0,), align_center=False)

    w.callout("The classic pipelining bug", [
        [N("You cut the datapath and forget to delay a valid flag, an operand or an "
           "address alongside it. Timing improves and correctness quietly does not — "
           "stage 2 is now combining this cycle's control with last cycle's data.")],
        [B("Every optimisation needs a functional re-check. A faster design that "
           "computes the wrong answer is not faster.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.h2("3.5  A real setup violation, and its solution")

    w.image("setup_violation", width=6.4)

    w.para([N("Same constraint file, same 400 MHz target, two versions of the same "
              "arithmetic. Before reaching for a fix, size the problem as a fraction "
              "of the period — that arithmetic tells you which fix is even plausible.")])

    w.table(["Slack as a fraction of the period", "What it usually means",
             "Where to start"],
            [["under about 2%", "the tool nearly got there",
              "check the constraint, then raise synthesis effort"],
             ["2% to 10%", "a genuinely long path", "restructure the logic, or retime"],
             ["10% to 40%", "too much work in one cycle", "pipeline it"],
             ["over about 40%", "the target is wrong for this technology",
              "renegotiate the frequency, or change architecture"]],
            widths=[2.0, 2.3, 2.5], size=9.2, bold_cols=(0,), align_center=False)

    w.callout("The measured case", [
        [N("−0.322 ns on a 2.5 ns period is 13% over budget: out of reach of a "
           "synthesis option, and about right for one pipeline cut — which is exactly "
           "what fixed it (+0.307 ns MET). Doing this arithmetic first saves you from "
           "trying the cheap fixes on a problem too big for them.")],
        [B("And change one thing per run, or you will not know which change helped.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("3.6  A real hold violation, and why the clock cannot help")

    w.image("hold_violation", width=6.5)

    w.para([N("The same design was analysed at 4 ns, 40 ns and 400 ns. The hold slack "
              "was −0.119 ns in all three: a hundred-fold change in clock frequency, "
              "and not one picosecond of change in the violation. Both flops are "
              "triggered by the same edge, so the period never enters the race.")])

    w.table(["", "SETUP violation", "HOLD violation"],
            [["what happened", "the data arrived too late for this clock",
              "the data changed too soon after the same edge"],
             ["slow the clock", "fixes it", "does nothing whatsoever"],
             ["the chip", "works, at a lower frequency", "does not work at any speed"],
             ["found at", "synthesis, and again after layout",
              "only once a real clock tree exists"],
             ["reaching silicon", "a slower product", "a re-spin"]],
            widths=[1.3, 2.7, 2.8], size=9.2, bold_cols=(0,), align_center=False)

    w.para([N("So the fix is never the clock frequency. It is the clock TREE — "
              "rebalance it so the capture register sees less skew — or the data path: "
              "insert delay. Measured in the lab, dropping skew from 0.25 ns to "
              "0.10 ns took the slack from −0.119 ns to +0.031 ns.")])

    w.image("hold_why_late", width=6.4)

    w.callout("What RTL can do about hold: not make it impossible", [
        [N("No hand-gated clocks — use a clock enable; every FPGA and every standard "
           "cell library has one. No unsynchronised clock-domain crossings. No logic "
           "on an asynchronous reset. Beyond that, hold is place-and-route's job, and "
           "it has the one thing you do not: the real clock tree.")],
    ], color=NAVY, bar="0E2A47")

    w.h2("3.7  Practical examples of violations, and their solutions")

    w.table(["Symptom in the report", "Likely cause", "Solution"],
            [["one path fails, the rest are fine", "a genuinely long path",
              "restructure or pipeline that path"],
             ["one cell has a huge incremental delay",
              "high fanout, or a weak driver",
              "set_max_fanout; let the tool buffer it"],
             ["fifty small cells in one path", "the logic is too deep",
              "balance into a tree, then pipeline"],
             ["every path fails by a similar amount", "the period is too aggressive",
              "check the target against the technology"],
             ["fails only after place-and-route", "routing delay, not logic",
              "floorplan; keep the path local"],
             ["fails only at the slow corner", "correct behaviour",
              "that is the corner you sign off at"],
             ["hold fails on a short path after CTS", "clock skew",
              "rebalance the tree; insert hold buffers"],
             ["hold fails everywhere, at every speed", "a structural problem",
              "look for gated clocks and domain crossings"],
             ["a huge violation on a reset path", "a missing false path",
              "constrain it — this is not a design bug"]],
            widths=[2.4, 2.0, 2.4], size=9.0, bold_cols=(0,), align_center=False)

    w.callout("Part 3 self-check", [
        [N("1.  Write the setup inequality, then the hold inequality. What is missing "
           "from the second?")],
        [N("2.  Skew of +0.25 ns on the capture clock: what happens to setup slack, "
           "and to hold slack?")],
        [N("3.  A path fails by 0.05 ns on a 5 ns period. How big a problem is that, "
           "and why does the ratio matter more than the number?")],
        [N("4.  Why do hold violations appear suddenly after clock-tree synthesis?")],
        [N("5.  Your colleague proposes fixing a hold violation by halving the clock "
           "frequency. What do you say?")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()

    # ================================================================ Part 4
    w.h1("Part 4 · Timing Constraints for Synthesis")

    w.h2("4.1  A constraint file is an input, not a report setting")

    w.image("constraints_drive_synthesis", width=6.5)

    w.para([N("Synthesis is an optimisation problem, and an optimisation problem needs "
              "an objective. The constraint file supplies it. Give the tool no "
              "objective and it will optimise for area, because that is the default "
              "cost function — and the timing report it produces afterwards will be "
              "silent, because a report can only report on checks that were performed.")])

    w.h2("4.2  The minimum honest constraint set")

    w.image("sdc_minimum", width=6.4)

    w.code([
        "# ==================================================== constraints/pipe.sdc",
        "# ---- clock ------------------------------------------------------------",
        "# 400 MHz. pipe_unbal cannot make this; pipe_bal can. That is the experiment.",
        "create_clock -period 2.500",
        "",
        "# jitter, plus a placeholder for the clock-tree skew that does not exist yet",
        "set_clock_uncertainty 0.080 -setup",
        "set_clock_uncertainty 0.020 -hold",
        "",
        "# ---- boundary ---------------------------------------------------------",
        "# Without these two lines every path touching a port is UNCONSTRAINED,",
        "# and the analyser says so. Run without them once and read the warning.",
        "set_input_delay  0.40 -clock clk",
        "set_output_delay 0.35 -clock clk"])

    w.callout("The line to check on every single run", [
        [N("The count of unconstrained endpoints. It must be zero. A design with "
           "WNS +2.0 ns and four hundred unconstrained endpoints is in far worse shape "
           "than one with WNS −0.1 ns and none — the first has not been analysed at "
           "all.")],
        [B("Unchecked is not passed.")],
    ], color=RED, fill="FDECEF", bar="D6224A")

    w.para([N("Module 2 Topic 6 develops each of these commands in full: generated "
              "clocks, where the I/O delay numbers come from, false paths and "
              "multicycle paths. This part assumes them and asks what synthesis does "
              "once you have written them.")])

    w.h2("4.3  What synthesis does to a hazard fix")

    w.image("synth_deletes_fix", width=6.5)

    w.para([N("Part 2 taught you to add a redundant term to remove a hazard. Here is "
              "what happens when you write that term in RTL and synthesise it:")])

    w.code([
        "$ make synth",
        "",
        "  RTL written                      cells  gates",
        "  -------------------------------  -----  ---------------",
        "  f = a&~b | b&c                       1  {'$_MUX_': 1}",
        "  f = a&~b | b&c | a&c   (fixed)       1  {'$_MUX_': 1}",
        "",
        "  The two netlists are IDENTICAL. The consensus term was deleted."])

    w.para([N("And look at what it built instead: a single multiplexer. "),
            M("A B' + B C"), N(" is exactly "), M("B ? C : A"),
            N(", and the optimiser saw that before it saw anything else. Whether "),
            I("that"), N(" cell glitches is decided by its internals, in a library "
                         "you did not write.")])

    w.callout("Reconciling Part 2 with Part 4", [
        [B("What not to conclude: "), N("\"hazard analysis is pointless because the "
           "tool undoes it\", or \"just write RTL and trust synthesis\". The second "
           "one ships broken asynchronous interfaces.")],
        [B("What to conclude: "), N("hazard-freedom is a property of the NETLIST, not "
           "of your source. So where you genuinely need it, protect it structurally — "
           "a dont_touch or keep attribute, an instantiated library cell, or a module "
           "the tool is told not to flatten — and then re-run the glitch detector on "
           "the post-synthesis netlist, not on the RTL.")],
        [N("And on the vast majority of nets — everything sampled by a clock — you do "
           "not need it at all.")],
    ], color=AMBER, fill="FFF7EC", bar="C77514")

    w.h2("4.4  Circuit synthesis and timing analysis as one loop")

    w.image("synth_to_sta", width=6.4)

    w.para([N("RTL, constraints, synthesis, netlist, timing report, and back to one of "
              "the first two. You leave the loop once, when all three of these hold "
              "together:")])
    w.numbered([
        [N("Setup slack ≥ 0 at the slow corner, with realistic uncertainty.")],
        [N("Hold slack ≥ 0 at the fast corner.")],
        [N("Zero unconstrained endpoints.")],
    ])
    w.para([N("Two out of three is not closure.", {"b": True, "c": RED})])

    w.h2("4.5  Everything here is a trade")

    w.image("area_speed", width=6.4)

    w.callout("Part 4 self-check", [
        [N("1.  What does a constraint file do to synthesis?")],
        [N("2.  What circuit do you get with no constraints at all, and why?")],
        [N("3.  What did synthesis do to the consensus term, and why was that "
           "predictable?")],
        [N("4.  Where does hazard-freedom have to be verified?")],
        [N("5.  Name the three conditions for leaving the synthesis/analysis loop.")],
    ], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    w.page_break()
