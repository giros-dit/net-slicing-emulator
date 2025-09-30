echo "Creating ifb0"
ip link add ifb0 type ifb
ip link set dev ifb0 up

echo "Creating ingress qdisc"
tc qdisc add dev eth1 ingress
tc filter add dev eth1 parent ffff: matchall action mirred egress redirect dev ifb0

echo "Deleting previous qdisc"
tc qdisc del dev ifb0 root
tc qdisc del dev eth2 root

echo "Creating HTB"
tc qdisc add dev ifb0 root handle 1: htb
tc class add dev ifb0 parent 1: classid 1:1 htb rate 100mbit
tc class add dev ifb0 parent 1:1 classid 1:2 htb rate 50mbit ceil 100mbit
tc class add dev ifb0 parent 1:2 classid 1:20 htb rate 30mbit ceil 100mbit burst 31624b cburst 31624b quantum 1514
tc class add dev ifb0 parent 1:2 classid 1:21 htb rate 20mbit ceil 100mbit burst 58500b cburst 58500b quantum 1514
tc class add dev ifb0 parent 1:1 classid 1:3 htb rate 30mbit ceil 100mbit
tc class add dev ifb0 parent 1:3 classid 1:30 htb rate 10mbit ceil 10mbit burst 32250b cburst 32250b quantum 1514 
tc class add dev ifb0 parent 1:3 classid 1:31 htb rate 20mbit ceil 100mbit burst 21083b cburst 21083b quantum 1514
tc class add dev ifb0 parent 1:1 classid 1:4 htb rate 20mbit ceil 100mbit
tc class add dev ifb0 parent 1:4 classid 1:40 htb rate 20mbit ceil 100mbit burst 58500b cburst 58500b quantum 1514
tc class add dev ifb0 parent 1:4 classid 1:41 htb rate 3kbit ceil 100000mbit quantum 1514

tc qdisc add dev ifb0 parent 1:20 handle 20: pfifo limit 1
tc qdisc add dev ifb0 parent 1:21 handle 21: pfifo limit 1
tc qdisc add dev ifb0 parent 1:30 handle 30: pfifo limit 1
tc qdisc add dev ifb0 parent 1:40 handle 40: pfifo limit 1
tc qdisc add dev ifb0 parent 1:41 handle 41: pfifo limit 1
tc qdisc add dev ifb0 parent 1:31 handle 31: pfifo limit 1

echo "Creating DRR"
# Set Link Speed
tc qdisc add dev eth2 root handle 1: htb 
tc class add dev eth2 parent 1: classid 1:1 htb rate 100mbit
# Set priority and DRR queues
tc qdisc add dev eth2 parent 1:1 handle 2: prio
tc qdisc add dev eth2 parent 2:2 handle 20: drr
tc class add dev eth2 parent 20: classid 20:1 drr quantum 1875
tc class add dev eth2 parent 20: classid 20:2 drr quantum 1500
#tc class add dev eth2 parent 20: classid 20:3 drr quantum 0	TC does not allow to set a quantum of 0

tc qdisc add dev eth2 parent 2:1 handle 10: pfifo limit 1000
tc qdisc add dev eth2 parent 20:1 handle 100: pfifo limit 47
tc qdisc add dev eth2 parent 20:2 handle 200: pfifo limit 88
tc qdisc add dev eth2 parent 2:3 handle 23: pfifo limit 1000

echo "Installing filters"
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2/31 classid 1:20
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.4/31 classid 1:21
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6/31 classid 1:40
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8/31 classid 1:30
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10/31 classid 1:41
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.12/31 classid 1:31
tc filter add dev ifb0 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop


tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/24 classid 1:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.8 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.9 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/24 classid 2:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.2 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.3 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.12 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.13 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.4 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.5 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.6 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.7 classid 20:2
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.10 classid 2:3
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.11 classid 2:3
tc filter add dev eth2 protocol ip parent 20:0 prio 6 u32 match ip src 10.0.0.0/24 classid 20:3
tc filter add dev eth2 protocol arp parent 2:0 prio 6 u32 match u32 0 0 classid 2:3
