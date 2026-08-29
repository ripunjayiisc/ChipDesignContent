#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# sta.sh  -  synthesise a design and run the timing analyser on it.
#
#   ./scripts/sta.sh <top> [sdc file] [extra sta.py args...]
#
#   ./scripts/sta.sh add_ripple constraints/add32.sdc --paths 3
#   ./scripts/sta.sh hold_demo  constraints/hold_skew.sdc --hold
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
top=$1; shift
sdc=${1:-}
if [ -n "${sdc}" ] && [ -f "${sdc}" ]; then shift; else sdc=""; fi

./scripts/synth.sh "$top" > /dev/null
if [ -n "$sdc" ]; then
    python3 sta/sta.py "build/${top}.json" "$top" -c "$sdc" "$@"
else
    python3 sta/sta.py "build/${top}.json" "$top" "$@"
fi
