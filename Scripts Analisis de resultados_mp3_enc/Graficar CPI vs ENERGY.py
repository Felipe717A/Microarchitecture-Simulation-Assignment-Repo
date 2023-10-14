import pandas as pd
import matplotlib.pyplot as plt

# Ruta al archivo Excel
archivo_excel = "workload_felipe.xlsx"  # Reemplaza con la ubicación de tu archivo Excel

# Leer el archivo Excel
df = pd.read_excel(archivo_excel)

# Extraer las columnas 'Energy' y 'cpi' del DataFrame
x = df['Energy']
y = df['cpi']

# Calcular los valores extremos (mínimos y máximos) de Energy y cpi
min_energy = x.min()
max_energy = x.max()
min_cpi = y.min()
max_cpi = y.max()
plt.figure(figsize=(12, 8))

# Crear una gráfica de dispersión
plt.scatter(x, y, label='Datos', alpha=0.5)  # alpha controla la transparencia de los puntos

# Resaltar el punto de menor energía con un color y símbolo distintos
plt.scatter(min_energy, min_cpi, color='red', marker='o', s=100, label='Mínima Energía')

# Resaltar el punto de mayor energía con un color y símbolo distintos
plt.scatter(max_energy, max_cpi, color='green', marker='^', s=100, label='Máxima Energía')

# Agregar etiquetas a los ejes
plt.xlabel('Energy')
plt.ylabel('cpi')

# Agregar una leyenda
plt.legend()

# Mostrar la gráfica
plt.show()
