#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# equiv.sh  -  PROVE that two descriptions are the same circuit.
#
#   ./scripts/equiv.sh <fileA> <topA> <fileB> <topB>
#
# Simulation shows that two designs agree on the patterns you applied. For the
# full adder that happened to be exhaustive - three inputs, eight patterns - but
# exhaustive simulation stops being possible at about 30 inputs, and real
# designs have thousands.
#
# Equivalence checking answers the same question without enumerating anything.
# It builds a MITER: both designs fed the same inputs, their outputs compared,
# and an assertion that the comparison always holds. A SAT solver then tries to
# find any input pattern that breaks the assertion. If it cannot, no such
# pattern exists, and the two designs are equivalent for every input.
#
# "no model found" is the solver saying: I could not construct a
# counter-example, and I looked everywhere.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
fa=$1; ta=$2; fb=$3; tb=$4
mkdir -p build

out=$(yosys -p "
    read_verilog $fa
    synth -top $ta
    rename $ta gold
    design -stash A

    read_verilog $fb
    synth -top $tb
    rename $tb gate
    design -stash B

    design -copy-from A -as gold gold
    design -copy-from B -as gate gate

    miter -equiv -flatten -make_assert gold gate miter
    sat -verify -prove-asserts miter
" 2>&1) || true

if echo "$out" | grep -q "SAT proof finished - no model found: SUCCESS"; then
    vars=$(echo "$out" | grep -o "with [0-9]* variables" | head -1 | tr -dc 0-9)
    printf "  %-34s EQUIVALENT   (proved, %s SAT variables)\n" "$ta vs $tb" "$vars"
    exit 0
else
    printf "  %-34s NOT EQUIVALENT\n" "$ta vs $tb"
    echo "$out" | grep -iE "^ERROR|Solving|model found" | head -4 | sed 's/^/      /'
    exit 1
fi
