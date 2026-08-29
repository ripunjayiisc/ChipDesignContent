// ---------------------------------------------------------------------------
//  datapath_ctrl.v  -  the DATAPATH + CONTROLLER structure, written out.
//
//  Almost every digital block, from a UART to a GPU, decomposes the same way:
//
//     DATAPATH    the things that hold and transform data - registers,
//                 adders, muxes, counters.  Wide.  No decisions.
//     CONTROLLER  a finite state machine that decides WHEN each datapath
//                 element loads, clears or holds.  Narrow.  All decisions.
//
//  They talk over two thin bundles of wires:
//     controller -> datapath : CONTROL signals  (acc_clr, acc_en, cnt_ld, ...)
//     datapath -> controller : STATUS signals   (cnt_done)
//
//  Keeping them in separate modules is not decoration.  It means the datapath
//  can be re-timed, widened or pipelined without touching the state machine,
//  and the state machine can be re-specified without touching an adder.
//
//  The worked function: accumulate N samples.  Assert `start` with `n` on the
//  count port; feed one sample per clock on `data`; `done` pulses when the sum
//  of those N samples is valid on `sum`.
// ---------------------------------------------------------------------------

// ======================= the datapath =====================================
module accum_datapath #(
    parameter DW = 8,          // sample width
    parameter SW = 16,         // accumulator width (wide enough not to wrap)
    parameter CW = 8           // sample-count width
)(
    input                 clk,
    input                 rst_n,
    // data in
    input      [DW-1:0]   data,
    input      [CW-1:0]   n,
    // control in  (from the controller)
    input                 acc_clr,
    input                 acc_en,
    input                 cnt_ld,
    input                 cnt_dec,
    // status out  (to the controller)
    output                cnt_done,
    // data out
    output reg [SW-1:0]   sum
);
    reg [CW-1:0] cnt;

    // the accumulator
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)      sum <= {SW{1'b0}};
        else if (acc_clr) sum <= {SW{1'b0}};
        else if (acc_en)  sum <= sum + {{(SW-DW){1'b0}}, data};
    end

    // the sample counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)       cnt <= {CW{1'b0}};
        else if (cnt_ld)  cnt <= n;
        else if (cnt_dec) cnt <= cnt - {{(CW-1){1'b0}}, 1'b1};
    end

    assign cnt_done = (cnt == {CW{1'b0}});
endmodule


// ======================= the controller ===================================
module accum_ctrl (
    input      clk,
    input      rst_n,
    input      start,
    input      cnt_done,       // status from the datapath
    output reg acc_clr,        // control to the datapath
    output reg acc_en,
    output reg cnt_ld,
    output reg cnt_dec,
    output reg done
);
    localparam [1:0] S_IDLE = 2'd0,
                     S_RUN  = 2'd1,
                     S_DONE = 2'd2;

    reg [1:0] state, next_state;

    // block 1 : state register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S_IDLE;
        else        state <= next_state;
    end

    // block 2 : next-state logic
    always @(*) begin
        next_state = state;
        case (state)
            S_IDLE : if (start)    next_state = S_RUN;
            S_RUN  : if (cnt_done) next_state = S_DONE;
            S_DONE :               next_state = S_IDLE;
            default:               next_state = S_IDLE;
        endcase
    end

    // block 3 : output logic.
    // acc_clr / cnt_ld are Mealy (they depend on `start`), because the load
    // must happen in the SAME cycle the request arrives.  The rest are Moore.
    always @(*) begin
        acc_clr = 1'b0;
        acc_en  = 1'b0;
        cnt_ld  = 1'b0;
        cnt_dec = 1'b0;
        done    = 1'b0;
        case (state)
            S_IDLE : if (start) begin acc_clr = 1'b1; cnt_ld = 1'b1; end
            S_RUN  : if (!cnt_done) begin acc_en = 1'b1; cnt_dec = 1'b1; end
            S_DONE :                done   = 1'b1;
            default: ;
        endcase
    end
endmodule


// ======================= the two wired together ===========================
module accum_top #(
    parameter DW = 8,
    parameter SW = 16,
    parameter CW = 8
)(
    input                clk,
    input                rst_n,
    input                start,
    input      [CW-1:0]  n,
    input      [DW-1:0]  data,
    output     [SW-1:0]  sum,
    output               done
);
    wire acc_clr, acc_en, cnt_ld, cnt_dec, cnt_done;

    accum_ctrl u_ctrl (
        .clk(clk), .rst_n(rst_n), .start(start), .cnt_done(cnt_done),
        .acc_clr(acc_clr), .acc_en(acc_en),
        .cnt_ld(cnt_ld), .cnt_dec(cnt_dec), .done(done));

    accum_datapath #(.DW(DW), .SW(SW), .CW(CW)) u_dp (
        .clk(clk), .rst_n(rst_n), .data(data), .n(n),
        .acc_clr(acc_clr), .acc_en(acc_en),
        .cnt_ld(cnt_ld), .cnt_dec(cnt_dec),
        .cnt_done(cnt_done), .sum(sum));
endmodule
