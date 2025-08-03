import os

## This script cleans up .ori.bench and .satlock.bench files 
## by removing lines starting with "INPUT(IN-)"
## Only the specified files are processed, while the rest are left unchanged.

BENCHMARK_DIR = "results_0712"

filenames = ["c7552", "s38417", "s15850", "s13207", "s38584"]
cat_list = ["3_2", "4_2", "3_3", "3_4", "4_3", "4_4"]
total_mismatches = 0

for fname in filenames:
    for cat in cat_list:
        ori_file = f"{BENCHMARK_DIR}/{cat}/{fname}.ori.bench"
        sat_file = f"{BENCHMARK_DIR}/{cat}/{fname}.satblock.bench"

        # Process .ori file
        with open(ori_file, "r") as f:
            ori_lines = f.readlines()

        ori_cleaned = [line for line in ori_lines if not line.startswith("INPUT(IN-")]
        ori_removed = len(ori_lines) - len(ori_cleaned)

        # Process .satlock file
        with open(sat_file, "r") as f:
            sat_lines = f.readlines()

        sat_cleaned = [line for line in sat_lines if not line.startswith("INPUT(IN-")]
        sat_removed = len(sat_lines) - len(sat_cleaned)

        # Write back cleaned files (overwrite original)
        with open(ori_file, "w") as f:
            f.writelines(ori_cleaned)

        with open(sat_file, "w") as f:
            f.writelines(sat_cleaned)

        # Report
        print(f"{fname} {cat}: Removed {ori_removed} from .ori, {sat_removed} from .sat")

        if ori_removed != sat_removed:
            print(f"ERROR: MISMATCH in {fname} {cat} — .ori: {ori_removed}, .sat: {sat_removed}")
            total_mismatches += 1

print(f"\nFinished. {total_mismatches} file pairs had mismatched removal counts.")
