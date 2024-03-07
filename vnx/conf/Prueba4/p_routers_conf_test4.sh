echo "Creating PRIO queues"
tc qdisc add dev eth2 root handle 1: prio bands 3 #Creates automatically classes 1:1, 1:2, 1:3
tc qdisc add dev eth1 root handle 1: prio bands 3 #Creates automatically classes 1:1, 1:2, 1:3

echo "Installing filters"
tc filter add dev eth2 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:1
tc filter add dev eth2 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:1
tc filter add dev eth2 protocol ip parent 1:0 prio 5 u32 match ip src 10.0.0.0/24 classid 1:2

tc filter add dev eth1 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.2 classid 1:1
tc filter add dev eth1 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.6 classid 1:1
tc filter add dev eth1 protocol ip parent 1:0 prio 5 u32 match ip dst 10.0.0.0/24 classid 1:2
