# Lecture 01 - Introduction : lab targets
#
#   make sim      Lab 1  simulate the counter and write a waveform
#   make wave     Lab 1  open that waveform in GTKWave
#   make transform Lab 2 watch a CAD tool rewrite one HDL description as another
#   make prove    Lab 2  check that the rewrite did not change the behaviour
#   make ladder   Lab 3  count the cells at each level of the design flow
#   make target   Lab 4  compare the ASIC mapping with the FPGA mapping
#   make langs    Lab 5  run the same design in Verilog and in VHDL
#   make all      everything, in order
#   make clean    remove everything under out/

IVERILOG ?= iverilog
VVP      ?= vvp
YOSYS    ?= yosys
GTKWAVE  ?= gtkwave

.PHONY: all sim wave transform prove ladder target langs clean

all: sim transform prove ladder target langs

out:
	@mkdir -p out

sim: out
	$(IVERILOG) -g2012 -o out/tb_counter4.vvp rtl/counter4.v rtl/tb_counter4.v
	$(VVP) out/tb_counter4.vvp

wave: sim
	$(GTKWAVE) out/counter4.vcd

transform: out
	@echo "--- the behavioural description you wrote ---"
	@cat rtl/counter4.v
	@echo
	@echo "--- after synthesis to RTL: still Verilog, but now a netlist ---"
	@$(YOSYS) -q -s scripts/level1_rtl.ys
	@cat out/counter4_rtl.v
	@echo
	@echo "--- after mapping to gates: still Verilog, more detailed again ---"
	@$(YOSYS) -q -s scripts/level2_gates.ys
	@cat out/counter4_gates.v

prove: out
	@./scripts/prove_equivalence.sh

ladder: out
	@./scripts/ladder.sh

target: out
	@./scripts/asic_vs_fpga.sh

langs: out
	@./scripts/compare_languages.sh

clean:
	rm -rf out
