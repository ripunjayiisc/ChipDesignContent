# ---------------------------------------------------------------------------
# Topic 5 - Functional verification of RTL designs.
#
#   make            everything: lint, all labs, the clinic, coverage
#   make lint       static checks (one second - always start here)
#   make run        all labs against the golden FIFO
#   make clinic     the V1/V2/V3 x six-designs matrix - the centrepiece
#   make regress    multi-seed, multi-profile regression
#   make cover      coverage across three profiles, merged
#   make assert     assertions vs scoreboard on every broken design
#   make waves      run V3 and open the waveform with the saved view
#   make clean
# ---------------------------------------------------------------------------
.PHONY: all lint run clinic regress cover assert waves clean

all: lint run clinic cover assert
	@echo
	@echo "=== Topic 5 lab complete ==="

lint:    ; @./scripts/lint.sh
run:     ; @./scripts/run_all.sh
clinic:  ; @./scripts/clinic.sh
regress: ; @./scripts/regress.sh 4
cover:   ; @./scripts/coverage.sh
assert:  ; @./scripts/assert.sh

waves: build/tb_v3_random.vvp
	@vvp build/tb_v3_random.vvp +SEED=1 +CYCLES=400 > /dev/null 2>&1
	@echo "opening v3.vcd with the saved view ..."
	@gtkwave v3.vcd wave/v3_fifo.gtkw &

build/tb_v3_random.vvp: rtl/fifo.v rtl/fifo_bugs.v tb/tb_v3_random.v
	@mkdir -p build
	@iverilog -g2005 -o $@ $^

clean:
	@rm -rf build obj_dir *.vcd
	@echo "cleaned"
