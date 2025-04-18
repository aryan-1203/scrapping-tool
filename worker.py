# Imports and settings
import sys, time, json, os, csv, pandas as pd
from pathlib import Path
from datetime import datetime
from worker_actions.actions import driver

short_wait = 3
long_wait = 5
from worker_actions import select_something, open_website, click_something, E2W, E3W, return_header, return_row

# Parse command-line args
arg_holder = sys.argv[1:]
print(arg_holder)
sys.stdout.flush()

# Load JSON configs
with open('jsons/paths.json', 'r') as file:
    paths_json = json.load(file)

with open('jsons/states.json', 'r') as file:
    state_paths_json = json.load(file)

with open(f'jsons/{arg_holder[0]}_rtos.json') as file:
    rtos_json = json.load(file)

year_field_path = paths_json['year_field_path']
year_path = paths_json[f"data_year_{arg_holder[2]}_path"]
state_field_path = paths_json['state_field_path']
state_path = state_paths_json[arg_holder[0]]
rto_field_path = paths_json['rto_field_path']
rto_path = str(paths_json['rto_path']).replace('PLACEHOLDER', str(rtos_json[arg_holder[1]]))
x_axis_field_path = paths_json['x_axis_field_path']
x_axis_month_path = paths_json['x_axis_month_path']
y_axis_field_path = paths_json['y_axis_field_path']
y_axis_make_path = paths_json['y_axis_make_path']
button_refresh_main = paths_json['button_refresh_main']
button_expand = paths_json['button_expand']
button_refresh_side = paths_json['button_refresh_side']
button_download = paths_json['button_download']

# Product paths
fuel = paths_json['fuel']
pure = paths_json['pure']
vehicle_class = paths_json[arg_holder[3]]
two_wheeler_nt = paths_json['two_wheeler_nt']
two_wheeler_t = paths_json['two_wheeler_t']
three_wheeler_nt = paths_json['three_wheeler_nt']
three_wheeler_t = paths_json['three_wheeler_t']

print(arg_holder[3][0])
sys.stdout.flush()

# Set up cross-platform Downloads path and unique file name
download_dir = str(Path.home() / "Downloads")
default_xlsx_path = os.path.join(download_dir, "reportTable.xlsx")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
xlsx_renamed_path = os.path.join(download_dir, f"{arg_holder[1]}_{timestamp}.xlsx")

# Output and temp files
temp_path = 'temp/reportTable.csv'
output_file_path = f'output/{arg_holder[0]}.{arg_holder[1]}.{arg_holder[2]}.{arg_holder[3]}.csv'

# Product-specific UI handling
def product_settings():
    click_something(fuel)
    print("Log: Fuel selected")
    sys.stdout.flush()
    click_something(pure)
    print("Log: Pure EV selected")
    sys.stdout.flush()
    if vehicle_class != "NULL":
        click_something(vehicle_class)
    print(f"Log: {arg_holder[3]} selected")
    sys.stdout.flush()

    match arg_holder[3][0]:
        case "E":
            E2W(two_wheeler_nt, two_wheeler_t)
        case "L":
            E3W(three_wheeler_nt, three_wheeler_t)

# Main automation flow
open_website()
print("Log: URL opened")
sys.stdout.flush()

select_something(year_field_path, year_path)
time.sleep(short_wait)
print(f"Log: Year: {arg_holder[2]} selected")
sys.stdout.flush()

select_something(x_axis_field_path, x_axis_month_path)
time.sleep(short_wait)
print("Log: X-Axis: Month selected")
sys.stdout.flush()

select_something(y_axis_field_path, y_axis_make_path)
time.sleep(short_wait)
print("Log: Y-Axis: Maker selected")
sys.stdout.flush()

select_something(state_field_path, state_path)
time.sleep(short_wait)
print(f"Log: State: {arg_holder[0]} selected")
sys.stdout.flush()

click_something(button_refresh_main)
time.sleep(long_wait)
print("Log: Main refresh button pressed (1st)")
sys.stdout.flush()

select_something(rto_field_path, rto_path)
select_something(rto_field_path, rto_path)
time.sleep(short_wait)
print(f"Log: RTO: {arg_holder[1]} selected")
sys.stdout.flush()

click_something(button_refresh_main)
time.sleep(long_wait)
print("Log: Main refresh button pressed (2nd)")
sys.stdout.flush()

click_something(button_expand)
time.sleep(short_wait)
print("Log: Sidebar expanded")
sys.stdout.flush()

product_settings()
time.sleep(short_wait)

click_something(button_refresh_side)
time.sleep(long_wait)
print("Log: Side refresh button pressed")
sys.stdout.flush()

click_something(button_download)
time.sleep(3)  # Wait for download to complete
print("Log: Download button pressed")
sys.stdout.flush()

# Rename the downloaded file
if os.path.exists(default_xlsx_path):
    os.rename(default_xlsx_path, xlsx_renamed_path)
    print(f"Log: File renamed to {xlsx_renamed_path}")
    sys.stdout.flush()
else:
    print("❌ Download failed: reportTable.xlsx not found")
    sys.exit(1)

print("Done with browser")

# Convert XLSX to CSV
pd_worker = pd.read_excel(xlsx_renamed_path)
pd_worker.to_csv(temp_path, index=False)

# Format and save data
# Format and save data
trim = True if arg_holder[4] == "True" else False

list_of_rows = pd_worker.values.tolist()

header = return_header(list_of_rows, trim, arg_holder[2])

final_data = [header]

serial_no = 0
while True:
    row = return_row(list_of_rows, serial_no, trim, arg_holder[3], arg_holder[1], arg_holder[0])
    if row is None:
        break
    final_data.append(row)
    serial_no += 1

# Write final CSV
with open(output_file_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(final_data)

print(f"✅ Saved formatted output: {output_file_path}")

# Cleanup temp file
try:
    os.remove(temp_path)
    print("🧹 Temp file cleaned up")
except Exception as e:
    print(f"⚠️ Temp file cleanup failed: {e}")

# Quit driver
driver.quit()
print("✅ Driver closed successfully")

