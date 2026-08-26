# -*- coding: utf-8 -*-
"""Assemble the Module 2 Topic 4 deck."""
import os
import _boot
from deckkit import Deck
import t4_content_a, t4_content_b, t4_content_c, t4_content_d

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Module2_Topic4_RTLDesignUsingHDL.pptx"))

d = Deck("Chip Design Associate · Module 2 · Verilog RTL Coding for Synthesis · "
         "Topic 4: RTL Design Using HDL", "M2-T4")
for m in (t4_content_a, t4_content_b, t4_content_c, t4_content_d):
    m.build(d)
d.save(OUT)
