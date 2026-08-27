# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _boot
from wbkit import Workbook
import t5_wb1, t5_wb2, t5_wb3, t5_wb4

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "Module2_Topic5_Tutorial_Practice_Workbook.docx"))
w = Workbook("Module 2 · Topic 5 · RTL Simulation and Verification   ·   "
             "Chip Design Associate (O-Level ‘Chip Design’)   ·   NIE/ELE/N0102")
t5_wb1.build(w)
t5_wb2.build(w)
t5_wb3.build(w)
t5_wb4.build_exercises(w)
t5_wb4.build_solutions(w)
t5_wb4.build_reference(w)
w.save(OUT)
