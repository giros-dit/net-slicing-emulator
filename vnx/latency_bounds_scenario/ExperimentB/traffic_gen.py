from scapy.all import *
import subprocess
import time
import struct
from collections import defaultdict


# Duración de la simulación
duration1 = 0.2  # segundos
duration2 = 0.8
packet_len = 1458
t0 = time.time()
pcap_packets = []
flow_seq = defaultdict(int)

host_macs = {
    "10.0.0.2": "00:00:00:00:01:02",
    "10.0.0.3": "00:00:00:00:01:03",
    "10.0.0.4": "00:00:00:00:01:04",
    "10.0.0.5": "00:00:00:00:01:05",
    "10.0.0.6": "00:00:00:00:01:06",
    "10.0.0.7": "00:00:00:00:01:07",
    "10.0.0.8": "00:00:00:00:01:08",
    "10.0.0.9": "00:00:00:00:01:09",
    "10.0.0.10": "00:00:00:00:01:0A",
    "10.0.0.11": "00:00:00:00:01:0B",
    "10.0.0.12": "00:00:00:00:01:0C",
    "10.0.0.13": "00:00:00:00:01:0D",
}

dst_mac = subprocess.check_output(
    ["sudo", "lxc-attach", "-n", "PE1", "--", "cat", "/sys/class/net/eth1/address"],
    text=True
).strip()

# Tráfico en ráfagas (isochronous)
bursts = [
    {"src": "10.0.0.3", "dst": "10.2.0.3", "interval": 1.0, "count": 30},   # h2 -> server2
    {"src": "10.0.0.13", "dst": "10.2.0.13", "interval": 1.0, "count": 13}, # h12 -> server12
    {"src": "10.0.0.7", "dst": "10.2.0.7", "interval": 1.0, "count": 60},  # h6 -> server6
    {"src": "10.0.0.9", "dst": "10.2.0.9", "interval": 1.0, "count": 50},   # h8 -> server8
]

# Flujos constantes (aprox. en pps)
const_flows = [
    {"src": "10.0.0.2", "dst": "10.2.0.2", "pps": 2500},    # h1-server1 (30 Mbps)
    #{"src": "10.0.0.4", "dst": "10.2.0.4", "pps": 413},     # h3-server3
    {"src": "10.0.0.6", "dst": "10.2.0.6", "pps": 2500},    # h5-server5 (30 Mbps)
    {"src": "10.0.0.8", "dst": "10.2.0.8", "pps": 833},    # h7-server7 (10 Mbps)
    {"src": "10.0.0.10", "dst": "10.2.0.10", "pps": 2500},  # h9-server9 (30 Mbps)
    {"src": "10.0.0.12", "dst": "10.2.0.12", "pps": 1666},  # h11-server11 (20 Mbps)
]

const_flows2 = [
    {"src": "10.0.0.2", "dst": "10.2.0.2", "pps": 5833},    # h1-server1 (70 Mbps)
    #{"src": "10.0.0.4", "dst": "10.2.0.4", "pps": 413},     # h3-server3
    {"src": "10.0.0.6", "dst": "10.2.0.6", "pps": 2500},    # h5-server5 (30 Mbps)
    {"src": "10.0.0.8", "dst": "10.2.0.8", "pps": 833},    # h7-server7 (10 Mbps)
    {"src": "10.0.0.10", "dst": "10.2.0.10", "pps": 2500},  # h9-server9 (30 Mbps)
    {"src": "10.0.0.12", "dst": "10.2.0.12", "pps": 1666},  # h11-server11 (20 Mbps)
]



# Generador de tráfico constante
def generate_constant(flow, t0, duration, start):
    packets = []
    interval = 1.0 / flow["pps"]
    pkt_count = int(duration * flow["pps"])
    
    flow_id = (flow["src"], flow["dst"])

    for i in range(pkt_count):
        pkt_time = t0 + start + i * interval
        src_ip = flow["src"]
        src_mac = host_macs[src_ip]

        flow_seq[flow_id] += 1
        seq = flow_seq[flow_id]

        payload = struct.pack("!I", seq) + b"x" * (packet_len - 4)

        eth = Ether(src=src_mac, dst=dst_mac, type=0x0800)
        pkt = eth / IP(src=flow["src"], dst=flow["dst"], id=i)/UDP(sport=1234, dport=5001)/Raw(load=payload)
        pkt.time = pkt_time
        packets.append(pkt)
    return packets

# Generador de ráfagas
def generate_burst(flow, t0, start):
    packets = []
    current_time = 0
    burst_count = flow["count"]
    flow_id = (flow["src"], flow["dst"])

    if (flow["src"] == "10.0.0.9"):
        current_time = 0.055
    elif (flow["src"] == "10.0.0.13"):
        current_time = 0.07

    for i in range(burst_count):
        src_ip = flow["src"]
        src_mac = host_macs[src_ip]
        
        pkt_time = t0 + start + current_time +  i * 0.000001

        flow_seq[flow_id] += 1
        seq = flow_seq[flow_id]

        payload = struct.pack("!I", seq) + b"x" * (packet_len - 4)

        eth = Ether(src=src_mac, dst=dst_mac, type=0x0800)
        pkt = eth / IP(src=flow["src"], dst=flow["dst"], id=i)/UDP(sport=1234, dport=5001)/Raw(load=payload)
        pkt.time = pkt_time
        packets.append(pkt)
    return packets

# Generar paquetes
for flow in const_flows:
    pcap_packets += generate_constant(flow, t0, duration1, 0)

for flow in const_flows2:
    pcap_packets += generate_constant(flow, t0, duration2, duration1)

for flow in bursts:
    pcap_packets += generate_burst(flow, t0, duration1)

# Ordenar por tiempo
pcap_packets.sort(key=lambda p: p.time)

# Guardar el resultado
wrpcap("ExperimentB.pcap", pcap_packets)
print("✔ PCAP con ráfagas y tráfico constante generado 'ExperimentB.pcap'")
