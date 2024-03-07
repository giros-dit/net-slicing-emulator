import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('jitter_h1', 'r') as file:
    jitter_data = [float(line.strip()) for line in file]
with open('latency_h1', 'r') as file:
    latency1_data = [float(line.strip()) for line in file]
with open('latency_h2_with_zeros', 'r') as file:
    telemetry_data = [float(line.strip()) for line in file]
with open('latency_h3_with_zeros', 'r') as file:
    be1_data = [float(line.strip()) for line in file]
with open('latency_h4_with_zeros', 'r') as file:
    embb_data = [float(line.strip()) for line in file]
with open('latency_h5_with_zeros', 'r') as file:
    urllc1_data = [float(line.strip()) for line in file]
with open('latency_h6', 'r') as file:
    latency2_data = [float(line.strip()) for line in file]
with open('latency_h7', 'r') as file:
    latency3_data = [float(line.strip()) for line in file]
with open('latency_h8_with_zeros', 'r') as file:
    urllc2_data = [float(line.strip()) for line in file]
with open('latency_h9_with_zeros', 'r') as file:
    urllc3_data = [float(line.strip()) for line in file]
with open('latency_h10_with_zeros', 'r') as file:
    be2_data = [float(line.strip()) for line in file]



# Plot Customization
fig, axes = plt.subplots(nrows=1, ncols=2) # Create a figure with two subplots
fig.suptitle('RD Video Latency and Jitter Behaviour')
axes[0].plot(latency1_data, label='Video h1', color='#610B0B')
axes[0].plot(be1_data, label='BE Traffic h3', color='#FFFF00')
axes[0].plot(embb_data, label='eMBB Traffic', color='black', alpha=0.8)
axes[0].plot(telemetry_data, label='Telemetry Traffic (RD)', color='#F78181', alpha=0.8)
axes[0].plot(urllc1_data, label='URLLC Traffic h5', color='#0040FF', alpha=0.8)
axes[0].plot(latency2_data, label='Video h6', color='#8A0808')
axes[0].plot(latency3_data, label='Video h7', color='#B40404')
axes[0].plot(urllc2_data, label='URLLC Traffic h8', color='#007CFF', alpha=0.8)
axes[0].plot(urllc3_data, label='URLLC Traffic h9', color='#00D4FF', alpha=0.8)
axes[0].plot(be2_data, label='BE Traffic h10', color='#FFB200')

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

