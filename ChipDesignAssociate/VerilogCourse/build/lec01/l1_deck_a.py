# -*- coding: utf-8 -*-
"""Lecture 01 deck — front matter, Theory 1 (why) and Theory 2 (the problem)."""
import _boot
from deckkit import *

G = 91440
ACC = {"NAVY": NAVY, "TEAL": TEAL, "GREEN": GREEN, "AMBER": AMBER,
       "VIOLET": VIOLET, "RED": RED, "SLATE": SLATE}
FILLS = {"NAVY": CARD, "TEAL": CARD, "GREEN": CARD_G, "AMBER": CARD_A,
         "VIOLET": CARD, "RED": CARD_R, "SLATE": CARD}


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 12.0)}
    d.update(kw)
    return d


def card_from(d, sld, y, table, key, size=12.0, h=None):
    """Render one of a diagram module's CARDS entries as a real slide card."""
    head, text, accent = table[key]
    col = ACC[accent]
    return d.card(sld, y, head, [[R(text, s=size)]], accent=col,
                  fill=FILLS[accent], h=h)


def build(d):
    # ======================================================== front matter
    d.title_slide(
        "HARDWARE MODELING USING VERILOG · NPTEL",
        "Lecture 01 — Introduction",
        "Prof. Indranil Sengupta · Department of Computer Science and "
        "Engineering · IIT Kharagpur   ·   expanded for the Chip Design "
        "Associate programme",
        ["Theory 1 · Why this course exists — the six objectives, and what a "
         "hardware description language actually is",
         "Theory 2 · The problem — complexity, Moore's Law, and why manual "
         "design was ruled out",
         "Theory 3 · The answer — a standardized design flow, and the CAD "
         "tools that walk it",
         "Theory 4 · The steps, one at a time — behavioural, data path, "
         "logic, physical, and the rest",
         "Practical · Five labs · install the toolchain, then check every "
         "claim in the lecture on your own machine"])

    s = d.slide("THE COURSE", "Where This Lecture Sits")
    y = d.image(s, TOP - 45720, "course_map", 4100000)
    d.card(s, y + G, "Eight weeks, forty-one lectures",
           [[R("Lecture 01 carries no Verilog syntax at all. Its job is to "
               "give you the map: what a VLSI design flow is, what each step "
               "of it produces, and why a language like Verilog has to exist "
               "at all. Everything in Weeks 2–8 is a detail of this picture.")]],
           accent=NAVY)

    s = d.slide("CHIP DESIGN ASSOCIATE · NOS NIE/ELE/N0102", "Terminal Outcomes")
    y = d.image(s, TOP - 45720, "terminal_outcomes", 4300000)
    d.card(s, y + G, "Outcome 1 is this lecture, almost word for word",
           [[R("\"Explain the design cycle of a VLSI circuit.\" That is the "
               "whole of Lecture 01. The remaining outcomes are opened here "
               "and closed over the rest of the module.")]],
           accent=NAVY)

    s = d.slide("LECTURE 01", "Learning Outcomes", accent=GREEN)
    d.image(s, TOP - 45720, "learning_outcomes", 5200000)

    s = d.slide("LECTURE 01 · COVERAGE",
                "The Original Lecture, and How This Session Expands It")
    d.image(s, TOP - 45720, "source_map", 5200000)

    s = d.slide("HOW TO USE THIS DECK", "Theory, Then Proof")
    y = d.tiers(s, TOP, [
        ("THEORY",
         "Four sections that follow the lecturer's own running order, slide "
         "by slide. Nothing has been reordered; material has only been added "
         "around what is already there.", NAVY),
        ("PRACTICAL",
         "Five labs. Every one of them is a command you run, and every number "
         "quoted in this deck came out of running them. If a slide states a "
         "figure, a lab produced it.", GREEN),
        ("WORKBOOK",
         "A companion document carries the full tutorial, the installation "
         "walkthrough, worked solutions and the exercises. The deck is for "
         "the room; the workbook is for afterwards.", TEAL)],
        h=1005840)
    d.lead(s, y + G, [[R("The notional slot for Lecture 01 is about half an "
                         "hour. This deck is deliberately longer: lecture from "
                         "the section openers to fit the slot, and let the "
                         "rest carry the labs and the self-study.",
                         b=True, c=NAVY)]], h=457200)

    # ================================================== THEORY 1 — the why
    d.section_slide(
        "THEORY 1", "Why This Course Exists",
        "The lecturer opens with six objectives. They are worth reading "
        "slowly, because between them they describe everything the next "
        "eight weeks will do.",
        ["The six objectives of the course, and what each one will mean",
         "What a hardware description language is",
         "And — more important — what it is not"])

    s = d.slide("1.1 · THE OBJECTIVES", "Main Objectives of the Course")
    d.image(s, TOP - 45720, "objectives", 5200000)

    s = d.slide("1.2 · WHAT AN HDL IS",
                "A Hardware Description Language Is Not a Programming Language",
                accent=RED)
    y = d.image(s, TOP - 45720, "hdl_not_program", 4250000)
    d.card(s, y + G, "The single most common beginner error",
           [[R("Reading Verilog as if it were C. It is not a list of steps to "
               "carry out; it is a description of something that exists all at "
               "once and stays there. Hold on to that and most of the "
               "confusion in Weeks 2 and 3 never happens.")]],
           accent=RED, fill=CARD_R)

    s = d.slide("1.2 · WHAT AN HDL IS", "The Same Three Lines, Side by Side")
    y = d.cols(s, TOP, [
        ("In C, this is a sequence",
         [[R("Three assignments, carried out one after another. After the "
             "first line runs, a is 1. Time passes between the lines.",
             s=11.5)]], RED, CARD_R),
        ("In Verilog, this is a circuit",
         [[R("Three pieces of wire, each permanently driven. There is no "
             "\"after\". All three statements are true at every instant the "
             "circuit is powered.", s=11.5)]], GREEN, CARD_G)],
        h=1188720)
    y = d.code(s, y + G, [
        "// C                      // Verilog",
        "a = 1;                    assign a = 1;",
        "b = 2;                    assign b = 2;",
        "c = 3;                    assign c = 3;",
        "",
        "// swap two lines and     // swap two lines and",
        "// the program changes    // NOTHING changes",
    ], size=12.5, title="the text looks similar; the meaning is not")
    d.lead(s, y + G, [[R("Hardware is not executed. It is built, and then it "
                         "sits there behaving.", b=True, c=NAVY, s=12.5)]],
           h=320040)

    # =========================================== THEORY 2 — the problem
    d.section_slide(
        "THEORY 2", "The Problem",
        "Before the flow and the tools and the language, the reason for all "
        "three: designs got far bigger, far faster, than anyone could follow "
        "by hand.",
        ["The complexity of VLSI circuits, and what drove it",
         "Moore's Law — and why it is an observation, not a law",
         "The requirements that conflict: area, speed, power",
         "Why manual design was ruled out, in arithmetic"],
        accent=AMBER)

    s = d.slide("2.1 · THE PROCESS", "VLSI Design Process")
    y = d.image(s, TOP - 45720, "design_complexity", 4150000)
    d.card(s, y + G, "Read the chain left to right",
           [[R("Each box is caused by the one before it. The last box — \"CAD "
               "tools need a language\" — is where Verilog enters, and it is "
               "the only reason this course has a subject.")]],
           accent=NAVY)

    s = d.slide("2.2 · THE SCALE", "The Scale Problem, in Numbers")
    d.image(s, TOP - 45720, "scale_compare", 5200000)

    s = d.slide("2.3 · MOORE'S LAW", "Moore's Law — Measured, Not Predicted")
    y = d.image(s, TOP - 45720, "moore_plot", 4350000)
    d.card(s, y + G, "What a straight line on a log scale means",
           [[R("Constant exponential growth. Every point is a real, published "
               "transistor count, and the dashed line is a plain doubling "
               "every two years anchored on the 4004 — drawn to show that the "
               "data really does track it over five decades.")]],
           accent=NAVY)

    s = d.slide("2.3 · MOORE'S LAW",
                "Why It Is an Observation, Not a Law of Physics", accent=VIOLET)
    d.image(s, TOP - 45720, "moore_economics", 5200000)

    s = d.slide("2.4 · THE TECHNOLOGY",
                "What Made It Possible — and Where It Stands Now")
    d.image(s, TOP - 45720, "tech_ladder", 5200000)

    s = d.slide("2.4 · THE TECHNOLOGY", "What a \"Nanometre\" Actually Is")
    d.image(s, TOP - 45720, "feature_size", 5200000)

    s = d.slide("2.5 · THE TRADE-OFF",
                "The Three Requirements That Fight Each Other", accent=AMBER)
    y = d.image(s, TOP - 45720, "tradeoff_triangle", 4250000)
    d.card(s, y + G, "This is why the flow has choices in it",
           [[R("If one design were simply best, a tool could find it and the "
               "job would be done. Because these three pull against each "
               "other, somebody has to decide which matters most — and that "
               "somebody is the designer, not the tool.")]],
           accent=AMBER, fill=CARD_A)

    s = d.slide("2.6 · THE CONSEQUENCE",
                "\"Manual Design Is Simply Ruled Out\"", accent=RED)
    d.image(s, TOP - 45720, "manual_impossible", 5200000)
