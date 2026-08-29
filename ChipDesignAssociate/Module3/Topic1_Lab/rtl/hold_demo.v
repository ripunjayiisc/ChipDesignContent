// ---------------------------------------------------------------------------
// hold_demo.v  -  two flops back to back, with nothing between them.
//
// This is the shape of every hold violation there is: the launching flop's
// new value reaches the capturing flop's D pin almost immediately, and if the
// capture clock arrives late enough, it captures that NEW value on the edge
// that was supposed to capture the OLD one.
//
// Nothing here is unusual. A shift register looks exactly like this, and so
// does the second stage of any synchroniser.
// ---------------------------------------------------------------------------
module hold_demo (input clk, input din, output q);
    reg q1, q2;
    always @(posedge clk) begin
        q1 <= din;
        q2 <= q1;        // <- the path with no logic in it
    end
    assign q = q2;
endmodule
