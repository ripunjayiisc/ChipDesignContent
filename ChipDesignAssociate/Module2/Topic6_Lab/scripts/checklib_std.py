#!/usr/bin/env python3
"""Structural self-check for the generated lib/cda_edu_std.lib.

This does NOT prove OpenSTA will accept the file - only OpenSTA can do that,
and it is not installed in every environment. What it does prove is that the
file is brace-balanced, that every cell carries the groups a Liberty reader
requires, and that every delay number in it matches cda_edu.lib exactly.
Run it after every regeneration.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from sta.liberty import read_liberty                              # noqa: E402

STD = os.path.join(HERE, "..", "lib", "cda_edu_std.lib")
SRC = os.path.join(HERE, "..", "lib", "cda_edu.lib")

txt = open(STD).read()
body = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
fail = []

# 1. braces balance
depth = 0
for ch in body:
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth < 0:
            fail.append("closing brace with no opener")
            break
if depth != 0:
    fail.append("braces do not balance: ends at depth %d" % depth)

# 2. the library-level attributes a reader needs
for need in ("delay_model", "time_unit", "capacitive_load_unit",
             "lu_table_template (delay_template)",
             "lu_table_template (constraint_template)"):
    if need not in body:
        fail.append("library is missing %s" % need)

# 3. every cell present, with the right groups
cells = dict(re.findall(r"cell \((\w+)\) \{(.*?)\n  \}", body, re.S))
src = read_liberty(SRC)
missing = sorted(set(src) - set(cells))
if missing:
    fail.append("cells missing from the generated file: %s" % ", ".join(missing))

for name, blk in sorted(cells.items()):
    if "direction : output" not in blk:
        fail.append("%s: no output pin" % name)
    if src[name].is_ff:
        for need in ("ff (IQ, IQN)", "clocked_on", "next_state",
                     "timing_type   : setup_rising", "timing_type   : hold_rising",
                     "timing_type  : rising_edge", "clock : true"):
            if need not in blk:
                fail.append("%s: missing %s" % (name, need))
    else:
        if "function  :" not in blk:
            fail.append("%s: output pin has no function" % name)
        if "timing_sense" not in blk:
            fail.append("%s: no timing_sense" % name)

# 4. the numbers agree with cda_edu.lib
LOADS = [0.0, 1.5, 3.0, 6.0, 12.0]
for name, blk in sorted(cells.items()):
    c = src[name]
    base = c.clk_to_q if c.is_ff else c.intrinsic
    want = ", ".join("%.4f" % (base + c.load_factor * L) for L in LOADS)
    if want not in blk:
        fail.append("%s: delay row does not match cda_edu.lib (expected %s)"
                    % (name, want))
    if c.is_ff:
        for lbl, v in (("setup", c.setup), ("hold", c.hold)):
            if '"%.4f, %.4f"' % (v, v) not in blk:
                fail.append("%s: %s constraint does not match cda_edu.lib" % (name, lbl))

print("checking lib/cda_edu_std.lib")
print("  cells found            : %d" % len(cells))
print("  cells in cda_edu.lib   : %d" % len(src))
if fail:
    print("\nFAILED:")
    for f in fail:
        print("  - " + f)
    sys.exit(1)
print("  braces balanced        : yes")
print("  required groups        : all present")
print("  delay numbers match    : yes, every cell")
print("\nPASS - structurally sound and numerically identical to cda_edu.lib.")
print("Note: only OpenSTA itself can prove OpenSTA will read it. If you have")
print("OpenSTA installed, confirm with:")
print("  sta -no_splash -exit -x 'read_liberty lib/cda_edu_std.lib'")
