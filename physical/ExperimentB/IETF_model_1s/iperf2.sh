echo "Deleting previous data"
sudo -S rm -rf metrics/*
sudo -S rm -rf test_results/files/*

ssh -f PE1 "
  rm -f clase*
"

sleep 1

for i in {1..4}
do
  echo "$i iteration"

  ssh -f PE1 "
    ./ExperimentB/IETF/PE1_conf_IETF_${i}_.sh
  "

  sleep 1

  echo "Initiating iperf servers"
  sudo -S lxc-attach -n server1 -- iperf -s -u -e -i 1 > metrics5_${i} &
  sudo -S lxc-attach -n server2 -- iperf -s -u -e -i 1 > metrics1_${i} &
  sudo -S lxc-attach -n server3 -- iperf -s -u -e -i 1 > metrics2_${i} &
  sudo -S lxc-attach -n server4 -- iperf -s -u -e -i 1 > metrics3_${i} &
  sudo -S lxc-attach -n server5 -- iperf -s -u -e -i 1 > metrics4_${i} &

  echo "Initiating BE traffic"
  ssh -f PE1 "
    python3 ExperimentB/get_queue_packets.py ${i} &
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
  sudo -S ./latency_server2.sh ${i} metrics1_${i} metrics2_${i} metrics3_${i} metrics4_${i} metrics5_${i}
  sleep 10
done

mv metrics* metrics/

cd test_results
echo "Generating plot"
scp PE1:/root/clase* files/
sudo -S python3 plot.py

echo "Test completed"
