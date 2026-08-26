# -*- coding: utf-8 -*-
"""Workbook Part 4: guided tutorials T1-T4."""
from wbkit import *
from wb_part1 import B, N, I, M


def build(w):
    w.h1("Part 4 · Guided Tutorials")
    w.para([N("Everything from here is done at a keyboard. The tools are free, open-source, "
              "cross-platform and take about fifteen minutes to install. Every command and every "
              "expected output in this part has been run and verified.")])

    # ---------------------------------------------------------- 4.0
    w.h2("4.0  Installing the toolchain")
    w.image("toolchain", 6.5, "Figure 4.1 — one flow: draw it, describe it, simulate it, look at "
                              "it, synthesise it")
    w.table(["Tool", "What it is for", "Answers the question"],
            [["Logisim-Evolution", "draw and click logic circuits", "what does this circuit DO?"],
             ["Icarus Verilog", "compile and simulate Verilog", "does my code behave correctly?"],
             ["GTKWave", "view the .vcd waveform dump", "why did it do that?"],
             ["Yosys", "synthesise RTL to a gate netlist", "what hardware did I actually write?"]],
            [1.6, 2.5, 2.5], bold_cols=(0,), size=9, align_center=False)

    w.h3("Ubuntu, Debian or WSL")
    w.code(["sudo apt update",
            "sudo apt install -y iverilog gtkwave yosys graphviz default-jre",
            "",
            "# Logisim-Evolution: download the .jar from its GitHub releases page, then",
            "java -jar logisim-evolution.jar"], "Linux / WSL install")
    w.h3("Windows")
    w.numbered([
        [N("Open PowerShell as Administrator and run "), M("wsl --install -d Ubuntu"), N(".")],
        N("Reboot, open the Ubuntu terminal, and follow the Linux commands above."),
        N("For GTKWave graphics use WSLg (Windows 11) or install VcXsrv (Windows 10)."),
        N("Alternative without WSL: download the OSS CAD Suite ZIP, unzip it, and run "
          "environment.bat before using the tools."),
    ])
    w.h3("macOS")
    w.code(['/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            "brew install icarus-verilog gtkwave yosys graphviz temurin"], "macOS install via Homebrew")

    w.h3("Verify before the lab, not during it")
    w.code(["iverilog -V | head -1        # Icarus Verilog version 11.x or 12.x",
            "vvp -V      | head -1        # the Icarus runtime engine",
            "gtkwave --version | head -1  # GTKWave Analyzer v3.3.x",
            "yosys -V                     # Yosys 0.3x",
            "java -version                # openjdk 17 or later"],
           "Each of these must print a version")
    w.callout("Troubleshooting",
              [[B("'command not found' after apt succeeded "), N("→ close and reopen the terminal.")],
               [B("GTKWave opens but shows nothing "), N("→ you forgot "), M("$dumpfile"),
                N(" and "), M("$dumpvars"), N(" in the testbench.")],
               [B("Yosys says 'read_verilog: syntax error' "),
                N("→ Icarus accepts some non-standard code that Yosys rejects. Fix the RTL; do not "
                  "work around it.")],
               [B("Simulation runs forever "), N("→ you have no "), M("$finish"),
                N(" , or a clock generator with no timescale.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")

    # ---------------------------------------------------------- T1
    w.h2("4.1  Tutorial T1 — Logisim-Evolution: see the logic before you code it")
    w.para([B("Goal. "), N("Build three circuits by clicking, poke the inputs, and watch the wires "
              "change colour. Thirty minutes here saves hours of confusion later.")])
    w.para([B("Deliverable. "), N("Three .circ files plus a screenshot of each truth table.")])

    w.h3("T1.1  A half adder from scratch  (10 min)")
    w.numbered([
        [N("Launch: "), M("java -jar logisim-evolution.jar")],
        N("From the toolbar place two Input pins. Right-click each → Edit label → name them A and B."),
        N("From the Gates library in the left-hand tree, drag in one XOR gate and one AND gate."),
        N("Place two Output pins and label them S and C."),
        N("Wire A and B to BOTH gates. Connect XOR → S and AND → C."),
        N("Select the poke tool (the hand). Click A and B to toggle them and read S and C."),
        N("Verify all four rows against the half-adder truth table in §2.3."),
    ])
    w.callout("What you should notice",
              ["Wires are green when carrying 0, bright green when carrying 1, and RED when they "
               "are in conflict — two outputs driving one wire. Red wires are the visual "
               "equivalent of an X in simulation, and you will meet the same failure in Verilog "
               "when two always blocks drive the same signal."],
              color=TEAL)

    w.h3("T1.2  A 4-bit ripple-carry adder  (15 min)")
    w.numbered([
        [N("Project → Add Circuit… and name it "), M("full_adder"),
         N(". Build it from two half adders and an OR gate, as in Figure 2.3.")],
        N("Return to the main circuit. Your full_adder now appears in the project tree — drag in "
          "four copies."),
        N("Chain them: Cout of stage i to Cin of stage i+1. Tie the first Cin to a constant 0."),
        N("Drive A and B from two 4-bit input pins (set Data Bits = 4 in the pin's properties) and "
          "split them with a Splitter from the Wiring library."),
        N("Test: 5 + 3 should give 8 with Cout = 0. Then try 15 + 1 and confirm Cout goes high "
          "while the sum wraps to 0."),
    ])

    w.h3("T1.3  The '1011' detector  (20 min)")
    w.numbered([
        N("Place a 3-bit Register and a Clock, both from the Memory / Wiring libraries."),
        N("Implement the three next-state equations from §3.13 with gates, feeding the register's D input."),
        N("Drive X from an input pin and take Z from the register's Q2 bit."),
        N("Simulate → Tick Enabled. Set X by hand before each tick and step through 1, 0, 1, 1."),
        [B("Watch Z pulse. "), N("Then continue with 0, 1, 1 and confirm the OVERLAPPING second "
                                 "detection.")],
    ])
    w.callout("Checkpoint question",
              ["In T1.3, what happens if you change X at the same moment you tick the clock? "
               "Relate your answer to §3.7. (Logisim will usually resolve it one way or the other "
               "deterministically — real silicon will not.)"],
              color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- T2
    w.h2("4.2  Tutorial T2 — Icarus Verilog and GTKWave")
    w.para([B("Goal. "), N("Take the circuit you clicked together in T1, describe it in Verilog, "
              "prove it correct with a self-checking testbench, and look at the waveform.")])
    w.code([
        "// ---------- rtl/full_adder.v ----------",
        "`timescale 1ns / 1ps",
        "module full_adder (input a, input b, input cin, output sum, output cout);",
        "    assign sum  = a ^ b ^ cin;",
        "    assign cout = (a & b) | (cin & (a ^ b));",
        "endmodule",
    ], "The design")
    w.code([
        "// ---------- tb/tb_full_adder.v ----------",
        "`timescale 1ns / 1ps",
        "module tb_full_adder;",
        "    reg  a, b, cin;  wire sum, cout;",
        "    integer i;  integer errors = 0;",
        "",
        "    full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));",
        "",
        "    initial begin",
        "        $dumpfile(\"fa.vcd\");  $dumpvars(0, tb_full_adder);   // waveform dump",
        "        for (i = 0; i < 8; i = i + 1) begin",
        "            {a, b, cin} = i[2:0];  #10;",
        "            if ({cout, sum} !== (a + b + cin)) begin",
        "                $display(\"FAIL a=%b b=%b cin=%b\", a, b, cin);",
        "                errors = errors + 1;",
        "            end",
        "        end",
        "        if (errors == 0) $display(\"PASS - all 8 cases correct\");",
        "        $finish;",
        "    end",
        "endmodule",
    ], "A self-checking testbench")
    w.code(["iverilog -g2012 -o fa.out rtl/full_adder.v tb/tb_full_adder.v   # compile",
            "vvp fa.out                                    # run -> 'PASS - all 8 cases correct'",
            "gtkwave fa.vcd &                              # view the waveform"],
           "Three commands")
    w.h3("Reading the waveform in GTKWave")
    w.numbered([
        N("The left pane (SST) is the design hierarchy. Click tb_full_adder."),
        N("The signals appear below it. Select them all and click Insert."),
        N("Press the 'zoom fit' button (the magnifier with the square) to see the whole run."),
        N("Right-click a bus → Data Format → Decimal or Hex to make multi-bit signals readable."),
        N("File → Write Save File saves your signal selection, so you do not rebuild it every time."),
    ])
    w.callout("Why the testbench checks itself",
              ["A testbench you have to read a waveform to grade is a testbench that will not catch "
               "a regression. Self-checking means the CI system, the marker, and you at 2 a.m. all "
               "get the same one-word answer. Waveforms are for DIAGNOSING a failure, not for "
               "detecting one."],
              color=GREEN, fill="EEF7F1", bar="2A9D5C")
    w.para([B("Extend it. "), N("Build a 4-bit adder from four instances and check every one of "
              "the 512 input combinations in a triple-nested loop. The lab folder already "
              "contains this as "), M("tb/tb_adder4.v"), N(".")])

    # ---------------------------------------------------------- T3
    w.h2("4.3  Tutorial T3 — flip-flop, shift register, counter")
    w.para([B("Goal. "), N("See with your own eyes that a flip-flop samples only on the edge, that "
              "non-blocking assignment builds a real shift register, and that a mod-10 counter "
              "wraps at nine.")])
    w.code([
        "// dff.v",
        "always @(posedge clk or negedge rst_n)",
        "    if (!rst_n) q <= 1'b0;",
        "    else        q <= d;",
        "",
        "// shift4.v",
        "always @(posedge clk or negedge rst_n)",
        "    if (!rst_n) q <= 4'b0000;",
        "    else        q <= {q[2:0], sin};      // shift left, sin enters at bit 0",
        "",
        "// bcd_counter.v",
        "always @(posedge clk or negedge rst_n)",
        "    if (!rst_n)             cnt <= 4'd0;",
        "    else if (en) begin",
        "        if (cnt == 4'd9)    cnt <= 4'd0;",
        "        else                cnt <= cnt + 4'd1;",
        "    end",
    ], "The three designs (full sources are in Topic3_Lab/rtl/)")
    w.code(["iverilog -g2012 -o seq.out rtl/dff.v rtl/shift4.v rtl/bcd_counter.v \\",
            "         tb/tb_sequential.v",
            "vvp seq.out",
            "gtkwave seq.vcd &"], "Compile and run")
    w.h3("What to look for in the waveform")
    w.numbered([
        N("q changes ONLY at rising clk edges. The testbench deliberately moves d in the middle of "
          "a high phase; the flip-flop completely ignores it."),
        N("sr_q[3] lags sin by exactly four clock cycles — count the edges."),
        N("cnt runs …8, 9, 0, 1… and never reaches 10, and it freezes while en is low."),
    ])
    w.h3("Three experiments that teach the lesson")
    w.numbered([
        [B("Break the shift register. "), N("Change "), M("<="), N(" to "), M("="),
         N(" in shift4.v, re-run "), M("./scripts/synth_all.sh"),
         N(" and count the flip-flops. The blocking version collapses to ONE, because q[1] is "
           "updated before q[2] reads it.")],
        [B("Break the counter. "), N("Delete the "), M("if (cnt == 4'd9)"),
         N(" line and watch the counter run to 15 — you now have a mod-16 counter.")],
        [B("Prove the enable. "), N("Hold "), M("en"), N(" low for three cycles and confirm the "
          "count does not move.")],
    ])
    w.para([B("Deliverable. "), N("One annotated GTKWave screenshot per design, with the key "
              "transition circled and one sentence explaining it.")])

    # ---------------------------------------------------------- T4
    w.h2("4.4  Tutorial T4 — the FSM, end to end")
    w.para([B("Goal. "), N("Close the loop. Take the FSM you designed on paper, run it, then ask "
              "Yosys what hardware it actually becomes — and check that the answer matches your "
              "state diagram.")])
    w.code([
        "# ---- Step 1 : simulate ----",
        "iverilog -g2012 -o fsm.out rtl/seq_detect_1011.v \\",
        "         rtl/seq_detect_1011_mealy.v tb/tb_seq_detect.v",
        "vvp fsm.out          # -> 'PASS - both detectors found exactly two overlapping matches'",
        "gtkwave fsm.vcd &",
        "",
        "# ---- Step 2 : synthesise and read the statistics ----",
        "yosys -p 'read_verilog rtl/seq_detect_1011.v; \\",
        "          synth -top seq_detect_1011; \\",
        "          abc -g AND,OR,XOR,NAND,NOR; stat'",
        "",
        "# ---- Step 3 : look at the schematic Yosys produced ----",
        "yosys -p 'read_verilog rtl/seq_detect_1011.v; proc; opt; \\",
        "          show -format dot -prefix fsm'",
        "dot -Tpng fsm.dot -o fsm.png",
        "",
        "# ---- or just run the whole lab ----",
        "cd Topic3_Lab && ./scripts/run_all.sh && ./scripts/synth_all.sh",
    ], "Four steps")
    w.h3("What the stat report should tell you")
    w.table(["Line", "Expected", "If it differs"],
            [["Number of cells", "18", "your equations or your case statement differ from ours"],
             ["$_DFF_PN0_", "3", "three flip-flops = your 3-bit state register"],
             ["combinational cells", "15", "AND, NAND, NOR, NOT, OR"],
             ["$_DLATCH_", "ZERO", "a latch means a default assignment is missing — a BUG"]],
            [1.7, 1.3, 3.4], bold_cols=(0,), size=9, align_center=False)

    w.h3("Three experiments, each with a real and different answer")
    w.numbered([
        [B("See a latch. "), N("Synthesise "), M("rtl/broken_latch.v"), N(" and find "),
         M("$_DLATCH_N_"), N(" and "), M("$_DLATCH_P_"),
         N(" in the cell list. Add a default assignment at the top of each always block and watch "
           "both disappear.")],
        [B("Change the encoding. "), N("Synthesise "), M("rtl/seq_detect_1011_onehot.v"),
         N(". The only difference from the original is a "),
         M('(* fsm_encoding = "one-hot" *)'),
         N(" attribute on the state register — and you get 14 cells with 5 flip-flops instead of "
           "18 cells with 3. More registers, less combinational logic: exactly the trade-off in "
           "§3.12.")],
        [B("Find out why Yosys will not re-encode this FSM for you. "), N("Run:")],
    ])
    w.code(["yosys -p 'read_verilog rtl/seq_detect_1011.v; hierarchy -top seq_detect_1011; \\",
            "          proc; opt; fsm_detect'",
            "",
            "# Yosys replies:",
            "#   Not marking seq_detect_1011.state as FSM state register:",
            "#       Circuit seems to be self-resetting."], "Experiment 3")
    w.callout("A real engineering trade-off, not a tool bug",
              [[N("The "), M("default: next = S0;"),
                N(" branch that makes your FSM SAFE is exactly what makes Yosys decide the circuit "
                  "is self-resetting, so it declines to extract and re-encode it.")],
               [N("Delete that line, re-synthesise, and the tool now extracts the FSM and one-hot "
                  "encodes it by itself — 14 cells, 5 flip-flops. You have traded illegal-state "
                  "recovery for automatic optimisation.")],
               [B("Which is right? "), N("For anything safety-related, keep the default and force "
                  "the encoding with the attribute instead. That is what the "),
                M("_onehot"), N(" variant does.")]],
              color=AMBER, fill="FFF7EC", bar="C77514")
    w.para([B("This is the whole point of the topic. "),
            N("You predicted the hardware from the state diagram, and the tool agreed with you — "
              "and where it disagreed, you could say exactly why.")])

    # ---------------------------------------------------------- assessment
    w.h2("4.5  Lab deliverables and marking rubric")
    w.table(["Deliverable", "Evidence required", "Marks"],
            [["T1 — Logisim circuits",
              "half_adder.circ, adder4.circ, fsm1011.circ + one screenshot each", "15"],
             ["T2 — Full adder simulation",
              "full_adder.v, tb_full_adder.v, console showing PASS, GTKWave screenshot", "15"],
             ["T3 — Sequential designs",
              "dff.v, shift4.v, bcd_counter.v, three annotated waveform screenshots", "20"],
             ["T4 — FSM end to end",
              "seq_detect_1011.v, testbench, waveform showing TWO Z pulses, Yosys stat output", "25"],
             ["Written answers", "Part 5 exercises E1–E46 with working shown", "15"],
             ["Viva", "explain one design of the examiner's choosing at the whiteboard", "10"]],
            [1.7, 4.0, 0.7], bold_cols=(0, 2), size=9, align_center=False)
    w.callout("Pass criteria",
              ["50 % overall, with a COMPULSORY pass in T4. A student who cannot take a finite "
               "state machine from a state diagram to a verified, synthesised netlist has not met "
               "the terminal outcome for this topic. Resubmission of T4 is permitted once."],
              color=NAVY, bar="0E2A47")
    w.page_break()
