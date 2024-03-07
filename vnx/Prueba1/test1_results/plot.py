import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('bandwidth_server1', 'r') as file:
    be_data = [float(line.strip()) for line in file]
with open('bandwidth_server2_with_zeros', 'r') as file:
    video_data = [float(line.strip()) for line in file]
with open('bandwidth_server3_with_zeros', 'r') as file:
    telemetry_data = [float(line.strip()) for line in file]
with open('bandwidth_server4_with_zeros', 'r') as file:
    urllc_data = [float(line.strip()) for line in file]

# Compute Total Bandwidth
be_array = np.array(be_data)
video_array = np.array(video_data)
telemetry_array = np.array(telemetry_data)
urllc_array = np.array(urllc_data)

rd_bw = video_array + telemetry_array
total_bw = be_array + video_array + telemetry_array + urllc_array

# Plot Customization
plt.title('Proposed Model Behaviour')
plt.ylabel('Bandwidth (Mbps)')
plt.xlabel('t (s)')
plt.grid(True)

plt.plot(be_data, label='BE Traffic', color='#FFFF00')
plt.plot(video_data, label='Video Traffic (RD)', color='#DF0101', alpha=0.8)
plt.plot(telemetry_data, label='Telemetry Traffic (RD)', color='#F78181', alpha=0.8)
plt.plot(urllc_data, label='URLLC Traffic', color='#0040FF', alpha=0.8)
plt.plot(rd_bw, label='RD Traffic', color='#610B0B')
plt.plot(total_bw, label='Total Bandwidth', color='#0B610B', alpha=0.8)
plt.legend()
plt.show()

