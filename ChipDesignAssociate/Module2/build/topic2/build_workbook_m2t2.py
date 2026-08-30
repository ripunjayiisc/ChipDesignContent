# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _boot
from wbkit import Workbook
import m2t2_wb1, m2t2_wb2, m2t2_wb2b, m2t2_wb3, m2t2_wb4

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "Module2_Topic2_Tutorial_Practice_Workbook.docx"))
w = Workbook("Module 2 · Topic 2 · RTL Design Methodology   ·   "
             "Chip Design Associate (O-Level ‘Chip Design’)   ·   NIE/ELE/N0102")
m2t2_wb1.build(w)          # front matter, and Part 1 - what RTL is
m2t2_wb2.build_hdl(w)      # Part 2 - the language you say it in
m2t2_wb2.build(w)          # Part 3 - the methodology
m2t2_wb2b.build(w)         # Part 4 - the patterns
m2t2_wb3.build(w)          # Parts 5 and 6 - tools, and the guided tutorials
m2t2_wb4.build_exercises(w)
m2t2_wb4.build_solutions(w)
m2t2_wb4.build_reference(w)
w.save(OUT)
print("exercises:", len(m2t2_wb4.EX))
