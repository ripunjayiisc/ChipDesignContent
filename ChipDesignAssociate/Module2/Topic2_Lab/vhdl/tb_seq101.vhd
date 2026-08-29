-- Drives the same 17-bit stream as fsm/tb_seq101_trace.v and prints one line
-- per cycle in the same format, so the two transcripts can be diffed.
library ieee;
use ieee.std_logic_1164.all;
use std.textio.all;

entity tb_seq101 is
end entity tb_seq101;

architecture sim of tb_seq101 is
    constant N      : integer := 17;
    constant PERIOD : time    := 10 ns;

    signal clk   : std_logic := '0';
    signal rst_n : std_logic := '0';
    signal din   : std_logic := '0';
    signal det   : std_logic;
    signal done  : boolean   := false;

    type bit_array is array (0 to N-1) of std_logic;
    constant STREAM : bit_array :=
        ('1','1','0','1','1','0','1','0','1','0','1','0','0','1','1','0','1');
begin

    dut : entity work.seq101_moore
        port map (clk => clk, rst_n => rst_n, din => din, det => det);

    clk <= not clk after PERIOD/2 when not done else '0';

    stim : process
        variable l : line;

        function ch (b : std_logic) return string is
        begin
            if b = '1' then return "1"; else return "0"; end if;
        end function;
    begin
        rst_n <= '0';
        wait until falling_edge(clk);
        rst_n <= '1';

        for i in 0 to N-1 loop
            din <= STREAM(i);
            wait for 1 ns;
            write(l, string'("cycle "));
            write(l, i);
            write(l, string'(" din="));
            write(l, ch(din));
            write(l, string'(" det="));
            write(l, ch(det));
            writeline(output, l);
            wait until falling_edge(clk);
        end loop;

        done <= true;
        write(l, string'("VHDL detector run complete"));
        writeline(output, l);
        wait;
    end process;

end architecture sim;
