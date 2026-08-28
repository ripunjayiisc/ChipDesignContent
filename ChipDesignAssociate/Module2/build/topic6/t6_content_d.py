# -*- coding: utf-8 -*-
"""Topic 6 deck — tools, installation, the lab programme and the close."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ================================================== section: tools
    d.section_slide(
        "TOOLS", "Installing and Running the Timing Flow",
        "Everything in this topic runs on free software. The vendor tools "
        "the syllabus names are covered too - as the last step, not the first.",
        ["The landscape: Vivado, Quartus, PrimeTime, Tempus, OpenSTA, and yours",
         "Tier 1 install: one apt line, and every exercise runs",
         "The lab flow: RTL in, slack out - with no black box in between",
         "The same four steps in Vivado, and how SDC maps onto XDC"],
        accent=TEAL)

    # ------------------------------------------------------- landscape
    s = d.slide("TOOLS · LANDSCAPE", "What Exists, and What You Will Use")
    y = d.image(s, TOP - 45720, "tool_landscape", 4846320)
    d.lead(s, y + G, [[R("They all compute arrival, required and slack. The differences are "
                         "the delay models, the report format and the price.", s=10.5)]],
           h=274320)

    # ---------------------------------------------------- install tier 1
    s = d.slide("TOOLS · INSTALL", "Tier 1 - One Line, and Every Exercise Runs", accent=GREEN)
    y = d.image(s, TOP - 45720, "install_required", 3657600)
    y = d.code(s, y + G, [
        "sudo apt update",
        "sudo apt install yosys iverilog gtkwave python3 python3-matplotlib",
        "yosys -V && iverilog -V && python3 -c \"import matplotlib; print('ok')\""],
        title="Debian / Ubuntu / WSL2 — copy this line", size=10)
    d.lead(s, y + G, [[R("On Windows: install WSL2 first (wsl --install), then run the same "
                         "three lines inside it.", s=10.5)]], h=228600)

    # ------------------------------------------------ install tiers 2/3
    s = d.slide("TOOLS · INSTALL", "Tiers 2 and 3 - For the Last Four Exercises Only")
    y = d.image(s, TOP - 45720, "install_optional", 4114800)
    d.card(s, y + G, "Nothing in this course is gated behind a licence you cannot get",
           [[R("57 of the 62 exercises run on tier 1 alone. Tier 2 (OpenSTA) lets you check "
               "your engine against a real one. Tier 3 (Vivado, ModelSim) is there because "
               "the syllabus names them and because you will meet them at work.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=914400)

    # ------------------------------------------------- vivado install
    s = d.slide("TOOLS · VIVADO", "Installing Vivado, Step By Step")
    y = d.table(s, TOP,
                ["Step", "What to do", "Watch out for"],
                [["1", "Create a free AMD/Xilinx account",
                  "the download will not start without it"],
                 ["2", "Download the Unified Installer (web installer, ~200 MB)",
                  "not the full 40 GB archive"],
                 ["3", "Choose \"Vivado ML Edition\" then \"Vivado ML Standard\"",
                  "Standard is the free one - no licence file needed"],
                 ["4", "Deselect every device family except Artix-7",
                  "this cuts 40 GB to about 8 GB"],
                 ["5", "On Linux, install the cable drivers afterwards",
                  "only needed if you program a real board"],
                 ["6", "Verify:  vivado -version", "then everything below runs headless"]],
                [685800, 5943600, 4617720], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "You do not need a board",
           [[R("Every timing exercise in this topic is a synthesis-and-report exercise. "
               "Vivado will happily target a device it has never seen and give you a real "
               "timing report for it.", s=10.5)]],
           accent=TEAL, h=594360)

    # ------------------------------------------------------- lab flow
    s = d.slide("TOOLS · THE FLOW", "RTL In, Slack Out - With No Black Box In Between")
    y = d.image(s, TOP - 45720, "lab_flow", 3474720)
    y = d.code(s, y + G, [
        "make lib      # read the Liberty file and print the cell table",
        "make tiny     # three flops - a report you can check by hand",
        "make sweep    # Fmax against width, for three adder styles",
        "make hold     # a hold violation, then the same design fixed",
        "make mcp      # a false violation, then the multicycle path that removes it",
        "make verify   # prove every optimised netlist still computes the right answer"],
        size=9.5)

    # ------------------------------------------------------ vivado flow
    s = d.slide("TOOLS · VIVADO", "The Same Four Steps, In Vivado")
    y = d.image(s, TOP - 45720, "vivado_flow", 4846320)
    d.lead(s, y + G, [[R("Every line is the industrial equivalent of one line in your "
                         "Makefile. The concepts do not change - only the command names.",
                         s=10.5)]], h=274320)

    # ------------------------------------------------------ vivado tcl
    s = d.slide("TOOLS · VIVADO", "The Script, In Full")
    y = d.code(s, TOP, [
        "# scripts/vivado_timing.tcl   -   run with:  vivado -mode batch -source this.tcl",
        "set part xc7a35tcpg236-1",
        "",
        "read_verilog [glob rtl/*.v]",
        "read_xdc     constraints/vivado.xdc",
        "synth_design -top add32 -part $part -flatten_hierarchy rebuilt",
        "",
        "report_timing_summary -file rpt/post_synth_summary.rpt",
        "report_timing -delay_type max -max_paths 10 -file rpt/post_synth_setup.rpt",
        "report_timing -delay_type min -max_paths 10 -file rpt/post_synth_hold.rpt",
        "",
        "opt_design ; place_design ; route_design",
        "report_timing_summary -file rpt/post_route_summary.rpt",
        "",
        "# the number to compare against your own engine:",
        "puts \"WNS = [get_property SLACK [get_timing_paths -delay_type max]]\""],
        size=9.5)

    d.card(s, y + G, "The comparison that makes the whole topic land",
           [[R("Run your engine and Vivado on the same RTL. The absolute numbers will "
               "differ - different technology, different delay model. The STRUCTURE of the "
               "report, the critical path it names, and the effect of every constraint "
               "change will be the same.", s=10.5)]],
           accent=NAVY, h=822960)

    # --------------------------------------------------------- SDC vs XDC
    s = d.slide("TOOLS · SDC AND XDC", "The Same Language, Two Names")
    y = d.image(s, TOP - 45720, "sdc_vs_xdc", 3200400)
    y = d.code(s, y + G, [
        "# constraints/vivado.xdc  -  the timing half is identical to the SDC file",
        "create_clock -name clk -period 5.000 [get_ports clk]",
        "set_input_delay  -clock clk -max 1.20 [get_ports {a[*] b[*]}]",
        "set_property PACKAGE_PIN W5    [get_ports clk]     # <- the XDC-only half",
        "set_property IOSTANDARD LVCMOS33 [get_ports clk]"],
        size=9.5)

    # ==================================================== section: labs
    d.section_slide(
        "LABS T1–T7", "The Practical Component",
        "25 hours of hands-on work: build the analyser, then use it on real "
        "violations, then prove the ideas transfer to an industrial tool.",
        ["Syllabus: Timing Analysis and Closure Labs (10 h)",
         "Syllabus: Design Synthesis and Optimisation Labs (15 h)",
         "62 graded exercises, every one with a worked solution",
         "Nothing quoted in this topic that you cannot reproduce with make"],
        accent=GREEN)

    # ------------------------------------------------------- the lab map
    s = d.slide("LABS · MAP", "Seven Parts, 25 Hours")
    y = d.image(s, TOP - 45720, "lab_map", 5029200)
    d.lead(s, y + G, [[R("Parts A-C build the tool. Parts D-F use it on real violations. "
                         "Part G proves the ideas transfer.", b=True, c=GREEN, s=10.5)]],
           h=228600)

    # ---------------------------------------------------------- lab T1-T2
    s = d.slide("LABS · T1 AND T2", "Build the Delay Model, Then the Graph")
    y = d.cols(s, TOP, [
        ("T1 · The delay model (2 h)",
         [[R("Write lib/cda_edu.lib: 14 cells, each with an intrinsic delay, a load factor "
             "and an input capacitance.")],
          [R("Write sta/liberty.py to read it and print the cell table.")],
          [R("Deliverable: a table of 14 cells with every number accounted for.")],
          [R("Check:  make lib")]], TEAL, CARD),
        ("T2 · The timing graph (3 h)",
         [[R("Synthesise rtl/tiny.v with Yosys, write the netlist as JSON.")],
          [R("Turn the JSON into nodes and arcs: one node per pin, cell delay on the "
             "internal input-to-output arc.")],
          [R("Deliverable: the graph for a three-flop design, drawn on paper and printed "
             "by your code - and they agree.")],
          [R("Check:  make tiny")]], NAVY, CARD)],
        h=3017520)

    d.card(s, y + G, "The arc convention that makes reports readable",
           [[R("Charge the cell delay on the arc INSIDE the cell, using the load on its "
               "output net; charge clock-to-Q at the Q pin. Net arcs cost zero. Get this "
               "wrong and every report line is attributed to the wrong cell.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ---------------------------------------------------------- lab T3
    s = d.slide("LABS · T3", "Arrival, Required, Slack - the Engine Itself")
    y = d.code(s, TOP, [
        "$ ./scripts/sta.sh tiny --paths 1 -p 1.0",
        "",
        "  Path 1   endpoint q_reg/D  (DFF)",
        "           startpoint p_reg",
        "         incr   arrival   pin",
        "        0.000     0.000   clock edge at p_reg",
        "        0.164     0.164   p_reg/Q                    (DFF)",
        "        0.000     0.164   u97/B                      (XOR2)",
        "        0.117     0.281   u97/Y                      (XOR2)",
        "        0.000     0.281   q_reg/D                    (DFF)",
        "                  0.910   required (period - setup)",
        "                  0.629   SLACK   MET",
        "",
        "  WNS (worst slack)  : +0.629 ns   MET",
        "  longest path       : 0.371 ns          Fmax : 2693.2 MHz"],
        title="what your engine prints when T3 is finished", size=9.5)

    d.card(s, y + G, "The exercise that matters most in the whole topic",
           [[R("Compute +0.629 on paper before you run it. When your arithmetic and your "
               "code agree to three decimals, you understand static timing analysis - and "
               "no report from any vendor will ever be mysterious again.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ---------------------------------------------------------- lab T4
    s = d.slide("LABS · T4", "Constraints - Watch the Report Change")
    y = d.table(s, TOP,
                ["Exercise", "What you change", "What you must observe"],
                [["T4.1", "the period, from 5 ns down to 1 ns",
                  "the slack falls linearly; the path does not change"],
                 ["T4.2", "add set_input_delay for the first time",
                  "new paths appear in the report that were not there before"],
                 ["T4.3", "remove it again",
                  "the unconstrained count goes up; the WNS improves. Explain that."],
                 ["T4.4", "add 0.15 ns of uncertainty",
                  "every setup slack drops by exactly 0.15"],
                 ["T4.5", "add 0.30 ns of skew to one register",
                  "its setup slack improves and its hold slack collapses"],
                 ["T4.6", "set_false_path on the critical path",
                  "the WNS jumps. Write down why that is dangerous."]],
                [1188720, 4297680, 5760720], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "T4.3 and T4.6 are the two that teach the most",
           [[R("Both make the report look BETTER while making the analysis worse. "
               "Learning to distrust an improving number is the professional skill this "
               "topic is really about.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=594360)

    # ---------------------------------------------------------- lab T5
    s = d.slide("LABS · T5", "Setup Closure - the Fmax Sweep")
    y = d.code(s, TOP, [
        "$ make sweep",
        "",
        "  === hand-written carry chain ===    === a + b, delay-driven mapping ===",
        "   W   cells  longest(ns)  ns/bit      W   cells  longest(ns)  ns/bit",
        "   4      30      0.773    0.1933      4      33      0.831    0.2077",
        "   8      62      1.247    0.1559      8      74      1.183    0.1479",
        "  16     126      2.196    0.1373     16     159      1.547    0.0967",
        "  32     254      4.094    0.1279     32     332      1.939    0.0606",
        "  64     510      7.889    0.1233     64     681      2.318    0.0362",
        "",
        "  ripple:    ns/bit converges on 0.123  ->  delay is LINEAR in width",
        "  a+b fast:  ns/bit keeps FALLING       ->  the tool built a carry tree"],
        title="the experiment that shows what synthesis actually did", size=9.5)

    y = d.cols(s, y + G, [
        ("What you must explain",
         [[R("Why ns/bit is constant for the ripple chain and falling for the tool's "
             "adder.")],
          [R("Why the plain a+b is SLOWER than the ripple chain under area mapping.")]],
         AMBER, CARD_A),
        ("Then prove it still works",
         [[R("make verify runs all three netlists against a reference over 500 random "
             "vectors.")],
          [R("An optimisation you have not verified is not an optimisation.",
             b=True, c=NAVY)]], GREEN, CARD_G)],
        h=1554480)

    # ---------------------------------------------------------- lab T6
    s = d.slide("LABS · T6", "Hold Violations and Exceptions")
    y = d.code(s, TOP, [
        "$ make hold",
        "  WNS (worst slack)  : -0.165 ns   VIOLATED     (hold_demo, 0.30 ns skew)",
        "  WNS (worst slack)  : +0.071 ns   MET          (hold_fixed, same skew)",
        "",
        "$ make mcp",
        "  WNS (worst slack)  : -1.193 ns   VIOLATED     (slow_path, no multicycle)",
        "  WNS (worst slack)  : +0.392 ns   MET          (slow_path, multicycle 4)"],
        title="two violations, two different kinds of fix", size=10)

    y = d.table(s, y + G,
                ["Exercise", "Task"],
                [["T6.1", "Reproduce both violations, then explain in one sentence each why "
                          "the fix works"],
                 ["T6.2", "Increase the skew until hold_fixed also fails - how much delay "
                          "would it need?"],
                 ["T6.3", "Add the multicycle -setup line but NOT the -hold line. "
                          "Predict, then measure."],
                 ["T6.4", "Remove the enable from slow_path.v. The SDC is now a lie - "
                          "show what breaks."],
                 ["T6.5", "Write a false path that hides a real violation, then argue "
                          "against yourself."]],
                [1188720, 10058400], rh=283464, bold_cols=(0,))

    # ---------------------------------------------------------- lab T7
    s = d.slide("LABS · T7", "The Same Design In an Industrial Tool")
    y = d.table(s, TOP,
                ["Exercise", "Tool", "What you produce"],
                [["T7.1", "Vivado", "the same add32, synthesised for an Artix-7, with your "
                          "own XDC"],
                 ["T7.2", "Vivado", "post-synthesis and post-route timing summaries, "
                          "compared"],
                 ["T7.3", "Vivado", "the multicycle path applied in XDC - same effect, "
                          "vendor syntax"],
                 ["T7.4", "OpenSTA", "your netlist and a real .lib, read by a real STA tool"],
                 ["T7.5", "both", "a one-page comparison: what matched, what did not, "
                          "and why"]],
                [1188720, 1737360, 8321040], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "T7.5 is the deliverable that proves you learned the topic",
           [[R("The numbers will differ. The reasoning will not. If you can explain why "
               "Vivado's WNS differs from yours, and point at the delay model rather than "
               "shrugging, you can close timing on a real design.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------- assessment
    s = d.slide("LABS · ASSESSMENT", "How the 62 Exercises Are Weighted")
    y = d.table(s, TOP,
                ["Part", "Exercises", "Weight", "Assessed on"],
                [["A · delay model", "6", "8%", "every number traceable to the library"],
                 ["B · timing graph", "8", "12%", "hand-drawn graph matches the code"],
                 ["C · the engine", "10", "20%", "hand arithmetic matches the report"],
                 ["D · constraints", "12", "15%", "a defensible line-by-line SDC file"],
                 ["E · setup closure", "12", "20%", "measured Fmax, plus verification"],
                 ["F · hold and exceptions", "9", "15%", "correct diagnosis before the fix"],
                 ["G · industrial tools", "5", "10%", "the comparison write-up"]],
                [3017520, 2011680, 1737360, 4480560], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "The rule that runs through every part",
           [[R("A fix you cannot explain is not a fix. Marks are given for the reasoning, "
               "not for the green report - because in this field it is trivially easy to "
               "produce a green report on a broken design.", s=10.5)]],
           accent=NAVY, h=868680)

    # ------------------------------------------------------- glossary 1
    s = d.slide("REFERENCE", "Glossary - Terms Used In This Topic (1 of 2)")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["arrival time", "when the data actually reaches a pin, measured from the "
                              "clock edge"],
             ["required time", "when it had to be there by, for the check to pass"],
             ["slack", "required minus arrival. Positive fits, negative does not"],
             ["WNS", "worst negative slack - the single worst path in the design"],
             ["TNS", "total negative slack - every negative slack added up"],
             ["setup time", "how long D must be stable BEFORE the clock edge"],
             ["hold time", "how long D must stay stable AFTER the clock edge"],
             ["clock-to-Q", "how long after the edge before Q is valid"],
             ["clock skew", "the difference in clock arrival between two registers"],
             ["clock jitter", "cycle-to-cycle variation in the clock edge position"],
             ["uncertainty", "the margin that stands in for jitter and unmodelled skew"],
             ["critical path", "the path with the worst slack - the one that sets Fmax"]],
            [2743200, 8503920], rh=265176, bold_cols=(0,))

    # ------------------------------------------------------- glossary 2
    s = d.slide("REFERENCE", "Glossary - Terms Used In This Topic (2 of 2)")
    d.table(s, TOP,
            ["Term", "Meaning"],
            [["Fmax", "1 divided by the longest path delay - the highest safe clock"],
             ["endpoint", "where a path ends: a flop's D pin, or an output port"],
             ["startpoint", "where it begins: a flop's Q pin, or an input port"],
             ["path group", "reg-to-reg, in-to-reg, reg-to-out, in-to-out"],
             ["false path", "a path the tool must not check, because it cannot be "
                            "exercised"],
             ["multicycle path", "a path allowed more than one cycle to complete"],
             ["SDC / XDC", "the constraint language; XDC adds Xilinx physical constraints"],
             ["Liberty (.lib)", "the file that gives each cell its delay, setup and hold"],
             ["PVT corner", "a process/voltage/temperature combination to analyse at"],
             ["retiming", "moving an existing register across logic to balance stages"],
             ["pipelining", "adding a register to cut a long path in two"],
             ["timing closure", "the loop that ends when every check passes at every "
                                "corner"]],
            [2743200, 8503920], rh=265176, bold_cols=(0,))

    # ---------------------------------------------------------- summary
    s = d.slide("SUMMARY", "Topic 6 In Ten Lines", accent=GREEN)
    d.bullets(s, TOP, [
        "A flip-flop samples over a WINDOW around the clock edge, not at an instant.",
        "Setup means the data was too late. Hold means it changed too soon.",
        "slack = required - arrival, computed at every endpoint. That is all STA does.",
        "The clock period is in the setup equation and nowhere in the hold equation.",
        "An unconstrained path is not a passing path - it is an unexamined one.",
        "An exception is a promise. The tool believes you without checking.",
        "Half of all reported violations are constraint bugs, not design bugs.",
        "Setup is fixed by less logic or a slower clock; hold only by MORE delay.",
        "The same RTL ran at 217 MHz and 516 MHz. Only a synthesis option changed.",
        "Describe intent, not structure - then check what your tool did with it."],
        accent=GREEN, size=12.5, step=384048)

    # ------------------------------------------------------------ close
    s = d.slide("CLOSE", "What To Do Next", accent=TEAL)
    y = d.cols(s, TOP, [
        ("Before the next session",
         [[R("Install tier 1 and run  make  in the lab directory. It should end with "
             "\"Topic 6 lab complete\".")],
          [R("Compute the +0.629 ns slack on paper. Bring your working.")],
          [R("Read one timing report - any tool, any design - and find its critical "
             "path.")]], TEAL, CARD),
        ("Carry into every project after this",
         [[R("Write the constraint file before you write the RTL. It is the "
             "specification.")],
          [R("Check the unconstrained-endpoint count on every single run.")],
          [R("Never write an exception you cannot justify in one sentence.")],
          [R("Verify every optimisation. A faster design that computes the wrong answer "
             "is not faster.", b=True, c=NAVY)]], GREEN, CARD_G)],
        h=2926080)

    d.card(s, y + G, "The sentence to leave with",
           [[R("A timing report is not a verdict on your design. It is a verdict on your "
               "design AND your constraints - and only one of those two is usually the "
               "problem.", b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=868680)
