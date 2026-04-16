sudo rm -rf test_results/files/*

ssh -f PE1 "
  rm -f clase*
"

sleep 1

ssh -f PE1 "
  ./ExperimentA/PE1_conf_alternative_sharing.sh
"

sleep 1

echo "Initiating iperf servers"
sudo -S lxc-attach -n server1 -- iperf -s -u -e -i 1 > metrics5 &
sudo -S lxc-attach -n server2 -- iperf -s -u -e -i 1 > metrics1 &
sudo -S lxc-attach -n server3 -- iperf -s -u -e -i 1 > metrics2 &
sudo -S lxc-attach -n server4 -- iperf -s -u -e -i 1 > metrics3 &
sudo -S lxc-attach -n server5 -- iperf -s -u -e -i 1 > metrics4 &


echo "Initiating BE traffic"
ssh -f PE1 "
  python3 ExperimentA/get_queue_packets.py &
"
sudo -S lxc-attach -n h9 -- iperf -c server1 -i 1 -u -b 100M -l 1472 -t 100 &
sleep 20

echo "Initiating Video and Telemetry traffic"
sudo -S lxc-attach -n h1 -- iperf -c server2 -i 1 -u -b 100M -l 1472 -t 40 &
sudo -S lxc-attach -n h3 -- iperf -c server3 -i 1 -u -b 100M -l 1472 -t 60 &
sleep 20

echo "Initiating eMBB traffic"
sudo -S lxc-attach -n h5 -- iperf -c server4 -i 1 -u -b 100M -l 1472 -t 30 &
echo "Initiating uRLLC traffic"
sudo -S lxc-attach -n h7 -- iperf -c server5 -i 1 -u -b 100M -l 1472 -t 40 &
sleep 70

echo "Generating files"
sudo -S ./latency_server2.sh metrics1 metrics2 metrics3 metrics4 metrics5
sleep 10
sudo -S mv metrics* ./files_metrics/

cd test_results
echo "Generating plot"
scp PE1:/root/clase* files/
sudo -S python3 plot.py

echo "Test completed"
