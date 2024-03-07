echo "Configuring PEs"
sudo lxc-attach -n PE1 -- ./root/slices_conf.sh
sudo lxc-attach -n PE2 -- ./root/slices_conf_PE2.sh

echo "Configuring Ps"
sudo lxc-attach -n P1 -- ./root/p_routers_conf.sh
sudo lxc-attach -n P2 -- ./root/p_routers_conf.sh
sudo lxc-attach -n P3 -- ./root/p_routers_conf.sh


