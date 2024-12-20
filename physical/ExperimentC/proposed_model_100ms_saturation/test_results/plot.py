import matplotlib.pyplot as plt
import numpy as np

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
#with open('files/clase_1_backlog', 'r') as file:
 #   for line in file:
  #      try:
   #         backlog_tna.append(float(line.strip()))
    #    except ValueError:
     #       backlog_tna.append(0)
#with open('files/clase_2_backlog', 'r') as file:
 #   for line in file:
  #      try:
   #         backlog_tnb.append(float(line.strip()))
    #    except ValueError:
     #       backlog_tnb.append(0)
#with open('files/clase_3_backlog', 'r') as file:
 #   for line in file:
  #      try:
   #         backlog_tnc.append(float(line.strip()))
    #    except ValueError:
     #       backlog_tnc.append(0)
#with open('files/clase_4_backlog', 'r') as file:
 #   for line in file:
  #      try:
   #         backlog_tnd.append(float(line.strip()))
    #    except ValueError:
     #       backlog_tnd.append(0)
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
with open('files/lat_metrics5', 'r') as file:
    for line in file:
        try:
            be_data.append(float(line.strip()))
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
with open('files/lat_max_metrics5', 'r') as file:
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
with open('files/bandwidth_metrics5_sender_burst_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_bw2 = [1538/1472*float(line.strip()) for line in lines]
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
be1 = np.array(be_bw2)
be2 = np.array(be_s_bw)

video_bw_s = video1 + video2
telemetry_bw_s = tel1 + tel2
embb_bw_s = embb1 + embb2
urllc_bw_s = urllc1 + urllc2
be_bw_s = be1 + be2

bw_video = np.array(video_bw)
bw_telemetry = np.array(telemetry_bw)
bw_embb = np.array(embb_bw)
bw_urllc = np.array(urllc_bw)
bw_be = np.array(be_bw)

total_bw = bw_video + bw_telemetry + bw_embb + bw_urllc + bw_be

vector1 = np.arange(0.1, 60.1, 0.1)

# Plot Customization
# Figura 1: Latency Behaviour
fig1, ax1 = plt.subplots()
fig1.suptitle('Latency Behaviour')
ax1.plot(vector1, video_data, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.')
ax1.plot(vector1, be_data, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--')
ax1.plot(vector1, embb_data, label='eMBB Traffic', color='orange', marker='^', linestyle='--')
ax1.plot(vector1, telemetry_data, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.')
ax1.plot(vector1, urllc_data, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-')
ax1.set_xlabel('t (s)')
ax1.set_ylabel('Latency (ms)')
ax1.set_xlim(left=0)
ax1.grid(True)
ax1.legend()

# Figura 2: Maximum Latency Behaviour
fig2, ax2 = plt.subplots()
fig2.suptitle('Maximum Latency Behaviour')
ax2.plot(vector1, video2_data, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.')
ax2.plot(vector1, be2_data, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--')
ax2.plot(vector1, embb2_data, label='eMBB Traffic', color='orange', marker='^', linestyle='--')
ax2.plot(vector1, telemetry2_data, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.')
ax2.plot(vector1, urllc2_data, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-')
ax2.set_xlabel('t (s)')
ax2.set_ylabel('Latency (ms)')
ax2.set_xlim(left=0)
ax2.grid(True)
ax2.legend()

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots()
fig3.suptitle('Bandwidth Received')
ax3.plot(vector1, video_bw, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.')
ax3.plot(vector1, be_bw, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--' )
ax3.plot(vector1, embb_bw, label='eMBB Traffic', color='orange', marker='^', linestyle='--')
ax3.plot(vector1, telemetry_bw, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.')
ax3.plot(vector1, urllc_bw, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-')
ax3.plot(vector1, total_bw, label= 'Total Traffic', color='black', marker='x', linestyle='-')
ax3.set_xlabel('t (s)')
ax3.set_ylabel('BW (Mbps)')
ax3.set_xlim(left=0)
ax3.grid(True)
ax3.legend()

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
fig6, ax6 = plt.subplots()
fig6.suptitle('Bandwidth Sent')
ax6.plot(vector1, video_bw_s, label='Video Traffic (RD)', color='#610B0B', marker='*', linestyle='-.')
ax6.plot(vector1, be_bw_s, label='BE Traffic', color='#F5A9BC', marker='p', linestyle='--' )
ax6.plot(vector1, embb_bw_s, label='eMBB Traffic', color='orange', marker='^', linestyle='--')
ax6.plot(vector1, telemetry_bw_s, label='Telemetry Traffic (RD)', color='#BEF781', marker='D', linestyle='-.')
ax6.plot(vector1, urllc_bw_s, label='URLLC Traffic', color='#0040FF', marker='o', linestyle='-')
ax6.set_xlabel('t (s)')
ax6.set_ylabel('BW (Mbps)')
ax6.set_xlim(left=0)
ax6.grid(True)
ax6.legend()

plt.show()
