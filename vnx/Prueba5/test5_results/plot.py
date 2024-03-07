import matplotlib.pyplot as plt
import numpy as np

# Load values
with open('bandwidth_LP_equal', 'r') as file:
    LP_data = [float(line.strip()) for line in file]
with open('bandwidth_LP_aggressive', 'r') as file:
    LP_aggressive_data = [float(line.strip()) for line in file]
with open('bandwidth_HP_equal_with_zeros', 'r') as file:
    HP_data = [float(line.strip()) for line in file]
with open('bandwidth_HP_aggressive_with_zeros', 'r') as file:
    HP_aggressive_data = [float(line.strip()) for line in file]

#Compute Total Bandwidth
LP_data_array = np.array(LP_data)
HP_data_array = np.array(HP_data)
total_video = LP_data_array + HP_data_array

LP_data_a_array = np.array(LP_aggressive_data)
HP_data_a_array = np.array(HP_aggressive_data)
total_video_aggressive = LP_data_a_array + HP_data_a_array

# Plot Customization
fig, axes = plt.subplots(nrows=1, ncols=2) # Create a figure with two subplots
fig.suptitle('Video HP and LP Vehicules Behaviour')
axes[0].plot(HP_data_array, label='HP Vehicles Bandwidth', color='#610B0B')
axes[0].plot(LP_data_array, label= 'LP Vehicles Bandwidth', color='#FFFF00')
axes[0].plot(total_video, label = 'Total Bandwidth', color='#0B610B')
axes[0].set_title('Conservative mode')
axes[0].set_xlabel('t (s)')
axes[0].set_ylabel('Bandwidth (Mbps)')
axes[0].grid(True)
axes[0].legend()
axes[1].plot(HP_data_a_array, label='HP Vehicles Bandwidth', color='#610B0B')
axes[1].plot(LP_data_a_array, label= 'LP Vehicles Bandwidth', color='#FFFF00')
axes[1].plot(total_video_aggressive, label = 'Total Bandwidth', color='#0B610B')
axes[1].set_title('Aggressive mode')
axes[1].set_xlabel('t (s)')
axes[1].set_ylabel('Bandwidth (Mbps)')
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()


