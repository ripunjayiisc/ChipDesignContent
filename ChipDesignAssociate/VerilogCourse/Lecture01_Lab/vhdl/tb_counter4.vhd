-- tb_counter4.vhd - the same stimulus as the Verilog test bench, so the two
-- languages can be compared on identical input.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

entity tb_counter4 is
end entity tb_counter4;

architecture sim of tb_counter4 is
    signal clk : std_logic := '0';
    signal rst : std_logic := '1';
    signal q   : std_logic_vector(3 downto 0);
    signal run : boolean   := true;
begin
    dut : entity work.counter4 port map (clk => clk, rst => rst, q => q);

    clk <= not clk after 5 ns when run else '0';

    stim : process
        variable l        : line;
        variable expected : unsigned(3 downto 0);
        variable errors   : integer := 0;
    begin
        -- the rising edge at 5 ns clears the register, and we release reset on
        -- the falling edge at 10 ns, so the next rising edge already counts
        wait until falling_edge(clk);
        rst      <= '0';
        expected := to_unsigned(1, 4);

        for i in 0 to 19 loop
            wait until falling_edge(clk);
            if unsigned(q) /= expected then
                write(l, string'("MISMATCH at step "));
                write(l, i);
                write(l, string'(": q="));
                write(l, to_integer(unsigned(q)));
                write(l, string'(" expected="));
                write(l, to_integer(expected));
                writeline(output, l);
                errors := errors + 1;
            end if;
            expected := expected + 1;
        end loop;

        if errors = 0 then
            write(l, string'("PASS  counter4 counted 0..15 and wrapped correctly"));
        else
            write(l, string'("FAIL  "));
            write(l, errors);
            write(l, string'(" mismatches"));
        end if;
        writeline(output, l);

        run <= false;
        wait;
    end process stim;
end architecture sim;
