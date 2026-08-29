`timescale 1ns / 1ps

module tb_glitch_capture;

    reg a, b, c, clk;
    wire d_sampled;
    wire [7:0] c_edges;
    wire r_flag;

    glitch_capture dut (.a(a), .b(b), .c(c), .clk(clk),
                        .d_sampled(d_sampled), .c_edges(c_edges),
                        .r_flag(r_flag));

    initial begin clk = 0; forever #50 clk = ~clk; end

    integer baseline;         // edges seen while the circuit powered up

    initial begin
        $dumpfile("build/glitch_capture.vcd");
        $dumpvars(0, tb_glitch_capture);

        // hold A=1, C=1 and toggle B. Every falling B produces the glitch.
        a = 1; c = 1; b = 1;
        #120;

        // At t=0 f settles from x to 1, and that counts as one legitimate
        // posedge. Record it so the report can quote spurious edges only.
        baseline = c_edges;

        // four B pulses, each placed at 20 ns after a clock edge so the
        // glitch has 80 ns - far more than it needs - to settle before the
        // next sampling edge. This is the friendliest possible case.
        repeat (4) begin
            @(posedge clk); #20 b = 0;      // f glitches here
            @(posedge clk); #20 b = 1;
        end
        #200;

        $display("");
        $display("  === one glitchy signal, three consumers ===");
        $display("");
        $display("  f was driven through 4 falling-B transitions.");
        $display("  Each produced one static-1 glitch, 80 ns before any clock edge.");
        $display("");
        $display("  1. f as DATA, sampled by the clean clock");
        $display("       final d_sampled = %b        <- correct, glitch never seen",
                 d_sampled);
        $display("  2. f as a CLOCK");
        $display("       edges at power-up      = %0d   (legitimate: f settled x -> 1)",
                 baseline);
        $display("       edges after that       = %0d   <- should be 0. Each glitch",
                 c_edges - baseline);
        $display("                                     was a spurious clock edge.");
        $display("  3. f as an ASYNCHRONOUS RESET");
        $display("       r_flag = %b                  <- should be 1; a glitch reset it",
                 r_flag);
        $display("");
        if ((c_edges - baseline) == 0 && r_flag == 1'b1)
            $display("  RESULT: no consumer was harmed (unexpected - check the delays)");
        else
            $display("  RESULT: the SAME signal is harmless as data and fatal as a");
            $display("          clock or an asynchronous reset.");
        $display("");
        $finish;
    end

endmodule
