// BAD - an incomplete sensitivity list.
// The block reads a and b but only wakes on a. In SIMULATION y is stale
// whenever b changes alone. Synthesis ignores the list and builds the AND
// anyway - so simulation and silicon DISAGREE, which is the worst outcome
// of all: your testbench passes and the chip does not work.
module s04_incomplete_sens (input a, input b, output reg y);
    always @(a) begin
        y = a & b;              // b is read but not in the list
    end
endmodule
