# -*- coding: utf-8 -*-
"""Assemble the Module 2 Topic 2 deck."""
import os
import _boot
from deckkit import Deck
import t2_deck_a, t2_deck_lang, t2_deck_b, t2_deck_c2, t2_deck_c

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..",
    "Module2_Topic2_RTLDesignMethodology.pptx"))

d = Deck("Chip Design Associate · Module 2 · Verilog RTL Coding for Synthesis · "
         "Topic 2: RTL Design Methodology", "M2-T2")
for m in (t2_deck_a,       # Theory 1 - what RTL is
          t2_deck_lang,    # Theory 2 - the language
          t2_deck_b,       # Theory 3 - the methodology
          t2_deck_c2,      # Theory 4 - the patterns
          t2_deck_c):      # the practical component
    m.build(d)
d.save(OUT)
