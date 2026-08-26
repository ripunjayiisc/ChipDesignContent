// ---------------------------------------------------------------------------
// vending_fsm.v  -  vending machine controller  (Lab L3)
//
// Item costs 30. Accepts 5, 10 and 20 coins. Dispenses when the credit reaches
// 30 or more, and returns any change as a value on chg_amt.
//
// A Mealy machine would need fewer states; this is written as a Moore machine
// with an explicit credit register, which is both clearer and much closer to
// how you would really build it.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps
`default_nettype none

module vending_fsm (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       coin_valid,
    input  wire [1:0] coin,         // 00 = 5, 01 = 10, 10 = 20
    input  wire       cancel,
    output reg        dispense,
    output reg        return_coins,
    output reg  [5:0] chg_amt,
    output wire [5:0] credit
);

    localparam [1:0] IDLE = 2'd0, COLLECT = 2'd1, DISPENSE = 2'd2, REFUND = 2'd3;
    localparam [5:0] PRICE = 6'd30;

    reg [1:0] state, next;
    reg [5:0] cred;
    assign credit = cred;

    reg [5:0] coin_val;
    always @(*) begin
        case (coin)
            2'b00:   coin_val = 6'd5;
            2'b01:   coin_val = 6'd10;
            2'b10:   coin_val = 6'd20;
            default: coin_val = 6'd0;
        endcase
    end

    // ---- BLOCK 1 : state register + credit ----
    //
    // Note WHEN the credit is cleared. It must be cleared as we LEAVE the
    // DISPENSE/REFUND state, not as we enter it - the output logic still needs
    // the value while we are in that state, to work out the change. Clearing
    // it a cycle early is a real bug, and one the testbench catches.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            cred  <= 6'd0;
        end else begin
            state <= next;
            if (state == DISPENSE || state == REFUND)
                cred <= 6'd0;                        // clear on the way OUT
            else if (coin_valid)
                cred <= cred + coin_val;
        end
    end

    // ---- BLOCK 2 : next-state logic ----
    always @(*) begin
        next = state;
        case (state)
            IDLE:     if (cancel)                                  next = REFUND;
                      else if (coin_valid)                         next = COLLECT;
            COLLECT:  if (cancel)                                  next = REFUND;
                      else if (cred >= PRICE)                      next = DISPENSE;
            DISPENSE:                                              next = IDLE;
            REFUND:                                                next = IDLE;
            default:                                               next = IDLE;
        endcase
    end

    // ---- BLOCK 3 : output logic ----
    always @(*) begin
        dispense     = 1'b0;
        return_coins = 1'b0;
        chg_amt      = 6'd0;
        case (state)
            DISPENSE: begin
                dispense = 1'b1;
                chg_amt  = (cred > PRICE) ? (cred - PRICE) : 6'd0;
            end
            REFUND: begin
                return_coins = 1'b1;
                chg_amt      = cred;
            end
            default: ;
        endcase
    end

endmodule

`default_nettype wire
