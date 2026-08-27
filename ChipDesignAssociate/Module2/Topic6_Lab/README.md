# Module 2 · Topic 6 — Timing Constraints and Analysis · Lab Sources

The practical programme for Topic 6. A small standard-cell library, a **working
static timing analyser you can read**, and a set of designs whose timing is
deliberately interesting.

Everything quoted below is real output from the code in this folder, produced
by Yosys 0.33, Icarus Verilog 12.0 and Python 3.11. The Vivado script is a
working template — see *A note on the vendor tools*.

## The idea

Topic 5 asked "does it do the right thing?". Topic 6 asks the other half:

> **Does it do it in time?**

Most people meet timing as a report from a tool they cannot see inside, and
never quite believe. So this lab builds the tool. `sta/sta.py` is about 400
lines and it does what a commercial static timing analyser does:

1. read the gate netlist and the cell library,
2. walk the graph forward computing **arrival** times,
3. work out the **required** time at every endpoint from the clock,
4. subtract: **slack = required − arrival**.

Everything else in timing — skew, uncertainty, multicycle paths, false paths —
is a small adjustment to one of those three numbers. Once you have written it,
a vendor timing report stops being mysterious.

## Prerequisites

| Tool | Purpose | Install (Ubuntu / WSL) |
|---|---|---|
| Yosys ≥ 0.30 | synthesise RTL to gates | `sudo apt install yosys` |
| Python ≥ 3.8 | run the analyser | usually already there |
| Icarus Verilog ≥ 11 | prove the optimised designs still work | `sudo apt install iverilog` |

No commercial tool is needed for any lab. The syllabus names **Vivado Design
Suite**; `scripts/vivado_timing.tcl` and `constraints/vivado.xdc` run the same
analysis there.

## Quick start

```bash
cd Topic6_Lab
make lib        # what the analyser reads out of the Liberty file
make stdlib     # regenerate the standards-compliant library (for OpenSTA)
make tiny       # the smallest real path - check the arithmetic by hand
make sweep      # Fmax against adder width, two design styles
make closure    # the headline table
make hold       # a hold violation, then the same design with it fixed
make mcp        # a multicycle constraint turning a violation into a pass
make verify     # prove the optimised adders still add
make            # all of the above
```

## What is in here

```
lib/cda_edu.lib        a small standard-cell library in Liberty format.
                       Readable: 14 cells, one drive strength each, a
                       straight-line delay model. Real ones are the same
                       shape and tens of megabytes.
lib/cda_edu_std.lib    GENERATED. The same 14 cells and the same delay
                       numbers, written in standard Liberty - lookup-table
                       templates, per-pin unateness, ff() groups, setup and
                       hold constraint groups - for tools that will not
                       accept the custom cda_* attributes (OpenSTA,
                       PrimeTime). Rebuild it with `make stdlib`.

sta/liberty.py         a minimal Liberty reader - what the tool sees
sta/sta.py             THE STATIC TIMING ANALYSER. Read this file.

scripts/mklib_std.py   generates lib/cda_edu_std.lib from cda_edu.lib
scripts/checklib_std.py checks the generated file: braces balance, every
                       required group is present, and every delay number
                       matches cda_edu.lib exactly. It does NOT prove
                       OpenSTA will read the file - only OpenSTA can do
                       that, and it is not installed here. If you have it:
                         sta -no_splash -exit -x \
                             'read_liberty lib/cda_edu_std.lib'

rtl/tiny.v             three flops and two gates: hand-checkable
rtl/add_ripple.v       W-bit ripple-carry adder - delay grows LINEARLY with W
rtl/add_ripple_pipe.v  the same, cut in half by a pipeline register
rtl/add_fast.v         "a + b" - the tool chooses the structure
rtl/slow_path.v        a long path captured one cycle in four (multicycle)
rtl/hold_demo.v        two flops, no logic: the shape of every hold violation
rtl/hold_fixed.v       the same, with delay added to the data path
rtl/mac8.v             8x8 multiply-accumulate in one cycle
rtl/mac8_pipe.v        the same, in two stages

constraints/add32.sdc     an ordinary four-line constraint set
constraints/hold_skew.sdc a clock with 0.30 ns of skew on one register
constraints/mcp.sdc       the same clock, plus a multicycle promise
constraints/vivado.xdc    all of it again, in Vivado's syntax

tb/tb_add.v            the optimised adders, checked against a reference
```

## Verified results

### The smallest path, checkable by hand

```
$ make tiny
  Path 1   endpoint q_reg/D  (DFF)
           startpoint p_reg
         incr   arrival   pin
        0.000     0.000   clock edge at p_reg
        0.164     0.164   p_reg/Q                    (DFF)
        0.000     0.164   u97/B                      (XOR2)
        0.117     0.281   u97/Y                      (XOR2)
        0.000     0.281   q_reg/D                    (DFF)
                  0.910   required (period - setup)
                  0.629   SLACK   MET
```

Check it against the library yourself:

| step | from `cda_edu.lib` | value |
|---|---|---|
| DFF clock-to-Q | `0.145 + 0.013 × 1.5` (one XOR2 pin) | 0.1645 |
| XOR2 | `0.088 + 0.018 × 1.6` (one DFF D pin) | 0.1168 |
| **arrival** | | **0.2813** |
| required | `1.000 − 0.090` setup | 0.910 |
| **slack** | | **+0.629** |

The analyser and the arithmetic agree exactly. That is the point of the
exercise: nothing here is magic.

### Delay grows with the shape of the design, not its size

```
$ make sweep

  hand-written carry chain            "a + b", delay-driven mapping
  W    cells  longest   Fmax  ns/bit   W    cells  longest   Fmax  ns/bit
  4       30    0.773   1294  0.1933   4       33    0.831   1203  0.2077
  8       62    1.247    802  0.1559   8       74    1.183    845  0.1479
  16     126    2.196    455  0.1373   16     159    1.547    646  0.0967
  32     254    4.094    244  0.1279   32     332    1.939    516  0.0606
  64     510    7.889    127  0.1233   64     681    2.318    431  0.0362
```

Look at the last column. The ripple adder settles at a constant **0.123 ns per
bit** — every extra bit costs the same, so delay is linear in W and Fmax falls
off a cliff. The adder the tool designed for itself gets *cheaper per bit* as
it grows, because it builds a tree.

At 64 bits the difference is **7.889 ns against 2.318 ns — 3.4×**.

### The headline table

```
$ make closure

                       --- abc default (area) ---  --- abc -fast (delay) ---
  design                  cells  path(ns)     Fmax    cells  path(ns)     Fmax
  ----------------------------------------------------------------------------
  add_ripple                254     4.094      244      254     5.258      190
  add_ripple_pipe           303     2.315      432      303     2.906      344
  add_fast                  268     4.615      217      332     1.939      516
```

This table is the reason the topic exists, and it does **not** say what people
expect it to say.

* `add_ripple` hand-codes the carry chain, so the mapper has almost nothing
  left to decide. Asking for more effort does not help — the structure is
  already committed.
* `add_fast` writes `a + b` and lets the tool choose. Under the **default,
  area-oriented** mapping that is *slower* than the hand-written version.
  Under **delay-oriented** mapping it is more than twice as fast, and the best
  result in the table.
* So "describe intent, not structure" is only half the rule. The other half is
  **"and check what your tool did with it"**. The same RTL is 217 MHz or
  516 MHz depending on one flag.
* Pipelining works regardless of either, because it changes the amount of logic
  between registers rather than the way that logic is built.

Both netlists were checked equivalent to the RTL over 400 random vectors
before those numbers were quoted.

### A hold violation, and its fix

```
$ make hold

  --- two flops, nothing between them, 0.30 ns skew on the capture flop ---
        0.000     0.000   clock edge at q1_reg
        0.173     0.173   q1_reg/Q                   (DFFR)
        0.000     0.173   dout_reg/D                 (DFFR)
                  0.338   required (clock + hold)
                 -0.165   SLACK   *** VIOLATED ***

  --- the SAME skew, with two gate delays added to the data path ---
        0.171     0.171   q1_reg/Q                   (DFFR)
        0.118     0.289   u92/Y                      (XNOR2)
        0.120     0.409   u93/Y                      (XNOR2)
        0.000     0.409   dout_reg/D                 (DFFR)
                  0.338   required (clock + hold)
                  0.071   SLACK   MET
```

Note what is *absent* from that arithmetic: **the clock period**. A hold
violation is a race between two things that happen at the same edge, so
slowing the clock down does not help at all. That surprises everybody once.

Note also the direction of the fix. Setup is fixed by making the path
**faster**; hold is fixed by making it **slower**. It is the only time in
digital design you deliberately add delay.

### A constraint that fixes timing with no design change

```
$ make mcp
  --- without the multicycle promise ---
  WNS (worst slack)  : -1.193 ns   VIOLATED
  TNS (total neg)    : -6.555 ns over 11 failing endpoint(s)
  --- with set_multicycle_path 4 ---
  WNS (worst slack)  : +0.392 ns   MET
  TNS (total neg)    : +0.000 ns over 0 failing endpoint(s)
```

`slow_path.v` captures its result one cycle in four, so the adder really does
have four periods to settle. The analyser cannot know that; you have to tell
it. No RTL changed, no area was added, no latency appeared — the design was
always fine and the *constraints* were wrong.

This is the cheapest optimisation in the topic and the most dangerous. A
multicycle path is a **promise about the design**. If the promise is false the
chip fails, and no simulation will ever show it, because simulation does not
model delay. Somebody other than its author should check every one.

### The optimisations did not break anything

```
$ make verify
PASS - all three adders agree with the reference over 500 vectors
```

`add_ripple_pipe` answers one cycle later than the other two, and the testbench
knows that. An optimisation you did not verify is a bug you have not found yet.

## Experiments worth doing

1. **Predict, then measure.** Before running `make sweep`, work out from
   `lib/cda_edu.lib` how long one full-adder stage should take. Compare with
   the measured `ns/bit` column. Why is the measured figure lower than a naive
   XOR + AND + OR sum?

2. **Break the analyser's assumption.** Set `-p 0.5` on `add_ripple`. Read the
   report. Now find the smallest period at which it still passes, by bisection,
   and check it against the reported `longest path`.

3. **Delete the clock.** Run `sta.py` with no `-c` and no `-p`. Everything is
   unconstrained and everything "passes". This is what an SDC file with a
   missing `create_clock` does to a real project, and it has shipped broken
   chips.

4. **Make the skew worse.** In `constraints/hold_skew.sdc`, raise the skew
   until `hold_fixed` fails too. How much delay would you then need? At what
   point is fixing the clock tree obviously the better answer?

5. **Move the pipeline cut.** In `add_ripple_pipe.v`, cut at bit 8 or bit 24
   instead of bit 16. Measure. Why is the middle the best place, and what does
   that tell you about balancing pipeline stages?

6. **Cost the optimisation.** For each row of the closure table, divide cells by
   Fmax. Which design gives the most megahertz per gate? Is that the one you
   would ship?

7. **Write a false path and regret it.** Add `set_false_path` between two
   registers that really are connected, and watch the violation disappear. This
   is exactly how a real chip fails: the report is clean and the silicon is not.

## What this analyser does not model

Being clear about this is part of knowing what a timing report is worth.

* **Input slew.** Real cell delay depends on how sharp the incoming edge is,
  which is why real libraries use 2-D tables. Here delay depends only on load.
* **Wire delay.** A net costs only the load its sinks present. On a real chip
  past about 90 nm, wire delay often dominates gate delay.
* **On-chip variation and corners.** Real sign-off runs several corners (slow
  process/low voltage/high temperature for setup, fast/high/low for hold) with
  derating. Here there is one nominal corner.
* **Clock tree synthesis.** Skew is a number you type here. In a real flow it
  is computed from the physical clock tree after placement.
* **Latches, multiple clocks, generated clocks, clock gating, CDC.**

Every one of those makes real numbers worse than these. The *method* is
identical, which is the part worth learning.

## A note on the vendor tools

`scripts/vivado_timing.tcl` and `constraints/vivado.xdc` use standard,
version-stable commands (`create_clock`, `set_input_delay`,
`set_multicycle_path`, `synth_design`, `report_timing_summary`,
`report_timing`). They were **not** executed while this material was written,
because Vivado is not installed in the authoring environment. Check them
against your installed release before the lab session, and change the part
number to match your board.

One thing in the XDC file is worth reading even if you never run Vivado: a
setup multicycle of N needs a **hold multicycle of N−1** alongside it.
Relaxing setup moves the hold check too, and forgetting to move it back
creates a hold violation where there was none. It catches everybody once.

Everything run against Yosys 0.33, Icarus Verilog 12.0 and Python 3.11 in this
folder was executed, and the outputs quoted above are real.
