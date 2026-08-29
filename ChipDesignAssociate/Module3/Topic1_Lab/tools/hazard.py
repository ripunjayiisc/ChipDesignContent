#!/usr/bin/env python3
"""hazard.py - find static logic hazards in a two-level circuit, and say how
to remove them.

WHAT A HAZARD IS
----------------
A combinational output is supposed to settle to the value its truth table
says. On the way there it may glitch: a momentary pulse to the wrong value,
caused by two paths through the circuit having different delays and
reconverging.

A STATIC-1 hazard: the output should stay at 1 across an input change, but
dips to 0 on the way.
A STATIC-0 hazard: the output should stay at 0, but spikes to 1.
A DYNAMIC hazard: the output should change once, but changes three or more
times. It needs three or more reconverging paths, so it cannot happen in a
two-level circuit - this tool does not look for it (hz_dynamic.v does).

THE RULE THIS TOOL IMPLEMENTS
-----------------------------
Take a two-level AND-OR (sum-of-products) circuit. Consider two input
vectors that differ in exactly ONE variable and give F = 1 for both. As that
variable changes, SOME product term must hold the output up throughout. If
one single product term covers BOTH vectors, it stays 1 the whole time and
the output cannot dip. If no single term covers both, then the term that was
holding the output up must switch off while the term that takes over is
still switching on - and whether the output dips depends entirely on the
relative delays. That is a static-1 logic hazard.

The fix is to add the product term made of the literals the two vectors
agree on. It is logically redundant - it changes nothing in the truth table -
which is exactly why a logic minimiser removes it and why you have to ask
for it deliberately.

The dual holds for a two-level OR-AND (product-of-sums) circuit: it can have
static-0 hazards, found by the same argument on the 0-cells.

WHAT THIS DOES NOT COVER
------------------------
A FUNCTION hazard occurs when two or more inputs change at once and the
function itself demands a glitch. No implementation can remove it, so no
tool can offer you a fix; the only remedy is to not change those inputs
simultaneously. This tool only considers single-variable changes, which is
precisely the case where a fix exists.

USAGE
    python3 tools/hazard.py "A B' + B C"            # SOP, static-1
    python3 tools/hazard.py --pos "(A + B)(B' + C)" # POS, static-0
    python3 tools/hazard.py --selftest
"""
import itertools
import re
import sys


# --------------------------------------------------------------- parsing
def parse_terms(text):
    """'A B' + B C'  ->  [{'A':1,'B':0}, {'B':1,'C':1}], ['A','B','C']

    A literal is a capital letter optionally followed by ' or ! for negation.
    Terms are separated by +; literals within a term by spaces, * or nothing.
    For POS input the same parser is used on the text between brackets, with
    + as the within-clause separator - see parse_pos.
    """
    terms = []
    for chunk in text.split("+"):
        chunk = chunk.strip()
        if not chunk:
            continue
        lits = re.findall(r"([A-Z])\s*([!'~]?)", chunk)
        if not lits:
            raise ValueError("no literals in term %r" % chunk)
        cube = {}
        for var, neg in lits:
            val = 0 if neg else 1
            if var in cube and cube[var] != val:
                raise ValueError("term %r contains %s and %s' - always 0"
                                 % (chunk, var, var))
            cube[var] = val
        terms.append(cube)
    return terms


def parse_pos(text):
    """'(A + B)(B' + C)'  ->  [[{'A':1},{'B':1}], [{'B':0},{'C':1}]]

    Each clause becomes a list of literals; a clause is 0 only when every
    literal in it is 0.
    """
    groups = re.findall(r"\(([^)]*)\)", text)
    if not groups:
        groups = [text]
    clauses = []
    for g in groups:
        lits = []
        for chunk in g.split("+"):
            m = re.findall(r"([A-Z])\s*([!'~]?)", chunk)
            if not m:
                continue
            var, neg = m[0]
            lits.append({var: 0 if neg else 1})
        if lits:
            clauses.append(lits)
    return clauses


def variables(terms):
    v = set()
    for t in terms:
        v |= set(t)
    return sorted(v)


def covers(cube, vector, order):
    """Does this product term evaluate to 1 on this input vector?"""
    return all(vector[order.index(var)] == val for var, val in cube.items())


def eval_sop(terms, vector, order):
    return 1 if any(covers(t, vector, order) for t in terms) else 0


def eval_pos(clauses, vector, order):
    for cl in clauses:
        if not any(vector[order.index(v)] == val
                   for lit in cl for v, val in lit.items()):
            return 0
    return 1


def fmt_cube(cube, order):
    if not cube:
        return "1"
    return " ".join(v + ("" if cube[v] else "'") for v in order if v in cube)


def fmt_vec(vector, order):
    return " ".join("%s=%d" % (v, b) for v, b in zip(order, vector))


# ----------------------------------------------------------- the analysis
def static1_hazards(terms, order):
    """Every single-variable transition between two 1-cells that no single
    product term spans. Returns a list of dicts."""
    n = len(order)
    found = []
    for vec in itertools.product((0, 1), repeat=n):
        if eval_sop(terms, vec, order) != 1:
            continue
        for i in range(n):
            other = list(vec)
            other[i] ^= 1
            other = tuple(other)
            if other < vec:                       # report each pair once
                continue
            if eval_sop(terms, other, order) != 1:
                continue
            spanning = [t for t in terms
                        if covers(t, vec, order) and covers(t, other, order)]
            if spanning:
                continue
            need = {v: b for j, (v, b) in enumerate(zip(order, vec)) if j != i}
            found.append({
                "var": order[i],
                "from": vec,
                "to": other,
                "holds_before": [t for t in terms if covers(t, vec, order)],
                "holds_after": [t for t in terms if covers(t, other, order)],
                "fix": need,
            })
    return found


def static0_hazards(clauses, order):
    """The dual, for a two-level OR-AND circuit: two 0-cells one variable
    apart with no single sum term covering both."""
    n = len(order)
    found = []

    def zeroes(cl, vec):
        return not any(vec[order.index(v)] == val
                       for lit in cl for v, val in lit.items())

    for vec in itertools.product((0, 1), repeat=n):
        if eval_pos(clauses, vec, order) != 0:
            continue
        for i in range(n):
            other = list(vec)
            other[i] ^= 1
            other = tuple(other)
            if other < vec:
                continue
            if eval_pos(clauses, other, order) != 0:
                continue
            spanning = [cl for cl in clauses
                        if zeroes(cl, vec) and zeroes(cl, other)]
            if spanning:
                continue
            need = [{v: b} for j, (v, b) in enumerate(zip(order, vec)) if j != i]
            found.append({
                "var": order[i],
                "from": vec,
                "to": other,
                "fix": need,
            })
    return found


def truth_table(terms, order, sop=True):
    rows = []
    for vec in itertools.product((0, 1), repeat=len(order)):
        f = eval_sop(terms, vec, order) if sop else eval_pos(terms, vec, order)
        rows.append((vec, f))
    return rows


# ------------------------------------------------------------- reporting
def report_sop(text, terms, order):
    print("=" * 74)
    print("STATIC-1 HAZARD ANALYSIS   (two-level AND-OR)")
    print("=" * 74)
    print("  F = %s" % text.strip())
    print("  variables: %s" % ", ".join(order))
    print("  product terms: %s" % ", ".join(fmt_cube(t, order) for t in terms))
    print()

    print("  truth table")
    print("      %s   F" % "  ".join(order))
    for vec, f in truth_table(terms, order):
        print("      %s   %d" % ("  ".join(str(b) for b in vec), f))
    print()

    hz = static1_hazards(terms, order)
    if not hz:
        print("  NO static-1 logic hazard.")
        print("  Every single-variable transition between two 1-cells is spanned")
        print("  by one product term, so some term holds the output up throughout.")
        return [], hz

    print("  %d static-1 logic hazard(s) found:" % len(hz))
    print()
    fixes = []
    for h in hz:
        print("    %s changes %d -> %d   with  %s"
              % (h["var"], h["from"][order.index(h["var"])],
                 h["to"][order.index(h["var"])],
                 ", ".join("%s=%d" % (v, b) for v, b in zip(order, h["from"])
                           if v != h["var"])))
        print("      before the change, the output is held up by : %s"
              % ", ".join(fmt_cube(t, order) for t in h["holds_before"]))
        print("      after  the change, the output is held up by : %s"
              % ", ".join(fmt_cube(t, order) for t in h["holds_after"]))
        print("      no single term covers both, so the handover is a race.")
        print("      ADD the redundant term:  %s" % fmt_cube(h["fix"], order))
        print()
        if h["fix"] not in fixes:
            fixes.append(h["fix"])

    print("  hazard-free cover:")
    print("      F = %s" % "  +  ".join(
        fmt_cube(t, order) for t in terms + fixes))
    print()

    # prove the fix, and prove it changed nothing
    patched = terms + fixes
    left = static1_hazards(patched, order)
    same = all(eval_sop(terms, v, order) == eval_sop(patched, v, order)
               for v in itertools.product((0, 1), repeat=len(order)))
    print("  checking the proposed cover:")
    print("    remaining static-1 hazards : %d" % len(left))
    print("    truth table unchanged      : %s" % ("yes" if same else "NO - BUG"))
    if left or not same:
        print("    *** the fix is not sound - do not use this output ***")
    return fixes, hz


def report_pos(text, clauses, order):
    print("=" * 74)
    print("STATIC-0 HAZARD ANALYSIS   (two-level OR-AND)")
    print("=" * 74)
    print("  F = %s" % text.strip())
    print("  variables: %s" % ", ".join(order))
    print()
    hz = static0_hazards(clauses, order)
    if not hz:
        print("  NO static-0 logic hazard.")
        return hz
    print("  %d static-0 logic hazard(s) found:" % len(hz))
    for h in hz:
        print("    %s changes %d -> %d   with  %s"
              % (h["var"], h["from"][order.index(h["var"])],
                 h["to"][order.index(h["var"])],
                 ", ".join("%s=%d" % (v, b) for v, b in zip(order, h["from"])
                           if v != h["var"])))
        print("      ADD the redundant sum term:  (%s)"
              % " + ".join(fmt_cube(l, order) for l in h["fix"]))
    return hz


# -------------------------------------------------- independent semantics
def timeline_dips(terms, order, vec_from, var, switch_at):
    """Play the transition forward in time and say whether the output dips.

    switch_at maps a term's index to the instant its AND gate changes. Terms
    that do not contain `var` do not change at all. Returns (start, dipped,
    finish) where start and finish are the steady output values.
    """
    i = order.index(var)
    vec_to = list(vec_from)
    vec_to[i] ^= 1
    vec_to = tuple(vec_to)

    state = []
    for k, t in enumerate(terms):
        before = 1 if covers(t, vec_from, order) else 0
        after = 1 if covers(t, vec_to, order) else 0
        state.append((None if var not in t else switch_at[k], before, after))

    def or_at(t):
        for sw, before, after in state:
            v = before if (sw is None or t is None or t < sw) else after
            if v:
                return 1
        return 0

    times = sorted({sw for sw, _, _ in state if sw is not None})
    seen = [or_at(None)] + [or_at(t) for t in times]
    return seen[0], seen, seen[-1]


def can_glitch(terms, order, vec_from, var, trials=60, seed=1):
    """Is there ANY assignment of gate delays that makes the output glitch on
    this transition?

    This is the honest question. A hazard is not "this circuit glitches"; it is
    "whether this circuit glitches is decided by delays you do not control".
    So the check searches over random per-term switching times rather than
    assuming one delay profile - a fixed profile only ever exposes the glitch
    in one direction, which is exactly the trap this function avoids.

    Written deliberately as a timing argument, with no reference to the
    covering rule in static1_hazards(), so that the two can be cross-checked.
    """
    import random as _r
    rng = _r.Random(seed)
    for _ in range(trials):
        switch_at = [rng.uniform(1.0, 10.0) for _ in terms]
        start, seen, finish = timeline_dips(terms, order, vec_from, var, switch_at)
        if start == 1 and finish == 1 and 0 in seen:
            return True
        if start == 0 and finish == 0 and 1 in seen:
            return True
    return False


# -------------------------------------------------------------- selftest
def selftest():
    import random
    ok = True

    def check(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print("  %-54s %s  (got %s, want %s)"
              % (label, "PASS" if good else "FAIL", got, want))

    print("hazard.py self-test")
    print("-" * 74)
    print("A. the textbook example")

    t = parse_terms("A B' + B C")
    o = variables(t)
    h = static1_hazards(t, o)
    check("A B' + B C has exactly one static-1 hazard", len(h), 1)
    if h:
        check("  ... on variable B", h[0]["var"], "B")
        check("  ... fixed by the term A C", fmt_cube(h[0]["fix"], o), "A C")
        check("  ... and some delay assignment really does glitch",
              can_glitch(t, o, h[0]["from"], h[0]["var"]), True)

    t2 = parse_terms("A B' + B C + A C")
    check("A B' + B C + A C is hazard-free", len(static1_hazards(t2, o)), 0)
    same = all(eval_sop(t, v, o) == eval_sop(t2, v, o)
               for v in itertools.product((0, 1), repeat=3))
    check("  ... and computes the same function", same, True)
    check("  ... and then no delay assignment can glitch it",
          can_glitch(t2, o, (1, 1, 1), "B"), False)

    print()
    print("B. un-minimised logic is not automatically safe")
    t3 = parse_terms("A B + A B'")
    o3 = variables(t3)
    h3 = static1_hazards(t3, o3)
    check("A B + A B' (which IS just F = A) has a hazard", len(h3), 1)
    if h3:
        check("  ... removed by adding the term A", fmt_cube(h3[0]["fix"], o3), "A")
    check("the single term A is hazard-free",
          len(static1_hazards(parse_terms("A"), ["A"])), 0)

    print()
    print("C. a single product term can never glitch")
    t5 = parse_terms("A B C")
    check("A B C is hazard-free", len(static1_hazards(t5, variables(t5))), 0)

    print()
    print("D. the combinatorial rule agrees with a delay simulation")
    print("   (random functions; the rule and the timeline must never differ)")
    random.seed(20260829)
    disagreements = 0
    checked = 0
    for trial in range(400):
        nv = random.choice((3, 4))
        order = ["A", "B", "C", "D"][:nv]
        nterms = random.randint(1, 5)
        terms = []
        for _ in range(nterms):
            size = random.randint(1, nv)
            vs = random.sample(order, size)
            terms.append({v: random.randint(0, 1) for v in vs})
        rule = {(hz["from"], hz["var"]) for hz in static1_hazards(terms, order)}
        for vec in itertools.product((0, 1), repeat=nv):
            for var in order:
                other = list(vec)
                other[order.index(var)] ^= 1
                other = tuple(other)
                if eval_sop(terms, vec, order) != 1:
                    continue
                if eval_sop(terms, other, order) != 1:
                    continue
                checked += 1
                by_rule = (vec, var) in rule or (other, var) in rule
                by_sim = can_glitch(terms, order, vec, var)
                if by_rule != by_sim:
                    disagreements += 1
    check("static-1 transitions cross-checked", checked > 2000, True)
    check("disagreements between rule and simulation", disagreements, 0)

    print()
    print("E. the suggested fix always works, and never changes the function")
    random.seed(7)
    bad_fix = 0
    changed = 0
    had_hazard = 0
    for trial in range(400):
        nv = random.choice((3, 4))
        order = ["A", "B", "C", "D"][:nv]
        terms = []
        for _ in range(random.randint(1, 5)):
            vs = random.sample(order, random.randint(1, nv))
            terms.append({v: random.randint(0, 1) for v in vs})
        hz = static1_hazards(terms, order)
        if not hz:
            continue
        had_hazard += 1
        fixes = []
        for x in hz:
            if x["fix"] not in fixes:
                fixes.append(x["fix"])
        patched = terms + fixes
        if static1_hazards(patched, order):
            bad_fix += 1
        if any(eval_sop(terms, v, order) != eval_sop(patched, v, order)
               for v in itertools.product((0, 1), repeat=nv)):
            changed += 1
    check("functions that had a hazard", had_hazard > 100, True)
    check("fixes that left a hazard behind", bad_fix, 0)
    check("fixes that altered the truth table", changed, 0)

    print()
    print("F. the product-of-sums dual")
    c = parse_pos("(A + B)(B' + C)")
    oc = sorted({v for cl in c for lit in cl for v in lit})
    check("(A+B)(B'+C) has one static-0 hazard", len(static0_hazards(c, oc)), 1)

    print("-" * 74)
    print("SELF-TEST %s" % ("PASSED" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[1] == "--selftest":
        return selftest()
    if argv[1] == "--pos":
        text = " ".join(argv[2:])
        clauses = parse_pos(text)
        order = sorted({v for cl in clauses for lit in cl for v in lit})
        report_pos(text, clauses, order)
        return 0
    text = " ".join(argv[1:])
    terms = parse_terms(text)
    report_sop(text, terms, variables(terms))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
