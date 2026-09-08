# ESD Workstation — Technical Specifications

Procurement / tender specification for Electrostatic Discharge (ESD) protected
workstations for electronics and chip-design laboratories.

**Governing standards:** ANSI/ESD S20.20-2021 (ESD control program), IEC 61340-5-1,
ANSI/ESD S4.1 (worksurfaces), ANSI/ESD S6.1 (grounding), ANSI/ESD S1.1 (wrist straps),
ANSI/ESD STM3.1 (ionization), ANSI/ESD STM7.1 (flooring), ANSI/ESD STM12.1 (chairs).

> **Important:** ESD standards specify *electrical* performance (resistance, decay time,
> body-voltage generation). They do **not** specify sheet gauge, height, or colour.
> Those are mechanical/ergonomic and workmanship items that the buyer must state in the
> tender. The values below are the accepted industry/lab-furniture practice recommended
> for this specification.

---

## 1. Gauge of the metal base / frame

Material: **CRCA (Cold Rolled Close Annealed) MS steel**, IS 513 grade, powder coated.

| Member | Recommended thickness | Gauge (SWG) | Minimum acceptable |
|---|---|---|---|
| Vertical uprights / legs (load bearing) | **1.6 mm** | 16 SWG | 1.5 mm |
| Horizontal cross members, beams, aprons | **1.6 mm** | 16 SWG | 1.2 mm (18 SWG) |
| Overhead shelf, back/side panels, drawer bodies | **0.8 – 1.0 mm** | 20 – 22 SWG | 0.8 mm |
| Cable trays, trunking, covers | **0.8 mm** | 20 SWG | 0.7 mm |
| Base / foot plates under levelling bolts | **3 – 5 mm** MS plate | — | 3 mm |

**Recommended single-line tender wording:**
"Workstation frame fabricated from CRCA steel — legs and load-bearing members not less
than 1.6 mm (16 SWG), panels and shelves not less than 0.8 mm (20 SWG) — with 3 mm MS
base plates, duly powder coated."

Notes:
- Quote gauge as **SWG with the mm value in brackets**; SWG, US Standard and BWG gauge
  numbers are not identical, and mm is what is actually measurable at inspection.
- Sections: legs typically 50 × 50 mm or 60 × 60 mm square tube; beams 40 × 40 mm.
- **Load rating:** uniformly distributed load of **200 kg minimum** (300 kg preferred for
  instrument-loaded benches) with permanent deformation nil and deflection ≤ 3 mm at
  rated load.
- **Finish:** epoxy-polyester powder coating, **50 – 80 micron DFT**, after 7-tank
  pre-treatment (degrease, derust, phosphate, passivate). ESD-safe (dissipative) powder
  coat, surface resistance < 1 × 10⁹ Ω, is preferred; plain powder coat is acceptable only
  if all coated surfaces are outside the operator's touch zone.
- **All-welded frame**, welds ground smooth; no sharp edges. Adjustable levelling bolts
  (± 25 mm) at each leg.
- Every steel member must be **electrically continuous** and bonded to the ESD ground bus
  — resistance between any two frame points ≤ 1.0 Ω.

---

## 2. Complete height of the ESD workstation

| Dimension | Recommended value |
|---|---|
| **Worktop (working) height** | **750 mm ± 10 mm** (fixed) — or **700 – 900 mm** if height-adjustable |
| **Overall height — standard bench** (worktop + one overhead shelf + task light) | **1500 mm** |
| **Overall height — with full upright back panel / instrument rack** | **1800 mm** |
| Clear knee space under worktop | ≥ 650 mm high × ≥ 600 mm deep |
| Clearance from worktop to underside of overhead shelf | 450 – 500 mm |
| Worktop depth | **750 mm** (600 mm minimum) |
| Worktop width (per seat) | **1200 / 1500 / 1800 mm** — 1500 mm recommended |
| Overhead shelf depth | 300 mm |

**Recommended single-line tender wording:**
"Worktop height 750 mm from finished floor level; overall height of workstation 1500 mm
including overhead shelf and task light (1800 mm where a full-height back panel with
instrument rack is specified). Levelling bolts to provide ± 25 mm adjustment."

Notes:
- **750 mm** is the standard Indian/ISO seated desk height and suits an ESD chair with a
  450 – 600 mm adjustable seat.
- Prefer **height-adjustable** benches (manual crank or electric, 700 – 900 mm; 650 –
  1250 mm for sit-stand) where the lab is shared by many users — it is the single biggest
  ergonomic improvement and is now standard in electronics labs.
- Overall height must not exceed **1800 mm**, so that the top shelf stays within reach and
  does not obstruct sightlines, lighting or fire sprinklers.

---

## 3. Colour of the ESD mat

**Blue.**

The industry-conventional table mat is a **two-layer / three-layer rubber mat with a
matte blue static-dissipative top layer over a black conductive bottom layer.**

| Item | Colour | Notes |
|---|---|---|
| Table (worksurface) mat | **Blue** (sky/royal blue) — matte finish | Grey and green are acceptable alternatives |
| Bottom (conductive) layer | Black | Provides the low-resistance path to the ground stud |
| Floor mat / ESD floor covering | Grey or black | Hides scuffing; blue also used |
| EPA boundary marking tape | Yellow/black or green/white | For demarcating the ESD Protected Area |

Notes:
- **Colour is a convention, not a standard requirement.** No ESD standard mandates a
  colour. Blue is specified because it is the universal visual cue for "this is an ESD
  surface", it contrasts well with components and PCBs, and it is what is stocked.
- Specify a **matte / anti-glare** surface — glossy mats cause reflected glare under
  task lighting and inspection lamps.
- What *must* be specified is the electrical performance (see §4.1), not the colour.
  Do not accept a blue mat that fails the resistance test.

---

## 4. Other required specifications

### 4.1 ESD worksurface / table mat — electrical
- Two- or three-layer rubber mat, **2 mm thick** (3 mm for heavy-duty), heat and solder
  resistant, oil resistant.
- **Point-to-point resistance (Rtt): 1 × 10⁶ to 1 × 10⁹ Ω**
- **Resistance to groundable point (Rtg): 1 × 10⁶ to < 1 × 10⁹ Ω** (per ANSI/ESD S4.1)
- **Static decay:** 5000 V → < 50 V in **< 2 s** (FTMS 101C Method 4046); < 0.1 s preferred.
- **Triboelectric charge generation < 100 V.**
- Mat to be fitted with **two 10 mm press studs** and grounded via a cord containing a
  **1 MΩ ± 10% current-limiting resistor**.
- Worktop substrate: 25 mm pre-laminated board / MDF or 18 mm ply, with **ESD laminate
  (1.0 mm)** on top, 2 mm PVC edge banding; or 1.0 mm ESD laminate over a steel top.

### 4.2 Grounding (the single most important item)
- **Common Point Ground (CPG)** bar/stud on each bench, clearly marked with the ESD symbol.
- Dedicated **ESD ground bus** (copper strip or ≥ 2.5 mm² green/yellow insulated conductor)
  running the length of the bench row to the earth pit.
- **Resistance from the CPG to the equipment grounding conductor / earth ≤ 1.0 Ω**
  (ANSI/ESD S6.1). Earth pit resistance ≤ 1 Ω for a dedicated clean earth (≤ 5 Ω acceptable
  where a dedicated instrument earth is not available).
- **Minimum two ground sockets per operator position** (one for the mat, one for the wrist
  strap) plus one for the chair/trolley.
- Never bond the ESD ground to the neutral; use the protective earth or a dedicated ESD earth.

### 4.3 Personnel grounding
- **Wrist strap:** adjustable, metal-backed or conductive fabric, with coiled cord
  containing a **1 MΩ ± 10%** resistor; total person-to-ground resistance **< 3.5 × 10⁷ Ω**
  (ANSI/ESD S1.1). One per seat, plus 20% spares.
- **Wrist strap tester** — wall/bench mounted, at the entry to the EPA; daily test logged.
  Constant/continuous monitors optional but recommended for critical benches.
- **ESD footwear or heel/toe straps** and a **footwear tester** where the lab has ESD
  flooring and standing operations.
- **ESD smocks/coats** (surface resistance 1 × 10⁵ – 1 × 10¹¹ Ω per ANSI/ESD STM2.1),
  ESD gloves / finger cots.

### 4.4 ESD chair
- Conforming to **ANSI/ESD STM12.1**; resistance seat-to-floor **1 × 10⁴ – 1 × 10⁹ Ω**.
- Conductive PU or ESD fabric upholstery, **conductive castors** and a **drag chain**.
- Seat height adjustable **450 – 600 mm**, gas lift, backrest with lumbar support,
  footring for high benches.

### 4.5 Flooring
- ESD vinyl / epoxy floor or ESD floor mat within the EPA.
- **Resistance to ground 1 × 10⁶ – 1 × 10⁹ Ω** (ANSI/ESD STM7.1); system test with
  footwear: **body voltage generation < 100 V** (ANSI/ESD STM97.2).

### 4.6 Ionizer (mandatory where insulators cannot be eliminated)
- Bench-top or overhead bar ionizer per **ANSI/ESD STM3.1**.
- **Offset (balance) voltage ≤ ± 35 V**; discharge time **1000 V → 100 V in ≤ 20 s** at the
  work position. Verified every 6 months; balance checked periodically with a charged
  plate monitor.

### 4.7 Electrical and services on the bench
- **6 – 8 nos. 5/15 A universal sockets** per bench in a trunking mounted ~200 mm above
  the worktop, each circuit protected by an **MCB**, with a **30 mA RCCB** on the board.
- Separate **UPS (raw power) and mains** circuits, clearly labelled and differently
  coloured.
- Earth continuity from every socket earth pin to the ESD ground bus.
- Cable management trays/spine under the worktop; no trailing cables across the worktop.
- Optional: compressed-air point, LAN/RJ45 points (2 per seat), USB charging.

### 4.8 Lighting
- Task light on the overhead shelf, LED, **500 – 750 lux at the worktop**
  (750 – 1000 lux for fine assembly/inspection work), glare-free, > 80 CRI.
- Magnifier lamp with ESD-safe body where fine rework is done.

### 4.9 Environment
- Temperature **22 ± 3 °C**; **relative humidity 40 – 60 % RH** (30 – 70 % acceptable).
  Low RH dramatically increases triboelectric charging — humidity control is part of the
  ESD control programme, not an optional comfort item.

### 4.10 Storage and accessories
- ESD-safe storage bins, trays, component drawers, tote boxes, shielding/moisture-barrier
  bags, ESD trolleys — all dissipative, all bonded where mobile.
- ESD-safe hand tools, solder station with grounded tip (**tip-to-ground < 2 Ω**,
  tip leakage < 2 mV), ESD-safe brushes, vacuum/blower.
- **Strictly excluded from the EPA:** ordinary plastic bags, thermocol/polystyrene,
  cellophane tape, common vinyl binders, styrofoam cups, non-ESD chairs and mats.

### 4.11 Marking, testing and documentation
- **ESD Protected Area (EPA)** signage at every entrance; ESD symbol on each bench and
  ground point; floor demarcation tape.
- Test and audit instruments to be supplied with the workstations:
  - **Surface resistance meter** (megohmmeter with 2.27 kg concentric-ring electrodes,
    100 V / 500 V test voltage) — ANSI/ESD STM11.11 / S4.1
  - Wrist strap tester, footwear tester
  - Static field meter (electrostatic voltmeter), charged plate monitor (for ionizers)
- **Compliance verification plan** per ANSI/ESD S20.20 clause 7.4: documented periodic
  test schedule, test records, and a nominated ESD coordinator.
- Vendor to submit **factory test reports / type test certificates** for the mats, chairs
  and flooring, plus a **site test report** after installation.

### 4.12 Warranty and installation
- Minimum **1 year** comprehensive warranty on the workstation (3 years on the frame);
  mats and consumables as per manufacturer.
- Supply, installation, earthing, commissioning and **on-site handover testing** in the
  scope of the vendor.
- Training of lab staff on ESD control practice and daily testing procedure.

---

## 5. Quick acceptance checklist

| # | Item | Acceptance criterion |
|---|---|---|
| 1 | Frame steel thickness | Legs/beams ≥ 1.6 mm; panels ≥ 0.8 mm (verify with a micrometer) |
| 2 | Powder coat DFT | 50 – 80 micron (verify with a coating thickness gauge) |
| 3 | Worktop height | 750 mm ± 10 mm |
| 4 | Overall height | 1500 mm (1800 mm with back panel) |
| 5 | Load test | 200 kg UDL, deflection ≤ 3 mm, no permanent set |
| 6 | Mat colour/finish | Blue, matte, 2 mm, two-layer |
| 7 | Mat Rtg | 1 × 10⁶ – < 1 × 10⁹ Ω |
| 8 | Mat Rtt | 1 × 10⁶ – 1 × 10⁹ Ω |
| 9 | CPG to earth | ≤ 1.0 Ω |
| 10 | Wrist strap path | < 3.5 × 10⁷ Ω, 1 MΩ resistor present |
| 11 | Chair | 1 × 10⁴ – 1 × 10⁹ Ω seat to floor |
| 12 | Ionizer balance | ≤ ± 35 V, decay ≤ 20 s |
| 13 | Illumination | ≥ 500 lux at worktop |
| 14 | Humidity | 40 – 60 % RH maintained |
