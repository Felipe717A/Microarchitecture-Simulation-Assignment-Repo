import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

csv_file_path = "/home/santiago/universidad/arquitectura/jpeg2k_dec/output.csv"

df = pd.read_csv(csv_file_path)
df['cpi'] = df['cpi'].astype(float)

exclude_columns = ['ipc', 'Total Leakage', 'Runtime Dynamic', 'unique_id', 'cpi', 'Energy', 'EDP']

max_variation = -1
best_index = -1

for idx, row in df.iterrows():
    total_variation_count = 0
    valid_row = True

    for col in df.columns:
        if col not in exclude_columns:
            mask = (df.loc[:, df.columns != col] == row.loc[df.columns != col]).all(axis=1)
            variations = df[mask & (df[col] != row[col])]

            if variations.empty or (variations['cpi'] == row['cpi']).any():
                valid_row = False
                break

            total_variation_count += variations.shape[0]

    if valid_row and total_variation_count > max_variation:
        max_variation = total_variation_count
        best_index = idx

closest_cpi_index = best_index
closest_cpi_row = df.iloc[closest_cpi_index]

initial_seed_values = {col: closest_cpi_row[col] for col in df.columns if col not in exclude_columns}

print(f"Initial seed values for closest cpi to average:")
for key, value in initial_seed_values.items():
    print(f"{key}: {value}")

print(initial_seed_values.items())

colors = sns.color_palette("pastel")

for i, col in enumerate(initial_seed_values.keys()):
    mask = pd.Series([True] * len(df))
    for other_col in initial_seed_values.keys():
        if other_col != col:
            mask &= (df[other_col] == initial_seed_values[other_col])
    mask &= (df[col] != initial_seed_values[col])
    varied_rows = df[mask].copy()

    if varied_rows.empty:
        continue

    fig, ax = plt.subplots(figsize=(5, 5))

    seed_row = df.iloc[closest_cpi_index].copy()
    seed_row[col] = f"Seed ({seed_row[col]})"
    seed_row_for_plot = pd.DataFrame(seed_row).T
    varied_rows_for_plot = pd.concat([varied_rows, seed_row_for_plot])

    subplot_color = colors[i % len(colors)]
    sns.barplot(x=col, y='cpi', data=varied_rows_for_plot, ax=ax, ci=None, color=subplot_color)
    ax.set_title(f'CPI for varied {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('CPI')

    min_cpi = varied_rows_for_plot['cpi'].min()
    max_cpi = varied_rows_for_plot['cpi'].max()
    ax.set_ylim([min_cpi - (0.01 * abs(min_cpi)), max_cpi + (0.01 * abs(max_cpi))])

    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height - (0.005 * height),
                '{:1.6f}'.format(height),
                ha="center", va='center', color='black', fontsize=10, rotation=90)

    plt.show()
