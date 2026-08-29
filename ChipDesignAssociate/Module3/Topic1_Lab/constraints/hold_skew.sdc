# ---------------------------------------------------------------------------
# hold_skew.sdc  -  a clock tree that reaches one register late.
#
# Before layout there is no clock tree, so there is no skew and hold checks
# pass trivially. This file forces the situation that appears the day after
# clock-tree synthesis: 0.25 ns of extra delay to one capture register.
#
# Skew that arrives LATE at the capture register helps setup and hurts hold,
# by the same amount. Run the analyser with --hold to see it.
# ---------------------------------------------------------------------------
create_clock -period 4.0
set_clock_skew 0.25 -regs q2_reg
