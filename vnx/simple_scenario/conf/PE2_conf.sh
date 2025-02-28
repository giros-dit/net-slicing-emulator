echo "Creating Hierarchical DRR"
#Set Link Speed
tc qdisc add dev eth2 root handle 1: htb
tc class add dev eth2 parent 1: classid 1:1 htb rate 1gbit

#Set Hierarchical DRR
tc qdisc add dev eth2 parent 1:1 handle 10: drr
tc class add dev eth2 parent 10: classid 10:1 drr quantum 1538
tc class add dev eth2 parent 10: classid 10:2 drr quantum 1538
tc class add dev eth2 parent 10: classid 10:3 drr quantum 1538

tc qdisc add dev eth2 parent 10:2 handle 200: drr
tc class add dev eth2 parent 200: classid 200:1 drr quantum 1538
tc class add dev eth2 parent 200: classid 200:2 drr quantum 1538

tc qdisc add dev eth2 parent 10:3 handle 300: drr
tc class add dev eth2 parent 300: classid 300:1 drr quantum 1538
tc class add dev eth2 parent 300: classid 300:2 drr quantum 1538

tc qdisc add dev eth2 parent 10:1 handle 100: bfifo limit 1538
tc qdisc add dev eth2 parent 200:1 handle 210: bfifo limit 1538
tc qdisc add dev eth2 parent 200:2 handle 220: bfifo limit 1538
tc qdisc add dev eth2 parent 300:1 handle 310: bfifo limit 1538
tc qdisc add dev eth2 parent 300:2 handle 320: bfifo limit 1538

echo "Installing filters"
tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/24 classid 1:1
tc filter add dev eth2 protocol arp parent 1:0 prio 7 u32 match u32 0 0 classid 1:1

tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.2 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.3 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.4 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.5 classid 10:2
tc filter add dev eth2 protocol ip parent 200:0 prio 1 u32 match ip src 10.0.0.2 classid 200:1
tc filter add dev eth2 protocol ip parent 200:0 prio 1 u32 match ip src 10.0.0.3 classid 200:1
tc filter add dev eth2 protocol ip parent 200:0 prio 1 u32 match ip src 10.0.0.4 classid 200:2
tc filter add dev eth2 protocol ip parent 200:0 prio 1 u32 match ip src 10.0.0.5 classid 200:2

tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.6 classid 10:3
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.7 classid 10:3
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.10 classid 10:3
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.11 classid 10:3
tc filter add dev eth2 protocol ip parent 300:0 prio 1 u32 match ip src 10.0.0.6 classid 300:1
tc filter add dev eth2 protocol ip parent 300:0 prio 1 u32 match ip src 10.0.0.7 classid 300:1
tc filter add dev eth2 protocol ip parent 300:0 prio 1 u32 match ip src 10.0.0.10 classid 300:2
tc filter add dev eth2 protocol ip parent 300:0 prio 1 u32 match ip src 10.0.0.11 classid 300:2

tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.8 classid 10:1
tc filter add dev eth2 protocol ip parent 10:0 prio 1 u32 match ip src 10.0.0.9 classid 10:1
tc filter add dev eth2 protocol arp parent 10:0 prio 7 u32 match u32 0 0 classid 10:1

tc filter add dev eth2 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop
