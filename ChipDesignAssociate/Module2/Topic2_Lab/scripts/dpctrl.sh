#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# dpctrl.sh  -  datapath + controller, simulated and then synthesised as a
# hierarchy so you can see the two halves as separate objects in the netlist.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

iverilog -g2012 -o build/accum.vvp rtl/datapath_ctrl.v rtl/tb_datapath_ctrl.v
vvp build/accum.vvp | grep -v "VCD info"

echo "  --- the hierarchy the synthesiser sees ---"
echo
yosys -p "read_verilog rtl/datapath_ctrl.v; hierarchy -top accum_top; \
          proc; opt; stat" > build/accum_hier.log 2>&1
# strip Yosys's internal $paramod$<hash>\ prefix so the names read normally
awk '/^=== /{p=1} p' build/accum_hier.log \
    | grep -E "^=== |Number of cells:|accum_" \
    | sed -E 's/\$paramod\$[0-9a-f]+\\//' | sed 's/^/    /' | head -20
echo
./scripts/stat.sh "accum_ctrl   (controller)" accum_ctrl     rtl/datapath_ctrl.v
./scripts/stat.sh "accum_datapath (datapath)" accum_datapath rtl/datapath_ctrl.v
./scripts/stat.sh "accum_top    (both)"       accum_top      rtl/datapath_ctrl.v
echo
echo "  The controller is a handful of gates; the datapath is nearly all of"
echo "  the area. That ratio is why the two are kept apart: you re-time and"
echo "  re-width the expensive half without touching the half that decides."
