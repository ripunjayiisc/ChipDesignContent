# ---------------------------------------------------------------------------
# vivado_synth.tcl  -  synthesise one design and report the hardware.
#
#   vivado -mode batch -source scripts/vivado_synth.tcl -tclargs uart_tx
#
# Reports produced (in build/vivado/):
#   *_utilization.rpt   how many LUTs, flip-flops, BRAMs and DSPs you used
#   *_timing.rpt        the worst paths, once a clock is constrained
#
# The PART is a small Artix-7; change it to match your board.
#
# NOTE: provided as a template - see the note in vivado_sim.tcl.
# ---------------------------------------------------------------------------

set top  [lindex $argv 0]
if {$top eq ""} { set top "uart_tx" }
set part "xc7a35tcpg236-1"

array set SRC {
    mux4        {rtl/mux4.v}
    alu         {rtl/alu.v}
    counter     {rtl/counter.v}
    traffic_fsm {rtl/traffic_fsm.v}
    vending_fsm {rtl/vending_fsm.v}
    sync_fifo   {rtl/sync_fifo.v}
    sync_ram    {rtl/sync_ram.v}
    uart_tx     {rtl/uart_tx.v}
    uart_rx     {rtl/uart_rx.v rtl/synchroniser.v}
}
if {![info exists SRC($top)]} {
    puts "unknown top '$top'. Choose one of: [array names SRC]"
    exit 1
}

file mkdir build/vivado
foreach f $SRC($top) { read_verilog $f }

# a 50 MHz clock constraint, so the timing report means something
create_clock -period 20.000 -name clk [get_ports clk]

synth_design -top $top -part $part

report_utilization -file build/vivado/${top}_utilization.rpt
report_timing_summary -file build/vivado/${top}_timing.rpt

puts "=== $top synthesised. Now READ build/vivado/${top}_utilization.rpt ==="
puts "=== and check the Messages tab for every \[Synth 8-xxx\] warning.   ==="
