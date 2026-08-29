#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# stat.sh  -  synthesise one module and print three numbers:
#             flip-flops, total cells, and the estimated logic depth.
#
#   ./scripts/stat.sh <label> <top> <file...>
#
# Everything downstream in this lab that says "the tool built N cells" gets
# its number from here, so the numbers in the slides and the workbook are
# whatever your own installation actually produces.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
label=$1; top=$2; shift 2
mkdir -p build

log=build/stat_${top}.log
yosys -p "read_verilog $*; synth -top $top; stat" > "$log" 2>&1

# `synth` prints statistics more than once, so keep only the LAST
# "=== <top> ===" block: that one describes the finished netlist.
awk -v t="=== $top ===" '$0 ~ t {buf=""} {buf = buf $0 "\n"} END {printf "%s", buf}' \
    "$log" > build/stat_${top}.last

cells=$(awk '/Number of cells:/ {n=$4} END {print n+0}' build/stat_${top}.last)
ffs=$(awk '/\$_[SA]?DFF/   {s += $2} END {print s+0}' build/stat_${top}.last)
latch=$(awk '/\$_DLATCH/   {s += $2} END {print s+0}' build/stat_${top}.last)

printf "  %-32s %5s cells  %4s flip-flops" "$label" "$cells" "$ffs"
if [ "$latch" -gt 0 ]; then
    printf "   *** %s LATCH(ES) INFERRED ***" "$latch"
fi
printf "\n"
