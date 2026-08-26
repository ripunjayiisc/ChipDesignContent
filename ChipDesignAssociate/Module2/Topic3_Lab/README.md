# Module 2 · Topic 3 — Digital Logic Design Principles · Lab Sources

All the Verilog for tutorials **T1–T4**, with self-checking testbenches and
scripts. Everything here has been compiled, simulated and synthesised with the
open-source toolchain described on slides 63–64 of the deck.

## Prerequisites

| Tool | Purpose | Install (Ubuntu / WSL) |
|---|---|---|
| Icarus Verilog ≥ 11 | compile and simulate | `sudo apt install iverilog` |
| GTKWave | view `.vcd` waveforms | `sudo apt install gtkwave` |
| Yosys ≥ 0.30 | synthesise to gates | `sudo apt install yosys` |
| Graphviz (optional) | render Yosys schematics | `sudo apt install graphviz` |
| Java 17+ (optional) | run Logisim-Evolution | `sudo apt install default-jre` |

macOS: `brew install icarus-verilog gtkwave yosys graphviz temurin`
Windows: use WSL2 and follow the Ubuntu column, or install the OSS CAD Suite.

Verify before the lab — each of these must print a version:

```bash
iverilog -V | head -1
vvp -V      | head -1
gtkwave --version | head -1
yosys -V
```

## Quick start

```bash
cd Topic3_Lab
./scripts/run_all.sh      # compile + simulate every design; all should PASS
./scripts/synth_all.sh    # synthesise every design; all should report no latches
gtkwave fsm.vcd &         # look at the 1011 detector
```

## What is here

### `rtl/` — the designs

| File | Topic | What it shows |
|---|---|---|
| `half_adder.v` | 3b | S = A⊕B, C = A·B — and why it is not enough on its own |
| `full_adder.v` | 3b | the 3-input cell every adder is tiled from |
| `adder4.v` | 3b | 4-bit ripple carry — correct, compact, and slow by construction |
| `mux4.v` | 3b | 4:1 multiplexer, with the default assignment that prevents a latch |
| `decoder2to4.v` | 3b | binary → one-hot, with an enable |
| `dff.v` | 3c | the reference D flip-flop, asynchronous active-low reset |
| `shift4.v` | 3c | 4-bit SIPO shift register — the `<=` vs `=` demonstration |
| `bcd_counter.v` | 3c | mod-10 synchronous up-counter with enable |
| `seq_detect_1011.v` | 3c | Moore FSM, three-block template, safe default |
| `seq_detect_1011_mealy.v` | 3c | Mealy version — 4 states, asserts one cycle earlier |
| `seq_detect_1011_onehot.v` | 3c | identical behaviour, one-hot encoded (5 FFs instead of 3) |
| `broken_latch.v` | 3b | **deliberately wrong** — exists so you can see `$_DLATCH_` in a report |

### `tb/` — self-checking testbenches

Every testbench prints `PASS` or `FAIL` and dumps a `.vcd`. They are
self-checking on purpose: a testbench you have to read a waveform to grade is
a testbench that will not catch a regression.

| File | Covers |
|---|---|
| `tb_comb.v` | half adder (4 rows), MUX (64 combinations), decoder (enabled and disabled) |
| `tb_full_adder.v` | all 8 input cases, with a printed truth table |
| `tb_adder4.v` | all 512 combinations of a, b and cin |
| `tb_sequential.v` | flip-flop edge behaviour, 4-cycle shift latency, BCD wrap and enable |
| `tb_seq_detect.v` | Moore and Mealy on the same stream — expects exactly 2 overlapping hits |

### `scripts/`

| File | What it does |
|---|---|
| `run_all.sh` | compiles and runs all five simulations, reports pass/fail |
| `synth_all.sh` | synthesises every design and checks that **no latches** were inferred |
| `synth.ys` | the Tutorial T4 Yosys script: synthesise the FSM, map to gates, dump the netlist |

## Expected results

`./scripts/run_all.sh`

```
=== comb ===        PASS - half_adder, mux4 and decoder2to4 all correct
=== full_adder ===  PASS - all 8 cases correct
=== adder4 ===      PASS - all 512 combinations correct
=== sequential ===  PASS - dff, shift4 and bcd_counter all behaved correctly
=== fsm ===         PASS - both detectors found exactly two overlapping matches
ALL LABS PASSED
```

`yosys -s scripts/synth.ys` on the Moore FSM gives **18 cells: 3 D flip-flops
(the 3-bit state register) plus 15 combinational cells, and zero latches.**

## Experiments worth doing

1. **Break the shift register.** In `shift4.v` change `<=` to `=`, re-run
   `synth_all.sh`, and count the flip-flops. The blocking version collapses to
   one flip-flop, because `q[1]` is updated before `q[2]` reads it.

2. **See a latch.** Synthesise `broken_latch.v` and find `$_DLATCH_N_` and
   `$_DLATCH_P_` in the cell list. Add a default assignment at the top of each
   `always` block and watch both disappear.

3. **Change the state encoding.** Compare `seq_detect_1011.v` (binary) with
   `seq_detect_1011_onehot.v`. The only difference is the
   `(* fsm_encoding = "one-hot" *)` attribute:

   | Version | Cells | Flip-flops |
   |---|---|---|
   | binary | 18 | 3 |
   | one-hot | 14 | 5 |

   More registers, less combinational logic — exactly the trade-off described
   on slide 54.

4. **Find out why Yosys will not extract this FSM.** Run
   `yosys -p "read_verilog rtl/seq_detect_1011.v; hierarchy -top seq_detect_1011; proc; opt; fsm_detect"`
   and read the message: *"Circuit seems to be self-resetting."* The `default:
   next = S0;` branch that makes the FSM **safe** is exactly what stops the tool
   re-encoding it. Delete that line, re-synthesise, and the tool now extracts
   and one-hot-encodes it by itself. Safety and automatic optimisation pull in
   opposite directions here — a real engineering trade-off, not a tool bug.

5. **Look at the schematic.**
   ```bash
   yosys -p 'read_verilog rtl/seq_detect_1011.v; proc; opt; show -format dot -prefix fsm'
   dot -Tpng fsm.dot -o fsm.png
   ```
