# Verifying the one-task pilot

Instructions for cloning, rerunning, and verifying this pilot run. You will need Docker, Python 3.10+, and sufficient disk space for the SWE-bench test images.

## Get the artifacts

```bash
git clone https://github.com/trustableclaw/swebench-lite-proof-eval.git
cd swebench-lite-proof-eval
```

Or from this repo:

```bash
cd evals/swebench-lite-pilot
```

`task_ids.txt` should have exactly one Lite `instance_id`.

## Rerun SWE-bench

```bash
git clone https://github.com/SWE-bench/SWE-bench.git
cd SWE-bench
pip install -e .
```

```bash
python -m swebench.harness.run_evaluation \
  --dataset_name princeton-nlp/SWE-bench_Lite \
  --predictions_path /path/to/predictions.jsonl \
  --max_workers 1 \
  --run_id third_party_rerun
```

Our `predictions.jsonl` only has one line for this pilot. Compare your run's resolved/failed for that `instance_id` against our `swebench_results/`. Timestamps in logs can differ; pass/fail should match.

Harness git commit should match `run_metadata.json` → `swebench_harness_version`.

## Check hashes

Either hash files yourself:

```bash
shasum -a 256 task_ids.txt run_metadata.json predictions.jsonl
```

Or from the pilot dir:

```bash
./scripts/hash_artifacts.sh
```

Compare output to `artifact_hashes.json` (we store digests as `sha256:<hex>`).

## TrustableClaw side

Use the published `trustableclaw_receipts/` and ledger from the bundle. Verify ledger integrity with the CLI (same as the main app):

```bash
trustableclaw verify <head-hash> <ledger-root>
```

`trustableclaw_verification_results.json` should show receipt + ledger pass and patch/log/result hashes matching `artifact_hashes.json`.

## Tamper test

We intentionally corrupt copies of the patch, a test log, and a result json after a clean import. Verification should fail on those copies. See `tamper_test_results.json` for what we tried.

## Note

One task from Lite isn't a score on the full 300-task set. SWE-bench answers whether the patch fixes the issue; TrustableClaw answers whether we stored and hashed the run correctly and catch edits afterward.
