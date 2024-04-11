import matplotlib.pyplot as plt
import numpy as np

latency1_data = []
telemetry1_data = []
be1_data = []
embb1_data = []
urllc1_data = []
latency2_data = []
telemetry2_data = []
be2_data = []
embb2_data = []
urllc2_data = []

# Load values
with open('latency_metrics1_with_zeros', 'r') as file:
    for line in file:
        try:
            latency1_data.append(float(line.strip()))
        except ValueError:
            latency1_data.append(0)
with open('latency_metrics2_with_zeros', 'r') as file:
    for line in file:
        try:
            telemetry1_data.append(float(line.strip()))
        except ValueError:
            telemetry1_data.append(0)
with open('latency_metrics3_with_zeros', 'r') as file: 
    for line in file:
        try:
            embb1_data.append(float(line.strip()))
        except ValueError:
            embb1_data.append(0)
with open('latency_metrics4', 'r') as file:
    for line in file:
        try:
            be1_data.append(float(line.strip()))
        except ValueError:
            be1_data.append(0)
with open('latency_metrics5_with_zeros', 'r') as file:
    for line in file:
        try:
            urllc1_data.append(float(line.strip()))
        except ValueError:
            urllc1_data.append(0)
with open('latency_max_metrics1_with_zeros', 'r') as file:
    for line in file:
        try:
            latency2_data.append(float(line.strip()))
        except ValueError:
            latency2_data.append(0)
with open('latency_max_metrics2_with_zeros', 'r') as file:
    for line in file:
        try:
            telemetry2_data.append(float(line.strip()))
        except ValueError:
            telemetry2_data.append(0)
with open('latency_max_metrics3_with_zeros', 'r') as file:
    for line in file:
        try:
            embb2_data.append(float(line.strip()))
        except ValueError:
            embb2_data.append(0)
with open('latency_max_metrics4', 'r') as file:
    for line in file:
        try:
            be2_data.append(float(line.strip()))
        except ValueError:
            be2_data.append(0)
with open('latency_max_metrics5_with_zeros', 'r') as file:
    for line in file:
        try:
            urllc2_data.append(float(line.strip()))
        except ValueError:
            urllc2_data.append(0)
with open('bandwidth_metrics1_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    video_bw = [float(line.strip()) for line in lines]
with open('bandwidth_metrics2_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    telemetry_bw = [float(line.strip()) for line in lines]
with open('bandwidth_metrics3_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    embb_bw = [float(line.strip()) for line in lines]
with open('bandwidth_metrics4', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    be_bw = [float(line.strip()) for line in lines]
with open('bandwidth_metrics5_with_zeros', 'r') as file:
    lines = [line.replace(',', '.') for line in file]
    urllc_bw = [float(line.strip()) for line in lines]

vector1 = np.arange(1, 120, 1)

# Compute Total Bandwidth
be_array = np.array(be_bw)
video_array = np.array(video_bw)
telemetry_array = np.array(telemetry_bw)
urllc_array = np.array(urllc_bw)
embb_array = np.array(embb_bw)

rd_bw = video_array + telemetry_array
total_bw = be_array + video_array + telemetry_array + urllc_array + embb_array

# Plot Customization
# Figura 1: Latency Behaviour
fig1, ax1 = plt.subplots()
fig1.suptitle('Latency Behaviour')
ax1.plot(vector1, latency1_data, label='Video h1', color='#610B0B')
ax1.plot(vector1, be1_data, label='BE Traffic h4', color='#F5A9BC', alpha=0.6)
ax1.plot(vector1, embb1_data, label='eMBB Traffic', color='orange', alpha=0.9)
ax1.plot(vector1, telemetry1_data, label='Telemetry Traffic (RD)', color='#BEF781', alpha=0.6)
ax1.plot(vector1, urllc1_data, label='URLLC Traffic h5', color='#0040FF')
ax1.set_xlabel('t (s)')
ax1.set_ylabel('Latency (ms)')
ax1.set_xlim(left=0)
ax1.grid(True)
ax1.legend()

# Figura 2: Maximum Latency Behaviour
fig2, ax2 = plt.subplots()
fig2.suptitle('Maximum Latency Behaviour')
ax2.plot(vector1, latency2_data, label='Video h1', color='#610B0B')
ax2.plot(vector1, be2_data, label='BE Traffic h4', color='#F5A9BC', alpha=0.6)
ax2.plot(vector1, embb2_data, label='eMBB Traffic', color='orange', alpha=0.9)
ax2.plot(vector1, telemetry2_data, label='Telemetry Traffic (RD)', color='#BEF781', alpha=0.6)
ax2.plot(vector1, urllc2_data, label='URLLC Traffic h5', color='#0040FF')
ax2.set_xlabel('t (s)')
ax2.set_ylabel('Latency (ms)')
ax2.set_xlim(left=0)
ax2.grid(True)
ax2.legend()

# Figura 3: Bandwidth Behaviour
fig3, ax3 = plt.subplots()
fig3.suptitle('Bandwidth Behaviour')
ax3.plot(vector1, video_bw, label='Video h1', color='#DF0101')
ax3.plot(vector1, be_bw, label='BE Traffic h4', color='#F5A9BC', alpha=0.6)
ax3.plot(vector1, embb_bw, label='eMBB Traffic', color='orange', alpha=0.9)
ax3.plot(vector1, telemetry_bw, label='Telemetry Traffic (RD)', color='#BEF781', alpha=0.6)
ax3.plot(vector1, urllc_bw, label='URLLC Traffic h5', color='#0040FF')
plt.plot(vector1, rd_bw, label='RD Traffic', color='#610B0B')
plt.plot(vector1, total_bw, label='Total Bandwidth', color='#0B610B', alpha=0.8)

ax3.set_xlabel('t (s)')
ax3.set_ylabel('BW (Mbps)')
ax3.set_xlim(left=0)
ax3.grid(True)
ax3.legend()

plt.show()
