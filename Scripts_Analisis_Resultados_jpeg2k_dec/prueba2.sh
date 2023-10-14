#!/bin/bash

docker run -u $UID:$GID --volume /home/santiago/universidad/arquitectura/scripts/docker_prueba.sh:/gem5/docker_prueba.sh --volume /home/santiago/universidad/arquitectura/gem5:/gem5 --rm gcr.io/gem5-test/ubuntu-20.04_all-dependencies:v22-1 /bin/bash -c "/gem5/docker_prueba.sh"

echo "Terminé"