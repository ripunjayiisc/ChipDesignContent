#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# regress.sh  -  a REGRESSION: the same testbench, many seeds, many profiles.
#
# One random run is one sample. A regression is what turns random stimulus into
# evidence: dozens of independent runs, every one reproducible from its seed,
# run automatically after every change.
#
#   ./scripts/regress.sh              # 12 runs, default
#   ./scripts/regress.sh 40           # 40 seeds per profile
#
# When a run fails, the seed printed on its line reproduces it EXACTLY:
#   vvp build/regress.vvp +SEED=<n> +CYCLES=3000 +WR=<w> +RD=<r>
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

N=${1:-4}
DUT=${DUT:-fifo}

iverilog -g2005 -o build/regress.vvp -DDUT=$DUT -DDUTNAME="\"$DUT\"" \
         rtl/fifo.v rtl/fifo_bugs.v tb/tb_v3_random.v || exit 1

pass=0; fail=0; failed_seeds=""
echo "regression on $DUT : $N seeds x 3 profiles"
echo
printf '  %-14s %-8s %-8s %s\n' profile seed cycles result
printf '  %s\n' "------------------------------------------------------"

for prof in "balanced 55 45" "write-heavy 85 30" "read-heavy 30 85"; do
    set -- $prof
    name=$1; w=$2; r=$3
    for s in $(seq 1 $N); do
        out=$(vvp build/regress.vvp +SEED=$s +CYCLES=3000 +WR=$w +RD=$r 2>/dev/null)
        if echo "$out" | grep -q "^PASS"; then
            printf '  %-14s %-8s %-8s %s\n' "$name" "$s" 3000 pass
            pass=$((pass+1))
        else
            printf '  %-14s %-8s %-8s %s\n' "$name" "$s" 3000 FAIL
            echo "$out" | grep -E "^  FAIL|^FAIL" | head -3 | sed 's/^/      /'
            failed_seeds="$failed_seeds $name/$s"
            fail=$((fail+1))
        fi
    done
done

echo
echo "  $pass passed, $fail failed"
if [ $fail -ne 0 ]; then
    echo "  reproduce with: vvp build/regress.vvp +SEED=<seed> +WR=<w> +RD=<r>"
    echo "  failing runs:$failed_seeds"
    exit 1
fi
echo "  REGRESSION CLEAN"
