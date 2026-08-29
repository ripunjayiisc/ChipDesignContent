# -*- coding: utf-8 -*-
"""Module 2 Topic 2 deck — Theory 3: the patterns every real block is built from."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 3", "The Patterns Every Block Is Built From",
        "Three structures account for almost all synthesisable RTL. Once you "
        "can recognise them, most designs stop looking unfamiliar.",
        ["Datapath and controller — the split that organises everything else",
         "The finite state machine, and the three-block way to write one",
         "Moore against Mealy, in structure and in measured timing",
         "State encoding, and what it actually costs",
         "Parameters, hierarchy and generate: from a module to an IP"],
        accent=VIOLET)

    # =============================================== datapath + controller
    s = d.slide("3.1 · THE SPLIT", "Datapath and Controller")
    y = d.image(s, TOP - 45720, "datapath_controller", 4950000)
    d.lead(s, y + G, [[R("A UART, a cache, a GPU. Different sizes, the same two "
                         "halves.", b=True, c=NAVY, s=12.0)]], h=228600)

    s = d.slide("3.1 · THE SPLIT", "The Worked Example: Accumulate N Samples")
    y = d.code(s, TOP, [
        "// the CONTROLLER decides.  Narrow. No data passes through it.",
        "always @(*) begin",
        "    acc_clr = 0; acc_en = 0; cnt_ld = 0; cnt_dec = 0; done = 0;",
        "    case (state)",
        "        S_IDLE : if (start)    begin acc_clr=1; cnt_ld =1; end",
        "        S_RUN  : if (!cnt_done) begin acc_en =1; cnt_dec=1; end",
        "        S_DONE :                     done   =1;",
        "    endcase",
        "end",
        "",
        "// the DATAPATH holds and transforms.  Wide. It decides nothing.",
        "always @(posedge clk or negedge rst_n)",
        "    if      (!rst_n)  sum <= 0;",
        "    else if (acc_clr) sum <= 0;",
        "    else if (acc_en)  sum <= sum + data;"], size=11.2)

    d.card(s, y + G, "Read the interface between them",
           [[R("Four control wires down, one status wire up. That is the entire "
               "contract. The controller never touches sum; the datapath never "
               "looks at state.", b=True, c=NAVY)]],
           accent=VIOLET, h=822960)

    s = d.slide("3.1 · THE SPLIT", "Measured, On the Accumulator")
    y = d.table(s, TOP,
                ["module", "cells", "flip-flops", "what it contains"],
                [["accum_ctrl", "10", "2", "three states, five control outputs"],
                 ["accum_datapath", "145", "24", "a 16-bit accumulator, an 8-bit "
                  "down-counter"],
                 ["accum_top", "156", "26", "both, plus the wires between them"]],
                [2560320, 1188720, 1463040, 6035040], rh=329184, bold_cols=(0,),
                col_colors={1: VIOLET})

    y = d.card(s, y + G, "Six per cent of the cells, one hundred per cent of the "
               "behaviour",
               [[R("That ratio is the whole argument for the split. You will "
                   "re-time, widen and pipeline the expensive half many times over "
                   "the life of a design — and each time, the half that decides "
                   "what happens stays exactly as it was.")],
                [R("It also means the part that is hardest to get right is the part "
                   "small enough to read in one sitting.", b=True, c=NAVY)]],
               accent=GREEN, fill=CARD_G, h=1097280)

    d.lead(s, y + G, [[R("make dpctrl  prints every control signal on every cycle, "
                         "next to the accumulated sum.", s=12.0)]], h=228600)

    # ============================================================== the FSM
    s = d.slide("3.2 · THE FSM", "The Three-Block Coding Pattern")
    y = d.image(s, TOP - 45720, "fsm_pattern", 4950000)
    d.lead(s, y + G, [[R("Every state machine in this lab is written exactly like "
                         "this. So is most industrial RTL.", s=12.0)]], h=228600)

    s = d.slide("3.2 · THE FSM", "Why Not One Block?")
    y = d.lead(s, TOP, [[R("You can write a working state machine in a single "
                           "clocked block, with the case statement inside it. "
                           "Nothing about it is illegal.", s=12.0)]], h=274320)

    y = d.table(s, y + G,
                ["", "one block", "three blocks"],
                [["works?", "yes", "yes"],
                 ["where is the reset?", "mixed in with the logic",
                  "block 1, and nowhere else"],
                 ["where is the clock?", "wrapped around everything",
                  "block 1, and nowhere else"],
                 ["outputs are", "registered, always",
                  "your choice — Moore or Mealy"],
                 ["reviewing a change", "you re-read the timing every time",
                  "blocks 2 and 3 have no timing to re-read"],
                 ["adding a state", "one place, easy to miss a branch",
                  "two places, both of them a case statement"]],
                [2743200, 4114800, 4389120], rh=310896, bold_cols=(0,), size=11.2)

    d.lead(s, y + G, [[R("One block is not wrong. Three blocks are easier to be "
                         "right in, which over a project is the same thing.",
                         b=True, c=NAVY, s=12.0)]], h=274320)

    s = d.slide("3.2 · THE FSM", "The Default Assignment, and Why It Matters",
                accent=GREEN)
    y = d.code(s, TOP, [
        "always @(*) begin",
        "    next_state = state;          // <-- THE DEFAULT ASSIGNMENT",
        "    case (state)",
        "        S_MAIN_GREEN  : if (car && timeout) next_state = S_MAIN_YELLOW;",
        "        S_MAIN_YELLOW : if (timeout)        next_state = S_SIDE_GREEN;",
        "        ...",
        "    endcase",
        "end",
        "",
        "// Not one of those if statements has an else.  Not one of them needs",
        "// one: next_state was already written, unconditionally, on line 2.",
        "// No path through this block leaves it unassigned, so no latch."],
        size=11.2)

    d.card(s, y + G, "This is the idiom the lab linter had to learn",
           [[R("A naive latch rule flags every one of those if statements. Yosys "
               "builds a latch in none of them. make lintcheck puts the two "
               "opinions side by side on sixteen designs — and a linter that cries "
               "wolf gets switched off, which makes it worse than no linter at "
               "all.")]],
           accent=GREEN, fill=CARD_G, h=1005840)

    # ========================================================= Moore/Mealy
    s = d.slide("3.3 · MOORE AND MEALY", "Where the Output Comes From")
    y = d.image(s, TOP - 45720, "moore_mealy", 4950000)
    d.lead(s, y + G, [[R("One structural difference — whether the output logic can "
                         "see the input. Everything else follows.", s=12.0)]],
           h=228600)

    s = d.slide("3.3 · MOORE AND MEALY", "The Differences, In One Table")
    y = d.image(s, TOP - 45720, "moore_mealy_table", 4950000)
    d.lead(s, y + G, [[R("Five rows. The last one is measured, not assumed.",
                         s=12.0)]], h=228600)

    s = d.slide("3.3 · MOORE AND MEALY", "The '101' Detector, Moore")
    y = d.image(s, TOP - 45720, "seq101_moore_states", 4950000)
    d.lead(s, y + G, [[R("Four states. The output is decoded from the state "
                         "register alone.", s=12.0)]], h=228600)

    s = d.slide("3.3 · MOORE AND MEALY", "The Same Detector, Mealy")
    y = d.image(s, TOP - 45720, "seq101_mealy_states", 4950000)
    d.lead(s, y + G, [[R("Three states. The output is written on the arrows, as "
                         "input / output.", s=12.0)]], h=228600)

    s = d.slide("3.3 · MOORE AND MEALY", "The One-Cycle Difference, Measured",
                accent=AMBER)
    y = d.image(s, TOP - 45720, "moore_mealy_timing", 4950000)
    d.lead(s, y + G, [[R("Five matches, zero mismatches against a golden model "
                         "computed from the stream itself.", b=True, c=GREEN,
                         s=12.0)]], h=228600)

    s = d.slide("3.3 · MOORE AND MEALY", "Choosing Between Them")
    y = d.tiers(s, TOP, [
        ("CHOOSE MOORE",
         "when the output leaves the block, drives other logic, or is timing "
         "critical. It comes out of a decode of registered bits, so it is clean, "
         "predictable and easy to constrain.", GREEN),
        ("CHOOSE MEALY",
         "when the cycle genuinely matters — a handshake that must be answered "
         "immediately, or a pipeline where one more cycle of latency costs "
         "throughput you cannot spare.", RED),
        ("EITHER WAY, REGISTER IT AT THE BOUNDARY",
         "A Mealy output that leaves your block hands the next designer a "
         "combinational path they did not ask for. If it crosses a module "
         "boundary, put a flip-flop on it — which turns it back into Moore.",
         NAVY)],
        h=1005840)

    d.card(s, y + G, "The trap in the folklore",
           [[R("\"Mealy needs fewer states\" is true and almost never the reason "
               "to pick it. Here it saved one flip-flop's worth of nothing — both "
               "machines needed two — and cost one cell more. The real trade is "
               "the cycle against the glitch-free output, and that is a system "
               "question, not a coding one.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ============================================================ encoding
    s = d.slide("3.4 · ENCODING", "The Choice You Make By Typing Numbers")
    y = d.image(s, TOP - 45720, "state_encoding", 4950000)
    d.lead(s, y + G, [[R("Same behaviour, different hardware — and the direction of "
                         "the difference is not the one usually quoted.",
                         b=True, c=RED, s=12.0)]], h=228600)

    s = d.slide("3.4 · ENCODING", "Which Encoding, and When")
    y = d.image(s, TOP - 45720, "state_encoding_choice", 4950000)
    d.lead(s, y + G, [[R("Three encodings, three different reasons. None of them "
                         "is a default.", s=12.0)]], h=228600)

    # =========================================================== the timer
    s = d.slide("3.5 · A CONTROLLER WITH A TIMER", "The Traffic Light")
    y = d.image(s, TOP - 45720, "traffic_states", 4950000)
    d.lead(s, y + G, [[R("Two safety properties, checked on every one of forty "
                         "cycles. Zero violations.", b=True, c=GREEN, s=12.0)]],
           h=228600)

    s = d.slide("3.5 · A CONTROLLER WITH A TIMER", "Checking a Property Instead of "
                "a Waveform", accent=GREEN)
    y = d.code(s, TOP, [
        "// P1 : the two roads are never green at the same time",
        "if (main_light == GREEN && side_light == GREEN) begin",
        "    $display(\"*** P1 VIOLATED at cycle %0d\", cycles);",
        "    errors = errors + 1;",
        "end",
        "",
        "// P2 : a green never goes straight to red - yellow comes first",
        "if (prev_main == GREEN && main_light == RED) begin",
        "    $display(\"*** P2 VIOLATED at cycle %0d\", cycles);",
        "    errors = errors + 1;",
        "end"], size=11.2)

    y = d.card(s, y + G, "You write the rule once; the simulator tests it every "
               "cycle of every run",
               [[R("This is the cheap half of formal verification, available in "
                   "any simulator, in about ten lines. It scales to runs far "
                   "longer than anyone would page through by hand, and it keeps "
                   "working after you change the design.")]],
               accent=GREEN, fill=CARD_G, h=868680)

    d.lead(s, y + G, [[R("The expensive half — proving the property holds for every "
                         "possible input — is what make prove does with a SAT "
                         "solver.", s=12.0)]], h=228600)

    # ============================================================== reuse
    s = d.slide("3.6 · FROM MODULE TO IP", "Parameters, Hierarchy and Generate")
    y = d.image(s, TOP - 45720, "hierarchy_generate", 4950000)
    d.lead(s, y + G, [[R("Eight flip-flops per stage, exactly N stages, measured at "
                         "four depths.", b=True, c=GREEN, s=12.0)]], h=228600)

    s = d.slide("3.6 · FROM MODULE TO IP", "What Elaboration Actually Does")
    y = d.code(s, TOP, [
        "module delayline #(parameter W = 8, parameter N = 4)",
        "                 (input clk, rst, en, input [W-1:0] din,",
        "                  output [W-1:0] dout);",
        "",
        "    wire [W-1:0] tap [0:N];      // one more element than stages",
        "    assign tap[0] = din;",
        "",
        "    genvar k;",
        "    generate",
        "        for (k = 0; k < N; k = k + 1) begin : stage",
        "            preg #(.W(W)) u_reg (.clk(clk), .rst(rst), .en(en),",
        "                                 .d(tap[k]), .q(tap[k+1]));",
        "        end",
        "    endgenerate",
        "",
        "    assign dout = tap[N];",
        "endmodule"], size=9)

    d.lead(s, y + G, [[R("The for loop is an instruction to the ELABORATOR, not a "
                         "loop in hardware. After elaboration there are N preg "
                         "instances and no loop anywhere.", b=True, c=NAVY,
                         s=12.0)]], h=274320)

    # ========================================================== checkpoint
    s = d.slide("THEORY 3 · CHECKPOINT", "Eight Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What are the two halves of almost every block?",
                  "a datapath that holds, a controller that decides"],
                 ["2", "What crosses between them?",
                  "control signals down, status signals up"],
                 ["3", "Name the three blocks of an FSM.",
                  "state register, next-state logic, output logic"],
                 ["4", "Why does a default assignment prevent a latch?",
                  "every output is written before any branch runs"],
                 ["5", "What does the output logic read in a Moore machine?",
                  "the state, and nothing else"],
                 ["6", "How much later does a Moore output appear?",
                  "exactly one clock cycle, every time"],
                 ["7", "One-hot: fewer or more flip-flops than binary?",
                  "more — one per state instead of log2(states)"],
                 ["8", "Does a generate loop exist in the netlist?",
                  "no — it is elaborated away before synthesis"]],
                [548640, 5029200, 5669280], rh=310896, bold_cols=(0,), size=11.0)
    d.lead(s, y + G, [[R("Theory 4 is about the notation — which turns out to be "
                         "the least important part.", b=True, c=GREEN, s=12.0)]],
           h=274320)
