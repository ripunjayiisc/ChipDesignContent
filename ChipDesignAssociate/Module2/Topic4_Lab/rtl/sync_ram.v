// ---------------------------------------------------------------------------
// sync_ram.v  -  single-port synchronous RAM  (Lab L4)
//
// The REGISTERED read is what makes this inferable as a block RAM. Change
// `q <= mem[addr];` to `assign q = mem[addr];` and the tool will build it out
// of flip-flops and multiplexers instead - orders of magnitude larger.
//
// Read-during-write behaviour here is READ-OLD: q gets the value that was in
// mem[addr] before this cycle's write. Vendors also offer read-new; if it
// matters to you, say so explicitly rather than relying on the default.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module sync_ram #(
    parameter integer W     = 8,
    parameter integer DEPTH = 256
)(
    input  wire                     clk,
    input  wire                     we,
    input  wire [$clog2(DEPTH)-1:0] addr,
    input  wire [W-1:0]             din,
    output reg  [W-1:0]             q
);

    reg [W-1:0] mem [0:DEPTH-1];

    always @(posedge clk) begin
        if (we) mem[addr] <= din;
        q <= mem[addr];                 // registered read -> block RAM
    end

endmodule

`default_nettype wire
