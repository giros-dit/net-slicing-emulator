#!/bin/bash

lxc-attach -n P1 -- bash ./root/ExperimentA/P1_conf1.sh
echo "==== EXPERIMENTO 1 ===="
./captura.sh exp1 &
CAP_PID=$!

wait $CAP_PID

lxc-attach -n P1 -- bash ./root/ExperimentA/P1_conf2.sh
echo "==== EXPERIMENTO 2 ===="
./captura.sh exp2 &
CAP_PID=$!

wait $CAP_PID

echo "==== TODOS LOS EXPERIMENTOS COMPLETADOS ===="

python3 comparation.py
