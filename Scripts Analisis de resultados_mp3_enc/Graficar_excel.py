# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 11:52:53 2023

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ruta al archivo Excel
archivo_excel = "workload_felipe.xlsx"  # Reemplaza con la ubicación de tu archivo Excel

# Leer el archivo Excel
df = pd.read_excel(archivo_excel)


# Seleccionar la fila 34 como referencia
fila_referencia = df.iloc[33, :11]  # Columnas hasta la 11, los índices comienzan desde 0

# Crear una lista para almacenar los índices de las filas que cumplen con la condición
filas_que_cumplen = []

columnas_cambiadas = []

# Iterar fila por fila
for index, fila in df.iterrows():
    cambios = 0
    
    # Compara los valores de la fila actual con la fila de referencia
    for columna in range(11):  # Iterar desde la columna 0 hasta la columna 10
        if fila[columna] != fila_referencia[columna]:
            cambios += 1
            columna_cambiada = columna
    
    # Si hay solo un cambio en la fila, guarda el índice en la lista de filas que cumplen
    if cambios == 1:
        filas_que_cumplen.append(index)
        columnas_cambiadas.append(columna_cambiada)


# Crear una lista con los valores únicos en columnas_cambiadas
valores_unicos = set(columnas_cambiadas)
columna2=[]
columna3=[]
count=0
colores = plt.cm.viridis(np.linspace(0.5, 1, len(valores_unicos)))
# Iterar sobre los valores únicos
for valor in valores_unicos:
    repeticiones = columnas_cambiadas.count(valor)  # Contar repeticiones de un valor
    print(f"El valor {valor} se repite {repeticiones} veces en columnas_cambiadas.")
    
    # Obtener las posiciones correspondientes en filas_que_cumplen
    posiciones = [i for i, v in enumerate(columnas_cambiadas) if v == valor]
    
    # Imprimir las posiciones
    for pos in posiciones:
        valor_cambiado = str(df.iloc[filas_que_cumplen[pos]-1, columnas_cambiadas[pos]])
        columna2.append(valor_cambiado)
        valor_cambiado=float(df.iloc[filas_que_cumplen[pos]-1, 16])
        columna3.append(valor_cambiado)
        print(f"En filas_que_cumplen, la posición correspondiente es {pos}")
    columna2.append(str(df.iloc[32, columnas_cambiadas[pos]]))
    columna3.append(float((df.iloc[32, 16])))
    print(columna2)
    print(columna3)
    factor_de_escala = 100
    columna3_escalada = [((valor) * factor_de_escala)-118.8  for valor in columna3]
    
    plt.figure(figsize=(12, 8))
    plt.bar(columna2,columna3_escalada, width=0.5, color=colores[count])
    for i, valor in enumerate(columna3):
        plt.text(i, valor , f'{valor}', ha='center', va='top')
    nombres_columnas = str(df.columns[columnas_cambiadas[pos]])
    plt.xlabel(nombres_columnas)
    plt.ylabel('CPI')
    plt.ylim(1,1.4 )
    
    plt.show()
    columna2=[]
    columna3=[]
    count+=1

