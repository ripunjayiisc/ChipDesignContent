#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# coverage.sh  -  run several stimulus profiles, then MERGE their coverage.
#
# No single run hits every corner, and no single run has to. Coverage is closed
# ACROSS a regression: each run contributes what it reached, the results are
# merged, and what is still missing tells you which test to write next.
#
# This is the loop that decides when verification is finished:
#
#     run  ->  merge  ->  look at the MISSes  ->  write stimulus for them
#       ^                                                     |
#       +-----------------------------------------------------+
#
#   ./scripts/coverage.sh
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build
rm -f build/cov_*.txt

iverilog -g2005 -o build/cov.vvp rtl/fifo.v tb/tb_v4_coverage.v || exit 1

run () {   # run <tag> <wr%> <rd%> <seed>
    echo "  --- profile $1 (wr=$2 rd=$3 seed=$4) ---"
    vvp build/cov.vvp +SEED=$4 +CYCLES=1500 +WR=$2 +RD=$3 +TAG=$1 2>/dev/null \
        | grep -E "bins covered|MISS" | sed 's/^/  /'
}

echo "running three stimulus profiles"
echo
run writeheavy 90 10 1
run readheavy  10 90 1
run balanced   50 50 1

echo
echo "  merged coverage across all three runs"
echo "  ---------------------------------------------------------------"
awk '{ idx=$1; c[idx]+=$2; $1=""; $2=""; sub(/^  /,""); name[idx]=$0 }
     END {
       hit=0; n=0
       for (i=0; i<12; i++) {
         n++
         printf("   %-30s %8d   %s\n", name[i], c[i], (c[i]>0)?"HIT":"MISS  <-- still not covered")
         if (c[i]>0) hit++
       }
       printf("  ---------------------------------------------------------------\n")
       printf("  merged: %d of %d bins covered (%d%%)\n", hit, n, hit*100/n)
       if (hit==n) printf("  COVERAGE CLOSED\n"); else printf("  COVERAGE HOLES REMAIN - write stimulus for the MISSes above\n")
     }' build/cov_*.txt
