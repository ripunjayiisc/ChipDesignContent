# -*- coding: utf-8 -*-
"""Render Course_Outline.md as a formatted document in the house style.

The Markdown file is the source of truth; this only typesets it. Re-run after
editing Course_Outline.md.
"""
import os
import re
import _boot
from wbkit import *
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "Course_Outline.md")
OUT = os.path.join(HERE, "..", "PCB_Design_with_KiCad_Course_Outline.docx")

BOLD = re.compile(r"\*\*(.+?)\*\*")
ITAL = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
CODE = re.compile(r"`([^`]+?)`")


def runs(text):
    """Turn a line of inline Markdown into wbkit run tuples."""
    out = []
    pos = 0
    pattern = re.compile(r"\*\*(.+?)\*\*|(?<!\*)\*([^*]+?)\*(?!\*)|`([^`]+?)`")
    for m in pattern.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], {}))
        if m.group(1) is not None:
            out.append((m.group(1), {"b": True, "c": NAVY}))
        elif m.group(2) is not None:
            out.append((m.group(2), {"i": True}))
        else:
            out.append((m.group(3), {"f": MONOF, "s": 10}))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], {}))
    return out or [(text, {})]


def fix_widths(t, widths):
    """Make Word honour the column widths.

    python-docx writes a width onto every cell, but Word and LibreOffice both
    ignore those while the table is set to autofit - they re-flow the columns
    to the content instead, which squeezes a prose column next to a column of
    two-digit numbers. Turning the layout to fixed is what makes the widths
    stick.
    """
    t.autofit = False
    tblPr = t._tbl.tblPr
    for tag in ("w:tblLayout",):
        for el in tblPr.findall(qn(tag)):
            tblPr.remove(el)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    grid = t._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for col, wd in zip(grid.findall(qn("w:gridCol")), widths):
            col.set(qn("w:w"), str(int(wd * 1440)))
    for row in t.rows:
        for cell, wd in zip(row.cells, widths):
            cell.width = Inches(wd)
    return t


def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def main():
    w = Workbook("PCB Design with KiCad  ·  Short-Term Course Outline  ·  "
                 "draft v0.1  ·  NIELIT")
    lines = open(SRC, encoding="utf-8").read().splitlines()

    i = 0
    # ---------------------------------------------------------------- cover
    w.para("", space_after=70)
    w.para([("Short-Term Course", {"s": 15, "c": TEAL, "b": True,
                                   "f": HEADF})],
           align=AL.CENTER, space_after=4)
    w.para([("PCB Design with KiCad", {"s": 30, "c": NAVY, "b": True,
                                       "f": HEADF})],
           align=AL.CENTER, space_after=10)
    w.para([("Course Outline — draft for review, v0.1", {"s": 14, "c": AMBER,
                                                         "b": True,
                                                         "f": HEADF})],
           align=AL.CENTER, space_after=26)
    w.para([("60 hours  ·  20 theory + 40 practical  ·  KiCad 10.0.6",
             {"s": 12, "c": SLATE})], align=AL.CENTER, space_after=40)
    w.callout("What the learner leaves with", [
        "A fabricated, assembled, working board of their own design — "
        "schematic, layout, manufacturing package and all.",
    ], color=GREEN, bar="2A9D5C", fill="EEF7F1")
    w.page_break()

    skip_title = True
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if not s or s == "---":
            i += 1
            continue

        # tables -----------------------------------------------------------
        if s.startswith("|") and i + 1 < len(lines) and \
                set(lines[i + 1].strip().replace("|", "").replace(" ", "")) <= set("-:"):
            head = split_row(s)
            i += 2
            body = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                body.append([c for c in split_row(lines[i])])
                i += 1
            # a two-column table with an empty header is a parameter list
            if all(h == "" for h in head):
                for row in body:
                    w.para([(row[0].replace("**", ""), {"b": True,
                                                        "c": NAVY}),
                            ("   ", {}),
                            (row[1].replace("**", ""), {})],
                           indent=0.12, space_after=4)
            else:
                ncol = len(head)
                body = [r[:ncol] + [""] * (ncol - len(r)) for r in body]
                avail = 6.8
                # size each column from the longest thing in it, with a floor,
                # so narrow numeric columns stop stealing room from prose ones
                span = []
                for j in range(ncol):
                    longest = max([len(head[j])] +
                                  [len(r[j]) for r in body]) if body else len(head[j])
                    span.append(max(4, min(longest, 60)))
                tot = float(sum(span))
                wid = [max(0.45, avail * c / tot) for c in span]
                scale = avail / sum(wid)
                wid = [x * scale for x in wid]
                t = w.table([h.replace("**", "") for h in head],
                            [[c.replace("**", "") for c in r] for r in body],
                            widths=wid, size=9.5, align_center=(ncol > 2))
                fix_widths(t, wid)
            continue

        # headings ---------------------------------------------------------
        if s.startswith("#### "):
            w.h4(s[5:]); i += 1; continue
        if s.startswith("### "):
            w.h3(s[4:].replace("**", "")); i += 1; continue
        if s.startswith("## "):
            w.h2(s[3:]); i += 1; continue
        if s.startswith("# "):
            if skip_title:
                skip_title = False
                i += 1
                continue
            w.h1(s[2:]); i += 1; continue

        # bullets ----------------------------------------------------------
        if s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(runs(lines[i].strip()[2:]))
                i += 1
            w.bullets(items, size=10.5)
            continue

        # numbered ---------------------------------------------------------
        m = re.match(r"^(\d+)\. (.*)$", s)
        if m:
            items = []
            start = int(m.group(1))
            while i < len(lines):
                mm = re.match(r"^(\d+)\. (.*)$", lines[i].strip())
                if not mm:
                    break
                items.append(runs(mm.group(2)))
                i += 1
            w.numbered(items, size=10.5, start=start)
            continue

        # a bold-led paragraph that reads as a callout -----------------------
        if s.startswith("**") and s.endswith("**") and len(s) < 90:
            w.para(runs(s), space_after=3)
            i += 1
            continue

        # ordinary paragraph -------------------------------------------------
        buf = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and \
                not lines[i].strip().startswith(("#", "-", "|", "---")) and \
                not re.match(r"^\d+\. ", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        w.para(runs(" ".join(buf)), size=10.5)

    w.save(OUT)


if __name__ == "__main__":
    main()
