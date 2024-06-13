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
b_URLLC = [322, 15136, 30272, 45408]

q_TNtheta = [1538, 6152, 15380, 15380, 30760, 61520] 
T_theta = 1538
T_theta_min = 1538
B_max = 228884

b = range(T_theta, int(B_max*1.5) ,4614)
delay_video = np.zeros((len(q_TNtheta)*len(b_URLLC), len(b)))

for k in range(len(b_URLLC)):
    for i in range(len(q_TNtheta)):
        suma_q_s = sum(q_s[i])
        for j in range(len(b)):
            delay_video[len(q_TNtheta)*k + i][j] = delay_max(t_proc, T_theta, R_max, b_URLLC[k], R_min, b[j], q_TNtheta[i], suma_q_s, T_theta_min, Gamma_URLLC)*1000

fig2, ax2 = plt.subplots()
fig2.suptitle('Burst Size and Quantum influence on Video delay')
ax2.plot([valor / 1000 for valor in b], delay_video[0], label='B_TNA=322, q_TNB=1538, q_TNC=1538, q_TND=1538', color='red', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[1], label='B_TNA=322, q_TNB=6152, q_TNC=3076, q_TND=1538', color='red', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[2], label='B_TNA=322, q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[3], label='B_TNA=322, q_TNB=15380, q_TNC=7690, q_TND=1538', color='red', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[4], label='B_TNA=322, q_TNB=30760, q_TNC=7690, q_TND=3076', color='red', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[5], label='B_TNA=322, q_TNB=61520, q_TNC=7690, q_TND=3076', color='red', marker='p', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[6], label='B_TNA=15136, q_TNB=1538, q_TNC=1538, q_TND=1538', color='orange', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[7], label='B_TNA=15136, q_TNB=6152, q_TNC=3076, q_TND=1538', color='orange', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[8], label='B_TNA=15136, q_TNB=15380, q_TNC=4614, q_TND=1538', color='orange', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[9], label='B_TNA=15136, q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[10], label='B_TNA=15136, q_TNB=30760, q_TNC=7690, q_TND=3076', color='orange', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[11], label='B_TNA=15136, q_TNB=61520, q_TNC=7690, q_TND=3076', color='orange', marker='p', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[12], label='B_TNA=30272, q_TNB=1538, q_TNC=1538, q_TND=1538', color='green', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[13], label='B_TNA=30272, q_TNB=6152, q_TNC=3076, q_TND=1538', color='green', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[14], label='B_TNA=30272, q_TNB=15380, q_TNC=4614, q_TND=1538', color='green', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[15], label='B_TNA=30272, q_TNB=15380, q_TNC=7690, q_TND=1538', color='green', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[16], label='B_TNA=30272, q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[17], label='B_TNA=30272, q_TNB=61520, q_TNC=7690, q_TND=3076', color='green', marker='p', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[18], label='B_TNA=45408, q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[19], label='B_TNA=45408, q_TNB=6152, q_TNC=3076, q_TND=1538', color='#0040FF', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], delay_video[20], label='B_TNA=45408, q_TNB=15380, q_TNC=4614, q_TND=1538', color='#0040FF', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[21], label='B_TNA=45408, q_TNB=15380, q_TNC=7690, q_TND=1538', color='#0040FF', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], delay_video[22], label='B_TNA=45408, q_TNB=30760, q_TNC=7690, q_TND=3076', color='#0040FF', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], delay_video[23], label='B_TNA=45408, q_TNB=61520, q_TNC=7690, q_TND=3076', color='#0040FF', marker='p', linestyle='--')
ax2.set_xlabel('Burst Size (kB)')
ax2.set_ylabel('Maximum Delay (ms)')
ax2.grid(True)
ax2.legend()


plt.show()

