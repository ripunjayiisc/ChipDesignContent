#!/bin/bash
# compare_languages.sh - simulate the SAME counter in Verilog and in VHDL,
# then compare the two waveforms signal by signal.
set -e
cd "$(dirname "$0")/.."
mkdir -p out/ghdl

echo "--- Verilog (Icarus) ---"
iverilog -g2012 -o out/tb_counter4.vvp rtl/counter4.v rtl/tb_counter4.v
vvp out/tb_counter4.vvp | grep -E 'PASS|FAIL|MISMATCH'

echo
echo "--- VHDL (GHDL) ---"
ghdl -a --workdir=out/ghdl vhdl/counter4.vhd vhdl/tb_counter4.vhd
ghdl -r --workdir=out/ghdl tb_counter4 --vcd=out/counter4_vhdl.vcd \
    | grep -E 'PASS|FAIL|MISMATCH'

python3 scripts/vcd_q.py out/counter4.vcd      q > out/q_verilog.txt
python3 scripts/vcd_q.py out/counter4_vhdl.vcd q > out/q_vhdl.txt

echo
echo "--- the whole run, including time zero ---"
if diff -q out/q_verilog.txt out/q_vhdl.txt >/dev/null; then
    echo "identical"
else
    echo "they differ, and ONLY here:"
    diff out/q_verilog.txt out/q_vhdl.txt | sed 's/^/    /'
    echo
    echo "    Why: a Verilog 'reg' holds x (unknown) until something drives it,"
    echo "    so q is xxxx until the reset edge at 5 ns clears it. The VHDL"
    echo "    signal was declared with an initial value, so it reads 0000 from"
    echo "    time zero. The DESCRIBED HARDWARE is the same - a real flip-flop"
    echo "    also powers up in an unpredictable state, which is exactly why"
    echo "    every design has a reset."
fi

echo
echo "--- from the end of reset onwards (15 ns) ---"
python3 scripts/vcd_q.py out/counter4.vcd      q 15 > out/q_verilog_r.txt
python3 scripts/vcd_q.py out/counter4_vhdl.vcd q 15 > out/q_vhdl_r.txt
if diff -q out/q_verilog_r.txt out/q_vhdl_r.txt >/dev/null; then
    n=$(wc -l < out/q_verilog_r.txt)
    echo "IDENTICAL - $n transitions, same value at the same time in both languages"
else
    diff out/q_verilog_r.txt out/q_vhdl_r.txt
    exit 1
fi
