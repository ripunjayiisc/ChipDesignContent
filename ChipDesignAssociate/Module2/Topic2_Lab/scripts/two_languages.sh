#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# two_languages.sh  -  the same design, in Verilog and in VHDL.
#
# The syllabus says "Hardware Description Languages (HDLs) such as Verilog or
# VHDL". The word doing the work is OR. They are two notations for the same
# ideas, and an engineer who understands RTL can read both after an afternoon.
#
# This runs both descriptions of the same design, through two different
# simulators, and diffs the transcripts. If a single line differs, something
# in one of the two files is not saying what the other says.
#
# Two designs are compared: a counter, and the Moore '101' detector. The
# second one matters more, because a state machine is where the languages
# really do differ - VHDL has a proper enumerated type for the states, and
# will not let a case statement be non-exhaustive.
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

# --------------------------------------------------------------------------
# and the harder case: a state machine
# --------------------------------------------------------------------------
echo "  === the same '101' detector, both languages ==="
mkdir -p build/vhdl_fsm

iverilog -g2012 -o build/s101_v.vvp fsm/seq101_moore.v fsm/tb_seq101_trace.v
vvp build/s101_v.vvp | grep -v "VCD info" > build/s101_v.log

(
  cd build/vhdl_fsm
  ghdl -a --std=08 ../../vhdl/seq101_moore.vhd ../../vhdl/tb_seq101.vhd
  ghdl -e --std=08 tb_seq101
  ghdl -r --std=08 tb_seq101
) > build/s101_vhdl.log 2>&1

if diff <(grep "^cycle" build/s101_v.log) \
        <(grep "^cycle" build/s101_vhdl.log) > build/lang_fsm.diff; then
    n=$(grep -c "^cycle" build/s101_v.log)
    echo "  IDENTICAL over all $n cycles, detections included."
    echo
    echo "  Verilog:  localparam [1:0] S_IDLE = 2'd0, ...   a number"
    echo "  VHDL:     type state_t is (S_IDLE, S_1, ...)    a type"
    echo
    echo "  The VHDL version cannot be assigned an illegal state; the compiler"
    echo "  rejects it. The Verilog version can be assigned 2'd7 and nobody"
    echo "  complains until silicon. That is the trade, in one sentence."
else
    echo "  THEY DIFFER:"
    sed 's/^/    /' build/lang_fsm.diff | head -10
    exit 1
fi
echo
