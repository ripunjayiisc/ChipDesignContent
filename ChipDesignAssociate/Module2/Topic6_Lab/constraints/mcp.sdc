# ---------------------------------------------------------------------------
# mcp.sdc  -  the same clock, plus one promise about slow_path.
# ---------------------------------------------------------------------------
create_clock -name clk -period 3.0
set_clock_uncertainty 0.10 -setup
set_input_delay  0.4
set_output_delay 0.4

# The operands and the accumulator only move on a tick, one cycle in four.
# Therefore the adder has FOUR periods, not one, to settle.
#
# Before you write a line like this, satisfy yourself that it is TRUE. It is
# a promise, not a hint, and a false promise produces a chip that fails in a
# way no simulation will reproduce.
#   NOTE ON SYNTAX: this analyser matches -from and -to as regular expressions
#   against register names of the form <signal>[<bit>]_reg. Real SDC uses
#   [get_cells ...] / [get_pins ...] collections instead; the idea is the same.
set_multicycle_path 4 -from a_q -to acc
set_multicycle_path 4 -from b_q -to acc
