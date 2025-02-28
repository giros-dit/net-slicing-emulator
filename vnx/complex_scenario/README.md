To generate traffic the following commands should be applied:

ip vrf exec pe1/pe2/pe3/pe4 iperf ...

or

ip vrf exec pe1/pe2/pe3/pe4 /bin/bash
iperf ...

To configure only one path:
sudo vnx -f scenario.xml -x default

To configure two tn paths:
sudo vnx -f scenario.xml -x tn_paths
