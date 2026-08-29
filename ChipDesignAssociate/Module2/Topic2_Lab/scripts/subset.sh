#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# subset.sh  -  which Verilog constructs actually synthesise?
#
# "Verilog is not a programming language" stays a slogan until you watch a
# synthesiser refuse to build something. This runs each construct in subset/
# through Yosys and reports what came out: whether it synthesised at all, the
# cell count, whether a LATCH was inferred, and the tool's own words.
#
# The column to watch is LATCH. An inferred latch is not an error - the tool
# builds one happily, mentions it in a log nobody reads, and hands you a design
# with a level-sensitive memory element you never asked for.
# ---------------------------------------------------------------------------
set -u
cd "$(dirname "$0")/.."
mkdir -p build

# s12, s13 and s14 are fixtures for the LINTER, not constructs under study:
# s12 breaks several rules at once, s13 has two drivers, and s14 repeats s03's
# latch so that scripts/lint_check.sh has two independent latch cases to
# cross-check. Including them here would pad this table with rows that are not
# about the synthesisable subset.
for f in subset/s0*.v subset/s1[01]_*.v; do
    m=$(basename "$f" .v)
    yosys -p "read_verilog $f; synth -top $m; write_json build/${m}.json" \
          > "build/${m}_synth.log" 2>&1 || true
done

python3 - <<'PY'
import glob, json, os, re

print()
print("  %-22s %-8s %-6s %-7s %s"
      % ("construct", "synth", "cells", "latch", "what the tool said"))
print("  " + "-" * 88)

files = sorted(glob.glob("subset/s0*.v") + glob.glob("subset/s1[01]_*.v"))
for f in files:
    m = os.path.basename(f)[:-2]
    log = open("build/%s_synth.log" % m, errors="replace").read()
    js = "build/%s.json" % m

    err = re.search(r"ERROR:\s*(.+)", log)
    if err or not os.path.exists(js):
        msg = err.group(1).strip() if err else "no netlist produced"
        print("  %-22s %-8s %-6s %-7s %s" % (m, "REFUSED", "-", "-", msg[:46]))
        continue

    mod = list(json.load(open(js))["modules"].values())[0]
    types = {}
    for c in mod["cells"].values():
        types[c["type"]] = types.get(c["type"], 0) + 1
    latch = [t for t in types if "DLATCH" in t.upper() or t.startswith("$dlatch")]

    if latch:
        note = "inferred a LATCH: %s" % ", ".join(sorted(latch))
    elif len(mod["cells"]) == 0:
        note = "no logic at all - it is just wires"
    else:
        note = ", ".join("%s x%d" % (t.strip("$_"), n)
                         for t, n in sorted(types.items()))[:46]

    print("  %-22s %-8s %-6s %-7s %s"
          % (m, "OK", len(mod["cells"]), "YES" if latch else "no", note))
print()
PY
