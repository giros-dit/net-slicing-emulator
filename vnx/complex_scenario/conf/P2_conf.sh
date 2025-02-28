echo "Creating DRR"
tc qdisc add dev eth2 root handle 1: htb
tc class add dev eth2 parent 1: classid 1:1 htb rate 1gbit
tc qdisc add dev eth2 parent 1:1 handle 2: prio
tc qdisc add dev eth2 parent 2:3 handle 20: drr
tc class add dev eth2 parent 20: classid 20:1 drr quantum 1538
tc class add dev eth2 parent 20: classid 20:2 drr quantum 1538
tc class add dev eth2 parent 20: classid 20:3 drr quantum 1538

tc qdisc add dev eth2 parent 2:1 handle 10: bfifo limit 1538
tc qdisc add dev eth2 parent 20:1 handle 100: bfifo limit 1538
tc qdisc add dev eth2 parent 20:2 handle 200: bfifo limit 1538
tc qdisc add dev eth2 parent 20:3 handle 300: bfifo limit 1538

#tc qdisc add dev eth3 root handle 1: htb
#tc class add dev eth3 parent 1: classid 1:1 htb rate 100mbit
#tc qdisc add dev eth3 parent 1:1 handle 2: prio
#tc qdisc add dev eth3 parent 2:3 handle 20: drr
#tc class add dev eth3 parent 20: classid 20:1 drr quantum 1538
#tc class add dev eth3 parent 20: classid 20:2 drr quantum 1538
#tc class add dev eth3 parent 20: classid 20:3 drr quantum 1538

#tc qdisc add dev eth3 parent 2:1 handle 10: bfifo limit 1538
#tc qdisc add dev eth3 parent 20:1 handle 100: bfifo limit 1538
#tc qdisc add dev eth3 parent 20:2 handle 200: bfifo limit 1538
#tc qdisc add dev eth3 parent 20:3 handle 300: bfifo limit 1538


echo "Installing filters"
tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/16 classid 1:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.1.8 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.1.9 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.2.8 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.2.9 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/16 classid 2:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.2 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.3 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.2 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.3 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.4 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.5 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.6 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.7 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.4 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.5 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.6 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.7 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.10 classid 20:3
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.11 classid 20:3
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.10 classid 20:3
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.11 classid 20:3
tc filter add dev eth2 protocol ip parent 20:0 prio 6 u32 match ip src 10.0.0.0/16 classid 20:3
tc filter add dev eth2 protocol arp parent 2:0 prio 6 u32 match u32 0 0 classid 2:3
tc filter add dev eth2 protocol ip parent 2:0 prio 7 u32 match ip src 0/0 action drop

#tc filter add dev eth3 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/16 classid 1:1
#tc filter add dev eth3 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.1.8 classid 2:1
#tc filter add dev eth3 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.1.9 classid 2:1
#tc filter add dev eth3 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.2.8 classid 2:1
#tc filter add dev eth3 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.2.9 classid 2:1
#tc filter add dev eth3 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/16 classid 2:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.2 classid 20:1
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.3 classid 20:1
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.2 classid 20:1
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.3 classid 20:1
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.4 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.5 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.6 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.7 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.4 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.5 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.6 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.7 classid 20:2
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.10 classid 20:3
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.1.11 classid 20:3
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.10 classid 20:3
#tc filter add dev eth3 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.2.11 classid 20:3
#tc filter add dev eth3 protocol ip parent 20:0 prio 6 u32 match ip src 10.0.0.0/16 classid 20:3
#tc filter add dev eth3 protocol arp parent 2:0 prio 6 u32 match u32 0 0 classid 2:3
#tc filter add dev eth3 protocol ip parent 2:0 prio 7 u32 match ip src 0/0 action drop
