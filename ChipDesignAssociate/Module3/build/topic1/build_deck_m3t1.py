# -*- coding: utf-8 -*-
"""Assemble the Module 3 Topic 1 deck."""
import os
import _boot
from deckkit import Deck
import m3_deck_a, m3_deck_b, m3_deck_c, m3_deck_d

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Module3_Topic1_OverviewOfVLSI_STA.pptx"))

d = Deck("Chip Design Associate · Module 3 · Static Timing Analysis of VLSI Circuits · "
         "Topic 1: Overview of VLSI STA", "M3-T1")
for m in (m3_deck_a, m3_deck_b, m3_deck_c, m3_deck_d):
    m.build(d)
d.save(OUT)
