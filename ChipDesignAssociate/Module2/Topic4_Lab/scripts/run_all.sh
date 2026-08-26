#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# run_all.sh  -  compile and run every Topic 4 lab with Icarus Verilog.
#
#   cd Topic4_Lab && ./scripts/run_all.sh
#
# Produces build/<lab>.txt logs and *.vcd waveforms you can open with GTKWave.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
IV="iverilog -g2012"
fail=0
mkdir -p build

run () {                        # run <name> <sources...>
    local name=$1; shift
    printf '\n=== %-12s ===\n' "$name"
    if ! $IV -o "build/$name.out" "$@" 2> "build/$name.log"; then
        echo "  COMPILE ERROR - see build/$name.log"; cat "build/$name.log"; fail=1; return
    fi
    if [ -s "build/$name.log" ]; then
        echo "  --- compiler warnings ---"; cat "build/$name.log"
    fi
    vvp "build/$name.out" | tee "build/$name.txt"
    grep -q "^PASS" "build/$name.txt" || { echo "  --> did NOT report PASS"; fail=1; }
}

run L1_comb rtl/mux2.v rtl/mux4.v rtl/decoder3to8.v rtl/priority_encoder8.v \
            rtl/alu.v rtl/seven_seg.v rtl/adder_gen.v tb/tb_comb.v

run L2_seq  rtl/reg_en.v rtl/shift_reg.v rtl/counter.v rtl/edge_detect.v \
            rtl/synchroniser.v rtl/debouncer.v rtl/clk_divider.v tb/tb_seq.v

run L3_fsm  rtl/traffic_fsm.v rtl/vending_fsm.v rtl/seq_detect_1011.v tb/tb_fsm.v

run L4_mem  rtl/sync_fifo.v rtl/sync_ram.v tb/tb_mem.v

run L5_uart rtl/uart_tx.v rtl/uart_rx.v rtl/synchroniser.v tb/tb_uart.v

printf '\n=========================================\n'
if [ $fail -eq 0 ]; then
    echo "ALL LABS PASSED"
else
    echo "SOME LABS FAILED - scroll up for details"
fi
echo "Waveforms: $(ls *.vcd 2>/dev/null | tr '\n' ' ')"
exit $fail
