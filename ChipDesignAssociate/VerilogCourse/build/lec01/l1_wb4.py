# -*- coding: utf-8 -*-
"""Lecture 01 workbook — Part 5: exercises, solutions, reference."""
import _boot
from wbkit import *

# (question, solution) — kept together so they cannot drift apart
CONCEPT = [
 ("Name the five levels of the design flow, in order, from a design idea down "
  "to a finished chip.",
  "Behavioral design, data path design (register transfer level), logic "
  "design, physical design, manufacturing. The lecturer draws them as a "
  "ladder with \"design idea\" above the first and \"chip / board\" below the "
  "last."),
 ("What are the input and the output of a CAD tool, and how do they differ?",
  "Both are hardware descriptions written in an HDL. The output contains more "
  "detailed information about the hardware than the input. Nothing is "
  "compiled into a program; the design is simply re-described in more "
  "concrete terms."),
 ("Define a netlist.",
  "A directed graph whose vertices are components and whose edges are the "
  "interconnections between them. The whole graph is the design."),
 ("Why is a netlist represented as a graph rather than as a drawing?",
  "Because a graph is a data structure a program can hold in memory and "
  "transform. Every CAD step after synthesis — optimisation, technology "
  "mapping, placement, routing — is an operation on that graph."),
 ("What does \"register transfer\" refer to?",
  "That on each clock edge, values are transferred between registers, "
  "possibly passing through some combinational logic on the way. The name "
  "describes what the level models."),
 ("Give four ways of specifying the behaviour of a circuit.",
  "A Boolean expression; a truth table; a finite-state machine, as a state "
  "transition diagram or table; and a high-level algorithm written much as "
  "you would write C."),
 ("What do all four of those have in common?",
  "None of them says how the circuit is BUILT — only what it must DO. That is "
  "what makes them behavioural, and it is why a synthesis tool is free to "
  "build them in whichever way is cheapest under your constraints."),
 ("Why is a netlist also called a structural description?",
  "Because it names the parts and says how they are wired together, rather "
  "than describing the result. The lecturer states the equivalence "
  "explicitly: a netlist specification is also referred to as structural "
  "design."),
 ("State synthesis in one sentence, using the words behavioural and "
  "structural.",
  "You write behavioural Verilog; the tool emits structural Verilog."),
 ("What is a standard cell?",
  "A pre-designed circuit module — a gate, a flip-flop, a small multiplexer — "
  "held in a library as a symbol to place, a truth table to simulate, a "
  "timing model, and a finished piece of layout."),
 ("Why does a standard cell library exist at all?",
  "Laying out even a NAND gate correctly takes a skilled engineer a long "
  "time. Doing it once, perfectly, and reusing it a million times is the only "
  "way a billion-transistor design is economically possible."),
 ("Name three logic-optimisation goals that conflict with one another.",
  "Minimise the number of gates (area); minimise the number of gate levels "
  "(delay); minimise signal transition activity (dynamic power). Improving "
  "one usually makes at least one of the others worse."),
 ("State Moore's Law. Is it a law of physics?",
  "That the number of transistors on a chip doubles roughly every two years. "
  "It is not a law of physics: it was an observation about what the industry "
  "had been doing, and it kept holding largely because it became a planning "
  "target for the whole supply chain."),
 ("Why are the shapes in a layout all regular polygons, mostly rectangles?",
  "Because they are printed photographically, layer by layer, onto a silicon "
  "wafer. Regular shapes expose cleanly and etch predictably; awkward ones do "
  "not."),
 ("Give one advantage of an FPGA over an ASIC, and one the other way round.",
  "An FPGA can be programmed in your own laboratory in minutes and "
  "reprogrammed afterwards, with no mask costs. An ASIC is faster, smaller "
  "and far cheaper per unit at volume, because its logic is built from "
  "dedicated transistors rather than configurable ones."),
 ("Name three steps of the design flow that are not rungs of the ladder.",
  "Simulation for verification; formal verification; testability analysis and "
  "test pattern generation."),
 ("Why does the flow contain a verification step at every level rather than "
  "only one at the end?",
  "Because each level is produced from the one above it by a different tool, "
  "and a mistake is far cheaper to find at the step that made it than three "
  "steps later. It is also why fabrication, which is statistical rather than "
  "exact, needs test patterns of its own."),
 ("What is the difference between combinational and sequential logic?",
  "Combinational logic has no memory: its outputs depend only on its present "
  "inputs. Sequential logic has memory, held in registers and updated on a "
  "clock edge, so its outputs depend also on what happened before."),
]

HDL = [
 ("Why is Verilog not a programming language, even though it looks like one?",
  "Because its statements are not events in time. They are a description of "
  "hardware that exists all at once and stays there. Three assign statements "
  "describe three wires, all permanently driven; reordering them changes "
  "nothing."),
 ("What happens if you swap two assign statements in a Verilog module, and "
  "why?",
  "Nothing. Each assign describes a piece of wire that exists permanently, so "
  "there is no \"first\" and no \"next\" — only what is connected to what."),
 ("Name two HDLs other than Verilog and VHDL, and say what each is for.",
  "SystemVerilog, a large superset of Verilog adding classes, constrained "
  "random stimulus and assertions, aimed mostly at verification. SystemC, a "
  "C++ class library used to model whole systems before the hardware is "
  "written."),
 ("Will a synthesis tool produce different gates from a VHDL description than "
  "from an equivalent Verilog one?",
  "No. Both describe the same hardware, and the tool produces the same gates "
  "from either. The choice is a matter of house style, existing code and "
  "local convention."),
 ("What is a test bench, and why may it use constructs that are not "
  "synthesisable?",
  "A piece of HDL whose job is to drive a design with stimulus and check what "
  "comes out. It is never turned into hardware, so delays, loops and $display "
  "are all legitimate in it."),
 ("A test bench has no ports. Why not?",
  "Because nothing drives it and nothing reads it — it sits at the top of the "
  "hierarchy and instantiates the design under test inside itself."),
]

LAB = [
 ("Run  make sim  and then  make wave  . In the waveform, what is the value of "
  "q before the first clock edge, and why?",
  "xxxx — unknown. A Verilog reg holds x until something drives it, and the "
  "first rising edge (at 5 ns, with rst still high) is what clears it. A real "
  "flip-flop likewise powers up in an unpredictable state, which is why every "
  "design has a reset."),
 ("In the waveform, does q change at the clock edge or just after it?",
  "Just after. The delay is the flip-flop's clock-to-Q time, and it is the "
  "first thing that eats into the available clock period."),
 ("Run  make transform  . How many of the three printed descriptions are "
  "Verilog?",
  "All three. That is the point of the exercise: the tool re-described the "
  "design twice, each time in more detail, and never left the language."),
 ("Run  make ladder  . How many cells does the counter have at RTL, and what "
  "are they?",
  "Two: one $add and one $sdff. That is literally \"an adder and a register\", "
  "which is what data path design means."),
 ("One $sdff at RTL became four $_SDFF_PP0_ at gate level. Explain.",
  "At RTL a register is a single component that happens to be four bits wide. "
  "At gate level each bit is its own flip-flop. The vocabulary changed, not "
  "the circuit."),
 ("Change the counter to 8 bits. Re-run  make ladder  . Did the gate count "
  "double?",
  "No — it more than doubled. The 4-bit version is 10 cells (4 flip-flops and "
  "6 gates); the 8-bit version is 22 cells (8 flip-flops and 14 gates). The "
  "flip-flops scale exactly with width, but the carry chain that computes "
  "\"plus one\" grows faster, because each higher bit must test more of the "
  "lower bits."),
 ("Make the reset asynchronous —  always @(posedge clk or posedge rst)  — and "
  "compare the gate netlists. What changed?",
  "The total is still 10 cells, and the combinational logic is unchanged. "
  "What changed is the flip-flop: $_SDFF_PP0_ (synchronous reset) became "
  "$_DFF_PP0_ (asynchronous reset). The reset moved out of the logic and into "
  "the flip-flop itself."),
 ("Write a down-counter that loads 15 on reset, and compare it with the up "
  "counter.",
  "Also 10 cells, but a different mix: 4 flip-flops, 1 NOT, 2 OR and 3 XNOR, "
  "against the up counter's 1 AND, 1 NAND, 1 NOT, 1 XNOR and 2 XOR. The "
  "flip-flop is $_SDFF_PP1_ — one that resets to 1 rather than 0 — because "
  "the reset value is now 4'd15. Counting down costs the same as counting "
  "up."),
 ("Try  abc -lut 6  instead of  abc -lut 4  . Why do larger look-up tables "
  "not help here?",
  "The count stays at 8 cells — 4 flip-flops and 4 LUTs. Each next-state bit "
  "of a 4-bit counter already depends on at most four inputs, so a 4-input "
  "LUT is big enough. Making the LUTs larger cannot reduce a count that is "
  "already one LUT per bit."),
 ("Map the 8-bit counter for an FPGA. Is it bigger or smaller than the ASIC "
  "mapping?",
  "Smaller in cell count: 18 cells (8 flip-flops and 10 LUTs) against 22 for "
  "the gate mapping. Cell count is not area, though — a LUT is a small memory "
  "and occupies far more silicon than the gate it imitates, which is exactly "
  "the flexibility-for-speed trade."),
 ("Open out/counter4_behav.vcd and out/counter4_gates.vcd in GTKWave together "
  "and align them. What do you expect to see?",
  "Identical traces. make prove already compared them mechanically and "
  "reported 22 transitions at the same values and the same times; looking at "
  "them is the human confirmation of the same fact."),
 ("Run  make langs  . Where do the Verilog and VHDL runs differ, and why?",
  "Only at time zero. The Verilog reg reads xxxx until the reset edge clears "
  "it; the VHDL signal was declared with an initial value and so reads 0000 "
  "from the start. From the end of reset onwards the two are identical for "
  "all 20 transitions."),
]

APPLY = [
 ("A colleague says \"synthesis compiles Verilog into gates, like gcc "
  "compiles C into machine code\". What is wrong with the analogy?",
  "gcc produces something in a different kind of language — instructions for "
  "a processor to execute in sequence. Synthesis produces another hardware "
  "description, in the same language, of a thing that exists all at once. "
  "Nothing is ever executed."),
 ("Your design meets its area budget but misses its clock target. Name two "
  "things you could change, and what each would cost.",
  "Add pipeline registers, which shortens the longest logic path but costs "
  "area and adds latency. Or let the tool duplicate logic so parts run in "
  "parallel, which costs area and switching power. Both trade area or power "
  "for speed, as the triangle predicts."),
 ("You are asked to build 200 units of a product with a tight deadline and a "
  "modest budget. ASIC or FPGA? Justify it.",
  "FPGA. Mask costs dominate at low volume and would never be recovered over "
  "200 units, and the turnaround is minutes rather than months. You accept "
  "lower clock speed and higher unit cost in exchange."),
 ("Why can two synthesis runs of the same Verilog produce different cell "
  "counts?",
  "Because there is no single best answer. The tool searches for a solution "
  "satisfying the constraints it was given, and different constraints, "
  "different versions or different optimisation effort will land on different "
  "points of the area/speed/power trade."),
 ("You read in a datasheet that a chip is built on a \"3 nm\" process. What "
  "does the number mean?",
  "Essentially nothing dimensional. Node names are now marketing labels: no "
  "feature on a \"3 nm\" chip measures 3 nm. They indicate a generation, not a "
  "measurement — useful for comparing roadmap steps, not for computing "
  "anything."),
 ("If Moore's Law is slowing, why does the design flow in this lecture still "
  "apply?",
  "Because the flow is about managing complexity, not about transistor size. "
  "Chiplets, 3-D stacking and specialised accelerators all still need a "
  "behavioural description turned into a netlist and then into layout, with "
  "verification at each level."),
 ("Where in the flow does the course you are taking stop, and why?",
  "At logic design. Physical design, manufacturing and test are real and "
  "essential but are somebody else's job — and in practice the tools'. A "
  "Verilog designer's deliverable is a netlist."),
 ("Someone shows you a Verilog file full of named gate instances and asks "
  "whether it is behavioural or structural. How do you answer?",
  "Structural. It names the parts and wires them together rather than "
  "describing the result, which is exactly what a netlist is — and a netlist "
  "written as text is a structural description."),
]

GROUPS = [("Concept questions", CONCEPT, TEAL),
          ("The language", HDL, VIOLET),
          ("From the labs", LAB, GREEN),
          ("Applying it", APPLY, AMBER)]


def build_exercises(w):
    w.h1("Part 5 · Exercises")

    n = sum(len(g[1]) for g in GROUPS)
    w.para([("There are %d exercises below, in four groups. Worked solutions "
             "to every one of them begin on the next page — try each question "
             "before you look." % n, {})])

    w.callout("The ones that matter most", [
        "If you are short of time, do the concept questions on the netlist "
        "(3, 4, 8 and 9) and the whole of the lab group. Those are the ideas "
        "the rest of Module 2 is built on.",
    ], color=NAVY)

    k = 1
    for head, items, col in GROUPS:
        w.h2(head)
        for q, _ in items:
            w.para([("%d.  " % k, {"b": True, "c": col}), (q, {})],
                   indent=0.12, space_after=8)
            k += 1

    w.page_break()


def build_solutions(w):
    w.h1("Part 5 · Solutions")

    w.para("Each solution is numbered to match the exercise. Where a solution "
           "quotes a number, that number was measured by running the command, "
           "not estimated.")

    k = 1
    for head, items, col in GROUPS:
        w.h2(head)
        for q, a in items:
            w.para([("%d.  " % k, {"b": True, "c": col}),
                    (q, {"i": True, "c": SLATE})],
                   indent=0.12, space_after=3)
            w.para([(a, {})], indent=0.34, space_after=10)
            k += 1

    w.page_break()


def build_reference(w):
    w.h1("Part 6 · Reference")

    w.h2("6.1  The flow at a glance")
    w.table(["Level", "A component is…", "Produced by", "Checked by"],
            [["Behavioral", "a statement", "a human", "simulation"],
             ["Data path (RTL)", "register, adder, mux", "synthesis",
              "simulation, equivalence"],
             ["Logic", "gate or flip-flop", "technology mapping",
              "simulation, static timing"],
             ["Physical", "a placed cell", "place and route",
              "timing, DRC, LVS"],
             ["Manufacturing", "a polygon", "the foundry", "wafer test"]],
            widths=[1.3, 1.8, 1.7, 1.9], size=9.5, align_center=False)

    w.h2("6.2  Commands used in this workbook")
    w.table(["Command", "What it does"],
            [["iverilog -g2012 -o out/x.vvp a.v b.v",
              "compile Verilog into a simulation"],
             ["vvp out/x.vvp", "run that simulation"],
             ["gtkwave out/x.vcd", "view the waveform it recorded"],
             ["yosys -s script.ys", "run a synthesis script"],
             ["ghdl -a --workdir=out/ghdl x.vhd", "analyse VHDL"],
             ["ghdl -r --workdir=out/ghdl tb --vcd=out/x.vcd",
              "elaborate and run it"],
             ["make sim", "Lab 1"],
             ["make transform / make prove", "Lab 2"],
             ["make ladder", "Lab 3"],
             ["make target", "Lab 4"],
             ["make langs", "Lab 5"],
             ["make clean", "delete everything under out/"]],
            widths=[3.4, 3.3], size=9.5, align_center=False)

    w.h2("6.3  Yosys commands used in the scripts")
    w.table(["Command", "What it does"],
            [["read_verilog f.v", "parse a Verilog file"],
             ["hierarchy -top m", "pick the top module, resolve the hierarchy"],
             ["proc", "turn always blocks into registers and logic"],
             ["opt", "general optimisation"],
             ["techmap", "map internal operators onto simple cells"],
             ["abc -g AND,OR,XOR,…", "map logic onto a given set of gates"],
             ["abc -lut 4", "map logic onto 4-input look-up tables"],
             ["opt_clean", "remove unused cells and wires"],
             ["write_verilog -noattr f.v", "write the netlist back out as "
              "Verilog"],
             ["stat", "print how many cells the design now has"]],
            widths=[2.7, 4.0], size=9.5, align_center=False)

    w.callout("Reading a Yosys statistics block", [
        "Yosys prints statistics every time the stat command runs, and a "
        "script may run it more than once. Only the LAST block describes the "
        "finished netlist — which is why scripts/stat.sh extracts just that "
        "one.",
    ], color=AMBER, bar="C77514", fill="FFF7EC")

    w.h2("6.4  Glossary")
    terms = [
        ("ASIC", "Application-Specific Integrated Circuit — a chip "
         "manufactured for one design."),
        ("Behavioural description", "A description of what a circuit does, "
         "saying nothing about which parts build it."),
        ("CAD tool", "A program that reads a hardware description and writes a "
         "more detailed one."),
        ("Cell", "One component of a netlist: at gate level, a gate or a "
         "flip-flop."),
        ("Clock-to-Q", "The delay between a clock edge arriving at a flip-flop "
         "and its output changing."),
        ("Combinational logic", "Logic whose outputs depend only on its "
         "present inputs."),
        ("Design flow", "The standardized sequence of steps from a "
         "specification to a manufactured chip."),
        ("FPGA", "Field Programmable Gate Array — a manufactured chip full of "
         "configurable blocks you program yourself."),
        ("HDL", "Hardware Description Language. Verilog and VHDL are the two "
         "in common use."),
        ("LUT", "Look-Up Table — a small memory inside an FPGA that can "
         "compute any function of its inputs."),
        ("Netlist", "A directed graph whose vertices are components and whose "
         "edges are interconnections."),
        ("RTL", "Register Transfer Level — the level at which the components "
         "are registers, adders, multiplexers and buses."),
        ("Sequential logic", "Logic with memory, updated on a clock edge."),
        ("Standard cell", "A pre-designed module held in a library as symbol, "
         "behaviour, timing model and layout."),
        ("Structural description", "A description naming the parts and how "
         "they are wired. A netlist, written as text."),
        ("Synthesis", "The step that turns a behavioural description into a "
         "structural one."),
        ("Technology mapping", "Rewriting a netlist in terms of the cells a "
         "particular library or FPGA actually provides."),
        ("Test bench", "HDL that drives a design with stimulus and checks the "
         "result. Never synthesised."),
        ("VCD", "Value Change Dump — the file format a simulator writes so a "
         "waveform viewer can draw the result."),
    ]
    for t, d in terms:
        w.para([(t, {"b": True, "c": NAVY}), ("  —  ", {"c": SLATE}),
                (d, {})], indent=0.12, space_after=5)

    w.h2("6.5  Where to go next")
    w.para("Lecture 02, Design Representation, takes the idea this lecture "
           "left implicit — that the same design can be looked at from "
           "different angles — and makes it the subject. It arranges the "
           "behavioural, structural and physical views as the three arms of a "
           "Y-diagram, with the highest level of abstraction at the outside "
           "and the finished layout at the centre. Every design step is then a "
           "move along one arm, or a jump from one arm to another.")

    w.callout("Keep the lab directory", [
        "Everything from Lecture 02 onwards builds on the same toolchain. The "
        "counter, the test bench and the Makefile in Lecture01_Lab are a "
        "working template you can copy for any later design.",
    ], color=TEAL)
