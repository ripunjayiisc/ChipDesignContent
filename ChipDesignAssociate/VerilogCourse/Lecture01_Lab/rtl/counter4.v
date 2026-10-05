// counter4 - a 4-bit up counter, written BEHAVIOURALLY.
//
// Nothing here says which gates to use, or how many. It says only what the
// output must be after each rising clock edge. Choosing the gates is the
// synthesis tool's job - which is the whole point of Lecture 01.
module counter4 (
    input  wire       clk,
    input  wire       rst,     // synchronous, active high
    output reg  [3:0] q
);
    always @(posedge clk) begin
        if (rst) q <= 4'd0;
        else     q <= q + 4'd1;
    end
endmodule
