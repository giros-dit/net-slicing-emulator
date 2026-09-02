from scapy.all import *
import subprocess
import time
import struct
from collections import defaultdict


# Duración de la simulación
duration = 5  # segundos
packet_len = 1458
t0 = time.time()
pcap_packets1 = []
pcap_packets2 = []
flow_seq = defaultdict(int)

host_macs = {
    "10.0.0.2": "00:00:00:00:01:02",
    "10.0.0.3": "00:00:00:00:01:03",
    "10.0.0.4": "00:00:00:00:01:04",
    "10.0.0.5": "00:00:00:00:01:05",
    "10.0.0.6": "00:00:00:00:01:06",
    "10.0.0.7": "00:00:00:00:01:07",
    #"10.0.0.8": "00:00:00:00:01:08",
    #"10.0.0.9": "00:00:00:00:01:09",
    "10.3.0.2": "00:00:00:00:03:02",
    "10.3.0.3": "00:00:00:00:03:03",
    "10.3.0.4": "00:00:00:00:03:04",
    "10.3.0.5": "00:00:00:00:03:05",
    "10.3.0.6": "00:00:00:00:03:06",
    "10.3.0.7": "00:00:00:00:03:07",
    #"10.3.0.8": "00:00:00:00:03:08",
    #"10.3.0.9": "00:00:00:00:03:09",
}

dst_mac1 = subprocess.check_output(
    ["sudo", "lxc-attach", "-n", "PE1", "--", "cat", "/sys/class/net/eth1/address"],
    text=True
).strip()
dst_mac2 = subprocess.check_output(
    ["sudo", "lxc-attach", "-n", "PE3", "--", "cat", "/sys/class/net/eth1/address"],
    text=True
).strip()

# Tráfico en ráfagas (isochronous)
bursts1 = [
    {"src": "10.0.0.3", "dst": "10.2.0.3", "interval": 1.0, "count": 58},   
    {"src": "10.0.0.5", "dst": "10.2.0.5", "interval": 1.0, "count": 66},
    {"src": "10.0.0.7", "dst": "10.2.0.7", "interval": 1.0, "count": 23},  
]

bursts2 = [
    {"src": "10.3.0.3", "dst": "10.5.0.3", "interval": 5.0, "count": 97},   
    {"src": "10.3.0.5", "dst": "10.5.0.5", "interval": 5.0, "count": 111},  
    {"src": "10.3.0.7", "dst": "10.5.0.7", "interval": 5.0, "count": 40},
]

# Flujos constantes (aprox. en pps)
const_flows1 = [
    {"src": "10.0.0.2", "dst": "10.2.0.2", "pps": 4942},    # h1-server1 (60 Mbps)
    {"src": "10.0.0.4", "dst": "10.2.0.4", "pps": 2434},    # h5-server5 (30 Mbps)
    {"src": "10.0.0.6", "dst": "10.2.0.6", "pps": 810.3},    # h7-server7 (10 Mbps)
]

const_flows2 = [
    {"src": "10.3.0.2", "dst": "10.5.0.2", "pps": 5000},    # h1-server1 (60 Mbps)
    {"src": "10.3.0.4", "dst": "10.5.0.4", "pps": 2500},    # h5-server5 (30 Mbps)
    {"src": "10.3.0.6", "dst": "10.5.0.6", "pps": 833.3},    # h7-server7 (10 Mbps)
]

# Generador de tráfico constante
def generate_constant(flow, t0, duration, start, dst_mac):
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
def generate_burst(flow, t0, start, duration, dst_mac):
    packets = []
    burst_count = flow["count"] 
    interval = flow["interval"]
    flow_id = (flow["src"], flow["dst"])

    t = 0
    while t < duration:

        for i in range(burst_count):
            src_ip = flow["src"]
            src_mac = host_macs[src_ip]
            pkt_time = t0 + start + t + i * 0.000004

            flow_seq[flow_id] += 1
            seq = flow_seq[flow_id]

            payload = struct.pack("!I", seq) + b"x" * (packet_len - 4)

            eth = Ether(src=src_mac, dst=dst_mac, type=0x0800)
            pkt = eth / IP(src=flow["src"], dst=flow["dst"], id=i)/UDP(sport=1234, dport=5001)/Raw(load=payload)
            pkt.time = pkt_time
            packets.append(pkt)

        t += interval
    return packets


# Generar paquetes
for flow in const_flows1:
    pcap_packets1 += generate_constant(flow, t0, duration, 0, dst_mac1)

for flow in const_flows2:
    pcap_packets2 += generate_constant(flow, t0, duration, 0, dst_mac2)

for flow in bursts1:
    pcap_packets1 += generate_burst(flow, t0, 1, 5-1, dst_mac1)

for flow in bursts2:
    pcap_packets2 += generate_burst(flow, t0, 1, 1, dst_mac2)    

# Ordenar por tiempo
pcap_packets1.sort(key=lambda p: p.time)
pcap_packets2.sort(key=lambda p: p.time)

# Guardar el resultado
wrpcap("ExperimentB-p1.pcap", pcap_packets1)
wrpcap("ExperimentB-p2.pcap", pcap_packets2)
print("✔ PCAPs generados correctamente: ExperimentB-p1.pcap y ExperimentB-p2.pcap")
