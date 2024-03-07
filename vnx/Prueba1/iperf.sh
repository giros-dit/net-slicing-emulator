echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -i 1 > server1 &
sudo lxc-attach -n server2 -- iperf -s -u -i 1 > server2 &
sudo lxc-attach -n server3 -- iperf -s -u -i 1 > server3 &
sudo lxc-attach -n server4 -- iperf -s -u -i 1 > server4 &

echo "Initiating BE traffic"
sudo lxc-attach -n h4 -q -- iperf -c server1 -i 1 -u -b 100M -t 100 &
sleep 20

echo "Initiating Video and Telemetry traffic"
sudo lxc-attach -n h1 -q -- iperf -c server2 -i 1 -u -b 100M -t 60 &
sudo lxc-attach -n h2 -q -- iperf -c server3 -i 1 -u -b 100M -t 60 &
sleep 20

echo "Initiating uRLLC traffic"
sudo lxc-attach -n h5 -q -- iperf -c server4 -i 1 -u -b 100M -t 20 &
sleep 70

echo "Generating files"
./bandwidth_server.sh server1 server2 server3 server4
sleep 10
sudo rm -f server1 server2 server3 server4

echo "Vectorizing files"
cd test1_results
./vectorization.sh bandwidth_server2 20 20
./vectorization.sh bandwidth_server3 20 20
./vectorization.sh bandwidth_server4 40 40
sleep 10
sudo rm -f bandwidth_server2 bandwidth_server3 bandwidth_server4

echo "Generating plot"
pip install matplotlib
python3 plot.py

echo "Test completed"
