#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# run_all.sh  -  compile and run every lab against the GOLDEN FIFO.
#
# All of these must pass on rtl/fifo.v. If one fails on a clean checkout, your
# tool installation is the suspect, not the code.
#
#   ./scripts/run_all.sh
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build
fail=0

one () {                 # one <tag> <tbfile> <top> [plusargs...]
    local tag=$1 tbf=$2 top=$3; shift 3
    printf '\n=== %-28s ===\n' "$tag"
    if ! iverilog -g2005 -o "build/$top.vvp" rtl/fifo.v rtl/fifo_bugs.v "$tbf" \
            > "build/$top.log" 2>&1; then
        echo "  COMPILE FAILED - see build/$top.log"; fail=1; return
    fi
    vvp "build/$top.vvp" "$@" 2>/dev/null | grep -vE "^VCD info" | sed 's/^/  /'
    if ! vvp "build/$top.vvp" "$@" 2>/dev/null | grep -q "^PASS"; then fail=1; fi
}

one "V1 naive directed"      tb/tb_v1_naive.v     tb_v1_naive
one "V2 model + corner cases" tb/tb_v2_selfcheck.v tb_v2_selfcheck
one "V3 constrained-random"   tb/tb_v3_random.v    tb_v3_random +SEED=1 +CYCLES=3000
one "V4 functional coverage"  tb/tb_v4_coverage.v  tb_v4_coverage +SEED=1 +CYCLES=3000 +TAG=runall

printf '\n=== %-28s ===\n' "V6 layered + assertions"
rm -rf build/obj_runall
if verilator --binary --timing --assert -Wall -Wno-DECLFILENAME -Wno-WIDTHEXPAND \
        -Wno-WIDTHTRUNC -Wno-BLKSEQ -Wno-SYNCASYNCNET --Mdir build/obj_runall -o v6 \
        rtl/fifo.v rtl/fifo_bugs.v sva/fifo_sva.sv tb/tb_v6_assert.sv \
        --top-module tb_v6_assert > build/v6.log 2>&1; then
    ./build/obj_runall/v6 +SEED=7 +CYCLES=2000 2>&1 | grep -vE "^- " | sed 's/^/  /'
    ./build/obj_runall/v6 +SEED=7 +CYCLES=2000 2>&1 | grep -q "^PASS" || fail=1
else
    echo "  BUILD FAILED - see build/v6.log"; fail=1
fi

printf '\n=========================================\n'
if [ $fail -eq 0 ]; then
    echo "ALL LABS PASSED on the golden FIFO"
    echo
    echo "Now run ./scripts/clinic.sh - the same testbenches against five"
    echo "broken FIFOs. That is where Topic 5 actually starts."
else
    echo "PROBLEMS FOUND"
fi
exit $fail
