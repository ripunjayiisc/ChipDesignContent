// ---------------------------------------------------------------------------
// tb_uart.v  -  UART loopback test  (Lab L5, the capstone)
//
// The transmitter's tx line is wired straight into the receiver's rx line.
// Whatever we send must come back out identical. This is the single most
// valuable testbench pattern for any serial protocol: you do not have to model
// the wire format at all, because the two ends check each other.
//
// A second, independent test then decodes the tx line BY HAND, bit by bit, to
// prove the frame really is 8N1 and not merely self-consistent.
// ---------------------------------------------------------------------------
`timescale 1ns / 1ps

module tb_uart;

    localparam integer CPB = 16;          // clocks per bit - small, for speed

    reg clk = 1'b0, rst_n = 1'b0;
    integer errors = 0;
    integer i;

    always #5 clk = ~clk;

    task check1(input cond, input [255:0] msg);
        begin
            if (!cond) begin
                $display("  FAIL: %0s   (t=%0t)", msg, $time);
                errors = errors + 1;
            end
        end
    endtask

    // ------------------------------------------------ DUTs, wired loopback
    reg        tx_start;
    reg  [7:0] tx_data;
    wire       line;                      // the serial wire
    wire       tx_busy, tx_done;
    wire [7:0] rx_data;
    wire       rx_valid, rx_frame_err;

    uart_tx #(.CLKS_PER_BIT(CPB)) u_tx (
        .clk(clk), .rst_n(rst_n), .tx_start(tx_start), .tx_data(tx_data),
        .tx(line), .busy(tx_busy), .tx_done(tx_done));

    uart_rx #(.CLKS_PER_BIT(CPB)) u_rx (
        .clk(clk), .rst_n(rst_n), .rx(line),
        .rx_data(rx_data), .rx_valid(rx_valid), .frame_error(rx_frame_err));

    // capture whatever the receiver hands us
    reg [7:0] got;
    reg       got_valid;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            got <= 8'd0; got_valid <= 1'b0;
        end else begin
            if (rx_valid) begin got <= rx_data; got_valid <= 1'b1; end
        end
    end

    task send(input [7:0] d);
        begin
            @(posedge clk); #1;
            tx_data = d; tx_start = 1'b1;
            @(posedge clk); #1 tx_start = 1'b0;
            wait (tx_done == 1'b1);
            @(posedge clk);
        end
    endtask

    // ---- an INDEPENDENT decoder: read the line by hand, 8N1 ----
    task decode_line(output [7:0] byte_out, output ok);
        integer b;
        begin
            byte_out = 8'd0;
            ok       = 1'b1;
            @(negedge line);                              // start bit
            repeat (CPB + CPB/2) @(posedge clk);          // to the middle of D0
            for (b = 0; b < 8; b = b + 1) begin
                byte_out[b] = line;                       // LSB first
                repeat (CPB) @(posedge clk);
            end
            if (line !== 1'b1) ok = 1'b0;                 // stop bit must be high
        end
    endtask

    initial begin
        $dumpfile("uart.vcd");
        $dumpvars(0, tb_uart);
        $display("=== L5 UART loopback ===");

        tx_start = 1'b0; tx_data = 8'd0;
        #12 rst_n = 1'b1;
        #1;
        check1(line === 1'b1, "uart: tx line does not idle high");
        check1(tx_busy === 1'b0, "uart: busy asserted while idle");

        // ---------------- loopback over a set of tricky patterns ----------
        begin : loopback
            reg [7:0] patterns [0:7];
            patterns[0] = 8'h00;      // all zeros
            patterns[1] = 8'hFF;      // all ones
            patterns[2] = 8'h55;      // alternating
            patterns[3] = 8'hAA;      // alternating, inverted
            patterns[4] = 8'h41;      // 'A'
            patterns[5] = 8'h0F;
            patterns[6] = 8'hF0;
            patterns[7] = 8'h81;      // both ends set

            for (i = 0; i < 8; i = i + 1) begin
                got_valid = 1'b0;
                send(patterns[i]);
                // the receiver finishes a little after the transmitter
                repeat (CPB * 2) @(posedge clk);
                check1(got_valid === 1'b1, "uart: receiver produced no byte");
                if (got !== patterns[i]) begin
                    $display("  FAIL: uart loopback sent %02h, got %02h",
                             patterns[i], got);
                    errors = errors + 1;
                end
                check1(rx_frame_err === 1'b0, "uart: spurious framing error");
            end
        end

        // ---------------- independent frame check ----------------
        begin : frame_check
            reg [7:0] decoded;
            reg       frame_ok;
            fork
                begin
                    decode_line(decoded, frame_ok);
                    if (decoded !== 8'h3C) begin
                        $display("  FAIL: hand-decoded frame gave %02h, expected 3C",
                                 decoded);
                        errors = errors + 1;
                    end
                    check1(frame_ok === 1'b1, "uart: stop bit was not high");
                end
                begin
                    @(posedge clk); #1;
                    tx_data = 8'h3C; tx_start = 1'b1;
                    @(posedge clk); #1 tx_start = 1'b0;
                end
            join
        end

        // ---------------- busy must be honest ----------------
        @(posedge clk); #1;
        wait (tx_busy == 1'b0);
        check1(tx_busy === 1'b0, "uart: busy stuck high after the frame");

        if (errors == 0) $display("PASS - L5 UART, loopback and frame both correct");
        else             $display("FAIL - %0d error(s)", errors);
        $finish;
    end

endmodule
