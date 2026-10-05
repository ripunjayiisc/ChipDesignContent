#!/usr/bin/env python3
"""vcd_q.py <file.vcd> <signal> - print "<time in ns>  <value>" for one signal.

Icarus and GHDL write their VCDs with different timescales and different
identifier codes, so the raw files cannot be diffed directly. This normalises
both to nanoseconds and to plain binary, which makes the two languages
directly comparable.
"""
import re
import sys

UNIT = {"s": 1e0, "ms": 1e-3, "us": 1e-6, "ns": 1e-9, "ps": 1e-12, "fs": 1e-15}


def main(path, signal, after=0):
    scale = 1e-9
    code = None
    width = 1
    out = []
    now = 0          # femtoseconds
    with open(path) as fh:
        text = fh.read()

    m = re.search(r"\$timescale\s+(\d+)\s*([munpf]?s)\s*\$end", text)
    if m:
        scale = int(m.group(1)) * UNIT[m.group(2)]

    for m in re.finditer(r"\$var\s+\S+\s+(\d+)\s+(\S+)\s+(\S+?)(?:\s*\[[^\]]*\])?\s+\$end",
                         text):
        if m.group(3) == signal:
            width, code = int(m.group(1)), m.group(2)
            break
    if code is None:
        sys.exit("no signal %r in %s" % (signal, path))

    def expand(val):
        """Apply the VCD left-extension rule: a vector is padded on the left
        with 0, except that a value starting with x or z extends with that
        character instead."""
        val = val.lower()
        pad = val[0] if val[:1] in ("x", "z") else "0"
        return val.rjust(width, pad)

    body = text[text.index("$enddefinitions"):]
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            # keep time as an integer number of femtoseconds: comparing
            # floating-point times across two different timescales is not
            # reliable, and 15 ns must mean 15 ns in both files
            now = int(round(int(line[1:]) * scale / 1e-15))
        elif line.startswith(("b", "B")):
            val, _, ident = line[1:].partition(" ")
            if ident == code:
                out.append((now, expand(val)))
        elif line[1:] == code:
            out.append((now, line[0].lower()))

    for t, v in out:
        if t >= after:
            print("%10.3f ns   %s" % (t / 1e6, v))


if __name__ == "__main__":
    main(sys.argv[1],
         sys.argv[2] if len(sys.argv) > 2 else "q",
         int(round(float(sys.argv[3]) * 1e6)) if len(sys.argv) > 3 else 0)
