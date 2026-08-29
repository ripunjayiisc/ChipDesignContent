-- ---------------------------------------------------------------------------
-- counter.vhd  -  the same design as rtl/counter.v, in VHDL.
--
-- Read the two files side by side. The DESIGN is identical: a clocked process,
-- a synchronous reset, an enable, a vector, a wrap. Everything that differs is
-- notation.
--
-- The differences worth noticing:
--   * VHDL makes you declare the libraries you use. Verilog has none to declare.
--   * VHDL separates the ENTITY (the interface) from the ARCHITECTURE (the
--     implementation). Verilog puts both in one module.
--   * VHDL is strongly typed: unsigned and std_logic_vector are different
--     types and you must convert between them explicitly. Verilog would just
--     let you add 1 to anything.
--   * VHDL is not case sensitive. Verilog is.
-- ---------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
    generic (WIDTH : positive := 4);
    port (
        clk   : in  std_logic;
        rst   : in  std_logic;                     -- synchronous, active high
        en    : in  std_logic;
        count : out std_logic_vector(WIDTH-1 downto 0);
        tc    : out std_logic                      -- terminal count: all ones
    );
end entity counter;

architecture rtl of counter is
    signal cnt : unsigned(WIDTH-1 downto 0) := (others => '0');
begin

    process (clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                cnt <= (others => '0');
            elsif en = '1' then
                cnt <= cnt + 1;
            end if;
        end if;
    end process;

    count <= std_logic_vector(cnt);
    tc    <= '1' when cnt = (cnt'range => '1') else '0';

end architecture rtl;
