# -*- coding: utf-8 -*-
"""Topic 4 deck — 4B: designing combinational and sequential logic using HDL."""
import _boot
from deckkit import *

G = 91440
CMT = RGBColor(0x7F, 0x9C, 0xB5)


def R(t, **kw):
    d = {"t": t, "s": kw.pop("s", 11)}
    d.update(kw)
    return d


def C(t, **kw):
    d = {"t": t}
    d.update(kw)
    return [d]


def build(d):
    # =============================================== SECTION 4B
    d.section_slide("SUBTOPIC 4B", "Designing Combinational and Sequential Logic Using HDL",
                    "From here on, every construct is judged by one question: what hardware "
                    "does it produce?",
                    ["The inference map — code pattern in, hardware out",
                     "Combinational modelling, and the latch you must never infer",
                     "Sequential modelling, blocking vs non-blocking, and the event queue",
                     "Reset strategy, counters, shift registers, edge detection, CDC",
                     "State machines: styles, encodings, safe defaults",
                     "Memories, and pipelining for speed"], accent=GREEN)

    # ============================================================ inference map
    s = d.slide("TOPIC 4B · INFERENCE", "The Inference Map — Learn This Table Cold")
    y = d.lead(s, TOP, [[
        R("Synthesis is pattern matching. ", b=True, c=NAVY, s=12.5),
        R("The tool reads your code, recognises a pattern, and drops in the corresponding "
          "hardware. There is no intelligence in it — which is good news, because it means the "
          "mapping is completely predictable once you know the patterns.")]], h=594360)
    y = d.image(s, y + 45720, "inference_map", 3383280)
    d.card(s, y + G, "The single question to ask of every line you write",
           [[R("\"What does this become?\" ", b=True, c=TEAL),
             R("If you cannot answer that for a line of your own RTL, you have written something "
               "you do not understand, and the tool will make its own choice. Nine times out of "
               "ten that choice is a latch, a huge multiplexer, or a critical path you did not "
               "expect.")]],
           accent=TEAL, h=822960)

    # ============================================================ comb styles
    s = d.slide("TOPIC 4B · COMBINATIONAL", "Three Ways to Write the Same Multiplexer")
    y = d.lead(s, TOP, [[
        R("All three of these synthesise to identical hardware. ", b=True, c=NAVY, s=12.5),
        R("Choose by readability, not by any belief about efficiency — the synthesiser flattens "
          "all of them to the same boolean function before it optimises.")]], h=548640)
    y = d.code(s, y + 45720, [
        C("// Style 1 -- continuous assignment. Best for short expressions.", c=CMT),
        "assign y = sel ? b : a;",
        "",
        C("// Style 2 -- combinational always block with if/else.", c=CMT),
        "always @(*) begin",
        "  if (sel) y = b;",
        "  else     y = a;          // the else is what stops a latch",
        "end",
        "",
        C("// Style 3 -- combinational always block with case. Scales best.", c=CMT),
        "always @(*) begin",
        "  case (sel)",
        "    1'b0:    y = a;",
        "    default: y = b;        // default covers 1'b1, 1'bx and 1'bz",
        "  endcase",
        "end",
    ], size=10, title="Topic4_Lab/rtl/mux2.v uses style 1")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Style 1 for one-liners. Style 3 the moment there are three or more choices — a 4:1 "
          "multiplexer written as nested ternaries is unreadable, and unreadable RTL is where "
          "bugs live.", s=10.5)]])

    # ============================================================ latch
    s = d.slide("TOPIC 4B · LATCHES", "The Accidental Latch — The Number One Beginner Bug", RED)
    y = d.lead(s, TOP, [[
        R("If a combinational block does not assign a variable on EVERY possible path, ",
          b=True, c=NAVY, s=12.5),
        R("the variable must keep its old value when that path is taken. Keeping an old value is "
          "memory, and the only memory the tool can build from a level-sensitive block is a "
          "transparent latch.")]], h=594360)
    y = d.image(s, y + 45720, "latch_inference", 2834640)
    d.cols(s, y + G, [
        ("Why a latch is bad news",
         [[R("· It is transparent while enabled — data flows straight through, so it does not "
             "isolate one cycle from the next.", s=10.5)],
          [R("· Static timing analysis of latch-based paths is far harder; many flows simply "
             "cannot close timing on them.", s=10.5)],
          [R("· It was almost certainly not what you meant.", s=10.5, b=True, c=RED)]],
         RED, CARD_R),
        ("The two cures — use both",
         [[R("1. Default first. ", b=True, c=GREEN, s=10.5),
           R("Assign every output at the top of the block, then override in the branches.",
             s=10.5)],
          [R("2. Complete every branch. ", b=True, c=GREEN, s=10.5),
           R("Every if has an else; every case has a default. Then grep the synthesis log for "
             "the word 'latch' before you go home.", s=10.5)]], GREEN, CARD_G)], h=1325880)

    # ============================================================ latch demo
    s = d.slide("TOPIC 4B · LAB EVIDENCE", "Seeing the Latch in a Real Tool Report")
    y = d.lead(s, TOP, [[
        R("Do not take this on trust — make the tool show you. ", b=True, c=NAVY, s=12.5),
        R("Topic4_Lab/rtl/broken_examples.v contains deliberately wrong modules so you can watch "
          "each failure appear in a synthesis report and then watch it disappear when you fix it.")]],
        h=594360)
    y = d.code(s, y + 45720, [
        C("// bad_latch -- BOTH always blocks are incomplete", c=CMT),
        "always @(*) begin",
        "  if (enable) y = d[0];              // no else            -> LATCH on y",
        "end",
        "always @(*) begin",
        "  case (sel)",
        "    2'b00: w = d[0];",
        "    2'b01: w = d[1];",
        "    2'b10: w = d[2];                 // 2'b11 missing, no default -> LATCH on w",
        "  endcase",
        "end",
    ], size=10, title="rtl/broken_examples.v")
    y = d.code(s, y + G, [
        C("$ yosys -p \"read_verilog rtl/broken_examples.v; synth -top bad_latch; stat\"", c=TEAL),
        "     $_DLATCH_N_    1",
        "     $_DLATCH_P_    1              <-- two latches, exactly as predicted",
    ], size=10, accent=RED, title="Verified output — run this yourself in Lab L1")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Now add the else and the default, re-run, and the two DLATCH lines vanish. That "
          "before-and-after is the exercise; the slide is only the summary.", s=10.5, i=True,
          c=SLATE)]])

    # ============================================================ case to mux
    s = d.slide("TOPIC 4B · DECODE", "case Becomes a Multiplexer — or a Decoder, or an Encoder")
    y = d.lead(s, TOP, [[
        R("One construct, three familiar building blocks. ", b=True, c=NAVY, s=12.5),
        R("Which one you get depends only on what is being selected: data (multiplexer), a "
          "one-hot output (decoder), or a priority (encoder).")]], h=548640)
    y = d.image(s, y + 45720, "case_to_mux", 2743200)
    d.cols(s, y + G, [
        ("Decoder — Topic4_Lab/rtl/decoder3to8.v",
         [[R("always @(*) begin", f=MONO_FONT, s=10)],
          [R("  y = 8'b0;", f=MONO_FONT, s=10)],
          [R("  if (en) y[sel] = 1'b1;", f=MONO_FONT, s=10)],
          [R("end", f=MONO_FONT, s=10)],
          [R("A variable INDEX on the left of an assignment is a decoder. Perfectly legal, "
             "perfectly synthesisable.", s=10, c=SLATE)]], TEAL, CARD),
        ("Priority encoder — rtl/priority_encoder8.v",
         [[R("casez (req)", f=MONO_FONT, s=10)],
          [R("  8'b1???????: {v,y} = {1'b1,3'd7};", f=MONO_FONT, s=10)],
          [R("  8'b01??????: {v,y} = {1'b1,3'd6};", f=MONO_FONT, s=10)],
          [R("  ... default: {v,y} = {1'b0,3'd0};", f=MONO_FONT, s=10)],
          [R("casez, never casex. The valid bit tells you 'no request' apart from 'request 0'.",
             s=10, c=SLATE)]], GREEN, CARD_G)], h=1463040)

    # ============================================================ ALU
    s = d.slide("TOPIC 4B · WORKED EXAMPLE", "An 8-Operation ALU With Real Flags")
    y = d.lead(s, TOP, [[
        R("This is the first design in the lab that is big enough to be interesting. ",
          b=True, c=NAVY, s=12.5),
        R("Note the defaults at the top of the block, the width-(W+1) sum that captures the "
          "carry, and the fact that signed overflow is NOT the same thing as carry.")]], h=594360)
    y = d.code(s, y + 45720, [
        "wire [W:0] sum_ext  = {1'b0, a} + {1'b0, b};   // ONE bit wider -> carry is free",
        "always @(*) begin",
        "  result = {W{1'b0}};  carry = 1'b0;  overflow = 1'b0;   // defaults -> no latch",
        "  case (op)",
        "    OP_ADD: begin",
        "      result   = sum_ext[W-1:0];",
        "      carry    = sum_ext[W];",
        "      overflow = (a[W-1] == b[W-1]) && (result[W-1] != a[W-1]);",
        "    end",
        "    OP_SLT: result = ($signed(a) < $signed(b)) ? {{(W-1){1'b0}},1'b1} : {W{1'b0}};",
        "    ...",
        "    default: begin result = {W{1'b0}}; carry = 1'b0; overflow = 1'b0; end",
        "  endcase",
        "end",
        "assign zero     = ~|result;      // reduction NOR -- one operator, a whole NOR tree",
        "assign negative = result[W-1];",
    ], size=9.5, title="Topic4_Lab/rtl/alu.v (extract)")
    d.card(s, y + G, "The flag that always catches people",
           [[R("Carry is UNSIGNED overflow; V is SIGNED overflow. ", b=True, c=AMBER),
             R("Adding 8'h7F + 8'h01 gives 8'h80: no carry out at all, but a signed overflow "
               "(127 + 1 became −128). Adding 8'hFF + 8'h01 gives 8'h00: carry out set, but no "
               "signed overflow (−1 + 1 = 0 is correct). The lab testbench checks both.")]],
           accent=AMBER, fill=CARD_A, h=868680)

    # ============================================================ seq template
    s = d.slide("TOPIC 4B · SEQUENTIAL", "The Clocked Block — One Template, Used Everywhere")
    y = d.lead(s, TOP, [[
        R("Almost every sequential block you will ever write has this shape. ",
          b=True, c=NAVY, s=12.5),
        R("Learn it as a pattern and type it from muscle memory; then all your attention goes on "
          "the logic instead of the boilerplate.")]], h=548640)
    y = d.image(s, y + 45720, "seq_template", 2560320)
    y = d.code(s, y + G, [
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)      q <= RESET_VALUE;      // asynchronous, active-low reset",
        "  else if (clr)    q <= {W{1'b0}};        // synchronous clear",
        "  else if (load)   q <= din;              // priority order matters:",
        "  else if (en)     q <= next_value;       //   reset > clear > load > enable",
        "end",
    ], size=10, title="The template — priority runs top to bottom")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Everything assigned in this block becomes a flip-flop. Nothing else in the design may "
          "assign ", s=10.5), R("q", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" — one signal, one driving block, no exceptions.", s=10.5)]])

    # ============================================================ blocking
    s = d.slide("TOPIC 4B · = vs <=", "Blocking and Non-Blocking — The Rule and the Reason", RED)
    y = d.lead(s, TOP, [[
        R("The rule is two lines long and you must never break it. ", b=True, c=NAVY, s=12.5),
        R("Inside always @(*) use "), R("=", f=MONO_FONT, b=True, c=GREEN),
        R(". Inside always @(posedge clk) use "), R("<=", f=MONO_FONT, b=True, c=GREEN),
        R(". Never mix the two for the same variable, and never use = in a clocked block.")]],
        h=594360)
    y = d.image(s, y + 45720, "blocking_nonblocking", 3200400)
    d.cols(s, y + G, [
        ("= blocking — happens NOW",
         [[R("The right-hand side is evaluated and the left-hand side updated immediately, before "
             "the next statement runs. In a clocked block that makes the result depend on the "
             "ORDER you typed the statements — which no real flip-flop cares about.", s=10.5)]],
         AMBER, CARD_A),
        ("<= non-blocking — happens at the END",
         [[R("Every right-hand side in the block is sampled first, using the OLD values; only "
             "then are all the left-hand sides updated together. That is exactly what a bank of "
             "flip-flops does at a clock edge, which is why it is the correct operator.",
             s=10.5)]], GREEN, CARD_G)], h=1234440)

    # ============================================================ blocking evidence
    s = d.slide("TOPIC 4B · LAB EVIDENCE", "Two Flip-Flops or One? The Tool Decides")
    y = d.lead(s, TOP, [[
        R("A three-line difference that changes the hardware. ", b=True, c=NAVY, s=12.5),
        R("This is bad_blocking from the lab. Read the two versions, predict the flip-flop count, "
          "then run the synthesiser and see.")]], h=548640)
    y = d.cols(s, y + 45720, [
        ("WRONG — blocking in a clocked block",
         [[R("always @(posedge clk) begin", f=MONO_FONT, s=10)],
          [R("  q1 = d;", f=MONO_FONT, s=10, c=RED, b=True)],
          [R("  q2 = q1;   // q1 is ALREADY d", f=MONO_FONT, s=10, c=RED, b=True)],
          [R("end", f=MONO_FONT, s=10)],
          [R("q2 follows d in the same cycle. Synthesis merges them: ", s=10),
           R("1 flip-flop.", b=True, c=RED, s=10)]], RED, CARD_R),
        ("RIGHT — non-blocking",
         [[R("always @(posedge clk) begin", f=MONO_FONT, s=10)],
          [R("  q1 <= d;", f=MONO_FONT, s=10, c=GREEN, b=True)],
          [R("  q2 <= q1;  // the OLD q1", f=MONO_FONT, s=10, c=GREEN, b=True)],
          [R("end", f=MONO_FONT, s=10)],
          [R("A real two-stage shift register: ", s=10),
           R("2 flip-flops,", b=True, c=GREEN, s=10),
           R(" d delayed by two cycles.", s=10)]], GREEN, CARD_G)], h=1554480)
    y = d.code(s, y + G, [
        C("$ yosys -p \"read_verilog rtl/broken_examples.v; synth -top bad_blocking; stat\"", c=TEAL),
        "     $_DFF_P_       1              <-- ONE flip-flop, not two. Verified.",
    ], size=10, accent=RED)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Change the two = to <= and the same command reports 2. Nothing else in the file "
          "changes. That is how directly the operator maps to silicon.", s=10.5, i=True,
          c=SLATE)]])
    d.cols(s, y + 365760, [
        ("Why the tool is entitled to do that",
         [[R("Blocking assignment says 'update now, before the next statement'. So at the clock "
             "edge q1 takes d, and the very next statement gives q2 the NEW q1 — which is d. The "
             "tool sees two registers holding the same value and keeps one. It is not being "
             "clever; it is obeying the semantics you wrote.", s=10.5)]], AMBER, CARD_A),
        ("And if you swap the two lines?",
         [[R("Write ", s=10.5), R("q2 = q1; q1 = d;", f=MONO_FONT, b=True, c=NAVY, s=10.5),
           R(" and you get two flip-flops and correct behaviour — from the same operator. That is "
             "the real objection to blocking assignment in a clocked block: the hardware depends "
             "on the ORDER you typed the lines, which is not a property real flip-flops have.",
             s=10.5)]], RED, CARD_R)], h=1325880)

    # ============================================================ event queue
    s = d.slide("TOPIC 4B · UNDER THE HOOD", "The Stratified Event Queue — Why <= Actually Works")
    y = d.lead(s, TOP, [[
        R("This is the mechanism, for the students who want to know WHY. ", b=True, c=NAVY,
          s=12.5),
        R("At a single simulation time step the simulator processes events in defined regions, "
          "in order. Non-blocking updates land in a later region than the right-hand-side "
          "evaluations — and that separation is the whole trick.")]], h=594360)
    y = d.image(s, y + 45720, "event_queue", 3383280)
    d.card(s, y + G, "What this buys you",
           [[R("Every clocked block in the design samples its inputs in the Active region using "
               "the values that existed BEFORE the edge, and every register updates in the NBA "
               "region afterwards. So no clocked block can ever see another block's new value "
               "within the same edge — which is precisely the behaviour of real flip-flops, and "
               "why the order in which the simulator happens to visit your always blocks cannot "
               "change the answer. Use = in a clocked block and you throw that guarantee away.")]],
           accent=TEAL, h=1005840)

    # ============================================================ reset
    s = d.slide("TOPIC 4B · RESET", "Synchronous or Asynchronous Reset — Pick One and Be Consistent")
    y = d.lead(s, TOP, [[
        R("Reset is a design decision, not a detail. ", b=True, c=NAVY, s=12.5),
        R("Mixing styles inside one design is how you get a block that comes out of reset two "
          "cycles after its neighbour and starts in an impossible state.")]], h=548640)
    y = d.cols(s, y + 45720, [
        ("Asynchronous reset (used in this lab)",
         [[R("always @(posedge clk or negedge rst_n)", f=MONO_FONT, s=9.5)],
          [R("  if (!rst_n) q <= 1'b0;", f=MONO_FONT, s=9.5)],
          [R("  else        q <= d;", f=MONO_FONT, s=9.5)],
          [R("+ Works with no clock running — safe at power-up.", s=10, c=GREEN)],
          [R("− Release must be synchronised, or flip-flops can come out of reset on different "
             "cycles (and can go metastable).", s=10, c=AMBER)]], GREEN, CARD_G),
        ("Synchronous reset",
         [[R("always @(posedge clk)", f=MONO_FONT, s=9.5)],
          [R("  if (!rst_n) q <= 1'b0;", f=MONO_FONT, s=9.5)],
          [R("  else        q <= d;", f=MONO_FONT, s=9.5)],
          [R("+ One clock domain, easy timing, no release problem.", s=10, c=GREEN)],
          [R("− Needs a running clock; costs logic in front of the D input; a glitch shorter "
             "than a cycle is missed.", s=10, c=AMBER)]], TEAL, CARD)], h=1737360)
    d.card(s, y + G, "Reset-release synchroniser — assert asynchronously, release synchronously",
           [[R("The standard solution: drive the reset tree from two flip-flops clocked by clk "
               "whose asynchronous reset is the raw input. The reset asserts the instant the "
               "signal falls, and releases cleanly on a clock edge two cycles later. Every "
               "serious design does this; it costs two flip-flops.")]],
           accent=AMBER, fill=CARD_A, h=822960)

    # ============================================================ counter
    s = d.slide("TOPIC 4B · COUNTERS", "A Counter Is a Register Plus an Incrementer")
    y = d.lead(s, TOP, [[
        R("Counters are the workhorse of sequential design — timers, address generators, "
          "dividers, bit counters in a UART. ", b=True, c=NAVY, s=12.5),
        R("The lab counter is parameterised, up/down, loadable and has a terminal count.")]],
        h=594360)
    y = d.code(s, y + 45720, [
        "assign tc = en & (up ? (q == MAX[W-1:0]) : (q == {W{1'b0}}));",
        "",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)      q <= {W{1'b0}};",
        "  else if (load)   q <= din;",
        "  else if (en) begin",
        "    if (up)  q <= (q == MAX[W-1:0]) ? {W{1'b0}}  : q + 1'b1;",
        "    else     q <= (q == {W{1'b0}})  ? MAX[W-1:0] : q - 1'b1;",
        "  end",
        "end",
    ], size=10, title="Topic4_Lab/rtl/counter.v — W=4, MAX=15")
    y = d.code(s, y + G, [
        C("$ yosys -p \"read_verilog rtl/counter.v; synth -top counter; stat\"", c=TEAL),
        "   Number of cells:  38        $_DFF_NP0_  4     <-- 4 bits of state, as expected",
    ], size=10, accent=GREEN)
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Set MAX = 9 and you have a BCD decade counter with no other change — that is what "
          "parameterisation buys. Chain two of them with ", s=10.5),
        R("tc", f=MONO_FONT, b=True, c=NAVY, s=10.5),
        R(" as the enable of the next and you have a 0–99 counter.", s=10.5)]])

    # ============================================================ shift / edge
    s = d.slide("TOPIC 4B · SMALL, ESSENTIAL BLOCKS", "Shift Register and Edge Detector")
    y = d.lead(s, TOP, [[
        R("Two tiny modules that appear in almost every design you will ever build. ",
          b=True, c=NAVY, s=12.5),
        R("The edge detector in particular is the standard way to turn a level into a "
          "single-cycle pulse.")]], h=548640)
    y = d.cols(s, y + 45720, [
        ("Shift register — the concatenation idiom",
         [[R("always @(posedge clk or negedge rst_n)", f=MONO_FONT, s=9.5)],
          [R("  if (!rst_n) q <= {W{1'b0}};", f=MONO_FONT, s=9.5)],
          [R("  else if (en) q <= {q[W-2:0], sin};", f=MONO_FONT, s=9.5)],
          [R("One line shifts the whole register left and inserts the new bit. Reverse the "
             "concatenation for a right shift. This idiom builds serialisers, deserialisers, CRC "
             "engines and LFSRs.", s=10, c=SLATE)]], TEAL, CARD),
        ("Edge detector — one register and a gate",
         [[R("always @(posedge clk or negedge rst_n)", f=MONO_FONT, s=9.5)],
          [R("  if (!rst_n) sig_d <= 1'b0; else sig_d <= sig;", f=MONO_FONT, s=9.5)],
          [R("assign rise = sig & ~sig_d;", f=MONO_FONT, s=9.5, c=GREEN, b=True)],
          [R("assign fall = ~sig & sig_d;", f=MONO_FONT, s=9.5, c=GREEN, b=True)],
          [R("Remember what the signal was last cycle; compare. rise is high for exactly one "
             "clock cycle.", s=10, c=SLATE)]], GREEN, CARD_G)], h=1737360)
    d.card(s, y + G, "A testbench lesson from building this lab",
           [[R("The first edge-detector test failed. The cause was not the design — the "
               "testbench changed the input in the middle of a clock cycle, so the pulse was half "
               "a cycle wide and the check sampled it at the wrong moment. ", b=True, c=AMBER),
             R("Drive your stimulus just AFTER the active clock edge, and sample just BEFORE the "
               "next one. Half of all 'the design is broken' reports are really this.")]],
           accent=AMBER, fill=CARD_A, h=1005840)

    # ============================================================ CDC
    s = d.slide("TOPIC 4B · CROSSING CLOCKS", "Metastability and the Two-Flop Synchroniser", RED)
    y = d.lead(s, TOP, [[
        R("A flip-flop needs its D input stable for a setup time before the edge and a hold time "
          "after it. ", b=True, c=NAVY, s=12.5),
        R("A signal from another clock domain cannot honour that, so the flip-flop can enter a "
          "metastable state — an output that is neither 0 nor 1 and settles at an unpredictable "
          "moment. You cannot prevent this. You can only give it time to decay.")]], h=685800)
    y = d.code(s, y + 45720, [
        "reg [1:0] sync;",
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n) sync <= 2'b00;",
        "  else        sync <= {sync[0], async_in};   // stage 0 may go metastable ...",
        "end",
        "assign sync_out = sync[1];                   // ... stage 1 has a whole cycle to settle",
    ], size=10, title="Topic4_Lab/rtl/synchroniser.v")
    d.cols(s, y + G, [
        ("Rules for crossing a clock domain",
         [[R("· Two flip-flops minimum for a single-bit LEVEL. Three at very high clock rates.",
             s=10.5)],
          [R("· Never synchronise a multi-bit bus bit by bit — the bits will arrive on different "
             "cycles and you will read a value that never existed.", s=10.5, c=RED, b=True)]],
         RED, CARD_R),
        ("What to do instead for buses",
         [[R("· Gray-coded pointers (that is how an asynchronous FIFO works — only one bit "
             "changes per step, so a mis-sample gives the previous value, which is safe).",
             s=10.5)],
          [R("· Or a request/acknowledge handshake with the data held stable throughout.",
             s=10.5)]], GREEN, CARD_G)], h=1097280)

    # ============================================================ FSM styles
    s = d.slide("TOPIC 4B · STATE MACHINES", "Three Coding Styles — Use the Three-Block Style")
    y = d.lead(s, TOP, [[
        R("A finite state machine is a state register, next-state logic and output logic. ",
          b=True, c=NAVY, s=12.5),
        R("How many always blocks you split those across is a style choice — and it matters more "
          "than students expect.")]], h=548640)
    y = d.image(s, y + 45720, "fsm_styles", 3200400)
    d.table(s, y + G,
            ["Style", "Blocks", "Pros", "Cons"],
            [["One-block", "1 clocked", "Compact; outputs are registered automatically",
              "Next-state and output logic tangled; hard to read"],
             ["Two-block", "1 clocked + 1 comb", "Clear separation of state and logic",
              "Outputs still mixed into the combinational block"],
             ["Three-block", "1 clocked + 2 comb", "State, next-state and outputs each separate",
              "Slightly more typing — that is the whole cost"]],
            [1737360, 2011680, 3657600, 3840480], rh=329184, bold_cols=(0,), size=9.5,
            col_colors={0: NAVY})

    # ============================================================ FSM worked
    s = d.slide("TOPIC 4B · FSM WORKED EXAMPLE", "A Traffic-Light Controller, Three Blocks")
    y = d.code(s, TOP, [
        C("// ---- BLOCK 1 : state register (and the dwell timer) ----", c=CMT),
        "always @(posedge clk or negedge rst_n) begin",
        "  if (!rst_n)       begin state <= MAIN_GREEN; timer <= 8'd0; end",
        "  else if (tick)    begin",
        "    if (done)       begin state <= next; timer <= 8'd0; end",
        "    else                  timer <= timer + 1'b1;",
        "  end",
        "end",
        C("// ---- BLOCK 2 : next-state logic (pure combinational) ----", c=CMT),
        "always @(*) begin",
        "  next = state;                       // default -> no latch, and a safe self-loop",
        "  case (state)",
        "    MAIN_GREEN : next = MAIN_YELLOW;",
        "    MAIN_YELLOW: next = SIDE_GREEN;",
        "    SIDE_GREEN : next = SIDE_YELLOW;",
        "    SIDE_YELLOW: next = MAIN_GREEN;",
        "    default    : next = MAIN_GREEN;   // SAFE FSM -- recover from an illegal state",
        "  endcase",
        "end",
        C("// ---- BLOCK 3 : output logic (Moore -- depends on state ONLY) ----", c=CMT),
        "always @(*) begin",
        "  main_light = RED;  side_light = RED;              // defaults",
        "  case (state)",
        "    MAIN_GREEN : begin main_light = GREEN;  side_light = RED;    end",
        "    ...",
        "  endcase",
        "end",
    ], size=8.5, title="Topic4_Lab/rtl/traffic_fsm.v — verified: 52 cells, 12 flip-flops")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Twelve flip-flops: eight for the timer and FOUR for the state — Yosys re-encoded "
          "the 2-bit state to one-hot by itself. Predict, then check the log.",
          s=10.5, i=True, c=SLATE)]])

    # ============================================================ FSM encoding
    s = d.slide("TOPIC 4B · FSM ENCODING", "Binary or One-Hot — and How to Ask for It")
    y = d.lead(s, TOP, [[
        R("The state names in your code are symbols; the tool chooses the bit pattern. ",
          b=True, c=NAVY, s=12.5),
        R("Binary uses the fewest flip-flops; one-hot uses one flip-flop per state but makes the "
          "next-state and output logic trivially shallow — which on an FPGA, where flip-flops are "
          "free and logic depth is not, is usually the faster choice.")]], h=685800)
    y = d.code(s, y + 45720, [
        "(* fsm_encoding = \"one-hot\" *) reg [1:0] state, next;    // or \"binary\"",
        "",
        C("// Verified with Yosys 0.33 on a 4-state FSM, after abc -g AND,OR,XOR,NAND,NOR:", c=CMT),
        "//   binary   :  9 cells,  2 flip-flops",
        "//   one-hot  :  9 cells,  4 flip-flops     <-- more FFs, shallower next-state logic",
        "",
        C("// And Yosys chose one-hot BY ITSELF for traffic_fsm -- read the log:", c=CMT),
        "//   FSM_RECODE: mapping auto encoding to `one-hot` for this FSM",
    ], size=9.5, title="Requesting an encoding with an attribute")
    d.cols(s, y + G, [
        ("Always write a safe default",
         [[R("With one-hot, N states use 2^N possible patterns — the vast majority illegal. A "
             "single upset bit puts the machine somewhere it can never leave. ", s=10.5),
           R("default: next = IDLE;", f=MONO_FONT, b=True, c=GREEN, s=10.5),
           R(" costs nothing and guarantees recovery.", s=10.5)]], GREEN, CARD_G),
        ("A note from building this lab",
         [[R("On this 4-state machine the two encodings tie on cell count — the advantage of "
             "one-hot only appears when the state count grows and the next-state decode would "
             "otherwise get deep. ", s=10.5),
           R("Do not assume; measure.", b=True, c=NAVY, s=10.5),
           R(" And read the log: the tool may already have re-encoded your FSM without being "
             "asked, which is exactly what happened to traffic_fsm above.", s=10.5)]],
         AMBER, CARD_A)], h=1325880)

    # ============================================================ Moore vs Mealy
    s = d.slide("TOPIC 4B · MOORE vs MEALY", "Where the Output Comes From Changes the Timing")
    y = d.lead(s, TOP, [[
        R("Moore outputs depend on the state alone; Mealy outputs depend on the state AND the "
          "current inputs. ", b=True, c=NAVY, s=12.5),
        R("A Mealy machine reacts one cycle sooner and often needs fewer states — but its output "
          "is combinational from an input, so it can glitch and it lands on the wrong side of a "
          "timing path.")]], h=685800)
    y = d.table(s, y + 45720,
                ["", "Moore", "Mealy"],
                [["Output is a function of", "state only", "state and inputs"],
                 ["Reacts to an input", "one clock later", "in the same cycle"],
                 ["Output glitches?", "no — it is registered", "yes — it follows the input"],
                 ["Typical state count", "more", "fewer"],
                 ["Safe to drive off-chip?", "yes", "not without registering it"],
                 ["Use it when", "you want clean, predictable outputs",
                  "you need the earliest possible response"]],
                [3200400, 4023360, 4023360], rh=283464, bold_cols=(0,), size=10,
                col_colors={0: NAVY})
    d.card(s, y + G, "Lab L3 — build the same 1011 sequence detector both ways",
           [[R("Topic4_Lab/rtl/seq_detect_1011.v implements both in one module so you can watch "
               "the two "), R("found", f=MONO_FONT, b=True, c=NAVY),
             R(" outputs on the same waveform. The Mealy output pulses on the clock edge where "
               "the final 1 arrives; the Moore output pulses one cycle later. Overlapping "
               "detection is handled by returning to the correct partial-match state rather than "
               "to IDLE — 1011011 contains two matches, not one.")]],
           accent=TEAL, h=1051560)

    # ============================================================ memory
    s = d.slide("TOPIC 4B · MEMORY", "Inferring RAM — Write It the Way the Tool Expects")
    y = d.lead(s, TOP, [[
        R("You do not instantiate a RAM; you write a pattern the tool recognises. ",
          b=True, c=NAVY, s=12.5),
        R("Get the pattern right and you get a dedicated block RAM. Get it slightly wrong and you "
          "get thousands of flip-flops, or a design that will not fit at all.")]], h=594360)
    y = d.image(s, y + 45720, "memory_inference", 2743200)
    y = d.code(s, y + G, [
        "reg [W-1:0] mem [0:DEPTH-1];",
        "always @(posedge clk) begin",
        "  if (we) mem[waddr] <= wdata;",
        "  rdata <= mem[raddr];         // REGISTERED read -- this is what infers block RAM",
        "end",
    ], size=10, title="Topic4_Lab/rtl/sync_ram.v — synchronous read")
    d.text(s, ML, y + 45720, MW, 274320, [[
        R("Write ", s=10.5), R("assign rdata = mem[raddr];", f=MONO_FONT, b=True, c=RED, s=10.5),
        R(" instead — an asynchronous read — and no FPGA block RAM can implement it, so the tool "
          "builds the whole array out of registers and multiplexers. Same intent, wildly "
          "different silicon.", s=10.5)]])

    # ============================================================ pipelining
    s = d.slide("TOPIC 4B · SPEED", "Pipelining — Trading Latency for Throughput")
    y = d.lead(s, TOP, [[
        R("The clock period must be longer than the slowest combinational path between two "
          "flip-flops. ", b=True, c=NAVY, s=12.5),
        R("If that path is too slow, cut it in half with a register in the middle. You now need "
          "two cycles to get an answer — but you can start a new one every cycle.")]], h=594360)
    y = d.image(s, y + 45720, "pipelining", 3200400)
    d.cols(s, y + G, [
        ("What you gain and what you pay",
         [[R("+ Throughput: one result per clock, at a much higher clock.", s=10.5, c=GREEN)],
          [R("− Latency: the first result arrives N cycles later.", s=10.5, c=AMBER)],
          [R("− Area: the pipeline registers, and any control signal that must now be delayed to "
             "stay aligned with its data.", s=10.5, c=AMBER)]], TEAL, CARD),
        ("The trap",
         [[R("Every signal travelling alongside the data must be delayed by the SAME number of "
             "stages. ", b=True, c=RED, s=10.5),
           R("Pipeline the datapath and forget the valid bit, and your results arrive correctly "
             "but are marked valid two cycles early. Carry valid, and any tag or address, through "
             "the identical register chain.", s=10.5)]], RED, CARD_R)], h=1234440)

    # ============================================================ 4B checkpoint
    s = d.slide("TOPIC 4B · CHECKPOINT", "Predict the Hardware — Eight Snippets")
    d.lead(s, TOP, [[
        R("Show each snippet, ask 'what does the tool build?', then run it. ", b=True, c=NAVY,
          s=12.5),
        R("Full answers and the synthesis reports are in workbook section T4-B.")]], h=411480)
    y = d.table(s, 1554480,
                ["#", "Snippet", "What does synthesis produce?"],
                [["1", "assign y = sel ? b : a;", "One W-bit 2:1 multiplexer, no state"],
                 ["2", "always @(*) if (en) y = d;", "A transparent latch on y"],
                 ["3", "always @(posedge clk) q1 = d; q2 = q1;", "ONE flip-flop (verified above)"],
                 ["4", "always @(posedge clk) q <= {q[6:0], sin};", "An 8-bit shift register"],
                 ["5", "for (i=0;i<8;i=i+1) s = s + d[i];", "An adder tree — eight adders, unrolled"],
                 ["6", "assign z = ~|result;", "A NOR reduction tree — the zero flag"],
                 ["7", "rdata <= mem[raddr]; inside a clocked block", "A block RAM with registered read"],
                 ["8", "casex (sel) with an x in sel", "Simulation/synthesis mismatch — banned"]],
                [548640, 5303520, 5394960], rh=283464, bold_cols=(0,), size=9.5,
                col_colors={0: NAVY})
    d.card(s, y + G, "The habit this checkpoint is building",
           [[R("Predict, then verify. ", b=True, c=TEAL),
             R("A designer who can look at a page of RTL and describe the netlist before running "
               "the tool will catch problems in review, in minutes. A designer who cannot will "
               "find them in the lab, in days — or on the silicon, in months.")]],
           accent=TEAL, h=822960)
