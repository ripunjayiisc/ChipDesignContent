# -*- coding: utf-8 -*-
"""Assemble the Module 2 Topic 6 deck."""
import os
import _boot
from deckkit import Deck
import t6_content_a, t6_content_b, t6_content_c, t6_content_d

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Module2_Topic6_TimingConstraintsAndAnalysis.pptx"))

d = Deck("Chip Design Associate · Module 2 · Verilog RTL Coding for Synthesis · "
         "Topic 6: Timing Constraints and Analysis", "M2-T6")
for m in (t6_content_a, t6_content_b, t6_content_c, t6_content_d):
    m.build(d)
d.save(OUT)
