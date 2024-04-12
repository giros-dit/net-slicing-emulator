echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -i 1 > metrics1 &
sudo lxc-attach -n server2 -- iperf -s -u -e -i 1 > metrics2 &
sudo lxc-attach -n server3 -- iperf -s -u -e -i 1 > metrics3 &
sudo lxc-attach -n server4 -- iperf -s -u -e -i 1 > metrics4 &
sudo lxc-attach -n server5 -- iperf -s -u -e -i 1 > metrics5 &

echo "Initiating BE traffic"
sudo lxc-attach -n h3 -- iperf -c server4 -i 1 -u -b 100M -t 120 &
sleep 20

echo "Initiating Vídeo traffic"
sudo lxc-attach -n h1 -- iperf -c server1 -i 1 -u -b 100M -t 40 &
sleep 20

echo "Initiating Telemetry, eMBB and URLLC traffic"
sudo lxc-attach -n h2 -- iperf -c server2 -i 1 -u -b 100M -t 40 &
sudo lxc-attach -n h5 -- iperf -c server5 -i 1 -u -b 100M -t 40 &
sudo lxc-attach -n h4 -- iperf -c server3 -i 1 -u -b 100M -t 60 &
sleep 80



echo "Generating files"
sudo ./latency_server2.sh metrics1 metrics2 metrics3 metrics4 metrics5
sleep 10
#sudo rm -f metrics*

cd test2_results

echo "Generating plot"
python3 plot2.py

sudo rm -f latency_metrics2 latency_metrics1 latency_metrics3 latency_metrics5 latency_max_metrics2 latency_max_metrics1 latency_max_metrics3 latency_max_metrics5 bandwidth_metrics2 bandwidth_metrics1 bandwidth_metrics3 bandwidth_metrics5 
echo "Test completed"
