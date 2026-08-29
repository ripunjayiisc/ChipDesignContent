// The same three lines with BLOCKING assignments - and it is not a shift
// register any more. Each line completes before the next one starts, so
// q[0] already holds the NEW value when line 2 reads it. din races all the
// way to q[2] in a single clock cycle.
//
// Note what is NOT wrong here: the code compiles, simulates, and synthesises
// without a single warning. Only the behaviour is wrong. That is why the
// blocking/non-blocking rule is a methodology rule rather than a tool check.
module shift_bl (input clk, input din, output reg [2:0] q);
    always @(posedge clk) begin
        q[0] = din;
        q[1] = q[0];
        q[2] = q[1];
    end
endmodule
