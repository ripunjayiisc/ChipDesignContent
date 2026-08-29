#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# hazard_synth.sh  -  what does a synthesiser do with a hazard fix?
#
# The consensus term that makes a circuit hazard-free is, by construction,
# logically redundant. A logic optimiser exists to delete redundancy. This
# script runs both versions through Yosys and prints what came out.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

echo
echo "=== does synthesis preserve a hazard fix? ==="
echo
for m in hz_rtl_plain hz_rtl_fixed; do
    yosys -p "read_verilog rtl/hz_rtl.v
              synth -top $m
              abc -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
              opt_clean
              write_json build/${m}.json" > "build/${m}_synth.log" 2>&1
done

python3 - <<'PY'
import json

def cells(m):
    d = json.load(open("build/%s.json" % m))["modules"][m]
    t = {}
    for c in d["cells"].values():
        t[c["type"]] = t.get(c["type"], 0) + 1
    return len(d["cells"]), t

a = cells("hz_rtl_plain")
b = cells("hz_rtl_fixed")
print("  RTL written                      cells  gates")
print("  -------------------------------  -----  ---------------")
print("  f = a&~b | b&c                   %5d  %s" % (a[0], dict(a[1])))
print("  f = a&~b | b&c | a&c   (fixed)   %5d  %s" % (b[0], dict(b[1])))
print()
if a == b:
    print("  The two netlists are IDENTICAL. The consensus term was deleted.")
else:
    print("  The netlists differ - the redundant term survived on this tool version.")
print()
print("  And note WHAT it built: a single multiplexer. A B' + B C is exactly")
print("  B ? C : A, and the optimiser saw that before it saw anything else.")
print()
print("  Consequences you have to live with:")
print("    * You cannot express hazard-freedom in RTL and expect it to survive.")
print("      Redundancy is precisely what the optimiser is paid to remove.")
print("    * Where hazard-freedom is genuinely required - an asynchronous")
print("      circuit, or logic feeding a clock, a latch enable or an")
print("      asynchronous reset - you must protect it structurally: a")
print("      dont_touch / keep attribute, an instantiated library cell, or a")
print("      module the optimiser is told not to flatten.")
print("    * And once it is a library cell rather than your gates, whether it")
print("      glitches is decided by that cell's internals, not by your cover.")
PY
