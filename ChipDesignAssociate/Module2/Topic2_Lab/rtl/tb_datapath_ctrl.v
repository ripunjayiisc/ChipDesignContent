// ---------------------------------------------------------------------------
//  tb_datapath_ctrl.v  -  accumulate N samples, and check the sum against a
//  golden total computed in the testbench.  Also prints the control bundle
//  every cycle so the split between controller and datapath is visible.
// ---------------------------------------------------------------------------
`timescale 1ns/1ps

module tb_datapath_ctrl;
    localparam DW = 8, SW = 16, CW = 8;
    localparam N  = 6;

    reg clk = 0, rst_n = 0, start = 0;
    reg [CW-1:0] n    = 0;
    reg [DW-1:0] data = 0;
    wire [SW-1:0] sum;
    wire          done;

    always #5 clk = ~clk;

    accum_top #(.DW(DW), .SW(SW), .CW(CW)) dut (
        .clk(clk), .rst_n(rst_n), .start(start),
        .n(n), .data(data), .sum(sum), .done(done));

    reg [DW-1:0] samples [0:N-1];
    integer i, golden = 0, errors = 0, cycle = 0;

    initial begin
        samples[0]=8'd10; samples[1]=8'd20; samples[2]=8'd30;
        samples[3]=8'd40; samples[4]=8'd50; samples[5]=8'd7;
        for (i = 0; i < N; i = i + 1) golden = golden + samples[i];
    end

    initial begin
        $dumpfile("build/accum.vcd");
        $dumpvars(0, tb_datapath_ctrl);

        $display("");
        $display("  === datapath + controller : accumulate %0d samples ===", N);
        $display("");
        $display("  cycle  data  | clr en ld dec done |  sum");
        $display("  -----  ----  | --- -- -- --- ---- |  ----");

        rst_n = 0;
        @(negedge clk);
        rst_n = 1;

        // cycle 0 : request
        n = N; start = 1; data = 0;
        show; @(negedge clk);
        start = 0;

        // cycles 1..N : one sample per clock
        for (i = 0; i < N; i = i + 1) begin
            data = samples[i];
            show; @(negedge clk);
        end

        // let it finish
        data = 8'd0;
        for (i = 0; i < 3; i = i + 1) begin
            show;
            if (done && sum !== golden[SW-1:0]) errors = errors + 1;
            @(negedge clk);
        end

        $display("");
        $display("  golden total : %0d", golden);
        $display("  hardware sum : %0d", sum);
        if (sum === golden[SW-1:0] && errors == 0)
            $display("  PASS - controller sequenced the datapath correctly");
        else
            $display("  FAIL");
        $display("");
        $finish;
    end

    task show;
        begin
            #1;
            $display("  %5d   %3d  |  %b  %b  %b  %b   %b   | %5d",
                     cycle, data,
                     dut.acc_clr, dut.acc_en, dut.cnt_ld, dut.cnt_dec, done,
                     sum);
            cycle = cycle + 1;
        end
    endtask
endmodule
