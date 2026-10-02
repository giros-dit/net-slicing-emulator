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
tc class add dev ifb0 parent 1: classid 1:1 htb rate 150mbit burst 1b
tc class add dev ifb0 parent 1:1 classid 1:2 htb rate 40mbit ceil 150mbit 
tc class add dev ifb0 parent 1:2 classid 1:20 htb rate 30mbit ceil 150mbit burst 30872b cburst 30872b quantum 1500
tc class add dev ifb0 parent 1:2 classid 1:21 htb rate 10mbit ceil 150mbit burst 46314b cburst 46314b quantum 1500
tc class add dev ifb0 parent 1:1 classid 1:3 htb rate 30mbit ceil 150mbit 
tc class add dev ifb0 parent 1:3 classid 1:30 htb rate 10mbit ceil 10mbit burst 54686b cburst 54686b quantum 1500
tc class add dev ifb0 parent 1:3 classid 1:31 htb rate 20mbit ceil 150mbit burst 20081b cburst 20081b quantum 1500
tc class add dev ifb0 parent 1:1 classid 1:4 htb rate 30mbit ceil 150mbit 
tc class add dev ifb0 parent 1:4 classid 1:40 htb rate 30mbit ceil 150mbit burst 141944b cburst 141944b quantum 1500
tc class add dev ifb0 parent 1:4 classid 1:41 htb rate 1kbit ceil 150mbit quantum 1500
tc class add dev ifb0 parent 1:1 classid 1:5 htb rate 30mbit ceil 150mbit 
tc class add dev ifb0 parent 1:5 classid 1:50 htb rate 5mbit ceil 5mbit burst 26593b cburst 26593b quantum 1500
tc class add dev ifb0 parent 1:5 classid 1:51 htb rate 45mbit ceil 150mbit burst 213667b cburst 213667b quantum 1500

tc qdisc add dev ifb0 parent 1:20 handle 20: pfifo limit 1
tc qdisc add dev ifb0 parent 1:21 handle 21: pfifo limit 1
tc qdisc add dev ifb0 parent 1:30 handle 30: pfifo limit 1
tc qdisc add dev ifb0 parent 1:40 handle 40: pfifo limit 1
tc qdisc add dev ifb0 parent 1:41 handle 41: pfifo limit 1
tc qdisc add dev ifb0 parent 1:31 handle 31: pfifo limit 1
tc qdisc add dev ifb0 parent 1:50 handle 50: pfifo limit 1
tc qdisc add dev ifb0 parent 1:51 handle 51: pfifo limit 1


echo "Creating DRR"
# Set Link Speed
tc qdisc add dev eth2 root handle 1: htb 
tc class add dev eth2 parent 1: classid 1:1 htb rate 500mbit
# Set priority and DRR queues
tc qdisc add dev eth2 parent 1:1 handle 2: prio
tc qdisc add dev eth2 parent 2:2 handle 20: drr
tc class add dev eth2 parent 20: classid 20:1 drr quantum 1500
tc class add dev eth2 parent 20: classid 20:2 drr quantum 2550
#tc class add dev eth2 parent 20: classid 20:3 drr quantum 0	TC does not allow to set a quantum of 0

tc qdisc add dev eth2 parent 2:1 handle 10: bfifo limit 84429
tc qdisc add dev eth2 parent 20:1 handle 100: bfifo limit 86492
tc qdisc add dev eth2 parent 20:2 handle 200: bfifo limit 467521
tc qdisc add dev eth2 parent 2:3 handle 23: bfifo limit 551035

echo "Installing filters"
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2/31 classid 1:20
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.4/31 classid 1:21
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6/31 classid 1:40
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8/31 classid 1:30
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.12/31 classid 1:31
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10/31 classid 1:41
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.14/31 classid 1:50
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.16/31 classid 1:51
tc filter add dev ifb0 protocol ip parent 1:0 prio 7 u32 match ip src 0/0 action drop

tc filter add dev eth2 protocol ip parent 1:0 prio 0 u32 match ip src 10.0.0.0/24 classid 1:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.8/31 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.14/31 classid 2:1
tc filter add dev eth2 protocol ip parent 2:0 prio 3 u32 match ip src 10.0.0.0/24 classid 2:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.2/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.12/31 classid 20:1
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.4/31 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.6/31 classid 20:2
tc filter add dev eth2 protocol ip parent 20:0 prio 5 u32 match ip src 10.0.0.16/31 classid 20:2
tc filter add dev eth2 protocol ip parent 2:0 prio 1 u32 match ip src 10.0.0.10/31 classid 2:3
tc filter add dev eth2 protocol ip parent 20:0 prio 6 u32 match ip src 10.0.0.0/24 classid 2:3
tc filter add dev eth2 protocol arp parent 2:0 prio 0 u32 match u32 0 0 classid 2:3
