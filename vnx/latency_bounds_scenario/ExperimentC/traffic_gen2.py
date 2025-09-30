from scapy.all import *
import time

# Duración de la simulación
duration = 1  # segundos
packet_len = 1458
t0 = time.time()
pcap_packets = []

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

dst_mac = "be:54:f3:de:55:2b"

# Tráfico en ráfagas (isochronous)
bursts = [
    #{"src": "10.0.0.3", "dst": "10.2.0.3", "interval": 1.0, "count": 50},   # h2 -> server2
    {"src": "10.0.0.13", "dst": "10.2.0.13", "interval": 1.0, "count": 14}, # h12 -> server12
    {"src": "10.0.0.7", "dst": "10.2.0.7", "interval": 1.0, "count": 59},  # h6 -> server6
    {"src": "10.0.0.9", "dst": "10.2.0.9", "interval": 1.0, "count": 21},   # h8 -> server8
]

# Flujos constantes (aprox. en pps)
const_flows = [
    {"src": "10.0.0.2", "dst": "10.2.0.2", "pps": 8333},    # h1-server1 (100 Mbps)
    #{"src": "10.0.0.4", "dst": "10.2.0.4", "pps": 413},     # h3-server3
    {"src": "10.0.0.6", "dst": "10.2.0.6", "pps": 2500},    # h5-server5 (100 Mbps)
    {"src": "10.0.0.8", "dst": "10.2.0.8", "pps": 833.33},    # h7-server7 (100 Mbps)
    #{"src": "10.0.0.10", "dst": "10.2.0.10", "pps": 8256},  # h9-server9
    {"src": "10.0.0.12", "dst": "10.2.0.12", "pps": 1666.67},  # h11-server11 (20 Mbps)
]

# Generador de tráfico constante
def generate_constant(flow, t0):
    packets = []
    interval = 1.0 / flow["pps"]
    pkt_count = int(duration * flow["pps"])
    for i in range(pkt_count):
        pkt_time = t0 + i * interval
        src_ip = flow["src"]
        src_mac = host_macs[src_ip]
        eth = Ether(src=src_mac, dst=dst_mac, type=0x0800)
        pkt = eth / IP(src=flow["src"], dst=flow["dst"], id=i)/UDP(sport=1234, dport=5001)/Raw(load=b"x" * packet_len)
        pkt.time = pkt_time
        packets.append(pkt)
    return packets

# Generador de ráfagas
def generate_burst(flow, t0):
    packets = []
    current_time = 0.048
    burst_interval = flow["interval"]
    burst_count = flow["count"]
    if (flow["src"] == "10.0.0.7"):
        current_time = 0.0
    elif (flow["src"] == "10.0.0.13"):
        current_time = 0.0000000000001
    while current_time < duration:
        for i in range(burst_count):
            src_ip = flow["src"]
            src_mac = host_macs[src_ip]
            pkt_time = t0 + current_time +  i * 0.000004
            eth = Ether(src=src_mac, dst=dst_mac, type=0x0800)
            pkt = eth / IP(src=flow["src"], dst=flow["dst"], id=i)/UDP(sport=1234, dport=5001)/Raw(load=b"x" * packet_len)
            pkt.time = pkt_time
            packets.append(pkt)
        current_time += burst_interval
    return packets

# Generar paquetes
for flow in const_flows:
    pcap_packets += generate_constant(flow, t0)

for flow in bursts:
    pcap_packets += generate_burst(flow, t0)

# Ordenar por tiempo
pcap_packets.sort(key=lambda p: p.time)

# Guardar el resultado
wrpcap("ExperimentC-2.pcap", pcap_packets)
print("✔ PCAP con ráfagas y tráfico constante generado 'ExperimentC-2.pcap'")
