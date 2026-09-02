echo "Deleting previous qdisc"
tc qdisc del dev eth2 root

echo "Creating DRR"
tc qdisc add dev eth2 root handle 1: htb
tc class add dev eth2 parent 1: classid 1:1 htb rate 200mbit burst 200b
tc qdisc add dev eth2 parent 1:1 handle 2: prio
tc qdisc add dev eth2 parent 2:2 handle 20: drr
tc class add dev eth2 parent 20: classid 20:1 drr quantum 3000
tc class add dev eth2 parent 20: classid 20:2 drr quantum 1500

tc qdisc add dev eth2 parent 2:1 handle 10: bfifo limit 97000
tc qdisc add dev eth2 parent 20:1 handle 100: bfifo limit 303000
tc qdisc add dev eth2 parent 20:2 handle 200: bfifo limit 300000
tc qdisc add dev eth2 parent 2:3 handle 300: bfifo limit 603000


echo "Installing filters"
tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/24 classid 1:1
tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.3.0.0/24 classid 1:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.6/31 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.3.0.6/31 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/24 classid 2:2
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.3.0.0/24 classid 2:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.2/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.3.0.2/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.4/31 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.3.0.4/31 classid 20:2
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.8/31 classid 2:3
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.3.0.8/31 classid 2:3

tc filter add dev eth2 protocol arp parent 2:0 prio 7 u32 match u32 0 0 classid 2:3
