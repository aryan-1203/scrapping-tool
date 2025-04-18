import os, json

with open('jsons/maharashtra_rtos.json', 'r') as file:
    rtos = json.load(file)

    output_folder_path = f'output/'

list_of_rtos_downloaded = []
list_of_rtos_json = [item for item in rtos]

for item in os.listdir(output_folder_path):
    first_dot = item.find(".")
    second_dot = item.find(".", first_dot+1)
    list_of_rtos_downloaded.append(item[first_dot+1:second_dot])

# if not len(list_of_rtos_downloaded) == len(list_of_rtos_json):
#     print("MISMATCH IN NUMBER OF RTOS")
#     for x,y in zip(list_of_rtos_downloaded, list_of_rtos_json):
#         print("Check:", x, " and ", y)
# else:
#     for x,y in zip(list_of_rtos_downloaded, list_of_rtos_json):
#         if x == y:
#             pass
#         else:
#             print("MISMATCH of ", x, " and ", y)

def missing_rtos(a, b):
    missing = [rto for rto in set(a)-set(b)]
    return missing

for rto in missing_rtos(list_of_rtos_json, list_of_rtos_downloaded):
    print ("Missing RTO:", rto)
