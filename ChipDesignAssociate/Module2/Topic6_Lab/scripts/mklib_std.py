#!/usr/bin/env python3
"""Generate lib/cda_edu_std.lib - a standards-compliant Liberty view of the
teaching library, for tools such as OpenSTA that will not accept the custom
cda_* attributes.

The delay model is the same straight line:

    delay = intrinsic + load_factor * output_load

expressed as a 1x5 lookup table over output capacitance, which is the
smallest form every Liberty reader accepts. Timing values are IDENTICAL to
cda_edu.lib, so a report from OpenSTA and a report from sta.py can be
compared number for number.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from sta.liberty import read_liberty                              # noqa: E402

LOADS = [0.0, 1.5, 3.0, 6.0, 12.0]
SLEWS = [0.05, 0.20]

# input pins, the boolean function of the output, and the timing sense of
# each input pin. Unateness is not decoration: a real STA tool uses it to
# decide whether a rising input produces a rising or a falling output, and
# therefore which delay arc applies.
POS, NEG, NON = "positive_unate", "negative_unate", "non_unate"
FUNC = {
    "INV":     (["A"], "!A", {"A": NEG}),
    "BUF":     (["A"], "A", {"A": POS}),
    "NAND2":   (["A", "B"], "!(A B)", {"A": NEG, "B": NEG}),
    "NOR2":    (["A", "B"], "!(A+B)", {"A": NEG, "B": NEG}),
    "AND2":    (["A", "B"], "(A B)", {"A": POS, "B": POS}),
    "OR2":     (["A", "B"], "(A+B)", {"A": POS, "B": POS}),
    "ANDNOT2": (["A", "B"], "(A !B)", {"A": POS, "B": NEG}),
    "ORNOT2":  (["A", "B"], "(A+!B)", {"A": POS, "B": NEG}),
    "XOR2":    (["A", "B"], "(A^B)", {"A": NON, "B": NON}),
    "XNOR2":   (["A", "B"], "!(A^B)", {"A": NON, "B": NON}),
    "MUX2":    (["A", "B", "S"], "(!S A)+(S B)",
                {"A": POS, "B": POS, "S": NON}),
}
FF = {"DFF": None, "DFFR": "RN", "DFFE": "EN"}


def tbl(vals, indent):
    p = " " * indent
    return "%svalues(\"%s\");" % (p, ", ".join("%.4f" % v for v in vals))


def main():
    lib = read_liberty(os.path.join(HERE, "..", "lib", "cda_edu.lib"))
    out = []
    a = out.append

    a("/* --------------------------------------------------------------------")
    a(" * cda_edu_std.lib  -  GENERATED FILE. Do not edit; edit cda_edu.lib and")
    a(" * re-run  python3 scripts/mklib_std.py  instead.")
    a(" *")
    a(" * A standards-compliant Liberty view of the teaching library, for tools")
    a(" * that reject the custom cda_* attributes (OpenSTA, PrimeTime, ...).")
    a(" * The delay numbers are identical to cda_edu.lib, so the two reports")
    a(" * can be compared line by line.")
    a(" * ----------------------------------------------------------------- */")
    a("")
    a("library (cda_edu_std) {")
    a("  technology (cmos);")
    a("  delay_model              : table_lookup;")
    a("  time_unit                : \"1ns\";")
    a("  voltage_unit             : \"1V\";")
    a("  current_unit             : \"1mA\";")
    a("  pulling_resistance_unit  : \"1kohm\";")
    a("  leakage_power_unit       : \"1nW\";")
    a("  capacitive_load_unit     (1, pf);")
    a("  nom_voltage              : 1.20;")
    a("  nom_temperature          : 25.0;")
    a("  nom_process              : 1.0;")
    a("  default_max_transition   : 1.0;")
    a("")
    a("  lu_table_template (delay_template) {")
    a("    variable_1 : input_net_transition;")
    a("    variable_2 : total_output_net_capacitance;")
    a("    index_1 (\"%s\");" % ", ".join("%.2f" % s for s in SLEWS))
    a("    index_2 (\"%s\");" % ", ".join("%.2f" % L for L in LOADS))
    a("  }")
    a("  lu_table_template (constraint_template) {")
    a("    variable_1 : related_pin_transition;")
    a("    variable_2 : constrained_pin_transition;")
    a("    index_1 (\"%s\");" % ", ".join("%.2f" % s for s in SLEWS))
    a("    index_2 (\"%s\");" % ", ".join("%.2f" % s for s in SLEWS))
    a("  }")
    a("")

    for name in sorted(lib):
        c = lib[name]
        if name in FUNC:
            ins, fn, sense = FUNC[name]
            a("  cell (%s) {" % name)
            a("    area : %.1f;" % c.area)
            for p in ins:
                a("    pin (%s) { direction : input; capacitance : %.2f; }"
                  % (p, c.input_cap))
            a("    pin (Y) {")
            a("      direction : output;")
            a("      function  : \"%s\";" % fn)
            a("      max_capacitance : 16.0;")
            for p in ins:
                a("      timing () {")
                a("        related_pin  : \"%s\";" % p)
                a("        timing_sense : %s;" % sense[p])
                for kind in ("cell_rise", "cell_fall"):
                    a("        %s (delay_template) {" % kind)
                    a("          values(\"%s\", \\" % ", ".join(
                        "%.4f" % (c.intrinsic + c.load_factor * L) for L in LOADS))
                    a("                 \"%s\");" % ", ".join(
                        "%.4f" % (c.intrinsic + c.load_factor * L) for L in LOADS))
                    a("        }")
                for kind in ("rise_transition", "fall_transition"):
                    a("        %s (delay_template) {" % kind)
                    a("          values(\"%s\", \\" % ", ".join(
                        "%.4f" % (0.02 + 0.004 * L) for L in LOADS))
                    a("                 \"%s\");" % ", ".join(
                        "%.4f" % (0.02 + 0.004 * L) for L in LOADS))
                    a("        }")
                a("      }")
            a("    }")
            a("  }")
            a("")
        elif name in FF:
            extra = FF[name]
            a("  cell (%s) {" % name)
            a("    area : %.1f;" % c.area)
            a("    ff (IQ, IQN) {")
            a("      clocked_on : \"C\";")
            a("      next_state : \"D\";")
            if name == "DFFR":
                a("      clear      : \"!RN\";")
            a("    }")
            a("    pin (C) { direction : input; capacitance : %.2f; clock : true; }"
              % c.input_cap)
            a("    pin (D) {")
            a("      direction : input; capacitance : %.2f;" % c.input_cap)
            a("      timing () {")
            a("        related_pin   : \"C\";")
            a("        timing_type   : setup_rising;")
            a("        rise_constraint (constraint_template) {")
            a("          values(\"%.4f, %.4f\", \"%.4f, %.4f\");"
              % (c.setup, c.setup, c.setup, c.setup))
            a("        }")
            a("        fall_constraint (constraint_template) {")
            a("          values(\"%.4f, %.4f\", \"%.4f, %.4f\");"
              % (c.setup, c.setup, c.setup, c.setup))
            a("        }")
            a("      }")
            a("      timing () {")
            a("        related_pin   : \"C\";")
            a("        timing_type   : hold_rising;")
            a("        rise_constraint (constraint_template) {")
            a("          values(\"%.4f, %.4f\", \"%.4f, %.4f\");"
              % (c.hold, c.hold, c.hold, c.hold))
            a("        }")
            a("        fall_constraint (constraint_template) {")
            a("          values(\"%.4f, %.4f\", \"%.4f, %.4f\");"
              % (c.hold, c.hold, c.hold, c.hold))
            a("        }")
            a("      }")
            a("    }")
            if extra and name == "DFFR":
                a("    pin (RN) { direction : input; capacitance : %.2f; }" % c.input_cap)
            elif extra:
                a("    pin (EN) { direction : input; capacitance : %.2f; }" % c.input_cap)
            a("    pin (Q) {")
            a("      direction : output;")
            a("      function  : \"IQ\";")
            a("      max_capacitance : 16.0;")
            a("      timing () {")
            a("        related_pin  : \"C\";")
            a("        timing_type  : rising_edge;")
            for kind in ("cell_rise", "cell_fall"):
                a("        %s (delay_template) {" % kind)
                a("          values(\"%s\", \\" % ", ".join(
                    "%.4f" % (c.clk_to_q + c.load_factor * L) for L in LOADS))
                a("                 \"%s\");" % ", ".join(
                    "%.4f" % (c.clk_to_q + c.load_factor * L) for L in LOADS))
                a("        }")
            for kind in ("rise_transition", "fall_transition"):
                a("        %s (delay_template) {" % kind)
                a("          values(\"%s\", \\" % ", ".join(
                    "%.4f" % (0.02 + 0.004 * L) for L in LOADS))
                a("                 \"%s\");" % ", ".join(
                    "%.4f" % (0.02 + 0.004 * L) for L in LOADS))
                a("        }")
            a("      }")
            a("    }")
            a("  }")
            a("")

    a("}")

    dst = os.path.join(HERE, "..", "lib", "cda_edu_std.lib")
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")
    print("wrote lib/cda_edu_std.lib  -  %d cells, %d lines"
          % (sum(1 for n in lib if n in FUNC or n in FF), len(out) + 1))
    print("check it with:   sta -no_splash -exit "
          "-x 'read_liberty lib/cda_edu_std.lib'")


if __name__ == "__main__":
    main()
