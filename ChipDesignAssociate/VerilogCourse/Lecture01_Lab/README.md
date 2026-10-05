# Lecture 01 — Introduction · Lab

Five labs that check, on your own machine, what Lecture 01 asserts.

The lecture's central claim is that **a CAD tool transforms its HDL input into
an HDL output that contains more detailed information about the hardware** —
without changing what the circuit does. Lab 2 tests exactly that, in about
thirty seconds.

## Tools

| Tool | Why | Install (Ubuntu/Debian) |
|------|-----|-------------------------|
| Icarus Verilog | simulate Verilog | `sudo apt install iverilog` |
| GTKWave | view waveforms | `sudo apt install gtkwave` |
| Yosys | synthesis | `sudo apt install yosys` |
| GHDL | simulate VHDL | `sudo apt install ghdl` |

macOS: `brew install icarus-verilog yosys ghdl` and
`brew install --cask gtkwave`.
Windows: `wsl --install`, then follow the Ubuntu line inside Ubuntu.

Everything here was produced with Icarus 12.0, Yosys 0.33 and GHDL 4.1.0.
Newer versions are fine; a newer synthesiser may report slightly different
cell counts, which is itself worth discussing.

## Targets

```
make sim        Lab 1  simulate the counter, write out/counter4.vcd
make wave       Lab 1  open that waveform in GTKWave
make transform  Lab 2  print the design at three levels - all three Verilog
make prove      Lab 2  run the same test bench against the gate netlist
make ladder     Lab 3  count the cells at each level of the design flow
make target     Lab 4  compare the ASIC mapping with the FPGA mapping
make langs      Lab 5  run the same design in Verilog and in VHDL
make all        everything, in order
make clean      remove out/
```

## What each lab shows

**Lab 1 — simulation.** A ten-line behavioural counter and a self-checking
test bench. Prints `PASS` and writes a waveform.

**Lab 2 — the transformation, and that it is faithful.** `make transform`
prints the design as you wrote it, as Yosys re-wrote it at RTL, and as Yosys
mapped it to gates. All three are Verilog. `make prove` then runs the *same*
test bench against the gate netlist and diffs the two waveforms:

```
IDENTICAL - 22 transitions, same value at the same time.
The synthesiser changed the DESCRIPTION, not the BEHAVIOUR.
```

**Lab 3 — the ladder, in numbers.**

| Level | Cells | What they are |
|---|---|---|
| Behavioural source | — | 10 lines of Verilog |
| Data path (RTL) | 2 | 1 adder, 1 four-bit register |
| Logic, for an ASIC | 10 | 4 flip-flops + AND, NAND, NOT, XNOR, XOR ×2 |
| Logic, for an FPGA | 8 | 4 flip-flops + 4 look-up tables |

**Lab 4 — ASIC against FPGA.** The same source, two targets. The flip-flops
are identical; the combinational logic becomes six dedicated gates or four
look-up tables.

**Lab 5 — two languages.** The counter in Verilog and in VHDL, on identical
stimulus. They agree on all 20 transitions after reset. They differ only at
time zero, because a Verilog `reg` reads `x` until something drives it while
the VHDL signal was declared with an initial value — a real difference worth
teaching, not a bug.

## Layout

```
rtl/counter4.v            the design, written behaviourally
rtl/tb_counter4.v         the test bench
vhdl/counter4.vhd         the same design in VHDL
vhdl/tb_counter4.vhd      the VHDL test bench
scripts/level1_rtl.ys     behaviour -> RTL netlist
scripts/level2_gates.ys   behaviour -> gate netlist
scripts/fpga_luts.ys      behaviour -> 4-input LUTs
scripts/stat.sh           extract only the FINAL yosys statistics block
scripts/ladder.sh         Lab 3
scripts/asic_vs_fpga.sh   Lab 4
scripts/prove_equivalence.sh  Lab 2, step 2
scripts/compare_languages.sh  Lab 5
scripts/vcd_q.py          print one signal from a VCD, normalised to ns
out/                      everything the labs produce
```

## Two details that are easy to get wrong

**Reading yosys statistics.** Yosys prints a statistics block every time `stat`
runs, and a script may run it more than once. Only the **last** block describes
the finished netlist — which is why `scripts/stat.sh` extracts just that one.

**Comparing two VCD files.** Icarus and GHDL use different timescales and
different identifier codes, so the raw files cannot be diffed.
`scripts/vcd_q.py` normalises both. It keeps time as whole femtoseconds
(floating-point nanoseconds compare unreliably across timescales) and applies
VCD's left-extension rule properly: a vector pads on the left with `0`, except
that a value beginning `x` or `z` extends with that character — so an unknown
4-bit value reads `xxxx`, not `000x`.
