import matplotlib.pyplot as plt
import numpy as np
import os
import tikzplotlib

configurations = 4
classes_5g = ["video", "telemetry", "embb", "urllc", "be"]
classes_tn = ["tna", "tnb", "tnc", "tnd"]
metrics_per_5g_class = ["latency", "latency_max", "bandwidth"]
metrics_per_tn_class = ["pktloss", "backlog"]

qos_data_5g = {}
qos_data_tn = {}

for class_5g in classes_5g:
    qos_data_5g[class_5g] = {}
    for i in range(1, configurations + 1):
        qos_data_5g[class_5g][f"conf{i}"] = {}
        for metric in metrics_per_5g_class:
            qos_data_5g[class_5g][f"conf{i}"][metric] = {}

for tn_class in classes_tn:
    qos_data_tn[tn_class] = {}
    for i in range(1, configurations + 1):
        qos_data_tn[tn_class][f"conf{i}"] = {}
        for metric in metrics_per_tn_class:
            qos_data_tn[tn_class][f"conf{i}"][metric] = {}

file_directory = "files"

# Load values
def load_file(file_path, class_type, conf, metric):
    values = []
    with open(file_path, 'r') as file:
        if metric == "bandwidth":
           lines = [line.replace(',', '.') for line in file]
           values = [1538/1472*float(line.strip()) for line in lines]
        else:
            for line in file:
                try:
                    values.append(float(line.strip()))
                except ValueError:
                    values.append(0)
    if class_type in classes_5g:
       qos_data_5g[class_type][f"conf{conf}"][metric] = values
    else:
       qos_data_tn[class_type][f"conf{conf}"][metric] = values

for i, class_5g in enumerate(classes_5g, 1):
    for j in range(1, configurations + 1):
        for metric in metrics_per_5g_class:
           file_name = f"{metric}_metrics{i}_{j}"
           file_path = os.path.join(file_directory, file_name)
           if os.path.exists(file_path):
              load_file(file_path, class_5g, j, metric)

for x, tn_class in enumerate(classes_tn, 1):
    for j in range(1, configurations + 1):
        for metric in metrics_per_tn_class:
            file_name = f"clase_{x}_{metric}_{j}"
            file_path = os.path.join(file_directory, file_name)
            if os.path.exists(file_path):
               load_file(file_path, tn_class, j, metric)
vector1 = np.arange(1, 101, 1)
size=3
# Plot Customization
# Figura 1: Video Traffic Latency Behaviour
#fig1, ax1 = plt.subplots()
#fig1.suptitle('Video Traffic Latency Behaviour')
#ax1.plot(vector1, qos_data_5g["video"]["conf1"]["latency"], label='Video 1', color='#610B0B', marker='*', linestyle='-.')
#ax1.plot(vector1, qos_data_5g["video"]["conf2"]["latency"], label='Video 2', color='#AE1515', marker='p', linestyle='--')
#ax1.plot(vector1, qos_data_5g["video"]["conf3"]["latency"], label='Video 3', color='#E61D1D', marker='^', linestyle='--')
#ax1.plot(vector1, qos_data_5g["video"]["conf4"]["latency"], label='Video 4', color='#FC0303', marker='D', linestyle='-.')
#ax1.plot(vector1, qos_data_5g["telemetry"]["conf1"]["latency"], label='Telemetry 1', color='#BEF781', marker='*', linestyle='-.')
#ax1.plot(vector1, qos_data_5g["telemetry"]["conf2"]["latency"], label='Telemetry 2', color='#97D654', marker='p', linestyle='--')
#ax1.plot(vector1, qos_data_5g["telemetry"]["conf3"]["latency"], label='Telemetry 3', color='#71C616', marker='^', linestyle='--')
#ax1.plot(vector1, qos_data_5g["telemetry"]["conf4"]["latency"], label='Telemetry 4', color='#2A5200', marker='D', linestyle='-.')
#ax1.set_xlabel('t (s)')
#ax1.set_ylabel('Latency (ms)')
#ax1.set_xlim(left=0)
#ax1.grid(True)
#ax1.legend()

# Figura 2: Video Traffic Maximum Latency Behaviour
#fig2, ax2 = plt.subplots()
#fig2.suptitle('Video and Telemetry Traffic Maximum Latency Behaviour')
#ax2.plot(vector1, qos_data_5g["video"]["conf1"]["latency_max"], label='q_TNB=1538, q_TNC=1538, q_TND=15380', color='#610B0B', marker='*', linestyle='-.')
#ax2.plot(vector1, qos_data_5g["video"]["conf2"]["latency_max"], label='q_TNB=1538, q_TNC=15380, q_TND=1538', color='#AE1515', marker='p', linestyle='--')
#ax2.plot(vector1, qos_data_5g["video"]["conf3"]["latency_max"], label='q_TNB=15380, q_TNC=1538, q_TND=1538', color='#E61D1D', marker='^', linestyle='--')
#ax2.plot(vector1, qos_data_5g["video"]["conf4"]["latency_max"], label='q_TNB=15380, q_TNC=10766, q_TND=1538', color='#FC0303', marker='D', linestyle='-.')
#ax2.plot(vector1, qos_data_5g["telemetry"]["conf1"]["latency_max"], label='Telemetry q_TNB=1538, q_TNC=1538, q_TND=15380', color='#BEF781', marker='*', linestyle='-.')
#ax2.plot(vector1, qos_data_5g["telemetry"]["conf2"]["latency_max"], label='Telemetry q_TNB=1538, q_TNC=15380, q_TND=1538', color='#97D654', marker='p', linestyle='--')
#ax2.plot(vector1, qos_data_5g["telemetry"]["conf3"]["latency_max"], label='Telemetry q_TNB=15380, q_TNC=1538, q_TND=1538', color='#71C616', marker='^', linestyle='--')
#ax2.plot(vector1, qos_data_5g["telemetry"]["conf4"]["latency_max"], label='Telemetry q_TNB=15380, q_TNC=10766, q_TND=1538', color='#2A5200', marker='D', linestyle='-.')
#ax2.set_xlabel('t (s)')
#ax2.set_ylabel('Latency (ms)')
#ax2.set_xlim(left=0)
#ax2.grid(True)
#ax2.legend()

# Figura 3: TNB Queue Size in P
#fig3, ax3 = plt.subplots()
#fig3.suptitle('Packets Queued in TNB TNC Queue')
#ax3.plot(vector1, qos_data_tn["tnb"]["conf1"]["backlog"], label='TNB 1', color='#610B0B', marker='*', linestyle='-.')
#ax3.plot(vector1, qos_data_tn["tnb"]["conf2"]["backlog"], label='TNB 2', color='#AE1515', marker='p', linestyle='--')
#ax3.plot(vector1, qos_data_tn["tnb"]["conf3"]["backlog"], label='TNB 3', color='#E61D1D', marker='^', linestyle='--')
#ax3.plot(vector1, qos_data_tn["tnb"]["conf4"]["backlog"], label='TNB 4', color='#FC0303', marker='D', linestyle='-.')
#ax3.plot(vector1, qos_data_tn["tnc"]["conf1"]["backlog"], label='TNC 1', color='#BEF781', marker='*', linestyle='-.')
#ax3.plot(vector1, qos_data_tn["tnc"]["conf2"]["backlog"], label='TNC 2', color='#97D654', marker='p', linestyle='--')
#ax3.plot(vector1, qos_data_tn["tnc"]["conf3"]["backlog"], label='TNC 3', color='#71C616', marker='^', linestyle='--')
#ax3.plot(vector1, qos_data_tn["tnc"]["conf4"]["backlog"], label='TNC 4', color='#2A5200', marker='D', linestyle='-.')
#ax3.set_xlabel('t (s)')
#ax3.set_ylabel('Packets Queued')
#ax3.grid(True)
#ax3.legend()


# Figura 4: TNB Packet Loss in P
fig4, ax4 = plt.subplots(figsize=(10,6))
#fig4.suptitle('Packet Loss in TNB Queue')
ax4.plot(vector1, qos_data_tn["tnb"]["conf1"]["pktloss"], label='qTNB=1538, qTNC=1538, qTND=15380', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax4.plot(vector1, qos_data_tn["tnb"]["conf2"]["pktloss"], label='qTNB=1538, qTNC=15380, qTND=1538', color='#AE1515', marker='p', linestyle='--', markersize=size)
ax4.plot(vector1, qos_data_tn["tnb"]["conf3"]["pktloss"], label='qTNB=15380, qTNC=1538, qTND=1538', color='#E61D1D', marker='^', linestyle='--', markersize=size)
ax4.plot(vector1, qos_data_tn["tnb"]["conf4"]["pktloss"], label='qTNB=15380, qTNC=10766, qTND=1538', color='#FC0303', marker='D', linestyle='-.', markersize=size)
ax4.set_xlabel('t (s)')
ax4.set_ylabel('Packet Loss')
ax4.set_xlim(0,100)
ax4.grid(True)
#ax4.legend()
tikzplotlib.save("video_pl.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

# Figura 5: Video Traffic Bandwidth Behaviour
fig5, ax5 = plt.subplots(figsize=(10,6))
#fig5.suptitle('Video Traffic Bandwidth Behaviour')
ax5.plot(vector1, qos_data_5g["video"]["conf1"]["bandwidth"], label='q_TNB=1538, q_TNC=1538, q_TND=15380', color='#610B0B', marker='*', linestyle='-.', markersize=size)
ax5.plot(vector1, qos_data_5g["video"]["conf2"]["bandwidth"], label='q_TNB=1538, q_TNC=15380, q_TND=1538', color='#AE1515', marker='p', linestyle='--', markersize=size)
ax5.plot(vector1, qos_data_5g["video"]["conf3"]["bandwidth"], label='q_TNB=15380, q_TNC=1538, q_TND=1538', color='#E61D1D', marker='^', linestyle='--', markersize=size)
ax5.plot(vector1, qos_data_5g["video"]["conf4"]["bandwidth"], label='q_TNB=15380, q_TNC=10766, q_TND=1538', color='#FC0303', marker='D', linestyle='-.', markersize=size)
ax5.set_xlabel('t (s)')
ax5.set_ylabel('Bandwidth (Mbps)')
ax5.set_xlim(0,100)
ax5.grid(True)
#ax5.legend()
tikzplotlib.save("video_bandwidth.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

# Figura 6: Telemetry Traffic Latency Behaviour
#fig6, ax6 = plt.subplots()
#fig6.suptitle('Telemetry Traffic Latency Behaviour')
#ax6.plot(vector1, qos_data_5g["telemetry"]["conf1"]["latency"], label='Telemetry 1', color='#BEF781', marker='*', linestyle='-.')
#ax6.plot(vector1, qos_data_5g["telemetry"]["conf2"]["latency"], label='Telemetry 2', color='#97D654', marker='p', linestyle='--')
#ax6.plot(vector1, qos_data_5g["telemetry"]["conf3"]["latency"], label='Telemetry 3', color='#71C616', marker='^', linestyle='--')
#ax6.plot(vector1, qos_data_5g["telemetry"]["conf4"]["latency"], label='Telemetry 4', color='#2A5200', marker='D', linestyle='-.')
#ax6.set_xlabel('t (s)')
#ax6.set_ylabel('Latency (ms)')
#ax6.set_xlim(left=0)
#ax6.grid(True)
#ax6.legend()

# Figura 7: Maximum Latency Behaviour
#fig7, ax7 = plt.subplots()
#fig7.suptitle('Telemetry Traffic Maximum Latency Behaviour')
#ax7.plot(vector1, qos_data_5g["telemetry"]["conf1"]["latency_max"], label='q_TNB=1538, q_TNC=1538, q_TND=15380', color='#BEF781', marker='*', linestyle='-.')
#ax7.plot(vector1, qos_data_5g["telemetry"]["conf2"]["latency_max"], label='q_TNB=1538, q_TNC=15380, q_TND=1538', color='#97D654', marker='p', linestyle='--')
#ax7.plot(vector1, qos_data_5g["telemetry"]["conf3"]["latency_max"], label='q_TNB=15380, q_TNC=1538, q_TND=1538', color='#71C616', marker='^', linestyle='--')
#ax7.plot(vector1, qos_data_5g["telemetry"]["conf4"]["latency_max"], label='q_TNB=15380, q_TNC=10766, q_TND=1538', color='#2A5200', marker='D', linestyle='-.')
#ax7.set_xlabel('t (s)')
#ax7.set_ylabel('Latency (ms)')
#ax7.set_xlim(left=0)
#ax7.grid(True)
#ax7.legend()

# Figura 8: TNC Queue Size in P
#fig8, ax8 = plt.subplots()
#fig8.suptitle('Packets Queued in TNC Queue')
#ax8.plot(vector1, qos_data_tn["tnc"]["conf1"]["backlog"], label='TNC 1', color='#BEF781', marker='*', linestyle='-.')
#ax8.plot(vector1, qos_data_tn["tnc"]["conf2"]["backlog"], label='TNC 2', color='#97D654', marker='p', linestyle='--')
#ax8.plot(vector1, qos_data_tn["tnc"]["conf3"]["backlog"], label='TNC 3', color='#71C616', marker='^', linestyle='--')
#ax8.plot(vector1, qos_data_tn["tnc"]["conf4"]["backlog"], label='TNC 4', color='#2A5200', marker='D', linestyle='-.')
#ax8.set_xlabel('t (s)')
#ax8.set_ylabel('Packets Queued')
#ax8.grid(True)
#ax8.legend()


# Figura 9: TNC Packet Loss in P
fig9, ax9 = plt.subplots(figsize=(10,6))
#fig9.suptitle('Packet Loss in TNC Queue')
ax9.plot(vector1, qos_data_tn["tnc"]["conf1"]["pktloss"], label='qTNB=1538, qTNC=1538, qTND=15380', color='#BEF781', marker='*', linestyle='-.', markersize=size)
ax9.plot(vector1, qos_data_tn["tnc"]["conf2"]["pktloss"], label='qTNB=1538, qTNC=15380, qTND=1538', color='#97D654', marker='p', linestyle='--', markersize=size)
ax9.plot(vector1, qos_data_tn["tnc"]["conf3"]["pktloss"], label='qTNB=15380, qTNC=1538, qTND=1538', color='#71C616', marker='^', linestyle='--', markersize=size)
ax9.plot(vector1, qos_data_tn["tnc"]["conf4"]["pktloss"], label='qTNB=15380, qTNC=10766, qTND=1538', color='#2A5200', marker='D', linestyle='-.', markersize=size)
ax9.set_xlabel('t (s)')
ax9.set_ylabel('Packet Loss')
ax9.set_xlim(0,100)
ax9.grid(True)
#ax9.legend()
tikzplotlib.save("telemetry_pl.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

# Figura 10: Telemetry Traffic Bandwidth Behaviour
fig10, ax10 = plt.subplots(figsize=(10,6))
#fig10.suptitle('Telemetry Traffic Bandwidth Behaviour')
ax10.plot(vector1, qos_data_5g["telemetry"]["conf1"]["bandwidth"], label='q_TNB=1538, q_TNC=1538, q_TND=15380', color='#BEF781', marker='*', linestyle='-.', markersize=size)
ax10.plot(vector1, qos_data_5g["telemetry"]["conf2"]["bandwidth"], label='q_TNB=1538, q_TNC=15380, q_TND=1538', color='#97D654', marker='p', linestyle='--', markersize=size)
ax10.plot(vector1, qos_data_5g["telemetry"]["conf3"]["bandwidth"], label='q_TNB=15380, q_TNC=1538, q_TND=1538', color='#71C616', marker='^', linestyle='--', markersize=size)
ax10.plot(vector1, qos_data_5g["telemetry"]["conf4"]["bandwidth"], label='q_TNB=15380, q_TNC=10766, q_TND=1538', color='#2A5200', marker='D', linestyle='-.', markersize=size)
ax10.set_xlabel('t (s)')
ax10.set_ylabel('Bandwidth (Mbps)')
ax10.set_xlim(0,100)
ax10.grid(True)
#ax10.legend()
tikzplotlib.save("telemetry_bandwidth.tex", axis_width="\\textwidth", axis_height="0.6\\textwidth")

fig_legend1 = plt.figure(figsize=(10, 1))
handles, labels = ax4.get_legend_handles_labels()
fig_legend1.legend(handles, labels, loc='center', ncol=2)
plt.axis('off')
tikzplotlib.save("legend_video.tex")

fig_legend2 = plt.figure(figsize=(10, 1))
handles, labels = ax9.get_legend_handles_labels()
fig_legend2.legend(handles, labels, loc='center', ncol=2)
plt.axis('off')
tikzplotlib.save("legend_telemetry.tex")


plt.show()


