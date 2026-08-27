# -*- coding: utf-8 -*-
"""Topic 6 deck — 6c: setup and hold violations and their resolution."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ===================================================== section 6c
    d.section_slide(
        "PART 6c", "Setup and Hold Violations, and Their Resolution",
        "Two failures that look similar in a report and could not be more "
        "different in the silicon.",
        ["Setup: the data was too late. The chip runs slower.",
         "Hold: the data changed too soon. The chip does not work at any speed.",
         "Clock skew, jitter, and why hold problems appear only after layout",
         "A decision procedure you can follow under deadline pressure"],
        accent=RED)

    # ----------------------------------------------------- setup vs hold
    s = d.slide("6c · THE TWO FAILURES", "Setup and Hold Are Opposite Problems")
    y = d.image(s, TOP - 45720, "setup_vs_hold", 4572000)
    d.lead(s, y + G, [[R("A chip with a setup violation runs slower. A chip with a hold "
                         "violation does not work at any speed. That difference decides "
                         "everything you do next.", b=True, c=RED, s=11)]], h=365760)

    # ---------------------------------------------------------- the maths
    s = d.slide("6c · THE TWO EQUATIONS", "Side By Side, With the Difference Circled")
    y = d.code(s, TOP, [
        "SETUP     required  =  period  +  skew  -  setup  -  uncertainty",
        "          arrival   =  clk_to_q  +  logic",
        "          slack     =  required  -  arrival",
        "",
        "HOLD      required  =  skew  +  hold  +  uncertainty",
        "          arrival   =  clk_to_q  +  logic          <- the SHORTEST path, not "
        "the longest",
        "          slack     =  arrival  -  required",
        "",
        "#  the period appears in the setup equation and NOWHERE in the hold equation",
        "#  the subtraction is the other way round: setup wants arrival SMALL,",
        "#  hold wants it LARGE"],
        title="everything in part 6c follows from these two", size=9.5)

    d.cols(s, y + G, [
        ("Consequence 1",
         [[R("Slowing the clock fixes setup and does nothing at all for hold.")],
          [R("Speeding it up breaks setup and, again, does nothing to hold.")]],
         AMBER, CARD_A),
        ("Consequence 2",
         [[R("Adding logic fixes hold and breaks setup.")],
          [R("Removing logic fixes setup and can break hold. Every fix trades one against "
             "the other.", b=True, c=NAVY)]], TEAL, CARD)],
        h=1554480)

    # ----------------------------------------------------------- skew
    s = d.slide("6c · CLOCK SKEW", "The Clock Does Not Arrive Everywhere At Once")
    y = d.image(s, TOP - 45720, "clock_skew", 4663440)
    d.lead(s, y + G, [[R("Skew that makes the capture edge LATE helps setup and hurts hold. "
                         "Designers sometimes add it deliberately - it is called useful "
                         "skew.", s=10.5)]], h=274320)

    # --------------------------------------------------- skew in practice
    s = d.slide("6c · SKEW AND JITTER", "Where the Numbers Come From, and When You Know Them")
    y = d.table(s, TOP,
                ["Effect", "What causes it", "Known when?", "Modelled by"],
                [["Clock skew", "different clock-tree branch lengths",
                  "after clock-tree synthesis", "the real tree, or uncertainty before it"],
                 ["Clock jitter", "PLL and oscillator imperfection", "from the datasheet",
                  "set_clock_uncertainty, both checks"],
                 ["Duty-cycle distortion", "unbalanced buffers in the tree", "after layout",
                  "matters for both clock edges"],
                 ["On-chip variation", "process gradients across the die", "statistically",
                  "derating factors, or extra uncertainty"],
                 ["Crosstalk", "a neighbouring net switching", "after routing",
                  "signal-integrity analysis, post-route"]],
                [2377440, 3474720, 2377440, 3017520], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "Why hold violations always seem to arrive late in a project",
           [[R("Before layout there is no clock tree, so there is no real skew - and the "
               "hold check has almost nothing to fail against. The moment the tree is "
               "built, the skew becomes real and hold violations appear all at once. "
               "This is normal, and it is why hold is a place-and-route problem far more "
               "often than an RTL one.", s=10.5)]],
           accent=AMBER, fill=CARD_A, h=959040)

    # ------------------------------------------------------- uncertainty
    s = d.slide("6c · UNCERTAINTY", "The Margin That Stands In For What You Cannot See Yet")
    y = d.image(s, TOP - 45720, "uncertainty", 3474720)
    y = d.table(s, y + G,
                ["Stage", "Typical setup uncertainty", "Why"],
                [["post-synthesis (FPGA)", "0.10 - 0.20 ns",
                  "no clock tree exists; jitter unknown"],
                 ["post-place-and-route", "jitter only, 0.02 - 0.05 ns",
                  "the tool now uses the real skew"],
                 ["ASIC, pre-CTS", "0.15 - 0.30 ns", "plus a margin for OCV"],
                 ["ASIC, sign-off", "jitter + OCV derating", "the tree is measured"]],
                [3200400, 3931920, 4114800], rh=274320, bold_cols=(0,))
    d.lead(s, y + G, [[R("Take the uncertainty out and the report improves while the chip "
                         "does not.", b=True, c=RED, s=10.5)]], h=274320)

    # ------------------------------------------------------- setup detail
    s = d.slide("6c · SETUP VIOLATIONS", "What They Look Like, and What Causes Them")
    y = d.table(s, TOP,
                ["Symptom in the report", "Most likely cause", "First thing to try"],
                [["one path fails, the rest are fine", "a genuinely long path",
                  "look at its incr column"],
                 ["one cell has a huge incr", "high fanout, or a weak driver",
                  "set_max_fanout, or let the tool buffer it"],
                 ["fifty small cells in the path", "the logic is too deep",
                  "restructure, then pipeline"],
                 ["every path fails by a similar amount", "the period is too aggressive",
                  "sanity-check the target against the technology"],
                 ["fails only after place-and-route", "routing delay, not logic",
                  "floorplanning; keep the path local"],
                 ["fails only at the slow corner", "correct behaviour",
                  "that is the corner you sign off at"]],
                [3657600, 3383280, 4206240], rh=283464, bold_cols=(0,))

    d.card(s, y + G, "The number that tells you how much work it is",
           [[R("A slack of -0.05 ns on a 5 ns period is a 1% problem - the tool will often "
               "find it with a higher effort setting. A slack of -2.5 ns on the same period "
               "is a 50% problem: no option will close that, and you are looking at "
               "pipelining or a different architecture.", s=10.5)]],
           accent=NAVY, h=822960)

    # -------------------------------------------------------- hold detail
    s = d.slide("6c · HOLD VIOLATIONS", "A Race, Not a Delay Problem", accent=RED)
    y = d.image(s, TOP - 45720, "hold_race", 4663440)
    d.lead(s, y + G, [[R("Notice what is not in the hold equation: the clock period. "
                         "You can run this chip at 1 Hz and it is still broken.",
                         b=True, c=RED, s=11)]], h=274320)

    # ----------------------------------------------------- fixing hold
    s = d.slide("6c · FIXING HOLD", "Add Delay, On Purpose")
    y = d.image(s, TOP - 45720, "fix_hold", 4389120)
    d.card(s, y + G, "Measured in the lab",
           [[R("hold_demo with 0.30 ns of skew: -0.165 ns, VIOLATED. The same design with "
               "two delay cells in the data path: +0.071 ns, MET. Nothing else changed - "
               "not the clock, not the function.", s=10.5)]],
           accent=GREEN, fill=CARD_G, h=868680)

    # ------------------------------------------------ hold in RTL vs P&R
    s = d.slide("6c · FIXING HOLD", "Who Actually Fixes It - and What Your RTL Must Not Do")
    y = d.cols(s, TOP, [
        ("Place-and-route does the fixing",
         [[R("After layout, when the real skew is known, the tool inserts hold buffers "
             "automatically.")],
          [R("It has the one thing you do not: the actual clock-tree delays.")],
          [R("Hold fixing costs area and power, never frequency - which is why it is "
             "always possible.")]], GREEN, CARD_G),
        ("What RTL can do to make it impossible",
         [[R("Gate a clock by hand instead of using an enable - it adds skew you cannot "
             "control.")],
          [R("Cross clock domains without a synchroniser - no amount of buffering fixes "
             "that.")],
          [R("Use both clock edges in the same path - it halves the hold budget.")]],
         RED, CARD_R)],
        h=2011680)

    d.card(s, y + G, "The one hold fix that belongs in RTL",
           [[R("A proper two-flop synchroniser on every asynchronous crossing. That is not "
               "a hold fix in the STA sense - it is what stops the crossing being a timing "
               "question at all.", s=10.5)]],
           accent=TEAL, h=594360)

    # ---------------------------------------------------- the lab numbers
    s = d.slide("6c · MEASURED", "The Numbers You Will Produce Yourself")
    y = d.image(s, TOP - 45720, "measured_results", 4846320)
    d.lead(s, y + G, [[R("Nothing quoted in this topic is a claim you cannot reproduce "
                         "with  make.", b=True, c=TEAL, s=10.5)]], h=228600)

    # -------------------------------------------------- the honest caveat
    s = d.slide("6c · AN HONEST NOTE", "How the Hold Demo Adds Its Delay, and Why",
                accent=AMBER)
    y = d.code(s, TOP, [
        "// rtl/hold_fixed.v",
        "// dly_sel is a real input port, tied to 0 by the testbench.",
        "assign d0 = q1 ^ dly_sel[0];      // two XOR gates in the data path",
        "assign d1 = d0 ^ dly_sel[1];      // functionally a no-op when dly_sel == 0",
        "",
        "// Why not a chain of buffers with (* keep *) ?",
        "//   opt_clean deletes them. keep_hierarchy plus -flatten deletes them too.",
        "//   Only logic that a real port can influence survives optimisation."],
        title="what the lab actually does, and what it is standing in for", size=9.5)

    y = d.cols(s, y + G, [
        ("What this demonstrates honestly",
         [[R("That adding delay to the data path turns a hold violation into a met one, "
             "and by how much.")],
          [R("That the tool cannot be asked politely to keep useless logic.")]],
         GREEN, CARD_G),
        ("What it is NOT",
         [[R("A style to copy. In a real flow, place-and-route inserts hold buffers with "
             "knowledge of the actual clock tree.")],
          [R("Writing XOR gates into your datapath to fix hold is not engineering - it is "
             "a teaching device, and it is labelled as one.", b=True, c=RED)]],
         AMBER, CARD_A)],
        h=1920240)

    d.lead(s, y + G, [[R("Being told what a demonstration cannot show is part of the "
                         "demonstration.", b=True, c=NAVY, s=10.5)]], h=274320)

    # ------------------------------------------------------- the procedure
    s = d.slide("6c · THE PROCEDURE", "What To Do When the Report Is Red", accent=GREEN)
    y = d.table(s, TOP,
                ["Step", "Do this", "Because"],
                [["1", "Read the unconstrained-endpoint count first",
                  "a clean report on half a design is worthless"],
                 ["2", "Is it setup or hold? Look at the path type",
                  "the two need opposite fixes"],
                 ["3", "Read the startpoint and endpoint by name",
                  "it often names the problem for you"],
                 ["4", "Ask whether the path is real",
                  "half of all violations are constraint bugs"],
                 ["5", "Look at the largest incr in the path",
                  "one big cell or fifty small ones - different fixes"],
                 ["6", "Compare WNS with TNS", "one path, or the whole design?"],
                 ["7", "Apply the cheapest fix that could work",
                  "and re-run before trying the next one"],
                 ["8", "Change ONE thing per run", "or you will not know what helped"]],
                [685800, 4846320, 5715000], rh=274320, bold_cols=(0,))

    d.card(s, y + G, "Step 8 is the one people skip",
           [[R("Under deadline pressure it is tempting to change the period, the effort "
               "level and the RTL all at once. When the slack moves you will have no idea "
               "which change did it - and no idea what to undo when it moves the wrong "
               "way.", c=RED, s=10.5)]],
           accent=RED, fill=CARD_R, h=822960)

    # ------------------------------------------------------ closure loop
    s = d.slide("6c · CLOSURE", "Timing Closure Is a Loop, and You Exit It Once")
    y = d.image(s, TOP - 45720, "closure_loop", 4846320)
    d.lead(s, y + G, [[R("A design is closed when WNS >= 0 at the slow corner, hold >= 0 at "
                         "the fast corner, and the unconstrained count is zero. Two out of "
                         "three is not closed.", b=True, c=GREEN, s=10.5)]], h=274320)

    # -------------------------------------------------- common mistakes
    s = d.slide("6c · MISTAKES", "Ten Ways To Get a Green Report and a Broken Chip",
                accent=RED)
    y = d.table(s, TOP,
                ["#", "The mistake", "What it costs you"],
                [["1", "No constraint file at all", "every path unchecked, report meaningless"],
                 ["2", "Clock declared, I/O not", "every boundary path unchecked"],
                 ["3", "A generated clock never declared", "a whole domain unchecked"],
                 ["4", "set_false_path used to silence a real path", "a field failure"],
                 ["5", "Multicycle setup without the hold line", "a hold violation you created"],
                 ["6", "Multicycle claimed without an enable in the RTL", "wrong data captured"],
                 ["7", "Uncertainty reduced to make the report pass", "no margin on silicon"],
                 ["8", "Signing off setup at the typical corner", "fails on slow silicon"],
                 ["9", "Ignoring hold because the clock is slow", "fails at every speed"],
                 ["10", "Never checking the unconstrained count", "all of the above, silently"]],
                [548640, 5486400, 5212080], rh=265176, bold_cols=(0,))
    d.lead(s, y + G, [[R("Nine of these ten produce a report that says everything is fine.",
                         b=True, c=RED, s=11)]], h=274320)

    # ------------------------------------------------------ 6c checkpoint
    s = d.slide("6c · CHECKPOINT", "Eight Questions Before the Labs", accent=GREEN)
    y = d.table(s, TOP,
                ["#", "Question", "The answer in one line"],
                [["1", "Setup violation - what does the chip do?",
                  "works, but only at a lower frequency"],
                 ["2", "Hold violation - what does it do?", "does not work at any frequency"],
                 ["3", "Does the period appear in the hold equation?",
                  "no - that is the whole point"],
                 ["4", "Late capture clock: helps which check?",
                  "setup; it hurts hold by the same amount"],
                 ["5", "Why do hold problems appear after layout?",
                  "before it, there is no clock tree, so no real skew"],
                 ["6", "How is hold fixed?", "by ADDING delay to the data path"],
                 ["7", "What does that cost?", "area and power, never frequency"],
                 ["8", "Setup at which corner, hold at which?",
                  "setup at slow, hold at fast"]],
                [548640, 4846320, 5852160], rh=283464, bold_cols=(0,))
    d.lead(s, y + G, [[R("Answer these eight and the labs will feel like confirmation "
                         "rather than discovery.", b=True, c=GREEN, s=11)]], h=274320)
