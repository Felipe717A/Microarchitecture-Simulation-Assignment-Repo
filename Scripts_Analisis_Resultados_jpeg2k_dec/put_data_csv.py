import os
import pandas as pd

power_data_folder = "/home/santiago/universidad/arquitectura/jpeg2k_dec/power"

csv_file_path = "/home/santiago/universidad/arquitectura/jpeg2k_dec/output.csv"

df = pd.read_csv(csv_file_path)

df.columns = [col.strip() for col in df.columns]
df['unique_id'] = df['unique_id'].str.strip()

print(df.head())

df['Total Leakage'] = None
df['Runtime Dynamic'] = None

def extract_power_data(file_path):
    total_leakage = None
    runtime_dynamic = None
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if "Total Leakage" in line:
                total_leakage = float(line.split('=')[1].split('W')[0].strip())
            if "Runtime Dynamic" in line:
                runtime_dynamic = float(line.split('=')[1].split('W')[0].strip())
                if total_leakage is not None:
                    break
    return str(total_leakage), str(runtime_dynamic)

for index, row in df.iterrows():
    power_data_file = os.path.join(power_data_folder, f"power_data_{row['unique_id']}.log")

    if os.path.exists(power_data_file):
        total_leakage, runtime_dynamic = extract_power_data(power_data_file)
        df.at[index, 'Total Leakage'] = total_leakage
        df.at[index, 'Runtime Dynamic'] = runtime_dynamic

df.to_csv(csv_file_path, index=False)