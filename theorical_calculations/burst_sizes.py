import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def burst_max(b_TNtheta, D_theta_max, t_proc, T_theta, R_max, b_URLLC, R_min, q_TNtheta, suma_q_s, Gamma_URLLC):
    term1 = 3 * t_proc
    term2 = 2 * (T_theta * 8 / R_max)
    term3 = b_URLLC * 8 / R_min
    ceil_term = np.ceil(b_TNtheta / q_TNtheta)
    term4 = (b_URLLC + ceil_term * (suma_q_s - q_TNtheta) + b_TNtheta - T_theta_min) * 8 / R_min
    term4 *= (Gamma_URLLC / R_min)
    term5 = ceil_term * (suma_q_s - q_TNtheta) * 8 / R_min + b_TNtheta * 8 / R_min

    total = D_theta_max - term1 - term2 - term3 - term4 - term5
    return total

# Definir las variables comunes
t_proc = 0.00015
R_max = 1000000000
R_min = 100000000
Gamma_URLLC = 1200000

urllc_results = []

b_URLLC_without_floor = (0.003 - 3 * t_proc - 2 * 322 * 8 / R_max - 1538 * 8 / R_min) * R_min / 8
b_URLLC = np.floor(b_URLLC_without_floor)
b_URLLC_1ms=(0.001 - 3 * t_proc - 2 * 322 * 8 / R_max - 1538 * 8 / R_min) * R_min / 8
b_URLLC_2ms=(0.002 - 3 * t_proc - 2 * 322 * 8 / R_max - 1538 * 8 / R_min) * R_min / 8
b_URLLC_4ms=(0.004 - 3 * t_proc - 2 * 322 * 8 / R_max - 1538 * 8 / R_min) * R_min / 8
b_URLLC_5ms=(0.005 - 3 * t_proc - 2 * 322 * 8 / R_max - 1538 * 8 / R_min) * R_min / 8
urllc_results.append(np.floor(b_URLLC_1ms)/1000)
urllc_results.append(np.floor(b_URLLC_2ms)/1000)
urllc_results.append(b_URLLC/1000)
urllc_results.append(np.floor(b_URLLC_4ms)/1000)
urllc_results.append(np.floor(b_URLLC_5ms)/1000)

print(b_URLLC/1000)

######################################################################################## TN CLASS B
q_TNtheta = [1538, 6152, 15380, 15380, 30760, 61520]
q_s = np.array([
[1538, 1538, 1538],
[6152, 3076, 1538],
[15380, 4614, 1538],
[15380, 7690, 1538],
[30760, 7690, 3076],
[61520, 7690, 3076]
])
T_theta = 1538
T_theta_min = 1538
D_theta_max = [0.005, 0.01, 0.015, 0.02]
video_results = np.zeros((len(q_TNtheta), len(D_theta_max)))

for i in range(len(q_TNtheta)):
    for j in range(len(D_theta_max)):
        suma_q_s = sum(q_s[i])
        b_TNtheta_initial_guess = 1
        solution = fsolve(burst_max, b_TNtheta_initial_guess, args=(D_theta_max[j], t_proc, T_theta, R_max, b_URLLC, R_min, q_TNtheta[i], suma_q_s, Gamma_URLLC), maxfev=500000)
        video_results[i][j] = np.floor(solution[0])/1000

columns = [f"D_theta_max_{D}" for D in D_theta_max]
index = [f"q_TNtheta_{i}" for i in q_TNtheta]

df = pd.DataFrame(video_results, index=index, columns=columns)

# Mostramos la tabla
print(df)

######################################################################################## TN CLASS C
q_TNtheta = [1538, 3076, 4614, 7690, 7690, 7690]
T_theta = 1088
T_theta_min = 130
D_theta_max_tnc = [0.02, 0.03, 0.04, 0.05]
telemetry_results = np.zeros((len(q_TNtheta), len(D_theta_max_tnc)))

for i in range(len(q_TNtheta)):
    for j in range(len(D_theta_max_tnc)):
        suma_q_s = sum(q_s[i])
        b_TNtheta_initial_guess = 1
        solution = fsolve(burst_max, b_TNtheta_initial_guess, args=(D_theta_max_tnc[j], t_proc, T_theta, R_max, b_URLLC, R_min, q_TNtheta[i], suma_q_s, Gamma_URLLC), maxfev=500000)
        telemetry_results[i][j] = np.floor(solution[0])/1000

T_theta = 130
embb_results = np.zeros((len(q_TNtheta), len(D_theta_max_tnc)))

for i in range(len(q_TNtheta)):
    for j in range(len(D_theta_max_tnc)):
        suma_q_s = sum(q_s[i])
        b_TNtheta_initial_guess = 1
        solution = fsolve(burst_max, b_TNtheta_initial_guess, args=(D_theta_max_tnc[j], t_proc, T_theta, R_max, b_URLLC, R_min, q_TNtheta[i], suma_q_s, Gamma_URLLC), maxfev=500000)
        embb_results[i][j] = np.floor(solution[0])/1000

columns = [f"D_theta_max{D}" for D in D_theta_max_tnc]
index = [f"q_TNtheta_{i}" for i in q_TNtheta]

df = pd.DataFrame(telemetry_results, index=index, columns=columns)

# Mostramos la tabla
print(df)

columns = [f"D_theta_max{D}" for D in D_theta_max_tnc]
index = [f"q_TNtheta_{i}" for i in q_TNtheta]

df = pd.DataFrame(embb_results, index=index, columns=columns)

# Mostramos la tabla
print(df)


######################################################################################## TN CLASS D
q_TNtheta = [1538, 1538, 1538, 1538, 3076, 3076]
T_theta = 1088
T_theta_min = 130
D_theta_max_tnd = [0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
be_results = np.zeros((len(q_TNtheta), len(D_theta_max_tnd)))

for i in range(len(q_TNtheta)):
    for j in range(len(D_theta_max_tnd)):
        suma_q_s = sum(q_s[i])
        b_TNtheta_initial_guess = 1
        solution = fsolve(burst_max, b_TNtheta_initial_guess, args=(D_theta_max_tnd[j], t_proc, T_theta, R_max, b_URLLC, R_min, q_TNtheta[i], suma_q_s, Gamma_URLLC), maxfev=500000)
        be_results[i][j] = np.floor(solution[0])/1000

columns = [f"D_theta_max{D}" for D in D_theta_max_tnd]
index = [f"q_TNtheta_{i}" for i in q_TNtheta]

df = pd.DataFrame(be_results, index=index, columns=columns)

# Mostramos la tabla
print(df)


# Plots
fig1, ax1 = plt.subplots()
fig1.suptitle('URLLC Traffic Maximum Theorical Burst Size')
ax1.plot([1, 2, 3, 4, 5], urllc_results, label='URLLC', color='#0040FF', marker='*', linestyle='-')
ax1.set_xlabel('Maximum Delay (ms)')
ax1.set_ylabel('Burst Size (kB)')
ax1.grid(True)

fig2, ax2 = plt.subplots()
fig2.suptitle('Video Traffic Maximum Theorical Burst Size')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax2.plot([valor * 1000 for valor in D_theta_max], video_results[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax2.set_xlabel('Maximum Delay (ms)')
ax2.set_ylabel('Burst Size (kB)')
ax2.grid(True)
ax2.legend()

fig3, ax3 = plt.subplots()
fig3.suptitle('Telemetry Traffic Maximum Theorical Burst Size')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax3.plot([valor * 1000 for valor in D_theta_max_tnc], telemetry_results[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax3.set_xlabel('Maximum Delay (ms)')
ax3.set_ylabel('Burst Size (kB)')
ax3.grid(True)
ax3.legend()

fig4, ax4 = plt.subplots()
fig4.suptitle('eMBB Traffic Maximum Theorical Burst Size')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax4.plot([valor * 1000 for valor in D_theta_max_tnc], embb_results[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax4.set_xlabel('Maximum Delay (ms)')
ax4.set_ylabel('Burst Size (kB)')
ax4.grid(True)
ax4.legend()

fig5, ax5 = plt.subplots()
fig5.suptitle('BE Traffic Maximum Theorical Burst Size')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax5.plot([valor * 1000 for valor in D_theta_max_tnd], be_results[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax5.set_xlabel('Maximum Delay (ms)')
ax5.set_ylabel('Burst Size (kB)')
ax5.grid(True)
ax5.legend()

# Burst sharing between Telemetry and eMBB
b_telemetry = range(1088, int(telemetry_results[2,1]*1000)-1088, 1088)
b_embb = []

for value in b_telemetry:
    b_embb.append(float(embb_results[2,1])*1000-value)

fig6, ax6 = plt.subplots()
fig6.suptitle('Burst Size sharing in Transport Network Class C')
ax6.plot(b_telemetry, b_embb, color='red', marker='o', linestyle='-')
ax6.set_xlabel('Telemetry Burst Size (kB)')
ax6.set_ylabel('eMBB Burst Size (kB)')
ax6.grid(True)

plt.show()
