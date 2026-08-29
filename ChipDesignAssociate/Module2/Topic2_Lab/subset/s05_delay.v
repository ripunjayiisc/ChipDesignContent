// BAD for synthesis - a delay control inside RTL.
// #5 is a simulation instruction. Silicon has no way to wait five time units;
// the delay a real gate has is decided by the library and the layout, not by
// your source. Synthesis ignores this and you get logic that behaves
// differently from the simulation you signed off.
module s05_delay (input a, output reg y);
    always @* begin
        #5 y = ~a;
    end
endmodule
