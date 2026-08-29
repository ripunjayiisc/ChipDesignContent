# ---------------------------------------------------------------------------
# zynq.xdc  -  the constraints of constraints/pipe.sdc, in Xilinx syntax.
#
# The timing half is standard SDC and is copied across unchanged. The pin and
# I/O-standard half has no SDC equivalent - that is the whole difference
# between the two formats.
# ---------------------------------------------------------------------------

# ---- timing: identical to constraints/pipe.sdc ----------------------------
create_clock -name clk -period 2.500 [get_ports clk]
set_clock_uncertainty 0.080 -setup [get_clocks clk]
set_clock_uncertainty 0.020 -hold  [get_clocks clk]

set_input_delay  -clock clk -max 0.40 [get_ports {a[*] b[*]}]
set_input_delay  -clock clk -min 0.10 [get_ports {a[*] b[*]}]
set_output_delay -clock clk -max 0.35 [get_ports {y[*]}]
set_output_delay -clock clk -min 0.05 [get_ports {y[*]}]

# ---- physical: XDC only ---------------------------------------------------
# Zybo Z7-20 system clock, 125 MHz, on pin K17. Change these for your board;
# nothing above this line needs to change with it.
set_property PACKAGE_PIN K17     [get_ports clk]
set_property IOSTANDARD  LVCMOS33 [get_ports clk]
