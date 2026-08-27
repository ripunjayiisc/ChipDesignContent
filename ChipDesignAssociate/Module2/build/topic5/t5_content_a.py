# -*- coding: utf-8 -*-
"""Topic 5 deck — opening and 5a: functional verification techniques."""
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
    # ================================================================ title
    d.title_slide(
        "TOPIC 5",
        "RTL Simulation and Verification",
        "Functional verification techniques for RTL designs  ·  Introduction to test benches "
        "and testbench development  ·  Simulation and debugging of RTL designs",
        ["5a · Verification techniques — why, how much, and how you know when you are finished",
         "5b · Testbenches — structure, reference models, randomisation, coverage, assertions",
         "5c · Simulation and debugging — the event engine, waveforms, and a debugging procedure",
         "Tools · Vivado · ModelSim · Icarus + Verilator + GTKWave  ·  Labs V1–V6"])

    # ============================================================== roadmap
    s = d.slide("TOPIC 5 · ROADMAP", "What This Topic Covers, and Why It Is Bigger Than It Looks")
    y = d.lead(s, TOP, [[
        R("Topic 4 taught you to write RTL. Topic 5 asks the harder question: ", b=True,
          c=NAVY, s=12.5),
        R("how do you KNOW it works? ", b=True, c=AMBER, s=12.5),
        R("The syllabus gives this subtopic 6 theory hours; in industry it is where the "
          "majority of the engineering effort goes, and the practical component reflects that.",
          s=12.5)]], h=685800)

    y = d.table(s, y + G,
                ["Syllabus bullet — Topic 5", "Covered by", "Slides"],
                [["Functional verification techniques for RTL designs", "5a", "5–14"],
                 ["Introduction to test benches and testbench development", "5b", "15–46"],
                 ["Simulation and debugging of RTL designs", "5c", "47–56"],
                 ["Practical: validate RTL designs through simulation using test benches "
                  "and debugging techniques", "Labs V1–V6", "62–69"],
                 ["Practical: develop and execute test benches for comprehensive simulation "
                  "and debugging", "Tools + Labs", "57–69"]],
                [6217920, 3383280, 1645920], rh=329184, bold_cols=(1,))

    y = d.card(s, y + G, "Learning outcomes — by the end of this topic you can",
               [[R("· Write a self-checking testbench with a reference model, and say why each "
                   "check is there.")],
                [R("· Use constrained-random stimulus with seeds, and reproduce any failure "
                   "exactly.")],
                [R("· Define a functional coverage model and close it across a regression.")],
                [R("· Write assertions that catch a broken rule at the cycle it breaks.")],
                [R("· Debug an RTL failure by procedure rather than by guesswork.")]],
               accent=GREEN, fill=CARD_G, h=1509840)
    d.card(s, 5623560, "One sentence to open the session with",
           [[R("A testbench is not finished when it passes. It is finished when it would FAIL "
               "if the design were wrong — and this deck proves that with measured results.",
               b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=731520)

    # ============================================================ motivation
    s = d.slide("TOPIC 5 · MOTIVATION", "Why This Is Half the Job")
    y = d.lead(s, TOP, [[
        R("Verification is not a phase that follows design. ", b=True, c=NAVY, s=12.5),
        R("It is a separate discipline with its own tools, its own metrics and, on most teams, "
          "its own engineers — and it consumes more effort than the design itself.")]],
        h=548640)
    y = d.image(s, y + 45720, "why_verify", 3383280)
    d.card(s, y + G, "Why the cost curve is so steep",
           [[R("A bug is the same bug at every stage. What changes is what it costs to find and "
               "fix it. Lint reports it in one second with a file and a line number. The FPGA "
               "lab makes you re-synthesise, re-place and re-programme. Silicon makes you "
               "re-spin the mask set — months, and a great deal of money — and by then your "
               "customers have the part.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ============================================================ the gap
    s = d.slide("TOPIC 5 · THE PROBLEM", "You Cannot Test Everything — So What Do You Do?")
    y = d.lead(s, TOP, [[
        R("Exhaustive testing is impossible for anything real. ", b=True, c=NAVY, s=12.5),
        R("A single 32-bit adder has 2^64 input pairs; at a billion per second that is over "
          "500 000 years. The state space of a design with 100 flip-flops is larger than the "
          "number of atoms in the observable universe.")]], h=594360)
    y = d.image(s, y + 45720, "verification_gap", 3383280)
    d.card(s, y + G, "So verification is not proof — it is measured evidence",
           [[R("You choose the cases most likely to break it (directed), let a machine choose "
               "the ones you would not have thought of (random), state the rules so they are "
               "checked continuously (assertions), and then "),
             R("measure what you actually reached", b=True, c=GREEN),
             R(" (coverage). The last of those is what turns 'we tested it' into a number "
               "somebody can review.")]],
           accent=GREEN, fill=CARD_G, h=960120)

    # =============================================== SECTION 5A
    d.section_slide("SUBTOPIC 5A", "Functional Verification Techniques for RTL Designs",
                    "The methods, the metrics, and the argument for each one.",
                    ["The verification loop, and why it ends at coverage rather than at PASS",
                     "Directed, constrained-random, and where each one earns its place",
                     "Four ways to decide whether an answer was right",
                     "Code coverage and functional coverage — only one of them knows the spec",
                     "The verification plan, regression, and closure",
                     "Measured proof: three testbenches against five broken designs"],
                    accent=TEAL)

    # ============================================================ the loop
    s = d.slide("TOPIC 5A · THE LOOP", "The Verification Loop")
    y = d.lead(s, TOP, [[
        R("Notice where this loop ENDS. ", b=True, c=NAVY, s=12.5),
        R("Not at 'the simulation passed' — at 'coverage is closed'. A pass with unmeasured "
          "coverage tells you only that nothing broke in the cases you happened to run.")]],
        h=548640)
    y = d.image(s, y + 45720, "ver_flow", 3383280)
    d.cols(s, y + G, [
        ("The plan comes FIRST",
         [[R("Write the verification plan before the testbench, from the specification, and "
             "have it reviewed exactly as the design is reviewed. If you write the testbench "
             "first you will test what you happened to build, not what was asked for.",
             s=10.5)]], VIOLET, CARD),
        ("The loop closes on the holes",
         [[R("Coverage does not just report — it TELLS YOU WHAT TO DO NEXT. Every MISS is a "
             "specific piece of stimulus somebody has to write. That is why it is a loop and "
             "not a final report.", s=10.5)]], AMBER, CARD_A)], h=1188720)

    # ============================================================ directed vs random
    s = d.slide("TOPIC 5A · TECHNIQUES", "Directed and Constrained-Random")
    y = d.lead(s, TOP, [[
        R("These are not alternatives; they are different instruments. ", b=True, c=NAVY, s=12.5),
        R("Directed tests are precise and cheap and prove exactly what you meant. Random tests "
          "are broad and reach places you did not think of. A real project uses both, in that "
          "order.")]], h=594360)
    y = d.image(s, y + 45720, "directed_vs_random", 3200400)
    d.table(s, y + G,
            ["", "Directed", "Constrained-random"],
            [["You write", "the case AND the expected answer", "the constraints; a model gives the answer"],
             ["Cost per test", "high — one test, one case", "low — one test, thousands of cases"],
             ["Reproducible", "always", "yes, from the seed"],
             ["Finds", "what you thought of", "what you did not"],
             ["Use it for", "boundaries, reset, protocol corners", "volume, and the long tail"]],
            [2011680, 4023360, 5212080], rh=283464, bold_cols=(0,), size=10)

    # ============================================================ checkers
    s = d.slide("TOPIC 5A · CHECKING", "Four Ways to Decide Whether the Answer Was Right")
    y = d.lead(s, TOP, [[
        R("This is the single biggest determinant of how good a testbench is. ", b=True,
          c=NAVY, s=12.5),
        R("Not how many test cases it runs — how it decides whether each one was correct.")]],
        h=548640)
    y = d.image(s, y + 45720, "checker_taxonomy", 3566160)
    d.card(s, y + G, "The line that separates a testbench from a demonstration",
           [[R("If deciding whether the run was correct requires a human to look at a waveform, "
               "you cannot put it in a regression, you cannot run it overnight, and you will "
               "stop running it within a week. ", b=True, c=RED),
             R("The verdict must be a line of text a machine can grep for.")]],
           accent=RED, fill=CARD_R, h=868680)

    # ============================================================ coverage
    s = d.slide("TOPIC 5A · COVERAGE", "Code Coverage and Functional Coverage")
    y = d.lead(s, TOP, [[
        R("Coverage answers the question a passing test cannot: WHAT DID I ACTUALLY TEST? ",
          b=True, c=NAVY, s=12.5),
        R("There are two kinds, they measure different things, and you need both.")]], h=548640)
    y = d.image(s, y + 45720, "coverage_types", 3383280)
    d.card(s, y + G, "The trap that catches every team once",
           [[R("100% code coverage does not mean the design is verified. ", b=True, c=AMBER),
             R("It means every line you wrote was executed. It says nothing about the behaviour "
               "you FORGOT to write code for, nothing about whether the outputs were checked, "
               "and nothing about whether the FIFO ever went full. Functional coverage is the "
               "one written from the specification — and it is the one that says when you are "
               "finished.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ============================================================ plan
    s = d.slide("TOPIC 5A · THE PLAN", "The Verification Plan Is One Table")
    y = d.lead(s, TOP, [[
        R("A verification plan does not need to be a document. ", b=True, c=NAVY, s=12.5),
        R("It needs to be a table, written before the testbench, reviewed like the design, with "
          "one row per feature in the specification and a column that says how each is checked.")]],
        h=594360)
    y = d.image(s, y + 45720, "ver_plan", 3383280)
    d.cols(s, y + G, [
        ("Why writing it first matters",
         [[R("A plan written afterwards documents what you happened to build. A plan written "
             "first tells you what to build — and the gaps are visible while they are still "
             "cheap to close.", s=10.5)]], TEAL, CARD),
        ("Why the Status column matters",
         [[R("It is the only honest answer to \"are we done?\". Not \"the tests pass\" — "),
           R("\"these features are checked, by these mechanisms, and here are the ones that "
             "are not\".", b=True, c=GREEN, s=10.5)]], GREEN, CARD_G)], h=1188720)

    # ============================================================ bug filters
    s = d.slide("TOPIC 5A · THE FILTERS", "Each Stage Catches What the Previous One Cannot")
    y = d.lead(s, TOP, [[
        R("No single technique catches everything. ", b=True, c=NAVY, s=12.5),
        R("Each is a filter with a different mesh, and skipping one lets a whole class of bug "
          "through to the next — where it costs more.")]], h=548640)
    y = d.image(s, y + 45720, "bug_escape", 3200400)
    d.card(s, y + G, "Run them in cost order, every time",
           [[R("Lint is one second and catches width truncation and inferred latches. "
               "Simulation is a minute and catches wrong behaviour. Assertions cost nothing "
               "extra once written and catch a broken rule at the cycle it breaks. Coverage "
               "catches what was never exercised at all. Synthesis catches the structural "
               "surprises the simulator hid from you.")]],
           accent=TEAL, h=960120)

    # ============================================================ THE PROOF
    s = d.slide("TOPIC 5A · THE PROOF", "Three Testbenches, Five Broken Designs, One Table", RED)
    y = d.lead(s, TOP, [[
        R("Everything in this topic reduces to this experiment. ", b=True, c=NAVY, s=12.5),
        R("One correct FIFO and five copies with a single realistic bug each. All five lint "
          "clean, all five synthesise, and all five pass a testbench that most students would "
          "call finished.")]], h=594360)
    y = d.image(s, y + 45720, "clinic_matrix", 3657600)
    d.card(s, y + G, "Run it yourself in ten seconds",
           [[R("cd Topic5_Lab && ./scripts/clinic.sh", f=MONO_FONT, b=True, c=GREEN),
             R("   — every cell in that table is produced by that command, on the code in the "
               "lab folder. Show it to the room before you explain anything else; the rest of "
               "the topic is the explanation of why the numbers come out that way.")]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ============================================================ what changed
    s = d.slide("TOPIC 5A · READING THE TABLE", "What Actually Changed Between V1, V2 and V3")
    y = d.lead(s, TOP, [[
        R("The three testbenches do not differ in size or effort. ", b=True, c=NAVY, s=12.5),
        R("They differ in three specific decisions, and each decision is worth a row of that "
          "table.")]], h=548640)
    y = d.tiers(s, y + 45720, [
        ("V1  →  V2", "Stopped typing expected values by hand and built a REFERENCE MODEL — an "
                      "independent implementation of the specification. Once you have one, you "
                      "can check every cycle instead of the few you remembered. Then added the "
                      "boundary cases: fill to full, drain to empty, write while full, read "
                      "while empty. Result: 0 of 5 becomes 4 of 5.", GREEN),
        ("V2  →  V3", "Replaced hand-written stimulus with WEIGHTED RANDOM stimulus, seeded so "
                      "any failure reproduces exactly. The fifth bug only appears when a read "
                      "and a write are asserted together on an EMPTY FIFO — a combination no "
                      "directed test in V2 ever produces, and one nobody thinks to write. "
                      "Result: 4 of 5 becomes 5 of 5.", TEAL),
        ("V3  →  V4", "Added a COVERAGE MODEL, so a run that passes also reports what it "
                      "reached. Without it you cannot tell a thorough run from a lucky one — "
                      "and the write-heavy profile, which passes cleanly, never reaches empty "
                      "at all.", AMBER),
        ("V3  →  V6", "Added ASSERTIONS bound to the DUT, so a broken rule is reported at the "
                      "cycle it breaks with the name of the rule — rather than three hundred "
                      "cycles later, at an output, as a wrong number.", VIOLET),
    ], h=822960, gap=45720)

    # ============================================================ 5A checkpoint
    s = d.slide("TOPIC 5A · CHECKPOINT", "Eight Questions Before We Build Anything")
    d.lead(s, TOP, [[
        R("Ask the room. These are all conceptual — no code yet. ", b=True, c=NAVY, s=12.5),
        R("Answers are in workbook section T5-A.")]], h=411480)
    y = d.cols(s, 1554480, [
        ("Questions 1–4",
         [[R("1. Why is 100% code coverage not the same as \"verified\"?", s=10.5)],
          [R("2. A testbench passes on a design you know is broken. What does that tell you "
             "about the testbench?", s=10.5)],
          [R("3. Why must a reference model be written from the specification and not from the "
             "RTL?", s=10.5)],
          [R("4. What does the SEED give you that makes random stimulus usable in a "
             "regression?", s=10.5)]], TEAL, CARD),
        ("Questions 5–8",
         [[R("5. Name one bug an assertion catches earlier than a scoreboard, and one it cannot "
             "catch at all.", s=10.5)],
          [R("6. What is the difference between a coverage HOLE and a test FAILURE?", s=10.5)],
          [R("7. Why does a regression usually dump no waveforms?", s=10.5)],
          [R("8. Your random test has passed 10 000 seeds. Are you finished? What would you "
             "need to see?", s=10.5)]], GREEN, CARD_G)], h=2011680)
    d.card(s, y + G, "If question 2 or 8 gave the room trouble",
           [[R("Those two are the whole topic. Go back to the clinic table and run "),
             R("./scripts/clinic.sh", f=MONO_FONT, b=True, c=GREEN),
             R(" live before continuing — the measured result convinces people in a way that "
               "an argument does not.")]],
           accent=AMBER, fill=CARD_A, h=776224)
