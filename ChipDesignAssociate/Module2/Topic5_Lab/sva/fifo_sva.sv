// ---------------------------------------------------------------------------
// fifo_sva.sv  -  Lab V6.  ASSERTIONS: the specification, written as checkable
//                 properties and bound to the DUT without touching its source.
//
// A testbench checks the design at the points where you remembered to look.
// An assertion checks it on EVERY clock edge of EVERY test, for ever, and it
// fires at the exact cycle and the exact line where the rule was broken -
// rather than three hundred cycles later, at the output, where you noticed.
//
// These are concurrent assertions written in the portable SystemVerilog
// subset (checked against Verilator 5.020). Run them with:
//
//   ./scripts/assert.sh
//
// Note on tool support: the open-source linter used here supports simple
// concurrent properties but NOT the ranged delay form (a |-> ##[1:3] b).
// ModelSim/Questa and Vivado's
// xsim support the full language. Everything here is written inside the
// portable subset on purpose, and each property says in words what it checks.
// ---------------------------------------------------------------------------
`default_nettype none

module fifo_sva #(
    parameter integer DEPTH = 8
)(
    input wire                   clk,
    input wire                   rst_n,
    input wire                   wr_en,
    input wire                   rd_en,
    input wire                   full,
    input wire                   empty,
    input wire [$clog2(DEPTH):0] count
);

    // Size the constant to the width of count. Comparing a 4-bit signal with a
    // bare integer makes the whole expression 32 bits wide, which the linter
    // flags - correctly, because that is exactly the width habit that hides
    // real truncation bugs elsewhere.
    localparam [$clog2(DEPTH):0] DEPTH_C = DEPTH[$clog2(DEPTH):0];

    // ---- 1. count and the flags must always agree -------------------------
    a_empty_iff_zero: assert property (@(posedge clk) disable iff (!rst_n)
        empty == (count == 0))
        else $error("empty=%0b but count=%0d", empty, count);

    a_full_iff_depth: assert property (@(posedge clk) disable iff (!rst_n)
        full == (count == DEPTH_C))
        else $error("full=%0b but count=%0d", full, count);

    // ---- 2. occupancy can never leave its legal range ----------------------
    a_count_range: assert property (@(posedge clk) disable iff (!rst_n)
        count <= DEPTH_C)
        else $error("count=%0d exceeds DEPTH=%0d", count, DEPTH_C);

    // ---- 3. the flags are mutually exclusive for DEPTH > 0 -----------------
    a_not_both: assert property (@(posedge clk) disable iff (!rst_n)
        !(full && empty))
        else $error("full and empty at the same time");

    // ---- 4. occupancy may only move by one per cycle, in the right direction
    // A write with no read adds exactly one; a read with no write removes
    // exactly one; both or neither leave it unchanged. |=> means "on the NEXT
    // clock edge", which is where a registered value shows the change.
    a_step_up: assert property (@(posedge clk) disable iff (!rst_n)
        (wr_en && !full && !(rd_en && !empty)) |=> (count == $past(count) + 1))
        else $error("a write did not increase count by exactly one");

    a_step_dn: assert property (@(posedge clk) disable iff (!rst_n)
        (rd_en && !empty && !(wr_en && !full)) |=> (count == $past(count) - 1))
        else $error("a read did not decrease count by exactly one");

    a_step_hold: assert property (@(posedge clk) disable iff (!rst_n)
        (!(wr_en && !full) && !(rd_en && !empty)) |=> (count == $past(count)))
        else $error("count moved with no accepted transfer");

    a_step_both: assert property (@(posedge clk) disable iff (!rst_n)
        (wr_en && !full && rd_en && !empty) |=> (count == $past(count)))
        else $error("a simultaneous read and write changed the occupancy");

    // ---- 5. nothing may be unknown once reset is released ------------------
    a_no_x: assert property (@(posedge clk) disable iff (!rst_n)
        !$isunknown({full, empty, count}))
        else $error("an output went to x");

    // ---- COVER: these are not checks. They record that the interesting
    // situations actually HAPPENED, so a run that passes without ever filling
    // the FIFO cannot be mistaken for a run that proved anything.
    c_full:       cover property (@(posedge clk) disable iff (!rst_n) full);
    c_empty:      cover property (@(posedge clk) disable iff (!rst_n) empty);
    c_wr_at_full: cover property (@(posedge clk) disable iff (!rst_n) wr_en && full);
    c_rd_at_empt: cover property (@(posedge clk) disable iff (!rst_n) rd_en && empty);
    c_both_empty: cover property (@(posedge clk) disable iff (!rst_n) wr_en && rd_en && empty);
    c_both_full:  cover property (@(posedge clk) disable iff (!rst_n) wr_en && rd_en && full);

endmodule

`default_nettype wire
