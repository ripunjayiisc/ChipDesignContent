// BAD - an INFERRED LATCH, and the single most common RTL methodology bug.
// When en = 0 the code does not say what y should be, so the tool must build
// something that REMEMBERS the old value. That something is a level-sensitive
// latch, which you did not ask for and almost certainly do not want.
module s03_latch (input en, input d, output reg y);
    always @* begin
        if (en) y = d;          // <-- no else
    end
endmodule
