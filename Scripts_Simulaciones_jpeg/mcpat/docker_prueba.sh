#!/bin/bash

cd /gem5/gem5/

declare -a sizes=('1kB' '2kB' '4kB' '8kB' '16kB' '32kB' '64kB' '128kB' '256kB' '512kB' '1024kB' '2048kB' '4096kB' '8192kB' '16384kB' '32768kB' '65536kB' '131072kB' '262144kB' '524288kB')

# Realizar iteraciones
for i in {1..100}
do
    # Select random values for l2_size_str and l1d_size_str from sizes array
    l2_size_str=${sizes[$RANDOM % ${#sizes[@]}]}
    l1d_size_str=${sizes[$RANDOM % ${#sizes[@]}]}

    # Ejecutar el programa y generar el archivo stats.txt
    build/X86/gem5.opt /gem5/gem5/configs/learning_gem5/part1/two_level.py --l2_size="$l2_size_str" --l1d_size="$l1d_size_str"

    # Espera a que gem5 genere el archivo stats.txt
    while [ ! -f /gem5/gem5/m5out/stats.txt ]
    do
        sleep 1
    done

    # Capturar los valores requeridos de stats.txt
    cpi=$(grep "system.cpu.cpi" /gem5/gem5/m5out/stats.txt | awk '{print $2}')
    ipc=$(grep "system.cpu.ipc" /gem5/gem5/m5out/stats.txt | awk '{print $2}')

    # Escribir los valores a un archivo CSV
    echo "$l2_size_str, $l1d_size_str, $cpi, $ipc" >> /gem5/gem5/output.csv

    # Optional: Move or rename stats.txt here if needed for each iteration
done
