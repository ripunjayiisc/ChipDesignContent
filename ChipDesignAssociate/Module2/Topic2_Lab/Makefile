# ---------------------------------------------------------------------------
# Module 2 Topic 2 - RTL Design Methodology.
#
#   make            everything below, in order
#
#   -- what RTL is ----------------------------------------------------------
#   make transfer   what "register transfer level" literally means
#   make ladder     one adder at four levels of abstraction, all simulated
#   make prove      formal proof that the levels are the same circuit
#   make mux        one function, three coding styles, measured and proved
#
#   -- what synthesises, and what bites -------------------------------------
#   make subset     which Verilog constructs actually synthesise
#   make mismatch   when simulation and silicon disagree - the worst bug there is
#   make pitfalls   the inferred latch and the blocking-assignment trap
#   make lint       the RTL coding rules, checked by a tool
#   make lintcheck  and cross-checked against what Yosys actually builds
#
#   -- how real blocks are structured ---------------------------------------
#   make fsm        Moore vs Mealy, encoding, and a controller with a timer
#   make dpctrl     datapath + controller, the shape of almost every block
#   make reuse      parameters, hierarchy and generate: from module to IP
#
#   -- the flow -------------------------------------------------------------
#   make langs      the same design in Verilog and in VHDL, both run
#   make flow       the whole methodology, executed: spec to formal proof
#   make clean
#
# Needs: iverilog, yosys, python3.  make langs also needs ghdl.
# ---------------------------------------------------------------------------
.PHONY: all transfer ladder prove mux subset mismatch pitfalls lint lintcheck \
        fsm dpctrl reuse langs flow clean

IV = iverilog -g2005

all: transfer ladder prove mux subset mismatch pitfalls lint lintcheck \
     fsm dpctrl reuse langs flow
	@echo
	@echo "=== Module 2 Topic 2 lab complete ==="

build:
	@mkdir -p build

# ------------------------------------------------------- what RTL means
transfer: build
	@echo
	@echo "=== 1. what 'register transfer level' literally means ==="
	@$(IV) -o build/transfer.vvp rtl/tb_transfer.v rtl/transfer.v
	@vvp build/transfer.vvp | grep -v "VCD info"

# ------------------------------------------------- the abstraction ladder
ladder: build
	@echo
	@echo "=== 2. one full adder, four levels of abstraction ==="
	@$(IV) -o build/ladder.vvp ladder/tb_ladder.v ladder/fa_behav.v \
	       ladder/fa_dataflow.v ladder/fa_gate.v ladder/fa_switch.v
	@vvp build/ladder.vvp | grep -v "VCD info"

prove: build
	@echo
	@echo "=== 3. simulation shows; proof settles ==="
	@echo "  Exhaustive simulation covered all 8 patterns. For anything larger"
	@echo "  that stops being possible, so here is the same claim, proved:"
	@echo
	@./scripts/equiv.sh ladder/fa_behav.v fa_behav ladder/fa_dataflow.v fa_dataflow
	@./scripts/equiv.sh ladder/fa_behav.v fa_behav ladder/fa_gate.v fa_gate
	@./scripts/equiv.sh ladder/fa_dataflow.v fa_dataflow ladder/fa_gate.v fa_gate
	@echo
	@echo "  and the same checker, on a full adder with one term missing:"
	@-./scripts/equiv.sh ladder/fa_behav.v fa_behav ladder/fa_broken.v fa_broken
	@echo
	@echo "  A checker that cannot fail is not evidence of anything."

mux: build
	@echo
	@echo "=== 4. one function, three coding styles ==="
	@./scripts/mux.sh

# ------------------------------------------------- the synthesisable subset
subset: build
	@echo
	@echo "=== 5. which constructs actually synthesise ==="
	@./scripts/subset.sh

mismatch: build
	@echo
	@echo "=== 6. when simulation and silicon disagree ==="
	@yosys -p "read_verilog subset/s04_incomplete_sens.v; \
	           synth -top s04_incomplete_sens; \
	           abc -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT; opt_clean; \
	           rename s04_incomplete_sens s04_net; \
	           write_verilog -noattr build/s04_net.v" > build/s04_net.log 2>&1
	@$(IV) -o build/mismatch.vvp subset/tb_mismatch.v \
	       subset/s04_incomplete_sens.v build/s04_net.v
	@vvp build/mismatch.vvp | grep -v "VCD info"

pitfalls: build
	@echo
	@echo "=== 7. the two mistakes that cost beginners the most time ==="
	@./scripts/pitfalls.sh

# ------------------------------------------------------------ methodology
lint:
	@echo
	@echo "=== 8. the coding rules, checked by a tool ==="
	@echo "  --- files written the way the methodology asks: ---"
	@python3 tools/rtl_lint.py rtl/counter.v rtl/counter4.v rtl/transfer.v \
	         rtl/reuse.v fsm/traffic.v fsm/seq101_moore.v \
	         subset/s01_ok_comb.v subset/s02_ok_seq.v
	@echo "  --- and files that break the rules on purpose: ---"
	@-python3 tools/rtl_lint.py subset/s12_bad_style.v \
	          subset/s13_two_drivers.v subset/s03_latch.v \
	          subset/s04_incomplete_sens.v pitfalls/shift_bl.v

lintcheck: build
	@echo
	@echo "=== 9. is the linter telling the truth? ==="
	@./scripts/lint_check.sh

# ------------------------------------------------- how blocks are structured
fsm: build
	@echo
	@echo "=== 10. the finite state machine ==="
	@./scripts/fsm.sh

dpctrl: build
	@echo
	@echo "=== 11. datapath + controller ==="
	@./scripts/dpctrl.sh

reuse: build
	@echo
	@echo "=== 12. parameters, hierarchy and generate ==="
	@./scripts/reuse.sh

# ------------------------------------------------------------- languages
langs: build
	@echo
	@echo "=== 13. Verilog or VHDL - the word doing the work is OR ==="
	@./scripts/two_languages.sh

# ------------------------------------------------------------- the flow
flow: build
	@echo
	@echo "=== 14. the whole methodology, executed ==="
	@./scripts/flow.sh

clean:
	rm -rf build *.cf *.o work-obj*.cf
