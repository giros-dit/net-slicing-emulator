import numpy as np
import matplotlib.pyplot as plt

# Quantum and Burst influence in delay
def delay_max(t_proc, T_theta, R_max, b_URLLC, R_min, b_TNtheta, q_TNtheta, suma_q_s, T_theta_min, Gamma_URLLC):
    term1 = 3 * t_proc
    term2 = 2 * (T_theta * 8 / R_max)
    term3 = b_URLLC * 8 / R_min
    ceil_term = np.ceil(b_TNtheta / q_TNtheta)
    term4 = (b_URLLC + ceil_term * (suma_q_s - q_TNtheta) + b_TNtheta - T_theta_min) * 8/ R_min
    term4 *= (Gamma_URLLC / R_min)
    term5 = ceil_term * (suma_q_s - q_TNtheta) * 8 / R_min + b_TNtheta * 8 / R_min

    total = term1 + term2 + term3 + term4 + term5
    return total

t_proc = 0.00015
R_max = 1000000000
R_min = 100000000
Gamma_URLLC = 1200000
q_s = np.array([
[1538, 1538, 1538],
[6152, 3076, 1538],
[15380, 4614, 1538],
[15380, 7690, 1538],
[30760, 7690, 3076],
[61520, 7690, 3076]
])
b_URLLC = 30272

############################################################################################# TN Class A
T_theta = 322
B_max = 30272

b = range(T_theta, int(B_max*1.5), 3220)
delay_urllc = []

for value in b:
    delay_urllc.append(3 * t_proc + 2 * 322 * 8 / R_max + 1538 * 8 / R_min + value * 8 / R_min)

fig1, ax1 = plt.subplots()
fig1.suptitle('Burst Size influence on URLLC delay')
ax1.plot([valor / 1000 for valor in b],[valor * 1000 for valor in delay_urllc], color='#0040FF', marker='o', linestyle='-')
ax1.set_xlabel('Burst Size (kB)')
ax1.set_ylabel('Maximum Delay (ms)')
ax1.grid(True)

############################################################################################# TN Class B

q_TNtheta = [1538, 6152, 15380, 15380, 30760, 61520] 
T_theta = 1538
T_theta_min = 1538
B_max = 228884

b = range(T_theta, int(B_max*1.5) ,4614)
delay_video = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        delay_video[i][j] = delay_max(t_proc, T_theta, R_max, b_URLLC, R_min, b[j], q_TNtheta[i], suma_q_s, T_theta_min, Gamma_URLLC)*1000

fig2, ax2 = plt.subplots()
fig2.suptitle('Burst Size and Quantum influence on Video delay')
ax2.plot([valor / 1000 for valor in b], delay_video[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax2.set_xlabel('Burst Size (kB)')
ax2.set_ylabel('Maximum Delay (ms)')
ax2.grid(True)
ax2.legend()

########################################################################################### TN Class C

q_TNtheta = [1538, 3076, 4614, 7690, 7690, 7690]
T_theta = 1088
T_theta_min = 130 
B_max = 121500

b = range(T_theta, int(B_max*1.5) ,2176)
delay_telemetry = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        delay_telemetry[i][j] = delay_max(t_proc, T_theta, R_max, b_URLLC, R_min, b[j], q_TNtheta[i], suma_q_s, T_theta_min, Gamma_URLLC)*1000

fig3, ax3 = plt.subplots()
fig3.suptitle('Burst Size and Quantum influence on Telemetry delay')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax3.plot([valor / 1000 for valor in b], delay_telemetry[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax3.set_xlabel('Burst Size (kB)')
ax3.set_ylabel('Maximum Delay (ms)')
ax3.grid(True)
ax3.legend()

########################################################################################### TN Class D

q_TNtheta = [1538, 1538, 1538, 1538, 3076, 3076]
T_theta = 130
T_theta_min = 130
B_max = 615200

b = range(T_theta, int(B_max*3/2), 6500)
delay_be = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        delay_be[i][j] = delay_max(t_proc, T_theta, R_max, b_URLLC, R_min, b[j], q_TNtheta[i], suma_q_s, T_theta_min, Gamma_URLLC)*1000

fig4, ax4 = plt.subplots()
fig4.suptitle('Burst Size and Quantum influence on BE delay')
ax4.plot([valor / 1000 for valor in b], delay_be[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax4.plot([valor / 1000 for valor in b], delay_be[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax4.plot([valor / 1000 for valor in b], delay_be[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax4.plot([valor / 1000 for valor in b], delay_be[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax4.plot([valor / 1000 for valor in b], delay_be[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax4.plot([valor / 1000 for valor in b], delay_be[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax4.set_xlabel('Burst Size (kB)')
ax4.set_ylabel('Maximum Delay (ms)')
ax4.grid(True)
ax4.legend()

plt.show()
