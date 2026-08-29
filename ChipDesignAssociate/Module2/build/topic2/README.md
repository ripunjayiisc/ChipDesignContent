# Module 2 Topic 2 source — how to regenerate the deliverables

The presentation, its diagrams and the workbook are generated from the scripts
here. They reuse the shared toolkit one level up (`dsl.py`, `deckkit.py`,
`wbkit.py`, `checkfit.py`, `render.sh`), so a fix to the design system flows
into every topic.

`_boot.py` sets `CDA_IMG_DIR` to `topic2/img/` and puts the parent folder on the
import path, so every script starts with `import _boot`.

## Rebuild everything

```bash
cd ChipDesignAssociate/Module2/build/topic2

# 1. the 34 diagrams  ->  topic2/img/*.png
python3 t2_rtl.py        # 6  what RTL is, the ladder, proof
python3 t2_method.py     # 9  the flow, the subset, latches, lint, reuse
python3 t2_hdl.py        # 7  HDLs, concurrency, module anatomy, Verilog vs VHDL
python3 t2_tools.py      # 7  tools, install, lab flow, lab map, Vivado
python3 t2_outcomes.py   # 5  terminal and learning outcomes, syllabus map

# 2. the deck  ->  ../../Module2_Topic2_RTLDesignMethodology.pptx
python3 build_deck_m2t2.py
python3 ../checkfit.py ../../Module2_Topic2_RTLDesignMethodology.pptx
#   must print "total flagged: 0"

# 3. the workbook  ->  ../../Module2_Topic2_Tutorial_Practice_Workbook.docx
python3 build_workbook_m2t2.py

# 4. the PDF
bash ../render.sh ../../Module2_Topic2_RTLDesignMethodology.pptx /tmp/m2t2
```

`img/` and `__pycache__/` are generated and are not committed.

## Layout rules that keep the diagrams clean

`dsl.fig(w, h)` locks the aspect ratio and makes the y-axis run from 0 to
`100*h/w`. Every diagram function computes `H` first and lays its content out
top-down against an explicit vertical budget. When two elements collide, the fix
is almost always to increase `Hin` rather than to shuffle coordinates.

`sheet.py` stacks rendered PNGs into one contact sheet, which is how every
diagram in this topic was reviewed before it went into the deck:

```bash
python3 sheet.py /tmp/check.png rtl_definition ladder proof_vs_test
```

## Where the numbers come from

Every measured figure in the deck and the workbook was produced by
`Module2/Topic2_Lab`. If you change the lab, re-run it and update:

| Figure / slide | Source command |
|---|---|
| `ladder`, four levels agreeing | `make ladder` |
| `ladder_synthesis`, 5 vs 6 cells | the synthesis step in `make ladder` |
| `proof_vs_test`, the SAT results | `make prove` |
| `synth_subset`, the eleven rows | `make subset` |
| `sim_synth_mismatch` | `make mismatch` |
| `lint_rules`, 0 disagreements | `make lint`, `make lintcheck` |
| `two_languages_result` | `make langs` |
| `flow_executed`, the seven stages | `make flow` |

Vivado and ModelSim were not run — the deck says so on the slide that shows
their commands.

## Files

```
t2_rtl.py           diagrams: what RTL is, the abstraction ladder, proof
t2_method.py        diagrams: the design process and methodology
t2_hdl.py           diagrams: hardware description languages
t2_tools.py         diagrams: tools, installation, the lab programme
t2_outcomes.py      diagrams: terminal and learning outcomes, syllabus map

t2_deck_a.py        deck: front matter, outcomes, Theory 1   (17 slides)
t2_deck_b.py        deck: Theory 2 — the methodology         (14 slides)
t2_deck_c.py        deck: Theory 3 and the practical part    (23 slides)
build_deck_m2t2.py  assembles the 54-slide deck

m2t2_wb1.py         workbook: front matter, outcomes, Theory Part 1
m2t2_wb2.py         workbook: Theory Parts 2 and 3
m2t2_wb3.py         workbook: Practical — tools, and nine tutorials
m2t2_wb4.py         workbook: 60 exercises, solutions, reference card
build_workbook_m2t2.py
```
