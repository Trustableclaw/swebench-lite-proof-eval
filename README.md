# TrustableClaw - SWE-bench Lite Proof of Evaluation (One-Task Pilot)

This repository contains the complete cryptographic audit ledger for our single-task SWE-bench Lite evaluation pilot (targeting `django__django-10914`). 

The goal of this pilot is to demonstrate how TrustableClaw's accountability layer mathematically secures evaluation runs, logs, and outputs to prevent tampering.

---

## Privacy & Role Attribution

This benchmark repository intentionally avoids displaying individual human names. Reports and receipts use role-based labels such as benchmark_runner, internal_reviewer, and TrustableClaw Eval Team. This keeps the focus on reproducible benchmark evidence, not personal attribution.

### Benchmark Attribution
* **Evaluated by:** TrustableClaw Eval Team
* **System tested:** TrustableClaw accountability layer with SWE-bench Lite task artifacts
* **Verification method:** Public hashes, receipts, result files, and rerun instructions
* **Human names:** Not displayed. The benchmark is attributed to the TrustableClaw project, not to individual contributors.

---

## Pilot Overview

* **Benchmark:** SWE-bench Lite
* **Instance ID:** `django__django-10914`
* **Resolved:** Yes (128 / 128 unit tests passed)
* **Agent / Model:** OpenAI Python Agent (`gpt-4o`)
* **Harness Version:** `v1.0.0-placeholder`
* **Ledger Status:** Verified & intact (9 chained receipts)

---

## Repository Structure

* [predictions.jsonl](predictions.jsonl) - The model-generated patch file.
* [swebench_results/test_log.txt](swebench_results/test_log.txt) - Raw test output from the evaluation harness.
* [trustableclaw_receipts/](trustableclaw_receipts/) - Chronological, dual-sealed receipt files (01 to 09).
* [artifact_hashes.json](artifact_hashes.json) - Master SHA-256 manifest of the workspace.
* [reports/trustableclaw_swebench_lite_one_task_pilot.md](reports/trustableclaw_swebench_lite_one_task_pilot.md) - Comprehensive pilot audit report.
* [verification_instructions.md](verification_instructions.md) - Step-by-step audit and reproduction instructions.

---

## Ledger Receipts (Chronological Hash Chain)

TrustableClaw secures each step of the evaluation sequence in a sequential cryptographic ledger:
1. `01_task_imported.json` - Workspace import check.
2. `02_patch_recorded.json` - Model patch capture.
3. `03_test_log_recorded.json` - Evaluation test logs seal.
4. `04_swe_result_recorded.json` - Overall task outcome registration.
5. `05_proof_package_created.json` - Public bundle packaging confirmation.
6. `06_predictions_file.json` - Predictions manifest locking.
7. `07_swe_results_dir.json` - Log directory proof.
8. `08_hash_manifest.json` - Master SHA-256 manifest locking.
9. `09_final_report.json` - Evaluation report sealing.

---

## How to Verify the Ledger

Follow the step-by-step guide in [verification_instructions.md](verification_instructions.md) to:
1. Re-calculate workspace hashes and compare them with `artifact_hashes.json`.
2. Verify the sequential integrity of the 9 JSON receipts.
3. Re-run the SWE-bench container to verify that the patch solves the task.
