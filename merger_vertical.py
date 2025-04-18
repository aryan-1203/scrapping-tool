import time, os, csv
start_time = time.time()

header_present = False

path = 'merger/input'
output_file_path = 'merger/output/merged_vertically.csv'

holder = []

for file in range(len(os.listdir(path))):
     file_name = f"{os.listdir(path)[file]}"
     file_path = path +"/"+ file_name
     with open(file_path) as data_file:
          rows = list(csv.reader(data_file))
          if not header_present:
               header_present = True
               for row in rows:
                    holder.append(row)
          else:
               count = 0
               for row in rows:
                    if count == 0:
                         count = count +1
                    else:
                         holder.append(row)
                

with open(output_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(holder)


end_time = time.time()
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")