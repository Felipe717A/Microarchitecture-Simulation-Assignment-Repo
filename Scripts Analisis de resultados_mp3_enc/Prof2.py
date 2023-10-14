import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_file_path = "workload_felipe.xlsx"
df = pd.read_excel(csv_file_path)

metrics = ['cpi', 'ipc', 'TotalLeakage (W)', 'RuntimeDynamic (W)', 'Energy', 'EDP']
parameter_columns = [col for col in df.columns if col not in metrics + ['#ID']]
pastel_colors = sns.color_palette("pastel")

def generate_enhanced_bar_charts(df, parameter_columns, metrics, colors):
    df_melted = df.melt(id_vars=metrics, value_vars=parameter_columns)

    # Create an order column to ensure consistent bar grouping
    df_melted['order'] = df_melted['variable'] + df_melted['value'].astype(str)
    df_melted = df_melted.sort_values('order')

    for metric in metrics:
        plt.figure(figsize=(28, 24))

        # Set the order for x-axis based on the created order column
        sns.barplot(data=df_melted, x='order', y=metric, hue='variable', palette=colors, edgecolor='black')
        plt.title(f'{metric} by Parameters', fontsize=10)
        plt.xlabel('Parameter Value', fontsize=8)
        plt.ylabel(metric, fontsize=8)
        plt.tick_params(axis='both', labelsize=5)

        # Adjusting y-axis limits
        y_min = min(df[metric])
        y_max = max(df[metric]) + 0.05 * (max(df[metric]) - min(df[metric]))  # 5% more than the maximum value
        plt.ylim(y_min, y_max)

        bars = plt.gca().patches
        for bar in bars:
            height = bar.get_height()
            plt.gca().annotate(f'{height:.4f}',
                               (bar.get_x() + bar.get_width() / 2, height - 0.01),
                               ha='center', va='top', fontsize=7, fontweight='bold', rotation=90)

        # Clean up x-axis labels
        x_labels = [label.split('_')[-1] for label in df_melted['order'].unique()]
        plt.xticks(plt.xticks()[0], x_labels)

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.gca().set_axisbelow(True)

        # Move legend to upper right
        plt.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig(f"{metric}_vs_parameters_enhanced_barchart.png")
        plt.show()

generate_enhanced_bar_charts(df, parameter_columns, metrics, pastel_colors)
