# -*- coding: utf-8 -*-
"""Workbook Part 3: sequential logic, flip-flops, registers, state machines."""
from wbkit import *
from wb_part1 import B, N, I, M


def build(w):
    w.h1("Part 3 · Sequential Logic, Flip-Flops, Registers and State Machines")
    w.para([N("Sequential logic is where TIME enters the design. Everything here follows from one "
              "structural change: a feedback path through a clocked storage element.")])

    # ---------------------------------------------------------- 3.1
    w.h2("3.1  The clock")
    w.image("clock_anatomy", 6.5, "Figure 3.1 — period, frequency, duty cycle, edges")
    w.table(["Quantity", "Definition", "Example"],
            [["Period T", "seconds per cycle", "2 ns"],
             ["Frequency f", "f = 1 / T", "500 MHz"],
             ["t_high", "time the clock spends high", "1 ns"],
             ["Duty cycle", "t_high / T, usually 50 %", "50 %"],
             ["Rising edge", "0 → 1 transition (posedge)", "the sampling instant"],
             ["Falling edge", "1 → 0 transition (negedge)", "rarely used for sampling"]],
            [1.3, 3.2, 2.0], bold_cols=(0,), size=9, align_center=False)
    w.para([B("Conversions to have at your fingertips: "),
            N("T = 10 ns → 100 MHz.  T = 2 ns → 500 MHz.  T = 400 ps → 2.5 GHz.  "
              "f = 3.2 GHz → T = 312.5 ps.")])
    w.callout("Two rules that are never broken in RTL",
              [N("1.  Never generate a clock in combinational logic. A glitch on a clock line is "
                 "fatal, and a gated clock breaks static timing analysis. Use a clock ENABLE on "
                 "the flip-flop instead — the tool will insert a proper integrated clock gate if "
                 "power demands it."),
               N("2.  Never mix posedge and negedge of the same clock without a documented reason. "
                 "You halve every timing budget and confuse every tool in the flow.")],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 3.2
    w.h2("3.2  Latches — the first memory")
    w.image("sr_latch", 6.5, "Figure 3.2 — cross-coupled NOR gates remember one bit")
    w.h3("The SR latch")
    w.para([N("Two NOR gates, each feeding the other's input. The loop has two stable "
              "configurations, and it stays in whichever one you last pushed it into.")])
    w.table(["S", "R", "Q⁺", "Meaning"],
            [["0", "0", "Q", "HOLD — remembers the previous value"],
             ["0", "1", "0", "RESET to 0"],
             ["1", "0", "1", "SET to 1"],
             ["1", "1", "—", "FORBIDDEN"]],
            [0.6, 0.6, 0.9, 3.5], bold_cols=(2,), align_center=False)
    w.para([B("Why S = R = 1 is forbidden. "),
            N("Both NOR outputs are forced to 0, so Q and Q' are no longer complements — the "
              "latch's whole invariant is violated. Worse, if both inputs are released at the same "
              "instant the loop settles unpredictably: the two gates race, and which one wins "
              "depends on picosecond-level manufacturing variation.")])
    w.para([B("A NAND version "), N("exists with active-low inputs (S̄R̄); its forbidden "
              "combination is 0,0. The NAND version with a pull-up on each input is the standard "
              "hardware de-bouncer for a mechanical switch.")])

    w.h3("Gated SR and D latches")
    w.para([N("Add an enable: gate S and R with EN so the latch only responds while EN is high. "
              "Then tie R = S' and you have a D latch — one data input, no forbidden state. "
              "The D latch is TRANSPARENT while EN is high: its output tracks D continuously.")])

    # ---------------------------------------------------------- 3.3
    w.h2("3.3  Latch versus flip-flop — the distinction that matters most")
    w.image("latch_vs_ff", 6.5, "Figure 3.3 — level-sensitive versus edge-triggered")
    w.table(["", "Latch", "Flip-flop"],
            [["Sensitive to", "the LEVEL of its enable", "the EDGE of its clock"],
             ["Transparent", "whenever EN is asserted", "never"],
             ["Output changes", "possibly many times per cycle", "exactly once per clock edge"],
             ["Area", "smaller (~half)", "larger — two latches inside"],
             ["Timing analysis", "hard — time borrowing, transparency windows",
              "straightforward — one equation per path"],
             ["Use it when", "almost never in RTL; deliberately in some custom design",
              "always"]],
            [1.4, 2.6, 2.8], bold_cols=(0,), size=9, align_center=False)

    w.h3("How edge-triggering is built")
    w.image("master_slave", 6.5, "Figure 3.4 — the master–slave D flip-flop")
    w.para([N("Two D latches in series on OPPOSITE clock phases. While clk = 0 the master is "
              "transparent and tracks D, and the slave holds the old Q. When clk rises the master "
              "freezes and the slave opens, copying whatever the master had captured. Because the "
              "two are never transparent simultaneously, data can never race through both in one "
              "phase — and that, precisely, is what 'edge-triggered' means.")])
    w.para([B("This also explains the timing parameters. "),
            N("Setup time is how long the master latch needs to capture reliably; hold time is how "
              "long the input must persist before the master actually closes; clock-to-Q is the "
              "delay through the slave. They are not arbitrary datasheet numbers — they are "
              "properties of this structure.")])

    # ---------------------------------------------------------- 3.4
    w.h2("3.4  The flip-flop family")
    w.image("ff_family", 6.5, "Figure 3.5 — D, T, JK and SR")
    w.h3("Characteristic equations")
    w.table(["Type", "Characteristic equation", "Behaviour"],
            [["D", "Q⁺ = D", "copy the input"],
             ["T", "Q⁺ = T ⊕ Q", "toggle when T = 1, hold when T = 0"],
             ["JK", "Q⁺ = J·Q' + K'·Q", "set / reset / hold / toggle — no forbidden state"],
             ["SR", "Q⁺ = S + R'·Q  (SR ≠ 11)", "set / reset / hold; 11 forbidden"]],
            [0.7, 2.2, 3.6], bold_cols=(0,), size=9, align_center=False)
    w.h3("Excitation table — the table you use to DESIGN")
    w.para([N("A characteristic table answers 'given the inputs, what is the next state?'. An "
              "EXCITATION table answers the reverse: 'to make this transition happen, what inputs "
              "do I need?'. You analyse with the first and design with the second.")])
    w.table(["Q → Q⁺", "D", "T", "J   K", "S   R"],
            [["0 → 0", "0", "0", "0   ×", "0   ×"],
             ["0 → 1", "1", "1", "1   ×", "1   0"],
             ["1 → 0", "0", "1", "×   1", "0   1"],
             ["1 → 1", "1", "0", "×   0", "×   0"]],
            [1.1, 0.7, 0.7, 1.3, 1.3], bold_cols=(0,))
    w.para([N("The × entries are don't-cares, and they are exactly why JK-based designs minimise "
              "so well on paper — every don't-care is a free K-map grouping opportunity.")])
    w.h3("Converting one flip-flop to another")
    w.numbered([
        N("Write the excitation table of the flip-flop you HAVE, beside the characteristic table "
          "of the one you WANT."),
        N("K-map the required inputs of the available flip-flop as functions of (present state, "
          "desired inputs)."),
        N("Add that logic in front."),
        [B("Two you should just remember: "), M("D = T ⊕ Q"), N("  (D-FF used as a T-FF) and "),
         M("T = D ⊕ Q"), N("  (T-FF used as a D-FF).")],
    ])
    w.callout("Why the D flip-flop won",
              ["It has no forbidden state, no toggle surprise, and its next state IS its input — "
               "so synthesis can map any next-state equation directly onto it with no conversion "
               "logic. Standard-cell libraries therefore contain dozens of D flip-flop variants "
               "(with and without reset, set, enable, scan) and no JK at all. If you need a T or "
               "JK, build it from a D plus a couple of gates."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 3.5
    w.h2("3.5  Reset")
    w.para([N("At power-up every flip-flop holds an unknown value. Reset forces the design into a "
              "known starting state. Choosing the wrong style, or releasing reset carelessly, "
              "produces bugs that appear only on real silicon.")])
    w.code([
        "// ASYNCHRONOUS reset - reset is in the sensitivity list",
        "always @(posedge clk or negedge rst_n)",
        "    if (!rst_n) q <= 1'b0;",
        "    else        q <= d;",
        "",
        "// SYNCHRONOUS reset - reset is just another input to the D logic",
        "always @(posedge clk)",
        "    if (!rst_n) q <= 1'b0;",
        "    else        q <= d;",
    ], "The two templates — memorise both exactly")
    w.table(["", "Asynchronous", "Synchronous"],
            [["Takes effect", "immediately, clock or no clock", "only on a clock edge"],
             ["At power-up", "works before the PLL has locked", "useless — there is no clock yet"],
             ["Timing analysis", "needs recovery / removal checks", "ordinary setup / hold"],
             ["Glitch on the reset line", "propagates straight into the design",
              "filtered — only sampled at the edge"],
             ["Area", "usually free (the cell has the pin)",
              "adds a gate in the data path"]],
            [1.5, 2.7, 2.6], bold_cols=(0,), size=9, align_center=False)
    w.callout("What industry actually does: the reset synchroniser",
              [N("Assert asynchronously, DE-assert synchronously. Two flip-flops clocked by the "
                 "destination clock, with their asynchronous reset pins tied to the raw reset. "
                 "The output is a reset that asserts the instant the raw signal drops (so it works "
                 "with no clock) but releases cleanly on a clock edge (so no flip-flop can violate "
                 "its recovery time)."),
               [B("Recovery and removal "), N("are setup and hold for the reset pin: recovery is "
                 "how long before the clock edge the reset must be de-asserted; removal is how "
                 "long after. A raw asynchronous release violates both.")],
               [B("On FPGAs "), N("a global reset costs routing and is often unnecessary, because "
                 "the bitstream initialises every flip-flop. On an ASIC it is mandatory.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 3.6
    w.h2("3.6  Timing: setup, hold and clock-to-Q")
    w.image("ff_timing", 6.5, "Figure 3.6 — the three parameters from the datasheet")
    w.table(["Parameter", "Meaning", "Violated when"],
            [["t_setup", "D must be stable this long BEFORE the edge",
              "the data path is too SLOW"],
             ["t_hold", "D must stay stable this long AFTER the edge",
              "the data path is too FAST"],
             ["t_cq", "delay from the edge until Q is valid", "— (a cost, not a constraint)"]],
            [1.1, 3.3, 2.2], bold_cols=(0,), size=9, align_center=False)

    w.h3("The timing path")
    w.image("fmax_path", 6.5, "Figure 3.7 — launch flip-flop, logic, capture flip-flop")
    w.callout("The two checks",
              [[B("SETUP (max delay):   "),
                M("T_clk ≥ t_cq + t_logic,max + t_setup + t_jitter − t_skew")],
               [B("HOLD  (min delay):   "),
                M("t_cq + t_logic,min ≥ t_hold + t_skew")],
               N("Setup sets your maximum frequency. Hold is a RACE and is frequency-independent — "
                 "a hold violation is broken at DC and cannot be fixed by slowing the clock. "
                 "You fix hold by ADDING delay (buffers) to the short path.")],
              color=NAVY, bar="0E2A47")
    w.para([B("Slack "), N("= available time − required time. Positive slack means the requirement "
              "is met with margin; negative slack is a violation, and the number tells you by how "
              "much. Timing signoff is 'no negative slack on any path'.")])

    w.h3("Worked timing calculation")
    w.para([N("Given t_cq = 60 ps, t_setup = 50 ps, t_hold = 40 ps, skew = 25 ps (capture clock "
              "arrives LATE), jitter = 15 ps, t_logic,max = 240 ps, t_logic,min = 30 ps, and a "
              "target of 2.0 GHz:")])
    w.code([
        "SETUP",
        "  T_req = t_cq + t_logic,max + t_setup + t_jitter - t_skew",
        "        = 60  + 240          + 50      + 15       - 25",
        "        = 340 ps        ->  f_max = 1/340 ps = 2.94 GHz",
        "  Target 2.0 GHz means T_target = 500 ps",
        "  SETUP SLACK = 500 - 340 = +160 ps        PASS",
        "",
        "HOLD",
        "  Required:  t_cq + t_logic,min  >=  t_hold + t_skew",
        "             60   + 30           >=  40     + 25",
        "             90                  >=  65",
        "  HOLD SLACK = 90 - 65 = +25 ps            PASS",
    ], "Do setup and hold as two separate calculations, never together")
    w.callout("The sign of skew — the classic exam mistake",
              ["A LATE capture clock gives the data path more time, so it HELPS setup. But it also "
               "means the capture flip-flop samples later, giving the next launch more chance to "
               "corrupt it, so it HURTS hold. That is why t_skew appears with opposite signs in "
               "the two inequalities. Get the sign wrong and both answers are wrong."],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- 3.7
    w.h2("3.7  Metastability and clock-domain crossing")
    w.image("metastability", 6.5, "Figure 3.8 — the failure, and the standard fix")
    w.para([N("If data changes inside the setup/hold window, the flip-flop may enter a METASTABLE "
              "state: its output hovers at an invalid intermediate voltage, then resolves to 0 or "
              "1 at random after an unbounded time. It cannot be prevented — only made "
              "astronomically unlikely.")])
    w.callout(None,
              [[B("MTBF  =  e^(t_r / τ)  /  (T₀ · f_clk · f_data)")],
               N("t_r is the resolution time you allow (usually one clock period); τ and T₀ are "
                 "library constants; f_clk and f_data are the clock and data-change rates.")],
              color=NAVY, bar="0E2A47")
    w.para([N("Because t_r sits inside an exponential, adding ONE more synchroniser flip-flop "
              "typically moves MTBF from seconds to millions of years. That is why two stages is "
              "the universal minimum, and three are used for very high-speed or safety-critical "
              "crossings.")])
    w.callout("The rule you must never break",
              [N("Every signal entering your clock domain from outside it — another clock domain, "
                 "a push-button, a sensor, an off-chip pin — MUST pass through a synchroniser "
                 "first."),
               [B("For a BUS you cannot just synchronise each bit. "),
                N("Different bits will resolve on different cycles and you will read a value that "
                  "never existed. Use a Gray-coded pointer (only one bit changes per step), or a "
                  "handshake, or an asynchronous FIFO.")],
               N("CDC bugs are the leading cause of silicon respins, precisely because they are "
                 "intermittent and pass every simulation.")],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 3.8
    w.h2("3.8  Clock skew and jitter")
    w.image("clock_skew", 6.5, "Figure 3.9 — two ways the heartbeat goes wrong")
    w.bullets([
        [B("Skew "), N("— a FIXED difference in edge arrival time between flip-flops, caused by "
                       "unequal clock-tree path lengths and loads. Fixed by clock-tree synthesis "
                       "(CTS), which inserts buffers to balance every branch to within tens of "
                       "picoseconds.")],
        [B("Jitter "), N("— a RANDOM cycle-to-cycle variation in edge arrival, caused by PLL "
                         "noise, supply droop, crosstalk and temperature. It cannot be designed "
                         "out; it is budgeted as clock uncertainty in the SDC constraints and "
                         "paid for out of every clock period.")],
        [B("Useful skew "), N("— deliberately delaying a capture clock to borrow time for a slow "
                              "path from the following stage. Powerful, and dangerous: it "
                              "tightens the hold check on that same path.")],
    ])

    # ---------------------------------------------------------- 3.9
    w.h2("3.9  Registers and shift registers")
    w.image("shift_registers", 6.5, "Figure 3.10 — n flip-flops sharing one clock")
    w.para([N("A register is simply n flip-flops on one clock. Wire each Q to the next D and you "
              "have a shift register.")])
    w.table(["Mode", "Name", "Behaviour"],
            [["SISO", "serial in, serial out", "1 bit in, 1 bit out; n cycles to traverse"],
             ["SIPO", "serial in, parallel out", "shift in bit by bit, read all n at once"],
             ["PISO", "parallel in, serial out", "load all n at once, shift out bit by bit"],
             ["PIPO", "parallel in, parallel out", "load and read in one edge — a plain register"]],
            [0.8, 1.9, 3.7], bold_cols=(0,), size=9, align_center=False)
    w.h3("Where they are actually used")
    w.bullets([
        [B("Serialisation "), N("— SPI, UART, JTAG: PISO on the transmitter, SIPO on the receiver.")],
        [B("Delay lines "), N("— pipeline balancing, so two datapaths arrive at the same stage.")],
        [B("Synchronisers "), N("— a 2-bit shift register IS the standard 2-flop synchroniser.")],
        [B("Scan chains "), N("— during manufacturing test every flip-flop on the chip is rewired "
                              "into one giant shift register, so test patterns can be loaded and "
                              "results read out serially. This is how a chip is tested at all.")],
        [B("LFSRs "), N("— add an XOR feedback tap and you get a pseudo-random sequence generator "
                        "or a CRC engine. An n-bit maximal LFSR cycles through 2ⁿ−1 states (all "
                        "except all-zeros) in a scrambled order.")],
    ])

    # ---------------------------------------------------------- 3.10
    w.h2("3.10  Counters")
    w.image("counters", 6.5, "Figure 3.11 — ripple versus synchronous")
    w.para([B("Ripple (asynchronous): "),
            N("each flip-flop is clocked by the previous stage's output. Simple and small — and "
              "each stage adds one t_cq of skew, so an n-bit ripple counter can read out a WRONG "
              "value for up to n·t_cq after every edge. It also creates a second clock domain out "
              "of a data signal, which breaks static timing analysis entirely.")])
    w.para([B("Synchronous: "),
            N("every flip-flop shares one clock; AND gates decide which bits toggle. All bits "
              "change together. This is the only kind you should ever synthesise.")])
    w.h3("Varieties")
    w.bullets(["Up / down / up-down; loadable; with enable.",
               "Mod-N — divide by N, wrapping at N−1. A mod-10 counter is a BCD counter.",
               "Ring counter — a one-hot shift register; N states from N flip-flops; self-starting "
               "only if you force a legal state.",
               "Johnson (twisted-ring) counter — feed back the INVERTED last bit; 2N states from "
               "N flip-flops, and only one bit changes per step.",
               "LFSR — 2ⁿ−1 states, maximal length, extremely cheap, but not in numeric order."])
    w.h3("Worked design: mod-10 (BCD) up-counter")
    w.image("mod10_design", 6.5, "Figure 3.12 — state table, gate equations, and the RTL")
    w.numbered([
        N("Write the state table: 0000 … 1001, then wrap to 0000."),
        N("For each bit, tabulate Qᵢ → Qᵢ⁺."),
        N("Since D = Q⁺ for a D flip-flop, the D column IS the next-state column."),
        N("K-map each Dᵢ over Q₃Q₂Q₁Q₀, treating states 1010–1111 as don't-cares."),
        N("Read off the minimal SOP."),
    ])
    w.code(["D0 = Q0'",
            "D1 = Q1 XOR (Q0 . Q3')",
            "D2 = Q2 XOR (Q1 . Q0)",
            "D3 = Q3 XOR (Q3.Q0 + Q2.Q1.Q0)"], "The four next-state equations")
    w.para([B("Check one row by hand. "),
            N("At count 9 (Q = 1001): D0 = Q0' = 0. D1 = Q1 ⊕ (Q0·Q3') = 0 ⊕ (1·0) = 0. "
              "D2 = Q2 ⊕ (Q1·Q0) = 0 ⊕ 0 = 0. D3 = Q3 ⊕ (Q3Q0 + Q2Q1Q0) = 1 ⊕ (1+0) = 0. "
              "Next state 0000. Correct.")])
    w.callout("The trap: unreachable states are not impossible states",
              ["States 1010–1111 are unreachable in normal operation, but a glitch, a "
               "single-event upset or a marginal reset can land the counter in one of them. "
               "Because we treated them as don't-cares, the tool may have mapped them anywhere — "
               "including into a loop the counter can never leave.",
               [B("A SAFE counter "), N("forces any illegal state explicitly back to 0000. In RTL "
                 "that is a "), M("default"), N(" branch, exactly as in a safe FSM.")]],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 3.11
    w.h2("3.11  Finite state machines")
    w.para([N("An FSM is the formal name for a circuit that remembers where it is in a sequence. "
              "Formally it is a six-tuple (S, S₀, X, Y, δ, λ): a finite set of states, a start "
              "state, an input alphabet, an output alphabet, a next-state function δ, and an "
              "output function λ.")])
    w.h3("The three pieces of hardware")
    w.numbered([
        N("STATE REGISTER — n flip-flops holding the present state."),
        N("NEXT-STATE LOGIC — combinational; computes δ(present state, inputs)."),
        N("OUTPUT LOGIC — combinational; computes λ."),
    ])
    w.para([N("Drawn with the state register in a feedback loop, this is the HUFFMAN MODEL of a "
              "sequential circuit. Every sequential circuit, however complicated, reduces to it.")])
    w.h3("What counts as a 'state'")
    w.para([N("A state is an equivalence class of input HISTORIES: two histories are the same "
              "state if the machine will behave identically from now on. This is why a '1011' "
              "detector needs five states and not thirty-two — you only have to remember how much "
              "of the pattern currently matches, not what you actually received.")])
    w.para([B("What FSMs cannot do. "),
            N("Finite states means finite memory, so an FSM cannot count arbitrarily high or match "
              "arbitrarily deep nesting. For that you add a datapath — a counter, a stack — "
              "alongside it, which is the FSMD idea in §3.14.")])

    w.h3("Moore versus Mealy")
    w.image("moore_mealy", 6.5, "Figure 3.13 — where the output logic gets its inputs")
    w.table(["", "Moore", "Mealy"],
            [["Output is", "λ(state)", "λ(state, input)"],
             ["Output changes", "only just after a clock edge", "the moment the input does"],
             ["Glitches", "none — comes straight off flip-flops", "possible — combinational"],
             ["State count", "usually more", "usually fewer"],
             ["Reaction time", "one cycle later", "same cycle"],
             ["Drawn on the diagram", "output written INSIDE the state bubble",
              "output written ON the transition arc"]],
            [1.5, 2.5, 2.8], bold_cols=(0,), size=9, align_center=False)
    w.callout("Which should you use?",
              ["Default to Moore. Its outputs come straight off flip-flops, so they are glitch-free "
               "and trivially timeable. Use Mealy when you genuinely need the one-cycle-earlier "
               "response — and then REGISTER the Mealy output before it leaves the block, which "
               "of course turns it back into a Moore output one cycle later. That is not a "
               "contradiction; it is the point."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 3.12
    w.h2("3.12  The FSM design procedure")
    w.image("fsm_procedure", 6.4, "Figure 3.14 — six steps, in this order")
    w.numbered([
        N("Draw the state diagram — one bubble per thing the machine must remember."),
        N("Write the state table — present state + input → next state + output."),
        N("Minimise states (optional; merge equivalent states)."),
        N("Assign an encoding — binary, Gray or one-hot."),
        N("Derive the next-state and output equations, one per state bit."),
        N("Implement and verify."),
    ])
    w.callout("Two checks to run on the diagram BEFORE writing any code",
              [[B("Completeness: "), N("from every state, is there exactly one outgoing arc for "
                 "EVERY possible input value? A missing arc is an undefined transition — in "
                 "hardware, an inferred latch or a lock-up. For s states and one binary input "
                 "there must be exactly 2s arcs; count them.")],
               [B("Determinism: "), N("is there AT MOST one arc per input value? Two arcs labelled "
                 "'1' leaving one state is not a circuit, it is a contradiction.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    w.h3("State encoding")
    w.image("state_encoding", 6.5, "Figure 3.15 — three encodings, three silicon costs")
    w.table(["Encoding", "Flip-flops for n states", "Next-state logic", "Best for"],
            [["Binary", "⌈log₂ n⌉ — fewest", "most complex", "large FSMs on an ASIC"],
             ["Gray", "⌈log₂ n⌉", "similar to binary",
              "low power; crossing clock domains"],
             ["One-hot", "n — most", "trivial, one level deep", "FPGAs; speed-critical FSMs"]],
            [1.1, 1.9, 1.8, 2.0], bold_cols=(0,), size=9, align_center=False)
    w.para([B("In Verilog: "), N("declare state names with "), M("localparam"),
            N(" (or an enum in SystemVerilog) and let the tool choose the encoding — then CHECK "
              "the synthesis report to see what it actually chose.")])

    # ---------------------------------------------------------- 3.13
    w.h2("3.13  Worked FSM: the '1011' sequence detector")
    w.para([B("Specification. "), N("A serial input X arrives one bit per clock. Assert Z whenever "
              "the last four bits received were 1, 0, 1, 1. Overlapping sequences count, so the "
              "stream 1011011 contains TWO occurrences.")])
    w.h3("Step 1 — the state diagram")
    w.image("fsm_1011", 6.5, "Figure 3.16 — the Moore machine, five states")
    w.para([B("How the states were chosen. "),
            N("Ask: 'what is the longest PREFIX of 1011 that is currently a SUFFIX of what I have "
              "received?' That question has exactly five answers — none, 1, 10, 101, 1011 — so "
              "there are five states, and the answer to the question IS the state. This "
              "suffix-matching insight generalises to any pattern detector.")])
    w.h3("Step 2 — the state table")
    w.table(["Present state", "Encoding Q₂Q₁Q₀", "Next (X=0)", "Next (X=1)", "Z"],
            [["S0  (start)", "000", "S0  000", "S1  001", "0"],
             ["S1  (seen 1)", "001", "S2  010", "S1  001", "0"],
             ["S2  (seen 10)", "010", "S0  000", "S3  011", "0"],
             ["S3  (seen 101)", "011", "S2  010", "S4  100", "0"],
             ["S4  (seen 1011)", "100", "S2  010", "S1  001", "1"]],
            [1.6, 1.3, 1.2, 1.2, 0.5], bold_cols=(0, 4), size=9, align_center=False)
    w.h3("Steps 4–5 — encoding and equations")
    w.code([
        "K-map each D bit over Q2 Q1 Q0 X, treating codes 101/110/111 as don't-cares:",
        "",
        "  D2 = Q1 . Q0 . X                     only S3 (011) with X=1 reaches S4",
        "  D1 = X' . (Q2 + Q0)  +  Q1 . Q0' . X",
        "  D0 = X . (Q1 . Q0)'",
        "",
        "  Z  = Q2                              S4 is the only code with Q2 = 1",
    ], "Derived next-state and output equations")
    w.para([B("Always re-check row by row. "),
            N("S3 = 011 with X = 1: D₂ = 1·1·1 = 1; D₁ = 0·(…) + 1·0·1 = 0; D₀ = 1·(1·1)' = 0. "
              "Next state 100 = S4. Correct. Note that Z = Q₂ fell out for free because the "
              "encoding was chosen well — a different assignment would have needed real output "
              "logic.")])
    w.h3("Step 6 — the RTL")
    w.code([
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
        "        next = state;                    // default: no inferred latch",
        "        case (state)",
        "            S0: next = x ? S1 : S0;",
        "            S1: next = x ? S1 : S2;",
        "            S2: next = x ? S3 : S0;",
        "            S3: next = x ? S4 : S2;",
        "            S4: next = x ? S1 : S2;      // overlapping: reuse the suffix",
        "            default: next = S0;          // SAFE FSM",
        "        endcase",
        "    end",
        "",
        "    // ---- BLOCK 3 : output logic  (Moore - state only) ----",
        "    always @(*) z = (state == S4);",
        "",
        "endmodule",
    ], "The three-always-block template — use this shape for EVERY FSM")
    w.para([B("Why three blocks and not one. "),
            N("It separates the clocked element from the combinational logic, so the synthesised "
              "hardware matches the Huffman model exactly. It makes the reset behaviour explicit, "
              "keeps each block short enough to read, and makes latch inference impossible so long "
              "as you keep the default assignment. One-block FSMs are legal and much harder to "
              "debug.")])

    w.h3("Moore versus Mealy on the same stream")
    w.image("fsm_1011_timing", 6.5, "Figure 3.17 — Moore asserts one cycle after Mealy")
    w.para([N("Both machines see the fourth bit complete the pattern. Mealy asserts Z DURING that "
              "cycle, combinationally, the moment X goes high while the state is S3. Moore asserts "
              "Z in the NEXT cycle, once the clock edge has actually moved the register into S4. "
              "Overlapping means the trailing '11' is reused, so the pattern completes again on "
              "bit 7 and both machines fire a second time.")])

    w.h3("Five ways an FSM goes wrong in silicon")
    w.table(["Failure", "What happens", "Prevention"],
            [["Unreachable / illegal states",
              "5 states in 3 bits leaves codes 101–111 existing in hardware but not in your "
              "diagram; a glitch or SEU lands you there",
              "a `default` branch that returns to a safe state"],
             ["Deadlock / lock-up",
              "a group of states with no path back to normal operation; only a reset recovers",
              "prove reachability — from every state a path to S0 must exist"],
             ["Incomplete transitions",
              "a state with no arc for some input; in RTL this becomes an inferred latch",
              "assign `next` a default value at the top of the block"],
             ["Unregistered Mealy output",
              "a glitchy combinational output drives a clock enable or a memory write",
              "register the output, or use Moore"],
             ["Asynchronous input into the FSM",
              "a button or another clock domain violates setup/hold and the FSM enters an "
              "illegal state",
              "two-flop synchroniser on EVERY asynchronous input"]],
            [1.6, 3.0, 2.2], bold_cols=(0,), size=8.5, align_center=False)

    # ---------------------------------------------------------- 3.14
    w.h2("3.14  Sequential logic in Verilog: blocking versus non-blocking")
    w.para([N("This is the single most common Verilog error in the industry. Both versions below "
              "simulate; only one synthesises to what you meant, and simulation and hardware then "
              "disagree — the worst class of bug there is.")])
    w.code([
        "// CORRECT - non-blocking (<=) gives a true two-stage shift register",
        "always @(posedge clk) begin",
        "    q1 <= d;",
        "    q2 <= q1;        // q2 gets the OLD q1  ->  two flip-flops in series",
        "end",
        "",
        "// WRONG - blocking (=) makes q1 update immediately",
        "always @(posedge clk) begin",
        "    q1 = d;",
        "    q2 = q1;         // q2 gets d  ->  ONE flip-flop, and a race in simulation",
        "end",
    ], "Same intent, different hardware")
    w.callout("The rule — no exceptions",
              [[B("Non-blocking "), M("<="), N("  in every "), M("always @(posedge clk)"),
                N(" block.")],
               [B("Blocking "), M("="), N("  in every "), M("always @(*)"), N(" block.")],
               N("Never mix the two in one block. Never assign the same signal from two blocks."),
               [B("Why the rule exists: "),
                N("non-blocking assignments all sample their right-hand sides first and then update "
                  "together at the end of the time step — which is exactly what a bank of "
                  "flip-flops does on a clock edge. Blocking assignments execute in order, like "
                  "software, which models a wire, not a register.")]],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- 3.15
    w.h2("3.15  Controller plus datapath — the FSMD view")
    w.image("fsmd", 6.5, "Figure 3.18 — how every non-trivial block is organised")
    w.para([N("The combinational blocks from Part 2 form the DATAPATH; the FSM from Part 3 forms "
              "the CONTROLLER. Control signals (load, shift, select, enable) go one way; status "
              "flags (zero, negative, done, terminal count) come back. The controller decides "
              "WHEN; the datapath decides WHAT.")])
    w.h3("A concrete example you can build in an afternoon")
    w.para([B("A serial (shift-and-add) multiplier.")])
    w.bullets([
        [B("Datapath: "), N("a shift register holding the multiplier, an adder, an accumulator "
                            "register, and a counter for the loop.")],
        [B("Controller: "), N("an FSM with states IDLE → LOAD → ADD/SHIFT (looping) → DONE.")],
        [B("The interface: "), N("the FSM asserts load, add_en and shift_en; the counter asserts "
                                 "a 'terminal count' status flag that tells the FSM when to leave "
                                 "the loop.")],
    ])
    w.para([I("Every processor, DMA engine, UART, SPI controller and memory controller you will "
              "ever write has exactly this shape.")])
    w.page_break()
