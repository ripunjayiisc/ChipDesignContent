# ---------------------------------------------------------------------------
# vivado_timing.tcl  -  synthesise and report timing in Vivado.
#
#   vivado -mode batch -source scripts/vivado_timing.tcl -tclargs add_ripple 32
#
# NOTE: a working template, NOT executed while this material was written -
# Vivado is not installed in the authoring environment. The commands
# (synth_design, report_timing_summary, report_timing) are standard and
# version-stable, but check them, and change the part to match your board.
# ---------------------------------------------------------------------------
set top   [lindex $argv 0]
set width [lindex $argv 1]
if {$top   eq ""} { set top   "add_ripple" }
if {$width eq ""} { set width 32 }
set part "xc7a35tcpg236-1"

file mkdir build/vivado
read_verilog rtl/${top}.v
read_xdc     constraints/vivado.xdc

synth_design -top $top -part $part -generic W=$width

# THE SUMMARY: worst negative slack, total negative slack, failing endpoints.
# These three numbers are what a project actually tracks.
report_timing_summary -delay_type min_max -max_paths 10 \
                      -file build/vivado/${top}_summary.rpt

# THE WORST PATHS, in full, with every cell and net on them. This is the report
# you read to find out WHY, once the summary has told you THAT.
report_timing -delay_type max -max_paths 5 -nworst 5 -input_pins \
              -file build/vivado/${top}_setup.rpt
report_timing -delay_type min -max_paths 5 -nworst 5 -input_pins \
              -file build/vivado/${top}_hold.rpt

report_utilization -file build/vivado/${top}_util.rpt

# A quick verdict on the console, so a batch run is readable
set wns [get_property SLACK [get_timing_paths -delay_type max]]
set whs [get_property SLACK [get_timing_paths -delay_type min]]
puts "=== $top  W=$width  WNS=$wns  WHS=$whs ==="
puts "=== read build/vivado/${top}_summary.rpt for the detail ==="
