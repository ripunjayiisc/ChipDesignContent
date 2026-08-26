#!/bin/bash
# render.sh <pptx> <outdir>  — convert to PDF and rasterise pages for review
set -e
SP=/tmp/claude-0/-home-user/21001dbc-8f5e-5620-b4fb-6ca9041a22f9/scratchpad
SRC="$1"; OUT="${2:-$SP/pages}"
mkdir -p "$OUT"
soffice -env:UserInstallation=file://$SP/lo --headless --norestore \
        --convert-to pdf "$SRC" --outdir "$OUT" >/dev/null 2>&1
PDF="$OUT/$(basename "${SRC%.*}").pdf"
pdftoppm -r 72 -png "$PDF" "$OUT/p" 2>/dev/null || true
echo "$PDF"
ls "$OUT" | head -3
