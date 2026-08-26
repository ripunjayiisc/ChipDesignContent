# -*- coding: utf-8 -*-
"""Topic 4 deck — opening and 4A: Verilog syntax and constructs."""
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
        "TOPIC 4",
        "RTL Design Using HDL",
        "Subtopic 4a: Verilog syntax and constructs  ·  4b: Designing combinational and "
        "sequential logic using HDL  ·  4c: Writing RTL code for basic digital circuits",
        ["4a · The language — modules, types, literals, operators, and the synthesisable subset",
         "4b · Modelling logic — assign, always @(*), always @(posedge clk), and what each infers",
         "4c · Real circuits — MUXes, ALUs, counters, FSMs, memories, FIFOs and a working UART",
         "Tools · Vivado · ModelSim · Icarus + GTKWave + Verilator + Yosys  ·  Labs L1–L5"])

    # ================================================================ roadmap
    s = d.slide("TOPIC 4 · ROADMAP", "What This Topic Covers, and How Much Time It Really Needs")
    y = d.lead(s, TOP, [[
        R("Topic 3 gave you the hardware vocabulary. ", b=True, c=NAVY, s=12.5),
        R("Topic 4 is where you stop drawing gates and start writing them — and where the "
          "majority of this module's practical hours are spent. The syllabus lists 6 theory "
          "hours for this subtopic and ", s=12.5),
        R("40 hours of RTL Design and Implementation Labs", b=True, c=AMBER, s=12.5),
        R(" in the practical component. This deck is sized for that reality.", s=12.5)]],
        h=685800)

    y = d.table(s, y + G,
                ["Syllabus bullet — Topic 4", "Covered by", "Slides"],
                [["Introduction to Verilog syntax and constructs", "4a", "4–27"],
                 ["Designing combinational and sequential logic using HDL", "4b", "28–49"],
                 ["Writing RTL code for basic digital circuits", "4c", "50–65"],
                 ["Practical: simulating and verifying the functionality of RTL designs",
                  "Verification + Labs", "55–65, 75–79"],
                 ["Practical: designing and implementing digital circuits using HDL",
                  "Tools + Labs L1–L5", "66–79"]],
                [6217920, 3383280, 1645920], rh=329184, bold_cols=(1,))

    y = d.card(s, y + G, "Learning outcomes — by the end of this topic you can",
               [[R("· Read and write the synthesisable Verilog subset fluently, and say exactly "
                   "what hardware each construct becomes.")],
                [R("· Model combinational and sequential logic correctly — no accidental latches, "
                   "no blocking/non-blocking races.")],
                [R("· Write a self-checking testbench with a reference model, a scoreboard and "
                   "randomised stimulus.")],
                [R("· Take a real block — a UART, a FIFO, an FSM — from specification to verified, "
                   "synthesised netlist.")]],
               accent=GREEN, fill=CARD_G, h=1417320)
    d.card(s, 5486400, "How to run the session",
           [[R("Deliver 4a in one sitting — it is reference material and the room will not "
               "retain it all; the workbook carries the detail. Spend the real time on 4b and 4c, "
               "at the keyboard. Every design in this deck exists as verified, runnable code in "
               "Topic4_Lab/.")]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ================================================================ why HDL
    s = d.slide("TOPIC 4 · MOTIVATION", "Verilog Is Not a Programming Language")
    y = d.lead(s, TOP, [[
        R("This is the single most important idea in the topic, and the one that costs beginners "
          "the most time. ", b=True, c=NAVY, s=12.5),
        R("Verilog looks like C. It is not C. It DESCRIBES hardware that already exists and runs "
          "continuously and in parallel — it does not instruct a processor to do things in order.")]],
        h=594360)
    y = d.image(s, y + 45720, "hdl_vs_software", 3383280)
    d.card(s, y + 91440, "The habit that fixes almost everything",
           [[R("Before you write a line of Verilog, "),
             R("sketch the hardware you want", b=True, c=TEAL),
             R(" — the registers, the gates between them, what feeds what. Then write the code "
               "that describes that sketch. Designers who do this produce clean RTL from the "
               "start; designers who type first and hope produce latches, races and timing "
               "failures.")]],
           accent=TEAL, h=822960)

    # =============================================== SECTION 4A
    d.section_slide("SUBTOPIC 4A", "Verilog Syntax and Constructs",
                    "The language itself — and the narrow subset of it that becomes hardware.",
                    ["Modules, ports, and the four levels of abstraction",
                     "Values, nets and variables, literals, vectors",
                     "Operators, and the width rules that cause silent bugs",
                     "Procedural blocks, control flow, tasks, functions and generate",
                     "The synthesisable subset — and what is simulation-only"], accent=TEAL)

    # ================================================================ abstraction
    s = d.slide("TOPIC 4A · ABSTRACTION", "Four Levels of Description — Only Some Synthesise")
    y = d.lead(s, TOP, [[
        R("Verilog can describe hardware at four levels of detail. ", b=True, c=NAVY, s=12.5),
        R("All four are legal Verilog and all four simulate. Only the middle two are what you "
          "will write, and the synthesisable subset is a real, narrow boundary you must learn.")]],
        h=548640)
    y = d.image(s, y + 45720, "abstraction_levels", 3200400)
    d.card(s, y + 91440, "Why RTL is the level we work at",
           [[R("Register-transfer level describes WHAT happens to the data between clock edges, "
               "without saying which gates do it. That is abstract enough to be readable and "
               "portable between technologies, and concrete enough that the resulting hardware is "
               "predictable. Gate-level is what synthesis OUTPUTS; you should be able to read it, "
               "not write it.")]],
           accent=TEAL, h=1005840)

    # ================================================================ module
    s = d.slide("TOPIC 4A · THE MODULE", "Anatomy of a Verilog Module")
    y = d.lead(s, TOP, [[
        R("The module is the only unit of design in Verilog. ", b=True, c=NAVY, s=12.5),
        R("It is a box with a name, a set of ports, and a body. Everything you build in this "
          "topic is a box, or a box made of boxes.")]], h=502920)
    y = d.image(s, y + 45720, "module_anatomy", 3520440)
    d.cols(s, y + 91440, [
        ("Port directions",
         [[R("input", b=True, c=NAVY, s=10.5), R("  — read only inside the module.", s=10.5)],
          [R("output", b=True, c=GREEN, s=10.5), R("  — driven by exactly ONE source.", s=10.5)],
          [R("inout", b=True, c=AMBER, s=10.5), R("  — bidirectional; only on real chip pins.",
                                                  s=10.5)]], TEAL, CARD),
        ("Two port styles",
         [[R("ANSI (shown): direction, type and width all in the header. Use this.", s=10.5)],
          [R("Non-ANSI: bare names in the header, declared again in the body. You will meet it "
             "in older code; do not write new code that way.", s=10.5)]], AMBER, CARD_A)],
        h=1051560)

    # ================================================================ four values
    s = d.slide("TOPIC 4A · VALUES", "Signals Have Four Values, Not Two", RED)
    y = d.lead(s, TOP, [[
        R("Verilog's logic type has four states. ", b=True, c=NAVY, s=12.5),
        R("Two of them are hardware; two of them are things the SIMULATOR needs to say. "
          "Confusing the two categories is the root of a great deal of wasted debugging time.")]],
        h=502920)
    y = d.image(s, y + 45720, "four_value_logic", 3383280)
    d.card(s, y + 91440, "Where an x comes from — the five usual suspects",
           [[R("1. A register that was never reset.   2. A wire nothing drives.   "
               "3. A wire TWO things drive (a multi-driver).")],
            [R("4. Reading past the end of a vector or an array.   "
               "5. Arithmetic on a value that is already x — x is contagious, which is why you "
               "must chase it back to the FIRST signal that turned x, not the one you noticed.")]],
           accent=RED, fill=CARD_R, h=960120)

    # ================================================================ nets vs vars
    s = d.slide("TOPIC 4A · TYPES", "wire or reg? The Rule Is About How You Assign")
    y = d.lead(s, TOP, [[
        R("This is a naming accident that has confused students since 1985. ", b=True, c=NAVY,
          s=12.5),
        R("A "), R("reg", b=True, c=AMBER, f=MONO_FONT), R(" is NOT a register. It is a variable "
          "in the simulator. Whether it becomes a flip-flop depends entirely on HOW you assign "
          "it, and not at all on what you called it.")]], h=594360)
    y = d.image(s, y + 45720, "nets_vs_variables", 3200400)
    y = d.table(s, y + 91440,
                ["You want", "Declare it", "Assign it with"],
                [["A wire between two things", "wire", "assign, or a port connection"],
                 ["Combinational logic in a block", "reg", "= inside always @(*)"],
                 ["A flip-flop", "reg", "<= inside always @(posedge clk)"],
                 ["A module output driven by assign", "wire (the default)", "assign"],
                 ["A module output driven by a block", "reg", "inside the always block"]],
                [3657600, 3200400, 4389120], rh=283464, bold_cols=(1,), size=10)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("SystemVerilog fixes this with ", s=10.5), R("logic", b=True, c=GREEN, f=MONO_FONT, s=10.5),
        R(", which can be assigned either way. If your tools allow SystemVerilog, use it — "
          "but you must still be able to read Verilog-2001, because most existing IP is written "
          "in it.", s=10.5)]])

    # ================================================================ literals
    s = d.slide("TOPIC 4A · LITERALS", "Reading and Writing Number Literals")
    y = d.lead(s, TOP, [[
        R("Every constant in Verilog has a WIDTH as well as a value. ", b=True, c=NAVY, s=12.5),
        R("Leaving the width off does not mean 'whatever fits' — it means 32 bits, signed. That "
          "default is responsible for a whole family of silent bugs.")]], h=502920)
    y = d.image(s, y + 45720, "literals", 3566160)
    d.card(s, y + 91440, "The house rule",
           [[R("Size every literal. ", b=True, c=RED),
             R("Write "), R("8'd0", f=MONO_FONT, b=True, c=NAVY), R(" not "),
             R("0", f=MONO_FONT, b=True, c=NAVY), R(";  "),
             R("4'b0000", f=MONO_FONT, b=True, c=NAVY), R(" or "),
             R("{W{1'b0}}", f=MONO_FONT, b=True, c=NAVY),
             R(" not a bare zero. It costs three keystrokes and removes an entire class of bug.")]],
           accent=RED, fill=CARD_R, h=776224)

    # ================================================================ vectors
    s = d.slide("TOPIC 4A · VECTORS", "Slicing, Concatenating and Replicating")
    y = d.lead(s, TOP, [[
        R("Almost every signal in real RTL is a vector — a bus. ", b=True, c=NAVY, s=12.5),
        R("These four operations are how you take buses apart and put them back together, and "
          "you will use them constantly.")]], h=502920)
    y = d.image(s, y + 45720, "vector_ops", 2834640)
    d.cols(s, y + 91440, [
        ("Arrays are NOT vectors",
         [[R("reg [7:0] v;", s=10, f=MONO_FONT), R("  one 8-bit vector", s=10)],
          [R("reg v [0:7];", s=10, f=MONO_FONT), R("  eight 1-bit elements", s=10)],
          [R("reg [7:0] m [0:255];", s=10, f=MONO_FONT), R("  256 bytes — a memory", s=10)],
          [R("You can slice a vector; you index an array.", s=10, b=True, c=NAVY)]], TEAL, CARD),
        ("Indexed part-select",
         [[R("A plain slice needs constant bounds:  ", s=10.5),
           R("d[i:j]", f=MONO_FONT, b=True, c=RED, s=10.5), R("  is illegal for variable i.",
                                                              s=10.5)],
          [R("Use ", s=10.5), R("d[i +: 4]", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  (4 bits UP from i) or ", s=10.5),
           R("d[i -: 4]", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R(" (4 bits DOWN). The WIDTH is constant; only the position varies — which is exactly "
             "what a multiplexer can do.", s=10.5)]], GREEN, CARD_G)], h=1371600)

    # ================================================================ operators
    s = d.slide("TOPIC 4A · OPERATORS", "The Operators You Will Actually Use")
    y = d.image(s, TOP, "operator_map", 3840480)
    y = d.cols(s, y + 91440, [
        ("Logical vs bitwise — a classic slip",
         [[R("a && b", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R("  treats each side as true/false and gives ONE bit.", s=10.5)],
          [R("a & b", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R("  operates bit by bit and gives a VECTOR.", s=10.5)],
          [R("For 4'b0011 and 4'b1100: && gives 1, & gives 0000.", s=10.5, i=True, c=SLATE)]],
         AMBER, CARD_A),
        ("Reduction operators are underused",
         [[R("|req", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("  — is ANY bit set? (a valid flag)",
                                                              s=10.5)],
          [R("&full", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("  — are ALL bits set?", s=10.5)],
          [R("^data", f=MONO_FONT, b=True, c=GREEN, s=10.5), R("  — parity, in one character.",
                                                               s=10.5)],
          [R("~|result", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R("  — is the result zero? That is the ALU's Z flag.", s=10.5)]], GREEN, CARD_G)],
        h=1188720)

    # ================================================================ width rules
    s = d.slide("TOPIC 4A · WIDTH RULES", "Where Silent Bugs Come From", RED)
    y = d.lead(s, TOP, [[
        R("Verilog will not warn you when a value does not fit. ", b=True, c=NAVY, s=12.5),
        R("It truncates, silently, and the simulation and the hardware agree with each other — "
          "and both are wrong. This is the most common cause of 'it worked yesterday'.")]],
        h=548640)
    y = d.image(s, y + 45720, "width_rules", 3017520)
    d.card(s, y + 91440, "This is not hypothetical — it happened while writing this lab",
           [[R("The UART in Topic4_Lab originally wrote its bit-timing limit as "),
             R("CLKS_PER_BIT[CW-1:0]", f=MONO_FONT, b=True, c=RED),
             R(". With CLKS_PER_BIT = 16, CW is 4 — and 16 does not fit in 4 bits, so it "
               "truncated to ZERO.")],
            [R("The receiver stopped waiting half a bit before sampling, began sampling on bit "
               "boundaries instead of bit centres, and corrupted "),
             R("some", i=True), R(" byte patterns but not others. 0x00 passed; 0xFF came back as "
               "0xF7. See the UART lab for the full story.")]],
           accent=RED, fill=CARD_R, h=1188720)
