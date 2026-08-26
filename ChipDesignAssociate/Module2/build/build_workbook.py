import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wbkit import Workbook
import wb_part1, wb_part2, wb_part3, wb_part4, wb_part5

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                      "Module2_Topic3_Tutorial_Practice_Workbook.docx"))
w = Workbook()
wb_part1.build(w)
wb_part2.build(w)
wb_part3.build(w)
wb_part4.build(w)
wb_part5.build_exercises(w)
wb_part5.build_solutions(w)
wb_part5.build_reference(w)
w.save(OUT)
