# Module 3 · Topic 1 — Overview of VLSI STA · Lab

NOS **NIE/ELE/N0103**. This lab covers the practical half of the subtopic:
races and hazards in combinational circuits, setup and hold in sequential
circuits, maximum frequency of operation, timing constraints for synthesis,
and what synthesis does to all of it.

## Quick start

```bash
cd Topic1_Lab
make analyse    # find hazards in a two-level cover, and prove the fix
make glitch     # gate-level simulation: watch the glitch, and watch it go
make capture    # what a glitch does to a flop as data / as clock / as reset
make synth      # what synthesis does to a hazard fix (it deletes it)
make fmax       # Fmax of an unbalanced pipeline, and of a balanced one
make setup      # a real setup violation at 400 MHz, and its fix
make hold       # a hold violation, and why the clock period cannot help
make            # all of the above
```

Needs `yosys`, `iverilog` and `python3`. Nothing else. See the deck's
installation section, or:

```bash
sudo apt install yosys iverilog gtkwave python3 python3-matplotlib
```

## Why hazards get a lab of their own

Module 2 Topic 6 taught static timing analysis, and STA is *static*: it
measures how long each path is and never asks what the values are. A hazard
is the opposite kind of question. It is not about one path being too long —
it is about two paths of **different** length reconverging, so that the
output passes through a wrong value on its way to the right one.

That means **STA cannot see a hazard.** Run `sta/sta.py` on `hz_static1.v`
and every path meets timing, because every path does meet timing. The glitch
is still there. Only a dynamic simulation with delays shows it, which is what
`make glitch` does.

This is the single most important idea in the topic, and it is why the lab
uses two different tools on the same circuit.

## What is in here

```
tools/hazard.py        THE ANALYSER. Reads a two-level cover, finds every
                       static logic hazard, prescribes the redundant term
                       that removes it, then proves the fix works and did
                       not change the function.
                       Run  python3 tools/hazard.py --selftest

hazards/hz_static1.v      F = A B' + B C          - the textbook hazard
hazards/hz_static1_fix.v  + the consensus term A C - clean
hazards/hz_none.v         a control: no hazard anywhere
hazards/hz_dynamic.v      the static hazard feeding an XOR - 5 glitches
hazards/hz_dynamic_fix.v  consensus term added     - 4 glitches, not 0
hazards/hz_flat_fix.v     flattened and re-covered - clean
hazards/tb_hazard.v       THE DETECTOR. Walks every single-variable input
                          transition, counts output changes against how many
                          there should be, and records the settled truth
                          table so a "fix" cannot quietly change the function.
hazards/glitch_capture.v  one glitchy signal, three consumers
hazards/tb_glitch_capture.v

rtl/pipe_unbal.v       a 4-stage pipeline with one very heavy stage
rtl/pipe_bal.v         the same work, heavy stage split in two
rtl/hold_demo.v        two flops back to back - the shape of every hold bug
rtl/hz_rtl.v           the hazard example written as RTL, for make synth

constraints/pipe.sdc            a full constraint set, in the right order
constraints/hold_skew.sdc       0.25 ns of skew on one capture register
constraints/hold_skew_fixed.sdc the same after the tree was rebalanced

sta/liberty.py         Liberty reader        \  reused unchanged from
sta/sta.py             the timing analyser   /  Module 2 Topic 6
lib/cda_edu.lib        the 14-cell teaching library

vivado/zynq_sta.tcl    the same flow on xc7z020 (Zynq-7000), headless
vivado/zynq.xdc        the timing constraints above, in Xilinx syntax
```

## Measured results

Everything quoted in the slides and the workbook comes from these runs.

### Hazards — `make glitch`

| design | truth table | detector result |
|---|---|---|
| `hz_static1` | `10111000` | 1 glitch: ABC 111→101, static |
| `hz_static1_fix` | `10111000` | CLEAN |
| `hz_none` | `11100000` | CLEAN |
| `hz_dynamic` | `01110100` | 5 glitches: 4 static, 1 dynamic |
| `hz_dynamic_fix` | `01110100` | 4 glitches — dynamic gone, static remain |
| `hz_flat_fix` | `01110100` | CLEAN |

Identical truth signatures within a family prove each fix left the function
alone. The detector examines 24 transitions per design.

**Read `hz_dynamic_fix` carefully — it is the most instructive row.** Adding
the consensus term removed the dynamic hazard and left four static ones,
because those have a different cause: with A=0,C=1 the sub-expression
collapses to a *delayed copy of B*, so `f = s XOR B` computes `B XOR
B-delayed` and spikes on every edge. That is reconvergent fanout, and no
redundant product term can repair it. `hz_flat_fix.v` fixes it structurally
instead. "Add the consensus term" cures a two-level logic hazard, and only
that.

### Does a glitch matter? — `make capture`

One glitchy signal, four glitches, three consumers:

| consumer | result |
|---|---|
| `f` as **data**, sampled by a clean clock | correct — the glitch is never seen |
| `f` as a **clock** | 4 spurious clock edges |
| `f` as an **asynchronous reset** | the flag was cleared |

The glitch was placed 80 ns before any clock edge — the friendliest possible
case for "synchronous design tolerates glitches". It is true for the first
row and false for the other two.

### Synthesis — `make synth`

| RTL written | cells | gates |
|---|---|---|
| `f = a&~b \| b&c` | 1 | `$_MUX_` |
| `f = a&~b \| b&c \| a&c` (hazard-fixed) | 1 | `$_MUX_` |

The netlists are **identical**: the consensus term was deleted, because
deleting redundancy is exactly what an optimiser is for. And what it built
was a multiplexer — `A B' + B C` is precisely `B ? C : A`.

### Sequential timing — `make fmax`, `make setup`, `make hold`

| experiment | result |
|---|---|
| `pipe_unbal` Fmax | 364.7 MHz |
| `pipe_bal` Fmax | 473.2 MHz |
| `pipe_unbal` at 400 MHz | WNS −0.322 ns VIOLATED |
| `pipe_bal` at 400 MHz | WNS +0.307 ns MET |
| `hold_demo`, period 4 / 40 / 400 ns | −0.119 ns in **all three** |
| `hold_demo`, skew 0.25 → 0.10 ns | −0.119 → +0.031 ns |

Two results worth stopping on. Splitting one heavy stage moved the design
from failing to passing at 400 MHz — Fmax is set by one stage, not by the
average. And the hold slack is *identical* at 4 ns and at 400 ns: a hundred-
fold change in clock frequency, no change at all in the violation. The clock
period is not in the hold equation.

## Honest limits of this lab

* The delay numbers in `lib/cda_edu.lib` are invented, not any vendor's. They
  are chosen to be plausible and, more importantly, to be checkable by hand.
* The gate delays in the `hazards/*.v` files are chosen to make the glitch
  wide enough to see. A real 7 nm inverter is not 4 ns. The *mechanism* is
  real; the timescale is teaching-sized.
* `sta/sta.py` is reused unchanged from Module 2 Topic 6. It is a teaching
  analyser: a straight-line delay model, no slew propagation, no wire RC, one
  corner at a time. What it demonstrates about arrival, required and slack is
  exactly what PrimeTime demonstrates.
* `vivado/zynq_sta.tcl` has not been executed in the environment these
  materials were built in — Vivado is not installable there. It is written
  against the documented command set and is the one file in this lab whose
  output is not reproduced above. Run it and tell us what you get.
