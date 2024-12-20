sudo ovs-vsctl add-port Net0 enp1s0
sudo ovs-vsctl set port enp1s0 trunks=1000,1001

sudo lxc-attach -n h1 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h1 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h1 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h1 -- sudo ifconfig eth1 0
sudo lxc-attach -n h1 -- sudo ifconfig eth1.1001 10.0.4.2/24
sudo lxc-attach -n h1 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h1 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h2 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h2 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h2 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h2 -- sudo ifconfig eth1 0
sudo lxc-attach -n h2 -- sudo ifconfig eth1.1001 10.0.4.3/24
sudo lxc-attach -n h2 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h2 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h3 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h3 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h3 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h3 -- sudo ifconfig eth1 0
sudo lxc-attach -n h3 -- sudo ifconfig eth1.1001 10.0.4.4/24
sudo lxc-attach -n h3 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h3 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h4 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h4 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h4 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h4 -- sudo ifconfig eth1 0
sudo lxc-attach -n h4 -- sudo ifconfig eth1.1001 10.0.4.5/24
sudo lxc-attach -n h4 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h4 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h5 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h5 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h5 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h5 -- sudo ifconfig eth1 0
sudo lxc-attach -n h5 -- sudo ifconfig eth1.1001 10.0.4.6/24
sudo lxc-attach -n h5 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h5 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h6 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h6 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h6 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h6 -- sudo ifconfig eth1 0
sudo lxc-attach -n h6 -- sudo ifconfig eth1.1001 10.0.4.7/24
sudo lxc-attach -n h6 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h6 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h7 -- sudo ip link add link eth1 name eth1.1000 type vlan id 1000
sudo lxc-attach -n h7 -- sudo ip link set eth1.1000 up
sudo lxc-attach -n h7 -- sudo ip link set eth1.1000 type vlan egress 0:7
sudo lxc-attach -n h7 -- sudo ifconfig eth1 0
sudo lxc-attach -n h7 -- sudo ifconfig eth1.1000 10.0.0.2/24
sudo lxc-attach -n h7 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h7 -- sudo ip route add 0.0.0.0/0 via 10.0.0.1

sudo lxc-attach -n h8 -- sudo ip link add link eth1 name eth1.1000 type vlan id 1000
sudo lxc-attach -n h8 -- sudo ip link set eth1.1000 up
sudo lxc-attach -n h8 -- sudo ip link set eth1.1000 type vlan egress 0:7
sudo lxc-attach -n h8 -- sudo ifconfig eth1 0
sudo lxc-attach -n h8 -- sudo ifconfig eth1.1000 10.0.0.3/24
sudo lxc-attach -n h8 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h8 -- sudo ip route add 0.0.0.0/0 via 10.0.0.1


sudo lxc-attach -n h9 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h9 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h9 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h9 -- sudo ifconfig eth1 0
sudo lxc-attach -n h9 -- sudo ifconfig eth1.1001 10.0.4.8/24
sudo lxc-attach -n h9 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h9 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n h10 -- sudo ip link add link eth1 name eth1.1001 type vlan id 1001
sudo lxc-attach -n h10 -- sudo ip link set eth1.1001 up
sudo lxc-attach -n h10 -- sudo ip link set eth1.1001 type vlan egress 0:1
sudo lxc-attach -n h10 -- sudo ifconfig eth1 0
sudo lxc-attach -n h10 -- sudo ifconfig eth1.1001 10.0.4.9/24
sudo lxc-attach -n h10 -- sudo ip route del 0.0.0.0/0
sudo lxc-attach -n h10 -- sudo ip route add 0.0.0.0/0 via 10.0.4.1

sudo lxc-attach -n P -- sudo ip link add link enxd46e0e08bca7 name enxd.1000 type vlan id 1000
sudo lxc-attach -n P -- sudo ip link set enxd.1000 up
sudo lxc-attach -n P -- sudo ifconfig enxd46e0e08bca7 0
sudo lxc-attach -n P -- sudo ifconfig enxd.1000 10.1.0.2/30
sudo lxc-attach -n P -- sudo ip link add link enxd46e0e08bca7 name enxd.1001 type vlan id 1001
sudo lxc-attach -n P -- sudo ip link set enxd.1001 up
sudo lxc-attach -n P -- sudo ifconfig enxd.1001 10.1.4.2/30
sudo lxc-attach -n P -- ip route del 0.0.0.0/0
sudo lxc-attach -n P -- ip route add 0.0.0.0/0 via 10.1.0.66
sudo lxc-attach -n P -- ip route add 10.0.0.0/24 via 10.1.0.1
sudo lxc-attach -n P -- ip route add 10.0.4.0/24 via 10.1.4.1







