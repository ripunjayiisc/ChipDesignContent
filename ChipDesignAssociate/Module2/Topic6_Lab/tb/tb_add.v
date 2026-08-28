// ---------------------------------------------------------------------------
// tb_add.v  -  prove the optimised adders still ADD.
//
// Every optimisation in this lab changes the netlist. An optimisation you did
// not verify is a bug you have not found yet, so each variant is checked
// against a behavioural reference with random operands.
//
// Note the LATENCY difference: add_ripple and add_fast answer in 2 cycles,
// add_ripple_pipe answers in 3, because pipelining bought speed with latency.
// The testbench has to know that. Forgetting it is the classic way to
// "prove" a correct pipeline is broken.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_add;
    localparam integer W = 32;
    localparam integer CLK = 10;

    reg clk = 1'b0, rst_n;
    reg  [W-1:0] a, b;
    wire [W-1:0] s_rip, s_pipe, s_fast;
    wire         c_rip, c_pipe, c_fast;

    always #(CLK/2) clk = ~clk;

    add_ripple      #(.W(W)) u_rip  (.clk(clk), .rst_n(rst_n), .a(a), .b(b),
                                     .sum(s_rip),  .cout(c_rip));
    add_ripple_pipe #(.W(W)) u_pipe (.clk(clk), .rst_n(rst_n), .a(a), .b(b),
                                     .sum(s_pipe), .cout(c_pipe));
    add_fast        #(.W(W)) u_fast (.clk(clk), .rst_n(rst_n), .a(a), .b(b),
                                     .sum(s_fast), .cout(c_fast));

    // reference: the answer, and the same answer delayed by the pipeline depth
    reg [W:0] ref0, ref1, ref2, ref3;
    always @(posedge clk) begin
        ref0 <= {1'b0, a} + {1'b0, b};
        ref1 <= ref0;
        ref2 <= ref1;
        ref3 <= ref2;
    end

    integer i, errors = 0;
    reg [31:0] seed = 32'd12345;

    task chk(input [W:0] got, input [W:0] exp, input [127:0] who);
        begin
            if (got !== exp) begin
                if (errors < 5)
                    $display("  FAIL %0t %0s : got %h expected %h", $time, who, got, exp);
                errors = errors + 1;
            end
        end
    endtask

    initial begin
        rst_n = 1'b0; a = 0; b = 0;
        repeat (4) @(posedge clk);
        #1 rst_n = 1'b1;
        repeat (6) @(posedge clk);

        for (i = 0; i < 500; i = i + 1) begin
            @(posedge clk); #1;
            a = $random(seed);
            b = $random(seed);
            @(posedge clk); #1;
            // ref1 is the answer for the operands applied two edges ago,
            // which is exactly what a 2-cycle design is presenting now
            chk({c_rip,  s_rip},  ref1, "add_ripple");
            chk({c_fast, s_fast}, ref1, "add_fast");
            chk({c_pipe, s_pipe}, ref2, "add_ripple_pipe (3 cycles)");
        end

        if (errors == 0)
            $display("PASS - all three adders agree with the reference over 500 vectors");
        else
            $display("FAIL - %0d mismatches", errors);
        $finish;
    end

    initial begin
        #(CLK * 20000);
        $display("FAIL - timeout");
        $finish;
    end
endmodule
