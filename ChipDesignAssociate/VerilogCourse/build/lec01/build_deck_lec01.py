# -*- coding: utf-8 -*-
"""Assemble the Lecture 01 deck."""
import os
import _boot
from deckkit import Deck
import l1_deck_a, l1_deck_b, l1_deck_c

OUT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "Lecture01_Introduction.pptx"))

d = Deck("Hardware Modeling using Verilog (NPTEL, IIT Kharagpur) · "
         "Lecture 01: Introduction   ·   expanded for Chip Design Associate",
         "L01")
for m in (l1_deck_a,     # front matter, Theory 1 and Theory 2
          l1_deck_b,     # Theory 3 and Theory 4
          l1_deck_c):    # the practical component, and the close
    m.build(d)
d.save(OUT)
