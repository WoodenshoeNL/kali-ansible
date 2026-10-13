#!/bin/bash
# triage.sh — one-command Ghidra bughunt triage on a binary (or a directory of binaries).
# Usage: triage.sh <binary-or-dir> [outdir]
set -u
GHIDRA=~/tools/ghidra_12.1.4_PUBLIC
SCRIPTS=~/tools/ghidra-scripts
IN="${1:?usage: triage.sh <binary-or-dir> [outdir]}"
OUT="${2:-/tmp/ghidra-triage}"
mkdir -p "$OUT" ~/ghidra-proj

run_one() {
    local bin="$1" name
    name=$(basename "$bin")
    echo "[*] triaging: $name"
    "$GHIDRA/support/analyzeHeadless" ~/ghidra-proj triage \
        -import "$bin" -scriptPath "$SCRIPTS" \
        -postScript VulnTriage.java "$OUT/${name}-report.txt" \
        -deleteProject >"$OUT/${name}-ghidra.log" 2>&1
    if [ $? -ne 0 ]; then echo "    ERROR - see $OUT/${name}-ghidra.log"; else
        if grep -q "SCRIPT ERROR" "$OUT/${name}-ghidra.log"; then
            echo "    SCRIPT ERROR - see $OUT/${name}-ghidra.log"
        else
            echo "    -> $OUT/${name}-report.txt"
        fi
    fi
}

if [ -d "$IN" ]; then
    find "$IN" -maxdepth 1 -type f | while read -r b; do run_one "$b"; done
else
    run_one "$IN"
fi
echo "[*] done. Reports in $OUT"
