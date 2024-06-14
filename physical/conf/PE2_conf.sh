echo "Deleting previous PRIO queues"
tc qdisc del dev enp6s0 root

echo "Creating queues"
tc qdisc add dev enp6s0 root handle 1: drr
tc class add dev enp6s0 parent 1: classid 1:1 drr quantum 1
tc class add dev enp6s0 parent 1: classid 1:2 drr quantum 1
tc class add dev enp6s0 parent 1: classid 1:3 drr quantum 1
tc class add dev enp6s0 parent 1: classid 1:4 drr quantum 1

tc qdisc add dev enp6s0 parent 1:2 handle 20: drr
tc class add dev enp6s0 parent 20: classid 20:1 drr quantum 1
tc class add dev enp6s0 parent 20: classid 20:2 drr quantum 1

tc qdisc add dev enp6s0 parent 1:1 handle 10: bfifo limit 1538
tc qdisc add dev enp6s0 parent 1:3 handle 30: bfifo limit 1538
tc qdisc add dev enp6s0 parent 1:4 handle 40: bfifo limit 1538
tc qdisc add dev enp6s0 parent 20:1 handle 210: bfifo limit 1538
tc qdisc add dev enp6s0 parent 20:2 handle 220: bfifo limit 1538


tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.3 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.4 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.5 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 10:1
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 10:1
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 10:3
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.7 classid 10:3
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10 classid 10:4
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.11 classid 10:4

tc filter add dev enp6s0 protocol ip parent 10:0 prio 3 u32 match ip src 10.0.0.2 classid 10:1
tc filter add dev enp6s0 protocol ip parent 10:0 prio 3 u32 match ip src 10.0.0.3 classid 10:1
tc filter add dev enp6s0 protocol ip parent 10:0 prio 3 u32 match ip src 10.0.0.4 classid 10:2
tc filter add dev enp6s0 protocol ip parent 10:0 prio 3 u32 match ip src 10.0.0.5 classid 10:2

tc filter add dev enp6s0 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop

