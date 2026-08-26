# ---------------------------------------------------------------------------
# modelsim_run.do  -  run a Topic 5 lab in ModelSim / Questa.
#
#   vsim -c -do scripts/modelsim_run.do                    # V3 on the golden FIFO
#   vsim -c -gLAB=V6 -gDUT=fifo_b3 -do scripts/modelsim_run.do
#   vsim    -do scripts/modelsim_run.do                    # GUI, with waves
#
# ModelSim/Questa supports the full SystemVerilog assertion language, including
# the ranged delay forms that the open-source flow cannot handle, and it can
# report assertion and functional coverage directly.
#
# NOTE: a working template. ModelSim is not installed in the environment this
# material was authored in, so this was not executed. The commands (vlib, vlog,
# vsim, run, coverage) are standard; check them against your release.
# ---------------------------------------------------------------------------

if {![info exists LAB]} { set LAB V3 }
if {![info exists DUT]} { set DUT fifo }

# ---- 1. a fresh working library -------------------------------------------
if {[file exists work]} { vdel -all }
vlib work
vmap work work

# ---- 2. compile ------------------------------------------------------------
set DEFS "+define+DUT=$DUT +define+DUTNAME=\"$DUT\""

switch $LAB {
    V1 { vlog {*}$DEFS rtl/fifo.v rtl/fifo_bugs.v tb/tb_v1_naive.v
         set TOP tb_v1_naive }
    V2 { vlog {*}$DEFS rtl/fifo.v rtl/fifo_bugs.v tb/tb_v2_selfcheck.v
         set TOP tb_v2_selfcheck }
    V4 { vlog {*}$DEFS rtl/fifo.v rtl/fifo_bugs.v tb/tb_v4_coverage.v
         set TOP tb_v4_coverage }
    V6 { vlog -sv {*}$DEFS rtl/fifo.v rtl/fifo_bugs.v sva/fifo_sva.sv tb/tb_v6_assert.sv
         set TOP tb_v6_assert }
    default { vlog {*}$DEFS rtl/fifo.v rtl/fifo_bugs.v tb/tb_v3_random.v
              set TOP tb_v3_random }
}

# ---- 3. elaborate and load -------------------------------------------------
#   -voptargs=+acc keeps signal visibility - without it the optimiser removes
#   the very signals you want to look at
#   -assertdebug reports every assertion pass and failure, not just failures
if {$LAB eq "V6"} {
    vsim -voptargs=+acc -assertdebug +SEED=7 +CYCLES=2000 work.$TOP
    # show every assertion, and stop the run on the first failure
    assertion fail -action break -r /*
} else {
    vsim -voptargs=+acc +SEED=1 +CYCLES=3000 work.$TOP
}

# ---- 4. waves, in the GUI only ---------------------------------------------
if {[batch_mode] == 0} {
    add wave -divider "stimulus"
    add wave -position insertpoint sim:/$TOP/clk sim:/$TOP/rst_n \
                                   sim:/$TOP/wr_en sim:/$TOP/wr_data \
                                   sim:/$TOP/rd_en sim:/$TOP/rd_data
    add wave -divider "DUT state"
    add wave -position insertpoint sim:/$TOP/full sim:/$TOP/empty sim:/$TOP/count
    add wave -divider "internals"
    add wave -position insertpoint sim:/$TOP/u_dut/wr_ptr sim:/$TOP/u_dut/rd_ptr
    configure wave -timelineunits ns
}

run -all

# ---- 5. coverage, if it was compiled in ------------------------------------
#   compile with  vlog -cover bcesx  to enable code coverage, then:
#   coverage report -details -file build/coverage.txt

if {[batch_mode]} { quit -f }
