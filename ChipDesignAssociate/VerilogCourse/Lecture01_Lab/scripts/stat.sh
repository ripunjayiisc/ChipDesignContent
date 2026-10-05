#!/bin/bash
# stat.sh <script.ys> - run a yosys script and print only the FINAL statistics
# block.  yosys prints statistics more than once when a script contains several
# passes, and only the last block describes the finished netlist.
set -e
yosys -s "$1" 2>&1 | awk '
  /^=== .* ===$/ { buf = ""; capture = 1; next }
  capture && /^End of script/ { capture = 0 }
  capture { buf = buf $0 "\n" }
  END { printf "%s", buf }
' | sed '/^$/d'
