#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# run_all.sh  -  compile and run every Topic 3 lab, in order.
#
#   cd Topic3_Lab && ./scripts/run_all.sh
#
# Requires: iverilog (Icarus Verilog 11 or later).
# Produces: *.vcd waveform files you can open with  gtkwave <file>.vcd
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
IV="iverilog -g2012"
fail=0

run () {                       # run <name> <sources...>
    local name=$1; shift
    printf '\n=== %s ===\n' "$name"
    if ! $IV -o "build/$name.out" "$@" 2> "build/$name.log"; then
        echo "COMPILE ERROR - see build/$name.log"; cat "build/$name.log"; fail=1; return
    fi
    if ! vvp "build/$name.out" | tee "build/$name.txt"; then
        fail=1; return
    fi
    grep -q "^PASS" "build/$name.txt" || { echo "  --> did not report PASS"; fail=1; }
}

mkdir -p build

run comb        rtl/half_adder.v rtl/mux4.v rtl/decoder2to4.v tb/tb_comb.v
run full_adder  rtl/full_adder.v tb/tb_full_adder.v
run adder4      rtl/full_adder.v rtl/adder4.v tb/tb_adder4.v
run sequential  rtl/dff.v rtl/shift4.v rtl/bcd_counter.v tb/tb_sequential.v
run fsm         rtl/seq_detect_1011.v rtl/seq_detect_1011_mealy.v tb/tb_seq_detect.v

printf '\n=========================================\n'
if [ $fail -eq 0 ]; then
    echo "ALL LABS PASSED"
else
    echo "SOME LABS FAILED - scroll up for details"
fi
echo "Waveforms written: $(ls *.vcd 2>/dev/null | tr '\n' ' ')"
exit $fail
