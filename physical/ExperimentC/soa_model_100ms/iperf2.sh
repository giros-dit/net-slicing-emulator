echo "Deleting previous data"
sudo -S rm -rf metrics/*
sudo -S rm -rf test_results/files/*

#ssh -f PE1 "
 # rm -f clase*
#"

sleep 1

ssh -f PE1 "
  ./ExperimentC/PE1_conf_soa.sh
"

sleep 1

echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -p 5001 -i 0.1 > metrics1 &
sudo lxc-attach -n server2 -- iperf -s -u -e -p 5001 -i 0.1 > metrics2 &
sudo lxc-attach -n server3 -- iperf -s -u -e -p 5001 -i 0.1 > metrics3 &
sudo lxc-attach -n server4 -- iperf -s -u -e -p 5001 -i 0.1 > metrics4  &
sudo lxc-attach -n server5 -- iperf -s -u -e -p 5001 -i 0.1 > metrics5 &
sudo lxc-attach -n server1 -- iperf -s -u -e -p 5002 -i 0.1 > metrics1_burst &
sudo lxc-attach -n server2 -- iperf -s -u -e -p 5002 -i 0.1 > metrics2_burst &
sudo lxc-attach -n server3 -- iperf -s -u -e -p 5002 -i 0.1 > metrics3_burst &
sudo lxc-attach -n server4 -- iperf -s -u -e -p 5002 -i 0.1 > metrics4_burst &
#sudo lxc-attach -n server5 -- iperf -s -u -e -p 5002 -i 0.1 > metrics5_burst &

#ssh -f PE1 "
 #   python3 ExperimentC/get_queue_packets.py &
#"

#Each 5G QoS class transmits at a lower rate than its CIR

sudo lxc-attach -n h1 -- iperf -c server1 -p 5001 -u -i 0.1 -b 250pps -l 1472 -t 60 > metrics1_sender &
sudo lxc-attach -n h3 -- iperf -c server2 -p 5001 -u -i 0.1 -b 250pps -l 1472 -t 60 > metrics2_sender &
sudo lxc-attach -n h5 -- iperf -c server3 -p 5001 -u -i 0.1 -b 250pps -l 1472 -t 60 > metrics3_sender &
sudo lxc-attach -n h7 -- iperf -c server4 -p 5001 -u -i 0.1 -b 50pps -l 1472 -t 60 > metrics4_sender &
sudo lxc-attach -n h9 -- iperf -c server5 -u -i 0.1 -b 100M -l 1472 -t 60 > metrics5_sender &

sleep 10

#Each 5G QoS class transmits 50kbytes of burst traffic
sudo lxc-attach -n h2 -- iperf -c server1 -p 5002 -i 0.1 -u --isochronous=0.5:65p --ipg 0.001 -l 1472 -t 50 > metrics1_sender_burst &
sudo lxc-attach -n h4 -- iperf -c server2 -p 5002 -i 0.1 -u --isochronous=0.2:65p --ipg 0.001 -l 1472 -t 50 > metrics2_sender_burst &
sudo lxc-attach -n h6 -- iperf -c server3 -p 5002 -i 0.1 -u --isochronous=0.2:65p --ipg 0.001 -l 1472 -t 50 > metrics3_sender_burst &
sudo lxc-attach -n h8 -- iperf -c server4 -p 5002 -i 0.1 -u --isochronous=1:65p --ipg 0.001 -l 1472 -t 35 > metrics4_sender_burst &
#sudo lxc-attach -n h10 -- iperf -c server5 -p 5002 -i 0.1 -u --isochronous=0.1:30p --ipg 0.001 -l 1472 -t 50 > metrics5_sender_burst

sleep 55

echo "Generating files"
sudo ./latency_server2.sh metrics1 metrics2 metrics3 metrics4 metrics5 metrics1_burst metrics2_burst metrics3_burst metrics4_burst
#metrics5_burst
sudo ./bandwidth_server.sh metrics1_sender metrics2_sender metrics3_sender metrics4_sender metrics5_sender metrics1_sender_burst metrics2_sender_burst metrics3_sender_burst metrics4_sender_burst 
#metrics5_sender_burst

sleep 10
cd metrics/
sudo mv ../metrics* .

cd ../test_results

echo "Processing data"
for i in $(seq 1 5); do
    touch "files/bw_metrics${i}"
    touch "files/lat_metrics${i}"
    touch "files/lat_max_metrics${i}"
done

python3 process_data.py


echo "Generating plot"
#scp PE1:/root/clase* files/
python3 plot.py

echo "Test completed"
