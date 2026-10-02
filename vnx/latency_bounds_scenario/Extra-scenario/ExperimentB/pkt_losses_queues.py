from scapy.all import rdpcap, IP, UDP
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import tikzplotlib
import subprocess
import re
import struct

# Load packets in PE1-e2 and PE2-e2
pkts_sent = rdpcap("capturas/PE1-e2.pcap")
pkts_received = rdpcap("capturas/PE2-e2.pcap")

src_ips = set()
sent_dict = {}
t0 = min(pkt.time for pkt in pkts_sent if IP in pkt)
step = 0.001
max_interval = 0

for pkt in pkts_sent:
    if IP in pkt and UDP in pkt:
        interval = int((pkt.time -t0) / step + 1)
        if interval > max_interval:
            max_interval = interval
        src_ips.add(pkt[IP].src)
        seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
        key = (pkt[IP].src, pkt[IP].dst, seq)
        sent_dict[key] = pkt.time


for pkt in pkts_received:
    if IP in pkt and UDP in pkt:
        seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
        key = (pkt[IP].src, pkt[IP].dst, seq)
        if key in sent_dict:
            del sent_dict[key]  # Marked as received

my_pairs = [
    ("10.0.0.2", "10.0.0.3"),
    ("10.0.0.4", "10.0.0.5"),
    ("10.0.0.8", "10.0.0.9"),
    ("10.0.0.12", "10.0.0.13"),
    ("10.0.0.6", "10.0.0.7"),
    ("10.0.0.10", "10.0.0.11")
]

lost_by_pair = defaultdict(int)

# Lo que queda en sent_dict son paquetes no recibidos
for (src_ip, pkt_id, seq), _ in sent_dict.items():
    for ip1, ip2 in my_pairs:
        if src_ip == ip1 or src_ip == ip2:
            lost_by_pair[(ip1, ip2)] += 1
            break

print("\nLost packets per flow pair:")
for pair, lost in lost_by_pair.items():
    print(f"{pair}: {lost} packets")


# ---------------------------------
# Lost packets per interval
# ---------------------------------

lost_by_flow_interval = defaultdict(lambda: defaultdict(int))

# paquetes perdidos (los que quedan en sent_dict)
for (src_ip, dst_ip, seq), send_time in sent_dict.items():
    interval = int((send_time - t0) / step + 1)
    lost_by_flow_interval[src_ip][interval] += 1

# Agrupar por pares
lost_by_pair_interval = {}

for ip1, ip2 in my_pairs:
    lost_pair = defaultdict(int)
    for ip in (ip1, ip2):
        for interval, count in lost_by_flow_interval.get(ip, {}).items():
            lost_pair[interval] += count
    lost_by_pair_interval[(ip1, ip2)] = lost_pair

all_intervals = list(range(max_interval + 1))

# Rellenar intervalos vacíos
for (ip1, ip2), intervals in lost_by_pair_interval.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            lost_by_pair_interval[(ip1, ip2)][interval] = 0



size=3
line_size=2
# ---------------------------------
# Style configuration per flow
# ---------------------------------

flow_styles = {
    "10.0.0.2":  dict(label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size),
    "10.0.0.4":  dict(label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, linewidth=line_size),
    "10.0.0.8":  dict(label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.12": dict(label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size),
    "10.0.0.6":  dict(label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size),
    "10.0.0.10": dict(label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
}


# Plot packet losses
plt.figure(figsize=(10,7))

pairs = []
values = []
colors = []

for ip1, ip2 in my_pairs:
    lost = lost_by_pair.get((ip1, ip2),0)

    pairs.append(flow_styles[ip1]["label"])
    values.append(lost if lost > 0 else 0.025)
    colors.append(flow_styles[ip1]["color"])

x = np.arange(len(pairs))
plt.bar(x, values, color=colors)
plt.xticks(x, pairs, rotation=45)
plt.xlabel("Flow")
plt.ylabel("Dropped Packets")
plt.grid(False)

plt.tight_layout()

# tikzplotlib.save("pkt_losses_expb.tex",
#                  axis_width="\\textwidth",
#                  axis_height="0.7\\textwidth")

# Plot packet losses per interval
plt.figure(figsize=(10,7))

for (ip1, ip2), intervals in lost_by_pair_interval.items():
    style = flow_styles.get(ip1)

    x = sorted(intervals)
    y = [intervals[i] for i in x]
    vector1 = [i * step * 1000 for i in x]  # ms

    if style:
        plt.plot(vector1, y,
                 label=style["label"],
                 color=style["color"],
                 marker=style["marker"],
                 linestyle=style["linestyle"],
                 markersize=style["markersize"],
                 linewidth=style["linewidth"])

plt.xlabel("t (ms)")
plt.ylabel("Lost Packets per Interval")
plt.grid(True)
plt.xlim(100,500)

plt.tight_layout()

tikzplotlib.save("pkt_losses_expb.tex",
                 axis_width="\\textwidth",
                 axis_height="0.7\\textwidth")

plt.show()
