// ---------------------------------------------------------------------------
// tb_mismatch.v  -  the most dangerous bug in the subset table, demonstrated.
//
// s04_incomplete_sens.v has a sensitivity list that names only `a`, while the
// block reads both `a` and `b`. Everyone is told this is bad. Almost nobody is
// shown WHY it is worse than a plain error.
//
// It is worse because it does not fail. It produces a design where the
// SIMULATION and the SILICON compute different things - so the testbench you
// signed off on was testing something that will never be built.
//
// This bench drives the same stimulus into the RTL and into the netlist that
// Yosys produced from that RTL, and compares them cycle by cycle.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_mismatch;

    reg  a, b;
    wire y_rtl, y_net;

    s04_incomplete_sens u_rtl (.a(a), .b(b), .y(y_rtl));   // what you simulated
    s04_net             u_net (.a(a), .b(b), .y(y_net));   // what will be built

    integer diffs;

    task show (input [255:0] what);
        begin
            #1;
            $display("   %-26s a=%b b=%b    RTL y=%b    NETLIST y=%b   %s",
                     what, a, b, y_rtl, y_net,
                     (y_rtl === y_net) ? "" : "<-- THEY DISAGREE");
            if (y_rtl !== y_net) diffs = diffs + 1;
        end
    endtask

    initial begin
        $dumpfile("build/mismatch.vcd");
        $dumpvars(0, tb_mismatch);
        diffs = 0;

        $display("");
        $display("  === same source, two different circuits ===");
        $display("");

        a = 0; b = 0;  show("start");
        a = 1;         show("change a  (list wakes)");
        b = 1;         show("change b  (list ASLEEP)");
        b = 0;         show("change b  (list ASLEEP)");
        a = 0;         show("change a  (list wakes)");
        b = 1;         show("change b  (list ASLEEP)");

        $display("");
        $display("  disagreements: %0d of 6", diffs);
        $display("");
        if (diffs > 0) begin
            $display("  The RTL only re-evaluates when `a` changes, so y goes stale");
            $display("  whenever b moves on its own. Synthesis ignored the list");
            $display("  entirely and built the AND gate you meant.");
            $display("");
            $display("  Your testbench was verifying a circuit that does not exist.");
        end else
            $display("  No disagreement - check that both modules were compiled.");
        $display("");
        $finish;
    end

endmodule
