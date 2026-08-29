// ---------------------------------------------------------------------------
//  tb_seq101.v  -  drives ONE bit stream into BOTH '101' detectors and checks
//                  each against an independently computed golden answer.
//
//  The golden answer is not "what the FSM did".  It is computed straight from
//  the stream array with a windowed comparison, so a bug in either FSM shows
//  up as a mismatch rather than as two machines agreeing on the wrong thing.
//
//  What the run demonstrates:
//    * both machines find exactly the same matches, overlaps included
//    * the Mealy output rises in the SAME cycle as the third bit
//    * the Moore output rises ONE CYCLE LATER - always, without exception
// ---------------------------------------------------------------------------
`timescale 1ns/1ps

module tb_seq101;

    localparam N = 17;

    reg clk = 1'b0, rst_n = 1'b0, din = 1'b0;
    always #5 clk = ~clk;                       // 10 ns period

    wire det_moore, det_mealy, det_hot;

    seq101_moore        u_moore (.clk(clk), .rst_n(rst_n), .din(din), .det(det_moore));
    seq101_mealy        u_mealy (.clk(clk), .rst_n(rst_n), .din(din), .det(det_mealy));
    seq101_moore_onehot u_hot   (.clk(clk), .rst_n(rst_n), .din(din), .det(det_hot));

    // the stimulus stream, index 0 first
    reg        stream [0:N-1];
    reg        exp_mealy [0:N-1];
    reg        exp_moore [0:N-1];
    integer    i;
    integer    errors  = 0;
    integer    hits    = 0;

    initial begin
        // 1 1 0 1 1 0 1 0 1 0 1 0 0 1 1 0 1
        stream[ 0]=1; stream[ 1]=1; stream[ 2]=0; stream[ 3]=1; stream[ 4]=1;
        stream[ 5]=0; stream[ 6]=1; stream[ 7]=0; stream[ 8]=1; stream[ 9]=0;
        stream[10]=1; stream[11]=0; stream[12]=0; stream[13]=1; stream[14]=1;
        stream[15]=0; stream[16]=1;

        // golden: a Mealy hit at index i means bits i-2,i-1,i are 1,0,1
        for (i = 0; i < N; i = i + 1) begin
            exp_mealy[i] = (i >= 2) && (stream[i-2] === 1'b1)
                                    && (stream[i-1] === 1'b0)
                                    && (stream[i]   === 1'b1);
        end
        // golden: the Moore machine says the same thing one cycle later
        exp_moore[0] = 1'b0;
        for (i = 1; i < N; i = i + 1) exp_moore[i] = exp_mealy[i-1];
    end

    initial begin
        $dumpfile("build/seq101.vcd");
        $dumpvars(0, tb_seq101);

        $display("");
        $display("  === '101' sequence detector : Moore vs Mealy ===");
        $display("");
        $display("  cycle  din   mealy exp   moore exp");
        $display("  -----  ---   ---------   ---------");

        // release reset just before the first sampling edge
        rst_n = 1'b0;
        @(negedge clk);
        rst_n = 1'b1;

        for (i = 0; i < N; i = i + 1) begin
            din = stream[i];
            #1;                                  // let the combinational settle
            // sample both outputs in the middle of the cycle, before the edge
            if (det_mealy !== exp_mealy[i]) errors = errors + 1;
            if (det_moore !== exp_moore[i]) errors = errors + 1;
            // the one-hot encoding must be indistinguishable from the outside
            if (det_hot   !== det_moore)    errors = errors + 1;
            if (exp_mealy[i]) hits = hits + 1;

            $display("  %4d    %b     %b   %b     %b   %b   %s",
                     i, din, det_mealy, exp_mealy[i],
                        det_moore, exp_moore[i],
                     exp_mealy[i] ? "<- match" : "");
            @(negedge clk);
        end

        $display("");
        $display("  matches in the stream : %0d", hits);
        $display("  mismatches vs golden  : %0d", errors);
        if (errors == 0) begin
            $display("  PASS - same language, Moore trails Mealy by one cycle,");
            $display("         and the one-hot encoding is indistinguishable");
        end else
            $display("  FAIL - see the rows above");
        $display("");
        $finish;
    end

endmodule
