# -*- coding: utf-8 -*-
"""Lecture 01 deck — Theory 3 (the flow) and Theory 4 (the steps)."""
import _boot
from deckkit import *
from l1_deck_a import R, card_from
import l1_flow
import l1_steps

G = 91440


def build(d):
    # ============================================ THEORY 3 — the design flow
    d.section_slide(
        "THEORY 3", "The Answer: a Standardized Design Flow",
        "If no one person can place the transistors, the work has to be split "
        "into steps with defined inputs and outputs — and handed to programs.",
        ["The steps of the flow, and what each produces",
         "What a CAD tool actually does: HDL in, more detailed HDL out",
         "The two competing HDLs, and the others",
         "One circuit carried down all five levels"],
        accent=VIOLET)

    s = d.slide("3.1 · THE FLOW", "VLSI Design Flow")
    y = d.image(s, TOP - 45720, "design_flow_steps", 4150000)
    card_from(d, s, y + G, l1_flow.CARDS, "design_flow_steps",
              h=1097280)

    s = d.slide("3.2 · THE CAD TOOL", "What a CAD Tool Actually Does",
                accent=VIOLET)
    y = d.image(s, TOP - 45720, "cad_transform", 4150000)
    card_from(d, s, y + G, l1_flow.CARDS, "cad_transform")

    s = d.slide("3.3 · THE LANGUAGES", "Two Competing HDLs")
    y = d.image(s, TOP - 45720, "hdl_family", 4150000)
    card_from(d, s, y + G, l1_flow.CARDS, "hdl_family", h=1371600)

    s = d.slide("3.3 · THE LANGUAGES", "The Same Counter, in Both Languages")
    y = d.cols(s, TOP, [
        ("VERILOG  ·  rtl/counter4.v", [[R("Terse. The register, the reset and "
          "the increment fit in four lines.", s=11.5)]], TEAL, CARD),
        ("VHDL  ·  vhdl/counter4.vhd", [[R("Verbose and strongly typed — the "
          "count has to be converted before it leaves the entity.",
          s=11.5)]], VIOLET, CARD)],
        h=868680)
    yy = y + G
    d.code(s, yy, [
        "module counter4 (",
        "    input  wire       clk,",
        "    input  wire       rst,",
        "    output reg  [3:0] q",
        ");",
        "    always @(posedge clk) begin",
        "        if (rst) q <= 4'd0;",
        "        else     q <= q + 4'd1;",
        "    end",
        "endmodule",
    ], size=13.5, x=ML, w=(MW - 182880) / 2, h=2900000, accent=TEAL)
    d.code(s, yy, [
        "entity counter4 is",
        "  port (clk : in  std_logic;",
        "        rst : in  std_logic;",
        "        q   : out std_logic_vector(3 downto 0));",
        "end entity;",
        "architecture rtl of counter4 is",
        "  signal cnt : unsigned(3 downto 0);",
        "begin",
        "  process (clk) begin",
        "    if rising_edge(clk) then",
        "      if rst = '1' then cnt <= (others => '0');",
        "      else              cnt <= cnt + 1;",
        "      end if;",
        "    end if;",
        "  end process;",
        "  q <= std_logic_vector(cnt);",
        "end architecture;",
    ], size=11.0, x=ML + (MW + 182880) / 2, w=(MW - 182880) / 2,
        h=3960000, accent=VIOLET)

    s = d.slide("3.4 · THE LADDER", "Simplistic View of the Design Flow")
    d.image(s, TOP - 45720, "flow_ladder", 5200000)

    s = d.slide("3.4 · THE LADDER", "One Circuit, All Five Levels")
    y = d.image(s, TOP - 45720, "ladder_example", 4150000)
    card_from(d, s, y + G, l1_flow.CARDS, "ladder_example")

    s = d.slide("3.4 · THE LADDER", "What Counts as a \"Component\" at Each Level")
    y = d.image(s, TOP - 45720, "abstraction_what_changes", 4150000)
    card_from(d, s, y + G, l1_flow.CARDS, "abstraction_what_changes")

    # ============================================ THEORY 4 — the steps
    d.section_slide(
        "THEORY 4", "The Steps, One at a Time",
        "The lecturer now walks down the ladder, naming each level and saying "
        "what its description is made of. This section follows him rung by "
        "rung.",
        ["Behavioral design — four ways of saying what a circuit does",
         "Data path design, and what a netlist really is",
         "Logic design, standard cells, and the optimisation trade-off",
         "Physical design, manufacturing, and the FPGA alternative",
         "The other steps: simulation, formal verification, test"],
        accent=GREEN)

    s = d.slide("4.1 · BEHAVIORAL DESIGN", "The Four Ways of Saying What a "
                "Circuit Does", accent=VIOLET)
    y = d.image(s, TOP - 45720, "behavioral_forms", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "behavioral_forms")

    s = d.slide("4.2 · DATA PATH DESIGN", "Register Transfer Level")
    y = d.bullets(s, TOP, [
        [R("The components are no longer statements. They are ", s=12.5),
         R("registers, adders, multipliers, multiplexers, decoders and buses",
           b=True, c=NAVY, s=12.5), R(" — things you could point at on a "
           "block diagram.", s=12.5)],
        [R("The name says what happens: on each clock edge, values are ", s=12.5),
         R("TRANSFERRED between REGISTERS", b=True, c=TEAL, s=12.5),
         R(", possibly through some logic on the way.", s=12.5)],
        [R("This is the level a Verilog designer actually works at, and it is "
           "the level the rest of Module 2 is about.", s=12.5)],
    ], step=457200)
    y = d.code(s, y + G, [
        "// the behavioural description above, as the tool re-wrote it:",
        "assign _0_ = q + 4'h1;          // an incrementer",
        "always @(posedge clk)           // a 4-bit register",
        "  if (rst) q <= 4'h0;           // with a synchronous reset",
        "  else     q <= _0_;",
    ], size=12.0, title="out/counter4_rtl.v — produced by Yosys in Lab 2",
        accent=TEAL)
    d.lead(s, y + G, [[R("Two components: one adder and one register. That is "
                         "what \"data path design\" means, and you will see "
                         "Yosys report exactly those two cells.",
                         b=True, c=NAVY, s=12.0)]], h=457200)

    s = d.slide("4.2 · DATA PATH DESIGN", "A Netlist Is a Directed Graph")
    y = d.image(s, TOP - 45720, "netlist_graph", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "netlist_graph")

    s = d.slide("4.2 · DATA PATH DESIGN", "The Same Netlist, at Three Levels")
    y = d.image(s, TOP - 45720, "netlist_levels", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "netlist_levels")

    s = d.slide("4.3 · THE DISTINCTION",
                "Structural or Behavioural", accent=VIOLET)
    y = d.image(s, TOP - 45720, "struct_vs_behav", 3900000)
    card_from(d, s, y + G, l1_steps.CARDS, "struct_vs_behav_extra")

    s = d.slide("4.3 · THE DISTINCTION", "The Same Adder, Written Both Ways")
    yy = TOP
    d.code(s, yy, [
        "// BEHAVIOURAL - say what it does",
        "module add2 (input a, b, cin,",
        "             output sum, cout);",
        "    assign {cout, sum} = a + b + cin;",
        "endmodule",
        "",
        "// one line. The tool picks the gates.",
    ], size=13.0, x=ML, w=(MW - 182880) / 2, h=2080000, accent=VIOLET)
    y = d.code(s, yy, [
        "// STRUCTURAL - say what it is made of",
        "module add2 (input a, b, cin,",
        "             output sum, cout);",
        "    wire s1, c1, c2;",
        "    xor  u1 (s1,   a,  b);",
        "    and  u2 (c1,   a,  b);",
        "    xor  u3 (sum,  s1, cin);",
        "    and  u4 (c2,   s1, cin);",
        "    or   u5 (cout, c1, c2);",
        "endmodule",
    ], size=13.0, x=ML + (MW + 182880) / 2, w=(MW - 182880) / 2,
        h=2830000, accent=TEAL)
    d.card(s, y + G, "Both are legal Verilog, and both describe the same adder",
           [[R("You will write far more behavioural code than structural. But "
               "the tool's OUTPUT is always structural — which is exactly why "
               "you have to be able to read it.")]], accent=NAVY)

    s = d.slide("4.4 · LOGIC DESIGN", "What a Standard Cell Is", accent=GREEN)
    y = d.image(s, TOP - 45720, "standard_cell", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "standard_cell_extra")

    s = d.slide("4.4 · LOGIC DESIGN", "Why a Cell Library Exists",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "opt_conflict", 4000000)
    card_from(d, s, y + G, l1_steps.CARDS, "standard_cell")

    s = d.slide("4.4 · LOGIC DESIGN", "Three Goals That Pull Apart",
                accent=AMBER)
    y = d.tiers(s, TOP, [
        ("GATES", "Fewer cells, less silicon, cheaper chip — but the cheapest "
         "structure is often a deep one, and deep means slow.", TEAL),
        ("LEVELS", "The depth of the logic IS its delay, and delay is what "
         "limits the clock. Flattening it costs extra gates.", VIOLET),
        ("TRANSITIONS", "Every change at a gate output moves charge and "
         "spends energy. Reducing switching usually means adding control "
         "logic.", AMBER)],
        h=868680)
    card_from(d, s, y + G, l1_steps.CARDS, "opt_conflict")

    s = d.slide("4.5 · PHYSICAL DESIGN", "Polygons, One Layer at a Time",
                accent=AMBER)
    y = d.image(s, TOP - 45720, "physical_design", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "physical_design")

    s = d.slide("4.5 · PHYSICAL DESIGN", "Two Ways to Finish: ASIC or FPGA")
    y = d.image(s, TOP - 45720, "asic_vs_fpga", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "asic_vs_fpga")

    s = d.slide("4.6 · THE REST", "Other Steps in the Design Flow",
                accent=GREEN)
    y = d.image(s, TOP - 45720, "other_steps", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "other_steps")

    s = d.slide("4.7 · THE MAP", "Where the Rest of This Course Sits")
    y = d.image(s, TOP - 45720, "course_roadmap", 4150000)
    card_from(d, s, y + G, l1_steps.CARDS, "course_roadmap_extra")
