import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('jitter_h1', 'r') as file:
    jitter_data = [float(line.strip()) for line in file]
with open('latency_h1', 'r') as file:
    latency_data = [float(line.strip()) for line in file]
with open('latency_h1_max', 'r') as file:
    latency_data = [float(line.strip()) for line in file]
with open('latency_h1_min', 'r') as file:
    latency_data = [float(line.strip()) for line in file]

# Plot Customization
fig, axes = plt.subplots(nrows=1, ncols=2) # Create a figure with two subplots
fig.suptitle('RD Video Latency and Jitter Behaviour')
axes[0].plot(latency_data, color='#610B0B')
axes[0].plot(latency_data_max, color='black')
axes[0].plot(latency_data_min, color='blue')
axes[0].set_title('Latency Behaviour')
axes[0].set_xlabel('t (s)')
axes[0].set_ylabel('RTT (ms)')
axes[0].grid(True)
axes[1].plot(jitter_data, color='#610B0B')
axes[1].set_title('Jitter Behaviour')
axes[1].set_xlabel('t (s)')
axes[1].set_ylabel('Jitter (ms)')
axes[1].grid(True)

plt.tight_layout()
plt.show()

