#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# pitfalls.sh  -  the two mistakes that account for most of the bugs a new
# RTL engineer files: the inferred latch, and blocking assignment in a
# clocked block. Both are shown in simulation AND in the netlist.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

echo "  --- pitfall 1: blocking assignment in a clocked block ---"
iverilog -g2012 -o build/shift.vvp \
    pitfalls/shift_nb.v pitfalls/shift_bl.v pitfalls/tb_shift.v
vvp build/shift.vvp | grep -v "VCD info"
echo "  and the hardware each one produced:"
echo
./scripts/stat.sh "shift_nb (non-blocking)" shift_nb pitfalls/shift_nb.v
./scripts/stat.sh "shift_bl (blocking)"     shift_bl pitfalls/shift_bl.v
echo
echo "  Three flip-flops against one. The blocking version did not build a"
echo "  slower shift register or a buggy one - it built a DIFFERENT CIRCUIT,"
echo "  and no tool warned about it, because nothing illegal was written."
echo

echo "  --- pitfall 2: the inferred latch ---"
echo
./scripts/stat.sh "s03_latch   (missing else)"    s03_latch    subset/s03_latch.v
./scripts/stat.sh "s14_latch_case (no default)"   s14_latch_case subset/s14_latch_case.v
./scripts/stat.sh "mux4_case   (has a default)"   mux4_case    rtl/mux4_styles.v
./scripts/stat.sh "mux4_if     (has a final else)" mux4_if     rtl/mux4_styles.v
echo
echo "  The rule 'assign every output on every path' is not a style"
echo "  preference. The first two lines are what happens when you break it."
