from scapy.all import rdpcap, IP, UDP
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import tikzplotlib
import subprocess
import re
import struct

# Load packets in PE1-e1 and PE2-e2
pkts_sent = rdpcap("capturas/PE1-e1.pcap")
pkts_received = rdpcap("capturas/PE2-e2.pcap")

src_ips = set()
sent_dict = {}
bw_sent_by_flow = defaultdict(lambda: defaultdict(float))
t0 = min(pkt.time for pkt in pkts_sent if IP in pkt)
step = 0.01
step_lat = 0.005

for pkt in pkts_sent:
    if IP in pkt and UDP in pkt:
        interval = int((pkt.time -t0) / step + 1)
        bw_sent_by_flow[pkt[IP].src][interval] += len(pkt) * 8
        src_ips.add(pkt[IP].src)


        seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
        key = (pkt[IP].src, pkt[IP].dst, seq)
        sent_dict[key] = pkt.time

delay_by_flow = defaultdict(list) # List of (recv_time, delay)
bw_by_flow = defaultdict(lambda: defaultdict(float)) # src_ip -> intervalo -> bps

for pkt in pkts_received:
    if IP in pkt and UDP in pkt:
        seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
        key = (pkt[IP].src, pkt[IP].dst, seq)
        recv_time = pkt.time
        if key in sent_dict:
            delay = recv_time - sent_dict[key]
            delay_by_flow[pkt[IP].src].append((recv_time, delay))
            interval = int((recv_time - t0)/step_lat + 1)
            bw_by_flow[pkt[IP].src][interval] += len(pkt) * 8
            del sent_dict[key]  # Marked as received

my_pairs = [
    ("10.0.0.2", "10.0.0.3"),
    ("10.0.0.4", "10.0.0.5"),
    ("10.0.0.6", "10.0.0.7"),
    ("10.0.0.8", "10.0.0.9"),
    ("10.0.0.10", "10.0.0.11"),
    ("10.0.0.12", "10.0.0.13")
]

bw_sent_by_pair = {}
for ip1, ip2 in my_pairs:
    bw_pair = defaultdict(float)
    for ip in (ip1, ip2):
        for interval, bits in bw_sent_by_flow.get(ip, {}).items():
            bw_pair[interval] += bits
    bw_sent_by_pair[(ip1, ip2)] = bw_pair

bw_by_pair = {}  # map from tuple pair -> dict(interval->bits)
for ip1, ip2 in my_pairs:
    bw_pair = defaultdict(float)
    for ip in (ip1, ip2):
        for interval, bits in bw_by_flow.get(ip, {}).items():
            bw_pair[interval] += bits
    bw_by_pair[(ip1, ip2)] = bw_pair

grouped_delays = defaultdict(lambda: defaultdict(list)) # src_ip -> interval -> list of delays
for src_ip, values in delay_by_flow.items():
    for recv_time, delay in values:
        interval = int((recv_time - t0) / step_lat + 1)
        grouped_delays[src_ip][interval].append(delay)
delay_by_pair = {} 
for ip1, ip2 in my_pairs:
    delay_pair = defaultdict(list)
    for ip in (ip1, ip2):
        for interval, delay in grouped_delays.get(ip, {}).items():
            delay_pair[interval].extend(delay)
    delay_by_pair[(ip1, ip2)] = delay_pair

all_intervals = set()
for intervals in grouped_delays.values():
    all_intervals.update(intervals.keys())

max_interval = max(all_intervals)

for (ip1, ip2), intervals in delay_by_pair.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            delay_by_pair[(ip1,ip2)][interval] = [0]

for (ip1, ip2), intervals in bw_sent_by_pair.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            bw_sent_by_pair[(ip1,ip2)][interval] = 0


for (ip1, ip2), intervals in bw_by_pair.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            bw_by_pair[(ip1,ip2)][interval] = 0

size=2
line_size=1
# ---------------------------------
# Style configuration per flow
# ---------------------------------

flow_styles = {
    "10.0.0.2":  dict(label='S1-C1', color='#006600', marker='*', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.4":  dict(label='S1-C2', color='#99FF99', marker='^', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.8":  dict(label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.12": dict(label='S2-C2', color='#DAE8FC', marker='*', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.6":  dict(label='S3-C1', color='orange', marker='^', linestyle='-', markersize=size, linewidth=line_size),
    "10.0.0.10": dict(label='S3-C2', color='#610B0B', marker='p', linestyle='-', markersize=size, linewidth=line_size)
}

# Plot Generated Traffic
plt.figure(figsize=(10,7))

for (ip1, ip2), intervals in bw_sent_by_pair.items():
    style = flow_styles.get(ip1)
    x = sorted(intervals)
    y = [bw_sent_by_pair[(ip1, ip2)][i] / step / 1e6 for i in x]  # Mbps
    vector1 = [i*step*1000 for i in x]  # ms
    
    if style:
        plt.plot(vector1, y, label=style["label"], color=style["color"], marker=style["marker"], linestyle=style["linestyle"], markersize=style["markersize"], linewidth=style["linewidth"])
plt.xlabel("t (ms)")
plt.ylabel("BW (Mbps)")
plt.grid(True)
#plt.ylim(0,80)
plt.xlim(0,1000)
plt.tight_layout()
tikzplotlib.save("bw_gen_expb.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Plot bandwidth
plt.figure(figsize=(10,7))
for (ip1, ip2), intervals in bw_by_pair.items():
    style = flow_styles.get(ip1)
    x = sorted(intervals)
    y = [intervals[i] / step_lat / 1000000 for i in x]  # bits por 10ms => bits/s
    vector1 = [i*step*1000 for i in x]

    if style:
        plt.plot(vector1, y, label=style["label"], color=style["color"], marker=style["marker"], linestyle=style["linestyle"], markersize=style["markersize"], linewidth=style["linewidth"])

plt.xlabel("t (ms)")
plt.ylabel("BW (Mbps)")
plt.grid(True)
plt.ylim(0,70)
plt.xlim(0,1000)
#plt.legend()
plt.tight_layout()

#tikzplotlib.save("bw_expb.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")


# Plot the delays
fig_delays, ax_delays = plt.subplots(figsize=(10,7))

for (ip1, ip2), intervals in delay_by_pair.items():
    style = flow_styles.get(ip1)
    x = []
    y = []
    for interval in sorted(intervals):
        max_delay = max(intervals[interval])
        x.append(interval * step_lat * 1000)
        y.append(max_delay * 1000)

    if style:
        ax_delays.plot(x, y, label=style["label"], color=style["color"], marker=style["marker"], linestyle=style["linestyle"], markersize=style["markersize"], linewidth=style["linewidth"])

ax_delays.axhline(3, color='#222222', linestyle='-', linewidth=4)
ax_delays.axhline(15, color='#008C95', linestyle='-', linewidth=4)
ax_delays.axhline(30, color='#B03060', linestyle='-', linewidth=4)
ax_delays.set_xlabel("t (ms)")
ax_delays.set_ylabel("Latency (ms)")
ax_delays.grid(True)
ax_delays.set_xlim(0,1000)
ax_delays.text(1.01, 3, 'TNA', transform=ax_delays.get_yaxis_transform(), color='#222222', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax_delays.text(1.01, 15, 'TNB', transform=ax_delays.get_yaxis_transform(), color='#008C95', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax_delays.text(1.01, 30, 'TNC', transform=ax_delays.get_yaxis_transform(), color='#B03060', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax_delays.set_ylim(0, 60)
ax_delays.set_xlim(0, 1000)
fig_delays.tight_layout()

tikzplotlib.save("latency_expb.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

plt.show()

