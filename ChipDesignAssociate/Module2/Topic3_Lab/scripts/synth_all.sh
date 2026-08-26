#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# synth_all.sh  -  synthesise every Topic 3 design and report the cell counts.
#
#   cd Topic3_Lab && ./scripts/synth_all.sh
#
# Requires: yosys.
#
# The point of this script is the LATCH CHECK.  Any design that reports a
# $_DLATCH_ cell has an incomplete combinational assignment somewhere - a
# missing else, or a case without a default - and that is a bug, not a style
# preference.  Every design here should report "no latches".
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build
fail=0

synth_one () {                 # synth_one <top> <sources...>
    local top=$1; shift
    local log="build/synth_$top.txt"
    printf '\n=== %-26s ===\n' "$top"
    if ! yosys -p "read_verilog $*; synth -top $top; abc -g AND,OR,XOR,NAND,NOR; stat" \
              > "$log" 2>&1; then
        echo "  yosys FAILED - see $log"; fail=1; return
    fi
    # print only the LAST statistics block (the post-abc one)
    awk '/Number of cells/{buf=""; p=1} p{buf=buf"  "$0"\n"} p&&/^$/{p=0; last=buf}
         END{printf "%s", last}' "$log"
    # a real latch shows up as a "$_DLATCH..." CELL line inside a stat block
    if awk '/Number of cells/{p=1} p&&/^\s+\$_DLATCH/{found=1} p&&/^$/{p=0}
            END{exit !found}' "$log"; then
        echo "  *** LATCH INFERRED in $top - this is a BUG ***"; fail=1
    else
        echo "  latch check: OK - no \$_DLATCH_ cells"
    fi
}

synth_one half_adder             rtl/half_adder.v
synth_one full_adder             rtl/full_adder.v
synth_one adder4                 rtl/full_adder.v rtl/adder4.v
synth_one mux4                   rtl/mux4.v
synth_one decoder2to4            rtl/decoder2to4.v
synth_one dff                    rtl/dff.v
synth_one shift4                 rtl/shift4.v
synth_one bcd_counter            rtl/bcd_counter.v
synth_one seq_detect_1011        rtl/seq_detect_1011.v
synth_one seq_detect_1011_onehot rtl/seq_detect_1011_onehot.v

printf '\n=========================================\n'
if [ $fail -eq 0 ]; then
    echo "ALL DESIGNS SYNTHESISED, NO LATCHES INFERRED"
else
    echo "PROBLEMS FOUND - scroll up"
fi
exit $fail
