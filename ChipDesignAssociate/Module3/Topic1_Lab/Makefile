# ---------------------------------------------------------------------------
# Module 3 Topic 1 - Overview of VLSI STA.
#
#   make            everything below, in order
#   make analyse    find the hazards in a two-level cover, and prove the fix
#   make glitch     gate-level simulation: watch the glitch, and watch it go
#   make capture    what a glitch does to a flop as data / clock / reset
#   make synth      what synthesis does to a hazard fix  (it deletes it)
#   make fmax       Fmax of an unbalanced pipeline, and of a balanced one
#   make setup      a real setup violation at 400 MHz, and its fix
#   make hold       a hold violation, and why the clock period cannot help
#   make clean
#
# The hazard targets are the new material in this topic; the setup/hold and
# constraint targets build on Module 2 Topic 6, whose analyser sta/sta.py is
# reused here.
# ---------------------------------------------------------------------------
.PHONY: all analyse glitch capture synth fmax setup hold clean

HAZ  = hz_static1 hz_static1_fix hz_none hz_dynamic hz_dynamic_fix hz_flat_fix
IV   = iverilog -g2005

all: analyse glitch capture synth fmax setup hold
	@echo
	@echo "=== Module 3 Topic 1 lab complete ==="

# ---------------------------------------------------------------- hazards
analyse:
	@echo
	@echo "=== 1. the analyser: find the hazard, prescribe the fix ==="
	@python3 tools/hazard.py --selftest
	@echo
	@python3 tools/hazard.py "A B' + B C"

glitch: build
	@echo
	@echo "=== 2. gate-level simulation: is the hazard real? ==="
	@for d in $(HAZ); do \
	    $(IV) -DDUT=$$d -DDUTNAME=\"$$d\" -o build/$$d.vvp \
	          hazards/tb_hazard.v hazards/$$d.v ; \
	    vvp build/$$d.vvp | grep -E "glitch detector|GLITCH|RESULT|TRUTH" ; \
	    echo ; \
	done
	@echo "  Same TRUTH signature within a family = the fix did not change the"
	@echo "  function. A 'fix' that alters the truth table is not a fix."

capture: build
	@echo
	@echo "=== 3. does a glitch matter? ==="
	@$(IV) -o build/glitch_capture.vvp \
	       hazards/tb_glitch_capture.v hazards/glitch_capture.v
	@vvp build/glitch_capture.vvp | grep -v "VCD info"

synth:
	@./scripts/hazard_synth.sh

# ------------------------------------------------------------- sequential
fmax:
	@echo
	@echo "=== 4. Fmax is set by ONE stage ==="
	@printf "  %-14s " pipe_unbal ; \
	  ./scripts/sta.sh pipe_unbal -p 20 2>&1 | grep Fmax | sed 's/^ *//' || true
	@printf "  %-14s " pipe_bal ; \
	  ./scripts/sta.sh pipe_bal   -p 20 2>&1 | grep Fmax | sed 's/^ *//' || true
	@echo "  Same arithmetic, one stage split in two."

setup:
	@echo
	@echo "=== 5. a real setup violation at 400 MHz, and its fix ==="
	@printf "  %-14s " pipe_unbal ; \
	  ./scripts/sta.sh pipe_unbal constraints/pipe.sdc 2>&1 \
	    | grep WNS | sed 's/^ *//' || true
	@printf "  %-14s " pipe_bal ; \
	  ./scripts/sta.sh pipe_bal constraints/pipe.sdc 2>&1 \
	    | grep WNS | sed 's/^ *//' || true
	@echo
	@echo "  The fix is not a faster tool setting - it is one more register."
	@echo "  Splitting the heavy stage moved the whole design across the line."

hold:
	@echo
	@echo "=== 6. hold does not care what the clock period is ==="
	@for p in 4.0 40.0 400.0 ; do \
	    printf "  period %6s ns   " $$p ; \
	    sed "s/^create_clock -period .*/create_clock -period $$p/" \
	        constraints/hold_skew.sdc > build/h.sdc ; \
	    ./scripts/sta.sh hold_demo build/h.sdc --hold 2>&1 \
	      | grep WNS | sed 's/^ *//' || true ; \
	done
	@echo
	@echo "  and the fix is the clock tree, not the clock frequency:"
	@printf "  skew 0.25 ns     " ; \
	  ./scripts/sta.sh hold_demo constraints/hold_skew.sdc --hold 2>&1 \
	    | grep WNS | sed 's/^ *//' || true
	@printf "  skew 0.10 ns     " ; \
	  ./scripts/sta.sh hold_demo constraints/hold_skew_fixed.sdc --hold 2>&1 \
	    | grep WNS | sed 's/^ *//' || true

build:
	@mkdir -p build

clean:
	rm -rf build vivado/rpt *.jou *.log
