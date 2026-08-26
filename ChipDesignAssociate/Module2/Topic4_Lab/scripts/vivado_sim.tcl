# ---------------------------------------------------------------------------
# vivado_sim.tcl  -  run one Topic 4 lab in Vivado, in NON-project mode.
#
#   vivado -mode batch -source scripts/vivado_sim.tcl -tclargs L5_uart
#
# Non-project mode keeps everything in this Tcl file, so the flow is
# reproducible and diffable. The GUI project flow does the same thing with
# menus; use whichever your lab prefers.
#
# NOTE: Vivado is not installed in the container this material was authored in,
# so this script is provided as a working template rather than a captured run.
# Check it against your installed version before the lab.
# ---------------------------------------------------------------------------

set lab [lindex $argv 0]
if {$lab eq ""} { set lab "L5_uart" }

# ---- source lists, one per lab ----------------------------------------------
array set SRC {
    L1_comb  {rtl/mux2.v rtl/mux4.v rtl/decoder3to8.v rtl/priority_encoder8.v
              rtl/alu.v rtl/seven_seg.v rtl/adder_gen.v tb/tb_comb.v}
    L2_seq   {rtl/reg_en.v rtl/shift_reg.v rtl/counter.v rtl/edge_detect.v
              rtl/synchroniser.v rtl/debouncer.v rtl/clk_divider.v tb/tb_seq.v}
    L3_fsm   {rtl/traffic_fsm.v rtl/vending_fsm.v rtl/seq_detect_1011.v tb/tb_fsm.v}
    L4_mem   {rtl/sync_fifo.v rtl/sync_ram.v tb/tb_mem.v}
    L5_uart  {rtl/uart_tx.v rtl/uart_rx.v rtl/synchroniser.v tb/tb_uart.v}
}
array set TOP {
    L1_comb tb_comb   L2_seq tb_seq   L3_fsm tb_fsm
    L4_mem  tb_mem    L5_uart tb_uart
}

if {![info exists SRC($lab)]} {
    puts "unknown lab '$lab'. Choose one of: [array names SRC]"
    exit 1
}

file mkdir build/vivado
cd build/vivado

# ---- 1. compile -------------------------------------------------------------
set files {}
foreach f $SRC($lab) { lappend files ../../$f }
exec xvlog -sv {*}$files

# ---- 2. elaborate -----------------------------------------------------------
exec xelab -debug typical $TOP($lab) -s ${lab}_sim

# ---- 3. simulate ------------------------------------------------------------
set fh [open run.tcl w]
puts $fh "run all"
puts $fh "quit"
close $fh
exec xsim ${lab}_sim -tclbatch run.tcl

puts "=== $lab finished. Open the waveform with:  xsim ${lab}_sim -gui ==="
