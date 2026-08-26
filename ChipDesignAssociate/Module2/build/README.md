# Topic 3 source — how to regenerate the deliverables

The presentation, its diagrams and the workbook in the folder above are all
generated from the scripts here, so a correction is made once and flows into
every deliverable.

## Prerequisites

```bash
pip install python-pptx python-docx matplotlib pillow
sudo apt install libreoffice-impress libreoffice-writer poppler-utils   # for PDF export
```

## Rebuild everything

```bash
python3 d_bool.py        # 3a diagrams  -> img/
python3 d_comb.py        # 3b diagrams  -> img/
python3 d_seq.py         # 3c diagrams  -> img/
python3 d_fsm.py         # FSM, register, counter and toolchain diagrams -> img/

python3 build_deck.py       # -> ../Module2_Topic3_DigitalLogicDesignPrinciples.pptx
python3 build_workbook.py   # -> ../Module2_Topic3_Tutorial_Practice_Workbook.docx

./render.sh ../Module2_Topic3_DigitalLogicDesignPrinciples.pptx   # PDF + page PNGs
python3 checkfit.py                                              # layout overflow check
```

`img/` is not committed — it is regenerated in a few seconds by the four
diagram scripts.

## What each file is

| File | Purpose |
|---|---|
| `dsl.py` | drawing primitives and the house palette: gates, wires, waveforms, tables, K-maps |
| `d_bool.py` `d_comb.py` `d_seq.py` `d_fsm.py` | the 38 diagrams, grouped by subtopic |
| `deckkit.py` | PowerPoint design system — geometry, type scale and slide/card/code/table blocks, taken verbatim from the Topic 1 deck so the two match |
| `content_a…d.py` | the 73 slides of deck content |
| `build_deck.py` | assembles the deck |
| `wbkit.py` | Word styling — Georgia headings, callouts, code blocks, tables |
| `wb_part1…5.py` | the seven parts of the workbook, including all 46 exercises and their solutions |
| `build_workbook.py` | assembles the workbook |
| `checkfit.py` | flags any card or text box that overflows its container or the slide |
| `render.sh` | converts a deck to PDF and rasterises the pages for visual review |
| `sheet.py` `pv.py` | contact-sheet helpers used while reviewing diagrams and slides |

## House style

Colours, fonts and geometry are copied from
`Module2_Topic1_Expanded.pptx` so Topic 3 is visually indistinguishable
from Topic 1. If you restyle one, restyle both.

- Navy `#0E2A47`, teal `#1B9AAA`, amber `#C77514`, green `#2A9D5C`, red `#C01F43`
- Cambria / Georgia for headings, Calibri for body, Consolas for code
- Slides are 13.3 × 7.5 in; content lives between y = 1 143 000 and 6 415 000 EMU

## A note on the diagram scripts

`dsl.fig(w, h)` locks the aspect ratio, so the y axis runs from 0 to
`100 * h / w`. Every diagram computes that value as `H` and budgets its
vertical space against it — otherwise content silently renders off the top of
the figure. Keep that convention when editing.
