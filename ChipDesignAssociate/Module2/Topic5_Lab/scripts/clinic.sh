#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# clinic.sh  -  Lab V5, the DEBUG CLINIC.
#
# Runs three testbenches of increasing strength against the golden FIFO and
# against five deliberately broken copies, and prints the result as a matrix.
#
# The matrix IS the lesson of Topic 5. A testbench is not "done" because it
# passes; it is done when it would FAIL if the design were wrong.
#
#   ./scripts/clinic.sh
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

DUTS="fifo fifo_b1 fifo_b2 fifo_b3 fifo_b4 fifo_b5"
declare -A RES

run_one () {              # run_one <tbfile> <tbtop> <tag> <dut> [plusargs...]
    local tbf=$1 top=$2 tag=$3 dut=$4; shift 4
    local vvp="build/${tag}_${dut}.vvp"
    if ! iverilog -g2005 -o "$vvp" -DDUT=$dut -DDUTNAME="\"$dut\"" \
            rtl/fifo.v rtl/fifo_bugs.v "$tbf" > "build/${tag}_${dut}.log" 2>&1; then
        RES[$tag,$dut]="BUILD-ERR"; return
    fi
    if vvp "$vvp" "$@" 2>/dev/null | grep -q "^PASS"; then
        RES[$tag,$dut]="pass"
    else
        RES[$tag,$dut]="CAUGHT"
    fi
}

echo "running the clinic - three testbenches x six designs ..."
for d in $DUTS; do
    run_one tb/tb_v1_naive.v     tb_v1_naive     V1 $d
    run_one tb/tb_v2_selfcheck.v tb_v2_selfcheck V2 $d
    run_one tb/tb_v3_random.v    tb_v3_random    V3 $d +SEED=1 +CYCLES=3000
done

echo
printf '  %-24s' "testbench"
for d in $DUTS; do printf '%-10s' "$d"; done; echo
printf '  %s\n' "----------------------------------------------------------------------------------------"
for tag in V1 V2 V3; do
    case $tag in
      V1) label="V1 naive directed" ;;
      V2) label="V2 model + corners" ;;
      V3) label="V3 constrained-random" ;;
    esac
    printf '  %-24s' "$label"
    for d in $DUTS; do printf '%-10s' "${RES[$tag,$d]}"; done
    echo
done
echo
echo '  "pass" on a broken design means the testbench MISSED the bug.'
echo '  "CAUGHT" means it failed, which on a broken design is the correct result.'
echo

# score: a testbench is judged by how many of the five bugs it caught
for tag in V1 V2 V3; do
    n=0
    for d in fifo_b1 fifo_b2 fifo_b3 fifo_b4 fifo_b5; do
        [ "${RES[$tag,$d]}" = "CAUGHT" ] && n=$((n+1))
    done
    good="${RES[$tag,fifo]}"
    printf '  %s : %d of 5 bugs caught, golden design %s\n' \
           "$tag" "$n" "$( [ "$good" = pass ] && echo 'passes (no false alarm)' || echo 'FAILS - FALSE ALARM' )"
done
