#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# fsm.sh  -  the finite state machine, the central RTL coding pattern.
#
# Runs both '101' detectors and the traffic-light controller, then synthesises
# them so the Moore/Mealy and binary/one-hot trade-offs are numbers you have
# measured rather than sentences you have read.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

echo "  --- Moore vs Mealy, same language, same stream ---"
iverilog -g2012 -o build/seq101.vvp \
    fsm/seq101_moore.v fsm/seq101_mealy.v fsm/seq101_moore_onehot.v \
    fsm/tb_seq101.v
vvp build/seq101.vvp | grep -v "VCD info"

echo "  --- and what each one costs in gates ---"
echo
./scripts/stat.sh "seq101_moore  binary"  seq101_moore        fsm/seq101_moore.v
./scripts/stat.sh "seq101_moore  one-hot" seq101_moore_onehot fsm/seq101_moore_onehot.v
./scripts/stat.sh "seq101_mealy  binary"  seq101_mealy        fsm/seq101_mealy.v
echo
echo "  Read those three lines carefully before you repeat the folklore."
echo "  On this generic gate library the one-hot version is BIGGER, not"
echo "  smaller: four states need four flip-flops instead of two, and the"
echo "  next-state logic has to drive four bits instead of two. One-hot pays"
echo "  off on an FPGA, where a flip-flop next to each lookup table is free"
echo "  and the win is the SHORT decode path, and on machines with many"
echo "  states, where binary decoding grows faster than the extra registers."
echo "  Measure your own target before choosing."
echo
echo "  --- a Moore controller with a datapath timer ---"
iverilog -g2012 -o build/traffic.vvp fsm/traffic.v fsm/tb_traffic.v
vvp build/traffic.vvp | grep -v "VCD info"
./scripts/stat.sh "traffic controller" traffic fsm/traffic.v
