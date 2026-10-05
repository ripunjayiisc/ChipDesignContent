# -*- coding: utf-8 -*-
"""Assemble the Lecture 01 tutorial and practice workbook."""
import os
import _boot
from wbkit import Workbook
import l1_wb1, l1_wb2, l1_wb3, l1_wb4

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Lecture01_Introduction_Workbook.docx"))

w = Workbook("Hardware Modeling using Verilog (NPTEL, IIT Kharagpur)  ·  "
             "Lecture 01: Introduction  ·  Tutorial and Practice Workbook  ·  "
             "Chip Design Associate")
l1_wb1.build(w)            # front matter, Part 1 and Part 2
l1_wb2.build(w)            # Part 3 - the design flow, step by step
l1_wb3.build(w)            # Part 4 - installing the tools, and the five labs
l1_wb4.build_exercises(w)  # Part 5 - the exercises
l1_wb4.build_solutions(w)  #          and their worked solutions
l1_wb4.build_reference(w)  # Part 6 - reference
w.save(OUT)
