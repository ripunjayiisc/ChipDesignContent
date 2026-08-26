# Topic 4 source — how to regenerate the deliverables

The Topic 4 presentation, its diagrams and the workbook are generated from the
scripts here. They reuse the shared toolkit one level up (`dsl.py`, `deckkit.py`,
`wbkit.py`, `checkfit.py`), so a fix to the design system flows into both topics.

`_boot.py` sets `CDA_IMG_DIR` to `topic4/img/` and puts the parent folder on the
import path, so every script starts with `import _boot`.

## Prerequisites

```bash
pip install python-pptx python-docx matplotlib pillow
sudo apt install libreoffice-impress libreoffice-writer poppler-utils
```

## Rebuild everything

```bash
cd build/topic4

python3 t4_lang.py       # 4a diagrams   -> img/
python3 t4_model.py      # 4b diagrams   -> img/
python3 t4_design.py     # 4c diagrams   -> img/
python3 t4_tools.py      # tool and flow diagrams -> img/

python3 build_deck_t4.py       # -> ../../Module2_Topic4_RTLDesignUsingHDL.pptx      (83 slides)
python3 build_workbook_t4.py   # -> ../../Module2_Topic4_Tutorial_Practice_Workbook.docx (69 pp)

python3 ../checkfit.py ../../Module2_Topic4_RTLDesignUsingHDL.pptx   # must report 0 flagged
```

`img/` is not committed — the four diagram scripts regenerate all 30 figures in a
few seconds.

## Layout rules worth knowing before you edit

* `deckkit.fig`-style slides run from `TOP = 1143000` to `BOTTOM = 6415000` EMU.
  `checkfit.py` catches anything that runs past the bottom or overflows a card;
  it must report `total flagged: 0` before you commit.
* In `dsl.fig(w, h)` the aspect ratio is locked and the y axis runs `0` to
  `100*h/w`. Budget vertical space explicitly — do not assume 100.
* `d.code()` line height is `size * 12700 * 1.48` EMU. Long listings need
  `size=9` or `8.5`.

## Where the numbers come from

Every synthesis figure quoted in the deck and workbook was produced by running
`Topic4_Lab/scripts/synth_all.sh` (Yosys 0.33, `abc -g AND,OR,XOR,NAND,NOR`).
Simulation results come from `Topic4_Lab/scripts/run_all.sh` (Icarus Verilog
12.0) and lint from `lint.sh` (Verilator 5.020). The Vivado and ModelSim scripts
in the lab are working templates that were **not** executed — see the note at the
end of `Topic4_Lab/README.md`.
