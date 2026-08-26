# ---------------------------------------------------------------------------
# modelsim_run.do  -  run one Topic 4 lab in ModelSim / Questa.
#
#   vsim -c -do scripts/modelsim_run.do            (batch, prints PASS/FAIL)
#   vsim     -do scripts/modelsim_run.do           (GUI, with waveforms)
#
# Change LAB below, or pass it in:
#   vsim -c -gLAB=L3_fsm -do scripts/modelsim_run.do
#
# NOTE: ModelSim is not installed in the container this material was authored
# in, so this is a working template rather than a captured run. The commands
# are standard and version-stable; check against your installation.
# ---------------------------------------------------------------------------

if {![info exists LAB]} { set LAB L5_uart }

# ---- 1. a fresh working library --------------------------------------------
if {[file exists work]} { vdel -all }
vlib work
vmap work work

# ---- 2. compile -------------------------------------------------------------
switch $LAB {
    L1_comb {
        vlog -sv rtl/mux2.v rtl/mux4.v rtl/decoder3to8.v rtl/priority_encoder8.v \
                 rtl/alu.v rtl/seven_seg.v rtl/adder_gen.v tb/tb_comb.v
        set TOP tb_comb
    }
    L2_seq {
        vlog -sv rtl/reg_en.v rtl/shift_reg.v rtl/counter.v rtl/edge_detect.v \
                 rtl/synchroniser.v rtl/debouncer.v rtl/clk_divider.v tb/tb_seq.v
        set TOP tb_seq
    }
    L3_fsm {
        vlog -sv rtl/traffic_fsm.v rtl/vending_fsm.v rtl/seq_detect_1011.v tb/tb_fsm.v
        set TOP tb_fsm
    }
    L4_mem {
        vlog -sv rtl/sync_fifo.v rtl/sync_ram.v tb/tb_mem.v
        set TOP tb_mem
    }
    default {
        vlog -sv rtl/uart_tx.v rtl/uart_rx.v rtl/synchroniser.v tb/tb_uart.v
        set TOP tb_uart
    }
}

# ---- 3. elaborate and simulate ---------------------------------------------
#   -voptargs=+acc keeps signal visibility so you can actually see them
vsim -voptargs=+acc work.$TOP

# ---- 4. add waves (GUI only) ------------------------------------------------
if {[batch_mode] == 0} {
    add wave -divider "testbench"
    add wave -position insertpoint sim:/$TOP/*
    configure wave -timelineunits ns
}

run -all

if {[batch_mode]} { quit -f }
