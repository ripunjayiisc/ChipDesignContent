# Module 2 · Topic 2 — RTL Design Methodology · Lab

NOS **NIE/ELE/N0102**. Covers the practical side of the three syllabus bullets:
basics of register transfer level design; the RTL design process and
methodology; and an introduction to HDLs such as Verilog or VHDL.

## Quick start

```bash
cd Topic2_Lab
# what RTL is
make transfer    # what "register transfer level" literally means
make ladder      # one adder at four levels of abstraction, all simulated
make prove       # formal proof that those levels are the same circuit
make mux         # one function, three coding styles, measured and proved
# what synthesises, and what bites
make subset      # which Verilog constructs actually synthesise
make mismatch    # when simulation and silicon disagree
make pitfalls    # the inferred latch and the blocking-assignment trap
make lint        # the RTL coding rules, checked by a tool
make lintcheck   # and cross-checked against what Yosys actually builds
# how real blocks are structured
make fsm         # Moore vs Mealy, state encoding, a controller with a timer
make dpctrl      # datapath + controller, the shape of almost every block
make reuse       # parameters, hierarchy and generate: from module to IP
# the flow
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
| Assign every output on every path | `make pitfalls` |
| `<=` in clocked blocks, `=` in combinational ones | `make pitfalls` |
| Write state machines in the three-block form | `make fsm` |
| Separate what holds data from what decides | `make dpctrl` |
| Parameterise once instead of copying fourteen times | `make reuse` |
| Lint before you simulate | `make lint`, `make lintcheck` |
| An HDL is a notation, not a religion | `make langs` |
| A flow is a sequence of gates, not a picture | `make flow` |

## What is in here

```
rtl/transfer.v         four registers and the transfers between them - the
                       definition of RTL, made watchable
rtl/counter.v          the design the whole flow runs on
rtl/tb_counter.v       its testbench
rtl/counter4.v         THE RUNNING EXAMPLE - a 4-bit counter with async reset,
rtl/tb_counter4.v      enable and terminal count, threaded through the deck,
                       the workbook and three of the labs
rtl/mux4_styles.v      one 4:1 mux written three ways - conditional expression,
rtl/tb_mux4.v          case, if/else - simulated exhaustively and proved equal
rtl/datapath_ctrl.v    DATAPATH + CONTROLLER: an accumulator, its FSM, and the
rtl/tb_datapath_ctrl.v control/status bundles between them
rtl/reuse.v            parameters, hierarchy and generate: preg, counter_n,
rtl/tb_reuse.v         delayline (a generate loop) and a two-instance prescaler

fsm/traffic.v          a Moore traffic-light controller in the three-block form
fsm/tb_traffic.v       with two safety properties checked on every cycle
fsm/seq101_moore.v     the '101' detector, Moore and Mealy, plus the same Moore
fsm/seq101_mealy.v     machine one-hot encoded instead of binary
fsm/seq101_moore_onehot.v
fsm/tb_seq101.v        all three against one golden model
fsm/tb_seq101_trace.v  a bare trace, in the format the VHDL twin prints

pitfalls/shift_nb.v    the same three lines with <= and with =, and what each
pitfalls/shift_bl.v    one actually builds
pitfalls/tb_shift.v

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
scripts/stat.sh        synthesise one module, report cells and flip-flops
scripts/mux.sh         three coding styles: simulated, proved, measured
scripts/subset.sh      the synthesisable-subset table
scripts/pitfalls.sh    the latch trap and the blocking trap, both measured
scripts/lint_check.sh  linter vs synthesiser, on latch inference
scripts/fsm.sh         Moore/Mealy/one-hot, simulated and synthesised
scripts/dpctrl.sh      the accumulator, and its hierarchy in the netlist
scripts/reuse.sh       generate at four depths, flip-flops counted
scripts/two_languages.sh   Verilog and VHDL, diffed - counter and FSM
scripts/flow.sh        the seven-stage flow

vhdl/counter.vhd       the same counter, in VHDL
vhdl/tb_counter.vhd    its testbench, printing the same lines
vhdl/seq101_moore.vhd  the same state machine, in VHDL, with a real enumerated
vhdl/tb_seq101.vhd     state type - the place the two languages differ most
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

### One function, three coding styles — `make mux`

A 4:1 multiplexer as a conditional expression, as a `case`, and as an
`if/else` chain. All 64 input patterns simulated, and both pairs proved
equivalent by SAT. Then synthesised:

| style | cells |
|---|---|
| `mux4_assign` — `sel[1] ? (sel[0] ? ... )` | **3** |
| `mux4_if` — `if (sel == 2'b00) ...` | 6 |
| `mux4_case` — `case (sel)` with a `default` | 10 |

The usual claim is that the optimiser flattens the difference. On Yosys 0.33
it does not: the conditional expression uses `sel[1]` and `sel[0]` directly as
mux selects, while the other two ask the tool to build equality comparators
and then re-derive that those comparisons *are* the select bits.

Two lessons, and the second is the important one. **Equivalent is not
identical** — formal equivalence tells you the function matches and says
nothing about area or timing. And **measure your own tool**: folklore about
what optimisers do is the least reliable knowledge in this field.

### The two pitfalls that cost beginners the most time — `make pitfalls`

**Blocking assignment in a clocked block.** The same three lines, written with
`<=` and with `=`:

```
  cycle  din   q_nb  q_bl   expected q[2]
      2    0   100   000         1
      4    1   001   111         0
      6    0   110   000         1

  non-blocking version : 0 wrong cycles
  blocking version     : 6 wrong cycles
```

| module | cells | flip-flops |
|---|---|---|
| `shift_nb` (non-blocking) | 3 | **3** |
| `shift_bl` (blocking) | 1 | **1** |

Three flip-flops against one. The blocking version did not build a slower or
buggier shift register — it built a *different circuit*, and no tool warned
about it, because nothing illegal was written.

**The inferred latch.**

| module | cells | latch? |
|---|---|---|
| `s03_latch` — `if` with no `else` | 1 | **1 latch inferred** |
| `s14_latch_case` — `case` with no `default` | 9 | **1 latch inferred** |
| `mux4_case` — has a `default` | 10 | none |
| `mux4_if` — has a final `else` | 6 | none |

"Assign every output on every path" is not a style preference. The first two
rows are what happens when you break it.

### State machines — `make fsm`

The `'101'` sequence detector, written Moore and Mealy, driven with one
17-bit stream and checked against a golden model computed from the stream
itself rather than from either machine:

```
  matches in the stream : 5
  mismatches vs golden  : 0
  PASS - same language, Moore trails Mealy by one cycle,
         and the one-hot encoding is indistinguishable
```

Mealy asserts in the **same** cycle as the third bit; Moore asserts one cycle
later, every time, without exception. That single cycle — against a Moore
output that is a clean function of a registered value — *is* the Moore/Mealy
decision.

| machine | cells | flip-flops |
|---|---|---|
| `seq101_moore`, binary encoded | 13 | 2 |
| `seq101_moore`, one-hot encoded | **30** | **4** |
| `seq101_mealy`, binary encoded | 14 | 2 |

Read that table before repeating the folklore. On this generic gate library
one-hot is *bigger*, not smaller: four states need four flip-flops instead of
two, and the next-state logic drives four bits instead of two. One-hot pays
off on an FPGA, where a flip-flop beside each lookup table is free and the win
is the short decode path, and on machines with many states, where binary
decoding grows faster than the extra registers do.

The Moore traffic-light controller (`fsm/traffic.v`, 75 cells, 10 flip-flops)
adds a datapath timer to the state machine and has two safety properties
checked on **every** cycle of the run — the roads are never both green, and a
green never goes straight to red. 40 cycles, 0 violations.

### Datapath and controller — `make dpctrl`

An accumulator that sums N samples on a start/done handshake, split the way
almost every real block is split:

| module | cells | flip-flops |
|---|---|---|
| `accum_ctrl` (the controller) | **10** | 2 |
| `accum_datapath` (the datapath) | **145** | 24 |
| `accum_top` (both) | 156 | 26 |

The controller is a handful of gates; the datapath is nearly all of the area.
That ratio is the reason the two are kept apart — you re-time and re-width the
expensive half without touching the half that decides.

### From module to IP — `make reuse`

`delayline #(W=8, N)` is one `generate` loop. Synthesised at four depths:

| N | cells | flip-flops |
|---|---|---|
| 1 | 8 | 8 |
| 2 | 16 | 16 |
| 4 | 32 | 32 |
| 8 | 64 | 64 |

Eight flip-flops per stage, exactly N stages, and no loop anywhere in the
netlist. `generate` is an instruction to the elaborator, not a construct that
survives into hardware. The same run checks that `counter_pair` — the same
`counter_n` module instantiated twice with different width parameters —
divides by exactly 16.

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
    ---- default-assignment idiom ----
  traffic                  no latch       no latch       agree
  seq101_moore             no latch       no latch       agree
  accum_ctrl               no latch       no latch       agree
  mux4_case                no latch       no latch       agree
  ... 16 files, 0 disagreements
```

The second half of that table is the interesting half. Those modules all use
the **default-assignment idiom** — every output written unconditionally at the
top of the block, then an `if` or `case` that need not cover every branch. A
naive latch rule flags all of them; Yosys builds a latch in none of them. L005
and L006 therefore have to understand the idiom, and the table is the evidence
that they do. A linter that cries wolf gets switched off, which makes it worse
than no linter at all.

### Two languages — `make langs`

Two designs, each written in both languages, run through two different
simulators (Icarus and GHDL) and diffed:

* the counter — **identical over all 18 cycles**, wrap and terminal count
  included;
* the Moore `'101'` detector — **identical over all 17 cycles**, detections
  included.

The state machine is the one worth studying, because it is where the two
languages genuinely differ:

```
  Verilog:  localparam [1:0] S_IDLE = 2'd0, ...   a number
  VHDL:     type state_t is (S_IDLE, S_1, ...)    a type
```

The VHDL version cannot be assigned an illegal state — the analyser rejects
it, and it also rejects a non-exhaustive `case`. The Verilog version can be
assigned `2'd7` and nobody complains until silicon. That is the trade in one
sentence: VHDL catches more mistakes at compile time and costs more
keystrokes; Verilog is faster to write and trusts you more than it should.

### The flow — `make flow`

Seven stages on `rtl/counter.v`: spec → lint → RTL simulation → synthesis →
gate-level simulation → transcript comparison → formal proof. Synthesis
produced 12 cells; the RTL and gate transcripts were identical on all 18
cycles; and equivalence was **proven by induction** over 5 equivalence points,
which covers every input sequence rather than the 18 that were tested.

## Honest limits of this lab

* `tools/rtl_lint.py` is a few hundred lines of regular expressions, not a
  Verilog parser. It reads code the way a careful reviewer skims it and can be
  fooled by unusual formatting. Building this lab found three false positives
  in it — `always @(*)` reported as a hand-written sensitivity list, the
  default-assignment idiom reported as a latch, and two modules in one file
  sharing a signal name reported as two drivers. All three are fixed, and
  `make lintcheck` is what keeps the latch rules honest. For real work use `verilator --lint-only` or a
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
