// The intended 3-stage shift register: NON-BLOCKING assignments.
// All three right-hand sides are evaluated with the OLD values, then all
// three left-hand sides are updated. That is exactly what three flip-flops
// in a chain do, so the code and the hardware agree.
module shift_nb (input clk, input din, output reg [2:0] q);
    always @(posedge clk) begin
        q[0] <= din;
        q[1] <= q[0];
        q[2] <= q[1];
    end
endmodule
