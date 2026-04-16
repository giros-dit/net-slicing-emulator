sudo rm -rf test_results/filesTN/*
sudo rm -rf metrics/*

ssh -f root@10.250.0.2 "
  rm -f clase*
"

sleep 1

ssh -f root@10.250.0.2 "
  ./PE1_conf-coimbra.sh
"

sleep 1

serverTN1="10.2.0.2"
serverTN2="10.2.0.3"
serverTN3="10.2.0.4"
serverTN4="10.2.0.5"
serverTN5="10.2.0.6"


echo "Initiating iperf servers"
sudo -S lxc-attach -n serverTN1 -- iperf -s -u -e -i 1 > metricsSTN1 &
sudo -S lxc-attach -n serverTN2 -- iperf -s -u -e -i 1 > metricsSTN2 &
sudo -S lxc-attach -n serverTN3 -- iperf -s -u -e -i 1 > metricsSTN3 &
sudo -S lxc-attach -n serverTN4 -- iperf -s -u -e -i 1 > metricsSTN4 &
sudo -S lxc-attach -n serverTN5 -- iperf -s -u -e -i 1 > metricsSTN5 &


ssh -f root@10.250.0.2 "
  python3 pktloss-policerPE1.py TN &
"

echo "Initiating BE traffic"
sudo -S lxc-attach -n hTN5 -- iperf -c $serverTN5 -i 1 -u -b 100M -l 1472 -t 110 &

echo "Initiating Video and Telemetry traffic"
sudo -S lxc-attach -n hTN1 -- iperf -c $serverTN1 -i 1 -u -b 100M -l 1472 -t 110 &
sudo -S lxc-attach -n hTN2 -- iperf -c $serverTN2 -i 1 -u -b 100M -l 1472 -t 110 &

echo "Initiating eMBB traffic"
sudo -S lxc-attach -n hTN3 -- iperf -c $serverTN3 -i 1 -u -b 100M -l 1472 -t 110 &
echo "Initiating uRLLC traffic"
sudo -S lxc-attach -n hTN4 -- iperf -c $serverTN4 -i 1 -u -b 100M -l 1472 -t 110 &
sleep 120
echo "Generating files"
sudo -S ./latency_server2TN.sh metricsSTN1 metricsSTN2 metricsSTN3 metricsSTN4 metricsSTN5
sleep 10
mv metricsSTN* ./metrics/

cd test_results
echo "Generating plot"
scp root@10.250.0.2:/root/clase* filesTN/
sudo -S python3 plotTN.py

echo "Test completed"
