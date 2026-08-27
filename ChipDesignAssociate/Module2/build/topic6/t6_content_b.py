# -*- coding: utf-8 -*-
"""Topic 6 deck — 6b: timing analysis and optimisation techniques."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ===================================================== section 6b
    d.section_slide(
        "PART 6b", "Timing Analysis and Optimization Techniques",
        "How a tool turns a netlist into a slack number - and what to do "
        "when that number is negative.",
        ["Static timing analysis: the graph, the two sweeps, the subtraction",
         "Reading a timing report line by line",
         "Path groups, WNS, TNS, Fmax and PVT corners",
         "Optimisation: constraints, mapping, restructuring, pipelining, retiming"],
        accent=VIOLET)

    # ------------------------------------------------------ STA vs sim
    s = d.slide("6b · WHY STA", "Static Timing Analysis Replaced Timing Simulation")
    y = d.image(s, TOP - 45720, "sta_vs_sim", 4297680)
    d.card(s, y + G, "The word \"static\" is the whole idea",
           [[R("STA never asks what the data values are. It only asks how long the path is. "
               "That is why it needs no stimulus, why it cannot miss a path - and why it "
               "will happily report a path that can never actually switch.", s=10.5)]],
           accent=TEAL, h=822960)

    # ------------------------------------------------------ timing graph
    s = d.slide("6b · STEP 1", "The Netlist Becomes a Graph of Delays")
    y = d.image(s, TOP - 45720, "timing_graph", 4297680)
    y = d.code(s, y + G, [
        "cell delay  =  intrinsic  +  load_factor x (sum of input caps on the output net)"],
        title="the delay model used throughout this topic", size=10.5)
    d.lead(s, y + G, [[R("Real Liberty libraries use a 2-D table indexed by input slew and "
                         "output load. The arithmetic below is the same; only the lookup "
                         "is bigger.", s=10.5)]], h=274320)

    # ----------------------------------------------------- the delay model
    s = d.slide("6b · THE DELAY MODEL", "A Liberty Cell, In Full")
    y = d.code(s, TOP, [
        "cell (XOR2) {",
        "    area              : 4.0 ;",
        "    cda_intrinsic     : 0.088 ;      /* ns, with no load at all              */",
        "    cda_load_factor   : 0.018 ;      /* ns per unit of capacitance on Y      */",
        "    cda_input_cap     : 1.5 ;        /* what this cell presents to its driver */",
        "    pin (A) { direction : input ;  }",
        "    pin (B) { direction : input ;  }",
        "    pin (Y) { direction : output ; function : \"(A^B)\" ; }",
        "}",
        "",
        "cell (DFF) {",
        "    cda_clk_to_q      : 0.145 ;      /* CK rising -> Q valid                  */",
        "    cda_setup         : 0.090 ;      /* D stable before CK                    */",
        "    cda_hold          : 0.035 ;      /* D stable after  CK                    */",
        "    cda_input_cap     : 1.6 ;",
        "}"],
        title="lib/cda_edu.lib — you write this file in lab T1", size=9.5)

    d.card(s, y + G, "Why you write the library yourself",
           [[R("Every delay number in this topic is one you chose. When the report says "
               "0.164 ns you can point at the two lines of the library it came from. "
               "There is no black box anywhere in the chain.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ------------------------------------------------------- worked delay
    s = d.slide("6b · WORKED EXAMPLE", "One Path, By Hand, To Three Decimal Places")
    y = d.code(s, TOP, [
        "path:   p_reg/Q  ->  u12/A  ->  u12/Y  ->  q_reg/D",
        "",
        "1.  p_reg/Q      clk-to-Q 0.145, driving a net loaded by u12/A (cap 1.5)",
        "                 0.145  +  0.013 x 1.5  =  0.1645          <- DFF load_factor 0.013",
        "",
        "2.  u12  (XOR2)  intrinsic 0.088, driving a net loaded by q_reg/D (cap 1.6)",
        "                 0.088  +  0.018 x 1.6  =  0.1168",
        "",
        "    arrival at q_reg/D   =  0.1645 + 0.1168  =  0.2813 ns",
        "",
        "3.  required = period 1.000 - setup 0.090 - uncertainty 0.000 = 0.910 ns",
        "",
        "    slack = 0.910 - 0.281 = +0.629 ns    MET"],
        size=9.5)
    d.card(s, y + G, "This is not an illustration - it is the lab's actual output",
           [[R("Run  make tiny  and the engine prints +0.629. You will have computed it "
               "on paper first. If the two ever disagree, one of them has a bug, and "
               "finding out which is the most useful hour in the topic.", s=10.5)]],
           accent=NAVY, h=822960)

    # -------------------------------------------------- arrival/required
    s = d.slide("6b · STEP 2", "Two Sweeps, Then One Subtraction")
    y = d.image(s, TOP - 45720, "arrival_required", 4389120)
    d.lead(s, y + G, [[R("Forward for arrival, backward for required, subtract at every "
                         "endpoint. A million-flop design is a million of these "
                         "subtractions - which is why STA finishes in minutes.", s=11)]],
           h=411480)

    # ------------------------------------------------------- the algorithm
    s = d.slide("6b · THE ALGORITHM", "Fifteen Lines That Do the Whole Job")
    d.code(s, TOP, [
        "def propagate(self):",
        "    for n in self._order():                  # topological order",
        "        for arc in n.fanin:",
        "            src, dly = arc.src, arc.delay",
        "            n.amax = max(n.amax, src.amax + dly)     # LATEST  -> setup",
        "            n.amin = min(n.amin, src.amin + dly)     # EARLIEST-> hold",
        "",
        "def setup_slack(self, ep):",
        "    required = self.period + self.skew(ep) - ep.cell.setup - self.uncert_setup",
        "    return required - ep.amax",
        "",
        "def hold_slack(self, ep):",
        "    required = self.skew(ep) + ep.cell.hold + self.uncert_hold",
        "    return ep.amin - required",
        "",
        "# WNS = min(setup_slack(ep) for ep in endpoints)",
        "# TNS = sum(s for s in slacks if s < 0)"],
        title="sta/sta.py — the core of the engine you complete in lab T3", size=9.5)

    # ------------------------------------------------------- max and min
    s = d.slide("6b · MAX AND MIN", "Why the Engine Carries Two Numbers Per Node", accent=AMBER)
    y = d.table(s, TOP,
                ["", "Setup check (max delay)", "Hold check (min delay)"],
                [["propagates", "the LATEST arrival", "the EARLIEST arrival"],
                 ["asks", "did it get there in time?", "did it stay put long enough?"],
                 ["compares against", "the NEXT clock edge", "the SAME clock edge"],
                 ["uses the period", "yes", "no - not at all"],
                 ["signed off at", "the SLOW corner", "the FAST corner"],
                 ["a violation means", "the chip must run slower", "the chip does not work"]],
                [2377440, 4434840, 4434840], rh=283464, bold_cols=(0,))

    y = d.cols(s, y + G, [
        ("A trap worth naming",
         [[R("If you propagate only the max delay, your hold check silently uses the wrong "
             "number and reports violations that are not there - or misses ones that are.")],
          [R("The engine in the lab keeps both, and the hold report traces the MIN path.")]],
         AMBER, CARD_A),
        ("What this looks like in a tool",
         [[R("Vivado: report_timing -delay_type max  vs  -delay_type min.")],
          [R("PrimeTime / OpenSTA: -setup vs -hold, or report_timing -delay_type min_max "
             "for both at once.")]], TEAL, CARD)],
        h=1600200)

    d.lead(s, y + G, [[R("Every real STA tool does exactly this. The two-number rule is not "
                         "a simplification - it is the whole reason setup and hold can "
                         "disagree.", b=True, c=NAVY, s=10.5)]], h=274320)

    # ------------------------------------------------------ report anatomy
    s = d.slide("6b · READING A REPORT", "It Is Always the Same Six Things")
    y = d.image(s, TOP - 45720, "report_anatomy", 4663440)
    d.lead(s, y + G, [[R("Read it bottom-up: the slack tells you IF there is a problem, "
                         "the incr column tells you WHERE it is.", b=True, c=NAVY, s=11)]],
           h=274320)

    # ------------------------------------------------ report in practice
    s = d.slide("6b · READING A REPORT", "The Four Numbers To Look At First")
    y = d.table(s, TOP,
                ["Look at", "If it says", "Then"],
                [["SLACK", "a positive number", "this path is fine - look at the next one"],
                 ["SLACK", "a negative number", "the size tells you how hard the fix is"],
                 ["Startpoint", "a port, not a flop",
                  "your input delay is in play - check it first"],
                 ["the largest incr", "one cell dominating",
                  "that cell or its load is the problem"],
                 ["the largest incr", "fifty small cells",
                  "the path is too deep - restructure or pipeline"],
                 ["TNS", "roughly equal to WNS", "one bad path - a local fix"],
                 ["TNS", "hundreds of times WNS",
                  "systemic - the target or the architecture is wrong"],
                 ["unconstrained", "anything but zero",
                  "fix that before believing any other number"]],
                [2560320, 3383280, 5303520], rh=274320, bold_cols=(0,))

    d.card(s, y + G, "A habit that will make you fast",
           [[R("Do not read the whole report. Read the slack, then the startpoint, then the "
               "biggest incr line. Three numbers will tell you what kind of problem you "
               "have in about twenty seconds.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ----------------------------------------------------------- path groups
    s = d.slide("6b · PATH GROUPS", "Four Kinds of Path, and Every Design Has All Four")
    y = d.image(s, TOP - 45720, "path_groups", 4663440)
    d.lead(s, y + G, [[R("A report that only shows reg-to-reg paths is a report on a "
                         "quarter of your design.", b=True, c=RED, s=11)]], h=274320)

    # ------------------------------------------------------------ WNS/TNS
    s = d.slide("6b · WNS AND TNS", "Two Numbers That Say Different Things")
    y = d.image(s, TOP - 45720, "wns_tns", 4297680)
    d.card(s, y + G, "Use them together or you will misjudge the work",
           [[R("WNS tells you how bad the worst path is. TNS tells you how many paths are "
               "bad. WNS -0.42 with TNS -0.42 is an afternoon; WNS -0.42 with TNS -180 is "
               "an architecture review.", s=10.5)]],
           accent=NAVY, h=594360)

    # -------------------------------------------------------------- Fmax
    s = d.slide("6b · FMAX", "One Path Sets the Speed of the Entire Chip")
    y = d.image(s, TOP - 45720, "fmax_idea", 4389120)
    d.lead(s, y + G, [[R("Not the average path. Not the second worst. The single longest "
                         "one - which is why all timing work is about one path at a time.",
                         b=True, c=NAVY, s=11)]], h=411480)

    # ------------------------------------------------------------ corners
    s = d.slide("6b · PVT CORNERS", "One Netlist, Several Silicons")
    y = d.image(s, TOP - 45720, "corners", 4389120)
    d.lead(s, y + G, [[R("Setup is a race against the clock, so check it where the logic is "
                         "SLOW. Hold is a race against the previous edge, so check it where "
                         "the logic is FAST.", b=True, c=AMBER, s=11)]], h=411480)

    # ================================================== optimisation intro
    s = d.slide("6b · OPTIMISATION", "The Menu, Cheapest First", accent=GREEN)
    y = d.image(s, TOP - 45720, "fix_setup_menu", 4663440)
    d.lead(s, y + G, [[R("Steps 1 and 2 cost you minutes. Step 7 costs your customer "
                         "performance for ever.", b=True, c=NAVY, s=11)]], h=274320)

    # ------------------------------------------------ the constraint check
    s = d.slide("6b · FIX 1", "Check the Constraint Before You Touch the Design")
    y = d.table(s, TOP,
                ["The report says", "Suspect first", "How to confirm in one minute"],
                [["a huge violation on a reset path", "a missing false path",
                  "look at the startpoint - is it rst_n?"],
                 ["every I/O path fails by the same amount", "input/output delay too large",
                  "compare it against the upstream datasheet"],
                 ["a path you know is slow fails", "a missing multicycle path",
                  "does the capture register have an enable?"],
                 ["a path across two clocks fails", "missing set_clock_groups",
                  "are the two clocks actually related?"],
                 ["WNS is exactly -(period)", "an undeclared generated clock",
                  "report_clocks - is anything missing?"],
                 ["nothing fails but you do not believe it", "unconstrained endpoints",
                  "report the count - it should be zero"]],
                [3657600, 3200400, 4389120], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "Roughly half of all reported violations are not design problems",
           [[R("They are constraint problems. Fixing the design first is the single "
               "biggest waste of time in timing closure - you can spend a week pipelining "
               "a path that was never real.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=594360)

    # ---------------------------------------------- the mapping experiment
    s = d.slide("6b · FIX 2", "Let the Tool Try Harder - the Measured Result", accent=GREEN)
    y = d.code(s, TOP, [
        "# the SAME RTL:   assign {cout, sum} = a_q + b_q;",
        "",
        "$ ABC=abc      make fmax        # default: area-oriented mapping",
        "  longest path 4.615 ns   ->   217 MHz",
        "",
        "$ ABC='abc -fast' make fmax     # delay-oriented mapping",
        "  longest path 1.939 ns   ->   516 MHz",
        "",
        "# and the hand-written ripple-carry chain, for comparison:",
        "  longest path 4.094 ns   ->   244 MHz    (area mapping)"],
        title="one flag, 2.4x the frequency", size=10)

    y = d.cols(s, y + G, [
        ("The result nobody expects",
         [[R("Under area-oriented mapping, the plain  a + b  is SLOWER than the "
             "hand-written ripple chain: 4.615 ns against 4.094 ns.")],
          [R("Both netlists were proved equivalent to the RTL over 400 random vectors "
             "before these numbers were quoted.")]], AMBER, CARD_A),
        ("What it means",
         [[R("\"Describe intent, not structure\" is only half the rule.")],
          [R("The other half: check what your tool did with it. The same source can be "
             "a slow design or a fast one depending on one option you did not set.",
             b=True, c=NAVY)]], GREEN, CARD_G)],
        h=1737360)

    d.lead(s, y + G, [[R("You will reproduce both numbers yourself in lab T5.",
                         b=True, c=TEAL, s=10.5)]], h=274320)

    # ----------------------------------------------------- restructuring
    s = d.slide("6b · FIX 3", "Restructuring - a Chain Is Depth N, a Tree Is Depth log N")
    y = d.image(s, TOP - 45720, "logic_restructure", 4389120)
    d.card(s, y + G, "What stops the tool doing it for you",
           [[R("Assign an intermediate sum to a named wire that something else also reads, "
               "and that reader pins the structure: the tool can no longer rebalance across "
               "it. If a sum must be fast, do not publish its intermediate results.",
               s=10.5)]],
           accent=TEAL, h=822960)

    # -------------------------------------------------------- pipelining
    s = d.slide("6b · FIX 4", "Pipelining - Cut the Path, Keep the Work")
    y = d.image(s, TOP - 45720, "pipelining", 4480560)
    d.lead(s, y + G, [[R("The biggest single win available - and the one with a real cost: "
                         "one more cycle of latency, and every control signal alongside the "
                         "data must be delayed to match.", s=11)]], h=411480)

    # ------------------------------------------------------ pipeline RTL
    s = d.slide("6b · FIX 4", "Pipelining In RTL - and the Mistake To Avoid")
    y = d.code(s, TOP, [
        "// BEFORE - one stage, the whole 32-bit carry chain in one cycle",
        "always @(posedge clk) {cout, sum} <= a_q + b_q;",
        "",
        "// AFTER - cut at bit 16. Note that a_q[31:16] and b_q[31:16] must be DELAYED",
        "// to meet the carry when it arrives, or the upper half adds the wrong operands.",
        "always @(posedge clk) begin",
        "    {cmid_q, sl_q} <= a_q[15:0] + b_q[15:0];   // stage 1",
        "    ah_q <= a_q[31:16];                        // <- the easy line to forget",
        "    bh_q <= b_q[31:16];",
        "",
        "    {cout, sum} <= {ah_q + bh_q + cmid_q, sl_q};   // stage 2",
        "end"],
        title="rtl/add_ripple_pipe.v", size=9.5)

    d.card(s, y + G, "The classic pipelining bug, in one sentence",
           [[R("You cut the datapath and forget to delay something that travels beside it - "
               "an operand, a valid flag, a write enable. The design still meets timing "
               "beautifully and computes the wrong answer. Lab T5 makes you find this "
               "one deliberately.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=822960)

    # --------------------------------------------------------- retiming
    s = d.slide("6b · FIX 5", "Retiming - Move the Register You Already Have")
    y = d.image(s, TOP - 45720, "retiming", 4297680)
    d.card(s, y + G, "Free in a way pipelining is not",
           [[R("No register is added, so latency does not change and no control signal "
               "needs re-aligning. Vivado does it with  synth_design -retiming; most ASIC "
               "tools have an equivalent. A register with an asynchronous reset, or one "
               "whose output goes straight to a port, usually cannot move.", s=10.5)]],
           accent=VIOLET, h=822960)

    # ------------------------------------------------------ 6b checkpoint
    s = d.slide("6b · CHECKPOINT", "Eight Questions Before We Move On", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What does STA propagate forward?",
                  "arrival time - the latest, for setup"],
                 ["2", "And backward?", "required time, from period minus setup"],
                 ["3", "Why does it need no stimulus?",
                  "it measures path length, not path activity"],
                 ["4", "What is the one weakness of that?",
                  "it reports paths that can never switch - false paths"],
                 ["5", "WNS -0.1, TNS -95. Diagnosis?",
                  "systemic; many paths just fail - review the target"],
                 ["6", "Which corner signs off setup?", "slow: slow silicon, low V, high T"],
                 ["7", "Cheapest fix for a setup violation?",
                  "check the constraint, then the mapping effort"],
                 ["8", "What does pipelining cost?",
                  "a cycle of latency, and every parallel signal must match"]],
                [548640, 4846320, 5852160], rh=283464, bold_cols=(0,))
    d.lead(s, y + G, [[R("Part 6c is where the two failures separate: setup and hold need "
                         "opposite fixes, and confusing them wastes days.", b=True,
                         c=GREEN, s=11)]], h=274320)
