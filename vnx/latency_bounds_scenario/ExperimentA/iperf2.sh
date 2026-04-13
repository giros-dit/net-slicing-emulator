echo "Deleting previous data"
sudo -S rm -rf metrics/*
sudo -S rm -rf test_results/files/*

mkdir -p metrics
mkdir -p test_results/files
chmod 744 metrics
chmod 744 test_results/files

sleep 1

echo "Initiating iperf servers"
sudo lxc-attach -n server1 -- iperf -s -u -e -i 0.1 > metrics1 &
sudo lxc-attach -n server2 -- iperf -s -u -e -i 0.1 > metrics2 &
sudo lxc-attach -n server3 -- iperf -s -u -e -i 0.1 > metrics3 &
sudo lxc-attach -n server4 -- iperf -s -u -e -i 0.1 > metrics4 &
sudo lxc-attach -n server5 -- iperf -s -u -e -i 0.1 > metrics6 &
sudo lxc-attach -n server6 -- iperf -s -u -e -i 0.1 > metrics5 &
sudo lxc-attach -n server7 -- iperf -s -u -e -i 0.1 > metrics1_burst &
sudo lxc-attach -n server8 -- iperf -s -u -e -i 0.1 > metrics2_burst &
sudo lxc-attach -n server9 -- iperf -s -u -e -i 0.1 > metrics3_burst &
sudo lxc-attach -n server10 -- iperf -s -u -e -i 0.1 > metrics4_burst &
sudo lxc-attach -n server11 -- iperf -s -u -e -i 0.1 > metrics5_burst &

sudo lxc-attach -n h1 -- iperf -c server1 -u -i 0.1 -b 2490pps -l 1458 -t 60 > metrics1_sender &
sudo lxc-attach -n h3 -- iperf -c server2 -u -i 0.1 -b 828pps -l 1458 -t 60 > metrics2_sender &
sudo lxc-attach -n h5 -- iperf -c server3 -u -i 0.1 -b 2488pps -l 1458 -t 45 > metrics3_sender &
sudo lxc-attach -n h7 -- iperf -c server4 -u -i 0.1 -b 809pps -l 1458 -t 60 > metrics4_sender &
sudo lxc-attach -n h11 -- iperf -c server6 -u -i 0.1 -b 1659pps -l 1458 -t 60 > metrics5_sender &

sleep 10.062

sudo parallel ::: \
    "sudo lxc-attach -n h2 -- iperf -c server7 -i 0.1 -u --isochronous=0.5:19p --ipg 0.001 -l 1458 -t 50 > metrics1_sender_burst &" \
    "sudo lxc-attach -n h6 -- iperf -c server9 -i 0.1 -u --isochronous=0.2:55p --ipg 0.001 -l 1458 -t 35 > metrics3_sender_burst &" \
    "sudo lxc-attach -n h4 -- iperf -c server8 -i 0.1 -u --isochronous=0.2:18p --ipg 0.001 -l 1458 -t 50 > metrics2_sender_burst &" \
    "sudo lxc-attach -n h8 -- iperf -c server10 -i 0.1 -u --isochronous=1:23p --ipg 0.001 -l 1458 -t 35 > metrics4_sender_burst &" \
    "sudo lxc-attach -n h12 -- iperf -c server11 -i 0.1 -u --isochronous=0.5:13p --ipg 0.001 -l 1458 -t 50 > metrics5_sender_burst &"

sleep 35

sudo lxc-attach -n h9 -- iperf -c server5 -u -i 0.1 -b 2500pps -l 1458 -t 15 > metrics6_sender &

sleep 17

echo "Generating files"
sudo ./latency_server2.sh metrics1 metrics2 metrics3 metrics4 metrics5 metrics6 metrics1_burst metrics2_burst metrics3_burst metrics4_burst metrics5_burst
sudo ./bandwidth_server.sh metrics1_sender metrics2_sender metrics3_sender metrics4_sender metrics5_sender metrics6_sender metrics1_sender_burst metrics2_sender_burst metrics3_sender_burst metrics4_sender_burst metrics5_sender_burst

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
python3 plot.py

echo "Test completed"
