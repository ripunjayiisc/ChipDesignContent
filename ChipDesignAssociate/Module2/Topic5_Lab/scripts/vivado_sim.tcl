# ---------------------------------------------------------------------------
# vivado_sim.tcl  -  run a Topic 5 lab in the Vivado simulator (xsim).
#
#   vivado -mode batch -source scripts/vivado_sim.tcl -tclargs V3 fifo_b1
#
#   arg 0 : lab       V1 | V2 | V3 | V4 | V6      (default V3)
#   arg 1 : dut       fifo | fifo_b1 .. fifo_b5   (default fifo)
#
# xsim, unlike Icarus, supports the full SystemVerilog assertion language, so
# V6 runs here with every property in sva/fifo_sva.sv active.
#
# NOTE: this is a working template. It was NOT executed while this material was
# prepared - Vivado is not installed in the authoring environment. The commands
# (xvlog, xelab, xsim) are standard and version-stable, but check them against
# your installed release before the lab session.
# ---------------------------------------------------------------------------

set lab [lindex $argv 0]
set dut [lindex $argv 1]
if {$lab eq ""} { set lab "V3" }
if {$dut eq ""} { set dut "fifo" }

array set TB {
    V1 {tb/tb_v1_naive.v      tb_v1_naive}
    V2 {tb/tb_v2_selfcheck.v  tb_v2_selfcheck}
    V3 {tb/tb_v3_random.v     tb_v3_random}
    V4 {tb/tb_v4_coverage.v   tb_v4_coverage}
    V6 {tb/tb_v6_assert.sv    tb_v6_assert}
}
if {![info exists TB($lab)]} {
    puts "unknown lab '$lab'. Choose one of: [array names TB]"
    exit 1
}
lassign $TB($lab) tbfile tbtop

file mkdir build/xsim

# ---- 1. analyse -----------------------------------------------------------
#   -d passes a `define, exactly like -D does to iverilog
set defs "-d DUT=$dut -d DUTNAME=\\\"$dut\\\""

if {$lab eq "V6"} {
    exec >@stdout 2>@stderr xvlog -sv {*}$defs rtl/fifo.v rtl/fifo_bugs.v \
                                    sva/fifo_sva.sv $tbfile
} else {
    exec >@stdout 2>@stderr xvlog {*}$defs rtl/fifo.v rtl/fifo_bugs.v $tbfile
}

# ---- 2. elaborate ---------------------------------------------------------
#   -debug typical keeps signal visibility for the waveform window
exec >@stdout 2>@stderr xelab -debug typical $tbtop -s ${tbtop}_sim

# ---- 3. run ---------------------------------------------------------------
#   plusargs are passed straight through, so the seed works exactly as it does
#   under Icarus and the same seed gives the same run
exec >@stdout 2>@stderr xsim ${tbtop}_sim -runall -testplusarg SEED=1 \
                                          -testplusarg CYCLES=3000

puts "=== $lab on $dut finished. Read the transcript above for PASS or FAIL. ==="
puts "=== For waveforms, open the GUI:  xsim ${tbtop}_sim -gui            ==="
