# Module 2 · Topic 2 — RTL Design Methodology · Lab

NOS **NIE/ELE/N0102**. Covers the practical side of the three syllabus bullets:
basics of register transfer level design; the RTL design process and
methodology; and an introduction to HDLs such as Verilog or VHDL.

## Quick start

```bash
cd Topic2_Lab
make transfer    # what "register transfer level" literally means
make ladder      # one adder at four levels of abstraction, all simulated
make prove       # formal proof that those levels are the same circuit
make subset      # which Verilog constructs actually synthesise
make mismatch    # when simulation and silicon disagree
make lint        # the RTL coding rules, checked by a tool
make lintcheck   # and cross-checked against what Yosys actually builds
make langs       # the same design in Verilog and in VHDL, both run
make flow        # the whole methodology, executed: spec to formal proof
make             # all of the above
```

```bash
sudo apt install yosys iverilog gtkwave python3    # everything except make langs
sudo apt install ghdl                              # only needed for make langs
```

## What this lab is for

Methodology is the hardest thing to teach, because the honest version of it is
a list of habits and the dishonest version is a list of slogans. Every habit
below is therefore attached to something you can run, and something that can
fail.

| Habit | What makes it real here |
|---|---|
| Write at the highest level that says what you mean | `make ladder` + `make prove` |
| Know the synthesisable subset | `make subset` — eleven constructs, measured |
| Never trust a sensitivity list you maintain by hand | `make mismatch` |
| Lint before you simulate | `make lint`, `make lintcheck` |
| An HDL is a notation, not a religion | `make langs` |
| A flow is a sequence of gates, not a picture | `make flow` |

## What is in here

```
rtl/transfer.v         four registers and the transfers between them - the
                       definition of RTL, made watchable
rtl/counter.v          the design the whole flow runs on
rtl/tb_counter.v       its testbench

ladder/fa_behav.v      THE ABSTRACTION LADDER, one full adder, four ways:
ladder/fa_dataflow.v     behavioural -> dataflow -> gate -> switch
ladder/fa_gate.v
ladder/fa_switch.v     down to individual pmos/nmos transistors
ladder/fa_broken.v     a full adder with one carry term missing, so that the
                       equivalence checker has something to fail on
ladder/tb_ladder.v     runs all four together, exhaustively

subset/s01..s14.v      one Verilog construct each: which synthesise, which
                       are refused, and which quietly build something you did
                       not ask for
subset/tb_mismatch.v   the RTL and its own netlist, disagreeing

tools/rtl_lint.py      seven RTL coding rules, checked
scripts/equiv.sh       prove two descriptions are the same circuit
scripts/subset.sh      the synthesisable-subset table
scripts/lint_check.sh  linter vs synthesiser, on latch inference
scripts/two_languages.sh   Verilog and VHDL, diffed
scripts/flow.sh        the seven-stage flow

vhdl/counter.vhd       the same counter, in VHDL
vhdl/tb_counter.vhd    its testbench, printing the same lines
```

## Measured results

Everything quoted in the slides and the workbook comes from these runs.

### The abstraction ladder — `make ladder`, `make prove`

All four descriptions agree on all 8 input patterns — exhaustive, since a full
adder has only three inputs. Then, because exhaustive testing stops being
possible at around 30 inputs, the same claim is **proved**:

| pair | result |
|---|---|
| `fa_behav` vs `fa_dataflow` | EQUIVALENT (proved, 94 SAT variables) |
| `fa_behav` vs `fa_gate` | EQUIVALENT (proved, 94 SAT variables) |
| `fa_dataflow` vs `fa_gate` | EQUIVALENT (proved, 100 SAT variables) |
| `fa_behav` vs `fa_broken` | **NOT EQUIVALENT** — as it must be |

`fa_broken` is wrong for exactly one input pattern in eight. A random test
could miss it; the solver cannot.

### What synthesis makes of each level

| level | synthesis | cells |
|---|---|---|
| behavioural | OK | **5** — `$_NAND_` ×3, `$_XOR_` ×2 |
| dataflow | OK | 6 |
| gate | OK | 6 — *identical netlist to dataflow* |
| switch | **REFUSED** | transistor primitives are not synthesisable |

Two things worth stopping on. The **behavioural** description produced the
*smallest* circuit, because it left the tool free to choose the Boolean form.
And **dataflow and gate produced the identical netlist** — once you have
written the Boolean expression you have already committed to the structure, and
naming the gates adds nothing but typing.

That is the argument for writing at the highest level that expresses your
intent: every level you descend takes a decision away from the tool and gives
it to you, whether or not you wanted it.

### The synthesisable subset — `make subset`

| construct | synth | cells | latch | what the tool said |
|---|---|---|---|---|
| `s01_ok_comb` | OK | 10 | no | clean |
| `s02_ok_seq` | OK | 8 | no | `SDFF_PP0` ×8 |
| `s03_latch` | OK | 1 | **YES** | inferred a LATCH: `$_DLATCH_P_` |
| `s04_incomplete_sens` | OK | 1 | no | `AND` ×1 — built despite the list |
| `s05_delay` | OK | 1 | no | `NOT` ×1 — the `#5` silently vanished |
| `s06_initial` | OK | 10 | no | accepted (FPGA-style init) |
| `s07_forloop` | OK | 7 | no | unrolled into 7 XOR gates |
| `s08_whileloop` | **REFUSED** | – | – | "While loops are only allowed in constant functions!" |
| `s09_real` | **REFUSED** | – | – | "syntax error, unexpected TOK_REAL" |
| `s10_divide` | OK | **371** | no | divide by a *variable* |
| `s11_shift` | OK | **0** | no | divide by a constant power of two — just wires |

371 cells against 0, for the same operator. The difference is entirely in what
you divided by.

### Simulation vs silicon — `make mismatch`

`s04_incomplete_sens` is the row that matters most, because it is the only one
that fails *silently*. The RTL and the netlist Yosys produced from it were
driven with identical stimulus:

```
   change b  (list ASLEEP)    a=1 b=1    RTL y=0    NETLIST y=1   <-- THEY DISAGREE
   disagreements: 1 of 6
```

The testbench was verifying a circuit that will never be built. That is worse
than an error, because an error stops you.

### The linter, and whether to believe it — `make lint`, `make lintcheck`

Seven rules, each firing on a file written to break it and on none of the files
written correctly. Rules L005 and L006 claim a missing `else` or a missing
`default` infers a latch — a claim about what a synthesiser will do, so the
synthesiser settles it:

```
  file                     linter says    yosys says     verdict
  s03_latch                latch          latch          agree
  s14_latch_case           latch          latch          agree
  ... 10 files, 0 disagreements
```

### Two languages — `make langs`

The same counter in Verilog and VHDL, run through two different simulators
(Icarus and GHDL), transcripts diffed: **identical over all 18 cycles**,
including the wrap and the terminal count.

### The flow — `make flow`

Seven stages on `rtl/counter.v`: spec → lint → RTL simulation → synthesis →
gate-level simulation → transcript comparison → formal proof. Synthesis
produced 12 cells; the RTL and gate transcripts were identical on all 18
cycles; and equivalence was **proven by induction** over 5 equivalence points,
which covers every input sequence rather than the 18 that were tested.

## Honest limits of this lab

* `tools/rtl_lint.py` is a few hundred lines of regular expressions, not a
  Verilog parser. It reads code the way a careful reviewer skims it and can be
  fooled by unusual formatting. For real work use `verilator --lint-only` or a
  commercial linter; the point of this one is that you can read all of it in an
  afternoon, and that its latch rules are cross-checked against Yosys rather
  than asserted.
* The gate counts come from Yosys' generic cell library, not a foundry library.
  They are good for comparing designs against each other and meaningless as
  absolute area figures.
* `fa_switch.v` is a *functional* transistor model. Icarus resolves the
  strengths correctly, which is enough to show the ladder reaches the bottom,
  but it is not a circuit simulation — there are no threshold voltages, no
  capacitances and no analogue behaviour of any kind. SPICE is the tool for
  that, and it is out of scope here.
* Yosys accepts `initial` blocks because it targets FPGAs, where the bitstream
  really does initialise the flops. An ASIC flow would not. This is flagged in
  `s06_initial.v` because it is a genuine trap: code that works on an FPGA and
  fails on an ASIC.
* Vivado and ModelSim, the tools the syllabus names, are not installed in the
  environment these materials were built in. Every result above came from the
  free toolchain. The deck shows the equivalent Vivado commands and labels them
  as not executed here.
