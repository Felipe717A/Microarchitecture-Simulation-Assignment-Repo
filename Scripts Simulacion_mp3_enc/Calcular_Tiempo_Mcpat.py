# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 16:30:37 2023

@author: felip
"""

import time
import subprocess

# Función para ejecutar un comando en la terminal
def ejecutar_comando(comando):
    start_time = time.time()
    try:
        subprocess.run(comando, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

# Comando 1
comando1 = "python2 gem5toMcPAT_cortexA76.py stats.txt config.json ARM_A76_2.1GHz.xml"
tiempo_comando1 = ejecutar_comando(comando1)
print(f"Comando 1 tomó {tiempo_comando1:.2f} segundos en ejecutarse.")

# Comando 2
comando2 = "./mcpat -infile config.xml > power_data.log"
tiempo_comando2 = ejecutar_comando(comando2)
print(f"Comando 2 tomó {tiempo_comando2:.2f} segundos en ejecutarse.")
