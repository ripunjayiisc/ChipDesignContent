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

# 1. the 60 diagrams  ->  topic2/img/*.png
python3 t2_rtl.py        # 6  what RTL is, the ladder, proof
python3 t2_method.py     # 9  the flow, the subset, latches, lint, reuse
python3 t2_struct.py     # 9  comb vs seq, the discipline, datapath+controller,
                         #    the running example, style, pitfalls, generate
python3 t2_fsm.py        # 9  the three-block pattern, Moore/Mealy, encoding
python3 t2_syntax.py     # 7  Verilog and VHDL cards, mapping, testbench
python3 t2_hdl.py        # 7  HDLs, concurrency, module anatomy, Verilog vs VHDL
python3 t2_tools.py      # 7  tools, install, lab flow, lab map, Vivado
python3 t2_outcomes.py   # 6  terminal and learning outcomes, syllabus map

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

## The readability budget — read this before editing a diagram

A 16:9 slide with a title bar leaves **12.30 x 5.76 inches** for the picture,
an aspect ratio of **2.14**. Anything taller in proportion is scaled DOWN to fit
the height, and its text shrinks with it. The first version of these diagrams
was drawn 11.5 inches wide and 7–10 inches tall, so a panel landed on the slide
around 6.5 inches wide and 8pt type in it read as **5pt**. That is why the
diagrams were unreadable, and no amount of raising point sizes alone fixes it:

```
effective pt on the slide = fontsize x (drawn width / panel width)
                          = fontsize x (image height cap / panel height)   when height-limited
```

So every panel is now drawn **wide and short**, from `dsl.panel()`:

```python
from dsl import *

def my_diagram():
    f, ax, H = panel()          # 11.5 x 5.6 in, aspect 2.05; H = 48.7 units
    title(ax, 50, H - 4.5, "...", FS_TITLE)
    ...                          # lay out downwards from H - 9.5
    save(f, "my_diagram")
```

`panel(PHT)` gives the taller 11.5 x 6.6 reference page (aspect 1.74) for
pages that are meant to be read rather than glanced at — the language cards,
the lab map, the long tables.

Point sizes come from the constants in `dsl.py` (`FS_TITLE` 17, `FS_HEAD` 13,
`FS_BODY` 12, `FS_SMALL` 11, `FS_TABLE` 11.5, `FS_MONO` 10.5), chosen so text
lands on the slide at roughly the size it is written here. Do not hard-code
sizes below `FS_MONO`.

The vertical budget is about **34 units** of content under the title. That is
roughly one table of 8 rows, or three stacked bands, or two side-by-side cards
of 8 lines. If it does not fit: **split the panel in two, or move the prose
onto the slide as a card** — do NOT increase `Hin`, because that shrinks the
whole panel on the slide and undoes the point of the exercise.

Prose that used to sit in a box at the bottom of a panel now lives on the slide
instead. There it is real vector text at 12pt that stays sharp at any zoom, and
it keeps the panel short.

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
| `mux_styles`, 3 / 6 / 10 cells | `make mux` |
| `blocking_measured`, 3 flops vs 1 | `make pitfalls` |
| `moore_mealy_timing`, 5 matches | `make fsm` |
| `state_encoding`, 13 vs 30 cells | `make fsm` |
| `traffic_states`, 40 cycles, 0 violations | `make fsm` |
| `datapath_controller`, 10 vs 145 cells | `make dpctrl` |
| `hierarchy_generate`, the four depths | `make reuse` |
| `two_languages_result` | `make langs` |
| `flow_executed`, the seven stages | `make flow` |

Vivado and ModelSim were not run — the deck says so on the slide that shows
their commands.

## Files

```
t2_rtl.py           diagrams: what RTL is, the abstraction ladder, proof
t2_method.py        diagrams: the design process and methodology
t2_struct.py        diagrams: how a real block is put together
t2_fsm.py           diagrams: finite state machines
t2_syntax.py        diagrams: the two languages as reference cards
t2_hdl.py           diagrams: hardware description languages
t2_tools.py         diagrams: tools, installation, the lab programme
t2_outcomes.py      diagrams: terminal and learning outcomes, syllabus map

t2_deck_a.py        deck: front matter, outcomes, Theory 1   (27 slides)
t2_deck_b.py        deck: Theory 2 — the methodology         (16 slides)
t2_deck_c2.py       deck: Theory 3 — the patterns            (20 slides)
t2_deck_c.py        deck: Theory 4 and the practical part    (33 slides)
build_deck_m2t2.py  assembles the 96-slide deck

m2t2_wb1.py         workbook: front matter, outcomes, Theory Part 1
m2t2_wb2.py         workbook: Theory Part 2, and Part 4 (build_hdl)
m2t2_wb2b.py        workbook: Theory Part 3 — the patterns
m2t2_wb3.py         workbook: Practical — tools, and fourteen tutorials
m2t2_wb4.py         workbook: 103 exercises, solutions, reference card
build_workbook_m2t2.py
```

## A note for the other topics

`dsl.py`, `deckkit.py` and `wbkit.py` are shared with Topics 3–6 and Module 3
Topic 1. The readability work above changed all three: `dsl.py` gained the
`panel()` helper and the `FS_*` constants, and `deckkit`/`wbkit` had their
default point sizes raised (deck body 11 -> 12, deck tables 10 -> 11.5, deck
code 10.5 -> 11.5; workbook body 10.5 -> 11.5, workbook tables 9.5 -> 10.5,
workbook code 8.8 -> 9.6).

Those topics' `.pptx` and `.docx` files are committed artefacts and are not
rebuilt automatically, so nothing about them has changed on disk. If you do
rebuild one, expect its text to come out larger and its layouts to need the
same treatment: reshape the diagrams to `panel()`, then run `checkfit.py` and
fix whatever it flags.
