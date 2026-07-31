echo "Creating ifb0"
ip link add ifb0 type ifb
ip link set dev ifb0 up

echo "Creating ingress qdisc"
tc qdisc del dev eth3 ingress
tc qdisc add dev eth3 ingress
tc filter add dev eth3 parent ffff: matchall action mirred egress redirect dev ifb0

echo "Deleting previous qdisc"
tc qdisc del dev ifb0 root
tc qdisc del dev eth2 root

echo "Creating HTB"
tc qdisc add dev ifb0 root handle 1: htb
tc class add dev ifb0 parent 1: classid 1:1 htb rate 100mbit burst 1b
tc class add dev ifb0 parent 1:1 classid 1:2 htb rate 70mbit ceil 100mbit 
tc class add dev ifb0 parent 1:2 classid 1:20 htb rate 60mbit ceil 100mbit burst 148453b cburst 148453b quantum 1500
tc class add dev ifb0 parent 1:2 classid 1:21 htb rate 10mbit ceil 100mbit burst 59200b cburst 59200b quantum 1500
tc class add dev ifb0 parent 1:1 classid 1:3 htb rate 30mbit ceil 100mbit 
tc class add dev ifb0 parent 1:3 classid 1:30 htb rate 1kbit ceil 100mbit quantum 1500
tc class add dev ifb0 parent 1:3 classid 1:31 htb rate 30mbit ceil 100mbit burst 165226b cburst 165226b quantum 1500

tc qdisc add dev ifb0 parent 1:20 handle 20: pfifo limit 1
tc qdisc add dev ifb0 parent 1:21 handle 21: pfifo limit 1
tc qdisc add dev ifb0 parent 1:30 handle 30: pfifo limit 1
tc qdisc add dev ifb0 parent 1:31 handle 31: pfifo limit 1




echo "Creating DRR"
tc qdisc add dev eth2 root handle 1: htb
tc class add dev eth2 parent 1: classid 1:1 htb rate 200mbit burst 200b
tc class add dev eth2 parent 1:1 classid 1:2 htb rate 100mbit ceil 200mbit burst 100b cburst 100b
tc class add dev eth2 parent 1:1 classid 1:3 htb rate 100mbit ceil 200mbit burst 100b cburst 100b

tc qdisc add dev eth2 parent 1:2 handle 2: prio
tc qdisc add dev eth2 parent 2:2 handle 20: drr
tc class add dev eth2 parent 20: classid 20:1 drr quantum 3000
tc class add dev eth2 parent 20: classid 20:2 drr quantum 1500

tc qdisc add dev eth2 parent 2:1 handle 10: bfifo limit 35850
tc qdisc add dev eth2 parent 20:1 handle 100: bfifo limit 112420
tc qdisc add dev eth2 parent 20:2 handle 200: bfifo limit 112960
tc qdisc add dev eth2 parent 2:3 handle 300: bfifo limit 225000

tc qdisc add dev eth2 parent 1:3 handle 3: prio
tc qdisc add dev eth2 parent 3:2 handle 30: drr
tc class add dev eth2 parent 30: classid 30:1 drr quantum 3000
tc class add dev eth2 parent 30: classid 30:2 drr quantum 1500

tc qdisc add dev eth2 parent 3:1 handle 11: bfifo limit 60850
tc qdisc add dev eth2 parent 30:1 handle 101: bfifo limit 191420
tc qdisc add dev eth2 parent 30:2 handle 201: bfifo limit 188000
tc qdisc add dev eth2 parent 3:3 handle 301: bfifo limit 344380


echo "Installing filters"
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.3.0.2/31 classid 1:20
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.3.0.6/31 classid 1:31
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.3.0.8/31 classid 1:21
tc filter add dev ifb0 protocol ip parent 1:0 prio 2 u32 match ip src 10.3.0.0/24 classid 1:30
tc filter add dev ifb0 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop

tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/8 classid 1:1

tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/24 classid 1:2
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.8/31 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/24 classid 2:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.2/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.12/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.4/31 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.6/31 classid 20:2
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.10/31 classid 2:3
tc filter add dev eth2 protocol ip parent 20:0 prio 6 u32 match ip src 10.0.0.0/24 classid 2:3


tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.3.0.0/24 classid 1:3
tc filter add dev eth2 protocol ip parent 3:0 prio 1 u32 match ip src 10.3.0.8/31 classid 3:1
tc filter add dev eth2 protocol ip parent 3:0 prio 3 u32 match ip src 10.3.0.0/24 classid 3:2
tc filter add dev eth2 protocol ip parent 30:0 prio 5 u32 match ip src 10.3.0.2/31 classid 30:1
tc filter add dev eth2 protocol ip parent 30:0 prio 5 u32 match ip src 10.3.0.12/31 classid 30:1
tc filter add dev eth2 protocol ip parent 30:0 prio 5 u32 match ip src 10.3.0.4/31 classid 30:2
tc filter add dev eth2 protocol ip parent 30:0 prio 5 u32 match ip src 10.3.0.6/31 classid 30:2
tc filter add dev eth2 protocol ip parent 3:0 prio 1 u32 match ip src 10.3.0.10/31 classid 3:3
tc filter add dev eth2 protocol ip parent 30:0 prio 6 u32 match ip src 10.3.0.0/24 classid 30:3
tc filter add dev eth2 protocol arp parent 2:0 prio 7 u32 match u32 0 0 classid 2:3
