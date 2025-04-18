import os
import json
import pandas as pd
import subprocess
import time

output_dir = "output"
final_output_path = "output/ALL_RTO_DATA.xlsx"
year = "2025"
product = "L3P"
trim = "True"
worker_script = "worker.py"  # Or use worker_india.py if preferred

# Load all states from JSON
with open("jsons/states.json", "r") as f:
    all_states = json.load(f)

all_data = []

# Loop through each state
for state in all_states:
    rto_json_path = f"jsons/{state}_rtos.json"
    if not os.path.exists(rto_json_path):
        print(f"RTO JSON not found for {state}")
        continue

    with open(rto_json_path, "r") as rto_file:
        rtos = json.load(rto_file)

    for rto in rtos:
        output_filename = f"{state}.{rto}.{year}.{product}.csv"
        output_path = os.path.join(output_dir, output_filename)

        # Skip if already exists
        if os.path.exists(output_path):
            print(f"Already exists: {output_filename}")
        else:
            print(f"Fetching: {state} -> {rto}")
            subprocess.run(["python", worker_script, state, rto, year, product, trim])

        # Try reading the output if exists
        if os.path.exists(output_path):
            df = pd.read_csv(output_path)
            df["State"] = state  # Append State column
            df["RTO"] = rto      # Optional: also add RTO name
            all_data.append(df)

# Combine all into one DataFrame and write to Excel
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_excel(final_output_path, index=False)
    print(f"\n✅ All data compiled into: {final_output_path}")
else:
    print("⚠️ No data collected.")
