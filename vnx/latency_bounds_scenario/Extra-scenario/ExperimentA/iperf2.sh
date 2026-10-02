#!/bin/bash

echo "Deleting previous data"
sudo rm -f metrics/*
sudo rm -f test_results/files/*
sudo rm -f PE*.pcap

sleep 1

FILE1="PE1-e2.pcap"
FILE2="PE2-e2.pcap"

wireshark -i PE1-e2 -k -f "udp && !icmp" -w $FILE1 &
PID1=$!

wireshark -i PE2-e2 -k -f "udp && !icmp" -w $FILE2 &
PID2=$!

sleep 10

echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -i 0.1 > metrics1 &
sudo lxc-attach -n server2 -- iperf -s -u -e -i 0.1 > metrics2 &
sudo lxc-attach -n server3 -- iperf -s -u -e -i 0.1 > metrics3 &
sudo lxc-attach -n server4 -- iperf -s -u -e -i 0.1 > metrics4 &
sudo lxc-attach -n server5 -- iperf -s -u -e -i 0.1 > metrics6 &
sudo lxc-attach -n server6 -- iperf -s -u -e -i 0.1 > metrics5 &
sudo lxc-attach -n server7 -- iperf -s -u -e -i 0.1 > metrics1_burst &
sudo lxc-attach -n server8 -- iperf -s -u -e -i 0.1 > metrics2_burst &
sudo lxc-attach -n server9 -- iperf -s -u -e -i 0.1 > metrics3_burst &
sudo lxc-attach -n server10 -- iperf -s -u -e -i 0.1 > metrics4_burst &
sudo lxc-attach -n server11 -- iperf -s -u -e -i 0.1 > metrics5_burst &

sudo lxc-attach -n server13 -- iperf -s -u -e -i 0.1 > metrics7 &
sudo lxc-attach -n server14 -- iperf -s -u -e -i 0.1 > metrics7_burst &
sudo lxc-attach -n server15 -- iperf -s -u -e -i 0.1 > metrics8 &
sudo lxc-attach -n server16 -- iperf -s -u -e -i 0.1 > metrics8_burst &

sudo lxc-attach -n h1 -- iperf -c server1 -u -i 0.1 -b 2490pps -l 1458 -t 60 > metrics1_sender &
sudo lxc-attach -n h3 -- iperf -c server2 -u -i 0.1 -b 827pps -l 1458 -t 60 > metrics2_sender &
sudo lxc-attach -n h5 -- iperf -c server3 -u -i 0.1 -b 2481pps -l 1458 -t 45 > metrics3_sender &
sudo lxc-attach -n h7 -- iperf -c server4 -u -i 0.1 -b 797pps -l 1458 -t 60 > metrics4_sender &
sudo lxc-attach -n h11 -- iperf -c server6 -u -i 0.1 -b 1659pps -l 1458 -t 60 > metrics5_sender &
sudo lxc-attach -n h13 -- iperf -c server13 -u -i 0.1 -b 399pps -l 1458 -t 60 > metrics7_sender &
sudo lxc-attach -n h15 -- iperf -c server15 -u -i 0.1 -b 3721pps -l 1458 -t 60 > metrics8_sender &


sleep 10.062

sudo parallel ::: \
    "sudo lxc-attach -n h2 -- iperf -c server7 -i 0.1 -u --isochronous=0.5:21p --ipg 0.001 -l 1458 -t 50 > metrics1_sender_burst &" \
    "sudo lxc-attach -n h6 -- iperf -c server9 -i 0.1 -u --isochronous=0.2:95p --ipg 0.001 -l 1458 -t 35 > metrics3_sender_burst &" \
    "sudo lxc-attach -n h4 -- iperf -c server8 -i 0.1 -u --isochronous=0.2:31p --ipg 0.001 -l 1458 -t 50 > metrics2_sender_burst &" \
    "sudo lxc-attach -n h8 -- iperf -c server10 -i 0.1 -u --isochronous=1:36p --ipg 0.001 -l 1458 -t 35 > metrics4_sender_burst &" \
    "sudo lxc-attach -n h12 -- iperf -c server11 -i 0.1 -u --isochronous=0.5:14p --ipg 0.001 -l 1458 -t 50 > metrics5_sender_burst &" \
    "sudo lxc-attach -n h14 -- iperf -c server14 -i 0.1 -u --isochronous=1:17p --ipg 0.001 -l 1458 -t 50 > metrics7_sender_burst &" \
    "sudo lxc-attach -n h16 -- iperf -c server16 -i 0.1 -u --isochronous=0.2:143p --ipg 0.001 -l 1458 -t 50 > metrics8_sender_burst &"

sleep 35

sudo lxc-attach -n h9 -- iperf -c server5 -u -i 0.1 -b 2500pps -l 1458 -t 15 > metrics6_sender &

sleep 17

kill -2 $PID1 $PID2
wait $PID1 $PID2

chmod 777 PE*.pcap

echo "Generating files"
sudo ./latency_server2.sh metrics1 metrics2 metrics3 metrics4 metrics5 metrics6 metrics7 metrics8 metrics1_burst metrics2_burst metrics3_burst metrics4_burst metrics5_burst metrics7_burst metrics8_burst
sudo ./bandwidth_server.sh metrics1_sender metrics2_sender metrics3_sender metrics4_sender metrics5_sender metrics6_sender metrics7_sender metrics8_sender metrics1_sender_burst metrics2_sender_burst metrics3_sender_burst metrics4_sender_burst metrics5_sender_burst metrics7_sender_burst metrics8_sender_burst

sleep 10
sudo mv metrics* metrics/

cd test_results

echo "Processing data"
for i in $(seq 1 8); do
    touch "files/bw_metrics${i}"
    touch "files/lat_metrics${i}"
    touch "files/lat_max_metrics${i}"
done

python3 process_data.py

echo "Generating plot"
python3 plot.py 

#cd ..

#echo "Generating packet loss"
#python3 comparation.py

echo "Test completed"
