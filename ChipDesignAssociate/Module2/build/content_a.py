# -*- coding: utf-8 -*-
"""Topic 3 deck — opening section and 3A: Boolean algebra and logic gates."""
from deckkit import *

G = 91440          # standard vertical gap


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def build(d):
    # ================================================================ 1 title
    d.title_slide(
        "TOPIC 3",
        "Digital Logic Design Principles",
        "Subtopic 3a: Boolean algebra and logic gates  ·  3b: Combinational logic design  ·  "
        "3c: Sequential logic — flip-flops, registers and state machines",
        ["3a · Binary, Boolean algebra, the seven gates, De Morgan, SOP/POS, K-map minimisation",
         "3b · Design procedure, adders, MUX, decoders, ALU, hazards, delay and fan-out",
         "3c · Latches, flip-flops, timing, metastability, registers, counters, FSMs",
         "Tools · Logisim-Evolution, Icarus Verilog, GTKWave, Yosys  ·  Tutorials T1–T4"])

    # ================================================================ 2 roadmap
    s = d.slide("TOPIC 3 · ROADMAP", "What This Topic Covers and How the 4 Hours Are Spent")
    y = d.lead(s, TOP, [[
        R("Where this sits. ", b=True, c=NAVY, s=12.5),
        R("Topic 2 gave you the RTL methodology — the idea that we describe hardware, not program it. "
          "Topic 3 gives you the ", s=12.5),
        R("hardware vocabulary itself", b=True, c=TEAL, s=12.5),
        R(". Every Verilog construct you write in Topic 4 maps onto one of the structures in this topic. "
          "Without this, RTL coding is guesswork.", s=12.5)]], h=640080)

    y = d.table(s, y + G,
                ["Syllabus bullet (NIE/ELE/N0102, Topic 3 — 4 hours)", "Covered by", "Time"],
                [["Boolean algebra and logic gates", "3a — slides 4–18", "1 h 15 m"],
                 ["Combinational logic design concepts", "3b — slides 19–32", "1 h 15 m"],
                 ["Sequential logic design concepts", "3c — slides 33–45", "45 m"],
                 ["Flip-flops, registers and state machines", "3c — slides 33–59", "45 m"],
                 ["Hands-on tools and tutorials T1–T4", "slides 60–66 + workbook", "lab time"]],
                [6400800, 3200400, 1645920], rh=329184, bold_cols=(1,))

    y = d.card(s, y + G, "Learning outcomes — by the end of this topic you can",
               [[R("· Simplify any Boolean function algebraically and with a Karnaugh map, "
                   "and justify why the minimal form matters in silicon.")],
                [R("· Design, analyse and hand-verify adders, multiplexers, decoders, comparators and an ALU.")],
                [R("· Explain latches vs flip-flops, compute fₘₐₓ from a timing path, and "
                   "recognise setup/hold and metastability failures.")],
                [R("· Design a finite state machine end to end — state diagram → table → encoding → "
                   "logic → Verilog → simulation → synthesis.")]],
               accent=GREEN, fill=CARD_G, h=1371600)

    d.card(s, 5312664, "How to run the session",
           [[R("Deliver 3a and 3b before the break, with a 10-minute Logisim demo after each; "
               "run 3c after the break and finish in the lab with tutorials T1–T4.")],
            [R("The six worked numerical examples are your checkpoints — if the room cannot follow "
               "one, slow down rather than skipping ahead.")]],
           accent=AMBER, fill=CARD_A, h=1051560)

    # ================================================================ 3 why
    s = d.slide("TOPIC 3 · MOTIVATION", "Why a Verilog Engineer Still Needs Gate-Level Thinking")
    y = d.lead(s, TOP, [[
        R("A synthesiser turns your Verilog into gates — so why learn gates at all? ", b=True, c=NAVY, s=12.5),
        R("Because the tool optimises what you WROTE, not what you MEANT. Every one of the following is a "
          "real, common bug that is invisible at the Verilog level and obvious at the logic level.", s=12.5)]],
        h=548640)
    y = d.cols(s, y + G, [
        ("You write", [[R("an ", s=10.5)], [R("incomplete if/else", b=True, c=RED, s=11)],
                       [R("in a combinational block", s=10.5)]], SLATE, CARD),
        ("Tool infers", [[R("a ", s=10.5)], [R("transparent LATCH", b=True, c=RED, s=11)],
                         [R("instead of pure gates", s=10.5)]], RED, CARD_R),
        ("Consequence", [[R("timing cannot be", s=10.5)], [R("closed; chip fails", b=True, c=RED, s=11)],
                         [R("intermittently", s=10.5)]], RED, CARD_R),
        ("You needed to know", [[R("what a latch IS", b=True, c=GREEN, s=11)],
                                [R("and why level-", s=10.5)], [R("sensitivity is deadly", s=10.5)]],
         GREEN, CARD_G)], h=1600200)

    y = d.card(s, y + G, "Three more examples of the same pattern",
               [[R("Async reset written as sync → ", b=True, c=NAVY),
                 R("the design never leaves an unknown state after power-up. You needed flip-flop reset behaviour.")],
                [R("A signal crossed from another clock → ", b=True, c=NAVY),
                 R("random one-in-a-million failures. You needed metastability.")],
                [R("A 32-bit ripple adder in a 1 GHz design → ", b=True, c=NAVY),
                 R("timing fails by 4 ns. You needed carry propagation delay.")]],
               accent=AMBER, fill=CARD_A, h=1417320)
    d.text(s, ML, y + 137160, MW, 320040, [[
        R("The rule for this whole module: ", b=True, c=TEAL, s=11.5),
        R("you must be able to picture the hardware your code will become — BEFORE you run synthesis.",
          s=11.5, c=NAVY, b=True)]])

    # =============================================== SECTION 3A divider
    d.section_slide("SUBTOPIC 3A", "Boolean Algebra and Logic Gates",
                    "The mathematics of 0 and 1 — and the physical devices that implement it.",
                    ["Binary, the digital abstraction, number systems and codes",
                     "The seven gates, universal gates, and De Morgan's theorems",
                     "Boolean axioms, laws and theorems — with proofs you can do on paper",
                     "Canonical forms (SOP / POS) and Karnaugh-map minimisation"], accent=TEAL)

    # ================================================================ digital abstraction
    s = d.slide("TOPIC 3A · FOUNDATION", "Why Digital? The Two-Valued Abstraction")
    y = d.lead(s, TOP, [[
        R("A digital circuit is an analog circuit that we have agreed to misread. ", b=True, c=NAVY, s=12.5),
        R("The wire really does carry a continuous voltage. We simply declare two bands — anything below "),
        R("Vᴵʟ", b=True, c=GREEN), R(" counts as 0, anything above "),
        R("Vᴵʜ", b=True, c=TEAL),
        R(" counts as 1 — and design so a signal never rests in between. That single decision buys us noise "
          "immunity, testability, and the ability to reason with algebra instead of calculus.")]], h=685800)
    y = d.image(s, y + 45720, "digital_abstraction", 3383280)
    d.card(s, y + 91440, "Terms you must be able to define",
           [[R("Bit ", b=True, c=NAVY), R("— one binary digit.   "),
             R("Logic level ", b=True, c=NAVY), R("— the 0/1 interpretation of a voltage.   "),
             R("Noise margin ", b=True, c=NAVY),
             R("— how much interference a signal can absorb and still be read correctly (NMᴸ = Vᴵʟ − Vᴼʟ, "
               "NMᴴ = Vᴼʜ − Vᴵʜ).   "),
             R("Restoring logic ", b=True, c=NAVY),
             R("— every gate outputs a clean full-swing level, so noise never accumulates.")]],
           accent=TEAL, h=1005840)

    # ================================================================ number systems
    s = d.slide("TOPIC 3A · REPRESENTATION", "Number Systems and Codes You Will Meet in RTL")
    y = d.lead(s, TOP, [[
        R("Hardware only stores bits. ", b=True, c=NAVY, s=12.5),
        R("What those bits MEAN is a convention you choose and must apply consistently — the same "
          "8 bits are 180 unsigned, −76 signed, 0xB4 in hex, or a BCD digit pair. Verilog will happily "
          "let you mix them up; the bug appears in silicon.")]], h=548640)
    y = d.image(s, y + 45720, "number_systems", 2971800)
    y = d.cols(s, y + 45720, [
        ("Gray code", [[R("Successive values differ in exactly ONE bit.", s=10)],
                       [R("Used for K-maps, FIFO pointers crossing clock domains, "
                          "and shaft encoders — because a multi-bit change can be sampled mid-flight.", s=10)]],
         AMBER, CARD_A),
        ("BCD", [[R("Each decimal digit in its own 4-bit nibble.", s=10)],
                 [R("Wastes 6 of 16 codes but makes decimal display and financial arithmetic exact. "
                    "The mod-10 counter you build later is a BCD counter.", s=10)]], TEAL, CARD),
        ("Two's complement", [[R("The universal signed format.", s=10)],
                              [R("One adder handles + and −; there is only one zero. In Verilog, declare "
                                 "`signed` or the tool assumes unsigned and your comparisons invert.", s=10)]],
         GREEN, CARD_G)], h=1508760)

    # ================================================================ boolean basics
    s = d.slide("TOPIC 3A · THE ALGEBRA", "Boolean Variables, Operators and Truth Tables")
    y = d.lead(s, TOP, [[
        R("Boolean algebra (George Boole, 1854; applied to switching circuits by Claude Shannon, 1937) "),
        R("is an algebra over exactly two values. ", b=True, c=NAVY),
        R("A variable is 0 or 1. There are three primitive operators, and every digital circuit that has "
          "ever been built is a composition of these three.")]], h=502920)
    y = d.table(s, y + G,
                ["Operator", "Symbols used", "Reads as", "Result is 1 when…"],
                [["AND", "A · B    A ∧ B    AB    A & B", "conjunction", "BOTH inputs are 1"],
                 ["OR", "A + B    A ∨ B    A | B", "disjunction", "AT LEAST ONE input is 1"],
                 ["NOT", "A'    Ā    ¬A    ~A", "complement / negation", "the input is 0"]],
                [1371600, 3657600, 2560320, 3657600], rh=365760, bold_cols=(0,),
                col_colors={0: TEAL})
    y = d.card(s, y + G, "The truth table — the ground truth of every combinational function",
               [[R("A truth table lists the output for every possible input combination. "
                   "For n inputs there are "),
                 R("2ⁿ rows", b=True, c=AMBER),
                 R(" — 2 inputs → 4 rows, 4 inputs → 16 rows, 16 inputs → 65 536 rows. This exponential "
                   "growth is exactly why we need algebra and K-maps rather than exhaustive tables.")],
                [R("Two circuits are ", ),
                 R("functionally equivalent", b=True, c=NAVY),
                 R(" if and only if their truth tables match on every row — no matter how differently they "
                   "are drawn. Equivalence checking (a signoff step in Topic 6) automates exactly this.")]],
               accent=TEAL, h=1508760)
    d.text(s, ML, y + 182880, MW, 274320, [[
        R("Precedence: ", b=True, c=NAVY, s=11),
        R("NOT binds tightest, then AND, then OR — so A + B·C means A + (B·C). "
          "When in doubt, bracket it. Verilog follows the same order.", s=11)]])
