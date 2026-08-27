# -*- coding: utf-8 -*-
"""Topic 6 deck — opening and 6a: timing constraints in RTL design."""
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
        "TOPIC 6",
        "Timing Constraints and Analysis",
        "Introduction to timing constraints in RTL design  ·  Timing analysis and "
        "optimization techniques  ·  Setup and hold time violations and resolution",
        ["6a · Constraints — what the tool cannot know until you tell it",
         "6b · Analysis — how static timing analysis actually computes slack",
         "6c · Violations — setup and hold, why they are opposite, and how to fix each",
         "Tools · Vivado · OpenSTA · a 400-line STA engine you build  ·  Labs T1–T7"])

    # ============================================================== roadmap
    s = d.slide("TOPIC 6 · ROADMAP", "What This Topic Covers, and Why Every Chip Depends On It")
    y = d.lead(s, TOP, [[
        R("Topic 4 taught you to write RTL. Topic 5 taught you to prove it is ", s=12.5),
        R("functionally ", b=True, c=NAVY, s=12.5),
        R("correct. Topic 6 asks the last question before silicon: ", s=12.5),
        R("is it fast enough, and will it work at all? ", b=True, c=AMBER, s=12.5),
        R("A design that simulates perfectly can still fail on the bench - "
          "because simulation does not know how long a wire takes.", s=12.5)]], h=685800)

    y = d.table(s, y + G,
                ["Syllabus bullet — Topic 6", "Covered by", "Slides"],
                [["Introduction to timing constraints in RTL design", "6a", "5–26"],
                 ["Timing analysis and optimization techniques", "6b", "27–48"],
                 ["Setup and hold time violations and resolution", "6c", "49–68"],
                 ["Practical: Timing Analysis and Closure Labs (10 h)", "Labs T1–T7",
                  "69–78"],
                 ["Practical: Design Synthesis and Optimisation Labs (15 h)",
                  "Labs T5–T7", "74–78"]],
                [6217920, 3383280, 1645920], rh=329184, bold_cols=(1,))

    y = d.card(s, y + G, "Learning outcomes — by the end of this topic you can",
               [[R("· Write a complete SDC/XDC constraint file and defend every line in it.")],
                [R("· Compute arrival, required and slack by hand, then verify a tool's "
                   "answer against your own.")],
                [R("· Read any timing report - Vivado, OpenSTA, PrimeTime - and find the "
                   "problem in under a minute.")],
                [R("· Diagnose a setup violation and pick the cheapest fix that works.")],
                [R("· Recognise a hold violation, explain why slowing the clock cannot help, "
                   "and fix it properly.")]],
               accent=GREEN, fill=CARD_G, h=1509840)
    d.card(s, 5623560, "One sentence to open the session with",
           [[R("A functional bug makes the chip do the wrong thing. A timing bug makes it do "
               "the right thing at the wrong moment - and no amount of simulation will "
               "show you that.", b=True, c=RED)]],
           accent=RED, fill=CARD_R, h=731520)

    # =========================================================== motivation
    s = d.slide("WHY THIS MATTERS", "The Bug That Simulation Cannot Find", accent=RED)
    y = d.lead(s, TOP, [[
        R("Your testbench applies a value, waits for a clock edge, and checks the answer. "
          "It assumes the logic finished in time. ", s=12.5),
        R("Real gates take real time. ", b=True, c=RED, s=12.5),
        R("If the answer is 0.2 ns late, the flop captures the OLD value - and your "
          "simulation, which had no delays in it, never noticed.", s=12.5)]], h=594360)

    y = d.cols(s, y + G, [
        ("What RTL simulation checks",
         [[R("Does the design compute the right value, given unlimited time?")],
          [R("Every functional bug you found in Topic 5 lives here.")],
          [R("Zero-delay: every assignment lands instantly.")]], TEAL, CARD),
        ("What static timing analysis checks",
         [[R("Does that value ARRIVE before the next clock edge?")],
          [R("And does it stay put long enough to be captured?")],
          [R("Real gate delays, real wire delays, real clock skew.")]], GREEN, CARD_G),
        ("What neither one checks",
         [[R("Whether your CONSTRAINTS describe the real system.")],
          [R("A wrong period or a missing input delay makes both tools lie in the "
             "same direction: everything looks fine.")]], RED, CARD_R)],
        h=1737360)

    d.card(s, y + G, "The order of operations, and it is not negotiable",
           [[R("1.  Simulate until the function is right.  "),
             R("2.  Constrain until the report is honest.  "),
             R("3.  Analyse until the slack is positive.  "),
             R("4.  Only then build.", b=True, c=NAVY)],
            [R("Skip step 2 and step 3 becomes theatre: the tool reports MET on paths it "
               "never examined.", c=RED)]],
           accent=NAVY, h=822960)

    # ===================================================== section 6a
    d.section_slide(
        "PART 6a", "Timing Constraints in RTL Design",
        "Synthesis has no idea how fast you want to go until you tell it. "
        "This part is about telling it - completely, and truthfully.",
        ["The clock: create_clock, period, waveform, uncertainty",
         "The boundary: set_input_delay and set_output_delay",
         "The exceptions: set_false_path and set_multicycle_path",
         "The order to write a constraint file, and the holes to check for"])

    # --------------------------------------------------- the whole picture
    s = d.slide("6a · THE ONE PICTURE", "A Flip-Flop Samples Over a Window, Not At an Instant")
    y = d.image(s, TOP - 45720, "setup_hold_window", 4160520)
    d.card(s, y + G, "Every timing concept in this topic comes from this one diagram",
           [[R("SETUP time: the data must be stable for this long BEFORE the edge. "
               "HOLD time: it must stay stable for this long AFTER it. "
               "Break the first and the flop captures a stale value; break the second "
               "and it captures the NEXT value, a whole cycle early.", s=10.5)]],
           accent=NAVY, h=914400)

    # ------------------------------------------------------ the four parts
    s = d.slide("6a · THE TIMING PATH", "Every Path Has Exactly Four Parts")
    y = d.image(s, TOP - 45720, "timing_path", 4297680)
    d.card(s, y + G, "Learn these four names and the rest of the topic is arithmetic",
           [[R("clock-to-Q "), R("(how long the launching flop takes to produce Q)  ·  ", s=10),
             R("logic delay "), R("(the combinational path)  ·  ", s=10),
             R("setup time "), R("(how early the capturing flop needs it)  ·  ", s=10),
             R("clock skew "), R("(the two flops do not see the edge at the same instant)",
                                 s=10)]],
           accent=TEAL, h=868680)

    # ------------------------------------------------------------- slack
    s = d.slide("6a · SLACK", "Slack Is a Subtraction, and That Is All It Is")
    y = d.image(s, TOP - 45720, "slack_equation", 3565800)
    y = d.code(s, y + G, [
        "slack  =  required time  -  arrival time",
        "",
        "arrival   =  clock-to-Q  +  logic delay          (when the data turns up)",
        "required  =  period + skew - setup - uncertainty (when it had to be there)"],
        title="the only equation you must memorise", size=10.5)
    d.lead(s, y + G, [[R("Positive slack: it fits, with room to spare. "
                         "Negative slack: it does not fit, and the number is by how much.",
                         b=True, c=NAVY, s=11)]], h=274320)

    # ------------------------------------------------------ why constrain
    s = d.slide("6a · WHY CONSTRAIN", "A Tool With No Constraints Is Not Careful - It Is Blind",
                accent=RED)
    y = d.image(s, TOP - 45720, "why_constrain", 4114800)
    d.card(s, y + G, "The single most dangerous report in engineering",
           [[R("A timing report with no violations on an unconstrained design. "
               "It is not telling you the design is fast. It is telling you it did not "
               "look.", b=True, c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=594360)

    # ------------------------------------------------------------ SDC map
    s = d.slide("6a · THE FOUR QUESTIONS", "Every Constraint File Answers the Same Four Things")
    y = d.image(s, TOP - 45720, "sdc_map", 4389120)
    d.lead(s, y + G, [[R("SDC (Synopsys Design Constraints) is the vendor-neutral format. "
                         "Xilinx XDC is SDC plus physical constraints. Intel Quartus reads "
                         "SDC directly. Learn it once.", s=11)]], h=457200)

    # ------------------------------------------------------- create_clock
    s = d.slide("6a · create_clock", "The One Constraint You Cannot Leave Out")
    y = d.image(s, TOP - 45720, "create_clock_anatomy", 2926080)
    y = d.code(s, y + G, [
        "# a 100 MHz primary clock arriving on the port called clk",
        "create_clock -name sys_clk -period 10.000 -waveform {0.000 5.000} [get_ports clk]",
        "",
        "# a clock made by a divide-by-2 inside the design - derive it, never re-declare it",
        "create_generated_clock -name clk_div2 -source [get_ports clk] \\",
        "                       -divide_by 2 [get_pins div_reg/Q]"],
        title="clocks, primary and generated", size=10)
    d.lead(s, y + G, [[R("If a register is clocked by something you never declared, "
                         "its paths are unconstrained and silently unchecked.",
                         b=True, c=RED, s=10.5)]], h=274320)

    # ------------------------------------------------------- uncertainty
    s = d.slide("6a · UNCERTAINTY", "Margin For What You Have Not Modelled Yet")
    y = d.image(s, TOP - 45720, "uncertainty", 3200400)
    y = d.code(s, y + G, [
        "set_clock_uncertainty 0.150 -setup [get_clocks sys_clk]   # jitter + unbuilt skew",
        "set_clock_uncertainty 0.050 -hold  [get_clocks sys_clk]   # jitter only"],
        title="before layout, uncertainty stands in for the clock tree", size=10)
    d.card(s, y + G, "A number you will be tempted to reduce, and should not",
           [[R("Uncertainty is the difference between \"the report says MET\" and \"the "
               "silicon works\". Shrinking it makes the report prettier and the chip no "
               "faster. Typical FPGA practice: 0.1-0.2 ns pre-layout, then let the tool "
               "use the real clock tree afterwards.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ---------------------------------------------------------- I/O delay
    s = d.slide("6a · I/O CONSTRAINTS", "Your First Flop Is Not the Start of the Path")
    y = d.image(s, TOP - 45720, "io_delay", 4297680)
    d.card(s, y + G, "The most common constraint bug in the world",
           [[R("Forget these two lines and every path touching a pin becomes "
               "UNCONSTRAINED. The report shows no violation because it never looked at "
               "them. Always check the unconstrained-endpoint count before you believe a "
               "clean report.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=822960)

    # ---------------------------------------------------------- io syntax
    s = d.slide("6a · I/O CONSTRAINTS", "Writing Them - and Where the Numbers Come From")
    y = d.code(s, TOP, [
        "# INPUT: how late the data arrives, measured from the SAME clock edge",
        "set_input_delay  -clock sys_clk -max 3.0 [get_ports {din[*] valid}]",
        "set_input_delay  -clock sys_clk -min 0.5 [get_ports {din[*] valid}]",
        "",
        "# OUTPUT: how much of the period the NEXT chip needs, before its own edge",
        "set_output_delay -clock sys_clk -max 2.5 [get_ports {dout[*] ready}]",
        "set_output_delay -clock sys_clk -min 0.2 [get_ports {dout[*] ready}]",
        "",
        "# a quick sanity sweep: constrain everything that is still bare",
        "set_input_delay  -clock sys_clk 3.0 [remove_from_collection \\",
        "                    [all_inputs] [get_ports clk]]"],
        title="constraints/io.sdc", size=10)

    y = d.table(s, y + G,
                ["-max is used for", "-min is used for", "Where the number comes from"],
                [["the SETUP check", "the HOLD check",
                  "the upstream chip's datasheet: clock-to-out"],
                 ["the slow corner", "the fast corner", "plus the board trace delay"],
                 ["the LATEST the data can arrive", "the EARLIEST it can change",
                  "when unknown, budget 30% of the period and revisit"]],
                [3474720, 3474720, 4297680], rh=274320, bold_cols=(0, 1))

    d.card(s, y + G, "A rule of thumb that has saved many projects",
           [[R("Register every input and every output. It costs one cycle of latency and "
               "removes the entire I/O timing problem: the path from pin to flop becomes "
               "short and the path from flop to pin becomes short. Do it unless you have a "
               "measured reason not to.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------------- budget
    s = d.slide("6a · THE BUDGET", "Where the 10 Nanoseconds Actually Goes")
    y = d.image(s, TOP - 45720, "io_budget", 4023360)
    d.card(s, y + G, "Read the middle bar before you touch the RTL",
           [[R("You asked for 100 MHz and your own logic got 4.5 ns of it. If the design "
               "will not close, the I/O budget is the first place to look - and registering "
               "the pins hands the whole period back.", s=10.5)]],
           accent=NAVY, h=822960)

    # --------------------------------------------------------- exceptions
    s = d.slide("6a · EXCEPTIONS", "Telling the Tool a Path Is Not What It Looks Like",
                accent=AMBER)
    y = d.image(s, TOP - 45720, "timing_exceptions", 4389120)
    d.lead(s, y + G, [[R("An exception is a promise, and the tool believes you without "
                         "checking. Every one needs a comment saying why it is true.",
                         b=True, c=RED, s=11)]], h=411480)

    # -------------------------------------------------------- false paths
    s = d.slide("6a · FALSE PATHS", "When \"Do Not Check This\" Is the Honest Answer")
    y = d.code(s, TOP, [
        "# a reset that is asserted asynchronously and released synchronously:",
        "# the assertion edge is never timed, the release IS - so cut only one direction",
        "set_false_path -from [get_ports rst_n]",
        "",
        "# a mode pin written once at power-up and never again",
        "set_false_path -from [get_cells cfg_mode_reg]",
        "",
        "# two clocks that are genuinely unrelated (no data crosses without a synchroniser)",
        "set_clock_groups -asynchronous -group [get_clocks sys_clk] \\",
        "                               -group [get_clocks usb_clk]"],
        title="the three legitimate uses", size=10)

    y = d.cols(s, y + G, [
        ("Legitimate",
         [[R("The path physically cannot be exercised.")],
          [R("A synchroniser already handles the crossing.")],
          [R("The endpoint is not sampled by that clock at all.")]], GREEN, CARD_G),
        ("Not legitimate",
         [[R("\"It always fails and I do not know why.\"")],
          [R("\"The tool is being pessimistic.\"")],
          [R("\"We ran out of time before tape-out.\"")]], RED, CARD_R)],
        h=1188720)

    d.card(s, y + G, "How this kills a chip",
           [[R("set_false_path on a path that IS real removes the only check that would "
               "have caught the bug. The report goes green, the design ships, and the "
               "failure appears in the field at one temperature and one voltage. "
               "Write the justification in the file, next to the line.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=822960)

    # ---------------------------------------------------- multicycle path
    s = d.slide("6a · MULTICYCLE PATHS", "When One Cycle Was Never the Requirement")
    y = d.image(s, TOP - 45720, "multicycle_waves", 3200400)
    y = d.code(s, y + G, [
        "set_multicycle_path 4 -setup -from [get_cells a_q*] -to [get_cells acc*]",
        "set_multicycle_path 3 -hold  -from [get_cells a_q*] -to [get_cells acc*]"],
        title="setup N, hold N-1 - and the hold line is not optional", size=10)
    d.card(s, y + G, "Why the hold number is N-1",
           [[R("The setup line moves the CAPTURE edge four cycles later. Left alone, the "
               "hold check would then compare against that same distant edge and demand an "
               "absurd amount of delay. The -hold N-1 line moves the hold check back to "
               "where it belongs: one edge after the launch.", s=10.5)]],
           accent=VIOLET, h=822960)

    # -------------------------------------------------------- mcp caveat
    s = d.slide("6a · MULTICYCLE PATHS", "The Part Everyone Forgets: the Hardware Must Agree")
    y = d.code(s, TOP, [
        "// the SDC exception is a claim about this design. Make the claim true:",
        "reg [1:0] phase;",
        "always @(posedge clk) phase <= phase + 1'b1;",
        "wire tick = (phase == 2'b11);          // one cycle in four",
        "",
        "always @(posedge clk) begin",
        "    if (tick) acc <= a_q + b_q;        // the ENABLE is what makes it legal",
        "end",
        "",
        "// a_q and b_q must also be held steady across all four cycles -",
        "// if they change every cycle, the multicycle claim is simply false."],
        title="rtl/slow_path.v — the enable that justifies the exception", size=10)

    y = d.table(s, y + G,
                ["Without the exception", "With it", "Measured in the lab"],
                [["worst slack -1.193 ns", "worst slack +0.392 ns", "one SDC line"],
                 ["the tool times a 32-bit ripple add in one cycle",
                  "it times it across four", "no RTL changed at all"],
                 ["you pipeline something that never needed it",
                  "you ship what you already had", "hours of work avoided"]],
                [3931920, 3931920, 3383280], rh=274320, bold_cols=(0, 1))

    d.card(s, y + G, "The discipline",
           [[R("Never write a multicycle path you cannot point at the enable for. "
               "If the capture register has no enable, the exception is a lie and the "
               "silicon will find it.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=594360)

    # -------------------------------------------------------- write order
    s = d.slide("6a · WRITING THE FILE", "The Order To Write It - and the Order To Debug It")
    y = d.image(s, TOP - 45720, "sdc_checklist", 4297680)
    d.card(s, y + G, "The check that catches everything else",
           [[R("Report unconstrained endpoints on every run. A design with 400 of them and "
               "WNS +2.0 ns is in far worse shape than one with zero and WNS -0.1 ns - "
               "the first one has not been analysed at all.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ------------------------------------------------------- full example
    s = d.slide("6a · A COMPLETE FILE", "Everything Above, In One Real Constraint File")
    d.code(s, TOP, [
        "# ============================================================ constraints/add32.sdc",
        "# clock ---------------------------------------------------------------------------",
        "create_clock -name clk -period 5.000 [get_ports clk]",
        "set_clock_uncertainty 0.100 -setup [get_clocks clk]",
        "set_clock_uncertainty 0.030 -hold  [get_clocks clk]",
        "",
        "# boundary ------------------------------------------------------------------------",
        "set_input_delay  -clock clk -max 1.20 [get_ports {a[*] b[*]}]",
        "set_input_delay  -clock clk -min 0.30 [get_ports {a[*] b[*]}]",
        "set_output_delay -clock clk -max 1.00 [get_ports {sum[*] cout}]",
        "set_output_delay -clock clk -min 0.20 [get_ports {sum[*] cout}]",
        "",
        "# exceptions ----------------------------------------------------------------------",
        "# cfg_mode is written by software at boot and read only when the core is halted.",
        "set_false_path -from [get_cells cfg_mode_reg]",
        "",
        "# environment ---------------------------------------------------------------------",
        "set_max_fanout 16 [current_design]"],
        size=9.5)

    # ------------------------------------------------------- 6a checkpoint
    s = d.slide("6a · CHECKPOINT", "Ten Questions Before We Move On", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "What does create_clock actually do?",
                  "gives the tool a target; without it there is none"],
                 ["2", "What is the unit of slack?", "time - nanoseconds, signed"],
                 ["3", "Positive slack means?", "the path fits, with that much to spare"],
                 ["4", "What does set_input_delay describe?",
                  "the part of the path outside your chip"],
                 ["5", "What happens if you omit it?",
                  "those paths become unconstrained - unchecked"],
                 ["6", "Why is uncertainty there?",
                  "jitter, and skew that does not exist yet"],
                 ["7", "When is a false path legitimate?",
                  "when the path cannot be exercised, and you can say why"],
                 ["8", "Multicycle 4 setup needs what hold?", "3 - almost always N-1"],
                 ["9", "What must the RTL have for it?",
                  "an enable that really does hold the capture"],
                 ["10", "What do you check last, every time?",
                  "the unconstrained-endpoint count"]],
                [548640, 4846320, 5852160], rh=274320, bold_cols=(0,))
    d.lead(s, y + G, [[R("If any of these is still fuzzy, the analysis in part 6b will not "
                         "land. Ask now.", b=True, c=GREEN, s=11)]], h=274320)
