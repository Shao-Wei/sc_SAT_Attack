import os
import sys
import shutil
import subprocess

# Check argument count
# if len(sys.argv) > 2:
#     print("Usage: python3 sat_attack.py")
#     sys.exit(1)

# Set general environment variables
LOGS_DIR = "sat_log_0801"
BENCHMARK_DIR = "results_0712"

# Benchmark list
## TESTING
# file_name_list = ["s208"]
## All, 2.5G
# file_name_list = ["c1908", "c5315", "c6288", "c7552", "s13207", "s15850", "s208", "s35932", "s38417", "s38584", "s5378", "s9234", "b14_C", "b15_C", "b17_C", "b20_C", "b21_C", "b22_C"]
## Cleaned up INPUT(IN-) lines, rerun 0802, 10G
# file_name_list = ["c7552", "s38417", "s15850", "s13207", "s38584"]
## Rerun 0802, 10G
appendix = "10G"
file_name_list = ["c1908", "c5315", "c6288", "s208", "s35932", "s5378", "s9234", "b14_C", "b15_C", "b17_C", "b20_C", "b21_C", "b22_C"]
# cat_list = ["3_2"]
cat_list = ["3_2", "4_2", "3_3", "3_4", "4_3", "4_4"]

for CAT in cat_list:
    # Create logs directory if it does not exist
    # if os.path.exists(f"{LOGS_DIR}/{CAT}"):
    #     shutil.rmtree(f"{LOGS_DIR}/{CAT}")
    # os.makedirs(f"{LOGS_DIR}/{CAT}", exist_ok=True)
    # Iterate over each file name in the list
    for FILENAME in file_name_list:
        # Construct the command (cleanly formatted)
        cmd = f"""./sld {BENCHMARK_DIR}/{CAT}/{FILENAME}.satblock.bench \\
    {BENCHMARK_DIR}/{CAT}/{FILENAME}.ori.bench \\
    -L {LOGS_DIR}/{CAT}/{FILENAME}.{appendix}.sim.log | tee "{LOGS_DIR}/{CAT}/{FILENAME}.{appendix}.full.log"
"""
        slurm_script = f"""#!/bin/bash
#SBATCH --export=NONE        #Do not propagate environment
#SBATCH --get-user-env=L     #Replicate login environment

##NECESSARY JOB SPECIFICATIONS
#SBATCH --job-name=job_{FILENAME}_{CAT}_{appendix}
#SBATCH --mail-type=END,FAIL   #Send email on job end or failure
#SBATCH --mail-user=shaowei22@tamu.edu
#SBATCH --time=96:00:00       
#SBATCH --ntasks=1                 #Request 1 task
#SBATCH --ntasks-per-node=1        #Request 1 task/core per node
#SBATCH --mem=10G                #Request 2560MB (2.5GB) per node
#SBATCH --output={LOGS_DIR}/{CAT}/job_{FILENAME}_{CAT}.{appendix}.%j    #Send stdout/err to "Example1Out.[jobID]"
#SBATCH --partition=cpu-research
#SBATCH --qos=olympus-cpu-research

source ~/.bashrc
conda activate sat
{cmd}
"""
        # Write the script to a file
        job_filename = f"{LOGS_DIR}/{CAT}/job_{FILENAME}_{CAT}.{appendix}.slurm"
        with open(job_filename, "w") as f:
            f.write(slurm_script)
        
        # Submit the job
        result = subprocess.run(["sbatch", job_filename], capture_output=True, text=True)
        print(f"Submitted {job_filename}: {result.stdout.strip()}")


print("All jobs submitted.")
