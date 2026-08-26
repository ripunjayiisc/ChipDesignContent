#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# lint.sh  -  static checks with Verilator, BEFORE you simulate.
#
#   cd Topic4_Lab && ./scripts/lint.sh
#
# Verilator's lint mode catches, for free and in about a second:
#   * width mismatches      (the commonest silent RTL bug)
#   * unused and undriven signals
#   * incomplete case statements  ->  the latch you did not mean to infer
#   * combinational loops
#
# Lint every file before you simulate it. The habit costs nothing and saves
# entire afternoons.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build
fail=0

lint_one () {                   # lint_one <top> <sources...>
    local top=$1; shift
    printf '\n=== %-20s ===\n' "$top"
    if verilator --lint-only -Wall -Wno-DECLFILENAME --top-module "$top" "$@" \
                 > "build/lint_$top.txt" 2>&1; then
        echo "  clean"
    else
        cat "build/lint_$top.txt"
        fail=1
    fi
}

lint_one mux2             rtl/mux2.v
lint_one mux4             rtl/mux4.v
lint_one decoder3to8      rtl/decoder3to8.v
lint_one priority_encoder8 rtl/priority_encoder8.v
lint_one alu              rtl/alu.v
lint_one seven_seg        rtl/seven_seg.v
lint_one adder_gen        rtl/adder_gen.v
lint_one reg_en           rtl/reg_en.v
lint_one shift_reg        rtl/shift_reg.v
lint_one counter          rtl/counter.v
lint_one edge_detect      rtl/edge_detect.v
lint_one synchroniser     rtl/synchroniser.v
lint_one debouncer        rtl/debouncer.v rtl/synchroniser.v
lint_one clk_divider      rtl/clk_divider.v
lint_one traffic_fsm      rtl/traffic_fsm.v
lint_one vending_fsm      rtl/vending_fsm.v
lint_one seq_detect_1011  rtl/seq_detect_1011.v
lint_one sync_fifo        rtl/sync_fifo.v
lint_one sync_ram         rtl/sync_ram.v
lint_one uart_tx          rtl/uart_tx.v
lint_one uart_rx          rtl/uart_rx.v rtl/synchroniser.v

printf '\n=========================================\n'
[ $fail -eq 0 ] && echo "LINT CLEAN" || echo "LINT FOUND PROBLEMS - fix them before simulating"
exit $fail
