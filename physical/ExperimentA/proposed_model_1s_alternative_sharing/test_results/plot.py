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

pktloss_tna = []
pktloss_tnb = []
pktloss_tnc = []
pktloss_tnd = []
backlog_tna = []
backlog_tnb = []
backlog_tnc = []
backlog_tnd = []

# Load values
with open('files/clase_1_pktloss', 'r') as file:
    for line in file:
        try:
            pktloss_tna.append(float(line.strip()))
        except ValueError:
            pktloss_tna.append(0)
with open('files/clase_2_pktloss', 'r') as file:
    for line in file:
        try:
            pktloss_tnb.append(float(line.strip()))
        except ValueError:
            pktloss_tnb.append(0)
with open('files/clase_3_pktloss', 'r') as file:
    for line in file:
        try:
            pktloss_tnc.append(float(line.strip()))
        except ValueError:
            pktloss_tnc.append(0)
with open('files/clase_4_pktloss', 'r') as file:
    for line in file:
        try:
            pktloss_tnd.append(float(line.strip()))
        except ValueError:
            pktloss_tnd.append(0)

with open('files/clase_1_backlog', 'r') as file:
    for line in file:
        try:
            backlog_tna.append(float(line.strip()))
        except ValueError:
            backlog_tna.append(0)
with open('files/clase_2_backlog', 'r') as file:
    for line in file:
        try:
            backlog_tnb.append(float(line.strip()))
        except ValueError:
            backlog_tnb.append(0)
with open('files/clase_3_backlog', 'r') as file:
    for line in file:
        try:
            backlog_tnc.append(float(line.strip()))
        except ValueError:
            backlog_tnc.append(0)
with open('files/clase_4_backlog', 'r') as file:
    for line in file:
        try:
            backlog_tnd.append(float(line.strip()))
        except ValueError:
            backlog_tnd.append(0)

with open('files/latency_metrics1_with_zeros', 'r') as file:
    for line in file:
        try:
            video_data.append(float(line.strip()))
        except ValueError:
            video_data.append(0)
with open('files/latency_metrics2_with_zeros', 'r') as file:
    for line in file:
        try:
            telemetry_data.append(float(line.strip()))
        except ValueError:
            telemetry_data.append(0)
with open('files/latency_metrics3_with_zeros', 'r') as file:
    for line in file:
        try:
            embb_data.append(float(line.strip()))
        except ValueError:
            embb_data.append(0)
with open('files/latency_metrics4_with_zeros', 'r') as file:
    for line in file:
        try:
            urllc_data.append(float(line.strip()))
        except ValueError:
            urllc_data.append(0)
with open('files/latency_metrics5', 'r') as file:
    for line in file:
        try:
            be_data.append(float(line.strip()))
        except ValueError:
            be_data.append(0)

with open('files/latency_max_metrics1_with_zeros', 'r') as file:
    for line in file:
        try:
            video2_data.append(float(line.strip()))
        except ValueError:
            video2_data.append(0)
with open('files/latency_max_metrics2_with_zeros', 'r') as file:
    for line in file:
        try:
            telemetry2_data.append(float(line.strip()))
        except ValueError:
            telemetry2_data.append(0)
with open('files/latency_max_metrics3_with_zeros', 'r') as file:
    for line in file:
        try:
            embb2_data.append(float(line.strip()))
        except ValueError:
            embb2_data.append(0)
with open('files/latency_max_metrics4_with_zeros', 'r') as file:
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

with open('files/bandwidth_metrics1_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics2_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics3_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics4_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_bw = [1538/1472*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_bw = [1538/1472*float(line.strip()) for line in lines]

video_bw = np.array(video_bw)
telemetry_bw = np.array(telemetry_bw)
embb_bw = np.array(embb_bw)
urllc_bw = np.array(urllc_bw)
be_bw = np.array(be_bw)

total_bw = video_bw + telemetry_bw + embb_bw + urllc_bw + be_bw
vector1 = np.arange(1, 101, 1)

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

size=3

# Figura 2: Maximum Latency Behaviour
fig2, ax2 = plt.subplots(figsize=(10,6))
#fig2.suptitle('Maximum Latency Behaviour')
ax2.plot(vector1, video2_data, label='RD: Video', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax2.plot(vector1, be2_data, label='eMBB: BE', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax2.plot(vector1, embb2_data, label='eMBB: VC', color='orange', marker='^', linestyle='--', markersize=size)
ax2.plot(vector1, telemetry2_data, label='RD: Telemetry', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax2.plot(vector1, urllc2_data, label='URLLC', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax2.set_xlabel('t (s)')
ax2.set_ylabel('Latency (ms)')
ax2.set_xlim(0,100)
ax2.grid(True)
#ax2.legend()

tikzplotlib.save("maximum_latency_behaviour.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots(figsize=(10,6))
#fig3.suptitle('Bandwidth Behaviour')
ax3.plot(video_bw, label='ToD: Video', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax3.plot(telemetry_bw, label='ToD: Telemetry', color='#BEF781', marker='D', linestyle='-.', markersize=size)
ax3.plot(embb_bw, label='eMBB: VC', color='orange', marker='^', linestyle='--', markersize=size)
ax3.plot(be_bw, label='eMBB: BE', color='#F5A9BC', marker='p', linestyle='--', markersize=size )
ax3.plot(urllc_bw, label='URLLC', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax3.plot(total_bw, label= 'Total', color='black', marker='x', linestyle='-', markersize=size)
ax3.set_xlabel('t (s)')
ax3.set_ylabel('BW (Mbps)')
ax3.set_xlim(0,100)
ax3.grid(True)
#ax3.legend()

tikzplotlib.save("bandwidth_behaviour.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")


# Figura 4: Packet Loss in P
fig4, ax4 = plt.subplots(figsize=(10,6))
#fig4.suptitle('Packet Loss')


ax4.plot(pktloss_tna, label='TN QoS Class A', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax4.plot(pktloss_tnb, label='TN QoS Class B', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax4.plot(pktloss_tnc, label='TN QoS Class C', color='orange', marker='^', linestyle='--', markersize=size)
ax4.plot(pktloss_tnd, label='TN QoS Class D', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax4.set_xlabel('t (s)')
ax4.set_ylabel('Packet Loss')
ax4.set_xlim(0,100)
ax4.set_ylim(-0.1,0.1)
ax4.set_yticks([0, 1])
ax4.grid(True)
#ax4.legend()

tikzplotlib.save("packet_loss.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

# Figura 5: Queue Size in P
fig5, ax5 = plt.subplots(figsize=(10,6))
#fig5.suptitle('Packets Queued')
ax5.plot(backlog_tna, label='TN QoS Class A', color='#0040FF', marker='o', linestyle='-', markersize=size)
ax5.plot(backlog_tnb, label='TN QoS Class B', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax5.plot(backlog_tnc, label='TN QoS Class C', color='orange', marker='^', linestyle='--', markersize=size)
ax5.plot(backlog_tnd, label='TN QoS Class D', color='#F5A9BC', marker='p', linestyle='--', markersize=size)
ax5.set_xlabel('t (s)')
ax5.set_ylabel('Packets Queued')
ax5.set_xlim(0,100)
ax5.set_ylim(-0.1,0.1)
ax5.set_yticks([0, 1])
ax5.grid(True)
#ax5.legend()
tikzplotlib.save("queue_size.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

fig_legend1 = plt.figure(figsize=(10, 1))
handles, labels = ax3.get_legend_handles_labels()
fig_legend1.legend(handles, labels, loc='center', ncol=3)
plt.axis('off')
tikzplotlib.save("legend_5g.tex")

fig_legend2 = plt.figure(figsize=(10, 1))
handles, labels = ax4.get_legend_handles_labels()
fig_legend2.legend(handles, labels, loc='center', ncol=5)
plt.axis('off')
tikzplotlib.save("legend_tn.tex")


plt.show()
