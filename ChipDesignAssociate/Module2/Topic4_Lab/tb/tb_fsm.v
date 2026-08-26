// ---------------------------------------------------------------------------
// tb_fsm.v  -  self-checking testbench for traffic_fsm, vending_fsm and
//              seq_detect_1011.  (Lab L3)
//
// Technique on show: checking a state machine by its OBSERVABLE OUTPUTS, not
// by peeking at its internal state. A testbench that reads dut.state passes
// even when the encoding changes underneath it - and fails for the wrong
// reason when someone re-encodes the FSM.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_fsm;

    reg clk = 1'b0, rst_n = 1'b0;
    integer errors = 0;
    integer i;

    always #5 clk = ~clk;

    task check1(input cond, input [255:0] msg);
        begin
            if (!cond) begin
                $display("  FAIL: %0s   (t=%0t)", msg, $time);
                errors = errors + 1;
            end
        end
    endtask

    localparam [2:0] RED = 3'b100, YELLOW = 3'b010, GREEN = 3'b001;

    // ------------------------------------------------ traffic lights
    reg tf_tick;  wire [2:0] tf_main, tf_side;
    traffic_fsm #(.T_GREEN(4), .T_YELLOW(2)) u_tf (
        .clk(clk), .rst_n(rst_n), .tick(tf_tick),
        .main_light(tf_main), .side_light(tf_side));

    // ------------------------------------------------ vending machine
    reg vm_valid, vm_cancel;  reg [1:0] vm_coin;
    wire vm_disp, vm_ret;  wire [5:0] vm_chg, vm_credit;
    vending_fsm u_vm (
        .clk(clk), .rst_n(rst_n), .coin_valid(vm_valid), .coin(vm_coin),
        .cancel(vm_cancel), .dispense(vm_disp), .return_coins(vm_ret),
        .chg_amt(vm_chg), .credit(vm_credit));

    // ------------------------------------------------ 1011 detector
    reg sd_x;  wire sd_z;
    seq_detect_1011 u_sd (.clk(clk), .rst_n(rst_n), .x(sd_x), .z(sd_z));
    integer sd_hits = 0;
    always @(posedge clk) if (rst_n) #1 if (sd_z) sd_hits = sd_hits + 1;

    // a coin is presented for exactly one clock
    task give_coin(input [1:0] c);
        begin
            @(posedge clk); #1 vm_coin = c; vm_valid = 1'b1;
            @(posedge clk); #1 vm_valid = 1'b0;
        end
    endtask

    initial begin
        $dumpfile("fsm.vcd");
        $dumpvars(0, tb_fsm);
        $display("=== L3 state machines ===");

        tf_tick = 1'b0;
        vm_valid = 1'b0; vm_coin = 2'b00; vm_cancel = 1'b0;
        sd_x = 1'b0;

        #12 rst_n = 1'b1;
        #1;

        // ---------------- traffic lights ----------------
        check1(tf_main === GREEN && tf_side === RED, "traffic: wrong reset state");
        // exactly one light must be lit on each road, always
        fork
            begin : safety_monitor
                forever begin
                    @(posedge clk); #1;
                    check1($countones(tf_main) == 1, "traffic: main not one-hot");
                    check1($countones(tf_side) == 1, "traffic: side not one-hot");
                    // both roads must never be green at once
                    check1(!(tf_main === GREEN && tf_side === GREEN),
                           "traffic: BOTH roads green - unsafe");
                end
            end
        join_none

        // T_GREEN = 4 ticks, so pulse tick and watch the sequence
        for (i = 0; i < 4; i = i + 1) begin
            @(posedge clk); #1 tf_tick = 1'b1;
            @(posedge clk); #1 tf_tick = 1'b0;
        end
        #1 check1(tf_main === YELLOW, "traffic: did not move to main yellow");
        for (i = 0; i < 2; i = i + 1) begin
            @(posedge clk); #1 tf_tick = 1'b1;
            @(posedge clk); #1 tf_tick = 1'b0;
        end
        #1 check1(tf_side === GREEN, "traffic: did not move to side green");

        // ---------------- vending machine ----------------
        // 20 + 20 = 40 >= 30  ->  dispense with 10 change
        give_coin(2'b10);
        #1 check1(vm_credit === 6'd20, "vending: credit after first 20");
        give_coin(2'b10);
        @(posedge clk); #1;
        check1(vm_disp === 1'b1, "vending: did not dispense at 40");
        check1(vm_chg  === 6'd10, "vending: wrong change for 40");
        @(posedge clk); #1;
        check1(vm_disp === 1'b0, "vending: dispense lasted more than one cycle");
        check1(vm_credit === 6'd0, "vending: credit not cleared");

        // exact money: 10 + 20 = 30, no change
        give_coin(2'b01);
        give_coin(2'b10);
        @(posedge clk); #1;
        check1(vm_disp === 1'b1, "vending: did not dispense at exactly 30");
        check1(vm_chg  === 6'd0,  "vending: change should be 0 for exact money");
        @(posedge clk); #1;

        // cancel refunds whatever is in there.
        // REFUND lasts exactly one cycle, so the check must happen in that
        // cycle - one edge later and the machine is already back in IDLE.
        give_coin(2'b00);                        // 5
        @(posedge clk); #1 vm_cancel = 1'b1;     // assert cancel
        @(posedge clk); #1 vm_cancel = 1'b0;     // THIS edge enters REFUND
        check1(vm_ret === 1'b1, "vending: cancel did not refund");
        check1(vm_chg === 6'd5,  "vending: wrong refund amount");
        @(posedge clk); #1;                      // and back to IDLE
        check1(vm_ret === 1'b0, "vending: refund lasted more than one cycle");
        check1(vm_credit === 6'd0, "vending: credit not cleared after refund");

        // ---------------- 1011 sequence detector ----------------
        // stream 1 0 1 1 0 1 1 0 contains TWO overlapping matches
        begin : stream
            reg [7:0] pattern;
            pattern = 8'b1011_0110;
            sd_hits = 0;
            for (i = 7; i >= 0; i = i - 1) begin
                @(posedge clk); #1 sd_x = pattern[i];
            end
            @(posedge clk); #1 sd_x = 1'b0;
            repeat (3) @(posedge clk);
            #1 check1(sd_hits == 2, "1011 detector: expected exactly 2 hits");
            if (sd_hits != 2) $display("      (got %0d)", sd_hits);
        end

        disable safety_monitor;

        if (errors == 0) $display("PASS - L3 state machines, all checks correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
