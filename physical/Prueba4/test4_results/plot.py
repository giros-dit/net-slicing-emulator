import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('h5', 'r') as file:
    h5_data = [float(line.strip()) for line in file]
with open('h1', 'r') as file:
    h1_data = [float(line.strip()) for line in file]
with open('h5_equal', 'r') as file:
    h5_equal_data = [float(line.strip()) for line in file]
with open('h1_equal', 'r') as file:
    h1_equal_data = [float(line.strip()) for line in file]

x_values = ["1Mbps", "3Mbps", "5Mbps", "10Mbps", "20 Mbps", "40 Mbps"]

# Plot Customization
bar_width= 0.2
bar_positions = np.arange(len(x_values))

plt.bar(bar_positions - 1.5 * bar_width, h1_data, width=bar_width, label='Video Latency with lower priority', color='#610B0B')
plt.bar(bar_positions - 0.5 * bar_width, h5_data, width=bar_width, label='URLLC Latency with higher priority', color='#0040FF')
plt.bar(bar_positions + 0.5 * bar_width, h1_equal_data, width=bar_width, label='Video Latency with equal priority', color='#FFBB33')
plt.bar(bar_positions + 1.5 * bar_width, h5_equal_data, width=bar_width, label='URLLC Latency with equal priority', color='#33F9FF')
plt.title('Latency Behaviour Regarding URLLC Bandwidths')
plt.xticks(bar_positions, x_values)
plt.xlabel('URLLC Bandwidths')
plt.ylabel('RTT (ms)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

