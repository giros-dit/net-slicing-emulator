echo "Creating ifb0"
ip link add ifb0 type ifb
ip link set dev ifb0 up

echo "Creating ingress qdisc"
tc qdisc add dev enp3s0 ingress
tc filter add dev enp3s0 parent ffff: matchall action mirred egress redirect dev ifb0

echo "Deleting previous HTB"
tc qdisc del dev ifb0 root

echo "Creating HTB"
tc qdisc add dev ifb0 root handle 1: htb default 12
tc class add dev ifb0 parent 1: classid 1:1 htb rate 100mbit ceil 100mbit
tc class add dev ifb0 parent 1:1 classid 1:2 htb rate 40mbit ceil 40mbit
tc class add dev ifb0 parent 1:1 classid 1:3 htb rate 20mbit ceil 100mbit prio 5
tc class add dev ifb0 parent 1:1 classid 1:4 htb rate 30mbit ceil 30mbit prio 0
tc class add dev ifb0 parent 1:2 classid 1:10 htb rate 30mbit ceil 30mbit prio 1
tc class add dev ifb0 parent 1:2 classid 1:11 htb rate 8bit ceil 40mbit prio 5 quantum 200000
tc class add dev ifb0 parent 1:1 classid 1:12 htb rate 8bit ceil 100mbit prio 5 quantum 200000

echo "Installing filters"
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.2 classid 1:10
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.7 classid 1:10
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.8 classid 1:10

tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.3 classid 1:11

tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.5 classid 1:3

tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.6 classid 1:4
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.9 classid 1:4
tc filter add dev ifb0 protocol ip parent 1:0 prio 1 u32 match ip src 10.0.0.10 classid 1:4

