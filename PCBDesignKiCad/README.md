# PCB Design with KiCad — short-term course

A 60-hour short-term course (20 theory + 40 practical), pinned to **KiCad
10.0.6**. Draft for review.

| File | What it is |
|---|---|
| `Course_Outline.md` | **The source of truth.** Edit this. |
| `PCB_Design_with_KiCad_Course_Outline.docx` / `.pdf` | The same thing typeset in the house style, for circulation |
| `build/build_outline.py` | Renders the Markdown into the .docx |

```
cd build && python3 build_outline.py
```

The builder reuses `ChipDesignAssociate/Module2/build/wbkit.py` for styling, so
the outline matches the Verilog-course workbooks.

## Status

This is a course **plan**, not the teaching material. Section 12 lists the five
decisions needed before the material is built: duration, fabrication budget,
lab hardware, certification route, and the choice of main project.

Once those are settled, the per-module decks and workbooks can be built the
same way as the Verilog lectures — see
`ChipDesignAssociate/VerilogCourse/build/lec01/README.md` for that toolchain.
