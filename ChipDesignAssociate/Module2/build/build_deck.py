import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deckkit import Deck
import content_a, content_b, content_c, content_d

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "Module2_Topic3_DigitalLogicDesignPrinciples.pptx")

d = Deck("Module 2 · Verilog RTL Coding for Synthesis", "NIE/ELE/N0102 · Topic 3")
for m in (content_a, content_b, content_c, content_d):
    m.build(d)
d.save(os.path.abspath(OUT))
