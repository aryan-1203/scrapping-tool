import pandas as pd
import time
start_time = time.time()

output_file_path = 'merger/output/merged_horizontally.csv'

a = 'merger/input/2022.csv'
b = 'merger/input/2023.csv'
c = 'merger/input/2024.csv'
d = 'merger/input/2025.csv'

def combine(*args):
    dataframes = []
    for arg in args:
        df = pd.read_csv(arg).set_index(['State', 'RTO', 'Variant','OEM'])
        dataframes.append(df)
    df_combined = pd.concat(dataframes, axis=1, join='outer')
    df_combined = df_combined.replace({',': ''}, regex=True) #removing commas
    # Format NaN as 0, convert all floats to integers, format dates as dates (just in case)
    df_combined_filled = df_combined.fillna(0).astype(int).sort_index()
    df_combined_filled.columns = pd.to_datetime(df_combined_filled.columns, errors='raise')
    df_combined_filled.to_csv(output_file_path, na_rep='NA')

combine(c, d)

end_time = time.time()
execution_time = end_time - start_time
minutes = int(execution_time // 60)
seconds = execution_time % 60
print(f"Execution time: {minutes} minutes and {seconds:.2f} seconds")