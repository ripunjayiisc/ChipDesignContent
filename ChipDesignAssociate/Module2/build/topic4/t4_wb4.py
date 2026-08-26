# -*- coding: utf-8 -*-
"""Topic 4 workbook — Part 4: tool setup and guided tutorials T1–T6."""
import _boot
from wbkit import *
from t4_wb1 import B, N, I, M


def build(w):
    w.page_break()
    w.h1("Part 4 · Tools and Guided Tutorials")
    w.para("Every flow does the same four jobs — lint, simulate, view waveforms, synthesise — and "
           "only the command names change. Learn the jobs and moving between vendors becomes a "
           "morning's work rather than a new skill.")
    w.image("toolchains", 6.4, "Four jobs, several tools for each.")
    w.table(["Job", "Open-source", "Vendor (syllabus)", "What it tells you"],
            [["Lint / static check", "Verilator --lint-only", "Vivado report_methodology",
              "Width bugs, latches, unused signals — in one second"],
             ["Simulate", "Icarus Verilog (iverilog / vvp)", "ModelSim, Questa, Vivado xsim",
              "Does it behave correctly?"],
             ["View waveforms", "GTKWave", "ModelSim wave window, Vivado simulator",
              "Where and when it went wrong"],
             ["Synthesise", "Yosys", "Vivado synth_design",
              "What hardware it becomes; area; latch warnings"]],
            widths=[1.4, 1.8, 1.6, 1.8], size=9, align_center=False)
    w.callout("Why this course uses both", [
        [N("The syllabus specifies "), B("Vivado Design Suite"), N(" and "), B("ModelSim"),
         N(", and the lab machines should have them. The open-source chain installs in under a "
           "minute on any laptop, runs on Windows through WSL2, and is what students can use at "
           "home. The concepts are identical; only the command names differ.")],
        [N("Everything in Topic4_Lab that is quoted as verified was run under Icarus Verilog "
           "12.0, Verilator 5.020 and Yosys 0.33. The Vivado and ModelSim scripts are working "
           "templates written from standard, version-stable commands, but they were "),
         B("not executed"),
         N(" while this material was prepared, because neither tool was installed in the "
           "authoring environment. Check them against your installed version before the session: "
           "part numbers and menu names change between releases.")],
    ], color=RED, fill="FDECEF", bar="C01F43")

    # ---------------------------------------------------------- 4.1
    w.h2("4.1  Installing the open-source toolchain")
    w.code([
        "# ---- Ubuntu / Debian / WSL2 ------------------------------------------------",
        "sudo apt update",
        "sudo apt install -y iverilog gtkwave verilator yosys graphviz",
        "",
        "# ---- macOS (Homebrew) ------------------------------------------------------",
        "brew install icarus-verilog gtkwave verilator yosys graphviz",
        "",
        "# ---- Windows ---------------------------------------------------------------",
        "#  Best:  install WSL2  (run  wsl --install  in an administrator PowerShell),",
        "#         then use the Ubuntu commands above inside it.",
        "#  Or:    download the OSS CAD Suite release for Windows, unzip it, and run",
        "#         its start.bat -- it contains all four tools, already built.",
        "",
        "# ---- verify ----------------------------------------------------------------",
        "iverilog -V | head -1        # Icarus Verilog version 12.0",
        "verilator --version          # Verilator 5.020",
        "yosys -V                     # Yosys 0.33",
        "gtkwave --version",
    ], caption="Copy-paste installation")
    w.callout("GTKWave on WSL2",
              [[N("GTKWave is a GUI application. On Windows 11, WSLg runs Linux GUIs with no "
                  "extra setup — just type "), M("gtkwave dump.vcd"),
                N(". On Windows 10 you need an X server such as VcXsrv plus "),
                M("export DISPLAY=:0"),
                N(", or you can simply install the native Windows build of GTKWave and open the "
                  ".vcd file that the WSL side wrote — the file system is shared.")]],
              color=TEAL)

    # ---------------------------------------------------------- 4.2
    w.h2("4.2  Installing Vivado Design Suite")
    w.numbered([
        "Create a free AMD/Xilinx account, then download the Unified Installer for Windows or "
        "Linux from the AMD downloads page.",
        "Run it and choose Vivado → Vivado ML Standard. This edition is free and needs no licence "
        "file; it covers every device you will use on a training board.",
        "On the device page select ONLY the family your board uses: Artix-7 for Basys 3 and Arty "
        "A7, Zynq-7000 for Zybo and PYNQ. Selecting everything costs well over 100 GB.",
        "Keep the Vivado Simulator (xsim) and, on Windows, the Cable Drivers. Without the drivers "
        "the board will not be detected.",
        "Disk: allow 60–100 GB for one device family. RAM: 8 GB minimum, 16 GB comfortable.",
        "Linux only: after installation run the cable-driver script under "
        "<install>/data/xicom/cable_drivers/lin64/install_script/install_drivers/",
        "Verify with  vivado -version  (source settings64.sh first on Linux).",
    ])
    w.table(["Board", "Device", "Part string", "Good for"],
            [["Basys 3", "Artix-7", "xc7a35tcpg236-1",
              "Switches, LEDs, four 7-segment digits — ideal for L1–L3"],
             ["Arty A7 / Nexys A7", "Artix-7", "xc7a35ticsg324-1L / xc7a100tcsg324-1",
              "Has a USB-UART bridge, so L5 talks to a terminal on the PC"],
             ["Zybo Z7 / PYNQ-Z2", "Zynq-7000", "xc7z010clg400-1 / xc7z020clg400-1",
              "More than this topic needs, but the same flow"]],
            widths=[1.5, 1.1, 1.9, 2.1], size=9, align_center=False)
    w.callout("Plan the session around the installer",
              ["Do not spend a scheduled lab hour installing Vivado. Either pre-install it on the "
               "lab machines, or set the download running at the start of the session and teach "
               "the open-source flow — which installs in under a minute — while it runs. The "
               "students are here to learn RTL, not an installer."],
              color=AMBER, fill="FFF7EC", bar="C77514")
    w.h3("Installation problems you will meet")
    w.bullets([
        "The installer appears to hang at 'Generating installed device list'. It is not hung; "
        "that step takes several minutes.",
        "The board is not detected: the cable drivers were skipped, or on Linux the udev rules "
        "were not installed.",
        "'No such part' from a TCL script: the part string does not match your board. Edit it in "
        "scripts/vivado_synth.tcl.",
        "On Linux, Vivado needs libtinfo and several 32-bit libraries on some distributions; the "
        "installer's log names them.",
    ])

    # ---------------------------------------------------------- 4.3
    w.h2("4.3  Installing ModelSim / Questa")
    w.bullets([
        "ModelSim Intel FPGA Starter Edition is free, needs no licence, and ships with Intel "
        "Quartus Prime Lite. Questa Intel FPGA Starter is its successor; either is fine for this "
        "course.",
        "Windows: run the installer and accept the default path.",
        [N("Linux: ModelSim is a 32-bit application. Install the multilib packages first — "),
         M("lib32z1 lib32ncurses6 libxft2:i386 libxext6:i386"),
         N(" — or vsim will exit immediately with a missing-library error.")],
        [N("Verify with "), M("vsim -version"), N(".")],
    ])
    w.h3("The commands that matter")
    w.code([
        "vlib work                              # create the working library",
        "vmap work work                         # map the logical name to it",
        "vlog rtl/*.v tb/tb_uart.v              # compile into it",
        "vsim -voptargs=+acc work.tb_uart       # elaborate and load  (+acc keeps visibility)",
        "run -all                               # simulate until $finish",
        "",
        "# with the provided script:",
        "vsim -c -gLAB=L3_fsm -do scripts/modelsim_run.do     # batch, prints PASS/FAIL",
        "vsim    -do scripts/modelsim_run.do                  # GUI, with waveforms added",
    ], caption="ModelSim / Questa")
    w.para([N("Without "), M("-voptargs=+acc"),
            N(" the optimiser removes the very signals you want to look at, and the wave window "
              "shows almost nothing. It costs simulation speed, which does not matter at this "
              "scale.")])

    # ---------------------------------------------------------- 4.4
    w.h2("4.4  The Vivado flow")
    w.image("vivado_flow", 6.2, "Create, add sources, simulate, synthesise, implement.")
    w.code([
        "# Batch simulation -- three tools, always in this order",
        "xvlog rtl/uart_tx.v rtl/uart_rx.v rtl/synchroniser.v tb/tb_uart.v   # analyse",
        "xelab -debug typical tb_uart -s tb_uart_sim                         # elaborate",
        "xsim tb_uart_sim -runall                                            # run",
        "",
        "# Batch synthesis",
        "vivado -mode batch -source scripts/vivado_synth.tcl -tclargs uart_tx",
    ], caption="Topic4_Lab/scripts/vivado_sim.tcl and vivado_synth.tcl")
    w.code([
        "create_clock -period 20.000 -name clk [get_ports clk]   # 50 MHz -- ESSENTIAL",
        "synth_design -top uart_tx -part xc7a35tcpg236-1",
        "report_utilization    -file build/vivado/uart_tx_utilization.rpt",
        "report_timing_summary -file build/vivado/uart_tx_timing.rpt",
    ], caption="What vivado_synth.tcl does")
    w.h3("What to read afterwards — not the schematic")
    w.table(["Report", "Read it for"],
            [["Utilization", "LUTs, flip-flops, block RAMs, DSPs. Compare the flip-flop count "
                             "with your own prediction from the source. A large disagreement "
                             "means the tool built something you did not intend."],
             ["Timing summary", "Worst negative slack (WNS). Positive means the design meets the "
                                "clock you constrained; negative says by how much it misses. "
                                "Without a create_clock the report is meaningless."],
             ["Messages tab", "Every [Synth 8-xxx] warning. Read all of them once. Latch "
                              "inference, width mismatch and unconnected-port warnings all live "
                              "here."]],
            widths=[1.5, 4.9], size=9, align_center=False)

    # ---------------------------------------------------------- 4.5
    w.h2("4.5  Command reference")
    w.table(["Task", "Open-source", "Vivado", "ModelSim"],
            [["Lint", "verilator --lint-only -Wall rtl/*.v", "report_methodology",
              "vlog (warnings)"],
             ["Compile", "iverilog -g2005 -o sim.vvp <files>", "xvlog <files>", "vlog <files>"],
             ["Elaborate", "(part of iverilog)", "xelab -debug typical <top>", "(part of vsim)"],
             ["Run", "vvp sim.vvp", "xsim <snapshot> -runall", "vsim -c work.<top>; run -all"],
             ["Waveforms", "gtkwave dump.vcd", "simulator wave window", "add wave -r /*"],
             ["Synthesise", "yosys -p \"...; synth -top X; stat\"", "synth_design -top X -part P",
              "(not a synthesis tool)"],
             ["Area report", "stat", "report_utilization", "—"],
             ["Timing report", "(none — no timing model)", "report_timing_summary", "—"],
             ["Find latches", "grep -i latch on the log", "Messages: [Synth 8-327]", "—"],
             ["Schematic", "show -format dot ; dot -Tpng", "Open Synthesized Design",
              "(not applicable)"]],
            widths=[1.1, 2.2, 1.7, 1.7], size=8.5, align_center=False)

    # ============================================================ TUTORIALS
    w.page_break()
    w.h1("Guided Tutorials T1 – T6")
    w.para("Six tutorials, done at the keyboard, in order. Each one ends with something you can "
           "see. Total time about four hours; they are the bridge between reading Parts 1–3 and "
           "attempting the exercises in Part 5.")

    # ---------------------------------------------------------- T1
    w.h2("T1 · First simulation — a multiplexer, end to end  (25 min)")
    w.para("Goal: compile, simulate and view a waveform, using nothing but the open-source chain.")
    w.numbered([
        "Open a terminal in the Topic4_Lab folder.",
        "Confirm the tools are present: iverilog -V, verilator --version, yosys -V.",
        "Read rtl/mux2.v. It is nine lines. Identify the parameter, the ports and the single "
        "assign.",
        "Read tb/tb_comb.v as far as the mux2 section. Find the check task, the instantiation and "
        "the $dumpfile call.",
        "Lint first:  verilator --lint-only -Wall -Wno-DECLFILENAME rtl/mux2.v",
        "Compile:  iverilog -g2005 -Wall -o build/comb.vvp rtl/mux2.v rtl/mux4.v "
        "rtl/decoder3to8.v rtl/priority_encoder8.v rtl/alu.v rtl/seven_seg.v rtl/adder_gen.v "
        "tb/tb_comb.v",
        "Run:  vvp build/comb.vvp    You should see  PASS - L1 combinational library, all checks "
        "correct",
        "Open the waveform:  gtkwave comb.vcd &   Expand tb_comb, drag a, b, sel and y into the "
        "wave pane, and press the zoom-fit button.",
        "Change sel's value in the testbench so one check must fail. Re-run. Read the FAIL message "
        "and note that it names the time, the value it got and the value it expected. Put it back.",
    ])
    w.callout("What you should be able to do now",
              ["Compile and run a simulation from the command line, read a PASS/FAIL transcript, "
               "and get a signal onto a waveform. Everything else in this topic builds on those "
               "three things."], color=GREEN, fill="EEF7F1", bar="2A9D5C")

    # ---------------------------------------------------------- T2
    w.h2("T2 · Seeing the hardware — synthesis and the latch  (30 min)")
    w.para("Goal: connect code to gates, and see a latch appear and disappear.")
    w.numbered([
        "Synthesise the multiplexer:",
        "  yosys -p \"read_verilog rtl/mux2.v; synth -top mux2; stat\"",
        "Read the cell count. There are no flip-flops, because there is no clock — confirm that "
        "matches your expectation.",
        "Now synthesise the counter:  yosys -p \"read_verilog rtl/counter.v; synth -top counter; "
        "stat\"  — 38 cells and 4 flip-flops. Before you look, predict the flip-flop count from "
        "the source. Where do the 4 come from?",
        "Re-synthesise with a different width:  yosys -p \"read_verilog rtl/counter.v; "
        "chparam -set W 16 counter; synth -top counter; stat\"  — the flip-flop count follows the "
        "parameter, with no source change at all.",
        "Now the interesting one:  yosys -p \"read_verilog rtl/broken_examples.v; synth -top "
        "bad_latch; stat\"   Look for $_DLATCH_N_ and $_DLATCH_P_. There are two.",
        "Copy bad_latch into a new file, add the missing else and the missing default, and "
        "synthesise again. The DLATCH lines are gone.",
        "Repeat for bad_blocking: it reports ONE $_DFF_P_. Change the two = to <= and it reports "
        "two.",
        "Optional, if graphviz is installed:  yosys -p 'read_verilog rtl/traffic_fsm.v; proc; opt; "
        "show -format dot -prefix tf'  then  dot -Tpng tf.dot -o tf.png  and open the picture.",
    ])
    w.callout("The habit this builds",
              ["Predict, then verify. A designer who can look at a page of RTL and describe the "
               "netlist before running the tool catches problems in review, in minutes. A "
               "designer who cannot finds them in the lab, in days."], color=TEAL)

    # ---------------------------------------------------------- T3
    w.h2("T3 · Lint before everything  (20 min)")
    w.para("Goal: learn what a linter catches that a simulator does not.")
    w.numbered([
        "Run the lab's lint script:  ./scripts/lint.sh   It should print LINT CLEAN.",
        "Now lint the deliberately broken file:  verilator --lint-only -Wall "
        "rtl/broken_examples.v   Read every message.",
        "Find the WIDTHTRUNC message for bad_width. It names the file, the line, the expected "
        "width and the actual width. That single message is what would have saved an hour on the "
        "UART bug.",
        "Introduce a fault of your own in a copy of rtl/counter.v: delete the reset branch, or "
        "assign q from two different always blocks, or misspell a signal name in a port "
        "connection.",
        "Lint it. Note which faults the linter catches immediately, which ones only synthesis "
        "catches, and which ones only simulation catches.",
        "Write down the answer to that last question in your own words. It is the most useful "
        "thing in this tutorial.",
    ])

    # ---------------------------------------------------------- T4
    w.h2("T4 · A sequential design — counters, edges and CDC  (35 min)")
    w.para("Goal: work confidently with clocked logic and understand what a testbench must do "
           "around a clock edge.")
    w.numbered([
        "Run lab 2:  iverilog -g2005 -o build/seq.vvp rtl/reg_en.v rtl/shift_reg.v rtl/counter.v "
        "rtl/edge_detect.v rtl/synchroniser.v rtl/debouncer.v rtl/clk_divider.v tb/tb_seq.v && "
        "vvp build/seq.vvp",
        "Open seq.vcd in GTKWave. Add clk, rst_n and the counter's q. Confirm that q changes only "
        "on rising clock edges and that reset forces it to zero immediately.",
        "Add the edge detector's sig, sig_d, rise and fall. Confirm rise is exactly one clock "
        "cycle wide and occurs one cycle after sig rises.",
        "Now break it deliberately: in the testbench, change the edge detector's stimulus so the "
        "input changes AT a clock edge rather than just after one. Re-run and look at the "
        "waveform. This is exactly the bug that cost time while writing this lab.",
        "Change the counter's parameters in the testbench from W=4, MAX=15 to W=4, MAX=9. Re-run "
        "and confirm it now wraps at 9 — a decade counter, from the same source.",
        "Look at rtl/synchroniser.v and find the two flip-flops. Add sync[0] and sync[1] to the "
        "waveform and confirm the output lags the input by two clock cycles.",
    ])

    # ---------------------------------------------------------- T5
    w.h2("T5 · A state machine from scratch  (45 min)")
    w.para("Goal: write a three-block FSM yourself, from a written specification.")
    w.para([B("Specification. "),
            N("Design a module "), M("door_lock"), N(" with inputs "), M("clk"), N(", "),
            M("rst_n"), N(", "), M("key_valid"), N(" and "), M("key [1:0]"), N(", and outputs "),
            M("unlocked"), N(" and "), M("alarm"),
            N(". The lock opens when the sequence 2, 1, 3 is entered on consecutive valid keys. "
              "Any wrong key returns the machine to the start; three consecutive wrong keys "
              "raise the alarm until reset. unlocked stays high for four clock cycles and then "
              "the machine returns to the start.")])
    w.numbered([
        "Draw the state diagram on paper FIRST. Name the states. Decide which outputs belong to "
        "which state — this is a Moore machine, so the outputs come from the state alone.",
        "Decide what extra state you need beyond the FSM state: a wrong-key counter and a "
        "four-cycle dwell timer. Count the flip-flops you expect.",
        "Write the module using the three-block template from 2.12. Give every case a default and "
        "every combinational block a default assignment at the top.",
        "Write a self-checking testbench. It must at minimum test: the correct sequence; a wrong "
        "key in each of the three positions; three wrong keys raising the alarm; reset clearing "
        "the alarm; and the unlocked pulse being exactly four cycles.",
        "Lint, simulate, then synthesise. Compare the flip-flop count with your prediction from "
        "step 2.",
        "Check the synthesis log for the word 'latch'. If it appears, find the branch you did not "
        "cover.",
    ])
    w.callout("If you get stuck",
              [[N("Read rtl/traffic_fsm.v (a timed Moore FSM) and rtl/seq_detect_1011.v (a "
                  "sequence detector with overlapping matches). Between them they contain every "
                  "technique this exercise needs. Exercise 55 in Part 5 gives the coverage "
                  "list your testbench must satisfy; the design itself is yours to write.")]],
              color=TEAL)

    # ---------------------------------------------------------- T6
    w.h2("T6 · The UART capstone  (60 min)")
    w.para("Goal: run, understand and extend a complete design that uses everything in the topic.")
    w.numbered([
        "Run lab 5:  iverilog -g2005 -o build/uart.vvp rtl/uart_tx.v rtl/uart_rx.v "
        "rtl/synchroniser.v tb/tb_uart.v && vvp build/uart.vvp   It prints PASS.",
        "Open uart.vcd. Add the tx line, rx_valid and rx_data. Find one complete frame: the idle "
        "high, the start bit low, eight data bits LSB first, the stop bit high. Count the clock "
        "cycles per bit and confirm it matches CLKS_PER_BIT in the testbench.",
        "Find the receiver's clk_cnt in the waveform and watch it reach HALF_BIT once, at the "
        "start, and FULL_BIT for every bit after that. That is the mid-bit alignment.",
        "Prove the design is really parameterised: change CPB in tb/tb_uart.v from 16 to 434 — the "
        "real 50 MHz / 115 200 value — and re-run. It still passes; the simulation just takes "
        "longer.",
        "Now reproduce the bug. In a COPY of rtl/uart_rx.v, change the two timing comparisons back "
        "to CLKS_PER_BIT[CW-1:0] and re-run at CPB = 16. Watch some bytes fail and others pass. "
        "Then run Verilator on it and read the WIDTHTRUNC message.",
        "Extend the design: add an odd parity bit to both the transmitter and the receiver, and a "
        "parity_error output. Update the testbench to check that a corrupted frame sets it.",
        "Optional, on a board: connect uart_tx to the USB-UART pin, send a byte per second, and "
        "read it in a terminal at the right baud rate. There is no substitute for seeing your own "
        "RTL talk to a PC.",
    ])
    w.callout("Why the UART is the capstone",
              ["It is the smallest design that contains all of it: combinational logic, "
               "sequential logic, a finite state machine, a datapath, a clock-domain crossing, "
               "parameterisation, and a self-checking testbench with an independent reference "
               "decoder. If a student can explain the UART line by line, they have understood "
               "Topic 4."], color=GREEN, fill="EEF7F1", bar="2A9D5C")
