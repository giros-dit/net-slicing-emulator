import matplotlib.pyplot as plt
import numpy as np
#import ikzplotlib

video_data = []
telemetry_data = []
be_data = []
embb_data = []
urllc_data = []

with open('filesNTN/bandwidth_metricsSNTN1', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_bw = [1538/1472*float(line.strip()) for line in lines]
with open('filesNTN/bandwidth_metricsSNTN2', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_bw = [1538/1472*float(line.strip()) for line in lines]
with open('filesNTN/bandwidth_metricsSNTN3', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_bw = [1538/1472*float(line.strip()) for line in lines]
with open('filesNTN/bandwidth_metricsSNTN4', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_bw = [1538/1472*float(line.strip()) for line in lines]
with open('filesNTN/bandwidth_metricsSNTN5', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_bw = [1538/1472*float(line.strip()) for line in lines]

video_bw = np.array(video_bw)
telemetry_bw = np.array(telemetry_bw)
embb_bw = np.array(embb_bw)
urllc_bw = np.array(urllc_bw)
be_bw = np.array(be_bw)

vector1 = np.arange(1, 100, 1)

size=3
fig3, ax3 = plt.subplots(figsize=(10,6))
ax3.plot(video_bw, label='RD: Video', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax3.plot(telemetry_bw, label='RD: Telemetry', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax3.plot(embb_bw, label='eMBB: VC', color='orange', marker='^', linestyle='--', markersize=size)
ax3.plot(be_bw, label='eMBB: BE', color='#F5A9BC', marker='p', linestyle='--', markersize=size )
ax3.plot(urllc_bw, label='URLLC', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax3.set_xlabel('t (s)')
ax3.set_ylabel('BW (Mbps)')
ax3.set_xlim(0,100)
ax3.grid(True)
ax3.legend()

plt.savefig("bw_NTN.png")

