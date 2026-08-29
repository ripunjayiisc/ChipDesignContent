// ---------------------------------------------------------------------------
// LEVEL 1 of 4 : BEHAVIOURAL  (also called algorithmic)
//
// You describe WHAT the circuit computes, using the same arithmetic you would
// write in software. There is no mention of gates, wires, or structure. The
// tool is left to work out how to build it.
//
// This is the highest level of abstraction Verilog offers for synthesisable
// logic, and it is where almost all real RTL is written.
// ---------------------------------------------------------------------------
module fa_behav (input a, input b, input cin, output reg sum, output reg cout);

    always @* begin
        {cout, sum} = a + b + cin;    // just add the three bits up
    end

endmodule
