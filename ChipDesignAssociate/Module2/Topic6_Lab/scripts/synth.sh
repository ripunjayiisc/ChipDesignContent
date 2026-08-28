#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# synth.sh  -  synthesise one design to a gate netlist the analyser can read.
#
#   ./scripts/synth.sh <top> [extra source files...]
#
# Yosys maps the RTL onto the generic gate set that lib/cda_edu.lib describes,
# then writes JSON. Everything downstream - the timing report, the Fmax sweep -
# reads that JSON.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
top=$1; shift || true
mkdir -p build

srcs="rtl/${top}.v"
for f in "$@"; do srcs="$srcs $f"; done

yosys -p "
    read_verilog $srcs
    synth -top $top
    abc -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
    opt_clean
    write_json build/${top}.json
    stat
" > "build/${top}_synth.log" 2>&1

awk '/Number of cells/{p=1} p{print "  " $0} p&&/^$/{exit}' "build/${top}_synth.log" \
    | head -20
echo "  -> build/${top}.json"
