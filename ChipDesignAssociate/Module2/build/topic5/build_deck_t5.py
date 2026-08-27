# -*- coding: utf-8 -*-
"""Assemble the Module 2 Topic 5 deck."""
import os
import _boot
from deckkit import Deck
import t5_content_a, t5_content_b, t5_content_d, t5_content_c

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Module2_Topic5_RTLSimulationAndVerification.pptx"))

d = Deck("Chip Design Associate · Module 2 · Verilog RTL Coding for Synthesis · "
         "Topic 5: RTL Simulation and Verification", "M2-T5")
for m in (t5_content_a, t5_content_b, t5_content_d, t5_content_c):
    m.build(d)
d.save(OUT)
