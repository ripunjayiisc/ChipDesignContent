# -*- coding: utf-8 -*-
"""
sta.py  -  a real, working static timing analyser, in about 400 lines.

It reads a Yosys JSON netlist and the Liberty library in lib/, builds the
timing graph, and computes arrival times, required times and slack for every
endpoint - exactly the algorithm a commercial STA tool runs, minus the
industrial-strength delay modelling.

    usage:  python3 sta/sta.py build/<top>.json <top> [-c constraints.sdc]
                              [-p PERIOD] [--paths N] [--hold] [--csv]

WHY IT EXISTS
-------------
A timing report is the single most important document in digital design, and
most people meet it as output from a tool they cannot see inside. Writing the
analyser removes the mystery: arrival time is a forward maximum over a graph,
required time is a backward minimum, and slack is the difference. Everything
else - clock skew, uncertainty, multicycle paths, false paths - is a small
adjustment to one of those three numbers.

WHAT IT MODELS
--------------
  * one clock, defined by create_clock, with a period and optional
    uncertainty (jitter + margin)
  * per-register clock arrival, so clock SKEW can be modelled and hold
    violations can be produced and then fixed
  * combinational delay = intrinsic + load_factor x (sum of driven pin caps),
    so fanout matters, as it does in reality
  * setup and hold checks at every flip-flop D pin
  * input_delay / output_delay for paths that cross the module boundary
  * set_false_path and set_multicycle_path

WHAT IT DOES NOT MODEL
----------------------
  * input slew and its effect on delay (real libraries use 2-D tables)
  * wire RC delay - here a net costs only the load its sinks present
  * on-chip variation, derating, min/max corners as separate libraries
  * transparent latches, multiple clocks, generated clocks, CDC
These are named on purpose: knowing what your analyser ignores is part of
knowing what its answer is worth.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from liberty import read_liberty                                    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LIB = os.path.join(HERE, "..", "lib", "cda_edu.lib")

# Yosys generic cell type  ->  library cell name
CELLMAP = {
    "$_NOT_": "INV",     "$_BUF_": "BUF",
    "$_AND_": "AND2",    "$_OR_": "OR2",
    "$_NAND_": "NAND2",  "$_NOR_": "NOR2",
    "$_XOR_": "XOR2",    "$_XNOR_": "XNOR2",
    "$_ANDNOT_": "ANDNOT2", "$_ORNOT_": "ORNOT2",
    "$_MUX_": "MUX2",
    "$_DFF_P_": "DFF",
    "$_DFF_PN0_": "DFFR", "$_DFF_PP0_": "DFFR",
    "$_DFF_PN1_": "DFFR", "$_DFF_PP1_": "DFFR",
    "$_DFFE_PP_": "DFFE", "$_DFFE_PN_": "DFFE",
    "$_SDFF_PP0_": "DFFR", "$_SDFF_PN0_": "DFFR",
    "$_DFFE_PN0P_": "DFFE", "$_DFFE_PP0P_": "DFFE",
    "$_DFFE_PN1P_": "DFFE", "$_DFFE_PP1P_": "DFFE",
}


# ===========================================================================
#  Constraints  (a small subset of SDC)
# ===========================================================================
class Constraints(object):
    def __init__(self):
        self.period = 10.0
        self.clock_name = "clk"
        self.uncertainty_setup = 0.0
        self.uncertainty_hold = 0.0
        self.input_delay = {}          # port -> ns after the clock edge
        self.output_delay = {}         # port -> ns required before the edge
        self.default_input_delay = None
        self.default_output_delay = None
        self.skew = {}                 # regex -> ns added to that reg's clock
        self.false_paths = []          # list of (from_re, to_re)
        self.multicycle = []           # list of (from_re, to_re, n)
        self.max_fanout = None

    def clock_arrival(self, reg_name):
        t = 0.0
        for pat, val in self.skew.items():
            if re.search(pat, reg_name):
                t += val
        return t

    def is_false(self, a, b):
        for fa, fb in self.false_paths:
            if re.search(fa, a) and re.search(fb, b):
                return True
        return False

    def cycles(self, a, b):
        n = 1
        for ma, mb, k in self.multicycle:
            if re.search(ma, a) and re.search(mb, b):
                n = k
        return n


def read_sdc(path):
    """Read the SDC subset this analyser understands."""
    c = Constraints()
    if not path:
        return c
    with open(path) as f:
        for raw in f:
            line = raw.split("#")[0].strip()
            if not line:
                continue
            m = re.match(r"create_clock\s+.*-period\s+([\d.]+)", line)
            if m:
                c.period = float(m.group(1))
                mn = re.search(r"-name\s+(\w+)", line)
                if mn:
                    c.clock_name = mn.group(1)
                continue
            m = re.match(r"set_clock_uncertainty\s+([\d.]+)(?:\s+-setup)?", line)
            if m:
                v = float(m.group(1))
                if "-hold" in line:
                    c.uncertainty_hold = v
                elif "-setup" in line:
                    c.uncertainty_setup = v
                else:
                    c.uncertainty_setup = c.uncertainty_hold = v
                continue
            m = re.match(r"set_input_delay\s+([\d.]+)(?:\s+.*?-port\s+(\S+))?", line)
            if m:
                if m.group(2):
                    c.input_delay[m.group(2)] = float(m.group(1))
                else:
                    c.default_input_delay = float(m.group(1))
                continue
            m = re.match(r"set_output_delay\s+([\d.]+)(?:\s+.*?-port\s+(\S+))?", line)
            if m:
                if m.group(2):
                    c.output_delay[m.group(2)] = float(m.group(1))
                else:
                    c.default_output_delay = float(m.group(1))
                continue
            m = re.match(r"set_clock_skew\s+([-\d.]+)\s+-regs\s+(\S+)", line)
            if m:
                c.skew[m.group(2)] = float(m.group(1))
                continue
            m = re.match(r"set_false_path\s+-from\s+(\S+)\s+-to\s+(\S+)", line)
            if m:
                c.false_paths.append((m.group(1), m.group(2)))
                continue
            m = re.match(r"set_multicycle_path\s+(\d+)\s+-from\s+(\S+)\s+-to\s+(\S+)", line)
            if m:
                c.multicycle.append((m.group(2), m.group(3), int(m.group(1))))
                continue
            m = re.match(r"set_max_fanout\s+([\d.]+)", line)
            if m:
                c.max_fanout = float(m.group(1))
                continue
    return c


# ===========================================================================
#  The timing graph
# ===========================================================================
def short(name):
    """Yosys auto-generates long unique names. Shorten them for the report
    without losing the identity: $abc$95$...parse_blif$97/Y  ->  u97/Y and
    $auto$ff.cc:266:slice$89/Q -> ff89/Q. The mapping is one-to-one."""
    m = re.match(r"\$abc\$\d+\$.*?\$(\d+)(/.*)?$", name)
    if m:
        return "u%s%s" % (m.group(1), m.group(2) or "")
    m = re.match(r"\$auto\$ff\.cc:\d+:\w+\$(\d+)(/.*)?$", name)
    if m:
        return "ff%s%s" % (m.group(1), m.group(2) or "")
    m = re.match(r"\$auto\$\w+\.cc:\d+:\w+\$(\d+)(/.*)?$", name)
    if m:
        return "n%s%s" % (m.group(1), m.group(2) or "")
    return name


class Node(object):
    """One pin in the design: a port, or one pin of one cell."""
    __slots__ = ("name", "kind", "cell", "cell_type", "fanin", "fanout",
                 "at_max", "at_min", "rat_max", "rat_min", "src_max", "src_min")

    def __init__(self, name, kind, cell=None, cell_type=None):
        self.name = name
        self.kind = kind          # in_port | out_port | cell_in | cell_out | ff_q | ff_d
        self.cell = cell
        self.cell_type = cell_type
        self.fanin = []           # list of (node, delay)
        self.fanout = []
        self.at_max = None
        self.at_min = None
        self.rat_max = None
        self.rat_min = None
        self.src_max = None
        self.src_min = None


class Design(object):
    def __init__(self, jsonfile, top, libfile=DEFAULT_LIB):
        self.lib = read_liberty(libfile)
        with open(jsonfile) as f:
            js = json.load(f)
        if top not in js["modules"]:
            raise SystemExit("module '%s' not in %s (have: %s)"
                             % (top, jsonfile, ", ".join(js["modules"])))
        self.m = js["modules"][top]
        self.top = top
        self.nodes = {}
        self.net_driver = {}      # net bit -> driving node
        self.net_sinks = {}       # net bit -> [nodes]
        self.unmapped = set()
        self.bitname = {}         # net bit -> the RTL signal name, where there is one
        self.reg_label = {}       # cell instance -> a name a human can constrain
        for nn, info in self.m.get("netnames", {}).items():
            if nn.startswith("$"):
                continue
            bits = info.get("bits", [])
            for i, b in enumerate(bits):
                if isinstance(b, int):
                    self.bitname[b] = nn if len(bits) == 1 else "%s[%d]" % (nn, i)
        self._build()

    def label(self, cellname):
        """A register is best identified by the signal it drives - that is the
        name in the RTL, and therefore the name somebody can write in an SDC
        constraint. Fall back to the synthesised instance name."""
        return self.reg_label.get(cellname, cellname)

    # ------------------------------------------------------------------
    def _node(self, name, kind, cell=None, ctype=None):
        n = self.nodes.get(name)
        if n is None:
            n = Node(name, kind, cell, ctype)
            self.nodes[name] = n
        return n

    def _libcell(self, ytype):
        lname = CELLMAP.get(ytype)
        if lname is None or lname not in self.lib:
            self.unmapped.add(ytype)
            return None
        return self.lib[lname]

    def _build(self):
        # ---- ports ----
        self.in_ports, self.out_ports = [], []
        for pname, p in self.m["ports"].items():
            for i, bit in enumerate(p["bits"]):
                if not isinstance(bit, int):
                    continue
                nm = pname if len(p["bits"]) == 1 else "%s[%d]" % (pname, i)
                if p["direction"] == "input":
                    n = self._node(nm, "in_port")
                    self.net_driver[bit] = n
                    self.in_ports.append((pname, nm, bit))
                else:
                    n = self._node(nm, "out_port")
                    self.net_sinks.setdefault(bit, []).append(n)
                    self.out_ports.append((pname, nm, bit))

        # ---- cells ----
        self.ffs = []
        self.comb_cells = []
        for cname, c in self.m["cells"].items():
            lc = self._libcell(c["type"])
            if lc is None:
                continue
            if lc.is_ff:
                self.ffs.append((cname, c, lc))
            else:
                self.comb_cells.append((cname, c, lc))

            for pin, dirn in c["port_directions"].items():
                conn = c["connections"].get(pin, [])
                for bit in conn:
                    if not isinstance(bit, int):
                        continue
                    if lc.is_ff and pin in ("C", "R"):
                        continue          # clock and async reset are not data
                    nm = "%s/%s" % (cname, pin)
                    if dirn == "output":
                        kind = "ff_q" if lc.is_ff else "cell_out"
                        n = self._node(nm, kind, cname, lc.name)
                        self.net_driver[bit] = n
                    else:
                        kind = "ff_d" if lc.is_ff else "cell_in"
                        n = self._node(nm, kind, cname, lc.name)
                        self.net_sinks.setdefault(bit, []).append(n)

        # ---- load on each driver, then arcs ----
        self.load = {}
        for bit, sinks in self.net_sinks.items():
            tot = 0.0
            for s in sinks:
                if s.kind in ("cell_in", "ff_d"):
                    tot += self.lib[s.cell_type].input_cap
                else:
                    tot += 1.0          # a module output pin: one unit load
            self.load[bit] = tot
        self.fanout_count = {b: len(s) for b, s in self.net_sinks.items()}

        # NET arcs: a net costs nothing itself. Its LOAD is charged to whatever
        # drives it, which is where a real report puts it too.
        for bit, drv in self.net_driver.items():
            for s in self.net_sinks.get(bit, []):
                s.fanin.append((drv, 0.0))
                drv.fanout.append((s, 0.0))

        # CELL arcs: inside a combinational cell every input pin reaches the
        # output pin, and THAT is where the cell's delay is charged -
        # intrinsic plus the load the output net presents.
        self.cell_delay = {}
        for cname, c, lc in self.comb_cells:
            outs = [p for p, d in c["port_directions"].items() if d == "output"]
            ins = [p for p, d in c["port_directions"].items() if d == "input"]
            for op in outs:
                on = self.nodes.get("%s/%s" % (cname, op))
                if on is None:
                    continue
                obits = [b for b in c["connections"].get(op, []) if isinstance(b, int)]
                oload = sum(self.load.get(b, 0.0) for b in obits)
                d = lc.intrinsic + lc.load_factor * oload
                self.cell_delay[on.name] = d
                for ip in ins:
                    inn = self.nodes.get("%s/%s" % (cname, ip))
                    if inn is None:
                        continue
                    inn.fanout.append((on, d))
                    on.fanin.append((inn, d))

        # A flip-flop's clock-to-Q is charged AT the Q pin, because Q is a
        # startpoint: the path begins there, at that time after the edge.
        self.ffq_delay = {}
        for cname, c, lc in self.ffs:
            for pin, dirn in c["port_directions"].items():
                if dirn == "output":
                    for b in c["connections"].get(pin, []):
                        if isinstance(b, int) and b in self.bitname:
                            self.reg_label[cname] = self.bitname[b] + "_reg"
                            break
        for cname, c, lc in self.ffs:
            for pin, dirn in c["port_directions"].items():
                if dirn != "output":
                    continue
                qn = self.nodes.get("%s/%s" % (cname, pin))
                if qn is None:
                    continue
                qbits = [b for b in c["connections"].get(pin, []) if isinstance(b, int)]
                qload = sum(self.load.get(b, 0.0) for b in qbits)
                self.ffq_delay[qn.name] = lc.clk_to_q + lc.load_factor * qload


# ===========================================================================
#  The analysis
# ===========================================================================
class Timer(object):
    def __init__(self, design, cons):
        self.d = design
        self.c = cons

    # -- topological order over the combinational graph -----------------
    def _order(self):
        indeg = {n: 0 for n in self.d.nodes.values()}
        for n in self.d.nodes.values():
            for (m, _) in n.fanout:
                indeg[m] += 1
        q = [n for n in self.d.nodes.values() if indeg[n] == 0]
        out = []
        while q:
            n = q.pop()
            out.append(n)
            for (m, _) in n.fanout:
                indeg[m] -= 1
                if indeg[m] == 0:
                    q.append(m)
        if len(out) != len(self.d.nodes):
            raise SystemExit("combinational loop detected - STA cannot proceed")
        return out

    # -- forward: arrival times -----------------------------------------
    def propagate(self):
        c = self.c
        for n in self.d.nodes.values():
            n.at_max = n.at_min = None
            n.src_max = n.src_min = None

        # startpoints
        for pname, nm, bit in self.d.in_ports:
            if pname == c.clock_name:
                continue
            n = self.d.nodes[nm]
            dly = c.input_delay.get(pname, c.default_input_delay)
            n.at_max = n.at_min = (0.0 if dly is None else dly)

        for cname, cell, lc in self.d.ffs:
            for pin, dirn in cell["port_directions"].items():
                if dirn == "output":
                    n = self.d.nodes.get("%s/%s" % (cname, pin))
                    if n is not None:
                        # clock edge arrives, then clock-to-Q elapses
                        n.at_max = n.at_min = (c.clock_arrival(self.d.label(cname))
                                               + self.d.ffq_delay.get(n.name, 0.0))

        for n in self._order():
            if n.at_max is not None:
                continue
            if not n.fanin:
                continue
            best_max = best_min = None
            for (p, dly) in n.fanin:
                if p.at_max is None:
                    continue
                a = p.at_max + dly
                if best_max is None or a > best_max:
                    best_max, n.src_max = a, p
                b = p.at_min + dly
                if best_min is None or b < best_min:
                    best_min, n.src_min = b, p
            n.at_max, n.at_min = best_max, best_min

    # -- endpoints -------------------------------------------------------
    def endpoints(self):
        eps = []
        for cname, cell, lc in self.d.ffs:
            for pin, dirn in cell["port_directions"].items():
                if dirn == "input" and pin not in ("C", "R"):
                    n = self.d.nodes.get("%s/%s" % (cname, pin))
                    if n is not None and n.at_max is not None:
                        eps.append((n, cname, lc))
        for pname, nm, bit in self.d.out_ports:
            n = self.d.nodes.get(nm)
            if n is not None and n.at_max is not None:
                eps.append((n, None, None))
        return eps

    # -- setup / hold slack ---------------------------------------------
    def setup_slack(self, node, cname, lc):
        c = self.c
        if self.launch_unconstrained(node):
            return None, None, None
        launch = self._launch_name(node)
        if cname is None:                       # to an output port
            pname = node.name.split("[")[0]
            od = c.output_delay.get(pname, c.default_output_delay)
            if od is None:
                return None, None, None
            req = c.period - od - c.uncertainty_setup
            return req - node.at_max, req, node.at_max
        lbl = self.d.label(cname)
        if launch and c.is_false(launch, lbl):
            return None, None, None
        n_cyc = c.cycles(launch or "", lbl)
        capture = n_cyc * c.period + c.clock_arrival(lbl)
        req = capture - lc.setup - c.uncertainty_setup
        return req - node.at_max, req, node.at_max

    def hold_slack(self, node, cname, lc):
        c = self.c
        if cname is None:
            return None, None, None
        if self.launch_unconstrained(node, use_min=True):
            return None, None, None
        launch = self._launch_name(node, use_min=True)
        lbl = self.d.label(cname)
        if launch and c.is_false(launch, lbl):
            return None, None, None
        capture = c.clock_arrival(lbl)          # same edge
        req = capture + lc.hold + c.uncertainty_hold
        return node.at_min - req, req, node.at_min

    def launch_unconstrained(self, node, use_min=False):
        """A path that starts at an input port with no set_input_delay is
        UNCONSTRAINED: the tool has not been told when the data arrives, so it
        cannot judge the path. Real tools report these separately, and an
        unconstrained path is not a passing path - it is an unchecked one."""
        n, guard = node, 0
        while n is not None and guard < 100000:
            if n.kind == "ff_q":
                return False
            if n.kind == "in_port":
                pname = n.name.split("[")[0]
                if pname == self.c.clock_name:
                    return True
                return (pname not in self.c.input_delay
                        and self.c.default_input_delay is None)
            n = n.src_min if use_min else n.src_max
            guard += 1
        return False

    def _launch_name(self, node, use_min=False):
        n, guard = node, 0
        while n is not None and guard < 100000:
            if n.kind == "ff_q":
                return self.d.label(n.cell)
            if n.kind == "in_port":
                return n.name
            n = n.src_min if use_min else n.src_max
            guard += 1
        return None

    # -- path trace -------------------------------------------------------
    def trace(self, node, use_min=False):
        path, n, guard = [], node, 0
        while n is not None and guard < 100000:
            path.append(n)
            n = n.src_min if use_min else n.src_max
            guard += 1
        return list(reversed(path))


# ===========================================================================
#  Reporting
# ===========================================================================
def fmt_path(timer, ep, use_min=False):
    path = timer.trace(ep, use_min)
    out = []
    prev_t = 0.0
    first = path[0] if path else None
    if first is not None and first.kind == "ff_q":
        lbl = timer.d.label(first.cell)
        skew = timer.c.clock_arrival(lbl)
        out.append("    %9.3f %9.3f   %s" % (skew, skew, "clock edge at " + short(lbl)))
        prev_t = skew
    for i, n in enumerate(path):
        t = n.at_min if use_min else n.at_max
        inc = t - prev_t
        nm = short(n.name)
        if n.kind in ("ff_q", "ff_d") and n.cell in timer.d.reg_label:
            nm = "%s/%s" % (timer.d.reg_label[n.cell], n.name.rsplit("/", 1)[-1])
        label = nm
        if n.cell_type:
            label = "%-26s (%s)" % (nm, n.cell_type)
        out.append("    %9.3f %9.3f   %s" % (inc, t, label))
        prev_t = t
    return out


def report(design, cons, args):
    t = Timer(design, cons)
    t.propagate()
    eps = t.endpoints()

    if design.unmapped:
        print("  WARNING: cell types with no library entry, ignored: %s"
              % ", ".join(sorted(design.unmapped)))

    kind = "HOLD" if args.hold else "SETUP"
    rows = []
    unconstrained = 0
    for (n, cname, lc) in eps:
        if args.hold and cname is None:
            continue          # hold is not checked at output ports here
        if args.hold:
            s, req, arr = t.hold_slack(n, cname, lc)
        else:
            s, req, arr = t.setup_slack(n, cname, lc)
        if s is None:
            unconstrained += 1
            continue
        rows.append((s, n, cname, lc, req, arr))
    rows.sort(key=lambda r: r[0])

    if args.csv:
        print("endpoint,slack,arrival,required")
        for s, n, cname, lc, req, arr in rows:
            en = ("%s/%s" % (design.reg_label[n.cell], n.name.rsplit("/", 1)[-1])
                  if n.cell in design.reg_label else short(n.name))
            print("%s,%.4f,%.4f,%.4f" % (en, s, arr, req))
        return 0

    print()
    print("  " + "=" * 74)
    print("  %s TIMING REPORT   design=%s   clock %s period=%.3f ns (%.1f MHz)"
          % (kind, design.top, cons.clock_name, cons.period, 1000.0 / cons.period))
    print("  " + "=" * 74)

    if not rows:
        print("  no %s-checked endpoints (did you set input/output delay?)" % kind.lower())
        return 0

    wns = rows[0][0]
    viol = [r for r in rows if r[0] < 0]
    tns = sum(r[0] for r in viol)

    for i, (s, n, cname, lc, req, arr) in enumerate(rows[:args.paths]):
        print()
        epn = ("%s/%s" % (design.reg_label[n.cell], n.name.rsplit("/", 1)[-1])
               if n.cell in design.reg_label else short(n.name))
        print("  Path %d   endpoint %s%s" % (i + 1, epn,
                                             "" if cname is None else "  (%s)" % lc.name))
        launch = t._launch_name(n, use_min=args.hold)
        print("           startpoint %s" % (short(launch) if launch else "?"))
        print("    %9s %9s   %s" % ("incr", "arrival", "pin"))
        for ln in fmt_path(t, n, args.hold):
            print(ln)
        if args.hold:
            print("    %9s %9.3f   required (clock + hold%s)"
                  % ("", req, " + uncertainty" if cons.uncertainty_hold else ""))
        else:
            print("    %9s %9.3f   required (period - setup%s)"
                  % ("", req, " - uncertainty" if cons.uncertainty_setup else ""))
        print("    %9s %9.3f   SLACK   %s" % ("", s, "MET" if s >= 0 else "*** VIOLATED ***"))

    print()
    print("  " + "-" * 74)
    print("  endpoints analysed : %d" % len(rows))
    if unconstrained:
        print("  UNCONSTRAINED      : %d endpoint(s) not checked - no input/output"
              % unconstrained)
        print("                       delay was set for them. Unchecked is not passed."
              )
    print("  WNS (worst slack)  : %+.3f ns   %s" % (wns, "MET" if wns >= 0 else "VIOLATED"))
    print("  TNS (total neg)    : %+.3f ns over %d failing endpoint(s)" % (tns, len(viol)))
    if not args.hold:
        crit = cons.period - wns
        print("  longest path       : %.3f ns" % crit)
        if crit > 0:
            print("  Fmax               : %.1f MHz" % (1000.0 / crit))
    print("  " + "-" * 74)

    if cons.max_fanout:
        bad = [(b, f) for b, f in design.fanout_count.items() if f > cons.max_fanout]
        if bad:
            print("  set_max_fanout %d violated on %d net(s)"
                  % (cons.max_fanout, len(bad)))
    return 0 if wns >= 0 else 1


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="a small static timing analyser")
    ap.add_argument("json")
    ap.add_argument("top")
    ap.add_argument("-c", "--sdc", default=None)
    ap.add_argument("-p", "--period", type=float, default=None)
    ap.add_argument("-l", "--lib", default=DEFAULT_LIB)
    ap.add_argument("--paths", type=int, default=1)
    ap.add_argument("--hold", action="store_true")
    ap.add_argument("--csv", action="store_true")
    args = ap.parse_args(argv)

    cons = read_sdc(args.sdc)
    if args.period is not None:
        cons.period = args.period
    d = Design(args.json, args.top, args.lib)
    return report(d, cons, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
