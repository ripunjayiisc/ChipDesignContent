# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _boot
from wbkit import Workbook
import m3_wb1, m3_wb2, m3_wb3, m3_wb4

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "Module3_Topic1_Tutorial_Practice_Workbook.docx"))
w = Workbook("Module 3 · Topic 1 · Overview of VLSI STA   ·   "
             "Chip Design Associate (O-Level ‘Chip Design’)   ·   NIE/ELE/N0103")
m3_wb1.build(w)
m3_wb2.build(w)
m3_wb3.build(w)
m3_wb4.build_exercises(w)
m3_wb4.build_solutions(w)
m3_wb4.build_reference(w)
w.save(OUT)
print("exercises:", len(m3_wb4.EX))
