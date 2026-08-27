// ---------------------------------------------------------------------------
// hold_fixed.v  -  the same two flip-flops, with real delay on the data path.
//
// A hold violation is fixed by making the DATA path slower. That is the
// opposite of every other timing fix, and it is why hold problems feel wrong
// the first time you meet one.
//
// READ THIS BEFORE COPYING THE STYLE
// ----------------------------------
// In a real flow you do NOT fix hold in RTL. You fix it either by
//
//   (a) improving the clock tree so the skew goes away, or
//   (b) letting the place-and-route tool insert delay cells, which it does
//       automatically once it knows the real skew and the real wire delays.
//
// You cannot write a buffer chain in RTL and expect it to survive: a
// synthesiser deletes redundant buffers immediately, and it is right to.
// Try it - put four (* keep *) buffers on the path and count the cells.
//
// So this module gets its delay from XOR gates whose second input is a real
// port, dly_sel, which the caller ties to zero. The tool cannot prove dly_sel
// is constant, so it cannot remove the gates, and dout still equals q1 delayed
// by one cycle. This exists so the lab can DEMONSTRATE the arithmetic of a
// hold fix. It is not a style to copy.
// ---------------------------------------------------------------------------
`default_nettype none

module hold_fixed (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       din,
    input  wire [1:0] dly_sel,   // tie to 2'b00 - see the note above
    output reg        dout
);
    reg  q1;
    wire d0, d1;

    assign d0 = q1 ^ dly_sel[0];
    assign d1 = d0 ^ dly_sel[1];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q1   <= 1'b0;
            dout <= 1'b0;
        end else begin
            q1   <= din;
            dout <= d1;
        end
    end
endmodule

`default_nettype wire
