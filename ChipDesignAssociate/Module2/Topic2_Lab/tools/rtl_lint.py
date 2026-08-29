#!/usr/bin/env python3
"""rtl_lint.py - check Verilog against the RTL coding rules this topic teaches.

WHY A LINT TOOL BELONGS IN A METHODOLOGY TOPIC
----------------------------------------------
"Methodology" degenerates into a list of good intentions unless something
checks it. Every rule below is one that a reviewer would otherwise have to
remember, on every file, for ever - which is exactly the kind of job people
are bad at and programs are good at.

Every real RTL team runs a linter before simulation, because a lint error
costs seconds and the bug it prevents can cost a silicon revision.

THE RULES
---------
L001  blocking assignment (=) inside a clocked always block
      Two clocked blocks that use = can see each other's half-updated values,
      and whether they do depends on the order the simulator happens to run
      them in. Use <= in clocked blocks.

L002  non-blocking assignment (<=) inside a combinational always block
      Legal, but it makes the block behave like a register in simulation while
      synthesis builds combinational logic - another simulate/synthesise
      mismatch. Use = in combinational blocks.

L003  mixed = and <= in the same always block
      Whatever the intent, no reader can tell what it was.

L004  explicit sensitivity list on a combinational block
      always @(a or b) is a promise you have to keep by hand, for ever, every
      time you edit the block. always @* keeps it for you. This is the rule
      that s04_incomplete_sens.v breaks, and the demonstration of what it
      costs is in subset/tb_mismatch.v.

L005  if without else in a combinational block
      Whatever the output is when the condition is false, you did not say -
      so the tool must remember the old value, which means a LATCH.

L006  case without default in a combinational block
      The same problem, wearing a different hat.

L007  a signal assigned in more than one always block
      Two drivers. In simulation the last one to run wins; in synthesis it is
      an error or a short.

WHAT THIS TOOL IS NOT
---------------------
It is a few hundred lines of regular expressions, not a Verilog parser. It
reads code the way a careful reviewer skims it, and it can be fooled by
unusual formatting. That is why rules L005 and L006 are cross-checked against
Yosys: the linter's opinion about latches is confirmed by the synthesiser
actually inferring one. Where a real team is concerned, use Verilator --lint-only
or a commercial linter; the point of this one is that you can read all of it.
"""
import re
import sys


class Issue:
    __slots__ = ("rule", "line", "text", "detail")

    def __init__(self, rule, line, text, detail):
        self.rule, self.line, self.text, self.detail = rule, line, text, detail


RULES = {
    "L001": "blocking (=) in a clocked block - use <=",
    "L002": "non-blocking (<=) in a combinational block - use =",
    "L003": "= and <= mixed in one always block",
    "L004": "explicit sensitivity list - use always @*",
    "L005": "if with no else in a combinational block - infers a latch",
    "L006": "case with no default in a combinational block - infers a latch",
    "L007": "signal driven from more than one always block",
}


def strip_comments(src):
    """Remove // and /* */ comments, preserving line count."""
    src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"),
                 src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    return src


def find_blocks(src):
    """Yield (start_line, header, body, is_clocked) for each always block.

    The body is taken by matching begin/end depth, or a single statement when
    the block has no begin.
    """
    out = []
    for m in re.finditer(r"\balways\b\s*(@\s*\(([^)]*)\)|@\s*\*|\*)?", src):
        head = m.group(0)
        sens = (m.group(2) or "").strip()
        star = ("@*" in head.replace(" ", "")) or (m.group(2) is None)
        clocked = bool(re.search(r"\b(posedge|negedge)\b", sens))
        line = src.count("\n", 0, m.start()) + 1

        rest = src[m.end():]
        bm = re.match(r"\s*begin\b", rest)
        if bm:
            depth, i = 0, bm.end()
            # walk tokens counting begin/end
            for tm in re.finditer(r"\b(begin|case|casex|casez|end|endcase)\b",
                                  rest[bm.start():]):
                tok = tm.group(1)
                if tok in ("begin", "case", "casex", "casez"):
                    depth += 1
                else:
                    depth -= 1
                    if depth == 0:
                        i = bm.start() + tm.end()
                        break
            body = rest[bm.end():i]
        else:
            semi = rest.find(";")
            body = rest[:semi + 1] if semi >= 0 else rest[:200]
        out.append((line, sens, star, clocked, body))
    return out


def lint(path):
    raw = open(path, errors="replace").read()
    src = strip_comments(raw)
    lines = raw.split("\n")
    issues = []

    def add(rule, line, detail=""):
        text = lines[line - 1].strip() if 0 < line <= len(lines) else ""
        issues.append(Issue(rule, line, text[:70], detail))

    assigned_in = {}          # signal -> set of always-block start lines

    for line, sens, star, clocked, body in find_blocks(src):
        # The character class already excludes <= >= != == , so these two
        # counts are disjoint and neither needs correcting for the other.
        bl = len(re.findall(r"[^<>=!]=(?!=)", body))
        nb = len(re.findall(r"<=(?!=)", body))

        if clocked and bl > 0:
            add("L001", line, "%d blocking assignment(s)" % bl)
        if not clocked and nb > 0:
            add("L002", line, "%d non-blocking assignment(s)" % nb)
        if bl > 0 and nb > 0:
            add("L003", line)
        if not clocked and not star and sens:
            add("L004", line, "list is (%s)" % sens)

        if not clocked:
            for im in re.finditer(r"\bif\b", body):
                tail = body[im.end():]
                # an else belonging to this if, before the block closes
                if not re.search(r"\belse\b", tail):
                    add("L005", line + body[:im.start()].count("\n"))
                    break
            if re.search(r"\bcase[xz]?\b", body) and not re.search(r"\bdefault\b", body):
                cm = re.search(r"\bcase[xz]?\b", body)
                add("L006", line + body[:cm.start()].count("\n"))

        for am in re.finditer(r"(\w+)\s*(?:\[[^\]]*\])?\s*<?=(?!=)", body):
            assigned_in.setdefault(am.group(1), set()).add(line)

    for sig, blocks in sorted(assigned_in.items()):
        if len(blocks) > 1:
            add("L007", min(blocks), "%s driven from lines %s"
                % (sig, ", ".join(str(b) for b in sorted(blocks))))

    return sorted(issues, key=lambda i: (i.line, i.rule))


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 0

    total = 0
    for path in argv[1:]:
        issues = lint(path)
        total += len(issues)
        print()
        print("  %s" % path)
        if not issues:
            print("    clean - no rule violations")
            continue
        for i in issues:
            print("    line %-4d %s  %s" % (i.line, i.rule, RULES[i.rule]))
            if i.detail:
                print("              %s" % i.detail)
            if i.text:
                print("              > %s" % i.text)
    print()
    print("  %d issue(s) across %d file(s)" % (total, len(argv) - 1))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
