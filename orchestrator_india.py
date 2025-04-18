import subprocess, json, time, os
start_time = time.time()

# reportTable.xlsx
# /c means to terminate after running

def run_worker(state, rto, year, product, trim):
    running = True
    process = subprocess.Popen(
        ['cmd', '/c', f"python worker_india.py {state} {rto} {year} {product} {trim}"],
        stdin=subprocess.PIPE,      # Pipe to send comms
        stdout=subprocess.PIPE,     # Pipe to receive comms
        stderr=subprocess.PIPE,     # Pipe to receive errors
        text=True                   # Text mode for stdin/out
    )
    while running:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        elif output.strip() == "Closed":
            running = False
        else:
            print(output.strip())

with open('jsons/rajasthan_rtos.json', 'r') as file:
    rtos = json.load(file)

# run_worker("madhya_pradesh", "ashoknagar", "2023", "L3G", "False")

list_of_rtos_downloaded = []
output_folder_path = f'output/'

for item in os.listdir(output_folder_path):
    first_dot = item.find(".")
    second_dot = item.find(".", first_dot+1)
    list_of_rtos_downloaded.append(item[first_dot+1:second_dot])



for rto in rtos:
    if rto in list_of_rtos_downloaded:
        continue
    run_worker("rajasthan", rto, "2022", "L5G", "False")

end_time = time.time()
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")
# RUN CHECKER FILE TO SEE IF ALL RTOS HAVE COME, YET TO INTEGRATE THEM INTO ORCH FILE