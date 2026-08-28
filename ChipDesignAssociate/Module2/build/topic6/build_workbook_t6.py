# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _boot
from wbkit import Workbook
import t6_wb1, t6_wb2, t6_wb3, t6_wb4, t6_wb5

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "Module2_Topic6_Tutorial_Practice_Workbook.docx"))
w = Workbook("Module 2 · Topic 6 · Timing Constraints and Analysis   ·   "
             "Chip Design Associate (O-Level ‘Chip Design’)   ·   NIE/ELE/N0102")
t6_wb1.build(w)
t6_wb2.build(w)
t6_wb3.build(w)
t6_wb4.build(w)
t6_wb5.build_exercises(w)
t6_wb5.build_solutions(w)
t6_wb5.build_reference(w)
w.save(OUT)
print("exercises:", len(t6_wb5.EX))
