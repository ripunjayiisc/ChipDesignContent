#!/bin/bash
# prove_equivalence.sh - run the SAME test bench against the behavioural source
# and against the gate netlist the synthesiser produced from it.
#
# This makes the central claim of Lecture 01 checkable: a CAD tool rewrites one
# hardware description as a more detailed one WITHOUT changing what it does.
set -e
cd "$(dirname "$0")/.."
mkdir -p out
# simcells.v ships with yosys and gives a simulator a definition for the
# primitives yosys emits ($_AND_, $_XOR_, $_SDFF_PP0_ ...). Distributions put
# it in different places, so look in the usual ones.
SIMCELLS=""
for d in "$(yosys-config --datdir 2>/dev/null)" /usr/share/yosys \
         /usr/local/share/yosys /opt/homebrew/share/yosys; do
    if [ -n "$d" ] && [ -f "$d/simcells.v" ]; then SIMCELLS="$d/simcells.v"; break; fi
done
if [ -z "$SIMCELLS" ]; then
    echo "could not find simcells.v - is yosys installed?" >&2
    exit 1
fi

echo "--- 1. the behavioural description (what the designer wrote) ---"
iverilog -g2012 -o out/tb_behav.vvp rtl/counter4.v rtl/tb_counter4.v
vvp out/tb_behav.vvp | grep -E 'PASS|FAIL|MISMATCH'
mv -f out/counter4.vcd out/counter4_behav.vcd

echo
echo "--- 2. synthesise it down to gates ---"
yosys -q -s scripts/level2_gates.ys
grep -c . out/counter4_gates.v | xargs printf '    wrote out/counter4_gates.v (%s lines)\n'

echo
echo "--- 3. the SAME test bench, run against the gate netlist ---"
iverilog -g2012 -o out/tb_gates.vvp out/counter4_gates.v "$SIMCELLS" rtl/tb_counter4.v
vvp out/tb_gates.vvp | grep -E 'PASS|FAIL|MISMATCH'
mv -f out/counter4.vcd out/counter4_gates.vcd

echo
echo "--- 4. compare the two waveforms, cycle by cycle ---"
python3 scripts/vcd_q.py out/counter4_behav.vcd q > out/q_behav.txt
python3 scripts/vcd_q.py out/counter4_gates.vcd q > out/q_gates.txt
if diff -q out/q_behav.txt out/q_gates.txt >/dev/null; then
    n=$(wc -l < out/q_behav.txt)
    echo "IDENTICAL - $n transitions, same value at the same time."
    echo "The synthesiser changed the DESCRIPTION, not the BEHAVIOUR."
else
    echo "they differ:"
    diff out/q_behav.txt out/q_gates.txt
    exit 1
fi
