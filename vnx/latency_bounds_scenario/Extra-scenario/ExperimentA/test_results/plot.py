import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

s1c1_data2 = []
s1c2_data2 = []
s3c2_data2 = []
s3c1_data2 = []
s2c1_data2 = []
s2c2_data2 = []
s4c1_data2 = []
s4c2_data2 = []


with open('files/lat_max_metrics1', 'r') as file:
    for line in file:
        try:
            s1c1_data2.append(float(line.strip()))
        except ValueError:
            s1c1_data2.append(0)
with open('files/lat_max_metrics2', 'r') as file:
    for line in file:
        try:
            s1c2_data2.append(float(line.strip()))
        except ValueError:
            s1c2_data2.append(0)
with open('files/lat_max_metrics3', 'r') as file:
    for line in file:
        try:
            s3c1_data2.append(float(line.strip()))
        except ValueError:
            s3c1_data2.append(0)
with open('files/lat_max_metrics4', 'r') as file:
    for line in file:
        try:
            s2c1_data2.append(float(line.strip()))
        except ValueError:
            s2c1_data2.append(0)
with open('files/latency_max_metrics6', 'r') as file:
    for line in file:
        try:
            s3c2_data2.append(float(line.strip()))
        except ValueError:
            s3c2_data2.append(0)
with open('files/lat_max_metrics5', 'r') as file:
    for line in file:
        try:
            s2c2_data2.append(float(line.strip()))
        except ValueError:
            s2c2_data2.append(0)
with open('files/lat_max_metrics7', 'r') as file:
    for line in file:
        try:
            s4c1_data2.append(float(line.strip()))
        except ValueError:
            s4c1_data2.append(0)
with open('files/lat_max_metrics8', 'r') as file:
    for line in file:
        try:
            s4c2_data2.append(float(line.strip()))
        except ValueError:
            s4c2_data2.append(0)

with open('files/bw_metrics1', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c1_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics2', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c2_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics3', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c1_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics4', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c1_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics6', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c2_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics5', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c2_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics7', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c1_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bw_metrics8', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c2_bw = [1500/1458*float(line.strip()) for line in lines]


with open('files/bandwidth_metrics1_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c1_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics2_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c2_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics3_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c1_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics4_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c1_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c2_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics7_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c1_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics8_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c2_bw2 = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics1_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c1_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics2_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s1c2_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics3_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c1_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics4_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c1_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c2_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics6_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c2_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics7_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c1_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics8_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s4c2_s_bw = [1500/1458*float(line.strip()) for line in lines]

s1c1 = np.array(s1c1_bw2) + np.array(s1c1_s_bw)
s1c2 = np.array(s1c2_bw2) + np.array(s1c2_s_bw)
s2c1 = np.array(s2c1_bw2) + np.array(s2c1_s_bw)
s2c2 = np.array(s2c2_bw2) + np.array(s2c2_s_bw)
s3c1 = np.array(s3c1_bw2) + np.array(s3c1_s_bw)
s3c2 = np.array(s3c2_s_bw)
s4c1 = np.array(s4c1_bw2) + np.array(s4c1_s_bw)
s4c2 = np.array(s4c2_bw2) + np.array(s4c2_s_bw)

total_bw = s1c1 + s1c2 + s2c1 + s2c2 + s3c1 + s3c2 + s4c1 + s4c2

vector1 = np.arange(0.1, 60.1, 0.1)
size=2
line_size = 2

# Plot Customization
# Figura 2: Maximum Latency Behaviour
fig2, ax2 = plt.subplots(figsize=(7,7))
#fig2.suptitle('Maximum Latency Behaviour')
ax2.plot(vector1, s1c1_data2, label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax2.plot(vector1, s3c2_data2, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
ax2.plot(vector1, s3c1_data2, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax2.plot(vector1, s1c2_data2, label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax2.plot(vector1, s2c2_data2, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax2.plot(vector1, s4c2_data2, label='S4-C2', color='#FCA2F7', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax2.plot(vector1, s2c1_data2, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax2.plot(vector1, s4c1_data2, label='S4-C1', color='#A803A0', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax2.axhline(5, label='TNA', color='#222222', linestyle='-', linewidth=4)
ax2.axhline(20, label='TNB', color='#008C95', linestyle='-', linewidth=4)
ax2.axhline(50, label='TNC', color='#B03060', linestyle='-', linewidth=4)
ax2.set_xlabel('t (s)', fontsize=14)
ax2.set_ylabel('Latency (ms)', fontsize=14)
ax2.set_xlim(0,60)
ax2.set_ylim(0,55)
ax2.text(1.01, 5, 'TNA', transform=ax2.get_yaxis_transform(), color='#222222', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax2.text(1.01, 20, 'TNB', transform=ax2.get_yaxis_transform(), color='#008C95', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax2.text(1.01, 50, 'TNC', transform=ax2.get_yaxis_transform(), color='#B03060', va='center', ha='left', fontsize=12, fontweight='bold', clip_on=False)
ax2.grid(True)
#ax2.legend()
#tikzplotlib.save("latency_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots(figsize=(7,7))
#fig3.suptitle('Bandwidth Received')
ax3.plot(vector1, s1c1_bw, label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax3.plot(vector1, s1c2_bw, label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, alpha=0.7, linewidth=line_size)
ax3.plot(vector1, s2c1_bw, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax3.plot(vector1, s2c2_bw, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax3.plot(vector1, s3c1_bw, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax3.plot(vector1, s3c2_bw, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
ax3.plot(vector1, s4c1_bw, label='S4-C1', color='#A803A0', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax3.plot(vector1, s4c2_bw, label='S4-C2', color='#FCA2F7', marker='^', linestyle='--', markersize=size, linewidth=line_size)

ax3.set_xlabel('t (s)', fontsize=14)
ax3.set_ylabel('BW (Mbps)', fontsize=14)
ax3.set_xlim(0,60)
ax3.grid(True)
#ax3.legend()
#tikzplotlib.save("bw_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 6: Bandwidth Sent Behaviour
fig6, ax6 = plt.subplots(figsize=(7,7))
#fig6.suptitle('Bandwidth Sent')
ax6.plot(vector1, s1c1, label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax6.plot(vector1, s3c2, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s3c1, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s1c2, label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s2c1, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size, alpha= 0.6)
ax6.plot(vector1, s2c2, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax6.plot(vector1, s4c1, label='S4-C1', color='#A803A0', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax6.plot(vector1, s4c2, label='S4-C2', color='#FCA2F7', marker='^', linestyle='--', markersize=size, linewidth=line_size)

ax6.set_xlabel('t (s)', fontsize=14)
ax6.set_ylabel('BW (Mbps)', fontsize=14)
ax6.set_xlim(0,60)
ax6.grid(True)
#ax6.legend()
#tikzplotlib.save("bw_gen_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

fig_legend1 = plt.figure(figsize=(10, 1))
handles, labels = ax3.get_legend_handles_labels()
fig_legend1.legend(handles, labels, loc='center', ncol=8)
plt.axis('off')
#tikzplotlib.save("legend_expA.tex")

plt.show()

