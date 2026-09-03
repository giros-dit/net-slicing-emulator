#!/bin/bash

rm -f capturas/*

lxc-attach -n P2 -- bash ./root/ExperimentC/P2_conf.sh
lxc-attach -n PE2 -- bash ./root/ExperimentC/PE2_conf.sh
lxc-attach -n PE4 -- bash ./root/ExperimentC/PE4_conf.sh

lxc-attach -n P1 -- bash ./root/ExperimentC/P1_conf1.sh
lxc-attach -n PE3 -- bash ./root/ExperimentC/PE3_conf1.sh
echo "==== EXPERIMENTO 1 ===="
./captura.sh exp1 &
CAP_PID=$!

wait $CAP_PID

lxc-attach -n P1 -- bash ./root/ExperimentC/P1_conf2.sh
lxc-attach -n PE3 -- bash ./root/ExperimentC/PE3_conf2.sh
echo "==== EXPERIMENTO 2 ===="
./captura.sh exp2 &
CAP_PID=$!

wait $CAP_PID

echo "==== TODOS LOS EXPERIMENTOS COMPLETADOS ===="

python3 comparation.py
