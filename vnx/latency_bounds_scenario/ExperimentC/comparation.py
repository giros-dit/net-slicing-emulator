from scapy.all import rdpcap, IP
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import tikzplotlib
import subprocess
import re


# Load packets in PE1-e1 and PE2-e2
pkts_sent = rdpcap("PE1.pcap")
pkts_received = rdpcap("PE2.pcap")

src_ips = set()
sent_dict = {}
bw_sent_by_flow = defaultdict(lambda: defaultdict(float))
t0 = min(pkt.time for pkt in pkts_sent if IP in pkt)
step = 0.01

for pkt in pkts_sent:
    if IP in pkt:
        interval = int((pkt.time -t0) / step)
        bw_sent_by_flow[pkt[IP].src][interval] += len(pkt) * 8
        src_ips.add(pkt[IP].src)
        key = (pkt[IP].src, pkt[IP].id)
        sent_dict[key] = pkt.time

delay_by_flow = defaultdict(list) # List of (recv_time, delay)
lost_by_flow = defaultdict(list)
bw_by_flow = defaultdict(lambda: defaultdict(float)) # src_ip -> intervalo -> bps

for pkt in pkts_received:
    if IP in pkt:
       key = (pkt[IP].src, pkt[IP].id)
       recv_time = pkt.time
       if key in sent_dict:
           delay = recv_time - sent_dict[key]
           delay_by_flow[pkt[IP].src].append((recv_time, delay))
           interval = int((recv_time - t0)/step)
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

# Group latencies by flow
grouped_delays = defaultdict(lambda: defaultdict(list)) # src_ip -> interval -> list of delays
for src_ip, values in delay_by_flow.items():
    for recv_time, delay in values:
        interval = int((recv_time - t0) / step + 1)
        grouped_delays[src_ip][interval].append(delay)
delay_by_pair = {} 
for ip1, ip2 in my_pairs:
    delay_pair = defaultdict(list)
    for ip in (ip1, ip2):
        for interval, delay in grouped_delays.get(ip, {}).items():
            delay_pair[interval].extend(delay)
    delay_by_pair[(ip1, ip2)] = delay_pair

# Group losses by flow
for (src_ip, _), send_time in sent_dict.items():
    lost_by_flow[src_ip].append(send_time)
print("Resumen de paquetes perdidos por flujo")
print("{:<20} {:>20}".format("Dirección IP", "Paquetes Perdidos"))
for src_ip in sorted(lost_by_flow):
    print("{:<20} {:>20}".format(src_ip, len(lost_by_flow[src_ip])))
grouped_losses = defaultdict(lambda: defaultdict(int))  # src_ip -> interval -> count
for src_ip, send_times in lost_by_flow.items():
    for send_time in send_times:
        interval = int((send_time - t0) / step + 1)
        grouped_losses[src_ip][interval] += 1
pl_by_pair = {}  # map from tuple pair -> dict(interval->count)
for ip1, ip2 in my_pairs:
    pl_pair = defaultdict(float)
    for ip in (ip1, ip2):
        for interval, losses in grouped_losses.get(ip, {}).items():
            pl_pair[interval] += losses
    pl_by_pair[(ip1, ip2)] = pl_pair


all_intervals = set()
for intervals in grouped_delays.values():
    all_intervals.update(intervals.keys())

max_interval = max(all_intervals)

for (ip1, ip2), intervals in pl_by_pair.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            pl_by_pair[(ip1,ip2)][interval] = 0

for (ip1, ip2), intervals in delay_by_pair.items():
    for interval in range(max_interval + 1):
        if interval not in intervals:
            delay_by_pair[(ip1,ip2)][interval] = [0]

cmd = ["sudo", "lxc-attach", "-n", "PE1", "--", "tc", "-s", "-d", "class", "show", "dev", "eth2"]

try:
    output = subprocess.check_output(cmd, text=True)
except subprocess.CalledProcessError as e:
    print("Error al ejecutar el comando:", e)
    exit(1) 

classes = {
"prio 2:1": "TNA",
    "drr 20:1": "TNB",
    "drr 20:2": "TNC",
    "prio 2:3": "TND"
}
resultados = {}

lines = output.splitlines()
actual_class = None
for line in lines:
    line = line.strip()
    # Detectar clase
    m_clase = re.match(r"^class\s+(\S+\s+\d+:\d+)", line)
    if m_clase:
        actual_class = m_clase.group(1)
        continue

    if actual_class in classes:
        m_dropped = re.search(r"dropped\s+(\d+)", line)
        if m_dropped:
            resultados[classes[actual_class]] = int(m_dropped.group(1))

with open("resultados.log", "a") as f:
    f.write(f"{resultados['TNA']},{resultados['TNB']},{resultados['TNC']},{resultados['TND']}\n")



size=2

# Plot Generated Traffic
plt.figure(figsize=(10,7))
for (ip1, ip2), intervals in bw_by_pair.items():
    x = sorted(intervals)
    y = [bw_sent_by_pair[(ip1, ip2)][i] / step / 1e6 for i in x]  # Mbps
    vector1 = [i*step*1000 for i in x]  # ms

    if ip1 == "10.0.0.2":
        plt.plot(vector1, y, label='S1-C1', color='green', linestyle='-.', marker='*', markersize=size)
    elif ip1 == "10.0.0.4":
        plt.plot(vector1, y, label='S1-C2', color='#BEF781', linestyle='--', marker='o', markersize=size)
    elif ip1 == "10.0.0.6":
        plt.plot(vector1, y, label='S3-C1', color='orange', linestyle='--', marker='o', markersize=size)
    elif ip1 == "10.0.0.8":
        plt.plot(vector1, y, label='S2-C1', color='#0040FF', linestyle='--', marker='o', markersize=size)
    elif ip1 == "10.0.0.10":
        plt.plot(vector1, y, label='S3-C2', color='#610B0B', linestyle='--', marker='o', markersize=size)
    elif ip1 == "10.0.0.12":
        plt.plot(vector1, y, label='S2-C2', color='cyan', linestyle='--', marker='o', markersize=size)

plt.xlabel("t (ms)")
plt.ylabel("BW (Mbps)")
plt.grid(True)
plt.ylim(0,105)
plt.xlim(0,1000)
plt.legend()
plt.tight_layout()
tikzplotlib.save("bw_gen_expc.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Plot bandwidth
plt.figure(figsize=(10,7))
for (ip1, ip2), intervals in bw_by_pair.items():
    x = sorted(intervals)
    y = [intervals[i] / 0.01 / 1000000 for i in x]  # bits por 10ms => bits/s
    vector1 = [i*0.01*1000 for i in x]
    if (ip1 == "10.0.0.2"):
    	plt.plot(vector1, y, label='S1-C1', color='green', marker='*', linestyle='-.', markersize=size)
    elif (ip1 == "10.0.0.4"):
    	plt.plot(vector1, y, label='S1-C2', color='#BEF781', marker='^', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.6"):
        plt.plot(vector1, y, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.8"):
	    plt.plot(vector1, y, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size)
    elif (ip1 == "10.0.0.10"):
	    plt.plot(vector1, y, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.12"):
	    plt.plot(vector1, y, label='S2-C2', color='cyan', marker='*', linestyle='-.', markersize=size)
#plt.title("Ancho de banda recibido cada 10ms por flujo")
plt.xlabel("t (ms)")
plt.ylabel("BW (Mbps)")
plt.grid(True)
plt.ylim(0,50)
plt.xlim(0,1000)
#plt.legend()
plt.tight_layout()

tikzplotlib.save("bw_expc.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")


# Plot the delays
plt.figure(figsize=(10,7))

for (ip1, ip2), intervals in delay_by_pair.items():
    x = []
    y = []
    for interval in sorted(intervals):
        max_delay = max(intervals[interval])
        x.append(interval * step * 1000)
        y.append(max_delay * 1000)
    if (ip1 == "10.0.0.2"):
        plt.plot(x, y, label='S1-C1', color='green', marker='*', linestyle='-.', markersize=size)
    elif (ip1 == "10.0.0.4"): 
    	plt.plot(x, y, label='S1-C2', color='#BEF781', marker='^', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.6"):
        plt.plot(x, y, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.8"):
	    plt.plot(x, y, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size)
    elif (ip1 == "10.0.0.10"):
	    plt.plot(x, y, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.12"):
	    plt.plot(x, y, label='S2-C2', color='cyan', marker='*', linestyle='-.', markersize=size)
#plt.title("Retardo máximo cada 10ms por flujo")
plt.xlabel("t (ms)")
plt.ylabel("Latency (ms)")
plt.grid(True)
#plt.legend()
plt.ylim(0,20)
plt.xlim(0,1000)
plt.tight_layout()

tikzplotlib.save("latency_expc.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Plot packet losses per TN QoS Class
import pandas as pd
import matplotlib.pyplot as plt

# Leer el fichero con pandas
columnas = ["TNA", "TNB", "TNC", "TND"]
df = pd.read_csv("resultados.log", names=columnas)

# Última fila → gráfico de barras
ultimo = df.iloc[-1]
colors = ["#0040FF","green","orange","#610B0B"]
plt.figure(figsize=(10,7))
bars = plt.bar(["TNA","TNB","TNC","TND"], [ultimo["TNA"], ultimo["TNB"], ultimo["TNC"], ultimo["TND"]], color=colors)
plt.xlabel("TN QoS Clases")
plt.ylabel("Dropped packets")
#plt.title(f"Dropped packets por clase (última muestra: {ultimo['timestamp']})")
plt.grid(True)
tikzplotlib.save("pkt_loss_expc.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Plot losses per flow
plt.figure(figsize=(12, 5))
for (ip1, ip2), intervals in pl_by_pair.items():
    x = sorted(intervals)
    y = [intervals[i] for i in x]
    vector1 = [i*step*1000 for i in x]
    if (ip1 == "10.0.0.2"):
    	plt.plot(vector1, y, label='S1-C1', color='green', marker='*', linestyle='-.', markersize=size)
    elif (ip1 == "10.0.0.4"): 
    	plt.plot(vector1, y, label='S1-C2', color='#BEF781', marker='^', linestyle='--', markersize=size, alpha=0.7)
    elif (ip1 == "10.0.0.6"):
        plt.plot(vector1, y, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.8"):
	    plt.plot(vector1, y, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size)
    elif (ip1 == "10.0.0.10"):
	    plt.plot(vector1, y, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size)
    elif (ip1 == "10.0.0.12"):
	    plt.plot(vector1, y, label='S2-C2', color='cyan', marker='*', linestyle='-.', markersize=size)

#plt.title("Evolución de paquetes perdidos cada 10 ms por flujo")
plt.xlabel("t (ms)")
plt.ylabel("Packet Losses")
plt.grid(True)
plt.tight_layout()
#plt.legend()
plt.ylim(0,50)
plt.xlim(0,1000)
tikzplotlib.save("pkt_loss_flow_expc.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")


fig_legend = plt.figure(figsize=(10, 1))
fig_legend.legend(bars, ["TNA", "TNB", "TNC", "TND"], loc="center", ncol=4)
plt.axis("off")
tikzplotlib.save("legend_tn_qos_classes.tex")

plt.show()



