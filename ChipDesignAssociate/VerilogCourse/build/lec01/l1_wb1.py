# -*- coding: utf-8 -*-
"""Lecture 01 workbook — front matter, Part 1 and Part 2."""
import _boot
from wbkit import *
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL


def build(w):
    # ------------------------------------------------------------- cover
    w.para("", space_after=60)
    w.para([("Hardware Modeling using Verilog", {"s": 15, "c": TEAL, "b": True,
                                                 "f": HEADF})],
           align=AL.CENTER, space_after=4)
    w.para([("Lecture 01 — Introduction", {"s": 30, "c": NAVY, "b": True,
                                           "f": HEADF})],
           align=AL.CENTER, space_after=10)
    w.para([("Tutorial and Practice Workbook", {"s": 15, "c": AMBER,
                                                "b": True, "f": HEADF})],
           align=AL.CENTER, space_after=22)
    w.para([("Prof. Indranil Sengupta · Department of Computer Science and "
             "Engineering · IIT Kharagpur (NPTEL)", {"s": 11, "c": SLATE})],
           align=AL.CENTER, space_after=4)
    w.para([("expanded and made hands-on for the Chip Design Associate "
             "programme · Module 2 · NOS NIE/ELE/N0102", {"s": 11,
                                                          "c": SLATE})],
           align=AL.CENTER, space_after=30)

    w.callout("How this workbook is organised", [
        [("Part 1", {"b": True, "c": NAVY}),
         ("  The lecture itself, written out in full. Every slide the lecturer "
          "shows is covered, in his order, with the explanation expanded so "
          "that nothing has to be looked up elsewhere.", {})],
        [("Part 2", {"b": True, "c": NAVY}),
         ("  The design flow in detail: what each step takes in, what it "
          "produces, and which tool does it.", {})],
        [("Part 3", {"b": True, "c": NAVY}),
         ("  Installing the toolchain, on Linux, macOS or Windows, with the "
          "checks that tell you it worked.", {})],
        [("Part 4", {"b": True, "c": NAVY}),
         ("  Five guided labs. Every command is given, and every output "
          "printed here was produced by actually running it.", {})],
        [("Part 5", {"b": True, "c": NAVY}),
         ("  Thirty-six exercises with full worked solutions, and a reference "
          "section.", {})],
    ], color=NAVY)

    w.callout("Before you start", [
        "You need a computer you can install software on, and about an hour. "
        "No licences, no university server and no vendor account are required: "
        "every tool used in this workbook is open source.",
        [("Everything in Parts 4 and 5 lives in ", {}),
         ("ChipDesignAssociate/VerilogCourse/Lecture01_Lab/", {"f": MONOF,
                                                               "s": 10}),
         (" in the course repository.", {})],
    ], color=AMBER, bar="C77514", fill="FFF7EC")

    w.page_break()

    # ===================================================== PART 1
    w.h1("Part 1 · The Lecture")

    w.para([("This part follows Lecture 01 slide by slide, in the lecturer's "
             "own order. Where he says something briefly, it is expanded; "
             "where he refers to something you may not know, it is explained. "
             "Nothing has been reordered.", {})])

    w.h2("1.1  What this course is for")

    w.para("The lecturer opens with six objectives. They are worth reading "
           "slowly, because between them they describe everything the next "
           "eight weeks will do.")
    w.image("objectives", width=6.6,
            caption="The six objectives, with what each will mean in practice")

    w.h3("Objective 1 — learn the Verilog hardware description language")
    w.para("Verilog is a language in which a designer specifies the behaviour, "
           "the functionality or the structure of a hardware circuit. You will "
           "learn its syntax, its data types, its operators, and the module as "
           "the unit of design.")

    w.h3("Objective 2 — behavioural and structural design styles")
    w.para("These are two different ways of saying what a circuit is, and the "
           "distinction runs through the entire course. A behavioural "
           "description says WHAT the circuit does. A structural description "
           "names WHICH PARTS it is built from and how they are wired "
           "together. Both are legal Verilog; both can describe the same "
           "circuit; and a synthesis tool turns the first into the second.")

    w.h3("Objective 3 — test benches and simulation results")
    w.para("A design you cannot test is a design you cannot trust. A test "
           "bench is a piece of Verilog whose job is to drive your design with "
           "stimulus and check what comes out. It is never turned into "
           "hardware, so it may use delays, loops and printing freely. Week 5 "
           "of the course is devoted to this; you will write your first one in "
           "Lab 1 of this workbook.")

    w.h3("Objective 4 — combinational and sequential circuits")
    w.para("Combinational logic has no memory: its outputs depend only on its "
           "present inputs. Sequential logic has memory: its outputs depend "
           "also on what happened before, which is held in registers and "
           "updated on a clock edge. Almost every real block is a mixture of "
           "the two.")

    w.h3("Objective 5 — good and bad coding practices")
    w.para("Verilog will happily let you write something that simulates "
           "correctly on your machine and synthesises into hardware that does "
           "something different. Week 6 is about avoiding that, and the "
           "reason it needs a whole week is the subject of the next section.")

    w.h3("Objective 6 — case studies")
    w.para("Week 8 builds a pipelined processor — both its data path and its "
           "control path — entirely in Verilog. Everything before it is "
           "preparation for that.")

    # ---------------------------------------------------------- 1.2 HDL
    w.h2("1.2  What a hardware description language is — and is not")

    w.para([("This is the single most common beginner error, so it is worth "
             "stating plainly before anything else: ", {}),
            ("Verilog is not a programming language.", {"b": True,
                                                        "c": RED}),
            ("  It looks like one. It is text, it has semicolons, it has "
             "if-statements. But what the text MEANS is completely different.",
             {})])

    w.image("hdl_not_program", width=6.6,
            caption="Three lines in C, and three lines in Verilog")

    w.para("In C, three assignments happen one after another. The order of the "
           "lines is the order of events; swap two of them and you change what "
           "the program does.")
    w.code([
        "a = 1;",
        "b = 2;",
        "c = 3;",
    ], caption="C — a sequence of events in time")

    w.para("In Verilog, those same three lines describe three pieces of wire, "
           "each permanently driven. All three statements are true at every "
           "instant the circuit is powered. There is no \"first\" and no "
           "\"next\". Swap two of them and nothing changes at all.")
    w.code([
        "assign a = 1;",
        "assign b = 2;",
        "assign c = 3;",
    ], caption="Verilog — a description of three wires that exist")

    w.callout("Hold on to this", [
        "You are not writing instructions for a machine to follow. You are "
        "writing a description of a machine that will be built. Once you "
        "really believe that, most of the confusion in Weeks 2 and 3 of the "
        "course never happens.",
    ], color=RED, bar="C01F43", fill="FDECEF")

    w.page_break()

    # ===================================================== PART 2
    w.h1("Part 2 · The Problem, and the Answer")

    w.h2("2.1  Why VLSI design had to become a process")

    w.para("A hardware description language only exists because of a problem, "
           "and the lecturer spends the first third of the lecture on that "
           "problem. It is a chain of consequences, each one caused by the "
           "one before it.")
    w.image("design_complexity", width=6.6,
            caption="Each box is caused by the one to its left")

    w.para("Fabrication technology improved, so more transistors fitted on one "
           "chip. Designs therefore grew bigger and more complex. Past a "
           "certain size, designing them by hand became impossible, so "
           "computer-aided design tools became essential — and a CAD tool "
           "needs a language to read and write. That last link is where "
           "Verilog enters, and it is the only reason this course has a "
           "subject.")

    w.h3("How big is \"too big\"?")
    w.para("The lecturer puts two chips side by side: the first commercial "
           "planar integrated circuit, and a modern processor.")
    w.image("scale_compare", width=6.6,
            caption="The two chips, and the factor between them")

    w.callout("The arithmetic that settles it", [
        "If you could place and wire one transistor per second, by hand, "
        "without ever sleeping, the 731-million-transistor Nehalem die would "
        "take you about twenty-three years. And then one change to the "
        "specification would send you back to the beginning.",
        [("That is what the lecturer means by ", {}),
         ("\"manual design is simply ruled out\"", {"b": True, "c": NAVY}),
         (". The job of a VLSI designer changed: a designer no longer places "
          "transistors, but writes a DESCRIPTION of what the circuit must do, "
          "and a program turns that description into transistors.", {})],
    ], color=NAVY)

    w.h2("2.2  Moore's Law")

    w.para("The growth that caused all this has a name. In 1965 Gordon Moore "
           "noticed that the number of components on a chip was doubling every "
           "year; in 1975 he revised it to every two years. That is Moore's "
           "Law, and it has held for about five decades.")
    w.image("moore_plot", width=6.6,
            caption="Published transistor counts, 1971–2022, on a log scale. "
                    "A straight line on a log scale means constant exponential "
                    "growth.")

    w.h3("It is not a law of physics")
    w.para("This matters more than it sounds. Moore's Law was an observation "
           "about what the industry had been doing, and it kept coming true "
           "largely because it became a target: equipment makers, materials "
           "suppliers and chip companies all planned their roadmaps around it, "
           "so the investment arrived on schedule to make the next node "
           "happen. A self-fulfilling forecast, not a force of nature.")
    w.image("moore_economics", width=6.6)

    w.h3("What a nanometre is")
    w.para("The lecture quotes \"CMOS up to 22 nm, FinFET 14 nm\", which was "
           "correct when it was recorded. Those node names are now marketing "
           "labels rather than measurements — no feature on a \"3 nm\" chip is "
           "3 nm across. But the physical scale is worth feeling.")
    w.image("feature_size", width=6.6)
    w.para("A 22 nm gate is roughly a hundred silicon atoms across. At that "
           "size a handful of stray atoms changes a transistor's behaviour, "
           "which is why fabrication is statistical rather than exact, why "
           "every chip is tested individually, and why the design flow carries "
           "a verification step at every single level.")

    w.h2("2.3  The requirements that conflict")

    w.para("If one design were simply best, a tool could find it and the job "
           "would be done. The reason design is hard — and the reason it needs "
           "a human — is that the three things you want pull against each "
           "other.")
    w.image("tradeoff_triangle", width=6.6)

    w.table(["If you want…", "You might…", "And this gets worse"],
            [["Less AREA", "share one adder between several operations",
              "speed — it now takes more clock cycles"],
             ["More SPEED", "add pipeline registers, or duplicate logic",
              "area, and switching power"],
             ["Less POWER", "lower the supply voltage, or gate the clock",
              "speed, and control-logic area"]],
            widths=[1.5, 2.6, 2.7], size=10)

    w.callout("Why this matters for synthesis", [
        "A synthesis tool does not find THE answer, because there isn't one. "
        "It finds an answer that satisfies the constraints you gave it. Give "
        "it different constraints and you get different hardware out of the "
        "same Verilog — which you will see for yourself in Lab 4.",
    ], color=AMBER, bar="C77514", fill="FFF7EC")

    w.page_break()
