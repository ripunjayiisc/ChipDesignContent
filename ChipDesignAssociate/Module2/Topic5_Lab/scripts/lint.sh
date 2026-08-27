#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# lint.sh  -  static checks. ONE SECOND. Run this before you simulate anything.
#
# Verilator reads the RTL without simulating it and reports width truncation,
# inferred latches, unused and undriven signals, and incomplete sensitivity
# lists. Every one of those is a bug the simulator would only show you later,
# indirectly, as a wrong number on a waveform.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
fail=0

echo "=== linting the RTL ==="
verilator --lint-only -Wall -Wno-DECLFILENAME rtl/fifo.v --top-module fifo || fail=1

for m in fifo_b1 fifo_b2 fifo_b3 fifo_b4 fifo_b5; do
    verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-WIDTHEXPAND \
              rtl/fifo_bugs.v --top-module $m || fail=1
done

echo "=== linting the assertions ==="
verilator --lint-only -Wall --assert -Wno-DECLFILENAME sva/fifo_sva.sv --top-module fifo_sva || fail=1

echo
if [ $fail -eq 0 ]; then
    echo "LINT CLEAN"
    echo
    echo "Note: the five broken FIFOs lint clean too. That is the point - a"
    echo "linter checks the FORM of your code, not its MEANING. Nothing but a"
    echo "testbench that knows the specification will find these bugs."
else
    echo "LINT PROBLEMS FOUND"
fi
exit $fail
