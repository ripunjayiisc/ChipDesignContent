# ---------------------------------------------------------------------------
# vivado.xdc  -  the same constraints, in the form Vivado expects.
#
# XDC is SDC with Vivado's object-query syntax. Compare it line by line with
# constraints/add32.sdc: the ideas are identical, only the way you name things
# differs.
#
# NOTE: a working template. It was NOT executed while this material was
# written, because Vivado is not installed in the authoring environment. The
# commands are standard; check them against your release.
# ---------------------------------------------------------------------------

# 1. the clock -- on a real board this is a pin with a real period
create_clock -name clk -period 4.000 [get_ports clk]

# 2. uncertainty. Vivado derives jitter itself from the clock source, so you
#    normally only add your own margin here.
set_clock_uncertainty -setup 0.150 [get_clocks clk]
set_clock_uncertainty -hold  0.050 [get_clocks clk]

# 3. when the inputs arrive, relative to that clock
set_input_delay  -clock clk 1.000 [get_ports {a[*] b[*]}]

# 4. how much of the period the outside world needs
set_output_delay -clock clk 1.000 [get_ports {sum[*] cout}]

# --- exceptions ------------------------------------------------------------
# reset is asynchronous and is never timed as a data path
set_false_path -from [get_ports rst_n]

# the slow_path design: the adder has four periods, not one
# set_multicycle_path -setup 4 -from [get_cells {a_q_reg[*] b_q_reg[*]}] \
#                              -to   [get_cells acc_reg[*]]
# set_multicycle_path -hold  3 -from [get_cells {a_q_reg[*] b_q_reg[*]}] \
#                              -to   [get_cells acc_reg[*]]
#
# NOTE the hold value is one LESS than the setup value. This catches everyone
# once: relaxing setup by N cycles moves the hold check as well, and you have
# to move it back or you create a hold violation where there was none.
