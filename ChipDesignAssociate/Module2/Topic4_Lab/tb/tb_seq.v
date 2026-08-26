// ---------------------------------------------------------------------------
// tb_seq.v  -  self-checking testbench for the L2 sequential library:
//              reg_en, shift_reg, counter, edge_detect, synchroniser,
//              debouncer and clk_divider.
//
// Techniques on show:
//   * a clock generator and a clean reset released BETWEEN edges
//   * driving stimulus off the NEGEDGE so it is stable at every posedge
//   * checking with #1 after the edge, once the flip-flops have settled
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_seq;

    reg clk = 1'b0, rst_n = 1'b0;
    integer errors = 0;
    integer i;

    always #5 clk = ~clk;                    // 100 MHz

    task check1(input cond, input [255:0] msg);
        begin
            if (!cond) begin
                $display("  FAIL: %0s   (t=%0t)", msg, $time);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------------ reg_en
    reg        re_en;  reg [7:0] re_d;  wire [7:0] re_q;
    reg_en #(.W(8), .INIT(8'hAA)) u_reg (
        .clk(clk), .rst_n(rst_n), .en(re_en), .d(re_d), .q(re_q));

    // ------------------------------------------------ shift_reg
    reg [1:0] sr_mode;  reg sr_sin;  reg [7:0] sr_din;  wire [7:0] sr_q;
    shift_reg #(.W(8)) u_sr (
        .clk(clk), .rst_n(rst_n), .mode(sr_mode), .sin(sr_sin),
        .din(sr_din), .q(sr_q));

    // ------------------------------------------------ counter (mod-10)
    reg  c_en, c_up, c_load;  reg [3:0] c_din;  wire [3:0] c_q;  wire c_tc;
    counter #(.W(4), .MAX(9)) u_cnt (
        .clk(clk), .rst_n(rst_n), .en(c_en), .up(c_up), .load(c_load),
        .din(c_din), .q(c_q), .tc(c_tc));

    // ------------------------------------------------ edge detector
    reg  ed_sig;  wire ed_rise, ed_fall, ed_any;
    edge_detect u_ed (.clk(clk), .rst_n(rst_n), .sig(ed_sig),
                      .rise(ed_rise), .fall(ed_fall), .any(ed_any));

    // ------------------------------------------------ debouncer (short count)
    reg  db_in;  wire db_out;
    debouncer #(.STABLE_COUNT(4)) u_db (
        .clk(clk), .rst_n(rst_n), .noisy_in(db_in), .clean_out(db_out));

    // ------------------------------------------------ tick generator
    wire tick;
    clk_divider #(.DIV(5)) u_div (.clk(clk), .rst_n(rst_n), .tick(tick));
    integer tick_count = 0;
    always @(posedge clk) if (rst_n && tick) tick_count = tick_count + 1;

    initial begin
        $dumpfile("seq.vcd");
        $dumpvars(0, tb_seq);
        $display("=== L2 sequential library ===");

        re_en = 0; re_d = 8'h00;
        sr_mode = 2'b00; sr_sin = 0; sr_din = 8'h00;
        c_en = 0; c_up = 1; c_load = 0; c_din = 4'd0;
        ed_sig = 0; db_in = 0;

        #12 rst_n = 1'b1;                     // release reset between edges
        #1;
        check1(re_q === 8'hAA, "reg_en did not take its INIT value on reset");
        check1(c_q  === 4'd0,  "counter did not reset to 0");

        // ---------------- reg_en: enable must gate the load ----------------
        @(negedge clk); re_d = 8'h5A; re_en = 1'b0;
        @(posedge clk); #1;
        check1(re_q === 8'hAA, "reg_en loaded while en was low");
        @(negedge clk); re_en = 1'b1;
        @(posedge clk); #1;
        check1(re_q === 8'h5A, "reg_en did not load while en was high");
        @(negedge clk); re_en = 1'b0; re_d = 8'hFF;
        @(posedge clk); #1;
        check1(re_q === 8'h5A, "reg_en changed while en was low");

        // ---------------- shift_reg: all four modes ----------------
        @(negedge clk); sr_mode = 2'b11; sr_din = 8'b1000_0001;   // load
        @(posedge clk); #1;
        check1(sr_q === 8'b1000_0001, "shift_reg parallel load");
        @(negedge clk); sr_mode = 2'b01; sr_sin = 1'b0;           // shift right
        @(posedge clk); #1;
        check1(sr_q === 8'b0100_0000, "shift_reg shift right");
        @(negedge clk); sr_mode = 2'b10; sr_sin = 1'b1;           // shift left
        @(posedge clk); #1;
        check1(sr_q === 8'b1000_0001, "shift_reg shift left");
        @(negedge clk); sr_mode = 2'b00;                          // hold
        @(posedge clk); #1;
        check1(sr_q === 8'b1000_0001, "shift_reg hold");

        // ---------------- counter: mod-10 up, wrap, tc, load, down ---------
        @(negedge clk); c_en = 1'b1; c_up = 1'b1;
        for (i = 0; i < 10; i = i + 1) begin
            @(posedge clk); #1;
            check1(c_q === ((i + 1) % 10), "counter up sequence");
            check1(c_q <= 4'd9, "counter exceeded MAX");
        end
        // tc must assert in the cycle where q == MAX
        @(negedge clk);
        while (c_q !== 4'd9) @(negedge clk);
        check1(c_tc === 1'b1, "counter tc did not assert at MAX");
        @(posedge clk); #1;
        check1(c_q === 4'd0, "counter did not wrap after MAX");

        @(negedge clk); c_load = 1'b1; c_din = 4'd7;
        @(posedge clk); #1; check1(c_q === 4'd7, "counter load");
        @(negedge clk); c_load = 1'b0; c_up = 1'b0;               // count down
        @(posedge clk); #1; check1(c_q === 4'd6, "counter down");

        // ---------------- edge detector ----------------
        // NOTE the stimulus timing. An edge detector produces a FULL-CYCLE
        // pulse only when its input changes just after a clock edge - i.e.
        // when the input is itself synchronous. Drive it mid-cycle and you
        // get a half-cycle sliver instead. That is not a flaw in the design;
        // it is why every asynchronous input must be synchronised first.
        @(posedge clk); #1 ed_sig = 1'b0;
        @(posedge clk); #1 ed_sig = 1'b1;         // change just after the edge
        @(negedge clk);                            // mid-cycle: pulse is up
        check1(ed_rise === 1'b1 && ed_fall === 1'b0, "edge_detect rising");
        @(posedge clk); #1;                        // next edge clears it
        check1(ed_rise === 1'b0, "edge_detect rise lasted more than one cycle");
        ed_sig = 1'b0;                             // falls just after this edge
        @(negedge clk);
        check1(ed_fall === 1'b1 && ed_rise === 1'b0, "edge_detect falling");
        check1(ed_any  === 1'b1, "edge_detect any");
        @(posedge clk); #1;
        check1(ed_fall === 1'b0, "edge_detect fall lasted more than one cycle");

        // ---------------- debouncer: a bouncing input ----------------
        @(negedge clk); db_in = 1'b1;         // bounce
        @(negedge clk); db_in = 1'b0;
        @(negedge clk); db_in = 1'b1;
        @(negedge clk); db_in = 1'b0;
        repeat (6) @(posedge clk); #1;
        check1(db_out === 1'b0, "debouncer accepted a bounce");
        @(negedge clk); db_in = 1'b1;         // now hold it steady
        repeat (12) @(posedge clk); #1;
        check1(db_out === 1'b1, "debouncer did not accept a stable input");

        // ---------------- clk_divider: exactly one tick per DIV cycles -----
        begin : tick_check
            integer t0, cycles;
            t0 = tick_count;
            cycles = 50;
            repeat (cycles) @(posedge clk);
            #1;
            // DIV = 5, so 50 clocks should give 10 ticks (+/- 1 for phase)
            check1((tick_count - t0) >= 9 && (tick_count - t0) <= 11,
                   "clk_divider tick rate wrong");
        end

        if (errors == 0) $display("PASS - L2 sequential library, all checks correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
