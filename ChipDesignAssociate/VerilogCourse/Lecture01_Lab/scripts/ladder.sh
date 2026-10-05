#!/bin/bash
# ladder.sh - walk ONE design down the design flow and count what comes out at
# each level. This is Lecture 01's "simplistic view of the design flow", made
# into numbers you can read.
set -e
cd "$(dirname "$0")/.."
mkdir -p out

cells () { ./scripts/stat.sh "$1" | awk '/Number of cells:/ {print $4}'; }
parts () { ./scripts/stat.sh "$1" | awk '/^ *\$/ {printf "%s x%s  ", $1, $2}'; }

printf '%-26s %8s   %s\n' "LEVEL" "CELLS" "WHAT THEY ARE"
printf '%-26s %8s   %s\n' "--------------------------" "--------" "-------------"

SRC_LINES=$(grep -vcE '^[[:space:]]*(//|$)' rtl/counter4.v)
printf '%-26s %8s   %s\n' "1  Behavioural (source)" "-" \
       "$SRC_LINES lines of Verilog - no cells yet"
printf '%-26s %8s   %s\n' "2  Data path (RTL)" "$(cells scripts/level1_rtl.ys)" \
       "$(parts scripts/level1_rtl.ys)"
printf '%-26s %8s   %s\n' "3  Logic (gates)" "$(cells scripts/level2_gates.ys)" \
       "$(parts scripts/level2_gates.ys)"
printf '%-26s %8s   %s\n' "   same, for an FPGA" "$(cells scripts/fpga_luts.ys)" \
       "$(parts scripts/fpga_luts.ys)"

cat <<'TXT'

Read it downwards. The description gets more detailed at every step and the
number of things in it grows, but the circuit still counts 0..15 and wraps.
Level 2 is where a Verilog designer works; everything below it was produced
by a tool, from that one short source file.
TXT
