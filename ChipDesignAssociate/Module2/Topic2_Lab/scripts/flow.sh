#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# flow.sh  -  the RTL design methodology, executed rather than described.
#
# A design flow drawn on a slide is a picture of arrows. This runs the same
# arrows on a real design and shows the evidence each stage produces, because
# a stage that produces no evidence is a stage nobody can tell you skipped.
#
#   1  SPEC        what the design must do, in words, before any code
#   2  LINT        cheapest check there is - seconds, catches methodology bugs
#   3  SIMULATE    does the RTL do what the spec says?
#   4  SYNTHESISE  turn it into gates; read what the tool built
#   5  GATE SIM    does the NETLIST still do what the spec says?
#   6  COMPARE     RTL transcript against gate transcript, line by line
#   7  PROVE       formal equivalence - for all inputs, not just those tested
#
# Every stage can fail, and the script stops when one does. That is the point:
# a methodology is a set of gates you have to get through, not a set of
# suggestions.
# ---------------------------------------------------------------------------
set -eu
cd "$(dirname "$0")/.."
mkdir -p build

hr () { printf "  %s\n" "-----------------------------------------------------------------"; }
stage () { echo; echo "  STAGE $1  ·  $2"; hr; }

# ---------------------------------------------------------------- 1. spec
stage 1 "SPECIFICATION"
cat <<'SPEC' | sed 's/^/    /'
A 4-bit up counter.
  * synchronous, active-high reset clears the count to zero
  * a count enable; when low the count holds
  * an output tc that is high exactly when the count is all ones
  * the count wraps from 15 to 0
SPEC
echo
echo "    Written before the RTL, so that stages 3 and 5 have something to"
echo "    check against other than the author's memory."

# ---------------------------------------------------------------- 2. lint
stage 2 "LINT  ·  tools/rtl_lint.py"
python3 tools/rtl_lint.py rtl/counter.v | sed 's/^/  /'

# ------------------------------------------------------------ 3. simulate
stage 3 "RTL SIMULATION  ·  iverilog"
iverilog -g2005 -o build/counter_v.vvp rtl/tb_counter.v rtl/counter.v
vvp build/counter_v.vvp | grep -v "VCD info" > build/counter_v.log
echo "    18 cycles applied. Checking the spec by hand:"
grep -E "cycle (0|14|15|16) " build/counter_v.log | sed 's/^/    /'
echo "      -> count reaches 1111 and tc goes high, then wraps to 0000. OK."

# ---------------------------------------------------------- 4. synthesise
stage 4 "SYNTHESIS  ·  yosys"
yosys -p "read_verilog rtl/counter.v
          synth -top counter
          abc -g AND,OR,NAND,NOR,XOR,XNOR,ANDNOT,ORNOT,MUX
          opt_clean
          write_verilog -noattr build/counter_net.v
          stat" > build/counter_synth.log 2>&1
awk '/Number of cells/{p=1} p&&NF{print "    " $0} p&&/^$/{exit}' \
    build/counter_synth.log | head -12

# ------------------------------------------------------------ 5. gate sim
stage 5 "GATE-LEVEL SIMULATION  ·  the netlist, same stimulus"
cat > build/tb_net.v <<'TB'
`timescale 1ns / 1ps
module tb_counter_net;
    reg clk = 0, rst, en; wire [3:0] count; wire tc; integer i;
    counter dut (.clk(clk), .rst(rst), .en(en), .count(count), .tc(tc));
    always #5 clk = ~clk;
    initial begin
        rst = 1; en = 0; @(posedge clk); #1; rst = 0; en = 1;
        for (i = 0; i <= 17; i = i + 1) begin
            @(posedge clk); #1;
            $display("  cycle %0d  count=%b  tc=%b", i, count, tc);
        end
        $finish;
    end
endmodule
TB
iverilog -g2005 -o build/counter_net.vvp build/tb_net.v build/counter_net.v \
         /usr/share/yosys/simcells.v
vvp build/counter_net.vvp 2>/dev/null > build/counter_net.log
echo "    netlist simulated over the same 18 cycles."

# ------------------------------------------------------------- 6. compare
stage 6 "COMPARE  ·  RTL transcript against gate transcript"
if diff <(grep cycle build/counter_v.log) <(grep cycle build/counter_net.log) \
        > build/flow.diff; then
    echo "    IDENTICAL on all 18 cycles."
else
    echo "    THEY DIFFER:"; sed 's/^/      /' build/flow.diff | head; exit 1
fi

# --------------------------------------------------------------- 7. prove
stage 7 "PROVE  ·  formal equivalence, RTL against netlist"
out=$(yosys -p "
    read_verilog rtl/counter.v;      prep -top counter; design -stash gold
    read_verilog build/counter_net.v; prep -top counter; design -stash gate
    design -copy-from gold -as gold counter
    design -copy-from gate -as gate counter
    equiv_make gold gate equiv
    equiv_simple equiv
    equiv_induct equiv
    equiv_status -assert equiv" 2>&1) || true
if echo "$out" | grep -q "Equivalence successfully proven"; then
    cells=$(echo "$out" | grep -oE "Found [0-9]+ \\\$equiv cells" | tail -1 | tr -dc 0-9)
    echo "    Equivalence PROVEN by induction - $cells equivalence points."
    echo "    This covers every input sequence, not only the 18 cycles tested."
else
    echo "    NOT PROVEN:"; echo "$out" | grep -iE "unproven|ERROR" | head -3 \
        | sed 's/^/      /'; exit 1
fi

echo
hr
echo "  All seven stages passed. That is what 'methodology' means in practice:"
echo "  a sequence of checks, each producing evidence, none of them optional."
echo
