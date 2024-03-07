echo "Initiating iperf servers"
sudo lxc-attach -n server2 -- iperf -s -u -e -i 1 &
sudo lxc-attach -n server1 -- iperf -s -u -e -i 1 &

echo "Test with URLLC Traffic at 1 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 1M -t 20 -e > latency_h5_1Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_1Mbps &
sleep 25

echo "Test with URLLC Traffic at 3 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 3M -t 20 -e > latency_h5_3Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_3Mbps &
sleep 25

echo "Test with URLLC Traffic at 5 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 5M -t 20 -e > latency_h5_5Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_5Mbps &
sleep 25

echo "Test with URLLC Traffic at 10 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 10M -t 20 -e > latency_h5_10Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_10Mbps &
sleep 25

echo "Test with URLLC Traffic at 20 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 20M -t 20 -e > latency_h5_20Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_20Mbps &
sleep 25

echo "Test with URLLC Traffic at 40 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 40M -t 20 -e > latency_h5_40Mbps &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_40Mbps &
sleep 25

echo "Test with different priorities completed"

echo "Changing configuration to the same priority"
sleep 120

echo "Start second test"
sleep 10

echo "Test with URLLC Traffic at 1 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 1M -t 20 -e > latency_h5_1Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_1Mbps_2 &
sleep 30

echo "Test with URLLC Traffic at 3 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 3M -t 20 -e > latency_h5_3Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_3Mbps_2 &
sleep 30

echo "Test with URLLC Traffic at 5 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 5M -t 20 -e > latency_h5_5Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_5Mbps_2 &
sleep 30

echo "Test with URLLC Traffic at 10 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 10M -t 20 -e > latency_h5_10Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_10Mbps_2 &
sleep 30

echo "Test with URLLC Traffic at 20 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 20M -t 20 -e > latency_h5_20Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_20Mbps_2 &
sleep 30

echo "Test with URLLC Traffic at 40 Mbps"
sudo lxc-attach -n h5 -- iperf -c server2 -i 1 -u -b 40M -t 20 -e > latency_h5_40Mbps_2 &
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -e -b 1M -t 20 > latency_h1_40Mbps_2 &
sleep 30

echo "Generating files"
sudo ./latency_h5.sh h5 latency_h5_1Mbps latency_h5_3Mbps latency_h5_5Mbps latency_h5_10Mbps latency_h5_20Mbps latency_h5_40Mbps
sudo ./latency_h5.sh h1 latency_h1_1Mbps latency_h1_3Mbps latency_h1_5Mbps latency_h1_10Mbps latency_h1_20Mbps latency_h1_40Mbps
sudo ./latency_h5.sh h5_equal latency_h5_1Mbps_2 latency_h5_3Mbps_2 latency_h5_5Mbps_2 latency_h5_10Mbps_2 latency_h5_20Mbps_2 latency_h5_40Mbps_2
sudo ./latency_h5.sh h1_equal latency_h1_1Mbps_2 latency_h1_3Mbps_2 latency_h1_5Mbps_2 latency_h1_10Mbps_2 latency_h1_20Mbps_2 latency_h1_40Mbps_2
sleep 10

echo "Generating plot"
cd test4_results
pip install matplotlib
python3 plot.py

echo "Deleting files generated"
cd ..
sudo rm -f latency_h1_* latency_h5_*

echo "Test completed"
