echo "Deleting previous queues"
tc qdisc del dev enp6s0 root

echo "Creating queues"
tc qdisc add dev enp6s0 root handle 1: drr
tc class add dev enp6s0 parent 1: classid 1:1 drr quantum 1538
tc class add dev enp6s0 parent 1: classid 1:2 drr quantum 46140
tc class add dev enp6s0 parent 1: classid 1:3 drr quantum 67672

tc qdisc add dev enp6s0 parent 1:2 handle 20: drr
tc class add dev enp6s0 parent 20: classid 20:1 drr quantum 6152
tc class add dev enp6s0 parent 20: classid 20:2 drr quantum 1538

tc qdisc add dev enp6s0 parent 1:3 handle 30: drr
tc class add dev enp6s0 parent 30: classid 30:1 drr quantum 1538000
tc class add dev enp6s0 parent 30: classid 30:2 drr quantum 1538


tc qdisc add dev enp6s0 parent 1:1 handle 10: bfifo limit 1538
tc qdisc add dev enp6s0 parent 20:1 handle 210: bfifo limit 1538
tc qdisc add dev enp6s0 parent 20:2 handle 220: bfifo limit 1538
tc qdisc add dev enp6s0 parent 30:1 handle 310: bfifo limit 1538
tc qdisc add dev enp6s0 parent 30:2 handle 320: bfifo limit 1538

tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.3 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.4 classid 1:2
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.5 classid 1:2
tc filter add dev enp6s0 protocol ip parent 20:0 prio 1 u32 match ip src 10.0.0.2 classid 20:1
tc filter add dev enp6s0 protocol ip parent 20:0 prio 1 u32 match ip src 10.0.0.3 classid 20:1
tc filter add dev enp6s0 protocol ip parent 20:0 prio 1 u32 match ip src 10.0.0.4 classid 20:2
tc filter add dev enp6s0 protocol ip parent 20:0 prio 1 u32 match ip src 10.0.0.5 classid 20:2

tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:3
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.7 classid 1:3
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10 classid 1:3
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.11 classid 1:3
tc filter add dev enp6s0 protocol ip parent 30:0 prio 1 u32 match ip src 10.0.0.6 classid 30:1
tc filter add dev enp6s0 protocol ip parent 30:0 prio 1 u32 match ip src 10.0.0.7 classid 30:1
tc filter add dev enp6s0 protocol ip parent 30:0 prio 1 u32 match ip src 10.0.0.10 classid 30:2
tc filter add dev enp6s0 protocol ip parent 30:0 prio 1 u32 match ip src 10.0.0.11 classid 30:2

tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:1
tc filter add dev enp6s0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:1

tc filter add dev enp6s0 protocol arp parent 1:0 prio 7 u32 match u32 0 0 classid 1:1
