-- ---------------------------------------------------------------------------
-- seq101_moore.vhd  -  the same Moore '101' detector as fsm/seq101_moore.v.
--
-- A state machine shows the two languages off better than a counter does,
-- because this is where their philosophies actually differ:
--
--   * VHDL has an ENUMERATED TYPE for states. `type state_t is (S_IDLE, ...)`
--     means the compiler will reject an assignment of any value that is not
--     one of those four. Verilog's localparam is just a number; nothing stops
--     you writing state <= 2'd7.
--   * The encoding is therefore the TOOL's choice in VHDL unless you override
--     it with an attribute, and YOUR choice in Verilog because you wrote the
--     numbers yourself.
--   * `case state is ... when others =>` is VHDL's `default`. It is not
--     optional here: without it the case would not be exhaustive and the
--     analyser would refuse to compile the file. Verilog would compile it
--     happily and hand you a latch.
--
-- That last point is the honest summary of the whole comparison: VHDL catches
-- more mistakes at compile time and costs more keystrokes; Verilog is faster
-- to write and trusts you more than it should.
-- ---------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;

entity seq101_moore is
    port (
        clk   : in  std_logic;
        rst_n : in  std_logic;                     -- asynchronous, active low
        din   : in  std_logic;
        det   : out std_logic
    );
end entity seq101_moore;

architecture rtl of seq101_moore is
    type state_t is (S_IDLE, S_1, S_10, S_101);
    signal state, next_state : state_t;
begin

    -- block 1 : state register
    process (clk, rst_n)
    begin
        if rst_n = '0' then
            state <= S_IDLE;
        elsif rising_edge(clk) then
            state <= next_state;
        end if;
    end process;

    -- block 2 : next-state logic
    process (state, din)
    begin
        next_state <= state;                       -- the default assignment
        case state is
            when S_IDLE => if din = '1' then next_state <= S_1;
                           else                 next_state <= S_IDLE; end if;
            when S_1    => if din = '1' then next_state <= S_1;
                           else                 next_state <= S_10;  end if;
            when S_10   => if din = '1' then next_state <= S_101;
                           else                 next_state <= S_IDLE; end if;
            when S_101  => if din = '1' then next_state <= S_1;
                           else                 next_state <= S_10;  end if;
            when others => next_state <= S_IDLE;
        end case;
    end process;

    -- block 3 : output logic, state only
    det <= '1' when state = S_101 else '0';

end architecture rtl;
