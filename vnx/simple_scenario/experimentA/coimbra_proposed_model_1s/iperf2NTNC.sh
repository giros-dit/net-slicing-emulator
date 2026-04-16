sudo rm -rf test_results/files/*
sudo rm -rf metrics/*

ssh -f root@10.250.0.6 "
  rm -f clase*
"

sleep 1

ssh -f root@10.250.0.6"
  ./satGNB_conf-coimbraC.sh
"

sleep 1

echo "Initiating iperf servers"
sudo -S lxc-attach -n serverNTN1 -- iperf -s -u -e -i 1 > metricsSNTN1 &
sudo -S lxc-attach -n serverNTN2 -- iperf -s -u -e -i 1 > metricsSNTN2 &
sudo -S lxc-attach -n serverNTN3 -- iperf -s -u -e -i 1 > metricsSNTN3 &
sudo -S lxc-attach -n serverNTN4 -- iperf -s -u -e -i 1 > metricsSNTN4 &
sudo -S lxc-attach -n serverNTN5 -- iperf -s -u -e -i 1 > metricsSNTN5 &


echo "Initiating BE traffic"
ssh -f root@10.250.0.6 "
  python3 get_queue_packets.py &
"
sudo -S lxc-attach -n hNTN6 -- iperf -c serverNTN6 -i 1 -u -b 100M -l 1472 -t 100 &
sleep 20

echo "Initiating Video and Telemetry traffic"
sudo -S lxc-attach -n hNTN1 -- iperf -c serverNTN2 -i 1 -u -b 100M -l 1472 -t 40 &
sudo -S lxc-attach -n hNTN2 -- iperf -c serverNTN3 -i 1 -u -b 100M -l 1472 -t 60 &
sleep 20

echo "Initiating eMBB traffic"
sudo -S lxc-attach -n hNTN4 -- iperf -c serverNTN4 -i 1 -u -b 100M -l 1472 -t 30 &
echo "Initiating uRLLC traffic"
sudo -S lxc-attach -n hNTN5 -- iperf -c serverNTN5 -i 1 -u -b 100M -l 1472 -t 40 &
sleep 70

echo "Generating files"
sudo -S ./latency_server2.sh metricsSNTN1 metricsSNTN2 metricsSNTN3 metricsSNTN4 metricsSNTN5
sleep 10
mv metrics* ./metrics/

cd test_results
echo "Generating plot"
scp root@10.250.0.6:/root/clase* files/
sudo -S python3 plot.py

echo "Test completed"
