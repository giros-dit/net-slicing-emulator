sudo rm -rf test_results/filesNTNC/*
sudo rm -rf metricsC/*

ssh -f root@10.250.0.6 "
  rm -f clase*
"

sleep 1

ssh -f root@10.250.0.6 "
  ./satGNB_conf-coimbraC.sh
"

hNTN1="20.0.0.2"
hNTN2="20.0.0.3"
hNTN3="20.0.0.4"
hNTN4="20.0.0.5"
hNTN5="20.0.0.6"

serverNTN1="20.2.0.2"
serverNTN2="20.2.0.3"
serverNTN3="20.2.0.4"
serverNTN4="20.2.0.5"
serverNTN5="20.2.0.6"

sleep 1

echo "Initiating iperf servers"
sudo -S lxc-attach -n serverNTN1 -- iperf -s -u -e -i 1 > metricsSNTN1 &
sudo -S lxc-attach -n serverNTN2 -- iperf -s -u -e -i 1 > metricsSNTN2 &
sudo -S lxc-attach -n serverNTN3 -- iperf -s -u -e -i 1 > metricsSNTN3 &
sudo -S lxc-attach -n serverNTN4 -- iperf -s -u -e -i 1 > metricsSNTN4 &
sudo -S lxc-attach -n serverNTN5 -- iperf -s -u -e -i 1 > metricsSNTN5 &


echo "Initiating BE traffic"
ssh -f root@10.250.0.6 "
  python3 pktloss-policerGNBC.py NTN &
"

#:<< 'EOF'
sudo -S lxc-attach -n hNTN5 -- iperf -c $serverNTN5 -i 1 -u -b 100M -l 1472 -t 110 &

echo "Initiating Video and Telemetry traffic"
sudo -S lxc-attach -n hNTN1 -- iperf -c $serverNTN1 -i 1 -u -b 100M -l 1472 -t 110 &
sudo -S lxc-attach -n hNTN2 -- iperf -c $serverNTN2 -i 1 -u -b 100M -l 1472 -t 110 &

echo "Initiating eMBB traffic"
sudo -S lxc-attach -n hNTN3 -- iperf -c $serverNTN3 -i 1 -u -b 100M -l 1472 -t 110 &
echo "Initiating uRLLC traffic"
sudo -S lxc-attach -n hNTN4 -- iperf -c $serverNTN4 -i 1 -u -b 100M -l 1472 -t 110 &
sleep 120
echo "Generating files"
sudo -S ./latency_server2NTN.sh metricsSNTN1 metricsSNTN2 metricsSNTN3 metricsSNTN4 metricsSNTN5
sleep 10
mv metricsSNTN* ./metricsC/

cd test_results
echo "Generating plot"
scp root@10.250.0.6:/root/clase* filesNTNC/
sudo -S python3 plotNTNC.py

echo "Test completed"
#EOF
