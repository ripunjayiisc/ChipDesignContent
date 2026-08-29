// ---------------------------------------------------------------------------
// tb_ladder.v  -  run all four abstraction levels side by side and prove they
// are the same circuit.
//
// The claim being tested is the central claim of this topic: the level of
// abstraction changes WHAT YOU WROTE, not WHAT IT DOES. Four descriptions that
// look nothing like each other must produce identical outputs on all eight
// input combinations.
//
// If that claim held only most of the time it would be useless, so the test is
// exhaustive: three inputs, eight patterns, no sampling.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_ladder;

    reg  a, b, cin;
    wire s_beh, c_beh, s_dfl, c_dfl, s_gat, c_gat, s_swi, c_swi;

    fa_behav    u_beh (.a(a), .b(b), .cin(cin), .sum(s_beh), .cout(c_beh));
    fa_dataflow u_dfl (.a(a), .b(b), .cin(cin), .sum(s_dfl), .cout(c_dfl));
    fa_gate     u_gat (.a(a), .b(b), .cin(cin), .sum(s_gat), .cout(c_gat));
    fa_switch   u_swi (.a(a), .b(b), .cin(cin), .sum(s_swi), .cout(c_swi));

    integer i, mismatches;
    reg [1:0] golden;                      // the reference: plain arithmetic

    initial begin
        $dumpfile("build/ladder.vcd");
        $dumpvars(0, tb_ladder);
        mismatches = 0;

        $display("");
        $display("  === one full adder, four levels of abstraction ===");
        $display("");
        $display("   a b cin | golden | behav  dataflow  gate  switch");
        $display("  ---------+--------+--------------------------------");

        for (i = 0; i < 8; i = i + 1) begin
            {a, b, cin} = i[2:0];
            #20;                            // let the transistor level settle
            golden = a + b + cin;

            $display("   %b %b  %b  |  %b_%b   |  %b_%b     %b_%b     %b_%b   %b_%b",
                     a, b, cin, golden[1], golden[0],
                     c_beh, s_beh, c_dfl, s_dfl, c_gat, s_gat, c_swi, s_swi);

            if ({c_beh, s_beh} !== golden) begin
                mismatches = mismatches + 1;
                $display("      ^ BEHAVIOURAL disagrees with the golden result");
            end
            if ({c_dfl, s_dfl} !== golden) begin
                mismatches = mismatches + 1;
                $display("      ^ DATAFLOW disagrees with the golden result");
            end
            if ({c_gat, s_gat} !== golden) begin
                mismatches = mismatches + 1;
                $display("      ^ GATE disagrees with the golden result");
            end
            if ({c_swi, s_swi} !== golden) begin
                mismatches = mismatches + 1;
                $display("      ^ SWITCH disagrees with the golden result");
            end
        end

        $display("");
        $display("  patterns applied : 8 of 8   (exhaustive - every possible input)");
        $display("  mismatches       : %0d", mismatches);
        if (mismatches == 0) begin
            $display("");
            $display("  PASS - all four descriptions are the same circuit.");
            $display("  Abstraction level changed WHAT YOU WROTE, not WHAT IT DOES.");
        end else
            $display("  FAIL - the four levels do not agree.");
        $display("");
        $finish;
    end

endmodule
