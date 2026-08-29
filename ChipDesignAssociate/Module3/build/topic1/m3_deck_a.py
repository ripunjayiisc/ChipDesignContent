# -*- coding: utf-8 -*-
"""Module 3 Topic 1 deck — front matter, outcomes, and Theory 1."""
import _boot
from deckkit import *

G = 91440


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ================================================================ title
    d.title_slide(
        "MODULE 3 · TOPIC 1",
        "Overview of VLSI STA",
        "Introduction to timing analysis  ·  Combinational circuit timing: races and "
        "hazards  ·  Sequential circuit timing: setup and hold  ·  Maximum frequency "
        "of operation  ·  Timing constraints for synthesis",
        ["Theory 1 · What timing analysis is, and what a truth table cannot tell you",
         "Theory 2 · Races and hazards — the new material, and most of the session",
         "Theory 3 · Setup, hold, maximum frequency, and real violations",
         "Theory 4 · Timing constraints for synthesis, and what synthesis does back",
         "Practical · Labs A–G · 12 hours · 58 exercises · Vivado on Zynq-7000"])

    # ==================================================== terminal outcomes
    s = d.slide("MODULE 3 · NOS NIE/ELE/N0103", "Terminal Outcomes")
    y = d.image(s, TOP - 45720, "terminal_outcomes", 4114800)
    d.card(s, y + G, "This subtopic is the foundation for both of them",
           [[R("Outcome 1 is built here and completed in subtopic 3. Outcome 2 needs "
               "the vocabulary and the diagnostic habits this subtopic establishes — "
               "you cannot write an ECO for a violation you cannot classify.",
               s=10.5)]],
           accent=NAVY, h=822960)

    # ==================================================== learning outcomes
    s = d.slide("MODULE 3 · TOPIC 1", "Key Learning Outcomes", accent=GREEN)
    y = d.image(s, TOP - 45720, "learning_outcomes", 4389120)
    d.lead(s, y + G, [[R("Every outcome on that slide is assessed by something you "
                         "run, not by something you recite.", b=True, c=GREEN,
                         s=11)]], h=365760)

    # ======================================================== syllabus map
    s = d.slide("TOPIC 1 · COVERAGE", "Every Syllabus Phrase, and Where It Is Covered")
    y = d.image(s, TOP - 45720, "syllabus_map", 4663440)
    d.lead(s, y + G, [[R("The genuinely new material in this subtopic is races and "
                         "hazards, so it is given the most room.", s=10.5)]],
           h=274320)

    # ======================================================== how it runs
    s = d.slide("TOPIC 1 · STRUCTURE", "How This Session Runs")
    y = d.image(s, TOP - 45720, "topic_structure", 4297680)
    d.card(s, y + G, "A note on overlap with Module 2 Topic 6",
           [[R("Setup, hold and constraints were taught there from the RTL designer's "
               "point of view. Here they return at gate level, as one half of a larger "
               "question — because a circuit can pass every timing check and still "
               "misbehave.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ===================================================== section THEORY 1
    d.section_slide(
        "THEORY 1", "What Timing Analysis Is",
        "A truth table tells you what a circuit computes. It says nothing at all "
        "about when.",
        ["Why a correct circuit can still be wrong",
         "The three questions timing asks",
         "Static analysis and dynamic simulation — two different questions",
         "The vocabulary the rest of the session assumes"])

    # ---------------------------------------------------------- motivation
    s = d.slide("1.1 · WHY", "A Circuit Can Be Correct and Still Be Wrong", accent=RED)
    y = d.lead(s, TOP, [[
        R("A truth table is a promise about ", s=12.5),
        R("settled values", b=True, c=NAVY, s=12.5),
        R(". It says that once everything has stopped moving, the output will be this. "
          "It makes no promise whatsoever about ", s=12.5),
        R("the journey", b=True, c=RED, s=12.5),
        R(" — and real gates take real time to make that journey.", s=12.5)]],
        h=685800)

    y = d.cols(s, y + G, [
        ("What the truth table guarantees",
         [[R("Given inputs A, B, C, the output will eventually be F.")],
          [R("Every row, every time.")],
          [R("This is what your RTL simulation checks.")]], GREEN, CARD_G),
        ("What it does not guarantee",
         [[R("That F goes there directly.")],
          [R("That F does not visit the wrong value first.")],
          [R("That F arrives before the next clock edge.")]], AMBER, CARD_A),
        ("And what neither one checks",
         [[R("Whether the value that mattered was sampled at the right instant.")],
          [R("A design can be functionally perfect and electrically unusable.")]],
         RED, CARD_R)],
        h=1737360)

    d.card(s, y + G, "Two failures that a functional simulation will never show you",
           [[R("1.  The output passes through a wrong value on its way to the right "
               "one — a HAZARD.")],
            [R("2.  The output arrives after the flip-flop needed it — a SETUP "
               "VIOLATION.")],
            [R("Both are invisible in a zero-delay simulation, because a zero-delay "
               "simulation has no delays to get wrong.", b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=1097280)

    # ------------------------------------------------ the three questions
    s = d.slide("1.2 · THE QUESTIONS", "Timing Analysis Asks Three Things")
    y = d.table(s, TOP,
                ["The question", "The failure if the answer is no", "Answered by"],
                [["Did the data arrive before the capturing edge needed it?",
                  "setup violation — the chip runs, but slower",
                  "static timing analysis"],
                 ["Did the data stay put long enough after that edge?",
                  "hold violation — the chip does not work at all",
                  "static timing analysis"],
                 ["Did the output pass through a wrong value on the way?",
                  "a hazard — a glitch, harmless or fatal depending on where it goes",
                  "simulation with delays"]],
                [4114800, 4297680, 2834640], rh=457200, bold_cols=(2,))

    y = d.card(s, y + G, "The first two are about ONE path. The third is about TWO.",
               [[R("Setup and hold ask how long a path is. A hazard asks what happens "
                   "when two paths of different length reconverge — so no measurement "
                   "of any single path can detect one.")],
                [R("That is why this topic needs two different tools on the same "
                   "circuit, and why a flow with only one of them has a blind spot.",
                   b=True, c=NAVY)]],
               accent=NAVY, h=1097280)

    d.lead(s, y + G, [[R("Module 2 Topic 6 answered the first two thoroughly. "
                         "This topic starts with the third.", b=True, c=TEAL,
                         s=11)]], h=274320)

    # ------------------------------------------------ static vs dynamic
    s = d.slide("1.3 · TWO TOOLS", "Two Tools, One Circuit, Two Different Questions")
    y = d.image(s, TOP - 45720, "sta_blind_to_hazards", 4663440)
    d.lead(s, y + G, [[R("Run STA on the hazard circuit and every path meets timing, "
                         "because every path does meet timing. The glitch is still "
                         "there.", b=True, c=RED, s=10.5)]], h=274320)

    # ----------------------------------------------------------- vocabulary
    s = d.slide("1.4 · VOCABULARY", "The Words the Rest of the Session Assumes")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["combinational logic", "output depends only on the present inputs"],
             ["sequential logic", "output depends on the inputs and on stored state"],
             ["propagation delay", "how long a gate takes to react to its input"],
             ["timing path", "a route from a start point to an end point, with a "
                             "delay"],
             ["arrival time", "when the data actually reaches a pin"],
             ["required time", "when it had to be there for the check to pass"],
             ["slack", "required minus arrival; negative means it does not fit"],
             ["setup time", "how long D must be stable BEFORE the clock edge"],
             ["hold time", "how long D must stay stable AFTER the clock edge"],
             ["clock skew", "the same edge reaching two registers at different "
                            "instants"],
             ["glitch", "a momentary wrong value on an output"],
             ["hazard", "a circuit's POTENTIAL to glitch, given unlucky delays"],
             ["race", "two signals changing where the order decides the outcome"]],
            [2926080, 8321040], rh=283464, bold_cols=(0,), size=10)

    # ---------------------------------------------- hazard vs glitch nuance
    s = d.slide("1.5 · A DISTINCTION", "Hazard and Glitch Are Not the Same Word")
    y = d.cols(s, TOP, [
        ("HAZARD",
         [[R("A property of the CIRCUIT.")],
          [R("It means: there exists an assignment of gate delays for which this "
             "output glitches.")],
          [R("You can find it by inspecting the logic, with no simulation at all — "
             "which is what tools/hazard.py does.")],
          [R("It is either there or it is not.", b=True, c=NAVY)]], VIOLET, CARD),
        ("GLITCH",
         [[R("An EVENT in one simulation.")],
          [R("It means: on this run, with these delays, the output actually moved when "
             "it should not have.")],
          [R("You can only see it by simulating with delays, and only on the "
             "transitions you stimulated.")],
          [R("It may or may not show up.", b=True, c=NAVY)]], TEAL, CARD)],
        h=2560320)

    d.card(s, y + G, "Why the distinction earns its keep",
           [[R("A circuit with a hazard may run for years without glitching, because "
               "the delays happened to fall the right way — until a new process "
               "corner, a new temperature, or a re-synthesis changes them. "
               "You remove hazards, not glitches.", b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=822960)
