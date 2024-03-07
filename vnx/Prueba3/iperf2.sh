echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -i 1 > latency_h1 &
sudo lxc-attach -n server2 -- iperf -s -u -e -i 1 > latency_h2 &
sudo lxc-attach -n server3 -- iperf -s -u -e -i 1 > latency_h3 &
sudo lxc-attach -n server4 -- iperf -s -u -e -i 1 > latency_h4 &
sudo lxc-attach -n server5 -- iperf -s -u -e -i 1 > latency_h5 &

echo "Initiating Video traffic"
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -b 10M -t 100 &
sleep 20

echo "Initiating BE traffic"
sudo lxc-attach -n h4 -- iperf -c server2 -i 1 -u -b 70M -t 20 &
sleep 20

echo "Initiating uRLLC traffic"
sudo lxc-attach -n h5 -- iperf -c server3 -i 1 -u -b 10M -t 20 &
sleep 20

echo "Initiating Telemetry and eMBB traffic"
sudo lxc-attach -n h2 -- iperf -c server4 -i 1 -u -b 20M -t 20 &
sudo lxc-attach -n h3 -- iperf -c server5 -i 1 -u -b 10M -t 20 &
sleep 50

echo "Generating files"
./latency_server.sh latency_h1
./latency_server2.sh latency_h2 latency_h3 latency_h4 latency_h5
sleep 10
sudo rm -f latency_h1 latency_h2 latency_h3 latency_h4 latency_h5

echo "Generating plot"
cd test3_results
python3 plot2.py

sudo rm -f latency_h2 latency_h3 latency_h4 latency_h5

echo "Test completed"
