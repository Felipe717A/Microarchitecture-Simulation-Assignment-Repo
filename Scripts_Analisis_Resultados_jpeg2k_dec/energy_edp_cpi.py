import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = "/home/santiago/universidad/arquitectura/jpeg2k_dec/output.csv"
df = pd.read_csv(csv_file_path)

energy = df['Energy']
ipc = df['cpi']
edp = df['EDP']

min_energy_point = (energy.min(), ipc[energy.idxmin()])
min_ipc_point = (energy[ipc.idxmin()], ipc.min())
min_edp_point = (energy[edp.idxmin()], ipc[edp.idxmin()])

plt.figure(figsize=(10, 7))
plt.scatter(energy, ipc, label='Data Points', s=40, alpha=0.5)
plt.scatter(*min_energy_point, color='red', label='Min Energy', s=100, zorder=5)
plt.scatter(*min_ipc_point, color='blue', label='Min CPI', s=100, zorder=5)
plt.scatter(*min_edp_point, color='green', label='Min EDP', s=100, zorder=5)

annotations = ['Min Energy', 'Min CPI', 'Min EDP']
points = [min_energy_point, min_ipc_point, min_edp_point]
offsets = [(20, -10), (20, -10), (20, 10)]

for annotation, point, offset in zip(annotations, points, offsets):
    plt.annotate(f'{annotation}\n({point[0]:.2f}, {point[1]:.2f})', point, xytext=offset, textcoords='offset points', arrowprops=dict(arrowstyle='->'))

plt.xlabel('Energy')
plt.ylabel('CPI')
plt.title('CPI vs Energy with EDP indication')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()