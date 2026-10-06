# Short-Term Course — PCB Design with KiCad

**Draft for review · v0.1**

| | |
|---|---|
| **Course title** | PCB Design with KiCad |
| **Sector / Sub-sector** | Electronics / Integrated Electronics and Circuits |
| **Duration** | **60 hours** — 20 theory + 40 practical |
| **Delivery pattern** | 6 weeks × 10 h/week (weekend or evening), or 2 weeks full-time |
| **Mode** | Classroom + lab (laptop per learner); runs equally well online |
| **Indicative NSQF level** | 4 |
| **Batch size** | 20 (one workstation per learner) |
| **Software** | KiCad 10.0.6 — free, open source, Windows / macOS / Linux |
| **Outcome** | Every learner leaves with a fabricated, assembled, working board of their own design |

---

## 1. Why this course, and why KiCad

Every electronics product ends on a printed circuit board. Schematic capture and
board layout are the two skills that turn a circuit idea into something a factory
can build — and they are the skills most often missing in fresh diploma and
engineering graduates, because the subject is rarely taught hands-on.

KiCad is the right tool to teach it with:

- **Free and unrestricted.** No licence, no node count limit, no board-size
  limit, no student-edition watermark on the outputs. A learner can keep using
  it after the course, commercially, at no cost.
- **Industry-real.** It produces standard Gerber / Excellon / IPC-2581 output
  that any fabricator in the world accepts, and it is used in production by
  CERN, Raspberry Pi, Olimex, SparkFun and many others.
- **Cross-platform.** The same build on Windows, macOS and Linux, so the lab
  and the learner's own laptop behave identically.
- **Transferable.** The concepts — netlist, footprint, design rules, stack-up,
  DFM, Gerbers — are identical in Altium, Allegro and Eagle. KiCad 10 can even
  import Altium, Eagle, Allegro and PADS projects, so the skill moves with the
  learner.

### Why not a longer course

Sixty hours is enough to carry a learner from "I have never opened a PCB tool"
to "I have designed, ordered, assembled and debugged a four-layer-capable,
USB-powered microcontroller board." It is not enough to make a signal-integrity
engineer, and the course does not pretend otherwise — Module 6 names what has
been left out and where to go for it.

---

## 2. Target learners and entry requirements

**Who this is for**

- Diploma and B.Tech students in Electronics / ECE / EEE / Instrumentation
- Working technicians and service engineers moving into design
- Hardware startup founders and makers who are outsourcing layout today
- Faculty who need to teach PCB design and have no hands-on background in it

**Minimum entry requirement**

- Passed 10+2 with Science, or 2nd year of a 3-year Diploma in Electronics /
  Electrical / Instrumentation / allied branches
- Able to read a simple schematic and identify common components
- Basic computer literacy — file management, installing software

**Assumed prior knowledge** (revised in Module 1, not taught from scratch)

- Ohm's law, series and parallel circuits
- What a resistor, capacitor, diode, LED, transistor and IC do
- Reading a resistor value and a capacitor marking

**Not assumed**

- Any prior CAD experience of any kind
- Any soldering experience — Module 5 includes it
- Any knowledge of manufacturing

---

## 3. Training outcomes

On completion, the learner will be able to:

1. Explain what a printed circuit board is physically — layers, copper weight,
   substrate, solder mask, silkscreen, finish — and read a fabricator's
   capability table.
2. Capture a schematic in KiCad: place and wire symbols, use power and ground
   symbols, build hierarchical sheets, annotate, and clear every ERC violation.
3. Select real, purchasable components from distributor catalogues and
   datasheets, and assign or create the correct footprint for each.
4. Create a symbol and a footprint from a datasheet when no library part exists,
   to IPC-7351 land-pattern guidance.
5. Lay out a two-layer board: place for function, route for manufacturability,
   pour and stitch ground, and pass DRC with the fabricator's real constraints
   loaded.
6. Generate a complete, correct manufacturing package — Gerbers, drill files,
   BOM, centroid — and verify it in a Gerber viewer before placing an order.
7. Order a board from a real fabricator, assemble it, bring it up safely, and
   debug it.
8. Apply basic design-for-manufacture and design-for-assembly rules, and explain
   why each exists.

---

## 4. Module structure

| # | Module | Th | Pr | Total |
|---|--------|---:|---:|------:|
| 1 | PCB fundamentals and the KiCad design flow | 4 | 4 | 8 |
| 2 | Schematic capture | 4 | 7 | 11 |
| 3 | Footprints, libraries and component selection | 3 | 6 | 9 |
| 4 | PCB layout and routing | 5 | 11 | 16 |
| 5 | Manufacturing, assembly and bring-up | 2 | 5 | 7 |
| 6 | Capstone project and where to go next | 2 | 7 | 9 |
| | **Total** | **20** | **40** | **60** |

### The two projects

**Mini-project (Module 1, 3 h).** A two-component LED board taken from blank
project to ordered Gerbers *in a single session* — before any of it has been
taught properly. The point is that the learner sees the whole flow, end to end,
on day one. Everything afterwards is filling in a picture they already have.

**Main project (Modules 2–6).** A **USB-C powered ESP32-C3 sensor board**: a
two-layer, mostly surface-mount board with USB-C input, a 3.3 V regulator, an
ESP32-C3-MINI-1 module, a boot/reset pair, status LEDs and a 4-pin I²C
connector. It is built up week by week, fabricated in Week 5, and assembled and
brought up in Week 6.

It was chosen because it is small and cheap to make, yet forces the learner to
meet nearly everything the course teaches: a switching input, a linear
regulator, decoupling strategy, a USB differential pair, an RF module with a
keep-out requirement, mixed SMD sizes down to 0603, a connector with mechanical
load, and a ground pour that has to actually work.

---

## 5. Module details

### Module 1 · PCB fundamentals and the KiCad design flow
**4 h theory + 4 h practical = 8 h**

**Terminal outcome.** Explain what a PCB physically is, name every step of the
design flow, and complete that flow once, end to end, on a trivial board.

**Learning outcomes**
- Describe the construction of a 1-, 2- and 4-layer board: core, prepreg,
  copper, solder mask, silkscreen, surface finish.
- Explain what copper weight means and what track width it permits.
- Name the five stages of the KiCad flow and say what each produces.
- Navigate the KiCad project manager and its editors.
- Produce a complete manufacturing package for a two-component board.

**Theory**
1. What a PCB is: substrate, copper, mask, silkscreen, finish; FR-4 and when it
   is not enough.
2. Layer counts and stack-up; why a ground plane exists; through-hole vs SMD.
3. The design flow — schematic → netlist → footprints → layout → DRC → Gerbers
   → fabrication → assembly → test — and what each step consumes and produces.
4. Where KiCad fits, what each of its tools does, and how the project files
   relate to one another.
5. Fabricator capabilities: minimum track/gap, minimum drill, annular ring,
   and how to read a capability table.

**Practical**
- L1.1 Install KiCad 10.0.6 and verify it; set up libraries and a work folder.
- L1.2 Guided tour: open a finished example project and look at every stage of
  it, including the 3D viewer.
- L1.3 **Mini-project** — a battery, a resistor and an LED: schematic, ERC,
  footprints, layout, DRC, Gerbers, Gerber-viewer check. One session, start to
  finish.

**Pitfalls addressed:** confusing the schematic with the board; believing the
3D view is the deliverable; not realising the fabricator's rules must be loaded
*before* routing, not after.

---

### Module 2 · Schematic capture
**4 h theory + 7 h practical = 11 h**

**Terminal outcome.** Capture a multi-sheet schematic that is electrically
correct, readable by another engineer, and clean under ERC.

**Learning outcomes**
- Place, wire and annotate symbols; use labels, buses and net classes.
- Use power and ground symbols correctly, including KiCad 10 *local* power
  symbols.
- Split a design into hierarchical sheets with proper sheet pins.
- Read and clear every ERC violation, and explain what each one meant.
- Apply schematic conventions that make a drawing reviewable.

**Theory**
1. The schematic as a *netlist with a drawing attached* — what the tool
   actually stores.
2. Symbols, units, alternate body styles; symbol vs footprint vs component.
3. Nets, labels, global vs local vs hierarchical labels, buses.
4. Power symbols, power flags, and why ERC complains about an unconnected
   power input.
5. Hierarchical design, and when to use it.
6. Annotation, and why re-annotating a laid-out board is dangerous.
7. Readability conventions: signal flow left to right, power up, ground down,
   decoupling drawn near its load, no wires crossing where a label will do.
8. KiCad 10 additions: hop-over wire display, design blocks, design variants.

**Practical**
- L2.1 Capture the USB-C input and the 3.3 V regulator section.
- L2.2 Add the ESP32-C3-MINI-1 module, its decoupling, boot and reset circuits.
- L2.3 Add status LEDs and the I²C connector; assign net classes.
- L2.4 Split the design into three hierarchical sheets.
- L2.5 Run ERC to zero violations; explain each one found on the way.
- L2.6 Peer review: swap schematics with another learner and mark it against a
  readability checklist.

**Pitfalls addressed:** nets that look connected but are not; missing power
flags; copy-pasted blocks with duplicate references; decoupling capacitors
drawn in a corner far from the IC they serve.

---

### Module 3 · Footprints, libraries and component selection
**3 h theory + 6 h practical = 9 h**

**Terminal outcome.** Choose a real, available part, and give it a footprint
that will actually solder.

**Learning outcomes**
- Read a datasheet's mechanical drawing and recommended land pattern.
- Assign footprints from the standard libraries and judge whether they fit.
- Create a new footprint to IPC-7351 density level B.
- Create a new symbol, and link symbol, footprint and 3D model.
- Search distributor catalogues for a part that is in stock and in budget.

**Theory**
1. What a footprint is: pads, paste, mask, courtyard, fabrication and assembly
   layers — and what each is for.
2. Package families and their names: 0402/0603/0805, SOT-23, SOIC, QFN, LGA.
3. IPC-7351 land patterns, density levels, and courtyard excess.
4. Through-hole: drill size, annular ring, plated vs non-plated.
5. Component selection: availability, lifecycle status, second sources, cost at
   quantity, and reading a distributor's stock page honestly.
6. Library management in KiCad: global vs project libraries, and why a project
   library is what you ship.

**Practical**
- L3.1 Assign footprints to every part in the main project.
- L3.2 Build a footprint for the ESP32-C3-MINI-1 from its datasheet, including
  the RF keep-out.
- L3.3 Build a symbol and footprint for a connector not in the libraries.
- L3.4 Attach 3D models and check mechanical fit in the 3D viewer.
- L3.5 Build a purchasable BOM: part number, distributor, stock, unit cost,
  cost at 10 and at 100.

**Pitfalls addressed:** a footprint that is mirrored; a footprint whose pin 1
is not the datasheet's pin 1; choosing a part that is end-of-life or has no
stock; courtyards that overlap so parts cannot be placed.

---

### Module 4 · PCB layout and routing
**5 h theory + 11 h practical = 16 h**

The core of the course, and the largest module.

**Terminal outcome.** Lay out a two-layer board that is routable, manufacturable
and electrically sound, and prove it with DRC.

**Learning outcomes**
- Define board outline, stack-up and design rules before routing.
- Place components for function, thermals, mechanics and assembly.
- Route with appropriate track widths and clearances; use vias correctly.
- Pour and stitch copper planes; understand return current.
- Route a USB differential pair with controlled spacing.
- Pass DRC with the fabricator's real constraints loaded.

**Theory**
1. Board outline, mounting holes, board edge clearance, mechanical constraints.
2. Stack-up and the design-rules dialog; net classes; the KiCad 10 **graphical
   DRC rule editor**.
3. Track width: current capacity, temperature rise, and IPC-2221 charts.
4. Placement strategy: connectors at edges, decoupling at pins, crystal close
   and quiet, heat spread out, assembly orientation consistent.
5. Routing: why 45° not 90°, why not to route over a plane split, via types and
   when each is used.
6. Ground: solid pour vs hatched, return current paths, stitching vias, and why
   a split ground plane is usually a mistake.
7. Power: trace widths, polygon pours, decoupling placement and loop area.
8. Differential pairs, length tuning, and the basics of impedance — introduced
   here, deepened in Module 6.
9. Silkscreen and assembly drawing: what must be readable after soldering.

**Practical**
- L4.1 Draw the board outline and mounting holes to a mechanical sketch.
- L4.2 Load the fabricator's constraints into the design rules.
- L4.3 Place all components; defend the placement to the group in two minutes.
- L4.4 Route power first, then the USB pair, then signals.
- L4.5 Pour and stitch the ground plane; inspect for isolated islands.
- L4.6 Clear DRC to zero errors.
- L4.7 Tidy the silkscreen; check every reference is visible and nothing sits
  on a pad.
- L4.8 Design review against a checklist, in pairs.

**Pitfalls addressed:** routing before setting rules; a ground pour with
isolated islands nobody noticed; tracks too thin for the current; silkscreen
printed under a component; mounting holes that foul the enclosure; a USB pair
routed as two unrelated signals.

---

### Module 5 · Manufacturing, assembly and bring-up
**2 h theory + 5 h practical = 7 h**

**Terminal outcome.** Produce a manufacturing package a fabricator accepts
without a query, and bring the resulting board up safely.

**Learning outcomes**
- Generate and verify Gerbers, drill files, BOM and centroid.
- Read the fabricator's and assembler's requirements and meet them.
- Place a real order.
- Hand-solder a mixed SMD/through-hole board.
- Bring up an unknown board without destroying it.

**Theory**
1. The manufacturing package: Gerber X2, Excellon drill, IPC-2581, and what
   each file is.
2. Fab notes: stack-up, finish, mask and silkscreen colour, impedance control,
   electrical test.
3. Assembly data: BOM format, centroid/CPL, fiducials, panelisation and
   tooling rails.
4. DFM and DFA: the rules that cost money when broken.
5. Cost drivers: layer count, board size, minimum feature, finish, quantity,
   lead time.

**Practical**
- L5.1 Generate the full output package.
- L5.2 Verify it in an independent Gerber viewer, layer by layer.
- L5.3 Run the fabricator's online DFM check and resolve every flag.
- L5.4 Place the order (instructor-coordinated group order).
- L5.5 Soldering workshop: paste, place, reflow or hot-air; hand-solder the
  through-hole parts; inspect under magnification.
- L5.6 Bring-up: visual inspection, continuity and short checks, current-limited
  first power-up, then programming.

**Pitfalls addressed:** sending the wrong layer set; forgetting the drill file;
a BOM the assembler cannot read; powering a new board at full current with no
limit; assuming the board is dead when it is the USB cable.

---

### Module 6 · Capstone project and where to go next
**2 h theory + 7 h practical = 9 h**

**Terminal outcome.** Complete, present and defend an individual board design;
know what this course did not cover.

**Learning outcomes**
- Take an individual design from requirement to manufacturing package.
- Review someone else's design and give actionable feedback.
- Name the topics that a two-layer, low-speed course necessarily leaves out.

**Theory**
1. Four-layer and multi-layer stack-ups, and when you need one.
2. Signal integrity in one hour: reflections, terminations, controlled
   impedance, and why length matching matters above a certain edge rate.
3. EMC basics: loop area, return paths, common-mode chokes, shielding.
4. Thermal design: copper as a heatsink, thermal vias, derating.
5. Where to go next — and a reading list.

**Practical**
- L6.1 Capstone: an individual board, chosen from a list or proposed by the
  learner and approved. Schematic → layout → DRC → outputs.
- L6.2 Four-layer exercise: restack the main project as a 4-layer board and
  compare the routing effort and the ground integrity.
- L6.3 Length tuning exercise using KiCad 10's tuning tools.
- L6.4 Formal design review, in pairs, against the course checklist.
- L6.5 Presentation: each learner presents their board, its constraints, and
  one thing they would do differently.

**Capstone options** (any one, or a learner proposal)
- A motor-driver carrier for a chosen H-bridge IC
- A 4-channel sensor front end with filtering and an ADC
- A USB-C PD trigger board
- A Raspberry Pi HAT to the mechanical spec
- An LED matrix driver board

---

## 6. Week-by-week session plan

| Week | Sessions | Content | Th | Pr |
|---:|---|---|---:|---:|
| 1 | 1–3 | Module 1 complete. Install, tour, mini-project end to end. | 4 | 4 |
| 2 | 4–6 | Module 2: capture, hierarchy, ERC, peer review. | 4 | 6 |
| 3 | 7–9 | Module 2 close-out; Module 3: footprints, libraries, BOM. | 3 | 7 |
| 4 | 10–12 | Module 4: rules, placement, routing, planes. | 5 | 6 |
| 5 | 13–15 | Module 4 close-out; Module 5: outputs, DFM, **place the order**. | 2 | 8 |
| 6 | 16–18 | Boards arrive: assembly, bring-up, capstone, presentations. | 2 | 9 |
| | | **Total** | **20** | **40** |

**The order must be placed at the end of Week 5.** Everything in Week 6 depends
on physical boards arriving. For a 5–7 day turnaround with an Indian fabricator
this works; if boards are to come from outside India, place the order at the end
of Week 4 using the main project and let the capstone remain unfabricated.

---

## 7. Infrastructure requirements

### Per learner
| Item | Specification |
|---|---|
| Workstation | 8 GB RAM minimum (16 GB recommended), 64-bit, 10 GB free disk, discrete or modern integrated graphics for the 3D viewer |
| OS | Windows 10/11, macOS 13+, or any current Linux |
| Display | 1920×1080 minimum — PCB work is unpleasant below this |
| Mouse | **A real three-button mouse with a scroll wheel.** Not optional; the trackpad workflow is painful. |
| Internet | Required for library downloads, datasheets and ordering |

### Shared lab
| Item | Quantity for a batch of 20 |
|---|---|
| Temperature-controlled soldering station | 5 |
| Hot-air rework station | 2 |
| Stencil + squeegee (per design) | 1 per design |
| Digital multimeter | 5 |
| Bench supply with current limit | 3 |
| USB microscope or magnifier lamp | 5 |
| Tweezers, flux, solder wick, IPA, brushes | 5 sets |
| ESD mats and wrist straps | 20 |

### Consumables and fabrication
- Components for the main project: approximately ₹400–600 per learner
- PCB fabrication, 5 pieces of a 50 × 40 mm 2-layer board: approximately
  ₹1,200–2,500 per design including shipping, depending on fabricator and
  turnaround *(indicative — obtain a current quote before each batch)*
- A single group order of all learners' boards is markedly cheaper than
  twenty individual orders.

### Software
All free: **KiCad 10.0.6** (design), plus an independent Gerber viewer for
verification, and the chosen fabricator's web DFM checker.

---

## 8. Assessment

| Component | Weight | Form |
|---|---:|---|
| Theory examination | 25% | 50 MCQ, 60 minutes, online |
| Continuous practical assessment | 25% | Lab exercises L1.1 – L5.6, assessed against a rubric at the end of each module |
| Main project | 30% | The ESP32-C3 board: schematic quality, layout quality, DRC/ERC clean, manufacturing package correct, board works |
| Capstone and presentation | 20% | Individual design, peer review conducted, and a 5-minute defence |

**Passing:** 50% overall with a minimum of 40% in each component.

**Rubric dimensions** applied to every design artefact — electrical correctness,
manufacturability, readability, completeness of outputs, and whether the learner
can explain their own decisions.

**Certificate:** *Certificate of Completion — PCB Design with KiCad (60 hours)*,
issued on passing, listing the modules covered.

---

## 9. Trainer requirements

| | |
|---|---|
| **Qualification** | B.E./B.Tech or 3-year Diploma in Electronics / ECE / EEE / Instrumentation or allied |
| **Industry experience** | Minimum 2 years in hardware design, with **at least three boards personally taken to fabrication** |
| **Tool proficiency** | Must have designed in KiCad, not only read about it. A trainer who has never had a board come back wrong cannot teach Module 5. |
| **Recommended** | Certified for the job role "Trainer (VET and skills)" (MEP/Q2601) or equivalent as per NCrF |

**Trainer preparation before the first batch:** build the main project end to
end, order it, assemble it, and keep the result as the reference board. Keep
one deliberately *faulty* board as well — a wrong footprint, a missing pull-up
— because the bring-up session is far better taught with a board that does not
work.

---

## 10. Variants

**30-hour compressed version.** Drop Module 6 entirely, reduce the capstone to a
design review of the main project, and shorten Module 4 to two-layer routing
without differential pairs. Keep Module 1's end-to-end mini-project and Module
5's fabrication — removing either removes the point of the course.

**90-hour extended version.** Add: four-layer design as a full module;
controlled impedance and stack-up calculation; flex and rigid-flex; high-speed
digital (DDR-class routing); EMC pre-compliance; KiCad scripting and the Python
API; version control for hardware with Git.

**Sector variants.** The capstone list can be retargeted — power electronics
(gate-drive layout, creepage and clearance), RF (antenna keep-outs, grounded
coplanar waveguide), or industrial (isolation barriers, IEC creepage tables).

---

## 11. Resources

**Primary**
- KiCad official documentation and the Getting Started guide — docs.kicad.org
- *KiCad Like a Pro*, Peter Dalmaris — the standard book, kept current with
  each major KiCad release
- Fabricator capability and DFM pages — the real specification the learner
  designs against

**Standards referenced** (awareness level, not certification)
- IPC-2221 — generic standard on printed board design
- IPC-7351 — land pattern geometries for surface-mount
- IPC-A-610 — acceptability of electronic assemblies

**Practice**
- Recreate an open-hardware board from its schematic and compare your layout
  with the original
- KiCad's own demo projects, which ship with the installation

---

## 12. Open questions for review

1. **Duration.** 60 hours is proposed. Confirm whether the intended slot is 60,
   or whether this should be cut to 40 or extended to 90.
2. **Fabrication budget.** Week 6 only works if boards are actually made. Is
   there a consumables budget, and does it cover a group order?
3. **Lab hardware.** The soldering and bring-up session needs the equipment in
   §7. If the lab does not have it, Module 5 becomes a demonstration rather
   than a practical, and the course loses much of its value.
4. **Certification route.** Is this to be mapped to an existing NOS/QP, or
   issued as a standalone NIELIT short-term certificate?
5. **Main project choice.** The ESP32-C3 board is proposed. A simpler
   alternative (no RF module, no USB differential pair) would reduce risk for a
   first batch; a harder one (four-layer, with a buck converter) would suit
   learners who already have some background.
