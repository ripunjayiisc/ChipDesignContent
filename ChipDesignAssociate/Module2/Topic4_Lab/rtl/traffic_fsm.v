// ---------------------------------------------------------------------------
// traffic_fsm.v  -  traffic-light controller  (Lab L3)
//
// A Moore FSM with a timer. This is the FSMD pattern in miniature: the FSM is
// the controller, the timer is a one-element datapath, and the 'timer done'
// flag is the status signal that comes back.
//
//   MAIN_GREEN -> MAIN_YELLOW -> SIDE_GREEN -> SIDE_YELLOW -> MAIN_GREEN
//
// Durations are parameters so the testbench can use short ones.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module traffic_fsm #(
    parameter integer T_GREEN  = 20,
    parameter integer T_YELLOW = 5
)(
    input  wire       clk,
    input  wire       rst_n,
    input  wire       tick,          // one pulse per time unit (e.g. 1 Hz)
    output reg  [2:0] main_light,    // {red, yellow, green}
    output reg  [2:0] side_light
);

    localparam [1:0] MAIN_GREEN  = 2'd0,
                     MAIN_YELLOW = 2'd1,
                     SIDE_GREEN  = 2'd2,
                     SIDE_YELLOW = 2'd3;

    localparam [2:0] RED = 3'b100, YELLOW = 3'b010, GREEN = 3'b001;

    reg [1:0]  state, next;
    reg [7:0]  timer;
    wire       done;

    // how long the CURRENT state lasts
    reg [7:0] limit;
    always @(*) begin
        case (state)
            MAIN_GREEN : limit = T_GREEN [7:0];
            MAIN_YELLOW: limit = T_YELLOW[7:0];
            SIDE_GREEN : limit = T_GREEN [7:0];
            SIDE_YELLOW: limit = T_YELLOW[7:0];
            default    : limit = T_GREEN [7:0];
        endcase
    end

    assign done = (timer >= limit - 1'b1);

    // ---- BLOCK 1 : state register + timer ----
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= MAIN_GREEN;
            timer <= 8'd0;
        end else if (tick) begin
            if (done) begin
                state <= next;
                timer <= 8'd0;
            end else begin
                timer <= timer + 1'b1;
            end
        end
    end

    // ---- BLOCK 2 : next-state logic ----
    always @(*) begin
        next = state;                      // default - no latch
        case (state)
            MAIN_GREEN : next = MAIN_YELLOW;
            MAIN_YELLOW: next = SIDE_GREEN;
            SIDE_GREEN : next = SIDE_YELLOW;
            SIDE_YELLOW: next = MAIN_GREEN;
            default    : next = MAIN_GREEN;   // SAFE FSM
        endcase
    end

    // ---- BLOCK 3 : output logic (Moore - state only) ----
    always @(*) begin
        main_light = RED;                  // defaults
        side_light = RED;
        case (state)
            MAIN_GREEN : begin main_light = GREEN;  side_light = RED;    end
            MAIN_YELLOW: begin main_light = YELLOW; side_light = RED;    end
            SIDE_GREEN : begin main_light = RED;    side_light = GREEN;  end
            SIDE_YELLOW: begin main_light = RED;    side_light = YELLOW; end
            default    : begin main_light = RED;    side_light = RED;    end
        endcase
    end

endmodule

`default_nettype wire
