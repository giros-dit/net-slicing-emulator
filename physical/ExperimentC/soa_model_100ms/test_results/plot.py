import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

video_data = []
telemetry_data = []
be_data = []
embb_data = []
urllc_data = []
video2_data = []
telemetry2_data = []
be2_data = []
embb2_data = []
urllc2_data = []

with open('files/lat_metrics1', 'r') as file:
    for line in file:
        try:
            video_data.append(float(line.strip()))
        except ValueError:
            video_data.append(0)
with open('files/lat_metrics2', 'r') as file:
    for line in file:
        try:
            telemetry_data.append(float(line.strip()))
        except ValueError:
            telemetry_data.append(0)
with open('files/lat_metrics3', 'r') as file:
    for line in file:
        try:
            embb_data.append(float(line.strip()))
        except ValueError:
            embb_data.append(0)
with open('files/lat_metrics4', 'r') as file:
    for line in file:
        try:
            urllc_data.append(float(line.strip()))
        except ValueError:
            urllc_data.append(0)
with open('files/latency_metrics5', 'r') as file:
    for line in file:
        try:
            value = float(line.split()[1])
            be_data.append(value)
#            be_data.append(float(line.strip()))
        except ValueError:
            be_data.append(0)
with open('files/lat_max_metrics1', 'r') as file:
    for line in file:
        try:
            video2_data.append(float(line.strip()))
        except ValueError:
            video2_data.append(0)
with open('files/lat_max_metrics2', 'r') as file:
    for line in file:
        try:
            telemetry2_data.append(float(line.strip()))
        except ValueError:
            telemetry2_data.append(0)
with open('files/lat_max_metrics3', 'r') as file:
    for line in file:
        try:
            embb2_data.append(float(line.strip()))
        except ValueError:
            embb2_data.append(0)
with open('files/lat_max_metrics4', 'r') as file:
    for line in file:
        try:
            urllc2_data.append(float(line.strip()))
        except ValueError:
            urllc_data.append(0)
with open('files/latency_max_metrics5', 'r') as file:
    for line in file:
        try:
            be2_data.append(float(line.strip()))
        except ValueError:
            be2_data.append(0)
with open('files/bw_metrics1', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bw_metrics2', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bw_metrics3', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bw_metrics4', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_bw = [1538/1472*float(line.strip()) for line in lines]

with open('files/bandwidth_metrics1_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_bw2 = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics2_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_bw2 = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics3_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_bw2 = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics4_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_bw2 = [1538/1472*float(line.strip()) for line in lines]
#with open('files/bandwidth_metrics5_sender_burst_with_zeros', 'r') as file:
 #   lines = [line.replace(',', '.') for line in file]
  #  be_bw2 = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics1_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_s_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics2_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_s_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics3_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_s_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics4_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_s_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_s_bw = [1538/1472*float(line.strip()) for line in lines]

video1 = np.array(video_bw2)
video2 = np.array(video_s_bw)
tel1 = np.array(telemetry_bw2)
tel2 = np.array(telemetry_s_bw)
embb1 = np.array(embb_bw2)
embb2 = np.array(embb_s_bw)
urllc1 = np.array(urllc_bw2)
urllc2 = np.array(urllc_s_bw)
#be1 = np.array(be_bw2)
be_bw_s = np.array(be_s_bw)

video_bw_s = video1 + video2
telemetry_bw_s = tel1 + tel2
embb_bw_s = embb1 + embb2
urllc_bw_s = urllc1 + urllc2

video_bw = np.array(video_bw)
telemetry_bw = np.array(telemetry_bw)
embb_bw = np.array(embb_bw)
urllc_bw = np.array(urllc_bw)
be_bw = np.array(be_bw)

total_bw = video_bw + telemetry_bw + embb_bw + urllc_bw + be_bw

vector1 = np.arange(0.1, 60.1, 0.1)
size=2
# Plot Customization
# Figura 1: Latency Behaviour
#fig1, ax1 = plt.subplots()
#fig1.suptitle('Latency Behaviour')
#ax1.plot(vector1, video_data, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.')
#ax1.plot(vector1, be_data, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--')
#ax1.plot(vector1, embb_data, label='eMBB Traffic', color='orange', marker='^', linestyle='--')
#ax1.plot(vector1, telemetry_data, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.')
#ax1.plot(vector1, urllc_data, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-')
#ax1.set_xlabel('t (s)')
#ax1.set_ylabel('Latency (ms)')
#ax1.set_xlim(left=0)
#ax1.grid(True)
#ax1.legend()

# Figura 2: Maximum Latency Behaviour
fig2, ax2 = plt.subplots(figsize=(10,6))
#fig2.suptitle('Maximum Latency Behaviour')
ax2.plot(vector1, video2_data, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax2.plot(vector1, be2_data, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax2.plot(vector1, embb2_data, label='eMBB Traffic', color='orange', marker='^', linestyle='--', markersize=size)
ax2.plot(vector1, telemetry2_data, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax2.plot(vector1, urllc2_data, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-', markersize=size, alpha=0.7)
ax2.set_xlabel('t (s)')
ax2.set_ylabel('Latency (ms)')
ax2.set_xlim(0,60)
ax2.grid(True)
#ax2.legend()
tikzplotlib.save("max_lat.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots(figsize=(10,7))
#fig3.suptitle('Bandwidth Received')
ax3.plot(vector1, video_bw, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax3.plot(vector1, be_bw, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax3.plot(vector1, embb_bw, label='eMBB Traffic', color='orange', marker='^', linestyle='--', markersize=size)
ax3.plot(vector1, telemetry_bw, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax3.plot(vector1, urllc_bw, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax3.plot(total_bw, label= 'Total', color='black', marker='x', linestyle='-', markersize=size)
ax3.set_xlabel('t (s)')
ax3.set_ylabel('BW (Mbps)')
ax3.set_xlim(0,60)
ax3.set_ylim(top=105)
ax3.grid(True)
#ax3.legend()
tikzplotlib.save("bandwidth_received.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 6: Bandwidth Sent Behaviour
fig6, ax6 = plt.subplots(figsize=(10,7))
#fig6.suptitle('Bandwidth Sent')
ax6.plot(vector1, video_bw_s, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax6.plot(vector1, be_bw_s, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax6.plot(vector1, embb_bw_s, label='eMBB Traffic', color='orange', marker='^', linestyle='--', markersize=size)
ax6.plot(vector1, telemetry_bw_s, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax6.plot(vector1, urllc_bw_s, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax6.set_xlabel('t (s)')
ax6.set_ylabel('BW (Mbps)')
ax6.set_xlim(0,60)
ax6.grid(True)
#ax6.legend()
tikzplotlib.save("bandwidth_sent.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

plt.show()

