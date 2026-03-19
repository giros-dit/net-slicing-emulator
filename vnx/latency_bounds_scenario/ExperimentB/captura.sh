#!/bin/bash

echo "Abriendo capturas en Wireshark..."

mkdir -p capturas

wireshark -i PE1-e1 -k -f "udp && !icmp" -w capturas/PE1-e1.pcap &
PID1=$!

wireshark -i PE1-e2 -k -f "udp && !icmp" -w capturas/PE1-e2.pcap &
PID2=$!

wireshark -i P1-e2 -k -f "udp && !icmp" -w capturas/P1-e2.pcap &
PID3=$!

wireshark -i PE2-e2 -k -f "udp && !icmp" -w capturas/PE2-e2.pcap &
PID4=$!

echo "Capturando (UDP) y mostrando (udp and !icmp)..."
echo "Presiona ENTER para detener..."

read

kill $PID1 $PID2 $PID3 $PID4
wait

echo "Capturas guardadas en ./capturas"
