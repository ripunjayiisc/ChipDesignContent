// ---------------------------------------------------------------------------
// tb_hazard.v  -  an automatic glitch detector.
//
// Looking for glitches by eye in a waveform viewer does not scale and does not
// go in a regression. This testbench walks every single-variable input
// transition, counts how many times the output changes, and compares that with
// how many times it SHOULD change:
//
//     steady value before == steady value after   ->  expect 0 changes
//     steady value before != steady value after   ->  expect 1 change
//
// More changes than expected is a glitch. A static hazard shows up as 2 extra
// changes on a transition that should have had none; a dynamic hazard as 2
// extra on a transition that should have had one.
//
// Build with -DDUT=<module name>, e.g.
//     iverilog -g2005 -DDUT=hz_static1 -o build/hz hazards/tb_hazard.v \
//              hazards/hz_static1.v
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

`ifndef DUT
 `define DUT hz_static1
`endif
`ifndef DUTNAME
 `define DUTNAME "DUT"
`endif

module tb_hazard;

    reg  a, b, c;
    wire f;

    // how long to wait for everything to settle. Longer than the slowest
    // path in any of the designs under test.
    localparam SETTLE = 40;

    integer changes;          // output transitions inside the window
    integer expected;
    integer glitches;         // transitions that glitched
    integer transitions;      // transitions examined
    integer worst_extra;      // the largest number of surplus changes seen
    reg     f_before, f_after;
    reg     watching;

    `DUT dut (.a(a), .b(b), .c(c), .f(f));

    // the counter: only armed while a transition is being observed
    always @(f) if (watching) changes = changes + 1;

    // apply one single-variable change and judge it
    task automatic step (input [2:0] start, input integer bit_index);
        reg [2:0] s;
        reg [2:0] e;
        begin
            s = start;
            e = start ^ (3'b001 << bit_index);

            // settle at the starting point with the counter disarmed
            watching = 0;
            {a, b, c} = s;
            #SETTLE;
            f_before = f;

            // arm, make the change, watch
            changes  = 0;
            watching = 1;
            {a, b, c} = e;
            #SETTLE;
            watching = 0;
            f_after  = f;

            expected    = (f_before === f_after) ? 0 : 1;
            transitions = transitions + 1;

            if (changes > expected) begin
                glitches = glitches + 1;
                if (changes - expected > worst_extra)
                    worst_extra = changes - expected;
                $display("  ABC %s%s%s -> %s%s%s  (%s changed)   f: %b -> %b   changes=%0d expected=%0d   %s",
                         s[2] ? "1" : "0", s[1] ? "1" : "0", s[0] ? "1" : "0",
                         e[2] ? "1" : "0", e[1] ? "1" : "0", e[0] ? "1" : "0",
                         (bit_index == 2) ? "A" : (bit_index == 1) ? "B" : "C",
                         f_before, f_after, changes, expected,
                         (expected == 0) ? "STATIC GLITCH" : "DYNAMIC GLITCH");
            end
        end
    endtask

    integer i, j;
    reg [7:0] truth;          // steady-state f for ABC = 000 .. 111

    initial begin
        $dumpfile("build/hazard.vcd");
        $dumpvars(0, tb_hazard);

        glitches    = 0;
        transitions = 0;
        worst_extra = 0;
        watching    = 0;

        $display("");
        $display("  === glitch detector: %s ===", `DUTNAME);
        $display("  walking every single-variable input transition (ABC)");
        $display("");

        for (i = 0; i < 8; i = i + 1)
            for (j = 0; j < 3; j = j + 1)
                step(i[2:0], j);

        // record the settled truth table, so that a "fix" which quietly
        // changes the function cannot pass as a fix
        watching = 0;
        for (i = 0; i < 8; i = i + 1) begin
            {a, b, c} = i[2:0];
            #SETTLE;
            truth[i] = f;
        end
        $display("  TRUTH(ABC=000..111) = %b", truth);

        $display("");
        $display("  transitions examined : %0d", transitions);
        $display("  transitions glitching: %0d", glitches);
        if (glitches == 0)
            $display("  RESULT: CLEAN - no glitch on any single-variable change");
        else
            $display("  RESULT: %0d GLITCH(ES), worst had %0d surplus change(s)",
                     glitches, worst_extra);
        $display("");
        $finish;
    end

endmodule
