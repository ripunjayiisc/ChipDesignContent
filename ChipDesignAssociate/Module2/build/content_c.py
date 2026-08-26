# -*- coding: utf-8 -*-
"""Topic 3 deck — 3C: sequential logic, flip-flops, registers, state machines."""
from deckkit import *
from content_a import R, G


def build(d):
    # =============================================== SECTION 3C divider
    d.section_slide("SUBTOPIC 3C", "Sequential Logic, Flip-Flops, Registers and State Machines",
                    "Circuits that remember — where time, the clock and state enter the design.",
                    ["The clock, latches, flip-flops and how edge-triggering is actually built",
                     "Setup, hold, clock-to-Q, metastability, skew and the fₘₐₓ calculation",
                     "Registers, shift registers and counters",
                     "Finite state machines: Moore, Mealy, encoding, and the Verilog template"],
                    accent=AMBER)

    # ================================================================ clock
    s = d.slide("TOPIC 3C · THE CLOCK", "The Clock — One Heartbeat for the Whole Design", AMBER)
    y = d.lead(s, TOP, [[
        R("Synchronous design means every storage element in a block changes at the same instant, "
          "on the same edge of one clock. ", b=True, c=NAVY, s=12.5),
        R("That single convention is what makes a billion-transistor chip analysable at all: it reduces "
          "'does this circuit work?' to a set of arithmetic checks on one clock period.")]], h=548640)
    y = d.image(s, y + 45720, "clock_anatomy", 3383280)
    d.cols(s, y + 91440, [
        ("Worked conversions",
         [[R("T = 10 ns → f = 100 MHz.   T = 2 ns → f = 500 MHz.   T = 400 ps → f = 2.5 GHz.", s=10.5)],
          [R("f = 3.2 GHz → T = 312.5 ps.", s=10.5)]], TEAL, CARD),
        ("Two rules that are never broken in RTL",
         [[R("1. Never generate a clock in combinational logic — use a clock enable instead.",
             s=10.5, b=True, c=RED)],
          [R("2. Never mix posedge and negedge of the same clock in one design without a very good, "
             "documented reason.", s=10.5, b=True, c=RED)]], RED, CARD_R)], h=1097280)

    # ================================================================ SR latch
    s = d.slide("TOPIC 3C · THE FIRST MEMORY", "The SR Latch — Cross-Coupling Creates Memory", AMBER)
    y = d.lead(s, TOP, [[
        R("Take two NOR gates and feed each one's output back into the other. ", b=True, c=NAVY, s=12.5),
        R("The circuit now has two stable configurations and will sit in whichever one you last pushed "
          "it into. That is memory — and it is the ancestor of every flip-flop, register and SRAM cell "
          "on the chip.")]], h=548640)
    y = d.image(s, y + 45720, "sr_latch", 3383280)
    d.card(s, y + 91440, "Where you actually meet an SR latch",
           [[R("Rarely by choice in RTL — but it is the internal structure of every D latch, and a "
               "NAND version (active-low S̄R̄) is the standard hardware de-bouncer for a mechanical "
               "switch. It is also what an accidental combinational feedback loop in your Verilog "
               "turns into, which is why simulators warn about them.")]],
           accent=TEAL, h=822960)

    # ================================================================ latch vs FF
    s = d.slide("TOPIC 3C · THE KEY DISTINCTION", "Latch vs Flip-Flop — The Difference That Matters Most",
                RED)
    y = d.lead(s, TOP, [[
        R("A latch is LEVEL-sensitive: it is transparent for as long as its enable is high. "
          "A flip-flop is EDGE-triggered: it samples once, at one instant. ", b=True, c=NAVY, s=12.5),
        R("Everything about timing analysis assumes flip-flops. Get this wrong and nothing downstream works.")]],
        h=594360)
    y = d.image(s, y + 45720, "latch_vs_ff", 3200400)
    d.cols(s, y + 91440, [
        ("Latch", [[R("Transparent while EN = 1", s=10.5)],
                   [R("Output may change many times per cycle", s=10.5)],
                   [R("Smaller and lower power", s=10.5)],
                   [R("Hard to time; usually unintended", b=True, c=RED, s=10.5)]], RED, CARD_R),
        ("Flip-flop", [[R("Samples only on the clock edge", s=10.5)],
                       [R("Exactly one change per cycle", s=10.5)],
                       [R("About twice the area of a latch", s=10.5)],
                       [R("The only element you should infer", b=True, c=GREEN, s=10.5)]],
         GREEN, CARD_G)], h=1188720)

    # ================================================================ master slave
    s = d.slide("TOPIC 3C · CONSTRUCTION", "How Edge-Triggering Is Built — The Master–Slave Pair", AMBER)
    y = d.lead(s, TOP, [[
        R("A flip-flop is two latches in series driven by opposite clock phases. ", b=True, c=NAVY, s=12.5),
        R("Because they are never transparent at the same time, data cannot race through both in one "
          "clock phase — and that, precisely, is edge-triggering.")]], h=502920)
    y = d.image(s, y + 45720, "master_slave", 3383280)
    d.card(s, y + 91440, "Why this matters to you as an RTL designer",
           [[R("It explains where t_setup, t_hold and t_cq physically come from: setup is the time the "
               "master latch needs to capture, hold is the time before the master closes, and t_cq is "
               "the delay through the slave. It also explains why a flip-flop is roughly twice the area "
               "of a latch — you are paying for two storage nodes.")]],
           accent=TEAL, h=822960)

    # ================================================================ FF family
    s = d.slide("TOPIC 3C · THE FAMILY", "D, T, JK and SR Flip-Flops")
    y = d.lead(s, TOP, [[
        R("Four behaviours, one clocked structure. ", b=True, c=NAVY, s=12.5),
        R("In modern design only the D flip-flop is ever instantiated — but you must be able to read and "
          "convert between all four, because textbooks, exams and legacy schematics use them all.")]],
        h=502920)
    y = d.image(s, y + 45720, "ff_family", 3520440)
    d.card(s, y + 91440, "Why the D flip-flop won",
           [[R("It has no forbidden state, no toggle surprise, and its next state is simply its input — "
               "which means synthesis can map any state equation directly onto it. Standard-cell "
               "libraries therefore contain dozens of D flip-flop variants (with/without reset, set, "
               "enable, scan) and no JK at all. "),
             R("If you need a T or JK, build it from a D plus a little logic.", b=True, c=NAVY)]],
           accent=GREEN, fill=CARD_G, h=960120)

    # ================================================================ char / excitation
    s = d.slide("TOPIC 3C · TABLES YOU NEED", "Characteristic and Excitation Tables, and FF Conversion")
    y = d.lead(s, TOP, [[
        R("A characteristic table answers 'given the inputs, what is the next state?'. "
          "An excitation table answers the reverse — 'to make this transition happen, what inputs do I "
          "need?'. ", b=True, c=NAVY, s=12.5),
        R("You use the characteristic table to ANALYSE a circuit and the excitation table to DESIGN one.")]],
        h=594360)
    y = d.table(s, y + G,
                ["Q → Q_next", "D", "T", "J   K", "S   R"],
                [["0  →  0", "0", "0", "0   ×", "0   ×"],
                 ["0  →  1", "1", "1", "1   ×", "1   0"],
                 ["1  →  0", "0", "1", "×   1", "0   1"],
                 ["1  →  1", "1", "0", "×   0", "×   0"]],
                [2560320, 1828800, 1828800, 2514600, 2514600], rh=365760,
                bold_cols=(0,), col_colors={0: TEAL}, size=11)
    y = d.cols(s, y + G, [
        ("Characteristic equations",
         [[R("D-FF:    Q⁺ = D", s=10.5, f=MONO_FONT)],
          [R("T-FF:    Q⁺ = T ⊕ Q", s=10.5, f=MONO_FONT)],
          [R("JK-FF:   Q⁺ = J·Q' + K'·Q", s=10.5, f=MONO_FONT)],
          [R("SR-FF:   Q⁺ = S + R'·Q   (SR ≠ 11)", s=10.5, f=MONO_FONT)]], TEAL, CARD),
        ("Converting one to another",
         [[R("Put the target's excitation table beside the source's, K-map the required source inputs "
             "as functions of (present state, target inputs), and add that logic in front.", s=10.5)],
          [R("D from T:   D = T ⊕ Q        T from D:   T = D ⊕ Q", s=10.5, f=MONO_FONT, b=True, c=NAVY)]],
         AMBER, CARD_A)], h=1188720)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("The × entries are don't-cares — and they are exactly what makes JK-based designs "
          "minimise so well on paper.", s=10.5, i=True, c=SLATE)]])

    # ================================================================ reset
    s = d.slide("TOPIC 3C · INITIALISATION", "Reset — Synchronous vs Asynchronous", RED)
    y = d.lead(s, TOP, [[
        R("At power-up every flip-flop holds an unknown value. ", b=True, c=NAVY, s=12.5),
        R("Reset is what forces the design into a known starting state. Choosing the wrong style, or "
          "releasing reset carelessly, produces bugs that only appear on real silicon.")]], h=502920)
    y = d.code(s, y + G, [
        "// ASYNCHRONOUS reset - reset appears in the sensitivity list",
        "always @(posedge clk or posedge rst)",
        "    if (rst) q <= 1'b0;",
        "    else     q <= d;",
        "",
        "// SYNCHRONOUS reset - reset is just another input to the D logic",
        "always @(posedge clk)",
        "    if (rst) q <= 1'b0;",
        "    else     q <= d;",
    ], size=10, title="The two templates — memorise both exactly", accent=AMBER)
    y = d.cols(s, y + G, [
        ("Asynchronous",
         [[R("Takes effect immediately, clock or no clock.", s=10.5)],
          [R("Essential at power-up, when the PLL has not locked and there is no clock yet.",
             s=10.5, b=True, c=GREEN)],
          [R("Danger: its RELEASE is asynchronous and can violate recovery/removal time — so it must be "
             "de-asserted synchronously.", s=10.5, b=True, c=RED)]], AMBER, CARD_A),
        ("Synchronous",
         [[R("Takes effect only on a clock edge.", s=10.5)],
          [R("Fully covered by normal static timing analysis; no special constraints; filters glitches on "
             "the reset line.", s=10.5, b=True, c=GREEN)],
          [R("Danger: useless if the clock is not running.", s=10.5, b=True, c=RED)]], TEAL, CARD),
        ("What industry actually does",
         [[R("Asynchronous assert, synchronous de-assert — the 'reset synchroniser'.",
             s=10.5, b=True, c=NAVY)],
          [R("Two flip-flops clocked by the destination clock, with their async reset tied to the raw "
             "reset. Best of both.", s=10.5)]], GREEN, CARD_G)], h=1737360)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Also note: ", b=True, c=NAVY, s=10.5),
        R("on most FPGAs a global reset costs routing resources and is often unnecessary because the "
          "bitstream initialises every flip-flop. On an ASIC it is mandatory.", s=10.5)]])

    # ================================================================ tiered 3C
    s = d.slide("TOPIC 3C · TIERED DEPTH", "Understanding Sequential Logic at Four Levels")
    y = d.lead(s, TOP, [[
        R("The same idea at four depths.", s=12)]], h=320040)
    d.tiers(s, y + G, [
        ("BASIC", "A circuit that remembers. Its output depends not only on what you feed it now but on "
                  "what happened before. A clock tells it when to update.", AMBER),
        ("INTERMEDIATE", "Combinational logic plus flip-flops in a feedback loop. The flip-flops hold the "
                         "STATE; the logic computes the next state and the outputs. Counters, shift "
                         "registers and controllers are all this shape.", AMBER),
        ("ADVANCED", "Correctness is a timing property, not just a logic one: every path must satisfy "
                     "T ≥ t_cq + t_logic + t_setup and t_cq + t_logic,min ≥ t_hold. Any input not "
                     "synchronous to the clock must be synchronised or it will cause metastability.",
         RED),
        ("INDUSTRY", "Written as `always @(posedge clk)` with non-blocking assignments. Timing is closed "
                     "by STA against SDC constraints; clock trees are balanced by CTS; every "
                     "clock-domain crossing is reviewed as a first-class design artefact — CDC bugs are "
                     "the leading cause of silicon respins.", GREEN)],
        h=960120, gap=68580)

    # ================================================================ ff timing
    s = d.slide("TOPIC 3C · TIMING PARAMETERS", "Setup, Hold and Clock-to-Q", RED)
    y = d.lead(s, TOP, [[
        R("A flip-flop is not instantaneous. ", b=True, c=NAVY, s=12.5),
        R("It requires the data to be steady for a window around the clock edge, and it takes time to "
          "produce its output afterwards. These three numbers come from the library datasheet and are "
          "the entire basis of timing analysis.")]], h=502920)
    y = d.image(s, y + 45720, "ff_timing", 3200400)
    d.cols(s, y + 91440, [
        ("Setup violation", [[R("Data arrives TOO LATE. Fix by shortening the logic path, or by "
                                "slowing the clock. ", s=10.5),
                              R("A setup problem is a speed problem.", b=True, c=NAVY, s=10.5)]],
         RED, CARD_R),
        ("Hold violation", [[R("Data arrives TOO EARLY and overwrites the value being captured. Fix by "
                               "ADDING delay (buffers) on the short path. ", s=10.5),
                             R("Slowing the clock does not help at all.", b=True, c=RED, s=10.5)]],
         AMBER, CARD_A),
        ("Clock-to-Q", [[R("Not a constraint but a cost — it eats into every clock period before your "
                           "logic even starts. Faster (larger) flip-flops have smaller t_cq and larger "
                           "area and power.", s=10.5)]], TEAL, CARD)], h=1188720)

    # ================================================================ metastability
    s = d.slide("TOPIC 3C · METASTABILITY", "When the Rules Are Broken — Metastability", RED)
    y = d.lead(s, TOP, [[
        R("If data changes inside the setup/hold window, the flip-flop may enter a metastable state: "
          "its output hovers at an invalid intermediate voltage for an unbounded time, then resolves "
          "randomly to 0 or 1. ", b=True, c=NAVY, s=12.5),
        R("It cannot be prevented — only made astronomically unlikely.")]], h=594360)
    y = d.image(s, y + 45720, "metastability", 3200400)
    d.card(s, y + 91440, "MTBF — the number you quote in a design review",
           [[R("MTBF = e^(t_r / τ) / (T₀ · f_clk · f_data)", b=True, c=NAVY, f=MONO_FONT),
             R("   where t_r is the resolution time you allow, τ and T₀ are library constants, and "
               "f_clk, f_data are the clock and data-change rates.")],
            [R("Because t_r sits in an exponential, adding ONE more synchroniser flip-flop typically "
               "moves MTBF from seconds to millions of years. That is why two stages is the universal "
               "minimum and three is used for very high-speed or safety-critical crossings.")]],
           accent=RED, fill=CARD_R, h=1280160)

    # ================================================================ timing path
    s = d.slide("TOPIC 3C · THE TIMING PATH", "Where the Maximum Clock Frequency Comes From")
    y = d.lead(s, TOP, [[
        R("Every synchronous design reduces to this one picture: ", b=True, c=NAVY, s=12.5),
        R("a launching flip-flop, some combinational logic, and a capturing flip-flop. The clock period "
          "must be long enough for a signal to get all the way across before the next edge arrives.")]],
        h=502920)
    y = d.image(s, y + 45720, "fmax_path", 3383280)
    d.card(s, y + 91440, "The two checks, and what each one means",
           [[R("Setup (max delay): ", b=True, c=RED),
             R("T_clk ≥ t_cq + t_logic,max + t_setup + t_skew + t_jitter.  "
               "The LONGEST path sets your maximum frequency.")],
            [R("Hold (min delay): ", b=True, c=AMBER),
             R("t_cq + t_logic,min ≥ t_hold + t_skew.  "
               "The SHORTEST path must still be long enough. This check is frequency-independent — a "
               "hold violation is broken at DC.")]],
           accent=TEAL, h=960120)

    # ================================================================ practical example 4
    s = d.slide("TOPIC 3C · PRACTICAL EXAMPLE 4", "Numerical: fₘₐₓ, Slack and the Hold Check", GREEN)
    y = d.card(s, TOP, "Given",
               [[R("t_cq = 60 ps, t_setup = 50 ps, t_hold = 40 ps, clock skew = 25 ps (capture clock "
                   "arrives LATE), jitter = 15 ps. The combinational path between two flip-flops has "
                   "t_logic,max = 240 ps and t_logic,min = 30 ps. Target frequency 2.0 GHz.")]],
               accent=TEAL, h=822960)
    y = d.code(s, y + G, [
        "SETUP CHECK",
        "  Required period  T_req = t_cq + t_logic,max + t_setup + t_jitter - t_skew",
        "                         = 60 + 240 + 50 + 15 - 25          (late capture clock HELPS setup)",
        "                         = 340 ps",
        "  f_max = 1 / 340 ps = 2.94 GHz",
        "  Target 2.0 GHz -> T_target = 500 ps",
        "  SETUP SLACK = 500 - 340 = +160 ps          PASS  (positive slack = met)",
        "",
        "HOLD CHECK",
        "  Required:  t_cq + t_logic,min  >=  t_hold + t_skew",
        "             60   + 30           >=  40     + 25",
        "             90                  >=  65",
        "  HOLD SLACK = 90 - 65 = +25 ps              PASS",
        "",
        "WHAT IF the short path were only 5 ps of logic?",
        "  60 + 5 = 65  >=  65   ->  slack = 0 ps, marginal; the tool would insert delay buffers.",
    ], size=8.4, title="Do setup and hold as two separate calculations — never together", accent=GREEN)
    d.cols(s, y + G, [
        ("Sign convention", [[R("Positive slack = requirement met, with margin to spare.", s=10.5)],
                             [R("Negative slack = VIOLATION. The number tells you by how much.",
                                s=10.5, b=True, c=RED)]], NAVY, CARD),
        ("Note on skew", [[R("A late capture clock helps setup and hurts hold — which is why skew "
                             "appears with opposite signs in the two checks. Getting that sign wrong is "
                             "the single most common exam mistake.", s=10.5)]], AMBER, CARD_A)],
        h=1005840)

    # ================================================================ skew
    s = d.slide("TOPIC 3C · CLOCK QUALITY", "Clock Skew and Jitter")
    y = d.lead(s, TOP, [[
        R("The idealisation that 'the clock edge arrives everywhere at once' is false. ",
          b=True, c=NAVY, s=12.5),
        R("Skew is a fixed difference between flip-flops; jitter is a random difference between cycles. "
          "Both are subtracted from the time available for your logic.")]], h=502920)
    y = d.image(s, y + 45720, "clock_skew", 3200400)
    d.cols(s, y + 91440, [
        ("Skew — systematic", [[R("Cause: unequal clock-tree path lengths and loads.", s=10.5)],
                               [R("Fixed by clock-tree synthesis (CTS), which inserts buffers to "
                                  "balance every branch to within a few tens of picoseconds.", s=10.5)]],
         TEAL, CARD),
        ("Jitter — random", [[R("Cause: PLL noise, supply droop, crosstalk, temperature.", s=10.5)],
                             [R("Cannot be designed out; budgeted as an uncertainty in the SDC "
                                "constraints and paid for out of every clock period.", s=10.5)]],
         AMBER, CARD_A),
        ("Useful skew", [[R("Deliberately delaying a capture clock borrows time for a slow path from the "
                            "next stage. Powerful, and dangerous — it tightens the hold check on the "
                            "same path.", s=10.5)]], GREEN, CARD_G)], h=1417320)

    # ================================================================ registers
    s = d.slide("TOPIC 3C · REGISTERS", "Registers and Shift Registers")
    y = d.lead(s, TOP, [[
        R("A register is simply n flip-flops sharing one clock. ", b=True, c=NAVY, s=12.5),
        R("Wire each Q to the next D and you have a shift register — the basis of serial links, delay "
          "lines, scan chains for test, and multiply/divide by two.")]], h=502920)
    y = d.image(s, y + 45720, "shift_registers", 3337560)
    d.card(s, y + 91440, "Applications you will actually build",
           [[R("Serialisation ", b=True, c=NAVY), R("(SPI, UART, JTAG) · "),
             R("Delay lines ", b=True, c=NAVY), R("and pipeline balancing · "),
             R("Synchronisers ", b=True, c=NAVY), R("(a 2-bit shift register is exactly the 2-FF "
                                                    "synchroniser) · ")],
            [R("Scan chains ", b=True, c=NAVY),
             R("— during manufacturing test every flip-flop in the chip is rewired into one giant shift "
               "register so patterns can be loaded and results read out.   "),
             R("LFSRs ", b=True, c=NAVY),
             R("— add an XOR feedback tap and you have a pseudo-random generator or a CRC engine.")]],
           accent=TEAL, h=960120)

    # ================================================================ counters
    s = d.slide("TOPIC 3C · COUNTERS", "Counters — Ripple vs Synchronous", AMBER)
    y = d.lead(s, TOP, [[
        R("A counter is a state machine whose state happens to be a number. ", b=True, c=NAVY, s=12.5),
        R("There are two ways to build one, and only one of them belongs in a synthesised design.")]],
        h=457200)
    y = d.image(s, y + G, "counters", 3383280)
    d.cols(s, y + 91440, [
        ("Varieties you should know",
         [[R("Up / down / up-down · loadable · with enable · mod-N (divide by N) · ring counter "
             "(one-hot, N states from N flip-flops) · Johnson / twisted-ring (2N states from N "
             "flip-flops) · LFSR (2ⁿ−1 states, maximal length, but not in numeric order).", s=10.5)]],
         TEAL, CARD),
        ("Rule",
         [[R("Never write a ripple counter in RTL.", b=True, c=RED, s=11)],
          [R("It creates a second clock domain out of a data signal, breaks static timing analysis, and "
             "produces transient wrong values. Always use one clock and an enable.", s=10.5)]],
         RED, CARD_R)], h=1051560)

    # ================================================================ practical example 5
    s = d.slide("TOPIC 3C · PRACTICAL EXAMPLE 5", "Worked: A Mod-10 (BCD) Synchronous Counter", GREEN)
    y = d.image(s, TOP, "mod10_design", 3520440)
    y = d.card(s, y + 91440, "How the gate-level equations were obtained",
               [[R("1. Write the state table (0000 … 1001 and the wrap to 0000).   "
                   "2. For each bit, tabulate Qᵢ → Qᵢ⁺.   "
                   "3. Since D = Q⁺, the D column IS the next-state column.   "
                   "4. K-map each Dᵢ over Q₃Q₂Q₁Q₀, treating states 1010–1111 as don't-cares.   "
                   "5. Read off the minimal SOP.")],
                [R("Check one row by hand: at count 9 (Q = 1001), D₀ = Q₀' = 0, "
                   "D₁ = Q₁ ⊕ (Q₀·Q₃') = 0 ⊕ (1·0) = 0, D₂ = Q₂ ⊕ (Q₁·Q₀) = 0 ⊕ 0 = 0, "
                   "D₃ = Q₃ ⊕ (Q₃Q₀ + Q₂Q₁Q₀) = 1 ⊕ 1 = 0. Next state = 0000. ",
                  i=True, c=SLATE),
                 R("Correct.", b=True, c=GREEN)],
                [R("Trap: ", b=True, c=RED),
                 R("states 1010–1111 are unreachable but not impossible — a glitch or SEU can land you "
                   "there. Because we treated them as don't-cares the counter may lock up. A SAFE "
                   "counter forces any illegal state back to 0000 explicitly.")]],
               accent=GREEN, fill=CARD_G, h=1600200)

    # ================================================================ FSM intro
    s = d.slide("TOPIC 3C · STATE MACHINES", "Finite State Machines — The Universal Controller")
    y = d.lead(s, TOP, [[
        R("An FSM is the formal name for 'a circuit that remembers where it is in a sequence'. ",
          b=True, c=NAVY, s=12.5),
        R("Formally it is a 6-tuple (S, S₀, X, Y, δ, λ): a finite set of states, a start state, an input "
          "alphabet, an output alphabet, a next-state function δ, and an output function λ. "
          "Every protocol engine, bus controller, arbiter and CPU control unit is one.")]], h=640080)
    y = d.cols(s, y + G, [
        ("The three pieces of hardware",
         [[R("1. State register — n flip-flops holding the present state.", s=10.5)],
          [R("2. Next-state logic — combinational, computes δ(state, input).", s=10.5)],
          [R("3. Output logic — combinational, computes λ.", s=10.5)],
          [R("Nothing else. Every FSM is this.", b=True, c=NAVY, s=10.5)]], TEAL, CARD),
        ("What counts as a 'state'",
         [[R("A state is an equivalence class of histories: two input histories are the same state if "
             "the machine will behave identically from now on.", s=10.5)],
          [R("This is why the 1011 detector needs five states — 'nothing', '1', '10', '101', '1011' — "
             "and not thirty-two.", s=10.5)]], AMBER, CARD_A),
        ("Why finite matters",
         [[R("Finite states = finite flip-flops = a circuit you can actually build and exhaustively "
             "verify.", s=10.5)],
          [R("An FSM cannot count arbitrarily high or match arbitrarily deep nesting — for that you need "
             "a datapath (counter, stack) alongside it. That is the FSMD idea at the end of this "
             "section.", s=10.5)]], GREEN, CARD_G)], h=2468880)
    d.card(s, y + 137160, "The Huffman model",
           [[R("Drawing the three blocks with the state register in a feedback loop is called the Huffman "
               "model of a sequential circuit. It is the same picture as the 'sequential' half of the "
               "very first diagram in subtopic 3b — every sequential circuit, however complicated, "
               "reduces to it.")]],
           accent=TEAL, h=1005840)

    # ================================================================ moore vs mealy
    s = d.slide("TOPIC 3C · TWO STYLES", "Moore vs Mealy Machines")
    y = d.lead(s, TOP, [[
        R("The only difference is whether the output logic can see the INPUT as well as the state. ",
          b=True, c=NAVY, s=12.5),
        R("That one wire changes the timing behaviour, the state count and the glitch risk.")]], h=457200)
    y = d.image(s, y + G, "moore_mealy", 3566160)
    d.card(s, y + 91440, "Which one should you use?",
           [[R("Default to Moore. ", b=True, c=GREEN),
             R("Its outputs come straight off flip-flops, so they are glitch-free and easy to time. "
               "Use Mealy when you genuinely need the one-cycle-earlier response, and then "),
             R("register the Mealy output", b=True, c=NAVY),
             R(" before it leaves the block — which, of course, turns it back into a Moore output one "
               "cycle later.")]],
           accent=GREEN, fill=CARD_G, h=776224)

    # ================================================================ FSM procedure
    s = d.slide("TOPIC 3C · PROCEDURE", "The Six Steps of FSM Design")
    y = d.lead(s, TOP, [[
        R("Do these in order, every time. ", b=True, c=NAVY, s=12.5),
        R("The state diagram is the design; everything after it is mechanical. If the diagram is wrong, "
          "no amount of Verilog will save you.")]], h=457200)
    y = d.image(s, y + G, "fsm_procedure", 2743200)
    y = d.card(s, y + 91440, "Two checks to run on the state diagram before you write any code",
               [[R("Completeness: ", b=True, c=NAVY),
                 R("from every state, is there exactly one outgoing arc for EVERY possible input value? "
                   "A missing arc means an undefined transition — in hardware, a latch or a lock-up.")],
                [R("Determinism: ", b=True, c=NAVY),
                 R("is there at most one arc for each input value? Two arcs labelled '1' out of one state "
                   "is not a circuit, it is a contradiction.")],
                [R("For a machine with s states and one binary input, count the arcs: there must be "
                   "exactly 2s of them.", i=True, c=SLATE)]],
               accent=AMBER, fill=CARD_A, h=1188720)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("State minimisation (step 3) is optional in practice — synthesis tools do it, and modern FPGAs "
          "have flip-flops to spare. Understand it; do not agonise over it.", s=10.5, i=True, c=SLATE)]])

    # ================================================================ encoding
    s = d.slide("TOPIC 3C · ENCODING", "State Encoding — Binary, Gray and One-Hot")
    y = d.lead(s, TOP, [[
        R("The states in your diagram are names; the flip-flops hold bits. ", b=True, c=NAVY, s=12.5),
        R("How you map one to the other changes the flip-flop count, the amount of next-state logic, the "
          "speed and the power — without changing the behaviour at all.")]], h=502920)
    y = d.image(s, y + 45720, "state_encoding", 3383280)
    d.card(s, y + 91440, "How to choose",
           [[R("FPGA: ", b=True, c=GREEN),
             R("one-hot, almost always. Flip-flops are free and abundant; LUT depth is what costs you "
               "speed, and one-hot next-state logic is one level deep.   ")],
            [R("ASIC with many states: ", b=True, c=TEAL),
             R("binary, to keep the register count and hence area down.   "),
             R("Low-power or clock-crossing: ", b=True, c=AMBER),
             R("Gray, because only one bit toggles per transition — less switching energy and safe to "
               "sample across a clock domain.")]],
           accent=TEAL, h=960120)

    # ================================================================ FSM worked: diagram
    s = d.slide("TOPIC 3C · WORKED EXAMPLE", "Designing a '1011' Sequence Detector — Step 1", GREEN)
    y = d.lead(s, TOP, [[
        R("Specification. ", b=True, c=NAVY, s=12.5),
        R("A serial input X arrives one bit per clock. Assert output Z whenever the last four bits "
          "received were 1, 0, 1, 1. Overlapping sequences count — so the stream 1011011 contains "
          "TWO occurrences.")]], h=502920)
    y = d.image(s, y + 45720, "fsm_1011", 3657600)
    d.card(s, y + 91440, "How each state was chosen",
           [[R("Ask: 'what is the longest PREFIX of 1011 that is currently a suffix of what I have "
               "received?' That question has exactly five answers — none, 1, 10, 101, 1011 — so there "
               "are five states, and the answer to the question IS the state. "),
             R("This suffix-matching insight generalises to any pattern detector.", b=True, c=NAVY)]],
           accent=GREEN, fill=CARD_G, h=822960)

    # ================================================================ FSM worked: table
    s = d.slide("TOPIC 3C · WORKED EXAMPLE", "'1011' Detector — Steps 2 to 5: Table, Encoding, Logic",
                GREEN)
    y = d.table(s, TOP, ["Present state", "Encoding Q₂Q₁Q₀", "Next state (X=0)", "Next state (X=1)", "Z"],
                [["S0  (start)", "000", "S0   000", "S1   001", "0"],
                 ["S1  (1)", "001", "S2   010", "S1   001", "0"],
                 ["S2  (10)", "010", "S0   000", "S3   011", "0"],
                 ["S3  (101)", "011", "S2   010", "S4   100", "0"],
                 ["S4  (1011)", "100", "S2   010", "S1   001", "1"]],
                [2743200, 2194560, 2560320, 2560320, 1188720], rh=310896,
                bold_cols=(0, 4), col_colors={0: TEAL, 4: GREEN}, size=10)
    y = d.code(s, y + G, [
        "Next-state equations   (K-map each D bit over Q2 Q1 Q0 X;  codes 101-111 are don't-cares)",
        "",
        "  D2 = Q1 . Q0 . X                     only S3 (011) with X=1 reaches S4",
        "",
        "  D1 = X' . (Q2 + Q0)  +  Q1 . Q0' . X",
        "       ^^^^^^^^^^^^^^     ^^^^^^^^^^^^",
        "       S1,S3,S4 on X=0    S2 on X=1  (010 -> 011)",
        "",
        "  D0 = X . (Q1 . Q0)'                  every X=1 arc lands on S1 or S3, both odd,",
        "                                       except S3 (011) which goes to S4 (100)",
        "",
        "Output equation  (Moore - a function of the state alone)",
        "  Z  = Q2                              S4 is the only state whose code has Q2 = 1",
    ], size=9.5, title="Derive, then ALWAYS re-check against the table row by row", accent=AMBER)
    d.text(s, ML, y + G, MW, 274320, [[
        R("Check one row by hand: S3 = 011 with X = 1 gives D₂ = 1·1·1 = 1, D₁ = 0·(…) + 1·0·1 = 0, "
          "D₀ = 1·(1·1)' = 0 → next state 100 = S4.  ✓   Notice too that Z = Q₂ fell out for free "
          "because we chose the encoding well. All of this is what synthesis does for you when you "
          "write the case statement on the next slide.", s=10.5, i=True, c=SLATE)]])

    # ================================================================ FSM verilog
    s = d.slide("TOPIC 3C · THE RTL TEMPLATE", "'1011' Detector — The Three-Block Verilog FSM", GREEN)
    y = d.code(s, TOP, [
        "module seq_detect_1011 (input clk, input rst_n, input x, output reg z);",
        "",
        "    localparam S0=3'd0, S1=3'd1, S2=3'd2, S3=3'd3, S4=3'd4;",
        "    reg [2:0] state, next;",
        "",
        "    // ---- BLOCK 1 : state register  (sequential, non-blocking) ----",
        "    always @(posedge clk or negedge rst_n)",
        "        if (!rst_n) state <= S0;",
        "        else        state <= next;",
        "",
        "    // ---- BLOCK 2 : next-state logic  (combinational, blocking) ----",
        "    always @(*) begin",
        "        next = state;                       // default: no latch",
        "        case (state)",
        "            S0: next = x ? S1 : S0;",
        "            S1: next = x ? S1 : S2;",
        "            S2: next = x ? S3 : S0;",
        "            S3: next = x ? S4 : S2;",
        "            S4: next = x ? S1 : S2;",
        "            default: next = S0;             // safe FSM: recover from illegal states",
        "        endcase",
        "    end",
        "",
        "    // ---- BLOCK 3 : output logic  (Moore - state only) ----",
        "    always @(*) z = (state == S4);",
        "",
        "endmodule",
    ], size=7.0, title="The three-always-block template — use this shape for EVERY FSM you write",
        accent=GREEN)
    d.card(s, y + G, "Why three blocks and not one",
           [[R("It separates the clocked element from the combinational logic, so the synthesised "
               "hardware matches the Huffman model exactly. It makes the reset behaviour explicit, keeps "
               "each block short enough to read, and makes latch inference impossible if you keep the "
               "default assignment. "),
             R("One-block FSMs are legal and much harder to debug.", b=True, c=NAVY)]],
           accent=TEAL, h=1005840)

    # ================================================================ Moore/Mealy trace
    s = d.slide("TOPIC 3C · PRACTICAL EXAMPLE 6", "Trace: Moore and Mealy on the Same Input Stream", GREEN)
    y = d.image(s, TOP, "fsm_1011_timing", 3383280)
    y = d.card(s, y + 91440, "Read the trace with the class, cycle by cycle",
               [[R("Input X = 1 0 1 1 0 1 1 0. Both machines see the fourth bit complete the pattern.")],
                [R("Mealy ", b=True, c=RED),
                 R("asserts Z during cycle 4 — combinationally, the moment X goes high while the state "
                   "is S3.   "),
                 R("Moore ", b=True, c=GREEN),
                 R("asserts Z during cycle 5 — the clock edge at the end of cycle 4 moved the register "
                   "into S4, and only then does Z = Q₂ become 1.")],
                [R("Second detection: overlapping means the '11' at the end is reused, so the pattern "
                   "completes again on bit 7 and both machines fire a second time.", i=True, c=SLATE)],
                [R("Exam question you should be able to answer instantly: ", b=True, c=NAVY),
                 R("'same behaviour, so why choose one?' — Mealy is one cycle faster and needs fewer "
                   "states; Moore is glitch-free and trivially timeable.")]],
               accent=GREEN, fill=CARD_G, h=1600200)

    # ================================================================ FSM pitfalls
    s = d.slide("TOPIC 3C · PITFALLS", "Five Ways an FSM Goes Wrong in Silicon", RED)
    y = d.table(s, TOP, ["Failure", "What happens", "How you prevent it"],
                [["Unreachable / illegal states",
                  "With 5 states in 3 bits, codes 101–111 exist in hardware but not in your diagram. "
                  "A glitch or radiation event lands you there.",
                  "Write a `default` branch that returns to a safe state — a SAFE FSM."],
                 ["Deadlock / lock-up",
                  "A group of states with no path back to normal operation. The block hangs and only a "
                  "reset recovers it.",
                  "Prove reachability: from every state, a path to the start state must exist."],
                 ["Incomplete transitions",
                  "A state with no arc for some input value. In RTL this becomes an inferred latch.",
                  "Assign `next` a default value at the top of the always block."],
                 ["Unregistered Mealy output",
                  "The glitchy combinational output drives a clock enable or a memory write. Random "
                  "corruption.",
                  "Register the output, or use Moore."],
                 ["Asynchronous input straight into the FSM",
                  "A button or a signal from another clock domain violates setup/hold and the FSM enters "
                  "an illegal state.",
                  "Two-flop synchroniser on EVERY asynchronous input."]],
                [3017520, 4297680, 3931920], rh=594360, bold_cols=(0,),
                col_colors={0: RED}, size=9.5)
    d.card(s, y + G, "The one-line summary",
           [[R("A state machine is only as reliable as its handling of the cases you did NOT draw. "
               "Always write the default branch, always synchronise the inputs, always simulate an "
               "illegal-state injection.", b=True, c=NAVY)]],
           accent=RED, fill=CARD_R, h=868680)

    # ================================================================ verilog sequential
    s = d.slide("TOPIC 3C · IN VERILOG", "Sequential Logic — Blocking vs Non-Blocking", RED)
    y = d.lead(s, TOP, [[
        R("This is the single most common Verilog error in the industry. ", b=True, c=NAVY, s=12.5),
        R("Both versions below simulate; only one synthesises to what you meant, and simulation and "
          "hardware then disagree — the worst class of bug there is.")]], h=502920)
    y = d.code(s, y + G, [
        "// CORRECT - non-blocking (<=) in a clocked block gives a true 2-stage shift register",
        "always @(posedge clk) begin",
        "    q1 <= d;",
        "    q2 <= q1;          // q2 gets the OLD q1  ->  two flip-flops in series",
        "end",
        "",
        "// WRONG - blocking (=) makes q1 update immediately, so q2 gets the NEW q1",
        "always @(posedge clk) begin",
        "    q1 = d;",
        "    q2 = q1;           // q2 gets d  ->  ONE flip-flop, and a race in simulation",
        "end",
    ], size=10, title="Same intent, different hardware", accent=RED)
    d.cols(s, y + G, [
        ("The rule — no exceptions",
         [[R("Non-blocking  <=  in every  always @(posedge clk)  block.", s=10.5, b=True, c=GREEN)],
          [R("Blocking  =  in every  always @(*)  block.", s=10.5, b=True, c=GREEN)],
          [R("Never mix the two in one block. Never assign the same signal from two blocks.",
             s=10.5, b=True, c=RED)]], GREEN, CARD_G),
        ("Why the rule exists",
         [[R("Non-blocking assignments all sample their right-hand sides first, then update together at "
             "the end of the time step — which is exactly what a bank of flip-flops does on a clock "
             "edge.", s=10.5)],
          [R("Blocking assignments execute in order, like software, which models a wire, not a register.",
             s=10.5)]], TEAL, CARD)], h=1417320)

    # ================================================================ FSMD
    s = d.slide("TOPIC 3C · SYNTHESIS OF IDEAS", "Controller Plus Datapath — How Real Blocks Are Built")
    y = d.lead(s, TOP, [[
        R("Everything in this topic now assembles into one architecture. ", b=True, c=NAVY, s=12.5),
        R("The combinational blocks from 3b form the datapath; the FSM from 3c forms the controller; "
          "control signals go one way and status flags come back. This partition is how every "
          "non-trivial digital block is organised.")]], h=548640)
    y = d.image(s, y + 45720, "fsmd", 3383280)
    d.card(s, y + 91440, "A concrete example you can build in one afternoon",
           [[R("A serial multiplier. ", b=True, c=NAVY),
             R("Datapath: a shift register for the multiplier, an adder, an accumulator register, a "
               "counter. Controller: an FSM with states IDLE → LOAD → ADD/SHIFT (looping) → DONE, "
               "using the counter's 'terminal count' status flag to decide when to leave the loop and "
               "driving the datapath's load, add and shift enables.")]],
           accent=TEAL, h=960120)
