-- counter4.vhd - exactly the same counter as rtl/counter4.v, in VHDL.
--
-- Compare the two files side by side. VHDL is more verbose and far more
-- strongly typed; the HARDWARE described is identical, and a synthesis tool
-- produces the same gates from either. Choosing between them is a matter of
-- house style, not of what the silicon can do.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter4 is
    port (clk : in  std_logic;
          rst : in  std_logic;                        -- synchronous, active high
          q   : out std_logic_vector(3 downto 0));
end entity counter4;

architecture rtl of counter4 is
    signal cnt : unsigned(3 downto 0) := (others => '0');
begin
    process (clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                cnt <= (others => '0');
            else
                cnt <= cnt + 1;
            end if;
        end if;
    end process;

    q <= std_logic_vector(cnt);
end architecture rtl;
