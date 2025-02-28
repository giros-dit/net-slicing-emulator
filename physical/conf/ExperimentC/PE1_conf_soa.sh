echo "Deleting previous qdisc"
tc qdisc del dev enp3s0 ingress
tc qdisc del dev enp4s0 root

echo "Creating ingress qdisc"
tc qdisc add dev enp3s0 ingress

echo "Creating PRIO"
tc qdisc add dev enp4s0 root handle 1: prio

tc qdisc add dev enp4s0 parent 1:1 handle 10: pfifo limit 1000
tc qdisc add dev enp4s0 parent 1:2 handle 20: pfifo limit 1000
tc qdisc add dev enp4s0 parent 1:3 handle 30: pfifo limit 1000


echo "Installing filters"
tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.2 \
    police rate 32mbit burst 50k overhead 38 continue

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.2 \
    action pedit ex munge ip dsfield set 0x04 pipe \
    csum ip and udp pipe \
    police rate 68mbit burst 50k overhead 38 drop

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.4 \
    police rate 4mbit burst 50k overhead 38 continue

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.4 \
    action pedit ex munge ip dsfield set 0x04 pipe \
    csum ip and udp pipe \
    police rate 96mbit burst 50k overhead 38 drop

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.6 \
    police rate 52.8mbit burst 50k overhead 38 continue

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.6 \
    action pedit ex munge ip dsfield set 0x04 pipe \
    csum ip and udp pipe \
    police rate 47.2mbit burst 50k overhead 38 drop

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.8 \
    police rate 1.2mbit burst 50k overhead 38 continue

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.8 \
    action pedit ex munge ip dsfield set 0x04 pipe \
    csum ip and udp pipe \
    police rate 98.8mbit burst 50k overhead 38 drop

tc filter add dev enp3s0 protocol ip parent ffff:fff1 prio 1 u32 \
    match ip src 10.0.0.10 \
    police rate 100mbit burst 50k overhead 38 drop

tc filter add dev enp4s0 protocol ip parent 1:0 prio 1 u32 match ip dsfield 0x04 0xFC classid 1:3
tc filter add dev enp4s0 protocol ip parent 1:0 prio 2 u32 match ip src 10.0.0.10 classid 1:3
tc filter add dev enp4s0 protocol ip parent 1:0 prio 3 u32 match ip src 10.0.0.0/24 classid 1:1
