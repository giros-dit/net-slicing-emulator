echo "Deleting PRIO queues"
tc qdisc del dev enxd46e0e08bca7 root
tc qdisc del dev enxd46e0e069255 root

echo "Creating PRIO queues"
tc qdisc add dev enxd46e0e08bca7 root handle 1: prio #Creates automatically classes 1:1, 1:2, 1:3
tc qdisc add dev enxd46e0e069255 root handle 1: prio #Creates automatically classes 1:1, 1:2, 1:3

echo "Installing filters"
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:1
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 5 u32 match ip src 10.0.0.0/24 classid 1:3
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.7 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:1
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10 classid 1:1

tc filter add dev enxd46e0e08bca7 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.2 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.7 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.8 classid 1:2
tc filter add dev enxd46e0e08bca7 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.6 classid 1:1
tc filter add dev enxd46e0e08bca7 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.9 classid 1:1
tc filter add dev enxd46e0e08bca7 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.0.10 classid 1:1
tc filter add dev enxd46e0e08bca7 protocol ip parent 1:0 prio 5 u32 match ip dst 10.0.0.0/24 classid 1:3
