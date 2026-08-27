# ---------------------------------------------------------------------------
# Topic 6 - Timing constraints and analysis.
#
#   make            everything below, in order
#   make lib        show what the analyser reads out of the Liberty file
#   make stdlib     regenerate + check lib/cda_edu_std.lib (for OpenSTA etc.)
#   make tiny       the smallest design, checkable by hand
#   make sweep      Fmax against adder width, both styles
#   make closure    the headline table: four designs, two mapping strategies
#   make hold       a hold violation, and the same design with it fixed
#   make mcp        a multicycle constraint turning a violation into a pass
#   make verify     prove the optimised adders still add
#   make clean
#
# NOTE: the hold and mcp targets deliberately show FAILING timing before they
# show it fixed, and the analyser exits non-zero when timing is violated (so
# that it can be used in CI). Those two recipe lines are prefixed with "-" so
# make does not stop on the failure it was asked to demonstrate.
# ---------------------------------------------------------------------------
.PHONY: all lib stdlib tiny sweep closure hold mcp verify clean

all: lib tiny sweep closure hold mcp verify
	@echo
	@echo "=== Topic 6 lab complete ==="

lib:
	@echo "=== what the analyser reads out of lib/cda_edu.lib ==="
	@python3 sta/liberty.py

# A standards-compliant view of the same library, for tools that reject the
# custom cda_* attributes. Regenerate it whenever cda_edu.lib changes.
stdlib:
	@echo
	@echo "=== the standards-compliant Liberty view (for OpenSTA / PrimeTime) ==="
	@python3 scripts/mklib_std.py
	@python3 scripts/checklib_std.py

tiny:
	@echo
	@echo "=== the smallest real timing path, checkable by hand ==="
	@./scripts/sta.sh tiny --paths 1 -p 1.0

sweep:
	@echo
	@echo "=== Fmax vs width: hand-written carry chain ==="
	@./scripts/fmax.sh add_ripple 4 8 16 32 64
	@echo
	@echo "=== Fmax vs width: a + b, delay-driven mapping ==="
	@ABC=-fast ./scripts/fmax.sh add_fast 4 8 16 32 64

closure:
	@./scripts/closure.sh

hold:
	@echo
	@echo "=== HOLD: two flops, 0.30 ns of clock skew ==="
	-@./scripts/sta.sh hold_demo constraints/hold_skew.sdc --hold --paths 1
	@echo
	@echo "=== the same skew, with delay added to the data path ==="
	@./scripts/sta.sh hold_fixed constraints/hold_skew.sdc --hold --paths 1

mcp:
	@echo
	@echo "=== a long path captured one cycle in four, at 3 ns ==="
	@./scripts/synth.sh slow_path > /dev/null
	@sed 's/^set_multicycle_path/#set_multicycle_path/' constraints/mcp.sdc > build/nomcp.sdc
	@echo "  --- without the multicycle promise ---"
	-@python3 sta/sta.py build/slow_path.json slow_path -c build/nomcp.sdc | grep -E "WNS|TNS"
	@echo "  --- with set_multicycle_path 4 ---"
	@python3 sta/sta.py build/slow_path.json slow_path -c constraints/mcp.sdc | grep -E "WNS|TNS"

verify:
	@echo
	@echo "=== do the optimised adders still add? ==="
	@mkdir -p build
	@iverilog -g2005 -o build/tb_add.vvp rtl/add_ripple.v rtl/add_ripple_pipe.v \
	          rtl/add_fast.v tb/tb_add.v
	@vvp build/tb_add.vvp | grep -E "PASS|FAIL"

clean:
	@rm -rf build
	@echo cleaned
