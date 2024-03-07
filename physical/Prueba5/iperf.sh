echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -i 1 > HP_equal &
sudo lxc-attach -n server2 -- iperf -s -u -e -i 1 > LP_equal &
sudo lxc-attach -n server3 -- iperf -s -u -e -i 1 > HP_aggressive &
sudo lxc-attach -n server4 -- iperf -s -u -e -i 1 > LP_aggressive &

echo "Test with BW pre-defined"
sudo lxc-attach -n h2 -q -- iperf -c server2 -i 1 -u -b 100M -t 80 &
sleep 25
sudo lxc-attach -n h1 -q -- iperf -c server1 -i 1 -u -b 100M -t 30 &
sleep 60

echo "Changing configuration to the same priority"
sleep 120

echo "Start second test"
sleep 10

echo "Test with BW share aggressive"
sudo lxc-attach -n h2 -- iperf -c server4 -i 1 -u -b 100M -t 80 &
sleep 25
sudo lxc-attach -n h1 -- iperf -c server3 -i 1 -u -b 100M -t 30 &
sleep 60

echo "Generating files"
sudo ./bandwidth_server.sh HP_equal LP_equal HP_aggressive LP_aggressive
sleep 10

echo "Vectorizing files"
cd test5_results
./vectorization.sh bandwidth_HP_equal 25 25
./vectorization.sh bandwidth_HP_aggressive 25 25
sleep 10

echo "Generating plot"
python3 plot.py

echo "Deleting files generated"
sudo rm -f bandwidth_HP_equal bandwidth_HP_aggressive
cd ..
sudo rm -f HP_equal LP_equal HP_aggressive LP_aggressive

echo "Test completed"
