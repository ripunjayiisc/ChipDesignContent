#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# fmax.sh  -  sweep a design's WIDTH parameter and report the longest path.
#
#   ./scripts/fmax.sh add_ripple 4 8 16 32 64
#
# The point of the sweep is to SEE the shape of the curve. A ripple-carry
# adder's delay grows linearly with W, because the carry has to pass through
# every bit in turn. An adder the tool is free to design for itself grows far
# more slowly. You do not have to take that on trust - measure it.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
top=$1; shift
mkdir -p build
ABC=${ABC:-}

printf '  %-6s %10s %12s %10s %10s\n' W cells "longest(ns)" "Fmax(MHz)" "ns/bit"
printf '  %s\n' "-------------------------------------------------------"
for w in "$@"; do
    yosys -p "
        read_verilog rtl/${top}.v
        chparam -set W $w ${top}
        synth -top ${top}
        abc ${ABC} -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
        opt_clean
        write_json build/${top}_w${w}.json
        stat
    " > "build/${top}_w${w}.log" 2>&1
    cells=$(grep 'Number of cells' "build/${top}_w${w}.log" | tail -1 | awk '{print $NF}')
    path=$(python3 sta/sta.py "build/${top}_w${w}.json" "$top" -p 1000 2>/dev/null \
           | grep 'longest path' | awk '{print $4}')
    if [ -z "$path" ]; then printf '  %-6s %10s %12s\n' "$w" "$cells" "(no path)"; continue; fi
    fmax=$(python3 -c "print('%.1f' % (1000.0/$path))")
    perbit=$(python3 -c "print('%.4f' % ($path/$w))")
    printf '  %-6s %10s %12s %10s %10s\n' "$w" "$cells" "$path" "$fmax" "$perbit"
done
