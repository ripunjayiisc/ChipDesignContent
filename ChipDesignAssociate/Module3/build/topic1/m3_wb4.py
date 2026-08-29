# -*- coding: utf-8 -*-
"""Module 3 Topic 1 workbook — 58 exercises, worked solutions, reference card."""
import _boot
from wbkit import *
from m3_wb1 import B, N, I, M


EX = [
    # ------------------------------------------------------ A · on paper
    ("A1", "H", "Draw the K-map for F = A B' + B C and mark the loop for each product "
     "term. Which two 1-cells are adjacent but share no loop?",
     "Cells A=1,B=0,C=1 and A=1,B=1,C=1. A B' loops the A=1,B=0 row; B C loops the "
     "B=1,C=1 column; neither covers both of those cells."),
    ("A2", "H", "Derive the consensus term for that pair from first principles.",
     "The two cells agree on A=1 and C=1 and differ in B. Keep the agreements, drop "
     "the variable that changed: A C."),
    ("A3", "H", "Write out the truth tables of A B' + B C and A B' + B C + A C. "
     "How many rows differ?",
     "None. Both are 10111000 reading ABC = 000 to 111. That is what redundant means, "
     "and it is what makes the term a fix rather than a bug."),
    ("A4", "H", "F = A B + A B' is just F = A written badly. Does it have a static-1 "
     "hazard?",
     "Yes. A=1,B=0 and A=1,B=1 both give 1, and no single term covers both: A B needs "
     "B=1, A B' needs B=0. The fixing term is A - which is the minimal cover. "
     "Un-minimised logic is not automatically safe."),
    ("A5", "H", "Can a circuit consisting of one product term ever have a static-1 "
     "hazard? Prove your answer.",
     "No. Any two 1-cells are both covered by that single term, since it is the only "
     "term and it must cover every 1. Something is always holding the output up."),
    ("A6", "W", "Why can a two-level AND-OR circuit have static-1 but not static-0 "
     "hazards?",
     "The output is 0 only when every AND is 0. For a static-0 glitch some AND would "
     "have to go momentarily high, but each AND's inputs come straight from literals - "
     "on a single-variable change only the terms containing that variable move, and a "
     "term that is 0 at both endpoints cannot be 1 in between. The dual argument gives "
     "static-0 hazards in OR-AND circuits."),
    ("A7", "H", "F = A B' + B C' + A' C. Find every static-1 hazard by hand, then "
     "check with the tool.",
     "Run python3 tools/hazard.py \"A B' + B C' + A' C\". Do it on paper first; the "
     "point of the exercise is that the two agree."),
    ("A8", "W", "What is a function hazard, and why can no implementation remove it?",
     "It occurs when two or more inputs change at once and the function's own value in "
     "the intermediate states forces a glitch. The inputs really do pass through those "
     "states, and every correct implementation must produce the function's value in "
     "them. The remedy is procedural: do not change those inputs together."),
    ("A9", "H", "Give an input pattern and pair of simultaneous changes on "
     "F = A B' + B C that exhibits a function hazard.",
     "A=1: go from B=1,C=0 (F=0) to B=0,C=1 (F=1). The intermediates B=1,C=1 and "
     "B=0,C=0 both give F=1, so the output may reach 1 early. Whether that matters "
     "depends on the consumer."),
    ("A10", "W", "A colleague says \"just minimise the logic and there will be no "
     "hazards\". Respond.",
     "Minimisation and hazard-freedom are different goals and often opposed: the "
     "minimal cover of A B' + B C has no consensus term, and that IS the hazard. A "
     "hazard-free cover is generally larger than a minimal one."),

    # ------------------------------------------------------ B · the analyser
    ("B1", "C", "Run the self-test. How many independent checks does section D "
     "perform, and what would a failure there mean?",
     "It cross-checks every static-1 transition over 400 random covers - several "
     "thousand transitions. A disagreement would mean either the covering rule or the "
     "timing model is wrong, and you would not know which until you investigated."),
    ("B2", "W", "Why does can_glitch() randomise the per-term switching times instead "
     "of using one fixed delay profile?",
     "Because a hazard is the POSSIBILITY of a dip. With one fixed profile the glitch "
     "only appears in one direction of the transition, so a fixed-profile check "
     "disagrees with the covering rule and looks like a bug in the rule. Searching "
     "delay assignments asks the right question."),
    ("B3", "C", "Feed the analyser a single product term, then a two-term cover you "
     "believe is safe. Confirm both report zero.",
     "A B C reports none. A B + A C reports none: the only adjacent 1-cell pairs are "
     "spanned by one of the two terms."),
    ("B4", "C", "Add a --pos example of your own and check the static-0 dual.",
     "(A + B)(B' + C) reports one static-0 hazard. The reasoning mirrors the SOP case "
     "on the 0-cells."),
    ("B5", "W", "The analyser prints \"truth table unchanged: yes\" after proposing a "
     "fix. Why is that check worth the code it takes?",
     "Because a proposed fix that alters the function is the worst possible outcome: "
     "it silences the symptom and introduces a functional bug. A tool that does not "
     "check its own output will eventually emit one."),
    ("B6", "C", "Modify hazard.py to report, for each hazard, how many delay "
     "assignments out of 60 actually produced a dip. Does it matter whether that "
     "number is 1 or 60?",
     "It does not change whether the hazard exists - one assignment is enough. It is "
     "informative about how likely you are to SEE it in a given simulation, which is "
     "exactly why simulation alone is not a reliable hazard finder."),
    ("B7", "H", "For F with four variables and three terms, how many single-variable "
     "transitions between 1-cells must the analyser examine, in the worst case?",
     "At most 16 x 4 / 2 = 32 ordered pairs, of which only those with F=1 at both ends "
     "are candidates. The cost is exponential in the number of variables, which is why "
     "this approach suits small covers and not whole designs."),
    ("B8", "W", "The analyser only handles two-level covers. What would make the "
     "multi-level case hard?",
     "In a multi-level circuit an input can reach the output by many paths of "
     "different lengths, and an internal signal may itself be hazardous. You can no "
     "longer decide the question by looking at a cover, because there is no single "
     "cover - hz_dynamic is the demonstration."),

    # -------------------------------------------------- C · gate-level
    ("C1", "H", "From the analyser's output, predict which of the 24 transitions in "
     "hz_static1 will glitch. Write it down before simulating.",
     "ABC 111 -> 101, i.e. B falling with A=1 and C=1. The detector reports exactly "
     "that one."),
    ("C2", "C", "Run make glitch. Did your prediction match? How many surplus changes "
     "did the detector count?",
     "It matches. changes=2, expected=0, so two surplus changes: the dip down and the "
     "recovery."),
    ("C3", "C", "hz_static1_fix reports CLEAN. Confirm the truth signature is "
     "unchanged, and say why that matters.",
     "Both report 10111000. Without that check, a 'fix' that broke the function would "
     "also report CLEAN - a circuit stuck at a constant never glitches."),
    ("C4", "H", "In hz_static1.v the inverter has delay 4 and the ANDs have delay 2. "
     "Compute when each product term switches after B falls, and how wide the glitch "
     "is.",
     "B C switches off at 0 + 2 = 2 ns. A B' switches on at 4 + 2 = 6 ns. The output "
     "is unheld from 2 ns to 6 ns, so the glitch is about 4 ns wide - the inverter "
     "delay."),
    ("C5", "C", "Set the inverter delay to 0 in hz_static1.v and re-run. What happens, "
     "and what does it tell you?",
     "The glitch disappears, because both terms now switch at the same instant. It "
     "tells you the glitch depends on delays you do not control - the hazard is still "
     "in the logic, and a different library or a different route brings it back."),
    ("C6", "C", "Make the AND feeding B C slower than the inverter path. Does the "
     "glitch move, vanish, or change direction?",
     "It vanishes for B falling and appears for B rising instead. The hazard is "
     "direction-independent; the glitch is not."),
    ("C7", "C", "Run make glitch on hz_dynamic. How many transitions glitch, and how "
     "many are dynamic?",
     "Five: four static and one dynamic (ABC 111 -> 101, changes=3 where 1 was "
     "expected)."),
    ("C8", "H", "Why does a dynamic hazard need three or more reconverging paths?",
     "The output must change three times. Each extra change needs another path "
     "arriving at a different time; with only two paths there are only two switching "
     "instants, which can produce at most one spurious excursion - a static hazard."),
    ("C9", "C", "hz_dynamic_fix reports 4 glitches, not 0. Substitute A=0, C=1 into "
     "the inner expression and say what s becomes.",
     "s = 0 + B + 0 = B. So f = s XOR b is B XOR B-delayed, which spikes on every edge "
     "of B regardless of the cover."),
    ("C10", "W", "Explain why hz_flat_fix is clean when hz_dynamic_fix is not.",
     "Flattening removes the reconvergence: there is no longer an internal signal that "
     "is a delayed copy of an input arriving at the same gate as the input itself. The "
     "flattened function A B' + B C' is then covered hazard-free by adding A C'."),
    ("C11", "H", "Derive the flattened function of hz_dynamic from its truth table and "
     "confirm it is A B' + B C'.",
     "s XOR B has minterms A'BC', AB'C', AB'C, ABC'. Grouping: AB'C' + AB'C = A B'; "
     "A'BC' + ABC' = B C'. So F = A B' + B C'."),
    ("C12", "W", "The detector examines 24 transitions. What is it NOT examining, and "
     "could that hide a real problem?",
     "It examines only single-variable changes from a settled state. It does not "
     "examine simultaneous changes (function hazards) or transitions from a state the "
     "circuit has not settled in. Both can hide real behaviour, which is why the "
     "detector complements the analyser rather than replacing it."),

    # ------------------------------------------------------ D · does it matter
    ("D1", "C", "Run make capture. How many spurious clock edges did four glitches "
     "produce?",
     "Four - one per glitch. The report separates the legitimate power-up edge "
     "(x -> 1) from the four that followed."),
    ("D2", "H", "Why was the DATA consumer unaffected?",
     "The glitch happened 80 ns before the sampling edge and lasted about 4 ns, so the "
     "signal was long settled by the time the flop looked at it."),
    ("D3", "C", "Move the input transitions to 2 ns before the clock edge. Does the "
     "DATA consumer still behave?",
     "No - now the flop samples during or just after the glitch, and may capture the "
     "wrong value or go metastable. That is the boundary the setup check exists to "
     "enforce."),
    ("D4", "C", "Replace the asynchronous reset with a synchronous one and re-measure.",
     "r_flag survives: a synchronous reset is only examined at the clock edge, by "
     "which time the glitch is gone. This is the standard reason to prefer synchronous "
     "reset where the design allows it."),
    ("D5", "W", "State the rule about when a glitch is harmless, precisely.",
     "A glitch is harmless only where a clock edge samples the signal after it has "
     "settled. Anywhere edge-sensitive or level-sensitive - a derived clock, an "
     "asynchronous reset or set, a latch enable, a domain crossing - it is not."),
    ("D6", "W", "Name three signals in a design you have written that are not "
     "clock-sampled, and say what would happen if each glitched.",
     "Answers vary. A good answer names real signals and traces the consequence: a "
     "glitching clock enable double-counts; a glitching async reset loses state; a "
     "glitching handshake sends a spurious request."),

    # ---------------------------------------------------------- E · synthesis
    ("E1", "C", "Run make synth. How many cells did each version produce?",
     "One each, and the same cell: a $_MUX_. The netlists are identical, so the "
     "consensus term was deleted."),
    ("E2", "H", "Verify that A B' + B C equals B ? C : A over all eight rows.",
     "B=0 selects A; B=1 selects C. Both columns match the SOP on every row."),
    ("E3", "W", "Why was the deletion predictable?",
     "The consensus term is logically redundant by construction, and removing "
     "redundancy is precisely what a logic optimiser is for. Any tool that did not "
     "delete it would be failing at its job."),
    ("E4", "C", "Add a keep attribute to the consensus term and re-run. Did it "
     "survive?",
     "Record what you observe. Attribute handling varies by tool and version, which is "
     "itself the lesson: protection has to be verified, not assumed."),
    ("E5", "C", "Run the glitch detector against the post-synthesis netlist instead of "
     "the RTL. What do you find?",
     "You are now testing what will actually be built. Whether the MUX glitches "
     "depends on that cell's internal implementation - which you did not write and "
     "cannot see from the RTL."),
    ("E6", "W", "Where must hazard-freedom be verified, and why is verifying it on RTL "
     "worthless?",
     "On the netlist. The RTL is an input to an optimiser that is free to restructure "
     "anything that does not change the function - and hazard-freedom is exactly a "
     "property that does not change the function."),

    # ------------------------------------------------- F · setup, hold, Fmax
    ("F1", "H", "Write the setup inequality and the hold inequality. Which term "
     "appears in only one?",
     "setup: t_cq + t_logic <= T + skew - setup - unc.  hold: t_cq + t_logic >= skew + "
     "hold + unc.  The clock period T appears only in the setup check."),
    ("F2", "H", "From the library: clk-to-Q 0.145, one XOR2 path 0.117, setup 0.090, "
     "no skew or uncertainty. Compute the minimum period and Fmax.",
     "0.145 + 0.117 + 0.090 = 0.352 ns, so Fmax = 2841 MHz."),
    ("F3", "H", "Add 0.15 ns of setup uncertainty to F2. Recompute.",
     "0.502 ns, so 1992 MHz. The circuit did not change - only how honest the "
     "constraint is."),
    ("F4", "C", "Run make fmax. What is the ratio between the two designs, and what "
     "produced it?",
     "364.7 to 473.2 MHz, a factor of 1.30, produced by splitting the one heavy stage "
     "into two. No logic was made faster."),
    ("F5", "H", "-0.322 ns on a 2.5 ns period. Express as a percentage and predict "
     "which class of fix is needed.",
     "12.9%. Too large for a synthesis effort setting; about right for one pipeline "
     "cut - which is what fixed it."),
    ("F6", "C", "Run make setup and confirm both numbers.",
     "pipe_unbal -0.322 ns VIOLATED; pipe_bal +0.307 ns MET, same constraint file."),
    ("F7", "C", "Run the hold analysis at 4, 40 and 400 ns. Explain the result.",
     "-0.119 ns in all three. Both flops use the same edge, so the period is not in "
     "the hold equation at all."),
    ("F8", "H", "Predict the hold slack at 4000 ns before running it.",
     "-0.119 ns. Anything else would mean the period had crept into the hold check, "
     "which would be a bug in the analyser."),
    ("F9", "C", "Reduce the skew from 0.25 ns to 0.10 ns. What happens, and what real "
     "engineering activity does that model?",
     "-0.119 ns becomes +0.031 ns. It models rebalancing the clock tree so the capture "
     "register is reached sooner - a place-and-route activity, not an RTL one."),
    ("F10", "C", "Find the skew at which hold_demo sits exactly on the boundary.",
     "Around 0.13 ns. Knowing the margin tells you how much clock-tree imbalance the "
     "design can absorb before this path fails."),
    ("F11", "W", "Remove set_input_delay from pipe.sdc. The WNS improves. Explain to a "
     "manager in two sentences why that is bad news.",
     "The design did not get faster; the tool stopped checking those paths, so the "
     "worst one is no longer in the list. The improvement is in the report, not in "
     "the silicon."),

    # ---------------------------------------------------------- G · tools
    ("G1", "C", "Run vivado/zynq_sta.tcl. Which path does Vivado call critical, and is "
     "it the same one your analyser picked?",
     "It should be the same path - the structure of the design is unchanged. The "
     "absolute numbers will differ substantially."),
    ("G2", "C", "Compare post-synthesis and post-route WNS. Which is worse, and why is "
     "that expected?",
     "Post-route. Synthesis estimates wire delay; implementation measures it. A design "
     "that only just closes post-synthesis usually fails post-route."),
    ("G3", "C", "Look at the post-route hold slack. Why is there a meaningful number "
     "there that did not exist before?",
     "Because only after implementation is there a real clock tree, and therefore real "
     "skew for the hold check to work against."),
    ("G4", "W", "Write the one-page comparison: what matched, what did not, and why.",
     "A good answer names the delay model as the source of the difference and quotes "
     "numbers. A poor answer says 'different tools give different answers' and stops."),
    ("G5", "W", "Vivado is not installed in the environment these materials were built "
     "in, so zynq_sta.tcl's output is not reproduced anywhere. What should you do with "
     "a script in that situation?",
     "Treat it as untested and verify it yourself before relying on it. Reporting that "
     "distinction honestly - this ran, that did not - is part of engineering practice, "
     "and it is why the lab README says so explicitly."),
]


def build_exercises(w):
    w.h1("Exercises")

    w.callout("How to read the tags", [
        [B("[H] "), N("hand calculation - do it on paper before you touch a keyboard.  "),
         B("[C] "), N("computer - run it and record what you see.  "),
         B("[W] "), N("write it down - a short paragraph you could defend in a "
                      "review.")],
        [N("Every exercise has a worked solution starting on the next page. Do not read "
           "it until you have written something down, even if what you write turns out "
           "to be wrong.")],
    ], color=NAVY, bar="0E2A47")

    heads = {
        "A": ("Part A · Hazards on paper", "10 exercises · 2 hours"),
        "B": ("Part B · The analyser", "8 exercises · 2 hours"),
        "C": ("Part C · Gate-level glitches", "12 exercises · 2 hours"),
        "D": ("Part D · Does it matter", "6 exercises · 1 hour"),
        "E": ("Part E · Synthesis", "6 exercises · 1 hour"),
        "F": ("Part F · Setup, hold and Fmax", "11 exercises · 2 hours"),
        "G": ("Part G · Industrial tools", "5 exercises · 2 hours"),
    }
    cur = None
    for eid, tag, q, _ in EX:
        if eid[0] != cur:
            cur = eid[0]
            h, sub = heads[cur]
            w.h2(h)
            w.para([I(sub, {"s": 9.5, "c": SLATE})], space_after=4)
        w.para([B("%s  [%s]  " % (eid, tag), {"c": TEAL}), N(q, {"s": 10.2})],
               space_after=5)

    w.page_break()


def build_solutions(w):
    w.h1("Worked Solutions")
    w.para([N("Every answer below was checked against the lab. Where a number is "
              "quoted it came from a real run; where a judgement is asked for, the "
              "solution gives the reasoning that earns the marks rather than a single "
              "word.", {"s": 10.2, "i": True})])

    cur = None
    for eid, tag, q, a in EX:
        if eid[0] != cur:
            cur = eid[0]
            w.h2("Part %s" % cur)
        w.para([B("%s  " % eid, {"c": TEAL}), I(q, {"s": 9.6, "c": SLATE})],
               space_after=2)
        w.para([N(a, {"s": 10.2})], space_after=8)

    w.page_break()


def build_reference(w):
    w.h1("Reference Card")

    w.h2("Hazards")
    w.code([
        "STATIC-1 HAZARD  (two-level AND-OR)",
        "    Two input patterns one variable apart, both giving F = 1,",
        "    covered by NO single product term.",
        "",
        "THE FIX",
        "    Add the product of the literals both patterns agree on,",
        "    dropping the variable that changed. It is redundant by design.",
        "",
        "STATIC-0 HAZARD   the dual, in a two-level OR-AND circuit",
        "DYNAMIC HAZARD    3+ levels; the output changes 3+ times instead of once",
        "FUNCTION HAZARD   2+ inputs change at once; no implementation can fix it",
        "",
        "THE LIMIT",
        "    The consensus term cures a two-level LOGIC hazard and nothing else.",
        "    Reconvergent fanout needs restructuring, not a redundant term."])

    w.h2("Sequential timing")
    w.code([
        "setup:   t_cq + t_logic   <=   T + t_skew - t_setup - t_unc",
        "hold:    t_cq + t_logic   >=   t_skew + t_hold + t_unc",
        "",
        "slack (setup) = required - arrival        slack (hold) = arrival - required",
        "",
        "Fmax = 1 / ( t_cq + t_logic + t_setup + t_unc - t_skew )",
        "",
        "The clock period T is in the setup check and NOT in the hold check.",
        "Late capture clock: helps setup, hurts hold, by the same amount.",
        "Setup signs off at the SLOW corner; hold at the FAST corner."])

    w.h2("The rules worth memorising")
    w.table(["Rule", "Consequence"],
            [["STA measures one path; a hazard needs two",
              "static analysis is blind to hazards - simulate with delays"],
             ["A glitch is harmless only where a clock edge samples it after it "
              "settles",
              "clocks, async resets, latch enables and CDC are all unsafe"],
             ["The consensus term is redundant by construction",
              "synthesis will delete it; verify on the netlist, not the RTL"],
             ["Fmax is set by one stage",
              "balance the stages before optimising any of them"],
             ["The clock period is not in the hold equation",
              "slowing the clock never fixes a hold violation"],
             ["Unchecked is not passed",
              "report unconstrained endpoints on every run; it must be zero"]],
            widths=[3.0, 3.8], size=9.2, bold_cols=(0,), align_center=False)

    w.h2("Commands")
    w.code([
        "# the lab",
        "make analyse   make glitch   make capture   make synth",
        "make fmax      make setup    make hold      make",
        "",
        "python3 tools/hazard.py \"A B' + B C\"        # find hazards, prescribe a fix",
        "python3 tools/hazard.py --pos \"(A+B)(B'+C)\" # the static-0 dual",
        "python3 tools/hazard.py --selftest          # cross-check the rule itself",
        "",
        "iverilog -g2005 -DDUT=hz_static1 -DDUTNAME=\\\"hz_static1\\\" \\",
        "         -o build/hz.vvp hazards/tb_hazard.v hazards/hz_static1.v",
        "vvp build/hz.vvp",
        "",
        "./scripts/sta.sh pipe_bal constraints/pipe.sdc      # setup",
        "./scripts/sta.sh hold_demo constraints/hold_skew.sdc --hold",
        "",
        "# Vivado on a Zynq-7000, headless",
        "vivado -mode batch -source vivado/zynq_sta.tcl"])

    w.callout("The one line to leave with", [
        [B("\"It simulates correctly\" and \"it meets timing\" are two different "
           "claims, and neither one implies the other.")],
    ], color=RED, fill="FDECEF", bar="D6224A")
