// ---------------------------------------------------------------------------
// tb_sequential.v  -  drives the D flip-flop, the shift register and the
//                     BCD counter together so one waveform shows all three.
//
//   iverilog -g2012 -o seq.out rtl/dff.v rtl/shift4.v rtl/bcd_counter.v \
//            tb/tb_sequential.v
//   vvp seq.out
//   gtkwave seq.vcd &
//
// WHAT TO LOOK FOR IN THE WAVEFORM
//   1. q follows d only at RISING clk edges - note the deliberate mid-phase
//      change of d, which the flip-flop completely ignores.
//   2. sr_q[3] lags sin by exactly FOUR clock cycles.
//   3. cnt runs 0..9 then wraps to 0 - it never reaches 10 - and it freezes
//      while en is low.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_sequential;

    reg        clk   = 1'b0;
    reg        rst_n = 1'b0;
    reg        d     = 1'b0;
    reg        sin   = 1'b0;
    reg        en    = 1'b1;
    wire       q;
    wire [3:0] sr_q;
    wire [3:0] cnt;

    integer errors = 0;
    integer i;
    reg [3:0] held;

    always #5 clk = ~clk;                        // 100 MHz

    dff         u_dff (.clk(clk), .rst_n(rst_n), .d(d),    .q(q));
    shift4      u_sr  (.clk(clk), .rst_n(rst_n), .sin(sin), .q(sr_q));
    bcd_counter u_cnt (.clk(clk), .rst_n(rst_n), .en(en),   .cnt(cnt));

    // ---- 1. edge sensitivity: move d in the MIDDLE of a high phase -------
    initial begin
        #12  d = 1'b1;                           // just after the edge at 15? no: before
        #10  d = 1'b0;
        #3   d = 1'b1;                           // deliberate mid-phase change
        #20  d = 1'b0;
    end

    initial begin
        $dumpfile("seq.vcd");
        $dumpvars(0, tb_sequential);

        #12 rst_n = 1'b1;                        // release reset between edges

        // ---- 2. shift register: push a single 1 in, expect it at q[3]
        //         exactly four clock cycles later -----------------------
        @(posedge clk);
        #2 sin = 1'b1;
        @(posedge clk);                          // cycle 1: q[0] = 1
        #2 sin = 1'b0;
        #1;
        if (sr_q !== 4'b0001) begin
            $display("FAIL shift4 after 1 cycle: expected 0001, got %b", sr_q);
            errors = errors + 1;
        end
        repeat (3) @(posedge clk);
        #1;
        if (sr_q !== 4'b1000) begin
            $display("FAIL shift4 after 4 cycles: expected 1000, got %b", sr_q);
            errors = errors + 1;
        end
        @(posedge clk);
        #1;
        if (sr_q !== 4'b0000) begin
            $display("FAIL shift4 after 5 cycles: expected 0000, got %b", sr_q);
            errors = errors + 1;
        end

        // ---- 3. BCD counter: must never exceed 9 -----------------------
        for (i = 0; i < 25; i = i + 1) begin
            @(posedge clk);
            #1;
            if (cnt > 4'd9) begin
                $display("FAIL bcd_counter reached %0d", cnt);
                errors = errors + 1;
            end
        end

        // ---- 4. enable: the count must freeze --------------------------
        #2 en = 1'b0;
        @(posedge clk); #1 held = cnt;
        repeat (3) @(posedge clk);
        #1;
        if (cnt !== held) begin
            $display("FAIL bcd_counter moved from %0d to %0d while en was low", held, cnt);
            errors = errors + 1;
        end
        #2 en = 1'b1;
        @(posedge clk); #1;
        if (cnt !== ((held == 4'd9) ? 4'd0 : held + 4'd1)) begin
            $display("FAIL bcd_counter did not resume correctly (%0d -> %0d)", held, cnt);
            errors = errors + 1;
        end

        repeat (12) @(posedge clk);

        if (errors == 0)
            $display("PASS - dff, shift4 and bcd_counter all behaved correctly");
        else
            $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
