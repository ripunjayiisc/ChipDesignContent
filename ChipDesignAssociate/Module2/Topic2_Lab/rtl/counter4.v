// ---------------------------------------------------------------------------
// counter4.v  -  THE RUNNING EXAMPLE.
//
// One small design carries every idea in this topic. It starts here as four
// flip-flops and an incrementer, and by the end of the lab it has grown a
// terminal-count output, an enable, a parameterised width, a hierarchy, and a
// controller. Nothing new has to be introduced to explain the next idea,
// because the design is already familiar.
//
//   Lab 3   this file: code -> simulate -> lint -> synthesise -> gate-sim
//   Lab 4   its controller becomes an FSM (fsm/traffic.v)
//   Lab 7   parameterised and instantiated twice (rtl/counter_pair.v)
//
// Read the always block as the RTL definition in miniature: ONE register
// (count), and ONE statement saying what transfers into it on each edge.
// ---------------------------------------------------------------------------
module counter4 (
    input            clk,
    input            rst_n,      // asynchronous, active LOW
    input            en,
    output reg [3:0] count,
    output           tc          // terminal count: high for one cycle at 15
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)     count <= 4'd0;
        else if (en)    count <= count + 4'd1;
    end

    assign tc = en & (count == 4'd15);

endmodule
