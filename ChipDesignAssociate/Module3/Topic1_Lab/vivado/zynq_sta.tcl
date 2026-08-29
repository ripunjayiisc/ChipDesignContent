# ---------------------------------------------------------------------------
# zynq_sta.tcl  -  the same analysis, on the board the syllabus names.
#
#   vivado -mode batch -source vivado/zynq_sta.tcl
#
# Target: xc7z020-clg400-1, the Zynq-7000 device on the Zybo Z7-20 and the
# ZedBoard. Nothing here needs the board to be plugged in - this is a
# synthesise-and-report flow, and Vivado will happily target a device it has
# never been connected to.
#
# The point of this script is NOT to get a number. It is to run the analysis
# you already ran with sta/sta.py through an industrial tool and see the same
# structure in the report: startpoint, endpoint, incremental delays, required
# time, slack.
# ---------------------------------------------------------------------------

set part   xc7z020clg400-1
set outdir vivado/rpt
file mkdir $outdir

read_verilog [glob rtl/pipe_unbal.v rtl/pipe_bal.v]
read_xdc     vivado/zynq.xdc

# ---- 1. synthesise ---------------------------------------------------------
synth_design -top pipe_bal -part $part -flatten_hierarchy rebuilt

# ---- 2. timing after synthesis --------------------------------------------
report_timing_summary -file $outdir/post_synth_summary.rpt
report_timing -delay_type max -max_paths 10 -file $outdir/post_synth_setup.rpt
report_timing -delay_type min -max_paths 10 -file $outdir/post_synth_hold.rpt

set wns_synth [get_property SLACK [get_timing_paths -delay_type max]]
puts "post-synthesis WNS = $wns_synth"

# ---- 3. implement, then time again ----------------------------------------
# Setup slack almost always gets WORSE here: synthesis estimated the wiring,
# implementation measured it. Hold violations usually APPEAR here for the
# first time, because only now does a real clock tree exist.
opt_design
place_design
route_design

report_timing_summary -file $outdir/post_route_summary.rpt
set wns_route [get_property SLACK [get_timing_paths -delay_type max]]
set whs_route [get_property SLACK [get_timing_paths -delay_type min]]
puts "post-route     WNS = $wns_route"
puts "post-route     WHS = $whs_route     (hold - this is the number that"
puts "                                     did not exist before layout)"

# ---- 4. utilisation, for the area/speed trade-off -------------------------
report_utilization -file $outdir/utilization.rpt

puts ""
puts "Reports written to $outdir/"
puts "Compare post_synth_setup.rpt with the output of ./scripts/sta.sh pipe_bal."
puts "The numbers will differ - a Zynq LUT is not lib/cda_edu.lib. The shape of"
puts "the report, and which path is critical, should not."
