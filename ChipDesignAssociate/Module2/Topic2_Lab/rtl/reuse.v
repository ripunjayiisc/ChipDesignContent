// ---------------------------------------------------------------------------
//  reuse.v  -  HIERARCHY, PARAMETERS and GENERATE: the three things that turn
//              a working module into a reusable IP.
//
//  Module 2's terminal outcome asks you to "design and develop IPs" and to
//  "emulate, debug and characterise REUSABLE IPs".  Reusable means one source
//  file that covers a family of widths and depths, not fourteen copies with
//  the numbers edited.  Three language features do all the work:
//
//     parameter    a compile-time constant the instantiator can override
//     hierarchy    a module instantiated inside another module
//     generate     a compile-time loop that builds N copies of a structure
//
//  None of them exist in the hardware.  They are all elaborated away before
//  synthesis sees a single gate.
// ---------------------------------------------------------------------------

// ---- a width-parameterised register with enable and synchronous reset -----
module preg #(
    parameter W = 8
)(
    input              clk,
    input              rst,      // SYNCHRONOUS, active high
    input              en,
    input      [W-1:0] d,
    output reg [W-1:0] q
);
    always @(posedge clk) begin
        if (rst)      q <= {W{1'b0}};
        else if (en)  q <= d;
    end
endmodule


// ---- the counter of Lab 3, now parameterised in width --------------------
// Compare this with rtl/counter4.v: same behaviour, but the width, the reset
// value and the terminal count all follow the parameter.  Writing {W{1'b1}}
// instead of 4'd15 is what makes it reusable.
module counter_n #(
    parameter W = 4
)(
    input              clk,
    input              rst_n,
    input              en,
    output reg [W-1:0] count,
    output             tc
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)  count <= {W{1'b0}};
        else if (en) count <= count + {{(W-1){1'b0}}, 1'b1};
    end
    assign tc = en & (count == {W{1'b1}});
endmodule


// ---- a delay line: N registers in a chain, built by a GENERATE loop -------
// The `for` here is not a loop in hardware.  It is an instruction to the
// elaborator: "make N instances of preg and wire stage k's output to stage
// k+1's input".  After elaboration there is no loop left, only N registers.
module delayline #(
    parameter W = 8,
    parameter N = 4
)(
    input          clk,
    input          rst,
    input          en,
    input  [W-1:0] din,
    output [W-1:0] dout
);
    // one extra element so tap[0] can be the input
    wire [W-1:0] tap [0:N];
    assign tap[0] = din;

    genvar k;
    generate
        for (k = 0; k < N; k = k + 1) begin : stage
            preg #(.W(W)) u_reg (
                .clk(clk), .rst(rst), .en(en),
                .d(tap[k]), .q(tap[k+1]));
        end
    endgenerate

    assign dout = tap[N];
endmodule


// ---- one parent, two instances of the SAME module, different parameters --
// The cascade wiring - the wide counter only advances when the narrow one
// wraps - is the classic prescaler.  Note that `en_slow` is a wire between
// two instances, which is all that "hierarchy" means.
module counter_pair #(
    parameter WFAST = 4,
    parameter WSLOW = 8
)(
    input                  clk,
    input                  rst_n,
    input                  en,
    output [WFAST-1:0]     fast,
    output [WSLOW-1:0]     slow,
    output                 slow_tc
);
    wire en_slow;

    counter_n #(.W(WFAST)) u_fast (
        .clk(clk), .rst_n(rst_n), .en(en),
        .count(fast), .tc(en_slow));

    counter_n #(.W(WSLOW)) u_slow (
        .clk(clk), .rst_n(rst_n), .en(en_slow),
        .count(slow), .tc(slow_tc));
endmodule
