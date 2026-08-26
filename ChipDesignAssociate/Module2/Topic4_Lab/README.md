# Module 2 · Topic 4 — RTL Design Using HDL · Lab Sources

The complete practical programme for Topic 4. Twenty-two Verilog designs, five
self-checking testbenches, and scripts for all three toolchains.

Everything here has been compiled, linted, simulated and synthesised with the
open-source toolchain. The Vivado and ModelSim scripts are working templates —
see *A note on the vendor tools* below.

## Prerequisites

| Tool | Purpose | Install (Ubuntu / WSL) |
|---|---|---|
| Icarus Verilog ≥ 11 | compile and simulate | `sudo apt install iverilog` |
| GTKWave | view `.vcd` waveforms | `sudo apt install gtkwave` |
| Verilator ≥ 5 | lint — catches width bugs | `sudo apt install verilator` |
| Yosys ≥ 0.30 | synthesise to gates | `sudo apt install yosys` |
| Graphviz (optional) | render Yosys schematics | `sudo apt install graphviz` |

macOS: `brew install icarus-verilog gtkwave verilator yosys graphviz`
Windows: use WSL2 and follow the Ubuntu column, or install the OSS CAD Suite.

The syllabus specifies **Vivado Design Suite** and **ModelSim**; scripts for
both are in `scripts/`. Use the free tools to learn the concepts at home, then
apply the identical flow on the vendor tools in the lab.

## Quick start

```bash
cd Topic4_Lab
./scripts/lint.sh          # static checks FIRST - one second, catches width bugs
./scripts/run_all.sh       # compile + simulate all five labs; all report PASS
./scripts/synth_all.sh     # synthesise everything; all report no latches
gtkwave uart.vcd &         # look at the UART loopback
```

## The five labs

| Lab | Designs | Testbench | What it teaches |
|---|---|---|---|
| **L1** combinational | `mux2` `mux4` `decoder3to8` `priority_encoder8` `alu` `seven_seg` `adder_gen` | `tb_comb.v` | `assign` vs `always @(*)`, default assignments, `case` vs `if/else-if`, `generate` |
| **L2** sequential | `reg_en` `shift_reg` `counter` `edge_detect` `synchroniser` `debouncer` `clk_divider` | `tb_seq.v` | the four clocked templates, non-blocking assignment, clock enables, CDC |
| **L3** state machines | `traffic_fsm` `vending_fsm` `seq_detect_1011` | `tb_fsm.v` | the three-block FSM template, safe defaults, Moore outputs |
| **L4** memory | `sync_fifo` `sync_ram` | `tb_mem.v` | memory inference, pointer arithmetic, scoreboards, randomised stimulus |
| **L5** UART (capstone) | `uart_tx` `uart_rx` | `tb_uart.v` | a complete FSMD, loopback testing, and an independent frame decoder |

Plus `broken_examples.v` — **deliberately wrong** code, so you can see each
failure in a real tool report rather than only reading about it.

## Expected results

```
$ ./scripts/lint.sh
LINT CLEAN

$ ./scripts/run_all.sh
=== L1_comb  ===  PASS - L1 combinational library, all checks correct
=== L2_seq   ===  PASS - L2 sequential library, all checks correct
=== L3_fsm   ===  PASS - L3 state machines, all checks correct
=== L4_mem   ===  PASS - L4 FIFO and RAM, all checks correct
=== L5_uart  ===  PASS - L5 UART, loopback and frame both correct
ALL LABS PASSED

$ ./scripts/synth_all.sh
ALL DESIGNS SYNTHESISED, NO LATCHES INFERRED
```

Representative Yosys cell counts (generic gates, after `abc`):

| Design | Cells | Flip-flops |
|---|---|---|
| `counter` (4-bit, mod-10) | 38 | 4 |
| `traffic_fsm` | 52 | 12 |
| `uart_tx` | 120 | 27 |
| `uart_rx` | 120 | 36 |
| `sync_fifo` (8 × 8) | 255 | 72 |

## Experiments worth doing

1. **See a latch.** `yosys -p "read_verilog rtl/broken_examples.v; synth -top
   bad_latch; stat"` reports `$_DLATCH_N_` and `$_DLATCH_P_`. Add a default
   assignment at the top of each `always` block and watch both disappear.

2. **See a shift register collapse.** Synthesise `bad_blocking`: it reports
   **one** `$_DFF_P_`, not two, because the blocking assignments make `q2` take
   `d` rather than the old `q1`. Change `=` to `<=` and you get two.

3. **See truncation.** Synthesise `bad_width` and work out why 9 + 8 gives 1.
   Then run `./scripts/lint.sh` and watch Verilator name the problem for you.

4. **Change a parameter, not the code.** Re-synthesise `counter` with
   `-chparam W 16` and confirm the flip-flop count goes from 4 to 16 with no
   source change at all.

5. **Prove the UART is really parameterised.** Edit `CPB` in `tb/tb_uart.v` from
   16 to 434 (the real 50 MHz / 115 200 value) and re-run. It still passes — the
   simulation just takes longer.

6. **Find the rule behind the UART bug.** Reintroduce the truncation (below) into a
   copy of `rtl/uart_rx.v`, then send all 256 byte values at several different
   `CLKS_PER_BIT` values. Measured with Icarus Verilog 12.0:

   | `CLKS_PER_BIT` | 8 | 16 | 27 | 32 | 64 | 100 | 434 |
   |---|---|---|---|---|---|---|---|
   | failures / 256 | 254 | 255 | **0** | 255 | 255 | **0** | **0** |

   The bug appears **exactly when `CLKS_PER_BIT` is a power of two**. `CW` is
   `$clog2(N)` — the bits needed to count 0..N-1. For any N that is not a power of
   two, N itself still fits in `CW` bits and the slice loses nothing, so the design
   works by luck. For N = 2^k it needs k+1 bits and truncates to zero. This is why
   434 hides the bug and 16 exposes it.

7. **Watch the tool re-encode your FSM.** `traffic_fsm` declares `reg [1:0] state`
   but synthesises to 12 flip-flops: 8 for the timer and **4** for the state.
   `grep -i fsm build/synth_traffic_fsm.txt` explains it:

   ```
   FSM_RECODE pass (re-assigning FSM state encoding)
   Recoding FSM `$fsm$\state$49' ... mapping auto encoding to `one-hot` for this FSM
   ```

   Ask for an encoding explicitly with `(* fsm_encoding = "binary" *)` and compare.
   On a 4-state machine the two encodings tie on cell count (9 vs 9 after
   `abc -g AND,OR,XOR,NAND,NOR`); one-hot uses 4 flip-flops against binary's 2.

8. **Read the schematic.**
   ```bash
   yosys -p 'read_verilog rtl/traffic_fsm.v; proc; opt; show -format dot -prefix tf'
   dot -Tpng tf.dot -o tf.png
   ```

## Two real bugs that were found while writing this lab

Both are preserved in the comments of the affected files, because they are
better teaching material than anything invented.

**A width-truncation bug in the UART.** The bit-timing limits were originally
written `CLKS_PER_BIT[CW-1:0]`. For `CLKS_PER_BIT = 16`, `CW` is 4 — and 16 does
not fit in 4 bits, so it truncated to **zero**. The receiver stopped waiting half
a bit before sampling, started sampling on bit boundaries instead of bit
centres, and corrupted some byte patterns but not others. The fix is to compute
the limits as integers and slice them where they are used. See the comment in
`rtl/uart_rx.v`.

**A state-timing bug in the vending machine.** The credit register was cleared
as the FSM *entered* the DISPENSE state, so the output logic — which needs the
credit to work out the change — saw zero. The fix is to clear it as the machine
*leaves* that state. See the comment in `rtl/vending_fsm.v`.

## A note on the vendor tools

`scripts/vivado_sim.tcl`, `scripts/vivado_synth.tcl` and
`scripts/modelsim_run.do` use standard, version-stable commands (`xvlog`,
`xelab`, `xsim`, `synth_design`, `report_utilization`; `vlib`, `vlog`, `vsim`).
They were **not** executed while this material was written, because neither tool
is installed in the authoring environment. Check them against your installed
version before the lab session — menu names and default part numbers change
between releases, and the part in `vivado_synth.tcl` must match your board.

Everything run against Icarus Verilog 12.0, Verilator 5.020 and Yosys 0.33 in
this folder was executed, and the outputs quoted above are real.
