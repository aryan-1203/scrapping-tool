# Imports and settings
import sys, time, json, os, csv, pandas as pd

short_wait = 3
long_wait = 5

# Imports arguements and modules
from worker_actions import select_something, open_website, click_something, E2W, E3W, return_header, return_row
arg_holder = []
for arg in sys.argv:
    arg_holder.append(arg)
arg_holder = arg_holder[1:]
print(arg_holder)
sys.stdout.flush()

# State RTO Year Product Trim_Str_Bool



# Imports paths
with open('jsons/paths.json', 'r') as file:
    paths_json = json.load(file)
year_field_path = paths_json['year_field_path']
year_path = paths_json[f"data_year_{arg_holder[2]}_path"]



with open('jsons/states.json', 'r') as file:
    state_paths_json = json.load(file)
state_field_path = paths_json['state_field_path']
state_path = state_paths_json[arg_holder[0]]


with open(f'jsons/{arg_holder[0]}_rtos.json') as file:
    rtos_json = json.load(file)

print('flag')
sys.stdout.flush()

x_axis_field_path = paths_json['x_axis_field_path']
x_axis_month_path = paths_json['x_axis_month_path']

y_axis_field_path = paths_json['y_axis_field_path']
y_axis_make_path = paths_json['y_axis_make_path']
button_refresh_main = paths_json['button_refresh_main']
button_expand = paths_json['button_expand']
button_refresh_side = paths_json['button_refresh_side']
button_download = paths_json['button_download']

rto_field_path = paths_json['rto_field_path']
rto_path = str(paths_json['rto_path']).replace('PLACEHOLDER', str(rtos_json[arg_holder[1]]))

# Import product specific paths
fuel = paths_json['fuel']
pure = paths_json['pure']
vehicle_class = paths_json[arg_holder[3]]
two_wheeler_nt = paths_json['two_wheeler_nt']
two_wheeler_t = paths_json['two_wheeler_t']
three_wheeler_t = paths_json['three_wheeler_t']
three_wheeler_nt = paths_json['three_wheeler_nt']

print(arg_holder[3][0])
sys.stdout.flush()




# Product specific functions
def product_settings():
    click_something(fuel)
    print("Log: Fuel selected")
    sys.stdout.flush()
    click_something(pure)
    print("Log: Pure EV selected")
    sys.stdout.flush()
    if vehicle_class != "NULL": click_something(vehicle_class)
    print(f"Log: {arg_holder[3]} selected")
    sys.stdout.flush()

    match arg_holder[3][0]:
        case "E":
            E2W(two_wheeler_nt, two_wheeler_t)
        case "L":
            E3W(three_wheeler_nt, three_wheeler_t)





# Open website
open_website()
print("Log: URL opened")
sys.stdout.flush()

# Year
select_something(year_field_path, year_path)
time.sleep(short_wait)
print(f"Log: Year: {arg_holder[2]} selected")
sys.stdout.flush()

# Month on X-Axis
select_something(x_axis_field_path, x_axis_month_path)
time.sleep(short_wait)
print(f"Log: X-Axis: Month selected")
sys.stdout.flush()

# Maker on Y-Axis
select_something(y_axis_field_path, y_axis_make_path)
time.sleep(short_wait)
print(f"Log: Y-Axis: Maker selected")

# State
select_something(state_field_path,state_path)
time.sleep(short_wait)
print(f"Log: State: {arg_holder[0]} selected")
sys.stdout.flush()

# Big refresh 1
click_something(button_refresh_main)
time.sleep(long_wait)
print("Log: Main refresh button pressed for the first time")
sys.stdout.flush()

# Select RTO
select_something(rto_field_path, rto_path)
select_something(rto_field_path, rto_path)
time.sleep(short_wait)
print(f"Log: RTO: {arg_holder[1]} selected")
sys.stdout.flush()

# Big refresh 2
click_something(button_refresh_main)
time.sleep(long_wait)
print("Log: Main refresh button pressed for the second time")
sys.stdout.flush()

# Expand side-menu
click_something(button_expand)
time.sleep(short_wait)
print("Log: Side-bar expanded")
sys.stdout.flush()

# Product settings
product_settings()
time.sleep(short_wait)

# Side button for refresh
click_something(button_refresh_side)
time.sleep(long_wait)
print("Log: Side refresh button pressed")
sys.stdout.flush()

# Download data
click_something(button_download)
time.sleep(1)
print("Log: Download button pressed")
sys.stdout.flush()

time.sleep(3)
print("Done with browser")





xlsx_path = f"C:/Users/russe/Downloads/reportTable.xlsx"
temp_path = f'temp/reportTable.csv'
output_file_path = f'output/{arg_holder[0]}.{arg_holder[1]}.{arg_holder[2]}.{arg_holder[3]}.csv'
pd_worker = pd.read_excel(xlsx_path)
pd_worker.to_csv(temp_path, index=False)



trim = True if arg_holder[4] == "True" else False
year = arg_holder[2]

with open(temp_path,'r') as data_file:
    rows = list(csv.reader(data_file))
    holder = []

    # Add header
    holder.append(return_header(rows, trim, year))

    number_of_data_rows = (len(rows)-4) #-4 is to skip stub rows + header
    for row in range(1, number_of_data_rows+1):
        holder.append(return_row(rows, row, trim, arg_holder[3], arg_holder[1], arg_holder[0]))

    with open(output_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(holder)


# State RTO Year Product Trim_Str_Bool
os.remove(temp_path)
os.remove(xlsx_path)