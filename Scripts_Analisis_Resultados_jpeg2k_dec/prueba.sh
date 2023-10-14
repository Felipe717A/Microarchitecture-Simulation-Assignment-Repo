#!/bin/bash

docker run -u $UID:$GID --volume /home/santiago/universidad/arquitectura/gem5:/gem5 --rm gcr.io/gem5-test/ubuntu-20.04_all-dependencies:v22-1 /bin/bash << 'EOF'

cd /gem5/gem5/

l2_size=1024
l1d_size=128

for i in {1..100}
do
    l2_size=$((l2_size + i))
    l1d_size=$((l1d_size + i))
    
    l2_size_str="${l2_size}kB"
    l1d_size_str="${l1d_size}kB"

    sed -i "s/l2_size='[0-9]*kB' --l1d_size='[0-9]*kB'/l2_size='$l2_size_str' --l1d_size='$l1d_size_str'/" /gem5/gem5/configs/learning_gem5/part1/two_level.py

    build/X86/gem5.opt /gem5/gem5/configs/learning_gem5/part1/two_level.py

    cpi=$(grep "system.cpu.cpi" /gem5/gem5/m5out/stats.txt | awk '{print $2}')
    ipc=$(grep "system.cpu.ipc" /gem5/gem5/m5out/stats.txt | awk '{print $2}')

    echo "$l2_size_str, $l1d_size_str, $cpi, $ipc" >> /gem5/gem5/output.csv
done

EOF

echo "Terminé"
