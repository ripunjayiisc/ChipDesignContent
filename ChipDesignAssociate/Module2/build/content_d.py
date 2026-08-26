# -*- coding: utf-8 -*-
"""Topic 3 deck — tool installation, tutorials T1-T4, glossary, recap."""
from deckkit import *
from content_a import R, G


def build(d):
    # =============================================== SECTION divider
    d.section_slide("HANDS-ON", "Tools, Installation and Tutorials",
                    "Everything from here is done at a keyboard. The tools are free and take about "
                    "fifteen minutes to install.",
                    ["Install: Logisim-Evolution, Icarus Verilog, GTKWave, Yosys",
                     "T1 — Build and simulate gates, an adder and an FSM visually in Logisim",
                     "T2 — Compile and simulate a full adder and a 4-bit adder; read the waveform",
                     "T3 — Flip-flops, a shift register and a mod-10 counter",
                     "T4 — The 1011 FSM: simulate it, then synthesise it and read the netlist"],
                    accent=GREEN)

    # ================================================================ toolchain overview
    s = d.slide("HANDS-ON · TOOLCHAIN", "The Four Tools and What Each One Is For", GREEN)
    y = d.image(s, TOP, "toolchain", 3383280)
    y = d.card(s, y + 91440, "Why this particular set",
               [[R("They are free, open-source, small, cross-platform and script-driven — so every "
                   "student can run the identical flow at home, and the whole lab can be checked "
                   "automatically. The commercial equivalents (ModelSim/Questa, VCS, Design Compiler, "
                   "Vivado) do the same jobs with the same concepts and a larger price tag.")]],
               accent=TEAL, h=776224)
    d.text(s, ML, y + 91440, MW, 274320, [[
        R("Java note: ", b=True, c=NAVY, s=10.5),
        R("Logisim-Evolution needs a Java Runtime (JRE 17 or later). Everything else is native.",
          s=10.5)]])

    # ================================================================ install
    s = d.slide("HANDS-ON · INSTALLATION", "Installing the Toolchain — Step by Step", GREEN)
    y = d.cols(s, TOP, [
        ("Windows  (recommended: WSL2)",
         [[R("1. Open PowerShell as Administrator:", s=9.5)],
          [R("wsl --install -d Ubuntu", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("2. Reboot, then open the Ubuntu terminal.", s=9.5)],
          [R("3. Run the Ubuntu commands opposite.", s=9.5)],
          [R("4. For GTKWave graphics, install VcXsrv or use WSLg (Win 11).", s=9.5)],
          [R("Alternative without WSL: download the OSS CAD Suite ZIP, unzip, and run "
             "environment.bat.", s=9.5, i=True, c=SLATE)]], TEAL, CARD),
        ("Ubuntu / Debian / WSL",
         [[R("sudo apt update", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("sudo apt install -y iverilog \\", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("    gtkwave yosys default-jre", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("", s=6)],
          [R("Logisim-Evolution: download the .jar from its GitHub releases page and run:", s=9.5)],
          [R("java -jar logisim-evolution.jar", s=9.5, f=MONO_FONT, c=NAVY, b=True)]],
         GREEN, CARD_G),
        ("macOS  (Homebrew)",
         [[R("/bin/bash -c \"$(curl -fsSL \\", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("  https://raw.githubusercontent.com/\\", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("  Homebrew/install/HEAD/install.sh)\"", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("", s=6)],
          [R("brew install icarus-verilog \\", s=9.5, f=MONO_FONT, c=NAVY, b=True)],
          [R("    gtkwave yosys temurin", s=9.5, f=MONO_FONT, c=NAVY, b=True)]], AMBER, CARD_A)],
        h=2011680)
    y = d.code(s, y + G, [
        "# ---- VERIFY the installation - every one of these must print a version ----",
        "iverilog -V   | head -1        # expect: Icarus Verilog version 11.x or 12.x",
        "vvp   -V      | head -1        # the Icarus runtime engine",
        "gtkwave --version | head -1    # expect: GTKWave Analyzer v3.3.x",
        "yosys -V                       # expect: Yosys 0.3x",
        "java -version                  # expect: openjdk 17 or later",
    ], size=9.5, title="Verification — run this before the lab, not during it", accent=GREEN)
    d.text(s, ML, y + G, MW, 274320, [[
        R("Troubleshooting: ", b=True, c=RED, s=10.5),
        R("'command not found' after apt succeeded → close and reopen the terminal.   "
          "GTKWave opens but shows nothing → you forgot $dumpfile/$dumpvars in the testbench.   "
          "Yosys 'read_verilog: syntax error' → Icarus accepts some non-standard code that Yosys "
          "rejects; fix the RTL, do not work around it.", s=10.5)]])

    # ================================================================ T1
    s = d.slide("HANDS-ON · TUTORIAL T1", "Logisim-Evolution — See the Logic Before You Code It", GREEN)
    y = d.lead(s, TOP, [[
        R("Goal: ", b=True, c=NAVY, s=12.5),
        R("build three circuits by clicking, poke the inputs, and watch the wires change colour. "
          "Thirty minutes here saves hours of confusion later. ", s=12.5),
        R("Deliverable: three .circ files plus a screenshot of each truth table.", i=True, c=SLATE,
          s=12.5)]], h=548640)
    y = d.card(s, y + G, "T1.1  —  A half adder from scratch  (10 min)",
               [[R("1. Launch:  java -jar logisim-evolution.jar", f=MONO_FONT, s=10)],
                [R("2. From the toolbar place two Input pins, label them A and B (right-click → Edit "
                   "label).", s=10.5)],
                [R("3. From the Gates library drag in one XOR and one AND gate.", s=10.5)],
                [R("4. Place two Output pins, label them S and C.", s=10.5)],
                [R("5. Wire A and B to both gates; XOR → S, AND → C.", s=10.5)],
                [R("6. Press the poke (hand) tool and click A and B to toggle them. Verify all four "
                   "rows against the truth table on slide 23.", s=10.5)]],
               accent=TEAL, h=1691640)
    y = d.cols(s, y + G, [
        ("T1.2  —  4-bit ripple adder  (15 min)",
         [[R("· Project → Add Circuit… name it  full_adder;  build it from two half adders + an OR.",
             s=10)],
          [R("· Back in main, place four copies of your full_adder from the project tree.", s=10)],
          [R("· Chain Cout → Cin. Drive A and B from 4-bit input pins.", s=10)],
          [R("· Add 5, add 3, check you get 8. Then add 15 + 1 and confirm Cout goes high.", s=10)]],
         AMBER, CARD_A),
        ("T1.3  —  The 1011 detector  (20 min)",
         [[R("· Place a 3-bit Register and a Clock from the Memory / Wiring libraries.", s=10)],
          [R("· Implement the next-state equations from slide 54 with gates.", s=10)],
          [R("· Simulate → Tick Enabled, then hand-enter 1,0,1,1 on X and watch Z pulse.", s=10)],
          [R("· Keep going with 0,1,1 and confirm the OVERLAPPING second hit.", s=10, b=True, c=GREEN)]],
         GREEN, CARD_G)], h=1508760)
    d.text(s, ML, y + 45720, MW, 228600, [[
        R("Checkpoint question for the class: ", b=True, c=SLATE, s=10),
        R("in T1.3, what happens if you tick the clock while X is changing? Relate the answer to "
          "the metastability slide.", s=10, i=True)]])

    # ================================================================ T2
    s = d.slide("HANDS-ON · TUTORIAL T2", "Icarus Verilog + GTKWave — Simulate a Full Adder", GREEN)
    y = d.lead(s, TOP, [[
        R("Goal: ", b=True, c=NAVY, s=12.5),
        R("take the same circuit you clicked together in T1 and describe it in Verilog, then prove it "
          "correct with a self-checking testbench and look at the waveform.", s=12.5)]], h=411480)
    y = d.code(s, y + G, [
        "// ---------- full_adder.v ----------",
        "module full_adder (input a, input b, input cin, output sum, output cout);",
        "    assign sum  = a ^ b ^ cin;",
        "    assign cout = (a & b) | (cin & (a ^ b));",
        "endmodule",
        "",
        "// ---------- tb_full_adder.v ----------",
        "`timescale 1ns/1ps",
        "module tb_full_adder;",
        "    reg a, b, cin;  wire sum, cout;  integer i;  integer errors = 0;",
        "    full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));",
        "",
        "    initial begin",
        "        $dumpfile(\"fa.vcd\");  $dumpvars(0, tb_full_adder);   // <-- waveform dump",
        "        for (i = 0; i < 8; i = i + 1) begin",
        "            {a, b, cin} = i[2:0];  #10;",
        "            if ({cout, sum} !== (a + b + cin)) begin",
        "                $display(\"FAIL a=%b b=%b cin=%b -> %b%b\", a, b, cin, cout, sum);",
        "                errors = errors + 1;",
        "            end",
        "        end",
        "        if (errors == 0) $display(\"PASS - all 8 cases correct\");",
        "        $finish;",
        "    end",
        "endmodule",
    ], size=6.6, title="Two files — the design and a self-checking testbench", accent=TEAL)
    y = d.code(s, y + G, [
        "iverilog -g2012 -o fa.out full_adder.v tb_full_adder.v   # compile",
        "vvp fa.out                                               # run -> 'PASS - all 8 cases correct'",
        "gtkwave fa.vcd &                                         # view the waveform",
        "# In GTKWave: pick tb_full_adder in the SST pane, select all, Insert, then 'zoom fit'.",
    ], size=7.6, title="Run it — three commands", accent=GREEN)

    # ================================================================ T3
    s = d.slide("HANDS-ON · TUTORIAL T3", "Sequential Logic — Flip-Flop, Shift Register, Counter", GREEN)
    y = d.lead(s, TOP, [[
        R("Goal: ", b=True, c=NAVY, s=12.5),
        R("see with your own eyes that a flip-flop samples only on the edge, that non-blocking "
          "assignment builds a real shift register, and that a mod-10 counter wraps at nine.", s=12.5)]],
        h=411480)
    y = d.code(s, y + G, [
        "// ---------- dff.v : the reference D flip-flop, async active-low reset ----------",
        "module dff (input clk, input rst_n, input d, output reg q);",
        "    always @(posedge clk or negedge rst_n)",
        "        if (!rst_n) q <= 1'b0;",
        "        else        q <= d;",
        "endmodule",
        "",
        "// ---------- shift4.v : four-stage shift register ----------",
        "module shift4 (input clk, input rst_n, input sin, output reg [3:0] q);",
        "    always @(posedge clk or negedge rst_n)",
        "        if (!rst_n) q <= 4'b0000;",
        "        else        q <= {q[2:0], sin};      // shift left, sin enters at bit 0",
        "endmodule",
        "",
        "// ---------- bcd_counter.v : mod-10 synchronous up-counter ----------",
        "module bcd_counter (input clk, input rst_n, input en, output reg [3:0] cnt);",
        "    always @(posedge clk or negedge rst_n)",
        "        if (!rst_n)        cnt <= 4'd0;",
        "        else if (en) begin",
        "            if (cnt == 4'd9) cnt <= 4'd0;",
        "            else             cnt <= cnt + 4'd1;",
        "        end",
        "endmodule",
    ], size=6.5, title="Three designs — build them in one file or three", accent=TEAL)
    y = d.cols(s, y + G, [
        ("What to look for in the waveform",
         [[R("· q changes ONLY at rising clk edges, never when d moves mid-cycle.", s=10)],
          [R("· The shift register's bit 3 lags sin by exactly four cycles.", s=10)],
          [R("· cnt goes …8, 9, 0, 1… and never reaches 10.", s=10)],
          [R("Deliverable: one annotated GTKWave screenshot per design, with the key transition "
             "circled and one sentence explaining it.", s=9.4, i=True, c=SLATE)]], GREEN, CARD_G),
        ("Experiments that teach the lesson",
         [[R("1. Change  <=  to  =  in shift4 and re-run. How many flip-flops does Yosys report now?",
             s=10, b=True, c=RED)],
          [R("2. Delete the  if (cnt == 4'd9)  line. Watch the counter run to 15 — a mod-16 counter.",
             s=10)],
          [R("3. Toggle  en  low for three cycles and confirm the count freezes.", s=10)]],
         AMBER, CARD_A)], h=1280160)

    # ================================================================ T4
    s = d.slide("HANDS-ON · TUTORIAL T4", "The 1011 FSM — Simulate, Then Synthesise It", GREEN)
    y = d.lead(s, TOP, [[
        R("Goal: ", b=True, c=NAVY, s=12.5),
        R("close the loop. Take the FSM you designed on paper, run it, then ask Yosys what hardware it "
          "actually becomes — and check that the answer matches your state diagram.", s=12.5)]],
        h=411480)
    y = d.code(s, y + G, [
        "# ---- Step 1 : simulate  (seq_detect_1011.v is the module from slide 55) ----",
        "iverilog -g2012 -o fsm.out seq_detect_1011.v tb_seq_detect.v",
        "vvp fsm.out                      # testbench drives 1011011 and checks Z pulses twice",
        "gtkwave fsm.vcd &",
        "",
        "# ---- Step 2 : synthesise and read the statistics ----",
        "yosys -p 'read_verilog seq_detect_1011.v; \\",
        "          synth -top seq_detect_1011; \\",
        "          stat'",
        "",
        "# ---- Step 3 : look at the schematic Yosys produced ----",
        "yosys -p 'read_verilog seq_detect_1011.v; proc; opt; show -format dot -prefix fsm'",
        "dot -Tpng fsm.dot -o fsm.png     # needs graphviz:  sudo apt install graphviz",
        "",
        "# ---- Step 4 : map to a real cell library and count gates ----",
        "yosys -p 'read_verilog seq_detect_1011.v; synth -top seq_detect_1011; \\",
        "          abc -g AND,OR,XOR,NAND,NOR; stat; write_verilog fsm_netlist.v'",
        "",
        "# ---- or run the whole lab in one go ----",
        "cd Topic3_Lab && ./scripts/run_all.sh && ./scripts/synth_all.sh",
    ], size=7.4, title="Four steps, four commands", accent=GREEN)
    y = d.cols(s, y + G, [
        ("What the stat report should tell you",
         [[R("· 18 cells in total", s=9.6)],
          [R("· 3 DFF cells — your 3-bit state register", s=9.6, b=True, c=GREEN)],
          [R("· 15 combinational cells", s=9.6)],
          [R("· ZERO $_DLATCH_ cells", s=9.6, b=True, c=RED)],
          [R("A latch means a default assignment is missing.", s=9.6)]], GREEN, CARD_G),
        ("Experiments — each gives a real, different answer",
         [[R("1. Synthesise  broken_latch.v  → find $_DLATCH_ in the cell list.", s=9.6)],
          [R("2. Synthesise  seq_detect_1011_onehot.v  → 14 cells and 5 flip-flops, "
             "not 18 and 3. The only change is one attribute.", s=9.6)],
          [R("3. Run  fsm_detect  → Yosys refuses to re-encode this FSM because the safe "
             "default makes it look self-resetting.", s=9.6, b=True, c=NAVY)]],
         AMBER, CARD_A)], h=1417320)
    d.text(s, ML, y + 45720, MW, 228600, [[
        R("This is the whole point of the topic: ", b=True, c=NAVY, s=10),
        R("you predicted the hardware from the state diagram, and the tool agreed with you.",
          s=10, i=True)]])

    # ================================================================ assessment
    s = d.slide("HANDS-ON · ASSESSMENT", "Lab Deliverables and Marking Rubric")
    y = d.table(s, TOP, ["Deliverable", "Evidence required", "Marks"],
                [["T1 — Logisim circuits",
                  "half_adder.circ, adder4.circ, fsm1011.circ + one screenshot each", "15"],
                 ["T2 — Full adder simulation",
                  "full_adder.v, tb_full_adder.v, console showing PASS, GTKWave screenshot", "15"],
                 ["T3 — Sequential designs",
                  "dff.v, shift4.v, bcd_counter.v, three annotated waveform screenshots", "20"],
                 ["T4 — FSM end to end",
                  "seq_detect_1011.v, testbench, waveform showing TWO Z pulses, Yosys stat output", "25"],
                 ["Written answers",
                  "Workbook Part 5 exercises E1–E14 with working shown", "15"],
                 ["Viva / explanation",
                  "Explain one design of the examiner's choosing at the whiteboard", "10"]],
                [3200400, 6217920, 1828800], rh=457200, bold_cols=(0, 2),
                col_colors={0: TEAL, 2: GREEN}, size=10)
    d.card(s, y + G, "Pass criteria",
           [[R("50 % overall, with a compulsory pass in T4 — a student who cannot take an FSM from "
               "state diagram to a verified, synthesised netlist has not met the terminal outcome for "
               "this topic. Resubmission of T4 is permitted once.")]],
           accent=AMBER, fill=CARD_A, h=914400)

    # ================================================================ glossary 1
    s = d.slide("TOPIC 3 · GLOSSARY (1 of 2)", "Key Terms — Boolean Algebra and Combinational Logic")
    terms1 = [
        ("Literal", "A variable or its complement — A and A' are two literals."),
        ("Minterm / Maxterm", "The AND term true for exactly one row / the OR term false for exactly one row."),
        ("Canonical form", "SOP or POS written directly from the truth table; unique but rarely minimal."),
        ("Implicant", "Any product term that covers only 1s of the function."),
        ("Prime implicant", "An implicant that cannot be combined further into a larger group."),
        ("Essential prime implicant", "The only prime implicant covering some particular minterm — always in the answer."),
        ("Don't-care (X)", "An input combination that cannot occur, or whose output is never read."),
        ("Universal gate", "NAND or NOR — enough on its own to build any function."),
        ("Duality", "Swap AND↔OR and 0↔1; a true Boolean identity stays true."),
        ("Fan-in / Fan-out", "Number of inputs to a gate / number of loads driven by one output."),
        ("Propagation delay t_pd", "Time from an input change to the corresponding output change."),
        ("Critical path", "The slowest input-to-output route; it sets the block's maximum speed."),
        ("Hazard / glitch", "A transient wrong output caused by unequal path delays; logic is still correct."),
        ("Gate equivalent (GE)", "Area unit: the area of one 2-input NAND cell in that technology."),
    ]
    y = TOP
    half = 7
    for col in range(2):
        x = ML + col * (MW / 2 + 91440)
        w = MW / 2 - 91440
        yy = TOP
        for t, defn in terms1[col * half:(col + 1) * half]:
            d.text(s, x, yy, w, 640080,
                   [[R(t + " — ", b=True, c=TEAL, s=10.5), R(defn, s=10.5)]], space_after=3)
            yy += 685800
    d.text(s, ML, 6172200, MW, 228600, [[
        R("Every term above appears in the workbook glossary with a worked micro-example.",
          s=10, i=True, c=SLATE)]])

    # ================================================================ glossary 2
    s = d.slide("TOPIC 3 · GLOSSARY (2 of 2)", "Key Terms — Sequential Logic and State Machines")
    terms2 = [
        ("Latch", "Level-sensitive storage: transparent for as long as its enable is asserted."),
        ("Flip-flop", "Edge-triggered storage: samples its input at one instant per clock cycle."),
        ("Setup time t_su", "How long data must be stable BEFORE the clock edge."),
        ("Hold time t_h", "How long data must stay stable AFTER the clock edge."),
        ("Clock-to-Q t_cq", "Delay from the clock edge until the output is valid."),
        ("Metastability", "An invalid intermediate output state after a setup/hold violation; resolves at random."),
        ("Synchroniser", "Two (or three) cascaded flip-flops that make metastable failure vanishingly unlikely."),
        ("Clock skew", "Fixed difference in edge arrival time between flip-flops; caused by the clock tree."),
        ("Jitter", "Random cycle-to-cycle variation in edge arrival; caused by noise and the PLL."),
        ("Slack", "Available time minus required time. Positive = met, negative = violation."),
        ("State", "An equivalence class of input histories — everything the circuit needs to remember."),
        ("Moore machine", "Output depends on the state only; glitch-free, reacts one cycle later."),
        ("Mealy machine", "Output depends on state AND input; fewer states, reacts immediately, can glitch."),
        ("Safe FSM", "One whose default branch returns any illegal state code to a known good state."),
    ]
    for col in range(2):
        x = ML + col * (MW / 2 + 91440)
        w = MW / 2 - 91440
        yy = TOP
        for t, defn in terms2[col * 7:(col + 1) * 7]:
            d.text(s, x, yy, w, 640080,
                   [[R(t + " — ", b=True, c=AMBER, s=10.5), R(defn, s=10.5)]], space_after=3)
            yy += 685800
    d.text(s, ML, 6172200, MW, 228600, [[
        R("Acronyms: SOP sum of products · POS product of sums · FSM finite state machine · "
          "CDC clock-domain crossing · STA static timing analysis · CTS clock-tree synthesis · "
          "MTBF mean time between failures.", s=10, i=True, c=SLATE)]])

    # ================================================================ recap
    s = d.slide("TOPIC 3 · RECAP", "Consolidation and Self-Check")
    y = d.cols(s, TOP, [
        ("3a — Boolean algebra and gates",
         [[R("· Digital = two voltage bands with a guard band between them.", s=10)],
          [R("· Three operators; seven gates; NAND and NOR are universal.", s=10)],
          [R("· De Morgan lets you push bubbles through any network.", s=10)],
          [R("· Truth table → canonical SOP/POS → K-map → minimal form.", s=10)],
          [R("· Minimisation buys area, power and speed — all three at once.", s=10)]], TEAL, CARD),
        ("3b — Combinational logic",
         [[R("· No feedback, no memory; output = f(inputs now).", s=10)],
          [R("· Seven-step procedure; the truth table is where bugs hide.", s=10)],
          [R("· Adders, MUX, decoders, comparators, ALU — know all five.", s=10)],
          [R("· Ripple carry is O(n); lookahead is O(log n).", s=10)],
          [R("· Hazards are real; synchronous design tolerates them.", s=10)]], AMBER, CARD_A),
        ("3c — Sequential logic and FSMs",
         [[R("· Feedback through a clocked element = memory = state.", s=10)],
          [R("· Latch is level-sensitive; flip-flop is edge-triggered. Use flip-flops.", s=10)],
          [R("· T ≥ t_cq + t_logic + t_setup sets fₘₐₓ; hold is a separate race.", s=10)],
          [R("· Synchronise every asynchronous input. Always.", s=10)],
          [R("· FSM = state register + next-state logic + output logic. Three always blocks.", s=10)]],
         GREEN, CARD_G)], h=2377440)
    y = d.card(s, y + G, "Self-check — you should be able to answer all ten without notes",
               [[R("1. Prove (A+B)' = A'B' with a truth table.   "
                   "2. Minimise Σm(0,2,5,7,8,10,13,15) on a 4-variable K-map.   "
                   "3. Why is NAND universal but AND is not?")],
                [R("4. Draw a full adder from two half adders.   "
                   "5. A 16-bit ripple adder has t_carry = 80 ps. What is its worst-case delay?   "
                   "6. Name three hazards and one cure for each.")],
                [R("7. Why does slowing the clock never fix a hold violation?   "
                   "8. Sketch the 2-flop synchroniser and say what it protects against.   "
                   "9. Convert the 1011 Moore machine to Mealy — how many states now?")],
                [R("10. Given t_cq = 50, t_logic = 300, t_setup = 40, skew = 20 ps, what is fₘₐₓ?",
                   b=True, c=NAVY)]],
               accent=NAVY, h=1554480)

    # ================================================================ next
    s = d.slide("TOPIC 3 · WHAT'S NEXT", "From Logic Diagrams to Verilog — Topic 4")
    y = d.lead(s, TOP, [[
        R("You now have the vocabulary. ", b=True, c=NAVY, s=12.5),
        R("Topic 4 (RTL Design Using HDL, 6 hours) is where you stop drawing gates and start writing "
          "them. Every construct you meet there maps onto something from this topic — which is why "
          "this topic came first.")]], h=548640)
    y = d.table(s, y + G, ["What you learned in Topic 3", "How it appears in Topic 4"],
                [["Truth table, SOP, K-map", "assign  and  always @(*)  with case/if"],
                 ["Multiplexer", "the ternary operator and every case statement"],
                 ["Full adder, ripple carry", "the  +  operator — and the timing report that follows it"],
                 ["D flip-flop, register", "always @(posedge clk)  with non-blocking assignment"],
                 ["Reset behaviour", "the two reset templates, and why the async one is in the "
                                     "sensitivity list"],
                 ["State diagram, state table", "the three-block FSM template with localparam states"],
                 ["Hazard, latch inference", "the synthesis warnings you must never ignore"]],
                [5486400, 5760720], rh=411480, bold_cols=(0,), col_colors={0: TEAL}, size=10.5)
    d.card(s, y + G, "Before the next session",
           [[R("Finish tutorials T1–T4 and the workbook exercises. Bring your working "
               "seq_detect_1011.v — Topic 4 begins by rewriting it three different ways and comparing "
               "the synthesis results.")]],
           accent=GREEN, fill=CARD_G, h=822960)
