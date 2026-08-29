// ---------------------------------------------------------------------------
//  tb_reuse.v  -  proves the three reuse features actually do what the
//  comments claim: the generate loop really builds N stages of delay, and the
//  two counter instances really form a 2^WFAST prescaler.
// ---------------------------------------------------------------------------
`timescale 1ns/1ps

module tb_reuse;
    localparam W = 8, N = 4;
    localparam WFAST = 4, WSLOW = 8;

    reg clk = 0, rst = 1, rst_n = 0, en = 1;
    always #5 clk = ~clk;

    reg  [W-1:0] din = 0;
    wire [W-1:0] dout;
    delayline #(.W(W), .N(N)) u_dl (
        .clk(clk), .rst(rst), .en(en), .din(din), .dout(dout));

    wire [WFAST-1:0] fast;
    wire [WSLOW-1:0] slow;
    wire             slow_tc;
    counter_pair #(.WFAST(WFAST), .WSLOW(WSLOW)) u_cp (
        .clk(clk), .rst_n(rst_n), .en(en),
        .fast(fast), .slow(slow), .slow_tc(slow_tc));

    integer i, dl_err = 0, cp_err = 0;
    reg [W-1:0] hist [0:63];

    initial begin
        $dumpfile("build/reuse.vcd");
        $dumpvars(0, tb_reuse);

        $display("");
        $display("  === hierarchy, parameters and generate ===");
        $display("");
        $display("  delayline #(W=%0d, N=%0d) - expect a %0d-cycle delay",
                 W, N, N);
        $display("");
        $display("  cycle  din   dout   expected");
        $display("  -----  ---   ----   --------");

        @(negedge clk);
        rst = 0; rst_n = 1;

        for (i = 0; i < 12; i = i + 1) begin
            din = i[W-1:0] + 8'd100;
            hist[i] = din;
            #1;
            begin : dlchk
                reg [W-1:0] exp;
                exp = (i >= N) ? hist[i-N] : {W{1'bx}};
                if (i >= N && dout !== exp) dl_err = dl_err + 1;
                $display("  %5d  %3d   %4d   %8s%0d", i, din, dout,
                         (i >= N) ? "" : "(fill) ", (i >= N) ? exp : 0);
            end
            @(negedge clk);
        end

        $display("");
        $display("  delayline mismatches : %0d", dl_err);
        $display("");
        $display("  counter_pair #(WFAST=%0d, WSLOW=%0d)"
                 , WFAST, WSLOW);
        $display("");
        $display("  cycle  fast  slow");
        $display("  -----  ----  ----");

        begin : cpchk
            integer c, last_slow, gap, prev_edge;
            last_slow = slow;
            prev_edge = -1;
            for (c = 0; c < 40; c = c + 1) begin
                #1;
                if (c % 4 == 0 || slow !== last_slow)
                    $display("  %5d  %4d  %4d", c, fast, slow);
                if (slow !== last_slow) begin
                    if (prev_edge >= 0) begin
                        gap = c - prev_edge;
                        if (gap != (1 << WFAST)) begin
                            $display("  *** prescaler ratio %0d, expected %0d",
                                     gap, (1 << WFAST));
                            cp_err = cp_err + 1;
                        end
                    end
                    prev_edge = c;
                    last_slow = slow;
                end
                @(negedge clk);
            end
        end

        $display("");
        $display("  prescaler ratio errors : %0d", cp_err);
        $display("");
        if (dl_err == 0 && cp_err == 0)
            $display("  PASS - generate built %0d real stages, and the two"
                     , N);
        else
            $display("  FAIL - see above");
        if (dl_err == 0 && cp_err == 0)
            $display("         counter instances divide by %0d", 1 << WFAST);
        $display("");
        $finish;
    end
endmodule
