# Module 2 · Topic 5 — RTL Simulation and Verification · Lab Sources

The practical programme for Topic 5. One device under test, five deliberately
broken copies of it, six testbenches of increasing strength, and the scripts
that turn them into a regression.

Everything here has been compiled, linted, simulated and — where the tool
supports it — checked with assertions, using the open-source toolchain. The
Vivado and ModelSim scripts are working templates; see *A note on the vendor
tools* at the end.

## The idea

Topic 4 taught you to write RTL. Topic 5 asks a harder question:

> **How do you know it works?**

The answer is not "the simulation passed". A testbench that passes proves
nothing unless it would have *failed* had the design been wrong. So this lab is
built the other way round: the broken designs come first, and each stage of the
testbench is judged by how many of them it catches.

| | `fifo` | `fifo_b1` | `fifo_b2` | `fifo_b3` | `fifo_b4` | `fifo_b5` | bugs caught |
|---|---|---|---|---|---|---|---|
| **V1** naive directed | pass | pass | pass | pass | pass | pass | **0 / 5** |
| **V2** model + corners | pass | CAUGHT | CAUGHT | CAUGHT | CAUGHT | pass | **4 / 5** |
| **V3** constrained-random | pass | CAUGHT | CAUGHT | CAUGHT | CAUGHT | CAUGHT | **5 / 5** |

Reproduce it yourself with `./scripts/clinic.sh`. Every cell above is real
output from this code.

## Prerequisites

| Tool | Purpose | Install (Ubuntu / WSL) |
|---|---|---|
| Icarus Verilog ≥ 11 | compile and simulate labs V1–V4 | `sudo apt install iverilog` |
| Verilator ≥ 5 | lint, and run lab V6 with assertions | `sudo apt install verilator` |
| GTKWave | view `.vcd` waveforms | `sudo apt install gtkwave` |
| Yosys (optional) | synthesise, to compare with Topic 4 | `sudo apt install yosys` |

macOS: `brew install icarus-verilog verilator gtkwave`
Windows: use WSL2 and follow the Ubuntu column, or the OSS CAD Suite.

The syllabus specifies **Vivado Design Suite** and **ModelSim**; scripts for
both are in `scripts/`.

## Quick start

```bash
cd Topic5_Lab
make lint          # one second - always first
make run           # every lab against the golden FIFO: all PASS
make clinic        # the matrix above. This is the point of Topic 5.
make cover         # coverage across three stimulus profiles, merged
make assert        # assertions vs scoreboard on every broken design
make regress       # multi-seed regression
make waves         # run V3 and open GTKWave with the saved view
```

## What is in here

```
rtl/fifo.v          the device under test. Its header comment IS the
                    specification your testbench is checking.
rtl/fifo_bugs.v     five broken copies. All lint clean, all synthesise, all
                    pass a naive testbench. Do not read the bug list until
                    after you have attempted the clinic.

tb/tb_v1_naive.v      V1  what everybody writes first: a few directed cases
tb/tb_v2_selfcheck.v  V2  a reference model + the boundary cases
tb/tb_v3_random.v     V3  weighted constrained-random, seeded, reproducible
tb/tb_v4_coverage.v   V4  functional coverage, by hand, with a closure verdict
tb/tb_v6_assert.sv    V6  a layered testbench: generator / driver / monitor /
                          scoreboard, with assertions bound alongside
sva/fifo_sva.sv       the specification written as checkable properties

scripts/lint.sh       static checks
scripts/run_all.sh    every lab on the golden design
scripts/clinic.sh     V5 - the debug clinic matrix
scripts/regress.sh    seeds x profiles, with reproduction instructions
scripts/coverage.sh   run three profiles and MERGE the coverage
scripts/assert.sh     which assertion caught which bug, and when
scripts/vivado_sim.tcl, scripts/modelsim_run.do   the vendor flows
wave/v3_fifo.gtkw     a saved GTKWave view, so everyone sees the same picture
```

## The six labs

| Lab | Hours | What you build | What it teaches |
|---|---|---|---|
| **V1** | 3 | A directed testbench with all six structural parts | A testbench is a module with no ports, a clock, stimulus and a verdict. Why passing is not the same as proving. |
| **V2** | 6 | A reference model and the boundary cases | Expected values come from an independent model of the specification, never from the design. Corners are where bugs live. |
| **V3** | 6 | Weighted constrained-random stimulus | Seeds, reproducibility, and finding the corner you did not think of. |
| **V4** | 6 | A functional coverage model, sampled and reported | "What did I actually test?" Coverage holes, and closing them across a regression. |
| **V5** | 5 | The debug clinic | Diagnosing five unknown bugs from symptoms, using waveforms, `$display`, bisection and x-chasing. |
| **V6** | 8 | A layered testbench with SystemVerilog assertions | Separation of generator/driver/monitor/scoreboard. Assertions catch the rule at the cycle it breaks; scoreboards catch what assertions do not describe. |

Thirty-four hours, sitting inside the syllabus practical allocation for
*Simulating and verifying the functionality of RTL designs*.

## Verified results

```
$ ./scripts/lint.sh
LINT CLEAN

$ ./scripts/run_all.sh
=== V1 naive directed            ===   PASS
=== V2 model + corner cases      ===   PASS
=== V3 constrained-random        ===   PASS - seed=1 cycles=3000
=== V4 functional coverage       ===   PASS - all 12 bins covered
=== V6 layered + assertions      ===   PASS - 2027 checks, 895 words in, 895 out
ALL LABS PASSED on the golden FIFO

$ ./scripts/clinic.sh
  V1 : 0 of 5 bugs caught, golden design passes (no false alarm)
  V2 : 4 of 5 bugs caught, golden design passes (no false alarm)
  V3 : 5 of 5 bugs caught, golden design passes (no false alarm)

$ ./scripts/coverage.sh
  writeheavy (wr=90 rd=10)   9 of 12 bins   (never reaches empty)
  readheavy  (wr=10 rd=90)   8 of 12 bins   (never reaches full)
  balanced   (wr=50 rd=50)  12 of 12 bins
  merged: 12 of 12 bins covered (100%)   COVERAGE CLOSED

$ ./scripts/assert.sh
  fifo      passes - correct, this is the golden design
  fifo_b1   CAUGHT by an ASSERTION  - a_full_iff_depth at 205 ns: full=0 but count=8
  fifo_b2   CAUGHT by an ASSERTION  - a_count_range   at 425 ns: count=15 exceeds DEPTH=8
  fifo_b3   CAUGHT by an ASSERTION  - a_step_both     at 545 ns
  fifo_b4   CAUGHT by the SCOREBOARD only - no assertion covers it
  fifo_b5   CAUGHT by an ASSERTION  - a_step_up       at 465 ns
```

Note the fourth line of the assertion run. `fifo_b4` corrupts **data**; the
assertions in `sva/fifo_sva.sv` describe the **control** interface — count,
full, empty. No property is violated, so no assertion fires, and the scoreboard
is what catches it. Assertions and scoreboards are not alternatives; each
covers what the other does not.

## Two bugs found while writing this lab

Both are preserved, because they are better teaching material than anything
invented.

**The reference model applied the write before deciding the read.** The model
originally pushed, then tested `empty` to decide whether to pop. On a
simultaneous read and write to an *empty* FIFO it pushed, observed itself no
longer empty, and popped again — reporting an occupancy of 0 where the hardware
correctly has 1. The golden design "failed"; `fifo_b5`, which really does drop
that write, "passed". A model must sample `full` and `empty` **once**, before
applying either operation, exactly as the hardware does. See `model_cycle` in
`tb/tb_v2_selfcheck.v`.

**`$urandom(seed)` re-seeds on every call.** In V6 the generator called
`$urandom(seed)` inside the loop, which sets the seed each time and therefore
returns the same number for ever. The run looked healthy and reported `PASS`,
but had driven 9 transactions instead of 895. Seed once with
`void'($urandom(seed0))`, then call `$urandom()` with no argument. A random test
that is silently not random is worse than no random test, because it is
believed.

## Experiments worth doing

1. **Break the golden FIFO yourself.** Change one character in `rtl/fifo.v` —
   `~full` to `full`, `<=` to `=`, an index off by one — and run
   `./scripts/clinic.sh`. Which stage catches your bug? Now write a bug that V3
   misses.

2. **Watch a seed reproduce.** Run V3 twice with the same seed and diff the
   transcripts: identical. Change the seed and it is a different run. This is
   the property that makes a random failure debuggable.

3. **Break coverage on purpose.** Run V4 with `+WR=95 +RD=5`. Three bins go
   MISS. Now write directed stimulus that hits exactly those three, and confirm
   the merged report closes.

4. **Delete an assertion.** Comment out `a_step_both` in `sva/fifo_sva.sv` and
   re-run `./scripts/assert.sh`. `fifo_b3` drops from "caught by an assertion"
   to "caught by the scoreboard only" — later, and with a less useful message.

5. **Find the bug from the waveform alone.** Pick one broken FIFO, run V3
   against it, note the failing cycle from the transcript, then open `v3.vcd` at
   that time and work backwards to the first signal that was wrong. That skill,
   not the tool, is what Topic 5 is teaching.

6. **Measure the cost of dumping.** Time `make run` with and without the
   `$dumpvars` line in a testbench. On a long regression, waveform dumping is
   often the single biggest simulation cost — which is why regressions dump
   nothing and only re-run a failing seed with dumping on.

## A note on the vendor tools

`scripts/vivado_sim.tcl` and `scripts/modelsim_run.do` use standard,
version-stable commands (`xvlog`, `xelab`, `xsim`; `vlib`, `vlog`, `vsim`,
`assertion fail`). They were **not** executed while this material was written,
because neither tool is installed in the authoring environment. Check them
against your installed version before the lab session.

Both vendor simulators support the *full* SystemVerilog assertion language,
including the ranged delay forms (`a |-> ##[1:3] b`) that the open-source flow
here cannot handle, and both report assertion and code coverage directly. The
assertions in `sva/fifo_sva.sv` are deliberately written inside the portable
subset so that the same file runs everywhere.

Everything run against Icarus Verilog 12.0 and Verilator 5.020 in this folder
was executed, and the outputs quoted above are real.
