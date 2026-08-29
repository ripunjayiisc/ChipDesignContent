# -*- coding: utf-8 -*-
"""
liberty.py  -  a minimal Liberty (.lib) reader.

A real Liberty parser handles a large grammar: 2-D delay tables indexed by
input slew and output load, operating-condition groups, wire-load models,
statetables, and much else. This one reads only what the Topic 6 STA engine
needs, which is enough to show what an STA tool is actually reading:

    * for a combinational cell : intrinsic delay, load factor, input capacitance
    * for a flip-flop          : clock-to-Q, setup, hold, input capacitance

The point of reading it yourself once is that "the library" stops being a
mysterious file the tool consumes and becomes a table of numbers you could
have written down.
"""
import re
import os


class Cell(object):
    __slots__ = ("name", "intrinsic", "load_factor", "input_cap",
                 "clk_to_q", "setup", "hold", "area", "is_ff", "pins")

    def __init__(self, name):
        self.name = name
        self.intrinsic = 0.0
        self.load_factor = 0.0
        self.input_cap = 1.0
        self.clk_to_q = None
        self.setup = None
        self.hold = None
        self.area = 0.0
        self.is_ff = False
        self.pins = {}          # pin name -> "input" | "output" | "clock"

    def __repr__(self):
        if self.is_ff:
            return ("Cell(%s ff clk_to_q=%.3f setup=%.3f hold=%.3f)"
                    % (self.name, self.clk_to_q, self.setup, self.hold))
        return ("Cell(%s comb intrinsic=%.3f load=%.3f cap=%.2f)"
                % (self.name, self.intrinsic, self.load_factor, self.input_cap))


_NUM = r"([-+]?[0-9]*\.?[0-9]+)"


def _strip_comments(text):
    return re.sub(r"/\*.*?\*/", " ", text, flags=re.S)


def read_liberty(path):
    """Return {cell_name: Cell}."""
    with open(path) as f:
        text = _strip_comments(f.read())

    cells = {}
    # Split on 'cell (NAME) {' and take the balanced body by brace counting.
    for m in re.finditer(r"\bcell\s*\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\)\s*\{", text):
        name = m.group(1)
        i = m.end()
        depth = 1
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[m.end():i - 1]

        c = Cell(name)
        for attr, field in (("cda_intrinsic", "intrinsic"),
                            ("cda_load_factor", "load_factor"),
                            ("cda_input_cap", "input_cap"),
                            ("cda_clk_to_q", "clk_to_q"),
                            ("cda_setup", "setup"),
                            ("cda_hold", "hold"),
                            ("area", "area")):
            mm = re.search(attr + r"\s*:\s*" + _NUM, body)
            if mm:
                setattr(c, field, float(mm.group(1)))

        c.is_ff = (c.clk_to_q is not None)

        for pm in re.finditer(r"\bpin\s*\(\s*([A-Za-z_][A-Za-z_0-9]*)\s*\)\s*\{([^}]*)\}",
                              body):
            pname, pbody = pm.group(1), pm.group(2)
            if re.search(r"clock\s*:\s*true", pbody):
                c.pins[pname] = "clock"
            elif re.search(r"direction\s*:\s*output", pbody):
                c.pins[pname] = "output"
            else:
                c.pins[pname] = "input"

        cells[name] = c
    return cells


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    lib = read_liberty(os.path.join(here, "..", "lib", "cda_edu.lib"))
    print("%d cells read from cda_edu.lib\n" % len(lib))
    print("%-9s %-5s %9s %9s %9s %9s %6s" %
          ("cell", "type", "intrinsic", "load/ld", "clk->Q", "setup", "cap"))
    print("-" * 66)
    for n in sorted(lib):
        c = lib[n]
        print("%-9s %-5s %9.3f %9.3f %9s %9s %6.2f" %
              (c.name, "FF" if c.is_ff else "comb", c.intrinsic, c.load_factor,
               "%.3f" % c.clk_to_q if c.is_ff else "-",
               "%.3f" % c.setup if c.is_ff else "-", c.input_cap))
