// tiny.v - the smallest design that has a real timing path.
// Used in the workbook to check the analyser's arithmetic by hand.
`default_nettype none
module tiny (input wire clk, input wire a, input wire b, output reg y);
    reg p, q;
    always @(posedge clk) begin
        p <= a & b;
        q <= p ^ a;
        y <= q | b;
    end
endmodule
`default_nettype wire
