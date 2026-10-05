#!/bin/bash
# asic_vs_fpga.sh - the SAME Verilog, mapped two different ways.
#
# Lecture 01: "as an alternative you can go for a field programmable gate
# array ... much greater flexibility, but the speed will be less."
# Here is what that difference looks like in the netlist.
set -e
cd "$(dirname "$0")/.."

echo "=== mapped to logic GATES (the ASIC route) ==="
./scripts/stat.sh scripts/level2_gates.ys | sed -n '/Number of cells/,$p'

echo
echo "=== mapped to 4-input LOOK-UP TABLES (the FPGA route) ==="
./scripts/stat.sh scripts/fpga_luts.ys | sed -n '/Number of cells/,$p'

cat <<'TXT'

Both are the same counter, and both came from the same ten lines of Verilog.

  ASIC route   each gate becomes a specific transistor arrangement that is
               manufactured once and can never be changed. Fast and small,
               but you must pay for masks and wait for a foundry.

  FPGA route   each LUT is a small memory already present on a chip you can
               buy today. You load a bitstream and the logic exists seconds
               later - but a LUT is slower than the dedicated gates it
               imitates, and you pay for the flexibility in area and speed.

The flip-flops are the same in both: four of them, one per bit of the counter.
TXT
