import subprocess, json, time, os, pandas as pd

start_time = time.time()

# Clear old output folder
output_folder_path = 'output/'
for f in os.listdir(output_folder_path):
    os.remove(os.path.join(output_folder_path, f))
print("🧹 Old output files cleared")

# Load RTOs
with open('jsons/rajasthan_rtos.json', 'r') as file:
    rtos = json.load(file)

# Track existing files
list_of_rtos_downloaded = []
for item in os.listdir(output_folder_path):
    first_dot = item.find(".")
    second_dot = item.find(".", first_dot + 1)
    list_of_rtos_downloaded.append(item[first_dot + 1:second_dot])

# Config
state = "rajasthan"
years = ["2023", "2024", "2025"]
products = ["L3P", "L3G", "L5P", "L5G"]
trim = "True" 
worker_script = "worker.py"

# Scrape each RTO
# Scrape each RTO for each year and each product
for year in years:
    for product in products:
        for rto in rtos:
            check_filename = f"{state}.{rto}.{year}.{product}.csv"
            if check_filename in os.listdir(output_folder_path):
                print(f"✅ Already downloaded: {rto} for {year} {product}")
                continue

            print(f"🚀 Running worker for RTO: {rto}, Year: {year}, Product: {product}")

            try:
                result = subprocess.run(
                    ["python", worker_script, state, rto, year, product, trim],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                print(result.stdout)
                if result.stderr:
                    print("⚠️ Error Output:")
                    print(result.stderr)

            except subprocess.CalledProcessError as e:
                print(f"❌ Failed for RTO: {rto}, Year: {year}, Product: {product}")
                print(e.output)
                print(e.stderr)


# Create separate combined Excels per year and product
for year in years:
    for product in products:
        combined_df = pd.DataFrame()
        for file in os.listdir(output_folder_path):
            if file.endswith(".csv") and file.startswith(f"{state}.") and f".{year}.{product}" in file:
                df = pd.read_csv(os.path.join(output_folder_path, file))
                combined_df = pd.concat([combined_df, df], ignore_index=True)

        output_filename = f"output/{state}_{year}_{product}_combined.xlsx"
        combined_df.to_excel(output_filename, index=False)
        print(f"📄 Combined Excel created: {output_filename}")

# Now create one big master combined Excel (for all years and products)
master_df = pd.DataFrame()
for file in os.listdir(output_folder_path):
    if file.endswith(".csv") and file.startswith(state):
        df = pd.read_csv(os.path.join(output_folder_path, file))
        master_df = pd.concat([master_df, df], ignore_index=True)

master_output = f"output/{state}_master_combined.xlsx"
master_df.to_excel(master_output, index=False)
print(f"📄 Master Combined Excel created: {master_output}")


end_time = time.time()
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"\n⏱️ Total Execution time: {minutes} minutes and {seconds:.2f} seconds")
