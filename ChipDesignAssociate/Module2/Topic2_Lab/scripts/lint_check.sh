#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# lint_check.sh  -  is the linter telling the truth about latches?
#
# tools/rtl_lint.py is regular expressions. Rules L005 and L006 claim that a
# missing else, or a case with no default, infers a latch. That is a claim
# about what a SYNTHESISER will do, so the synthesiser gets to settle it.
#
# For every file, this compares two independent opinions:
#     the linter    - does it raise L005 or L006?
#     Yosys         - does the netlist actually contain a $_DLATCH_ cell?
#
# They must agree on every file. A linter that cries wolf gets switched off,
# and a linter that stays quiet is worse than none at all.
#
# The second half of the table is the interesting one. Those modules all use
# the DEFAULT-ASSIGNMENT IDIOM: every output written unconditionally at the
# top of the block, then an if or case that may not cover every branch. A
# naive rule flags all of them; Yosys builds a latch in none of them. That
# gap is why L005 and L006 have to understand the idiom, and this table is
# the evidence that they do.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

echo
printf "  %-24s %-14s %-14s %s\n" "file" "linter says" "yosys says" "verdict"
printf "  %s\n" "---------------------------------------------------------------------"

fails=0

check_one() {
    f=$1; m=$2; label=$3

    if python3 tools/rtl_lint.py "$f" 2>/dev/null | grep -qE "L005|L006"; then
        lint="latch"
    else
        lint="no latch"
    fi

    yosys -p "read_verilog $f; synth -top $m; write_json build/${m}_lc.json" \
          > /dev/null 2>&1
    if [ -f "build/${m}_lc.json" ] && \
       grep -q "DLATCH" "build/${m}_lc.json"; then
        ys="latch"
    else
        ys="no latch"
    fi

    if [ "$lint" = "$ys" ]; then verdict="agree"; else verdict="DISAGREE"; fails=$((fails+1)); fi
    printf "  %-24s %-14s %-14s %s\n" "$label" "$lint" "$ys" "$verdict"
}

# --- the fixtures written to break one rule each ---------------------------
for f in subset/s0*.v subset/s1*.v; do
    m=$(basename "$f" .v)
    case "$m" in s08_*|s09_*|s12_*|s13_*) continue ;; esac   # do not synthesise
    check_one "$f" "$m" "$m"
done

# --- and the real designs, which all use the default-assignment idiom ------
printf "  %s\n" "  ---- default-assignment idiom ----"
check_one fsm/traffic.v           traffic        traffic
check_one fsm/seq101_moore.v      seq101_moore   seq101_moore
check_one rtl/datapath_ctrl.v     accum_ctrl     accum_ctrl
check_one rtl/mux4_styles.v       mux4_case      mux4_case
check_one rtl/mux4_styles.v       mux4_if        mux4_if
check_one rtl/mux4_styles.v       mux4_assign    mux4_assign

echo
if [ "$fails" -eq 0 ]; then
    echo "  The linter and the synthesiser agree on every file."
    echo "  L005 and L006 are not opinions - they predict what gets built."
else
    echo "  $fails disagreement(s). Trust the synthesiser, and fix the linter."
fi
echo
exit $fails
