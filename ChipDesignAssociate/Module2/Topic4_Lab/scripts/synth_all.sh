#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# synth_all.sh  -  synthesise every design with Yosys and report the hardware.
#
#   cd Topic4_Lab && ./scripts/synth_all.sh
#
# For each design this prints the cell counts and then runs the LATCH CHECK.
# Any $_DLATCH_ cell means an incomplete combinational assignment: a bug, not
# a style preference.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build
fail=0

synth_one () {                  # synth_one <top> <sources...>
    local top=$1; shift
    local log="build/synth_$top.txt"
    printf '\n=== %-20s ===\n' "$top"
    if ! yosys -p "read_verilog $*; synth -top $top; abc -g AND,OR,XOR,NAND,NOR; stat" \
              > "$log" 2>&1; then
        echo "  yosys FAILED - see $log"; fail=1; return
    fi
    awk '/Number of cells/{buf=""; p=1} p{buf=buf"  "$0"\n"} p&&/^$/{p=0; last=buf}
         END{printf "%s", last}' "$log"
    if awk '/Number of cells/{p=1} p&&/^\s+\$_DLATCH/{found=1} p&&/^$/{p=0}
            END{exit !found}' "$log"; then
        echo "  *** LATCH INFERRED in $top - this is a BUG ***"; fail=1
    else
        echo "  latch check: OK - no \$_DLATCH_ cells"
    fi
}

synth_one mux4             rtl/mux4.v
synth_one decoder3to8      rtl/decoder3to8.v
synth_one priority_encoder8 rtl/priority_encoder8.v
synth_one alu              rtl/alu.v
synth_one seven_seg        rtl/seven_seg.v
synth_one adder_gen        rtl/adder_gen.v
synth_one reg_en           rtl/reg_en.v
synth_one shift_reg        rtl/shift_reg.v
synth_one counter          rtl/counter.v
synth_one edge_detect      rtl/edge_detect.v
synth_one debouncer        rtl/debouncer.v rtl/synchroniser.v
synth_one traffic_fsm      rtl/traffic_fsm.v
synth_one vending_fsm      rtl/vending_fsm.v
synth_one sync_fifo        rtl/sync_fifo.v
synth_one sync_ram         rtl/sync_ram.v
synth_one uart_tx          rtl/uart_tx.v
synth_one uart_rx          rtl/uart_rx.v rtl/synchroniser.v

printf '\n=========================================\n'
[ $fail -eq 0 ] && echo "ALL DESIGNS SYNTHESISED, NO LATCHES INFERRED" || echo "PROBLEMS FOUND"
exit $fail
