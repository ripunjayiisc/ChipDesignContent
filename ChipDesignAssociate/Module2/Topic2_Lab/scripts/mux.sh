#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# mux.sh  -  one function, three coding styles: simulated exhaustively,
# proved equivalent by SAT, and then synthesised to compare the gate counts.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

iverilog -g2012 -o build/mux4.vvp rtl/mux4_styles.v rtl/tb_mux4.v
vvp build/mux4.vvp | grep -v "VCD info"

echo "  and the same claim, proved rather than sampled:"
echo
./scripts/equiv.sh rtl/mux4_styles.v mux4_assign rtl/mux4_styles.v mux4_case
./scripts/equiv.sh rtl/mux4_styles.v mux4_assign rtl/mux4_styles.v mux4_if
echo
echo "  and the hardware each style produced:"
echo
./scripts/stat.sh "mux4_assign" mux4_assign rtl/mux4_styles.v
./scripts/stat.sh "mux4_case"   mux4_case   rtl/mux4_styles.v
./scripts/stat.sh "mux4_if"     mux4_if     rtl/mux4_styles.v
echo
echo "  Proved equivalent, and yet three different cell counts. EQUIVALENT"
echo "  means the function matches - it says nothing about area or timing."
echo "  The conditional expression uses sel[1] and sel[0] straight as mux"
echo "  selects; the case and if/else versions build equality comparators"
echo "  against 2'b00, 2'b01 ... and this optimiser does not fully undo"
echo "  that. A different tool may. Measure yours instead of assuming."
