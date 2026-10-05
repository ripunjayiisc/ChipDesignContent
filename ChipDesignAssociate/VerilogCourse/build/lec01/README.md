# Building the Lecture 01 material

Source for `Lecture01_Introduction.pptx` and
`Lecture01_Introduction_Workbook.docx`.

```
python3 l1_front.py l1_why.py l1_flow.py l1_steps.py l1_lab.py   # the diagrams
python3 build_deck_lec01.py                                      # the deck
python3 build_workbook_lec01.py                                  # the workbook
python3 fitcheck.py                                              # must print 0
python3 ../../../Module2/build/checkfit.py \
        ../../Lecture01_Introduction.pptx                        # must print 0
```

`_boot.py` puts `Module2/build` (dsl.py, deckkit.py, wbkit.py) on the path and
points `CDA_IMG_DIR` at `img/`, which is gitignored — the PNGs are rebuilt by
the commands above.

## Where the content comes from

`ChipDesignAssociate/Hardware Modeling using Verilog NPTEL.pdf`, pages 4–19
(body pages 1–16): Lecture 01 of Prof. Indranil Sengupta's NPTEL course. All
fifteen of the lecturer's slides are kept, in his order; the expansion is built
around them, not in place of them. `source_map` in `l1_front.py` is the audit
trail — it lists each original slide, by its "Refer Slide Time" marker, beside
what this session adds to it.

## Two invariants

**1 — every panel fits inside its axes.** `fitcheck.py` measures each artist's
bounding box in data coordinates and flags anything outside `(0..100, 0..H)`.
This matters more than it looks: `dsl.save()` writes with
`bbox_inches="tight"`, so content drawn outside the axes is *not* clipped —
the figure silently grows instead, and the panel then lands on the slide
scaled down, with all its text shrunk. A clean fitcheck is what keeps the
readability budget in `dsl.py` honest.

**2 — no text overflows its card.** `Module2/build/checkfit.py`. Note that it
was corrected while this lecture was built: it modelled monospace at 0.60 em
and 1.34 line spacing, but Consolas is nearer 0.55 em and `deckkit.code()`
sets 1.12, so every code block looked like an overflow. The six existing
Module 2 and Module 3 decks still report 0 after the change.

## Two things worth knowing before editing a panel

**Character widths are measured, not guessed.** `l1_kit.py` wraps text to a
width in *panel units*, converting with an em-factor of 0.635 that was
obtained by rendering sample strings at 9–12 pt and reading their extents back
through `ax.transData`. Passing a character count instead is how the first
draft of every panel in this lecture overflowed.

**Panels carry no title of their own.** `deckkit.slide()` already draws the
title in real, sharp text; a title inside the PNG duplicates it and wastes a
line. Panels keep only their one-line subtitle, at `H - 3.5`. If you add a
panel, follow that — and if you add a *subtitle*, put it at exactly `H - 3.5`,
because a stray `H - 7.2` is how two panels survived the de-titling pass with
their subtitle sitting on top of the content.

## Prose belongs on the slide, not in the picture

Each diagram module exposes a `CARDS` dict: `{diagram_name: (heading, text,
accent)}`. `l1_deck_a.card_from()` renders one as a real slide card at 12 pt,
which stays sharp at any zoom and keeps the panel short and wide. A long
explanatory box drawn *inside* a panel makes it tall, and a tall panel is
scaled down to fit the slide height — shrinking its text. Several panels here
were rebuilt for exactly that reason.

## The numbers in the deck are measured

Every cell count quoted on a slide or in the workbook came out of
`Lecture01_Lab`, not from an estimate:

| Claim | Produced by |
|---|---|
| 2 RTL cells, 10 gate cells, 8 FPGA cells | `make ladder` |
| 22 identical waveform transitions | `make prove` |
| 33 lines in the gate netlist | `make prove` |
| 20 identical transitions across languages | `make langs` |
| 8-bit → 22 cells; async reset → `$_DFF_PP0_`; down-counter → `$_SDFF_PP1_`; LUT-6 → still 4 LUTs | the exercise solutions in `l1_wb4.py`, each run before being written down |

If you change `rtl/counter4.v`, re-run the labs and update the figures in
`l1_lab.py` (`measured`), `l1_deck_c.py` and `l1_wb3.py`/`l1_wb4.py`.
