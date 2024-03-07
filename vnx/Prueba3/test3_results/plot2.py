import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('jitter_h1', 'r') as file:
    jitter_data = [float(line.strip()) for line in file]
with open('latency_h1', 'r') as file:
    latency_data = [float(line.strip()) for line in file]
with open('latency_h2_with_zeros', 'r') as file:
    telemetry_data = [float(line.strip()) for line in file]
with open('latency_h3_with_zeros', 'r') as file:
    embb_data = [float(line.strip()) for line in file]
with open('latency_h4_with_zeros', 'r') as file:
    be_data = [float(line.strip()) for line in file]
with open('latency_h5_with_zeros', 'r') as file:
    urllc_data = [float(line.strip()) for line in file]

# Plot Customization
fig, axes = plt.subplots(nrows=1, ncols=2) # Create a figure with two subplots
fig.suptitle('RD Video Latency and Jitter Behaviour')
axes[0].plot(latency_data, label='Video', color='#610B0B')
axes[0].plot(be_data, label='BE Traffic', color='#FFFF00')
axes[0].plot(embb_data, label='eMBB Traffic', color='black', alpha=0.8)
axes[0].plot(telemetry_data, label='Telemetry Traffic (RD)', color='#F78181', alpha=0.8)
axes[0].plot(urllc_data, label='URLLC Traffic', color='#0040FF', alpha=0.8)
axes[0].set_title('Latency Behaviour')
axes[0].set_xlabel('t (s)')
axes[0].set_ylabel('RTT (ms)')
axes[0].grid(True)
axes[0].legend()
axes[1].plot(jitter_data, color='#610B0B')
axes[1].set_title('Jitter Behaviour')
axes[1].set_xlabel('t (s)')
axes[1].set_ylabel('Jitter (ms)')
axes[1].grid(True)

plt.tight_layout()
plt.show()

