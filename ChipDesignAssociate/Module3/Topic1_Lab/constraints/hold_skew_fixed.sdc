# ---------------------------------------------------------------------------
# hold_skew_fixed.sdc  -  the same design, after the clock tree was rebalanced.
#
# The hold violation in hold_skew.sdc was caused by 0.25 ns of skew reaching
# the capture register late. The honest fix is not to change the RTL: it is to
# balance the clock tree so that skew falls, or to let place-and-route insert
# delay on the data path. This file models the first of those.
# ---------------------------------------------------------------------------
create_clock -period 4.0
set_clock_skew 0.10 -regs q2_reg
