// GOOD - a clocked block written the way RTL methodology asks for.
// Non-blocking assignments (<=) inside a clocked block; synchronous reset.
module s02_ok_seq (input clk, input rst, input [7:0] d, output reg [7:0] q);
    always @(posedge clk) begin
        if (rst) q <= 8'd0;
        else     q <= d;
    end
endmodule
