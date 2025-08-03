import os
import re

## Parse SAT attack results ran by run_sat_attack.py
"""
Script Purpose:
Given a job `name`, this script checks whether `{name}.sim.log` exists.

- If it exists: assume success, and log `name` and the **first line** of `.sim.log` to `overall.log`.
- If not: treat as failed, and:
    - look for `{name}.full.log`
    - if last line starts with "slurmstepd" and contains "oom" → log `name` and "MO"
    - if last line starts with "iteration:" → log `name` and "R"
    - otherwise → log `name` and "UNKNOWN"

The result is always **appended** to `overall.log`.
"""

"""
Due to extra handling of files in file_name_list_part1 (executed cleanBench.py),
we split the file_name_list into two parts for clarity and to avoid confusion.
Two parts have different appendices on the result files.
"""

LOGS_DIR = "sat_log_0801"
WRITE_TO_FILE = "sat_log_0801/overall.log"
file_name_list_all = ["b14_C", "b15_C", "b17_C", "b20_C", "b21_C", "b22_C", "c1908", "c5315", "c6288", "c7552", "s13207", "s15850", "s208", "s35932", "s38417", "s38584", "s5378", "s9234"]
cat_list = ["3_2", "4_2", "3_3", "3_4", "4_3", "4_4"]

appendix_part1 = ""
file_name_list_part1 = ["c7552", "s38417", "s15850", "s13207", "s38584"]
appendix_part2 = ".10G"
file_name_list_part2 = ["c1908", "c5315", "c6288", "s208", "s35932", "s5378", "s9234", "b14_C", "b15_C", "b17_C", "b20_C", "b21_C", "b22_C"]

def find_job_with_max_id(name, directory):
    pattern = re.compile(rf"^{re.escape(name)}\.(\d+)$")
    max_id = -1
    max_file = None

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id
                max_file = filename

    return f"{directory}/{max_file}"

def analyze_log(path, name, job_name, output_log):
    sim_log = f"{path}/{name}.sim.log"
    # full_log = f"{path}/{name}.full.log"
    job_log = find_job_with_max_id(job_name, path)

    try:
        with open(output_log, "a") as out:
            if os.path.exists(sim_log):
                # Success: read first line of sim.log
                with open(sim_log, "r") as sim:
                    first_line = sim.readline().strip()
                out.write(f"{path} {name.split('.')[0]} S {first_line}\n")
            else:
                # Failure case: investigate full.log
                if os.path.exists(job_log):
                    with open(job_log, "r") as job:
                        lines = job.readlines()
                        if not lines:
                            reason = "EMPTY"
                        else:
                            last_line = next((line.strip() for line in reversed(lines) if line.strip()), None)
                            if last_line.startswith("slurmstepd"):
                                if "oom" in last_line.lower():
                                    reason = "MO"
                                else: 
                                    reason = "UNKNOWN"
                            elif last_line.startswith("iteration:"):
                                reason = "R"
                            else:
                                reason = "UNIDENTIFIED_WITH_JOB_LOG"
                else:
                    reason = f"MISSING: {job_log} not found"
                out.write(f"{path} {name.split('.')[0]} {reason}\n")
    except Exception as e:
        print(f"Error processing {name}: {e}")

set1 = set(file_name_list_part1)
set2 = set(file_name_list_part2)
# Open in write mode to clear content
with open(WRITE_TO_FILE, "w") as f:
    f.write("PATH NAME STATUS ITERATION TIME DECISION CONFLICT\n")
for cat in cat_list:
    for file in file_name_list_all:
        if file in set1:
            analyze_log(f"{LOGS_DIR}/{cat}", f"{file}{appendix_part1}", f"job_{file}_{cat}{appendix_part1}", WRITE_TO_FILE)
        elif file in set2:
            analyze_log(f"{LOGS_DIR}/{cat}", f"{file}{appendix_part2}", f"job_{file}_{cat}{appendix_part2}", WRITE_TO_FILE)
        else:
            print(f"Warning: {file} not found in either part lists.")



