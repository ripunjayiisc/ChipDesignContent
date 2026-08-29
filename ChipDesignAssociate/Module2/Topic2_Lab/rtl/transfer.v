// ---------------------------------------------------------------------------
// transfer.v  -  what "register transfer level" literally means.
//
// The name is not decoration. An RTL description says two things and nothing
// else:
//
//   1. WHICH REGISTERS EXIST                     (here: x, y, z, acc)
//   2. WHAT TRANSFERS INTO EACH ONE, EACH EDGE   (the <= lines below)
//
// Everything between the registers - the adder, the shifter, the comparison -
// is combinational logic that has one clock period to settle. You never say
// how long it takes or what gates it uses. You say what value lands in which
// register on the next edge.
//
// Read the always block as a table of simultaneous transfers, not as a
// sequence of statements. All four assignments use the OLD values of x, y, z
// and acc, and all four land at the same instant. That is what <= means.
// ---------------------------------------------------------------------------
module transfer (
    input            clk,
    input            rst,
    input      [7:0] din,
    output     [7:0] result,
    output     [7:0] r_x, r_y, r_z, r_acc      // exposed so you can watch them
);

    reg [7:0] x, y, z, acc;

    always @(posedge clk) begin
        if (rst) begin
            x <= 8'd0;  y <= 8'd0;  z <= 8'd0;  acc <= 8'd0;
        end else begin
            x   <= din;                 // input          -> x
            y   <= x + 8'd1;            // x, plus logic  -> y
            z   <= y << 1;              // y, plus logic  -> z
            acc <= acc + z;             // acc and z      -> acc
        end
    end

    assign result = acc;
    assign r_x = x;  assign r_y = y;  assign r_z = z;  assign r_acc = acc;

endmodule
