#!/usr/bin/env python3
import os
import sys
import json

def main():
    # Calculate pilot directory and search for django-pilot-env dynamically
    output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    desktop_dir = os.path.abspath(os.path.join(output_dir, "..", "..", ".."))
    sandbox_dir = os.getenv("DJANGO_PILOT_ENV", os.path.join(desktop_dir, "django-pilot-env"))
    patch_file = os.path.join(sandbox_dir, "predictions.patch")
    
    if not os.path.exists(patch_file):
        print(f"[ERROR] Patch file not found at {patch_file}!")
        print("Please generate it first by running: git diff django/conf/global_settings.py > predictions.patch")
        sys.exit(1)

    print(f"Reading patch from {patch_file}...")
    with open(patch_file, "r") as f:
        patch_content = f.read()

    if not patch_content.strip():
        print("[WARNING] The patch file is empty. Check if global_settings.py has actually been modified!")

    output_file = os.path.join(output_dir, "predictions.jsonl")

    prediction_record = {
        "instance_id": "django__django-10914",
        "model_patch": patch_content,
        "model_name_or_path": "gpt-4o"
    }

    print(f"Formatting and writing to {output_file}...")
    with open(output_file, "w") as f:
        f.write(json.dumps(prediction_record) + "\n")

    print("[SUCCESS] Successfully formatted and generated predictions.jsonl!")

if __name__ == "__main__":
    main()
