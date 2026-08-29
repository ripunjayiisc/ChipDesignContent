// ---------------------------------------------------------------------------
//  tb_traffic.v  -  exercises the Moore traffic-light controller and CHECKS
//                   two safety properties on every single clock cycle:
//
//    P1  the two roads are never green at the same time
//    P2  a road never jumps straight from green to red - yellow comes first
//
//  Property checking like this is the cheap half of formal verification: you
//  write the rule once, and the simulator tests it on every cycle of every
//  run, instead of you eyeballing a waveform.
// ---------------------------------------------------------------------------
`timescale 1ns/1ps

module tb_traffic;

    localparam GREEN_TICKS  = 6;
    localparam YELLOW_TICKS = 2;
    localparam [1:0] RED = 2'b00, YELLOW = 2'b01, GREEN = 2'b10;

    reg  clk = 1'b0, rst_n = 1'b0, car = 1'b0;
    always #5 clk = ~clk;

    wire [1:0] main_light, side_light;

    traffic #(.GREEN_TICKS(GREEN_TICKS), .YELLOW_TICKS(YELLOW_TICKS))
        dut (.clk(clk), .rst_n(rst_n), .car(car),
             .main_light(main_light), .side_light(side_light));

    reg [1:0] prev_main, prev_side;
    integer   errors = 0, cycles = 0, phase_len = 0;
    reg [1:0] phase_colour_main;

    function [39:0] name;                     // 5 chars
        input [1:0] c;
        begin
            case (c)
                GREEN  : name = "GREEN";
                YELLOW : name = "AMBER";
                default: name = " RED ";
            endcase
        end
    endfunction

    // ---- the property checks, run once per cycle -------------------------
    task check;
        begin
            // P1: mutual exclusion
            if (main_light == GREEN && side_light == GREEN) begin
                $display("  *** P1 VIOLATED at cycle %0d : both roads green",
                         cycles);
                errors = errors + 1;
            end
            // P2: green must be followed by yellow, never straight to red
            if (prev_main == GREEN && main_light == RED) begin
                $display("  *** P2 VIOLATED at cycle %0d : MAIN green->red",
                         cycles);
                errors = errors + 1;
            end
            if (prev_side == GREEN && side_light == RED) begin
                $display("  *** P2 VIOLATED at cycle %0d : SIDE green->red",
                         cycles);
                errors = errors + 1;
            end
        end
    endtask

    integer i;
    initial begin
        $dumpfile("build/traffic.vcd");
        $dumpvars(0, tb_traffic);

        $display("");
        $display("  === Moore traffic-light controller ===");
        $display("  green = %0d cycles, yellow = %0d cycles",
                 GREEN_TICKS, YELLOW_TICKS);
        $display("");
        $display("  cycle   car   MAIN    SIDE");
        $display("  -----   ---   -----   -----");

        rst_n = 1'b0;
        @(negedge clk);
        rst_n = 1'b1;
        prev_main = main_light;
        prev_side = side_light;

        for (i = 0; i < 40; i = i + 1) begin
            // a car arrives on the side road at cycle 8 and waits
            car = (i >= 8) ? 1'b1 : 1'b0;
            #1;
            check;
            $display("  %5d    %b    %0s   %0s", cycles, car,
                     name(main_light), name(side_light));
            prev_main = main_light;
            prev_side = side_light;
            cycles = cycles + 1;
            @(negedge clk);
        end

        $display("");
        $display("  cycles checked      : %0d", cycles);
        $display("  property violations : %0d", errors);
        if (errors == 0)
            $display("  PASS - mutual exclusion and yellow-before-red both hold");
        else
            $display("  FAIL - see the lines above");
        $display("");
        $finish;
    end

endmodule
