// ---------------------------------------------------------------------------
// counter.v  -  the same design as vhdl/counter.vhd, in Verilog.
//
// A 4-bit up counter with synchronous reset and a count enable. Chosen because
// it is small enough to read side by side with the VHDL and still contains
// every construct that matters: a clocked process, a reset, an enable, a
// vector, and a wrap.
// ---------------------------------------------------------------------------
module counter #(parameter WIDTH = 4) (
    input                    clk,
    input                    rst,      // synchronous, active high
    input                    en,
    output reg [WIDTH-1:0]   count,
    output                   tc        // terminal count: all ones
);

    always @(posedge clk) begin
        if (rst)      count <= {WIDTH{1'b0}};
        else if (en)  count <= count + 1'b1;
    end

    assign tc = &count;

endmodule
