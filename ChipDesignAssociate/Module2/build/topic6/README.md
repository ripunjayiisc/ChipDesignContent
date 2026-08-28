# Topic 6 source — how to regenerate the deliverables

The Topic 6 presentation, its diagrams and the workbook are generated from the
scripts here. They reuse the shared toolkit one level up (`dsl.py`, `deckkit.py`,
`wbkit.py`, `checkfit.py`), so a fix to the design system flows into all topics.

`_boot.py` sets `CDA_IMG_DIR` to `topic6/img/` and puts the parent folder on the
import path, so every script starts with `import _boot`.

## Rebuild everything

```bash
cd ChipDesignAssociate/Module2/build/topic6

# 1. the 37 diagrams  ->  topic6/img/*.png
python3 t6_basics.py        # 6  setup/hold window, path, slack, skew, uncertainty
python3 t6_constraints.py   # 8  SDC map, create_clock, I/O delay, exceptions
python3 t6_analysis.py      # 8  STA vs sim, graph, sweeps, report, WNS/TNS, corners
python3 t6_opt.py           # 8  fix menu, pipelining, retiming, hold race, closure
python3 t6_tools.py         # 7  landscape, install, flows, SDC/XDC, lab map

# 2. the deck  ->  ../../Module2_Topic6_TimingConstraintsAndAnalysis.pptx
python3 build_deck_t6.py
python3 ../checkfit.py ../../Module2_Topic6_TimingConstraintsAndAnalysis.pptx
#   must print "total flagged: 0"

# 3. the workbook  ->  ../../Module2_Topic6_Tutorial_Practice_Workbook.docx
python3 build_workbook_t6.py

# 4. the PDF
bash ../render.sh ../../Module2_Topic6_TimingConstraintsAndAnalysis.pptx /tmp/t6
```

`img/` and `__pycache__/` are generated and are not committed — rebuild them
with the five diagram scripts above.

## Layout rules that keep the diagrams clean

`dsl.fig(w, h)` locks the aspect ratio and makes the y-axis run from 0 to
`100*h/w`. Every diagram function therefore starts by computing `H` and lays
its content out top-down against an explicit vertical budget. If two elements
collide, the fix is almost always to increase `Hin` rather than to shuffle
coordinates.

`sheet.py` stacks rendered PNGs into one contact sheet, which is how the
diagrams were reviewed:

```bash
python3 sheet.py /tmp/check.png setup_hold_window timing_path slack_equation
```

## Where the numbers come from

Every measured figure in the deck and the workbook was produced by
`Module2/Topic6_Lab`. If you change the lab, re-run it and update:

| Figure / slide | Source command |
|---|---|
| `measured_results`, closure table | `make closure` |
| `fmax_idea`, `pipelining`, T5 sweep | `make sweep` |
| Tutorial 3 report, `report_anatomy` | `make tiny` |
| hold −0.165 / +0.071 | `make hold` |
| multicycle −1.193 / +0.392 | `make mcp` |

## Files

```
t6_basics.py        diagrams: the physics of a flip-flop
t6_constraints.py   diagrams: SDC/XDC
t6_analysis.py      diagrams: how STA works
t6_opt.py           diagrams: optimisation and closure
t6_tools.py         diagrams: tools, installation, the lab programme

t6_content_a.py     deck part 6a — constraints            (21 slides)
t6_content_b.py     deck part 6b — analysis, optimisation (22 slides)
t6_content_c.py     deck part 6c — setup and hold         (16 slides)
t6_content_d.py     deck — tools, labs, glossary, close   (22 slides)
build_deck_t6.py    assembles the 81-slide deck

t6_wb1.py           workbook part 1 + front matter
t6_wb2.py           workbook parts 2 and 3
t6_wb3.py           workbook parts 4, 5 and 6
t6_wb4.py           workbook part 7 — seven guided tutorials
t6_wb5.py           62 exercises, worked solutions, reference card
build_workbook_t6.py assembles the workbook
```
