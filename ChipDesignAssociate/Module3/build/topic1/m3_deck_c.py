# -*- coding: utf-8 -*-
"""Module 3 Topic 1 deck — Theory 3: sequential timing, Fmax, and real
setup/hold violations."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    d.section_slide(
        "THEORY 3", "Sequential Circuit Timing",
        "Once a clock is in charge, the question stops being \"did it glitch?\" "
        "and becomes \"had it finished glitching by the time the edge arrived?\".",
        ["The sampling window: setup and hold",
         "Maximum frequency of operation, derived rather than quoted",
         "A real setup violation and the fix that clears it",
         "A real hold violation, and why the clock frequency cannot help"],
        accent=NAVY)

    # -------------------------------------------------------- the window
    s = d.slide("3.1 · THE WINDOW", "A Flip-Flop Samples Over a Window, Not At an "
                                    "Instant")
    y = d.image(s, TOP - 45720, "setup_hold", 4389120)
    d.card(s, y + G, "Everything in this section comes from that one picture",
           [[R("Break the first half and the flop captures the previous value — a "
               "setup violation. Break the second and it captures the NEXT value, a "
               "whole cycle early — a hold violation.", s=10.5)]],
           accent=NAVY, h=868680)

    # --------------------------------------------------- the four terms
    s = d.slide("3.2 · THE FOUR TERMS", "What Consumes the Clock Period")
    y = d.table(s, TOP,
                ["Term", "What it is", "Who sets it"],
                [["clock-to-Q", "delay from the launching edge until Q is valid",
                  "the library cell"],
                 ["logic delay", "every gate and wire between the two flops",
                  "your design, and synthesis"],
                 ["setup time", "how early the capturing flop needs the data",
                  "the library cell"],
                 ["clock skew", "the difference in clock arrival between the two flops",
                  "the clock tree, after layout"],
                 ["uncertainty", "jitter, plus skew that is not modelled yet",
                  "you, in the constraint file"]],
                [2377440, 5486400, 3383280], rh=329184, bold_cols=(0,))

    y = d.code(s, y + G, [
        "setup:   t_cq + t_logic   <=   T + t_skew - t_setup - t_unc",
        "hold:    t_cq + t_logic   >=   t_skew + t_hold + t_unc",
        "",
        "#  the clock period T is in the first line and NOT in the second.",
        "#  everything surprising about hold follows from that one asymmetry."],
        size=10)

    d.card(s, y + G, "Note the sign on skew",
           [[R("A capture clock that arrives LATE gives the data more time, so it "
               "helps setup — and it eats hold margin by exactly the same amount. "
               "Every clock-tree decision trades one against the other.")]],
           accent=AMBER, fill=CARD_A, h=868680)

    # ------------------------------------------------------------- Fmax
    s = d.slide("3.3 · FMAX", "Maximum Frequency of Operation, Derived")
    y = d.image(s, TOP - 45720, "fmax_derivation", 4846320)
    d.lead(s, y + G, [[R("Not quoted from a datasheet — rearranged from the setup "
                         "inequality you just saw.", s=10.5)]], h=274320)

    s = d.slide("3.3 · FMAX", "Worked, With Real Numbers")
    y = d.code(s, TOP, [
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
        "The circuit did not change. Your honesty about the clock did."],
        size=9.5)

    d.card(s, y + G, "Which is why an Fmax figure without its assumptions is marketing",
           [[R("Ask what corner, what uncertainty, and whether it is post-synthesis or "
               "post-route. The same netlist will happily produce two numbers a factor "
               "of two apart under different answers to those three questions.")]],
           accent=RED, fill=CARD_R, h=822960)

    # ------------------------------------------------- Fmax is one stage
    s = d.slide("3.4 · ONE STAGE", "Fmax Is Set By One Stage — The Measurement")
    y = d.image(s, TOP - 45720, "fmax_one_stage", 4937760)
    d.lead(s, y + G, [[R("364.7 MHz to 473.2 MHz, by moving work rather than by making "
                         "anything faster.", b=True, c=GREEN, s=10.5)]], h=228600)

    s = d.slide("3.4 · ONE STAGE", "What Pipelining Costs, and What It Does Not")
    y = d.cols(s, TOP, [
        ("What you gain",
         [[R("A shorter longest path, so a faster clock.")],
          [R("Throughput is unchanged once the pipe is full — one result per cycle, "
             "still.")],
          [R("Measured here: 1.30x.")]], GREEN, CARD_G),
        ("What you pay",
         [[R("One more cycle of latency.")],
          [R("One more bank of registers — area and power.")],
          [R("And every control signal travelling beside the data must be delayed to "
             "match, or the design meets timing and computes the wrong answer.",
             b=True, c=RED)]], AMBER, CARD_A)],
        h=2103120)

    d.card(s, y + G, "The classic pipelining bug",
           [[R("You cut the datapath and forget to delay a valid flag, an operand or "
               "an address alongside it. Timing improves; correctness quietly does not. "
               "Every optimisation needs a functional re-check — which is why the "
               "Module 2 lab ends with make verify.")]],
           accent=RED, fill=CARD_R, h=822960)

    # ------------------------------------------------------ setup violation
    s = d.slide("3.5 · SETUP", "A Real Setup Violation, and the Fix That Clears It")
    y = d.image(s, TOP - 45720, "setup_violation", 4846320)
    d.lead(s, y + G, [[R("Same constraint file, same target, two versions of the same "
                         "arithmetic.", s=10.5)]], h=274320)

    s = d.slide("3.5 · SETUP", "Sizing the Problem Before Choosing the Fix")
    y = d.table(s, TOP,
                ["Slack as a fraction of the period", "What that usually means",
                 "Where to start"],
                [["under about 2%", "the tool nearly got there",
                  "check the constraint, then raise synthesis effort"],
                 ["2% to 10%", "a genuinely long path",
                  "restructure the logic, or retime"],
                 ["10% to 40%", "too much work in one cycle", "pipeline it"],
                 ["over about 40%", "the target is wrong for this technology",
                  "renegotiate the frequency, or change architecture"]],
                [3657600, 3657600, 3931920], rh=365760, bold_cols=(0,))

    y = d.card(s, y + G, "The measured case",
           [[R("−0.322 ns on a 2.5 ns period is 13% over budget. That is out of reach "
               "of a synthesis option and about right for one pipeline cut — which is "
               "exactly what fixed it. Doing this arithmetic first saves you from "
               "trying the cheap fixes on a problem too big for them.")]],
           accent=NAVY, h=1005840)

    d.lead(s, y + G, [[R("Change one thing per run, or you will not know which change "
                         "helped.", b=True, c=RED, s=10.5)]], h=274320)

    # ------------------------------------------------------- hold violation
    s = d.slide("3.6 · HOLD", "Hold Does Not Care What the Clock Period Is")
    y = d.image(s, TOP - 45720, "hold_violation", 4937760)
    d.lead(s, y + G, [[R("A hundred-fold change in frequency. Not one picosecond of "
                         "change in the violation.", b=True, c=RED, s=10.5)]],
           h=228600)

    s = d.slide("3.6 · HOLD", "Why It Is a Different Kind of Failure")
    y = d.cols(s, TOP, [
        ("SETUP violation",
         [[R("The data arrived too late for this clock.")],
          [R("Slow the clock down and the chip works.")],
          [R("You have shipped a less competitive product — but a working one.")],
          [R("Found at synthesis, and again after layout.")]], AMBER, CARD_A),
        ("HOLD violation",
         [[R("The data changed too soon after the same edge.")],
          [R("There is no clock frequency at which the chip works.")],
          [R("Reaching silicon with one means a re-spin.")],
          [R("Found only once a real clock tree exists.", b=True, c=RED)]],
         RED, CARD_R)],
        h=2377440)

    d.card(s, y + G, "So the fix is never the clock",
           [[R("It is the clock TREE — rebalance it so the capture register sees less "
               "skew — or the data path: insert delay. Measured here: dropping skew "
               "from 0.25 ns to 0.10 ns took the slack from −0.119 ns to +0.031 ns.")]],
           accent=GREEN, fill=CARD_G, h=822960)

    s = d.slide("3.6 · HOLD", "Why Hold Violations Turn Up So Late")
    y = d.image(s, TOP - 45720, "hold_why_late", 4023360)
    d.card(s, y + G, "What RTL can do about it: not make it impossible",
           [[R("No hand-gated clocks — use a clock enable. No unsynchronised domain "
               "crossings. No logic on an asynchronous reset. Beyond that, hold is "
               "place-and-route's job, and it has the one thing you do not: the real "
               "clock tree.", s=10.5)]],
           accent=NAVY, h=822960)

    # ------------------------------------------------- practical examples
    s = d.slide("3.7 · IN PRACTICE", "Practical Examples of Violations, and Their "
                                     "Solutions")
    d.table(s, TOP,
            ["Symptom", "Likely cause", "Solution"],
            [["one path fails, the rest are fine", "a genuinely long path",
              "restructure or pipeline that path"],
             ["one cell has a huge incremental delay", "high fanout or a weak driver",
              "set_max_fanout; let the tool buffer it"],
             ["fifty small cells in one path", "the logic is too deep",
              "balance it into a tree, then pipeline"],
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
              "constrain it properly — this is not a design bug"]],
            [3931920, 3383280, 3931920], rh=283464, bold_cols=(0,), size=9.5)

    # ------------------------------------------------------- checkpoint
    s = d.slide("THEORY 3 · CHECKPOINT", "Eight Questions", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "Write the setup inequality.",
                  "t_cq + t_logic <= T + skew - setup - uncertainty"],
                 ["2", "Which term is missing from the hold inequality?",
                  "the clock period T"],
                 ["3", "Setup violation — what does the chip do?",
                  "works, at a lower frequency"],
                 ["4", "Hold violation — what does it do?",
                  "does not work at any frequency"],
                 ["5", "Late capture clock helps which check?",
                  "setup; it hurts hold by the same amount"],
                 ["6", "Which stage sets Fmax?", "the slowest one, on its own"],
                 ["7", "−0.322 ns on a 2.5 ns period — how big a problem?",
                  "13%; pipeline territory, not a tool setting"],
                 ["8", "Why do hold problems appear after CTS?",
                  "before it there is no clock tree, so no real skew"]],
                [548640, 5029200, 5669280], rh=283464, bold_cols=(0,), size=9.5)
    d.lead(s, y + G, [[R("Theory 4 asks what synthesis does with everything you have "
                         "just decided.", b=True, c=GREEN, s=10.5)]], h=274320)
