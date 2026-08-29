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
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

echo
printf "  %-24s %-14s %-14s %s\n" "file" "linter says" "yosys says" "verdict"
printf "  %s\n" "---------------------------------------------------------------------"

fails=0
for f in subset/s0*.v subset/s1*.v; do
    m=$(basename "$f" .v)
    case "$m" in s08_*|s09_*|s12_*|s13_*) continue ;; esac   # do not synthesise

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
    printf "  %-24s %-14s %-14s %s\n" "$m" "$lint" "$ys" "$verdict"
done

echo
if [ "$fails" -eq 0 ]; then
    echo "  The linter and the synthesiser agree on every file."
    echo "  L005 and L006 are not opinions - they predict what gets built."
else
    echo "  $fails disagreement(s). Trust the synthesiser, and fix the linter."
fi
echo
exit $fails
