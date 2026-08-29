// A minimal trace of the Verilog Moore detector, in exactly the format the
// VHDL testbench prints, so scripts/two_languages.sh can diff the two runs.
`timescale 1ns/1ps
module tb_seq101_trace;
    localparam N = 17;
    reg clk = 0, rst_n = 0, din = 0;
    always #5 clk = ~clk;

    wire det;
    seq101_moore dut (.clk(clk), .rst_n(rst_n), .din(din), .det(det));

    reg stream [0:N-1];
    integer i;
    initial begin
        stream[ 0]=1; stream[ 1]=1; stream[ 2]=0; stream[ 3]=1; stream[ 4]=1;
        stream[ 5]=0; stream[ 6]=1; stream[ 7]=0; stream[ 8]=1; stream[ 9]=0;
        stream[10]=1; stream[11]=0; stream[12]=0; stream[13]=1; stream[14]=1;
        stream[15]=0; stream[16]=1;
    end

    initial begin
        rst_n = 0;
        @(negedge clk);
        rst_n = 1;
        for (i = 0; i < N; i = i + 1) begin
            din = stream[i];
            #1;
            $display("cycle %0d din=%b det=%b", i, din, det);
            @(negedge clk);
        end
        $display("Verilog detector run complete");
        $finish;
    end
endmodule
