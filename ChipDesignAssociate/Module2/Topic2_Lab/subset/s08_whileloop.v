// BAD for synthesis - a loop whose trip count depends on the data.
// The tool has to build a fixed amount of hardware. It cannot build "however
// many iterations this value happens to need". To do this in hardware you
// build a state machine that takes several clock cycles - which is a design
// decision you must make explicitly, not something a compiler can invent.
module s08_whileloop (input [7:0] d, output reg [3:0] leading);
    reg [7:0] t;
    always @* begin
        leading = 0;
        t = d;
        while (t[7] == 1'b0 && t != 0) begin
            t = t << 1;
            leading = leading + 1'b1;
        end
    end
endmodule
