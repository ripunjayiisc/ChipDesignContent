# -*- coding: utf-8 -*-
"""Layout helpers for the Lecture 01 panels.

The one rule these enforce: text is wrapped to a WIDTH IN PANEL UNITS, not to a
guessed character count, and every card sizes itself to the text it ends up
holding. That is what stops the overflow that the readability budget in dsl.py
warns about.
"""
import textwrap
from dsl import *

# A panel is PW inches mapped onto 100 units, so one unit is PW/100 inches,
# i.e. 72*PW/100 points. The em-factor below was MEASURED, not guessed: render
# a sample string at 9-12pt, read its extent back through ax.transData, and the
# average width per character comes out at 0.62 em. 0.635 leaves a little room.
_PT_PER_UNIT = 72.0 * PW / 100.0
_EM = 0.635


def chars_for(width_units, size):
    """How many characters of `size`-pt text fit across `width_units`."""
    return max(4, int(width_units * _PT_PER_UNIT / (_EM * size)))


def wrap(ax, x, y, width_units, text, size=None, color=BODY, lh=None,
         ha="left", weight="normal", style="normal"):
    """Wrapped text. Returns the y of the LAST line."""
    size = FS_SMALL if size is None else size
    lh = (size * 0.26) if lh is None else lh
    lines = textwrap.wrap(text, chars_for(width_units, size))
    for i, ln in enumerate(lines):
        ax.text(x, y - i * lh, ln, ha=ha, va="center", fontsize=size,
                color=color, fontweight=weight, fontstyle=style)
    return y - (len(lines) - 1) * lh


def wrapped_height(width_units, text, size=None, lh=None):
    size = FS_SMALL if size is None else size
    lh = (size * 0.26) if lh is None else lh
    return lh * len(textwrap.wrap(text, chars_for(width_units, size)))


def note(ax, x, y_top, w, head, text, col=NAVY, fill=LIGHT, size=None,
         head_size=None, pad=2.6):
    """A card that sizes itself to its wrapped text. Returns its bottom y."""
    size = FS_SMALL if size is None else size
    head_size = FS_BODY if head_size is None else head_size
    lh = size * 0.26
    hlh = head_size * 0.28
    inner = w - 2 * pad
    hh = wrapped_height(inner, head, head_size, hlh) if head else 0.0
    h = 2.6 + (hh + 1.2 if head else 0.0) + wrapped_height(inner, text, size, lh) + 1.4
    box(ax, x, y_top - h, w, h, fc=fill, ec=col, lw=1.6)
    yy = y_top - 3.0
    if head:
        yy = wrap(ax, x + pad, yy, inner, head, head_size, color=col,
                  lh=hlh, weight="bold") - (lh + 1.2)
    wrap(ax, x + pad, yy, inner, text, size, lh=lh)
    return y_top - h


def column_cards(ax, x0, y_top, total_w, specs, gap=1.8, head_h=4.4,
                 body_size=None, pad=1.9, min_h=0.0):
    """Equal-width cards side by side, all as tall as the tallest text.

    specs: list of (heading, body, colour) — or (heading, body, colour, note).
    Returns the bottom y.
    """
    body_size = (FS_SMALL - 1.0) if body_size is None else body_size
    lh = body_size * 0.26
    n = len(specs)
    w = (total_w - gap * (n - 1)) / n
    inner = w - 2 * pad
    bodies = [sp[1] for sp in specs]
    tallest = max(wrapped_height(inner, b, body_size, lh) for b in bodies)
    h = max(min_h, head_h + 2.2 + tallest + 1.8)
    x = x0
    for sp in specs:
        head, body, col = sp[0], sp[1], sp[2]
        box(ax, x, y_top - h, w, h, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, y_top - head_h, w, head_h, fc=col, ec=col, lw=1.0)
        ax.text(x + w / 2, y_top - head_h / 2, head, ha="center", va="center",
                fontsize=FS_SMALL - 0.5, color=WHITE, fontweight="bold",
                linespacing=1.5)
        wrap(ax, x + pad, y_top - head_h - 2.2, inner, body, body_size, lh=lh)
        x += w + gap
    return y_top - h


def rowcards(ax, x, y_top, w, rows, rh=None, body_size=None, bar=1.3, gap=1.0,
             pad=3.4):
    """Stacked cards, each with a coloured left bar, a heading and a body.

    rows: list of (heading, body, colour). Returns the bottom y.
    """
    body_size = (FS_SMALL - 1.0) if body_size is None else body_size
    lh = body_size * 0.26
    inner = w - pad - 2.0
    if rh is None:
        tallest = max(wrapped_height(inner, b, body_size, lh) for _, b, _ in rows)
        rh = 2.4 + 2.8 + tallest + 1.6
    y = y_top
    for head, body, col in rows:
        box(ax, x, y - rh, w, rh, fc=WHITE, ec=col, lw=1.5)
        box(ax, x, y - rh, bar, rh, fc=col, ec=col, lw=0, r=0.4)
        ax.text(x + pad, y - 2.6, head, ha="left", va="center",
                fontsize=FS_SMALL, color=col, fontweight="bold")
        wrap(ax, x + pad, y - 5.4, inner, body, body_size, lh=lh)
        y -= rh + gap
    return y + gap


def ladder(ax, x, y_top, w, steps, sh=4.6, gap=1.3, label_w=None,
           arrow_col=SLATE):
    """A vertical flow: list of (label, right-hand annotation, colour)."""
    y = y_top
    for i, (lab, ann, col) in enumerate(steps):
        box(ax, x, y - sh, w, sh, fc=WHITE, ec=col, lw=1.8)
        box(ax, x, y - sh, 1.2, sh, fc=col, ec=col, lw=0, r=0.4)
        ax.text(x + w / 2, y - sh / 2, lab, ha="center", va="center",
                fontsize=FS_SMALL, color=NAVY, fontweight="bold")
        if ann:
            wire(ax, [(x + w + 0.8, y - sh / 2), (x + w + 5.0, y - sh / 2)],
                 color=GRID, lw=1.2, ls="--")
            ax.text(x + w + 6.0, y - sh / 2, ann, ha="left", va="center",
                    fontsize=FS_SMALL - 1.0, color=col)
        if i < len(steps) - 1:
            arrow(ax, x + w / 2, y - sh - 0.15, x + w / 2, y - sh - gap + 0.15,
                  color=arrow_col, lw=1.8, ms=9)
        y -= sh + gap
    return y + gap
