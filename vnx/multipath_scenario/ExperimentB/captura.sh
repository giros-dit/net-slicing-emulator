#!/bin/bash

EXP_NAME=$1

echo "Iniciando captura: $EXP_NAME"

mkdir -p capturas
chmod 777 capturas

FILE1="capturas/${EXP_NAME}_PE1-e1.pcap"
FILE2="capturas/${EXP_NAME}_PE2-e2.pcap"
FILE3="capturas/${EXP_NAME}_PE3-e1.pcap"
FILE4="capturas/${EXP_NAME}_PE4-e2.pcap"

wireshark -i PE1-e2 -k -f "udp && !icmp" -w $FILE1 &
PID1=$!

wireshark -i PE2-e2 -k -f "udp && !icmp" -w $FILE2 &
PID2=$!

wireshark -i PE3-e2 -k -f "udp && !icmp" -w $FILE3 &
PID3=$!

wireshark -i PE4-e2 -k -f "udp && !icmp" -w $FILE4 &        
PID4=$!

sleep 15

tcpreplay --intf1=PE1-e1 --intf2=PE3-e1 --dualfile ExperimentB-p1.pcap ExperimentB-p2.pcap &
PID_TPREPLAY1=$!

wait $PID_TPREPLAY1
kill -2 $PID1 $PID2 $PID3 $PID4
wait $PID1 $PID2 $PID3 $PID4

chmod 777 capturas/*

echo "Capturas guardadas como:"
echo "$FILE1"
echo "$FILE2"
echo "$FILE3"
echo "$FILE4"
