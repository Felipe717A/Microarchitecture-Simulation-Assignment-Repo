import pandas as pd

csv_file_path = "workload_felipe2.xlsx"
df = pd.read_excel(csv_file_path)

# Best Performance
best_performance_config = df.loc[df['cpi'].idxmin()]
print("Best Performance Configuration:")
print(best_performance_config)

best_performance_config.to_csv('best_performance_config.csv', header=True)

# Best Energy
best_energy_config = df.loc[df['Energy'].idxmin()]
print("\nBest Energy Configuration:")
print(best_energy_config)

best_energy_config.to_csv('best_energy_config.csv', header=True)

# Best EDP
best_edp_config = df.loc[df['EDP'].idxmin()]
print("\nBest EDP Configuration:")
print(best_edp_config)

best_edp_config.to_csv('best_edp_config.csv', header=True)
