-- Drives the VHDL counter through the same stimulus as tb_counter.v drives the
-- Verilog one, and prints the same lines, so the two logs can be diffed.
library ieee;
use ieee.std_logic_1164.all;
use std.textio.all;

entity tb_counter is end entity;

architecture sim of tb_counter is
    signal clk, rst, en, tc : std_logic := '0';
    signal count            : std_logic_vector(3 downto 0);
    signal stop             : boolean := false;

    function to_str (v : std_logic_vector) return string is
        variable s : string(1 to v'length);
        variable k : integer := 1;
    begin
        for i in v'range loop
            if v(i) = '1' then s(k) := '1'; else s(k) := '0'; end if;
            k := k + 1;
        end loop;
        return s;
    end function;
begin

    dut : entity work.counter
        generic map (WIDTH => 4)
        port map (clk => clk, rst => rst, en => en, count => count, tc => tc);

    clk <= not clk after 5 ns when not stop else '0';

    process
        variable l : line;
    begin
        rst <= '1'; en <= '0';
        wait until rising_edge(clk); wait for 1 ns;
        rst <= '0'; en <= '1';

        for i in 0 to 17 loop
            wait until rising_edge(clk);
            wait for 1 ns;
            write(l, string'("  cycle "));
            write(l, i);
            write(l, string'("  count="));
            write(l, to_str(count));
            write(l, string'("  tc="));
            if tc = '1' then write(l, string'("1")); else write(l, string'("0")); end if;
            writeline(output, l);
        end loop;

        stop <= true;
        wait for 20 ns;
        report "VHDL run complete" severity note;
        wait;
    end process;

end architecture sim;
