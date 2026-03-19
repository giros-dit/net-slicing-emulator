import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

s1c1_data2 = []
s1c2_data2 = []
s3c2_data2 = []
s3c1_data2 = []
s2c1_data2 = []
s2c2_data2 = []


pktloss_tna = []
pktloss_tnb = []
pktloss_tnc = []
pktloss_tnd = []
backlog_tna = []
backlog_tnb = []
backlog_tnc = []
backlog_tnd = []

# Load values
#with open('files/clase_1_pktloss', 'r') as file:
 #   for line in file:
  #      try:
   #         pktloss_tna.append(float(line.strip()))
    #    except ValueError:
     #       pktloss_tna.append(0)
#with open('files/clase_2_pktloss', 'r') as file:
 #   for line in file:
  #      try:
   #         pktloss_tnb.append(float(line.strip()))
    #    except ValueError:
     #       pktloss_tnb.append(0)
#with open('files/clase_3_pktloss', 'r') as file:
 #   for line in file:
  #      try:
   #         pktloss_tnc.append(float(line.strip()))
    #    except ValueError:
     #       pktloss_tnc.append(0)
#with open('files/clase_4_pktloss', 'r') as file:
 #   for line in file:
  #      try:
   #         pktloss_tnd.append(float(line.strip()))
    #    except ValueError:
     #       pktloss_tnd.append(0)
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
with open('files/latency_max_metrics5', 'r') as file:
    for line in file:
        try:
            s2c2_data2.append(float(line.strip()))
        except ValueError:
            s2c2_data2.append(0)
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
with open('files/bandwidth_metrics6_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s3c2_s_bw = [1500/1458*float(line.strip()) for line in lines]
with open('files/bandwidth_metrics5_sender', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    s2c2_s_bw = [1500/1458*float(line.strip()) for line in lines]

s1c1 = np.array(s1c1_bw2) + np.array(s1c1_s_bw)
s1c2 = np.array(s1c2_bw2) + np.array(s1c2_s_bw)
s2c1 = np.array(s2c1_bw2) + np.array(s2c1_s_bw)
s2c2 = np.array(s2c2_bw2) + np.array(s2c2_s_bw)
s3c1 = np.array(s3c1_bw2) + np.array(s3c1_s_bw)
s3c2 = np.array(s3c2_s_bw)

total_bw = s1c1 + s1c2 + s2c1 + s2c2 + s3c1 + s3c2

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
ax2.plot(vector1, s2c1_data2, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax2.plot(vector1, s2c2_data2, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax2.set_xlabel('t (s)', fontsize=14)
ax2.set_ylabel('Latency (ms)', fontsize=14)
ax2.set_xlim(0,60)
ax2.set_ylim(0,30)
ax2.grid(True)
#ax2.legend()
tikzplotlib.save("latency_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots(figsize=(7,7))
#fig3.suptitle('Bandwidth Received')
ax3.plot(vector1, s1c1_bw, label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax3.plot(vector1, s2c1_bw, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size)
ax3.plot(vector1, s1c2_bw, label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, alpha=0.7, linewidth=line_size)
ax3.plot(vector1, s2c2_bw, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax3.plot(vector1, s3c1_bw, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax3.plot(vector1, s3c2_bw, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
ax3.set_xlabel('t (s)', fontsize=14)
ax3.set_ylabel('BW (Mbps)', fontsize=14)
ax3.set_xlim(0,60)
ax3.set_ylim(top=35)
ax3.grid(True)
#ax3.legend()
#tikzplotlib.save("bw_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

# Figura 4: Packet Loss in P
#fig4, ax4 = plt.subplots()
#fig4.suptitle('Packet Loss')
#ax4.plot(vector1, pktloss_tnb, label='TN QoS Class B', color='#610B0B', marker='*', linestyle='-.')
#ax4.plot(vector1, pktloss_tnd, label='TN QoS Class D', color='#F5A9BC', marker='p', linestyle='--' )
#ax4.plot(vector1, pktloss_tnc, label='TN QoS Class C', color='orange', marker='^', linestyle='--')
#ax4.plot(vector1, pktloss_tna, label='TN QoS Class A', color='#0040FF', marker='o', linestyle='-')
#ax4.set_xlabel('t (s)')
#ax4.set_ylabel('Packet Loss')
#ax4.grid(True)
#ax4.legend()

# Figura 5: Queue Size in P
#fig5, ax5 = plt.subplots()
#fig5.suptitle('Packets Queued')
#ax5.plot(vector1, backlog_tnb, label='TN QoS Class B', color='#610B0B', marker='*', linestyle='-.')
#ax5.plot(vector1, backlog_tnd, label='TN QoS Class D', color='#F5A9BC', marker='p', linestyle='--' )
#ax5.plot(vector1, backlog_tnc, label='TN QoS Class C', color='orange', marker='^', linestyle='--')
#ax5.plot(vector1, backlog_tna, label='TN QoS Class A', color='#0040FF', marker='o', linestyle='-')
#ax5.set_xlabel('t (s)')
#ax5.set_ylabel('Packets Queued')
#ax5.grid(True)
#ax5.legend()

# Figura 6: Bandwidth Sent Behaviour
fig6, ax6 = plt.subplots(figsize=(7,7))
#fig6.suptitle('Bandwidth Sent')
ax6.plot(vector1, s1c1, label='S1-C1', color='#006600', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax6.plot(vector1, s3c2, label='S3-C2', color='#610B0B', marker='p', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s3c1, label='S3-C1', color='orange', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s1c2, label='S1-C2', color='#99FF99', marker='^', linestyle='--', markersize=size, linewidth=line_size)
ax6.plot(vector1, s2c1, label='S2-C1', color='#0040FF', marker='o', linestyle='-', markersize=size, linewidth=line_size, alpha= 0.6)
ax6.plot(vector1, s2c2, label='S2-C2', color='#DAE8FC', marker='*', linestyle='-.', markersize=size, linewidth=line_size)
ax6.set_xlabel('t (s)', fontsize=14)
ax6.set_ylabel('BW (Mbps)', fontsize=14)
ax6.set_xlim(0,60)
ax6.grid(True)
#ax6.legend()
#tikzplotlib.save("bw_gen_expa.tex", axis_width="\\textwidth", axis_height="0.7\\textwidth")

#fig_legend1 = plt.figure(figsize=(10, 1))
#handles, labels = ax3.get_legend_handles_labels()
#fig_legend1.legend(handles, labels, loc='center', ncol=6)
#plt.axis('off')
#tikzplotlib.save("legend_expA.tex")

plt.show()

