# ---------------------------------------------------------------------------
# hold_skew.sdc  -  a 200 MHz clock, with 0.30 ns of skew on the capture flop.
#
# Every port is constrained. An UNCONSTRAINED port is not a passing path, it
# is an unchecked one, and the analyser will tell you how many it skipped.
# ---------------------------------------------------------------------------
create_clock -name clk -period 5.0

set_input_delay  0.5
set_output_delay 0.5

# The clock reaches dout_reg 0.30 ns after it reaches everything else.
# In a real design this comes from an unbalanced clock tree.
set_clock_skew 0.30 -regs dout_reg
