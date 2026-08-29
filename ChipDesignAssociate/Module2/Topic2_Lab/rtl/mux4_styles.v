// ---------------------------------------------------------------------------
//  mux4_styles.v  -  ONE function, THREE coding styles.
//
//  A 4-to-1 multiplexer written as a conditional expression, as a case
//  statement and as an if/else chain.  scripts/mux.sh proves by SAT that all
//  three are the same Boolean function, and then synthesises all three.
//
//  The usual classroom claim is "the optimiser flattens the difference, so
//  write whichever reads best".  Run the script before you believe it.  On
//  Yosys 0.33 the three styles come out at 3, 10 and 6 cells - same function,
//  same inputs, three different netlists.  The reason is visible in the
//  source: the conditional expression uses sel[1] and sel[0] directly as mux
//  selects, while the case and if/else versions ask the tool to build
//  equality comparators against 2'b00, 2'b01, ... and then re-derive that
//  those comparisons ARE the select bits.  A stronger optimiser may close the
//  gap; this one does not close it completely.
//
//  Two lessons, and the second is the important one:
//    1. EQUIVALENT is not the same as IDENTICAL.  Formal equivalence tells
//       you the function matches; it says nothing about area or timing.
//    2. Measure your own tool.  Folklore about what optimisers do is the
//       least reliable kind of knowledge in this field.
// ---------------------------------------------------------------------------

// style 1 - nested conditional operator.  Cannot infer a latch: an expression
// is total by construction.
module mux4_assign (
    input  [3:0] d,
    input  [1:0] sel,
    output       y
);
    assign y = sel[1] ? (sel[0] ? d[3] : d[2])
                      : (sel[0] ? d[1] : d[0]);
endmodule

// style 2 - case statement.  The `default` is what keeps it combinational.
module mux4_case (
    input  [3:0] d,
    input  [1:0] sel,
    output reg   y
);
    always @(*) begin
        case (sel)
            2'b00  : y = d[0];
            2'b01  : y = d[1];
            2'b10  : y = d[2];
            2'b11  : y = d[3];
            default: y = 1'b0;
        endcase
    end
endmodule

// style 3 - if/else chain.  The trailing `else` plays the role of `default`.
module mux4_if (
    input  [3:0] d,
    input  [1:0] sel,
    output reg   y
);
    always @(*) begin
        if      (sel == 2'b00) y = d[0];
        else if (sel == 2'b01) y = d[1];
        else if (sel == 2'b10) y = d[2];
        else                   y = d[3];
    end
endmodule
