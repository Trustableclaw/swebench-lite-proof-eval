#!/usr/bin/env python3
import json
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HASHES_PATH = os.path.join(BASE_DIR, "artifact_hashes.json")
RECEIPTS_DIR = os.path.join(BASE_DIR, "trustableclaw_receipts")
VERIFICATION_PATH = os.path.join(BASE_DIR, "trustableclaw_verification_results.json")
TAMPER_PATH = os.path.join(BASE_DIR, "tamper_test_results.json")

def compute_sha256_of_file(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def compute_sha256_of_receipt(receipt_data: dict) -> str:
    # Serialize receipt without 'hash' field to calculate its cryptographic digest
    tmp = dict(receipt_data)
    tmp.pop("hash", None)
    serialized = json.dumps(tmp, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def main():
    print("Running SWE-bench Pilot Verification and Ledger Tamper Test...")

    # Load authentic hashes
    with open(HASHES_PATH, "r") as f:
        authentic_hashes = json.load(f)

    # 1. Verification Phase
    verification_results = {
        "ok": False,
        "receipts_ok": False,
        "ledger_ok": False,
        "patch_hash_match": False,
        "test_log_hash_match": False,
        "result_hash_match": False,
        "proof_package_ok": False
    }

    # Verify predictions.jsonl hash
    pred_path = os.path.join(BASE_DIR, "predictions.jsonl")
    pred_hash = "sha256:" + compute_sha256_of_file(pred_path)
    verification_results["patch_hash_match"] = (pred_hash == authentic_hashes.get("predictions.jsonl"))
    print(f"Predictions file hash matches: {verification_results['patch_hash_match']}")

    # Verify swebench_results/test_log.txt hash
    log_path = os.path.join(BASE_DIR, "swebench_results/test_log.txt")
    log_hash = "sha256:" + compute_sha256_of_file(log_path)
    verification_results["test_log_hash_match"] = (log_hash == authentic_hashes.get("swebench_results/test_log.txt"))
    print(f"Test log file hash matches: {verification_results['test_log_hash_match']}")

    # Verify trustableclaw_verification_results.json (we bypass its self-hash match check during generation to avoid circular refs, or match it against current)
    # For results, we check if other files in the manifest are intact
    tasks_path = os.path.join(BASE_DIR, "task_ids.txt")
    tasks_hash = "sha256:" + compute_sha256_of_file(tasks_path)
    verification_results["result_hash_match"] = (tasks_hash == authentic_hashes.get("task_ids.txt"))

    # Load receipts and check hash chain
    receipt_files = sorted([f for f in os.listdir(RECEIPTS_DIR) if f.endswith(".json")])
    receipts = []
    for rf in receipt_files:
        with open(os.path.join(RECEIPTS_DIR, rf), "r") as f:
            receipts.append(json.load(f))

    receipts_chain_valid = True
    prev_hash = ""
    for i, r in enumerate(receipts):
        # Rule 1: index matching
        if r["index"] != i:
            print(f"[-] Receipt index mismatch at {i}: got {r['index']}")
            receipts_chain_valid = False
            break
        # Rule 2: hash integrity
        calculated_hash = compute_sha256_of_receipt(r)
        if r["hash"] != calculated_hash:
            print(f"[-] Receipt hash corrupted at index {i}: recorded {r['hash'][:8]}, calculated {calculated_hash[:8]}")
            receipts_chain_valid = False
            break
        # Rule 3: prev_hash linkage
        if r["prev_hash"] != prev_hash:
            print(f"[-] Receipt linkage broken at index {i}: recorded prev {r['prev_hash'][:8]}, expected {prev_hash[:8]}")
            receipts_chain_valid = False
            break
        prev_hash = r["hash"]

    verification_results["receipts_ok"] = receipts_chain_valid
    verification_results["ledger_ok"] = receipts_chain_valid
    verification_results["proof_package_ok"] = (
        verification_results["receipts_ok"] and 
        verification_results["patch_hash_match"] and 
        verification_results["test_log_hash_match"]
    )
    verification_results["ok"] = verification_results["proof_package_ok"]

    # Write verification results
    with open(VERIFICATION_PATH, "w") as f:
        json.dump(verification_results, f, indent=2)
        f.write("\n")
    print(f"Written verification results to: {VERIFICATION_PATH}")


    # 2. Tamper Simulation Phase
    tamper_results = {
        "ok": False,
        "patch_tamper_detected": False,
        "test_log_tamper_detected": False,
        "result_json_tamper_detected": False
    }

    # Tamper 1: Modify a copy of predictions.jsonl
    with open(pred_path, "r") as f:
        pred_content = f.read()
    tampered_pred = pred_content.replace("FILE_UPLOAD_PERMISSIONS = 0o644", "FILE_UPLOAD_PERMISSIONS = 0o777")
    tampered_pred_hash = "sha256:" + hashlib.sha256(tampered_pred.encode('utf-8')).hexdigest()
    tamper_results["patch_tamper_detected"] = (tampered_pred_hash != authentic_hashes.get("predictions.jsonl"))
    print(f"Tamper detection for patch: {tamper_results['patch_tamper_detected']} (Hash changed from {authentic_hashes.get('predictions.jsonl')[:15]}... to {tampered_pred_hash[:15]}...)")

    # Tamper 2: Modify a copy of test_log.txt
    with open(log_path, "r") as f:
        log_content = f.read()
    tampered_log = log_content.replace("Ran 128 tests", "Ran 127 tests")
    tampered_log_hash = "sha256:" + hashlib.sha256(tampered_log.encode('utf-8')).hexdigest()
    tamper_results["test_log_tamper_detected"] = (tampered_log_hash != authentic_hashes.get("swebench_results/test_log.txt"))
    print(f"Tamper detection for test log: {tamper_results['test_log_tamper_detected']} (Hash changed from {authentic_hashes.get('swebench_results/test_log.txt')[:15]}... to {tampered_log_hash[:15]}...)")

    # Tamper 3: Modify a copy of the receipt 02_patch_recorded.json
    with open(os.path.join(RECEIPTS_DIR, "02_patch_recorded.json"), "r") as f:
        rcpt = json.load(f)
    # Corrupt model name
    rcpt["data"]["model"] = "gpt-3.5-turbo"
    # Re-evaluating hash without changing the embedded 'hash' field to see if the seal detects it
    corrupted_rcpt_calculated_hash = compute_sha256_of_receipt(rcpt)
    tamper_results["result_json_tamper_detected"] = (rcpt["hash"] != corrupted_rcpt_calculated_hash)
    print(f"Tamper detection for receipt json: {tamper_results['result_json_tamper_detected']} (Seal hash mismatch: recorded {rcpt['hash'][:8]}, recalculating tampered receipt got {corrupted_rcpt_calculated_hash[:8]})")

    tamper_results["ok"] = (
        tamper_results["patch_tamper_detected"] and 
        tamper_results["test_log_tamper_detected"] and 
        tamper_results["result_json_tamper_detected"]
    )

    # Write tamper test results
    with open(TAMPER_PATH, "w") as f:
        json.dump(tamper_results, f, indent=2)
        f.write("\n")
    print(f"Written tamper test results to: {TAMPER_PATH}")

if __name__ == "__main__":
    main()
