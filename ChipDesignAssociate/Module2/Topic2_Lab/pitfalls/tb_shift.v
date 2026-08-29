// ---------------------------------------------------------------------------
//  tb_shift.v  -  the blocking / non-blocking difference, measured.
//
//  Both modules get the identical stimulus. The golden model is the DEFINITION
//  of a shift register: q[2] this cycle is din from three cycles ago.
// ---------------------------------------------------------------------------
`timescale 1ns/1ps

module tb_shift;
    reg clk = 0, din = 0;
    always #5 clk = ~clk;

    wire [2:0] q_nb, q_bl;
    shift_nb u_nb (.clk(clk), .din(din), .q(q_nb));
    shift_bl u_bl (.clk(clk), .din(din), .q(q_bl));

    reg [15:0] hist = 16'd0;      // hist[k] = din k cycles ago
    integer    i, nb_err = 0, bl_err = 0;

    // the stimulus: a single 1 walking through, then a pair
    reg stim [0:11];
    initial begin
        stim[0]=1; stim[1]=0; stim[2]=0; stim[3]=0;
        stim[4]=1; stim[5]=1; stim[6]=0; stim[7]=0;
        stim[8]=1; stim[9]=0; stim[10]=1; stim[11]=0;
    end

    initial begin
        $display("");
        $display("  === blocking vs non-blocking in a 3-stage shift register ===");
        $display("");
        $display("  cycle  din   q_nb  q_bl   expected q[2]");
        $display("  -----  ---   ----  ----   -------------");

        @(negedge clk);
        for (i = 0; i < 12; i = i + 1) begin
            din = stim[i];
            @(posedge clk);
            hist = {hist[14:0], din};      // record what was driven
            #1;
            begin : chk
                reg exp2;
                exp2 = (i >= 2) ? stim[i-2] : 1'bx;   // three FFs of delay
                // the first two cycles are pipeline fill - nothing to check
                if (i >= 2) begin
                    if (q_nb[2] !== exp2) nb_err = nb_err + 1;
                    if (q_bl[2] !== exp2) bl_err = bl_err + 1;
                end
                $display("  %5d    %b   %b   %b         %b", i, din,
                         q_nb, q_bl, exp2);
            end
            @(negedge clk);
        end

        $display("");
        $display("  non-blocking version : %0d wrong cycles", nb_err);
        $display("  blocking version     : %0d wrong cycles", bl_err);
        $display("");
        $display("  The blocking version passes din to q[2] in ONE cycle;");
        $display("  it is a wire with a flip-flop, not a 3-stage delay line.");
        $display("");
        $finish;
    end
endmodule
