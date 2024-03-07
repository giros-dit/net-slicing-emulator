echo "Deleting previous PRIO queues"
tc qdisc del dev enp5s0 root
tc qdisc del dev enp6s0 root

echo "Creating PRIO queues"
tc qdisc add dev enp5s0 root handle 1: prio #Creates automatically classes 1:1, 1:2, 1:3
tc qdisc add dev enp6s0 root handle 1: prio #Creates automatically classes 1:1, 1:2, 1:3

echo "Installing filters"
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:1
tc filter add dev enp6s0 protocol ip parent 1:0 prio 5 u32 match ip src 10.0.0.0/24 classid 1:3

tc filter add dev enp5s0 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.2 classid 1:2
tc filter add dev enp5s0 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.6 classid 1:1
tc filter add dev enp5s0 protocol ip parent 1:0 prio 5 u32 match ip dst 10.0.0.0/24 classid 1:3
