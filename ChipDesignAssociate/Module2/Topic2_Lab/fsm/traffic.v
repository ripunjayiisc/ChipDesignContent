// ---------------------------------------------------------------------------
//  traffic.v  -  Moore traffic-light controller
//
//  This file demonstrates the THREE-BLOCK FSM CODING PATTERN, which is the
//  house style used in almost every RTL group:
//
//     block 1  state register      sequential, non-blocking, reset here
//     block 2  next-state logic    combinational, always @(*), full case
//     block 3  output logic        combinational, depends on STATE ONLY
//
//  Because block 3 reads only `state`, this is a MOORE machine: the outputs
//  are a function of the present state, never of the inputs directly.  That
//  makes every output glitch-free and registered-clean one cycle after the
//  state changes.
//
//  The controller runs a two-road junction.  MAIN is the busy road, SIDE is
//  the minor road with a car sensor.  MAIN stays green until a car appears
//  on SIDE, then the sequence runs MAIN-YELLOW -> SIDE-GREEN -> SIDE-YELLOW
//  and back.  Green and yellow durations come from a down-counter so that
//  the same source works for any clock frequency.
// ---------------------------------------------------------------------------

module traffic #(
    parameter GREEN_TICKS  = 6,   // how long a green phase lasts
    parameter YELLOW_TICKS = 2    // how long a yellow phase lasts
)(
    input            clk,
    input            rst_n,       // asynchronous, active LOW
    input            car,         // car waiting on the side road
    output reg [1:0] main_light,  // 2'b00 red  2'b01 yellow  2'b10 green
    output reg [1:0] side_light
);

    // ---- state encoding ---------------------------------------------------
    // localparam, not `define: the names stay inside the module and cannot
    // leak into another file.  One-hot or binary is the synthesiser's choice;
    // we simply write readable names.
    localparam [1:0] S_MAIN_GREEN  = 2'd0,
                     S_MAIN_YELLOW = 2'd1,
                     S_SIDE_GREEN  = 2'd2,
                     S_SIDE_YELLOW = 2'd3;

    localparam [1:0] RED = 2'b00, YELLOW = 2'b01, GREEN = 2'b10;

    reg [1:0] state, next_state;
    // The timer is loaded with TICKS-1 and counts down to 0, so a phase
    // lasts exactly TICKS clock cycles.  Both parameters must be >= 1.
    reg [7:0] timer;              // counts down inside a phase
    wire      timeout = (timer == 8'd0);

    // ---- block 1: state register -----------------------------------------
    // Sequential.  Non-blocking assignment.  Reset is here and ONLY here.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= S_MAIN_GREEN;
        else        state <= next_state;
    end

    // the phase timer is sequential too; it reloads whenever the state moves
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            timer <= GREEN_TICKS - 1;
        else if (state != next_state)
            timer <= (next_state == S_MAIN_YELLOW ||
                      next_state == S_SIDE_YELLOW) ? YELLOW_TICKS - 1
                                                   : GREEN_TICKS - 1;
        else if (!timeout)
            timer <= timer - 8'd1;
    end

    // ---- block 2: next-state logic ---------------------------------------
    // Combinational.  Blocking assignment.  Note the DEFAULT ASSIGNMENT on
    // the first line: it guarantees next_state is written on every path, so
    // no latch can be inferred no matter what the case statement does.
    always @(*) begin
        next_state = state;                       // default: stay put
        case (state)
            S_MAIN_GREEN  : if (car && timeout) next_state = S_MAIN_YELLOW;
            S_MAIN_YELLOW : if (timeout)        next_state = S_SIDE_GREEN;
            S_SIDE_GREEN  : if (timeout)        next_state = S_SIDE_YELLOW;
            S_SIDE_YELLOW : if (timeout)        next_state = S_MAIN_GREEN;
            default       :                     next_state = S_MAIN_GREEN;
        endcase
    end

    // ---- block 3: output logic (MOORE - state only) ----------------------
    always @(*) begin
        main_light = RED;                          // defaults again
        side_light = RED;
        case (state)
            S_MAIN_GREEN  : begin main_light = GREEN;  side_light = RED;    end
            S_MAIN_YELLOW : begin main_light = YELLOW; side_light = RED;    end
            S_SIDE_GREEN  : begin main_light = RED;    side_light = GREEN;  end
            S_SIDE_YELLOW : begin main_light = RED;    side_light = YELLOW; end
            default       : begin main_light = RED;    side_light = RED;    end
        endcase
    end

endmodule
