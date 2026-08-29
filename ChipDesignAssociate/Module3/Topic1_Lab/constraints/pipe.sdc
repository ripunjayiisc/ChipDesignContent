# ---------------------------------------------------------------------------
# pipe.sdc  -  a complete constraint set for the pipeline designs.
#
# Written in the order of section 2.8 of the workbook: clock, uncertainty,
# boundary, exceptions, environment. Every line has a reason.
# ---------------------------------------------------------------------------

# ---- clock ----------------------------------------------------------------
# 400 MHz. pipe_unbal cannot make this; pipe_bal can. That is the experiment.
create_clock -period 2.500

# jitter, plus a placeholder for the clock-tree skew that does not exist yet
set_clock_uncertainty 0.080 -setup
set_clock_uncertainty 0.020 -hold

# ---- boundary -------------------------------------------------------------
# Without these two lines every path touching a port is UNCONSTRAINED, and
# the analyser says so. Run without them once and read the warning.
set_input_delay  0.40 -clock clk
set_output_delay 0.35 -clock clk
