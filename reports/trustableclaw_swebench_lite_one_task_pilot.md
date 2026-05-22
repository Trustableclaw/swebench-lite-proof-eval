# TrustableClaw Agent Accountability Eval — SWE-bench Lite One-Task Pilot

This report captures the results of our single-task SWE-bench Lite pilot, demonstrating how the execution run, patch, and results are verified and secured against tampering using TrustableClaw's cryptographic ledger.

## Results

| Metric | Result |
|--------|--------|
| SWE-bench Lite tasks tested | 1 |
| Task ID | `django__django-10914` |
| Resolved | **Yes (128 / 128 unit tests passed successfully)** |
| Agent | OpenAI Python Agent |
| Model | `gpt-4o` |
| Predictions published | Yes (`predictions.jsonl`) |
| Raw SWE-bench logs published | Yes (`swebench_results/test_log.txt`) |
| Artifact hashes | Verified (`artifact_hashes.json` matches all file system states) |
| Receipts generated | 9 chained JSON receipts generated in `trustableclaw_receipts/` |
| Receipt verification | **Passed** (100% hash integrity and index sequence match) |
| Ledger verification | **Passed** (Cryptographic hash-chain PrevHash linkage fully intact) |
| Tamper detection | **Passed** (Corruptions to patch, log, or receipts detected immediately) |
| Public proof package | Ready for publication (`proof_packages/public/` configured) |
## Disclaimer

This one-task pilot does not claim leaderboard performance. SWE-bench measures whether the coding agent solved the task. TrustableClaw measures whether the patch, logs, result, and report can be verified, audited, preserved, and checked for tampering.

## Cryptographic Evidence & Hash Chain

TrustableClaw secures each step of the evaluation pipeline in a chronological hash-chain ledger. The pilot run generated the following chained proof records (available in [trustableclaw_receipts/](../trustableclaw_receipts/)):

1. **`01_task_imported.json`** (`hash: 7dedc82d...`): Ingests target task ID and source dataset details.
2. **`02_patch_recorded.json`** (`hash: 8b25dfb4...`): Records the raw model-generated git patch for `django/conf/global_settings.py`.
3. **`03_test_log_recorded.json`** (`hash: 75be810f...`): Captures the detailed unit test log verifying 128 tests run.
4. **`04_swe_result_recorded.json`** (`hash: e6f72482...`): Seals the task resolution status.
5. **`05_proof_package_created.json`**: Packages the artifacts (including this report) and verifies their inclusion.
6. **`06_predictions_file.json`**: Verifies predictions file SHA-256 matches.
7. **`07_swe_results_dir.json`**: Receipt for raw log folders.
8. **`08_hash_manifest.json`**: Locks the `artifact_hashes.json` manifest.
9. **`09_final_report.json`**: Seals this report dynamically in the ledger, finalizing the cryptographic chain.

*Note: Receipts 05 through 09 dynamically lock the final report and manifest hashes, sealing the entire workspace state in an unbroken, tamper-evident chain.*

## Artifacts

- **Public Repository:** https://github.com/trustableclaw/swebench-lite-proof-eval
- **Reproduction Instructions:** [verification_instructions.md](../verification_instructions.md)
- **Evaluation Metadata:** [run_metadata.json](../run_metadata.json)

## Site Summary

TrustableClaw provides a tamper-evident audit layer for AI agent evaluations. We publish the predictions file (`predictions.jsonl`), raw unit test logs (`test_log.txt`), and a SHA-256 artifact manifest. Anyone can download these files and rerun the evaluation harness themselves to confirm the results. TrustableClaw seals all artifacts into a cryptographic hash-chain ledger: any modification to the patch, the logs, or the receipts breaks the hash chain and is caught immediately upon verification.

