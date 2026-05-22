#!/usr/bin/env bash
# write sha256 manifest for files in this eval dir
# run from evals/swebench-lite-pilot: ./scripts/hash_artifacts.sh

set -euo pipefail
cd "$(dirname "$0")/.."

out=artifact_hashes.json.generated
tmp=$(mktemp)

{
  echo "{"
  first=1
  hash_one() {
    local f=$1
    [[ -f $f ]] || return
    local h
    h=$(shasum -a 256 "$f" | awk '{print $1}')
    if [[ $first -eq 1 ]]; then first=0; else echo ","; fi
    printf '  "%s": "sha256:%s"' "$f" "$h"
  }
  hash_one task_ids.txt
  hash_one run_metadata.json
  hash_one predictions.jsonl
  hash_one verification_instructions.md
  hash_one reports/trustableclaw_swebench_lite_one_task_pilot.md
  hash_one trustableclaw_verification_results.json
  hash_one tamper_test_results.json
  while IFS= read -r -d '' f; do
    hash_one "${f#./}"
  done < <(find swebench_results proof_packages/public -type f ! -name .gitkeep -print0 2>/dev/null || true)
  echo ""
  echo "}"
} > "$tmp"

mv "$tmp" "$out"
echo "wrote $out — copy into artifact_hashes.json if it looks right"
