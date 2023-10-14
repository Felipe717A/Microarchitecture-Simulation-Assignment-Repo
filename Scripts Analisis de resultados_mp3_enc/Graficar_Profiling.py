import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'stats.txt'

with open(file_path, 'r') as f:
    lines = f.readlines()

columns = []
values = []

prefix = "system.cpu.commitStats0.committedInstType"
for line in lines:
    line = line.strip()
    if line.startswith(prefix) and "::" in line:
        parts = line.split()
        col_name = parts[0].split('::')[1]  # get the part after '::'
        value = parts[1]
        if value != '0' and col_name != "total":
            columns.append(col_name)
            values.append(value)

df = pd.DataFrame({
    'Instruction Type': columns,
    'Value': values
})

df['Value'] = df['Value'].astype(float)

total_value = df['Value'].sum()
df['Percentage'] = (df['Value'] / total_value) * 100

df = df[df['Percentage'] >= 0.5]

sns.set_style("whitegrid")
colors = sns.color_palette("hls", len(df['Instruction Type']))

plt.figure(figsize=(14, 8))
bar_plot = sns.barplot(x="Instruction Type", y="Percentage", data=df, palette=colors)
plt.title('Instruction Type Distribution Percentage', fontsize=15)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel('Instruction Type', fontsize=12)
plt.ylabel('Percentage', fontsize=12)

plt.tight_layout()
plt.show()

csv_path = 'output.csv'
df[['Instruction Type', 'Percentage']].T.to_csv(csv_path, header=False, index=False)

print(f"CSV file created at '{csv_path}'")
