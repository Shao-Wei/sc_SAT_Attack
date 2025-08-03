import os
import sys

file_name = sys.argv[1]

# Read the key from file
with open(f"test/{file_name}.keys", "r") as f:
    key_value = f.read().strip()

# Build the command string
cmd = f"./lcmp test/{file_name}.ori.bench test/{file_name}.satblock.bench key={key_value}"

# Run the command
os.system(cmd)
