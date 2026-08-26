# Topic 5 source — how to regenerate the deliverables

The Topic 5 presentation, its diagrams and the workbook are generated from the
scripts here. They reuse the shared toolkit one level up (`dsl.py`, `deckkit.py`,
`wbkit.py`, `checkfit.py`), so a fix to the design system flows into all topics.

`_boot.py` sets `CDA_IMG_DIR` to `topic5/img/` and puts the parent folder on the
import path, so every script starts with `import _boot`.

## Prerequisites

```bash
pip install python-pptx python-docx matplotlib pillow
sudo apt install libreoffice-impress libreoffice-writer poppler-utils
```

## Rebuild everything

```bash
cd build/topic5

python3 t5_concepts.py   # verification fundamentals   -> img/   (9 figures)
python3 t5_tb.py         # testbench construction      -> img/  (10 figures)
python3 t5_sim.py        # simulation and debugging    -> img/   (8 figures)
python3 t5_tools.py      # tools and regression        -> img/   (4 figures)

python3 build_deck_t5.py       # -> ../../Module2_Topic5_RTLSimulationAndVerification.pptx  (69 slides)
python3 build_workbook_t5.py   # -> ../../Module2_Topic5_Tutorial_Practice_Workbook.docx    (59 pp)

python3 ../checkfit.py ../../Module2_Topic5_RTLSimulationAndVerification.pptx   # must be 0 flagged
```

`img/` is not committed — the four diagram scripts regenerate all 31 figures in
a few seconds.

## Deck structure

| Part file | Slides | Covers |
|---|---|---|
| `t5_content_a.py` | 1–14 | title, roadmap, motivation, and subtopic 5a (verification techniques) |
| `t5_content_b.py` | 15–34 | subtopic 5b core — the six parts, V1 to V6, assertions |
| `t5_content_d.py` | 35–46 | subtopic 5b advanced — mechanics, file I/O, reuse, SystemVerilog, UVM, formal, CDC, metrics |
| `t5_content_c.py` | 47–69 | subtopic 5c (simulation and debugging), tools, labs, glossary, recap |

They are assembled in the order a, b, d, c by `build_deck_t5.py`. If you add or
remove slides, update the roadmap table in `t5_content_a.py` — it cites slide
ranges.

## Layout rules worth knowing before you edit

* Slides run from `TOP = 1143000` to `BOTTOM = 6415000` EMU. `checkfit.py` catches
  anything that runs past the bottom or overflows a card; it must report
  `total flagged: 0` before you commit.
* In `dsl.fig(w, h)` the aspect ratio is locked and the y axis runs `0` to
  `100*h/w`. Budget vertical space explicitly — do not assume 100.
* Matplotlib treats `$` as the start of math mode, so `$display` must be written
  `\\$display` in any diagram text.
* `d.code()` line height is `size * 12700 * 1.48` EMU. Long listings need
  `size=9` or smaller.
* `d.image(s, y, name, h, w=MW)` makes a wide diagram fill the content width;
  without `w` it is centred at its natural aspect ratio and can look small.

## Where the numbers come from

Every figure quoted in the deck and workbook — the 0/5, 4/5, 5/5 clinic matrix,
the coverage merge, the assertion timings — was produced by running the scripts
in `Topic5_Lab/` under Icarus Verilog 12.0 and Verilator 5.020. The Vivado and
ModelSim scripts in the lab are working templates that were **not** executed;
see the note at the end of `Topic5_Lab/README.md`.

Reproduce the headline result with:

```bash
cd ../../Topic5_Lab && make
```
