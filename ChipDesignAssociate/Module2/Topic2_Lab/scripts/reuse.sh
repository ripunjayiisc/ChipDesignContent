#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# reuse.sh  -  parameters, hierarchy and generate, with the flip-flop count
# proving that the generate loop really does build N stages.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

iverilog -g2012 -o build/reuse.vvp rtl/reuse.v rtl/tb_reuse.v
vvp build/reuse.vvp | grep -v "VCD info"

echo "  --- does the generate loop actually scale? ---"
echo
echo "  delayline #(W=8, N) synthesised at four different depths:"
echo
for n in 1 2 4 8; do
    cat > build/dl_$n.v <<VEOF
\`include "rtl/reuse.v"
module dl_$n (input clk, input rst, input en,
              input [7:0] din, output [7:0] dout);
    delayline #(.W(8), .N($n)) u (.clk(clk), .rst(rst), .en(en),
                                  .din(din), .dout(dout));
endmodule
VEOF
    ./scripts/stat.sh "  N = $n" dl_$n build/dl_$n.v
done
echo
echo "  8 flip-flops per stage, exactly N stages, no loop left anywhere in"
echo "  the netlist. 'generate' is a compile-time instruction to the"
echo "  elaborator, not a construct that survives into hardware."
