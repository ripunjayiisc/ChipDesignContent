# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _boot
from wbkit import Workbook
import t4_wb1, t4_wb2, t4_wb3, t4_wb4, t4_wb5

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "Module2_Topic4_Tutorial_Practice_Workbook.docx"))
w = Workbook("Module 2 · Topic 4 · RTL Design Using HDL   ·   "
              "Chip Design Associate (O-Level ‘Chip Design’)   ·   NIE/ELE/N0102")
t4_wb1.build(w)
t4_wb2.build(w)
t4_wb3.build(w)
t4_wb4.build(w)
t4_wb5.build_exercises(w)
t4_wb5.build_solutions(w)
t4_wb5.build_reference(w)
w.save(OUT)
