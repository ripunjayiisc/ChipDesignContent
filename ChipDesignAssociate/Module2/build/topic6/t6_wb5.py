# -*- coding: utf-8 -*-
"""Topic 6 workbook — 62 graded exercises, worked solutions, reference card."""
import _boot
from wbkit import *
from t6_wb1 import B, N, I, M


# ---------------------------------------------------------------- the bank
# (id, tag, question, answer)
EX = [
    # ---------------------------------------------------------- A · model
    ("A1", "H", "A DFF (clk→Q 0.145, load_factor 0.013) drives one XOR2 input "
     "(cap 1.5). What is the clock-to-Q arc delay?",
     "0.145 + 0.013 × 1.5 = 0.1645 ns. Round as the engine does: 0.164 ns."),
    ("A2", "H", "The same DFF now drives four XOR2 inputs. What is the delay, and by "
     "what factor did it grow?",
     "Load = 4 × 1.5 = 6.0. Delay = 0.145 + 0.013 × 6.0 = 0.223 ns — 1.36× the "
     "single-load figure. The intrinsic term does not scale, which is why fanout hurts "
     "fast cells more than slow ones."),
    ("A3", "H", "An INV (0.021 / 0.012 / cap 1.0) drives eight INV inputs. Compare its "
     "delay with the single-load case.",
     "Single load: 0.021 + 0.012 × 1.0 = 0.033 ns. Eight loads: 0.021 + 0.012 × 8.0 = "
     "0.117 ns — 3.5× slower. This is the argument for set_max_fanout."),
    ("A4", "C", "Run make lib. Which cell has the largest intrinsic delay, and which "
     "has the largest load_factor?",
     "XNOR2 has the largest intrinsic (0.091 ns); XOR2 and XNOR2 share the largest "
     "load_factor (0.018 ns per unit load). Complex functions cost both."),
    ("A5", "W", "Why does a Liberty file give a cell an input capacitance as well as a "
     "delay?",
     "Because a cell's delay depends on what it drives. The input capacitance is what "
     "this cell contributes to its DRIVER's load — so the same number appears in two "
     "different calculations: once as this cell's own delay, once as part of the "
     "upstream cell's."),
    ("A6", "W", "Real Liberty files use a 2-D table indexed by input slew and output "
     "load. What does the slew axis capture that this model ignores?",
     "A slowly-rising input takes longer to cross the switching threshold, so the cell "
     "responds later and its own output transition is slower — which then slows the "
     "NEXT cell. Slew propagates. Ignoring it makes this model optimistic on long, "
     "lightly-driven nets."),

    # ---------------------------------------------------------- B · graph
    ("B1", "H", "How many nodes does a 2-input XOR gate contribute to the timing graph, "
     "and how many arcs?",
     "Three nodes (A, B, Y) and two arcs (A→Y and B→Y), each carrying the cell delay "
     "computed with the load on Y."),
    ("B2", "H", "Where is a cell's delay charged — on the net arc into it, or on the "
     "arc inside it? Why does the choice matter?",
     "On the arc inside it, input pin to output pin. Charge it on the incoming net arc "
     "and every report line attributes a delay to the wrong cell: you would read "
     "'u34/A  0.088' when the 0.088 belongs to u21's output."),
    ("B3", "H", "Why do net arcs carry zero delay in this model, and what is the real "
     "answer?",
     "Because the wire's RC delay is folded into the driving cell's load term. In "
     "reality a long net has its own delay, which after routing can exceed the cell "
     "delays entirely — which is why post-route timing differs from post-synthesis."),
    ("B4", "C", "Synthesise tiny.v and count the cells in build/tiny.json. Draw the "
     "graph by hand first, then compare node and arc counts.",
     "Three DFFs and one XOR2. Your drawing should have the same node count as the "
     "engine reports; if it does not, you have most likely forgotten the clock pins or "
     "the output port."),
    ("B5", "W", "Yosys names a cell $abc$95$auto$blifparse.cc:492:parse_blif$97. Why "
     "does the engine shorten this, and why is that not merely cosmetic?",
     "An unreadable report does not get read, and a report that does not get read finds "
     "no bugs. Legibility is a functional requirement of a diagnostic tool."),
    ("B6", "C", "Find the reg_label logic in sta.py. How does it recover the name "
     "'q_reg' from the JSON?",
     "By looking up the flop's Q net in the netnames section and appending _reg to the "
     "signal name — the same convention every commercial synthesiser uses."),
    ("B7", "H", "A node has three fan-in arcs with source arrivals 0.20, 0.31 and 0.28 "
     "and arc delays 0.05, 0.02 and 0.04. Give amax and amin.",
     "Candidates: 0.25, 0.33, 0.32. amax = 0.33 (setup); amin = 0.25 (hold)."),
    ("B8", "W", "Why must the graph be traversed in topological order, and what does it "
     "mean if you cannot produce one?",
     "A node's arrival is only correct once every predecessor is final. If no "
     "topological order exists there is a combinational loop — the design has a cycle "
     "with no register in it, which STA cannot analyse and which is almost always a bug."),

    # ---------------------------------------------------------- C · engine
    ("C1", "H", "p_reg/Q → u97 (XOR2) → q_reg/D. Compute the arrival at q_reg/D.",
     "0.145 + 0.013×1.5 = 0.164; 0.088 + 0.018×1.6 = 0.117; total 0.281 ns."),
    ("C2", "H", "With a 1.000 ns period and setup 0.090, what is the required time and "
     "the slack?",
     "Required 1.000 − 0.090 = 0.910 ns. Slack 0.910 − 0.281 = +0.629 ns, MET."),
    ("C3", "H", "Same path, period 0.35 ns. Slack?",
     "Required 0.350 − 0.090 = 0.260. Slack 0.260 − 0.281 = −0.021 ns, VIOLATED."),
    ("C4", "H", "At what period does that path have exactly zero slack, and what Fmax "
     "does that correspond to?",
     "Period = arrival + setup = 0.281 + 0.090 = 0.371 ns → 2695 MHz. The engine "
     "reports 2693.2 MHz from unrounded internals."),
    ("C5", "C", "Run make tiny. Confirm your C1–C4 answers against it.",
     "The report prints arrival 0.281, required 0.910, slack +0.629, longest path 0.371, "
     "Fmax 2693.2 MHz."),
    ("C6", "H", "Add 0.15 ns of setup uncertainty to C2. What happens to the slack, and "
     "why exactly that much?",
     "Slack falls to +0.479. Uncertainty is subtracted from the required time, so it "
     "moves the slack one-for-one — a useful sanity check that a tool is applying it."),
    ("C7", "W", "Why does every node carry both amax and amin?",
     "Setup needs the latest possible arrival; hold needs the earliest. Propagating only "
     "the max makes the hold check use the wrong number, and it will be wrong quietly."),
    ("C8", "C", "The report ends with 'UNCONSTRAINED: 2 endpoint(s) not checked'. Which "
     "two, and how would you remove the line?",
     "The output port q and the input port din: no output/input delay was set. Add "
     "set_input_delay and set_output_delay and the count goes to zero."),
    ("C9", "W", "Your engine says +0.629 and a commercial tool says +0.41 on the same "
     "RTL. Is one of them wrong?",
     "Neither, necessarily. Different libraries, different wire models, possibly "
     "different uncertainty. What SHOULD match is which path is critical and how the "
     "slack responds to a change in period. Chase a discrepancy in those, not in the "
     "absolute number."),
    ("C10", "W", "TNS is 'the sum of every negative slack'. Why not the average?",
     "An average hides the count. Two designs with average slack −0.2 ns are very "
     "different if one has three failing endpoints and the other three thousand. TNS "
     "preserves that, and the pair (WNS, TNS) tells you both how bad and how many."),

    # ---------------------------------------------------- D · constraints
    ("D1", "H", "Write create_clock for a 250 MHz clock on a port named clk_in, named "
     "core_clk.",
     "create_clock -name core_clk -period 4.000 [get_ports clk_in]"),
    ("D2", "H", "A design has a divide-by-4 built from flops. Why is a second "
     "create_clock the wrong answer?",
     "Two independent create_clock commands tell the tool the domains are unrelated, so "
     "paths between them are either unchecked or checked against a meaningless "
     "relationship. create_generated_clock keeps the derived relationship intact."),
    ("D3", "C", "Run sta.py on tiny with -p 1.0, then 0.5, then 0.35. Tabulate the "
     "slack and confirm it is linear in the period.",
     "+0.629, +0.129, −0.021. Each 0.5 ns of period is 0.5 ns of slack: the arrival "
     "time did not change, only the budget."),
    ("D4", "W", "Removing set_input_delay improves the WNS. Explain that to a manager "
     "in two sentences.",
     "It did not make the design faster; it stopped the tool from checking those paths, "
     "so the worst one is no longer in the list. The improvement is in the report, not "
     "in the silicon."),
    ("D5", "H", "An upstream chip has a clock-to-out of 2.2 ns max and the board trace "
     "adds 0.3 ns. Your period is 8 ns. Write the constraint and say how much is left "
     "for your logic.",
     "set_input_delay -clock clk -max 2.5 [get_ports din*]. You have 8.0 − 2.5 = 5.5 ns, "
     "minus your own setup time and uncertainty."),
    ("D6", "H", "The downstream chip needs data 1.8 ns before its edge; the trace adds "
     "0.4 ns. Write the output constraint.",
     "set_output_delay -clock clk -max 2.2 [get_ports dout*]."),
    ("D7", "W", "Give one legitimate and one illegitimate use of set_false_path, and "
     "state the test that separates them.",
     "Legitimate: a configuration register written only at boot, when the core is "
     "halted. Illegitimate: a path that fails and nobody has time to fix. The test: can "
     "you write one sentence explaining why the path cannot be exercised? If not, it is "
     "not a false path."),
    ("D8", "C", "Run make mcp. How many failing endpoints does the multicycle path "
     "remove, and how much RTL changed?",
     "Eleven failing endpoints go to zero, and no RTL changed at all. The design was "
     "always correct; the analysis was wrong."),
    ("D9", "H", "You write set_multicycle_path 6 -setup. What hold line must follow, "
     "and what happens if you omit it?",
     "set_multicycle_path 5 -hold. Omit it and the hold check measures against the "
     "distant capture edge, demanding nearly six cycles of data stability — hundreds of "
     "artificial hold violations after clock-tree synthesis."),
    ("D10", "W", "What must be true of the RTL before a multicycle path is honest?",
     "The capture register must actually be enabled only every Nth cycle, and its data "
     "inputs must be stable across all N cycles. Without the enable the constraint is a "
     "claim about hardware that does not exist."),
    ("D11", "C", "Edit constraints/add32.sdc to set the period to 2.0 ns. What breaks, "
     "and is it the design or the constraint?",
     "The adder path fails by a large margin. At 2.0 ns a 32-bit ripple chain genuinely "
     "does not fit — this one is the design, and the fix is pipelining or a different "
     "adder, not a constraint edit."),
    ("D12", "W", "Order these by how much damage a mistake in each does: create_clock, "
     "set_input_delay, set_false_path. Justify the order.",
     "set_false_path is worst — it silently removes a real check. create_clock is next: "
     "a wrong period scales every number, but at least every path is still analysed. "
     "set_input_delay is least damaging because its absence is visible in the "
     "unconstrained count, if you look."),

    # ---------------------------------------------------- E · setup closure
    ("E1", "C", "Run make sweep. What is the ns/bit for the 64-bit ripple chain, and "
     "what does the trend tell you?",
     "0.1233 ns/bit, converging downward towards a constant. Constant ns/bit means "
     "delay is linear in width — the definition of a ripple chain."),
    ("E2", "C", "What is the ns/bit for the 64-bit a+b under delay mapping, and why is "
     "the trend different?",
     "0.0362, and still falling. Falling ns/bit means sub-linear depth — the tool built "
     "a carry-lookahead or carry-select structure from a source file that never "
     "mentioned one."),
    ("E3", "H", "From the sweep, predict the 128-bit ripple delay. Then say how much "
     "confidence you have in the prediction.",
     "About 0.123 × 128 ≈ 15.7 ns. High confidence: the ns/bit has converged, and a "
     "chain has no mechanism to become sub-linear. The a+b prediction would be far less "
     "safe, since its ns/bit is still moving."),
    ("E4", "C", "Run make closure. Why is add_fast SLOWER than add_ripple under "
     "area-oriented mapping?",
     "4.615 ns against 4.094 ns. Area-oriented mapping optimises cell count, and the "
     "cheapest structure for a+b is a ripple chain built from slightly worse cells than "
     "the hand-written one. Idiomatic code lost, on that setting."),
    ("E5", "C", "Why does add_ripple get WORSE under delay mapping (5.258 ns)?",
     "The source already fixes the structure, so the mapper has nothing to restructure. "
     "The extra effort only re-covers the same chain, and lands on a slightly worse "
     "covering. More effort is not monotonically better."),
    ("E6", "W", "State the lesson of E4 and E5 in one sentence, and say what it implies "
     "for your coding style.",
     "\"Describe intent, not structure\" is only half the rule; the other half is \"and "
     "check what your tool did with it\". Write a + b, then measure — do not assume "
     "either that the tool will do well or that hand-coding will do better."),
    ("E7", "C", "Pipeline add_ripple at the halfway point. What Fmax do you get, and "
     "what did you pay?",
     "2.315 ns → 432 MHz, from 4.094 ns → 244 MHz: 1.8×. You paid one cycle of latency "
     "and 49 extra cells."),
    ("E8", "C", "Delete the two lines in add_ripple_pipe.v that delay the upper "
     "operands. What happens to the timing, and what happens to make verify?",
     "Timing is unchanged or slightly better — the design got smaller. make verify "
     "fails: stage 2 now combines this cycle's upper operands with last cycle's carry. "
     "This is why timing results mean nothing without functional verification."),
    ("E9", "H", "A path is 6.2 ns and the target period is 5.0 ns. Express the problem "
     "as a percentage and say which fixes are plausible.",
     "24% over. That is beyond what an effort setting will find (typically a few "
     "percent) and within reach of one pipeline cut (which roughly halves the path). "
     "Restructuring might do it if the path is a deep chain."),
    ("E10", "H", "A path is 5.05 ns against a 5.0 ns target. Same question.",
     "1% over. Try the constraint first, then a higher effort setting. Pipelining this "
     "would be enormous overkill and would cost a cycle of latency for 0.05 ns."),
    ("E11", "W", "Why is 'reduce the clock frequency' listed last rather than banned?",
     "Because it always works, and sometimes it is the right engineering answer — a "
     "product that ships at 180 MHz beats one that never ships at 200. It is last "
     "because it should be a decision someone takes deliberately, not one that happens "
     "by default when the deadline arrives."),
    ("E12", "W", "You improve WNS from −0.30 to −0.05 and TNS from −140 to −138. What "
     "actually happened?",
     "You fixed one path and nothing else. The WNS looks much better because the single "
     "worst path improved; TNS shows that the other ~500 failing endpoints are "
     "untouched. This design has a systemic problem and you have been polishing one "
     "corner of it."),

    # ------------------------------------------------ F · hold, exceptions
    ("F1", "H", "Write the hold equation and point at what is missing compared with "
     "setup.",
     "hold slack = arrival − skew − hold − uncertainty. The clock period is absent. That "
     "single absence is why the clock frequency is not a lever for hold."),
    ("F2", "C", "Run make hold. Why is the violation −0.165 ns?",
     "Arrival 0.164 (clk→Q into an unloaded net), minus skew 0.300, minus hold 0.035 = "
     "−0.171; the engine reports −0.165 from unrounded internals."),
    ("F3", "C", "Run hold_demo at 3 ns, 30 ns and 300 ns. Explain the result.",
     "The hold slack is identical in all three. Both flops are triggered by the same "
     "edge, so the period never enters the race."),
    ("F4", "H", "How much delay must be added to hold_demo's data path to reach zero "
     "slack, and how much did the two XOR cells actually add?",
     "0.165 ns to reach zero. The two XORs added enough for +0.071, so about 0.236 ns — "
     "consistent with two XOR2 delays of roughly 0.117 each."),
    ("F5", "W", "Why does place-and-route fix hold rather than synthesis?",
     "Synthesis has no clock tree, so it does not know the skew, so it cannot know which "
     "paths will fail hold. Place-and-route builds the tree, measures the skew and "
     "inserts buffers where they are actually needed."),
    ("F6", "W", "Name three things in RTL that make hold violations harder to fix and "
     "say why each one hurts.",
     "Hand-gated clocks (add uncontrolled skew the CTS cannot balance); unsynchronised "
     "clock-domain crossings (no buffering can fix a genuinely asynchronous capture); "
     "using both clock edges in one path (halves the budget for both checks)."),
    ("F7", "C", "Remove the if (tick) enable from slow_path.v and re-run make mcp. What "
     "does the report say, and what would silicon do?",
     "The report is still green — the tool believed the constraint. Silicon would latch "
     "a half-computed sum on the cycles the adder has not finished, producing wrong "
     "results intermittently and data-dependently."),
    ("F8", "W", "Explain why hold_fixed.v uses XOR gates fed by a real port rather than "
     "a chain of buffers with (* keep *).",
     "opt_clean deletes buffers whose output is a copy of their input, and keep_hierarchy "
     "with -flatten deletes them too. Only logic a real input can influence survives. "
     "It is a teaching device, not a style to copy — in a real flow place-and-route "
     "inserts hold buffers with knowledge of the actual clock tree."),
    ("F9", "H", "A path has setup slack +0.02 ns and hold slack +0.01 ns. Is it safe? "
     "What would you do?",
     "Technically met, practically not. Both margins are smaller than typical on-chip "
     "variation. Ask what uncertainty was used; if it was optimistic, this path is a "
     "silicon failure waiting for a temperature change."),

    # -------------------------------------------------------- G · tools
    ("G1", "C", "Run scripts/vivado_timing.tcl. Which path does Vivado call critical, "
     "and is it the same one your engine picked?",
     "It should be the same path — the design's structure is the same. The absolute "
     "numbers will differ substantially because the FPGA fabric is not cda_edu.lib."),
    ("G2", "C", "Compare Vivado's post-synthesis and post-route WNS. Which is worse, "
     "and why is that expected?",
     "Post-route is worse. Post-synthesis uses estimated wire delays; routing adds real "
     "ones. A design that only just closes post-synthesis usually fails post-route."),
    ("G3", "C", "Apply the multicycle path in XDC rather than SDC. What changed in the "
     "syntax, and what changed in the effect?",
     "Nothing in either — set_multicycle_path is standard SDC and XDC accepts it "
     "unchanged. That is the point of the exercise."),
    ("G4", "C", "Run make stdlib, then read the generated library in OpenSTA. What did "
     "the generator have to add that cda_edu.lib does not contain?",
     "Lookup-table templates, per-pin timing_sense (unateness), proper cell_rise/"
     "cell_fall and rise/fall_transition groups, an ff() group on each flop with "
     "clocked_on and next_state, and setup_rising/hold_rising constraint groups. The "
     "custom cda_* attributes are convenient but are not part of the standard."),
    ("G5", "W", "Write the one-page comparison: what matched between your engine and "
     "the industrial tool, what did not, and why.",
     "A good answer names the delay model as the source of the difference and gives a "
     "number — e.g. an Artix-7 LUT delay against this library's XOR2 at 0.088 ns, plus "
     "routing delay the model has none of. A poor answer says 'different tools give "
     "different answers' and stops."),
]


def build_exercises(w):
    w.h1("Exercises")

    w.callout("How to read the tags", [
        [B("[H] "), N("hand calculation — do it on paper before you touch a keyboard.  "),
         B("[C] "), N("computer — run it and record what you see.  "),
         B("[W] "), N("write it down — a short paragraph you can defend in review.")],
        [N("Every exercise has a worked solution starting on the next page. Do not read "
           "it until you have written something down, even if what you write is wrong. "
           "A wrong answer you committed to teaches more than a right answer you read.")],
    ], color=NAVY, bar="0E2A47")

    heads = {
        "A": ("Part A · The delay model", "6 exercises · 2 hours"),
        "B": ("Part B · The timing graph", "8 exercises · 3 hours"),
        "C": ("Part C · Arrival, required, slack", "10 exercises · 4 hours"),
        "D": ("Part D · Constraints", "12 exercises · 4 hours"),
        "E": ("Part E · Setup closure", "12 exercises · 5 hours"),
        "F": ("Part F · Hold and exceptions", "9 exercises · 4 hours"),
        "G": ("Part G · Industrial tools", "5 exercises · 3 hours"),
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
    w.para([N("Every answer below was checked against the lab. Where a number is quoted "
              "it came from a real run; where a judgement is asked for, the solution "
              "gives the reasoning that earns the marks rather than a single word.",
              {"s": 10.2, "i": True})])

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

    w.h2("The equations")
    w.code([
        "SETUP    arrival   =  clk_to_q  +  logic            (the LONGEST path)",
        "         required  =  period  +  skew  -  setup  -  uncertainty",
        "         slack     =  required  -  arrival",
        "",
        "HOLD     arrival   =  clk_to_q  +  logic            (the SHORTEST path)",
        "         required  =  skew  +  hold  +  uncertainty",
        "         slack     =  arrival  -  required",
        "",
        "         Fmax      =  1 / (longest path delay)",
        "         WNS       =  min(slack) over all endpoints",
        "         TNS       =  sum(slack) over endpoints where slack < 0",
        "",
        "         cell delay = intrinsic + load_factor x (output load)"])

    w.h2("The constraints")
    w.code([
        "create_clock -name clk -period 10.0 -waveform {0 5} [get_ports clk]",
        "create_generated_clock -name div2 -source [get_ports clk] \\",
        "                       -divide_by 2 [get_pins div_reg/Q]",
        "",
        "set_clock_uncertainty 0.15 -setup [get_clocks clk]",
        "set_clock_uncertainty 0.05 -hold  [get_clocks clk]",
        "",
        "set_input_delay  -clock clk -max 3.0 [get_ports din*]",
        "set_input_delay  -clock clk -min 0.5 [get_ports din*]",
        "set_output_delay -clock clk -max 2.5 [get_ports dout*]",
        "set_output_delay -clock clk -min 0.2 [get_ports dout*]",
        "",
        "set_false_path -from [get_ports rst_n]",
        "set_clock_groups -asynchronous -group [get_clocks a] -group [get_clocks b]",
        "",
        "set_multicycle_path N   -setup -from [get_cells x*] -to [get_cells y*]",
        "set_multicycle_path N-1 -hold  -from [get_cells x*] -to [get_cells y*]",
        "",
        "set_max_fanout 16 [current_design]"])

    w.h2("The commands")
    w.code([
        "# the lab",
        "make lib      make stdlib   make tiny     make sweep",
        "make closure  make hold     make mcp      make verify",
        "",
        "python3 sta/sta.py build/<top>.json <top> [-c file.sdc] [-p PERIOD]",
        "                   [--paths N] [--hold] [--csv]",
        "",
        "# Vivado, headless",
        "vivado -mode batch -source scripts/vivado_timing.tcl",
        "report_timing_summary -file rpt/summary.rpt",
        "report_timing -delay_type max -max_paths 10",
        "report_timing -delay_type min -max_paths 10",
        "",
        "# OpenSTA",
        "read_liberty lib/cda_edu_std.lib ; read_verilog netlist.v",
        "link_design <top> ; read_sdc constraints.sdc",
        "report_checks -path_delay max -digits 3"])

    w.h2("The diagnosis, in eight steps")
    w.table(["Step", "Do this"],
            [["1", "read the unconstrained-endpoint count — it must be zero"],
             ["2", "setup or hold? read the path type"],
             ["3", "read the startpoint and endpoint by name"],
             ["4", "ask whether the path is real"],
             ["5", "look at the largest incr in the path"],
             ["6", "compare WNS with TNS"],
             ["7", "apply the cheapest fix that could work"],
             ["8", "change ONE thing per run"]],
            widths=[0.6, 6.2], size=9.5, bold_cols=(0,), align_center=False)

    w.h2("The seven fixes for a setup violation, cheapest first")
    w.table(["#", "Fix", "Costs you"],
            [["1", "check the constraint", "minutes"],
             ["2", "raise the synthesis effort / delay-oriented mapping", "minutes, area"],
             ["3", "restructure the logic", "an hour, and a re-verification"],
             ["4", "pipeline", "a cycle of latency, and every parallel signal"],
             ["5", "retime", "nothing, when it is available"],
             ["6", "change the architecture", "real design work"],
             ["7", "slow the clock", "your product's performance, permanently"]],
            widths=[0.4, 3.6, 2.8], size=9.5, bold_cols=(0,), align_center=False)

    w.callout("The one line to remember", [
        [B("Unchecked is not passed. "),
         N("A timing report is a verdict on your design AND your constraints, and only "
           "one of those two is usually the problem.")],
    ], color=RED, fill="FDECEF", bar="D6224A")
