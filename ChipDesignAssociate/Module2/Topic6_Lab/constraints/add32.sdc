# ---------------------------------------------------------------------------
# add32.sdc  -  a complete, ordinary set of constraints for a 32-bit adder.
#
# Four lines is most of what a real SDC file does. Everything else is
# exceptions to these four.
# ---------------------------------------------------------------------------

# 1. THE CLOCK. Without this there is no timing analysis at all - every path
#    is unconstrained, and every report says "met" because nothing was checked.
create_clock -name clk -period 4.0

# 2. UNCERTAINTY. Real clocks jitter and real clock trees have skew you have
#    not modelled yet. Give the analysis some margin so that closing timing in
#    the report means closing it on silicon.
set_clock_uncertainty 0.15 -setup
set_clock_uncertainty 0.05 -hold

# 3. WHEN INPUTS ARRIVE, relative to the clock edge. The path from a port into
#    the first register is a real path and it is somebody's responsibility.
set_input_delay 1.0

# 4. HOW LONG THE OUTSIDE NEEDS. The path from the last register to a port is
#    equally real.
set_output_delay 1.0
