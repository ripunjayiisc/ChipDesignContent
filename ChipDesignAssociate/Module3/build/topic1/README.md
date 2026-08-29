# Module 3 Topic 1 source — how to regenerate the deliverables

The presentation, its diagrams and the workbook are generated from the scripts
here. They reuse the shared toolkit that lives in `Module2/build/` — `dsl.py`,
`deckkit.py`, `wbkit.py`, `checkfit.py`, `render.sh`. That toolkit is
course-wide, not Module-2-specific; `_boot.py` puts it on the import path and
points `CDA_IMG_DIR` at this topic's `img/`.

## Rebuild everything

```bash
cd ChipDesignAssociate/Module3/build/topic1

# 1. the 34 diagrams  ->  topic1/img/*.png
python3 m3_hazard.py     # 7  hazards: mechanism, kinds, race, K-map, fix, results
python3 m3_seq.py        # 9  races, setup/hold, Fmax, violations, STA vs simulation
python3 m3_synth.py      # 6  constraints for synthesis, and what synthesis does back
python3 m3_tools.py      # 7  tool landscape, installation, lab flow, Vivado, labs
python3 m3_outcomes.py   # 5  terminal outcomes, learning outcomes, syllabus map

# 2. the deck  ->  ../../Module3_Topic1_OverviewOfVLSI_STA.pptx
python3 build_deck_m3t1.py
python3 ../../../Module2/build/checkfit.py \
        ../../Module3_Topic1_OverviewOfVLSI_STA.pptx
#   must print "total flagged: 0"

# 3. the workbook  ->  ../../Module3_Topic1_Tutorial_Practice_Workbook.docx
python3 build_workbook_m3t1.py

# 4. the PDF
bash ../../../Module2/build/render.sh \
     ../../Module3_Topic1_OverviewOfVLSI_STA.pptx /tmp/m3
```

`img/` and `__pycache__/` are generated and are not committed — rebuild them
with the five diagram scripts.

## Layout rules that keep the diagrams clean

`dsl.fig(w, h)` locks the aspect ratio and makes the y-axis run from 0 to
`100*h/w`. Every diagram function computes `H` first and lays its content out
top-down against an explicit vertical budget. When two elements collide, the
fix is almost always to increase `Hin` rather than to shuffle coordinates.

Two helpers are easy to misjudge, and both cost a rebuild cycle here:

* `gate(ax, kind, x, y, w, h)` takes `x` as the **left edge** and `y` as the
  **vertical centre**, and the drawn shape extends past `x+w` by the output
  stub. Wiring several gates together by hand is error-prone — the
  hazard diagrams use timing waveforms instead, which show the race better
  anyway.
* `wave(ax, x0, y, width, seq, unit)` takes `width` as the width **per sample**,
  so the trace spans `len(seq) * width`, and rises `0.62 * unit` above `y`.

`sheet.py` stacks rendered PNGs into one contact sheet, which is how every
diagram in this topic was reviewed:

```bash
python3 sheet.py /tmp/check.png hazard_idea hazard_race consensus_fix
```

## Where the numbers come from

Every measured figure in the deck and the workbook was produced by
`Module3/Topic1_Lab`. If you change the lab, re-run it and update:

| Figure / slide | Source command |
|---|---|
| `hazard_results`, the six-row table | `make glitch` |
| `where_hazards_matter` | `make capture` |
| `synth_deletes_fix` | `make synth` |
| `fmax_one_stage` | `make fmax` |
| `setup_violation` | `make setup` |
| `hold_violation` | `make hold` |
| the analyser self-test | `python3 tools/hazard.py --selftest` |

The one exception is `vivado/zynq_sta.tcl`, which has not been executed in the
environment these materials were built in. Both the lab README and the deck say
so.

## Files

```
m3_hazard.py        diagrams: races and hazards
m3_seq.py           diagrams: sequential timing, Fmax, violations
m3_synth.py         diagrams: constraints for synthesis
m3_tools.py         diagrams: tools, installation, the lab programme
m3_outcomes.py      diagrams: terminal and learning outcomes, syllabus map

m3_deck_a.py        deck: front matter, outcomes, Theory 1     (11 slides)
m3_deck_b.py        deck: Theory 2 — races and hazards         (20 slides)
m3_deck_c.py        deck: Theory 3 — sequential timing, Fmax   (14 slides)
m3_deck_d.py        deck: Theory 4 and the practical component (22 slides)
build_deck_m3t1.py  assembles the 67-slide deck

m3_wb1.py           workbook: front matter, outcomes, Theory 1 and 2
m3_wb2.py           workbook: Theory 3 and 4
m3_wb3.py           workbook: Practical — tools, and seven tutorials
m3_wb4.py           workbook: 58 exercises, solutions, reference card
build_workbook_m3t1.py
```
