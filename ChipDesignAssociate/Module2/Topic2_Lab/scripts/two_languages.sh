#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# two_languages.sh  -  the same design, in Verilog and in VHDL.
#
# The syllabus says "Hardware Description Languages (HDLs) such as Verilog or
# VHDL". The word doing the work is OR. They are two notations for the same
# ideas, and an engineer who understands RTL can read both after an afternoon.
#
# This runs both descriptions of the same counter, through two different
# simulators, and diffs the transcripts. If a single line differs, something
# in one of the two files is not saying what the other says.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build/vhdl

echo
echo "  === Verilog: iverilog ==="
iverilog -g2005 -o build/counter_v.vvp rtl/tb_counter.v rtl/counter.v
vvp build/counter_v.vvp | grep -v "VCD info" > build/counter_v.log
tail -4 build/counter_v.log | sed 's/^/  /'

echo
echo "  === VHDL: ghdl ==="
(
  cd build/vhdl
  ghdl -a --std=08 ../../vhdl/counter.vhd ../../vhdl/tb_counter.vhd
  ghdl -e --std=08 tb_counter
  ghdl -r --std=08 tb_counter 2>&1 | grep -v "^$"
) > build/counter_vhdl.log 2>&1
grep -E "cycle|complete" build/counter_vhdl.log | tail -4 | sed 's/^/  /'

echo
echo "  === diff of the two transcripts ==="
if diff <(grep "cycle" build/counter_v.log) \
        <(grep "cycle" build/counter_vhdl.log) > build/lang.diff; then
    n=$(grep -c cycle build/counter_v.log)
    echo "  IDENTICAL over all $n cycles - including the wrap and the terminal count."
    echo "  Two languages, two simulators, one design."
else
    echo "  THEY DIFFER:"
    sed 's/^/    /' build/lang.diff | head -10
    exit 1
fi
echo
