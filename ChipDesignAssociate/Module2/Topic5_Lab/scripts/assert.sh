#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# assert.sh  -  Lab V6.  ASSERTIONS versus a scoreboard.
#
# Builds the layered SystemVerilog testbench with sva/fifo_sva.sv bound to the
# DUT, runs it against the golden FIFO and every broken one, and reports WHICH
# assertion fired and WHEN.
#
# Read the output carefully. Four of the five bugs are caught by a named
# assertion at the exact cycle the rule was broken. One of them is not caught by
# any assertion at all - because the assertions in this file describe the
# CONTROL interface (count, full, empty) and that bug corrupts DATA. The
# scoreboard catches it instead.
#
# That is the whole argument for having both.
#
#   ./scripts/assert.sh
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

VFLAGS="--binary --timing --assert -Wall -Wno-DECLFILENAME -Wno-WIDTHEXPAND
        -Wno-WIDTHTRUNC -Wno-BLKSEQ -Wno-SYNCASYNCNET"

for d in fifo fifo_b1 fifo_b2 fifo_b3 fifo_b4 fifo_b5; do
    rm -rf build/obj_$d
    if ! verilator $VFLAGS --Mdir build/obj_$d -o v6_$d \
            -DDUT=$d -DDUTNAME="\"$d\"" \
            rtl/fifo.v rtl/fifo_bugs.v sva/fifo_sva.sv tb/tb_v6_assert.sv \
            --top-module tb_v6_assert > build/assert_build_$d.log 2>&1; then
        echo "  $d : BUILD FAILED - see build/assert_build_$d.log"
        continue
    fi
    out=$(./build/obj_$d/v6_$d +SEED=7 +CYCLES=2000 2>&1)
    a=$(echo "$out" | grep -m1 "Assertion failed" \
        | sed -E 's/.*\[([0-9]+)\].*\.([a-z_0-9]+): (.*)/assertion \2 fired at \1 ps: \3/')
    if [ -n "$a" ]; then
        printf '  %-9s CAUGHT by an ASSERTION  - %s\n' "$d" "$a"
    elif echo "$out" | grep -q "^FAIL"; then
        printf '  %-9s CAUGHT by the SCOREBOARD only - no assertion covers it\n' "$d"
        echo "$out" | grep -m1 "SCOREBOARD" | sed 's/^/               /'
    elif echo "$out" | grep -q "^PASS"; then
        printf '  %-9s passes - %s\n' "$d" \
               "$( [ "$d" = fifo ] && echo 'correct, this is the golden design' || echo 'MISSED' )"
    else
        printf '  %-9s no verdict - see the log\n' "$d"
    fi
done
