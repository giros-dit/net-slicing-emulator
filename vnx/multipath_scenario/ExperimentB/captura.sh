#!/bin/bash

EXP_NAME=$1

echo "Iniciando captura: $EXP_NAME"

mkdir -p capturas
chmod 777 capturas

FILE1="capturas/${EXP_NAME}_PE1-e1.pcap"
FILE2="capturas/${EXP_NAME}_PE2-e2.pcap"
FILE3="capturas/${EXP_NAME}_P1-e3.pcap"

wireshark -i PE1-e1 -k -f "udp && !icmp" -w $FILE1 &
PID1=$!

wireshark -i PE2-e2 -k -f "udp && !icmp" -w $FILE2 &
PID2=$!

wireshark -i P1-e3 -k -f "udp && !icmp" -w $FILE3 &
PID3=$!

sleep 10

tcpreplay --intf1=PE1-e1 --intf2=P1-e3 --dualfile ExperimentB-p1.pcap ExperimentB-p2.pcap &
PID_TPREPLAY1=$!

wait $PID_TPREPLAY1
kill -2 $PID1 $PID2 $PID3
wait $PID1 $PID2 $PID3

echo "Capturas guardadas como:"
echo "$FILE1"
echo "$FILE2"
echo "$FILE3"
