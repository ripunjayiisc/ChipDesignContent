#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# closure.sh  -  the whole point of Topic 6, as one table.
#
# The same 32-bit addition, described four ways, timed under two different
# synthesis settings. Nothing here is asserted; every number is measured.
#
#   ./scripts/closure.sh
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

run () {                       # run <top> <abcflag>
    yosys -p "read_verilog rtl/$1.v
              synth -top $1
              abc $2 -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
              opt_clean
              write_json build/cl_$1.json
              stat" > "build/cl_$1.log" 2>&1
    cells=$(grep 'Number of cells' "build/cl_$1.log" | tail -1 | awk '{print $NF}')
    path=$(python3 sta/sta.py "build/cl_$1.json" "$1" -p 1000 2>/dev/null \
           | grep 'longest path' | awk '{print $4}')
    fmax=$(python3 -c "print('%.0f' % (1000.0/$path))")
    echo "$cells|$path|$fmax"
}

echo
printf '  %-20s %26s %26s\n' "" "--- abc default (area) ---" "--- abc -fast (delay) ---"
printf '  %-20s %8s %9s %8s %8s %9s %8s\n' design cells "path(ns)" "Fmax" cells "path(ns)" "Fmax"
printf '  %s\n' "----------------------------------------------------------------------------"
for d in add_ripple add_ripple_pipe add_fast; do
    IFS='|' read -r c1 p1 f1 <<< "$(run $d '')"
    IFS='|' read -r c2 p2 f2 <<< "$(run $d '-fast')"
    printf '  %-20s %8s %9s %8s %8s %9s %8s\n' "$d" "$c1" "$p1" "$f1" "$c2" "$p2" "$f2"
done
echo
cat <<'NOTE'
  Read the table, not a slogan:

   * add_ripple hand-codes the carry chain, so the mapper has almost nothing
     left to decide. Asking for MORE effort does not help - it is already
     committed to a slow structure.

   * add_fast writes "a + b" and lets the tool choose. With the default,
     area-oriented mapping that is SLOWER than the hand-written version. With
     delay-oriented mapping it is more than twice as fast.

   * So "describe intent, not structure" is only half the rule. The other half
     is "and check what your tool did with it".

   * Pipelining works regardless of either: it halves the path because it
     halves the logic between registers.
NOTE
