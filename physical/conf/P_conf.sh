echo "Deleting previous queues"
tc qdisc del dev enxd46e0e069255 root

echo "Creating DRR"
tc qdisc add dev enxd46e0e069255 root handle 1: prio
tc qdisc add dev enxd46e0e069255 parent 1:2 handle 10: drr
tc class add dev enxd46e0e069255 parent 10: classid 10:1 drr quantum 1
tc class add dev enxd46e0e069255 parent 10: classid 10:2 drr quantum 1
tc class add dev enxd46e0e069255 parent 10: classid 10:3 drr quantum 1

tc qdisc add dev enxd46e0e069255 parent 1:1 handle 10: bfifo 1538
tc qdisc add dev ifb0 parent 10:1 handle 100: bfifo 1538
tc qdisc add dev ifb0 parent 10:2 handle 200: bfifo 1538
tc qdisc add dev ifb0 parent 10:3 handle 300: bfifo 1538


echo "Installing filters"
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:1
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:1
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 3 u32 match ip src 10.0.0.0/24 classid 1:2
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.2 classid 10:1
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.3 classid 10:1
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.4 classid 10:2
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.5 classid 10:2
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.6 classid 10:2
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.7 classid 10:2
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.10 classid 10:3
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.11 classid 10:3
tc filter add dev enxd46e0e069255 protocol ip parent 10:0 prio 6 u32 match ip src 10.0.0.0/24 classid 10:3
tc filter add dev enxd46e0e069255 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop
