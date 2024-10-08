echo "Creating ifb0"
ip link add ifb0 type ifb
ip link set dev ifb0 up

echo "Creating ingress qdisc"
tc qdisc add dev eth1 ingress
tc filter add dev eth1 parent ffff: matchall action mirred egress redirect dev ifb0

echo "Creating HTB"
tc qdisc add dev ifb0 root handle 1: stab overhead 24 htb
tc class add dev ifb0 parent 1: classid 1:1 htb rate 100mbit
tc class add dev ifb0 parent 1:1 classid 1:2 htb rate 36mbit
tc class add dev ifb0 parent 1:2 classid 1:20 htb rate 32mbit
tc class add dev ifb0 parent 1:2 classid 1:21 htb rate 4mbit ceil 36mbit
tc class add dev ifb0 parent 1:1 classid 1:3 htb rate 52.8mbit
tc class add dev ifb0 parent 1:1 classid 1:4 htb rate 1.2mbit
tc class add dev ifb0 parent 1:1 classid 1:5 htb rate 5mbit ceil 100mbit

tc qdisc add dev ifb0 parent 1:20 handle 20: pfifo limit 1
tc qdisc add dev ifb0 parent 1:21 handle 21: pfifo limit 1
tc qdisc add dev ifb0 parent 1:3 handle 30: pfifo limit 1
tc qdisc add dev ifb0 parent 1:4 handle 40: pfifo limit 1
tc qdisc add dev ifb0 parent 1:5 handle 50: pfifo limit 1 

echo "Creating DRR"
tc qdisc add dev eth2 root handle 1: prio
tc qdisc add dev eth2 parent 1:2 handle 10: drr
tc class add dev eth2 parent 10: classid 10:1 drr quantum 15380
tc class add dev eth2 parent 10: classid 10:2 drr quantum 4614
tc class add dev eth2 parent 10: classid 10:3 drr quantum 1538

tc qdisc add dev eth2 parent 1:1 handle 11: bfifo limit 30290
tc qdisc add dev eth2 parent 10:1 handle 100: bfifo limit 117897
tc qdisc add dev eth2 parent 10:2 handle 200: bfifo limit 96342
tc qdisc add dev eth2 parent 10:3 handle 300: bfifo limit 131734


echo "Installing filters"
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:20
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.3 classid 1:20
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.4 classid 1:21
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.5 classid 1:21
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:3
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.7 classid 1:3
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:4
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:4
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10 classid 1:5
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.11 classid 1:5 
tc filter add dev ifb0 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop

tc filter add dev eth2 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:1
tc filter add dev eth2 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:1
tc filter add dev eth2 protocol ip parent 1:0 prio 3 u32 match ip src 10.0.0.0/24 classid 1:2
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.2 classid 10:1
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.3 classid 10:1
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.4 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.5 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.6 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.7 classid 10:2
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.10 classid 10:3
tc filter add dev eth2 protocol ip parent 10:0 prio 5 u32 match ip src 10.0.0.11 classid 10:3
tc filter add dev eth2 protocol ip parent 10:0 prio 6 u32 match ip src 10.0.0.0/24 classid 10:3
tc filter add dev eth2 protocol arp parent 1:0 prio 6 u32 match u32 0 0 classid 1:3
tc filter add dev eth2 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop
