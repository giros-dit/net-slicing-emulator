import numpy as np
import matplotlib.pyplot as plt

# Quantum and Burst influence in Q size
def queue_size_max(T_theta, b_TNA, R_min, b_TNtheta, q_TNtheta, suma_q_s, Gamma_TNA, Gamma_theta):
    term1 = b_TNtheta * 8
    term2 = (b_TNA + suma_q_s - q_TNtheta)*8/R_min + (b_TNA + suma_q_s - q_TNtheta + T_theta)*8/R_min*Gamma_TNA/R_min
    term2 *= Gamma_theta

    total = np.floor((term1 + term2) / 8) / 1000
    return total

R_min = 100000000
Gamma_TNA = 1200000
q_s = np.array([
[1538, 1538, 1538],
[6152, 3076, 1538],
[15380, 4614, 1538],
[15380, 7690, 1538],
[30760, 7690, 3076],
[61520, 7690, 3076]
])
b_TNA = 30272

######################################################################################## TN Class A
T_theta = 322
T_max = 1538
B_max = 30272


b = range(T_theta, int(B_max*1.5), 3220)
q_tna = []

for value in b:
    q_tna.append(np.floor(Gamma_TNA * 1538 / R_min + value))

fig1, ax1 = plt.subplots()
fig1.suptitle('Burst Size influence on TN Class A Queue Size')
ax1.plot([valor / 1000 for valor in b],[valor / 1000 for valor in q_tna], color='#0040FF', marker='o', linestyle='-')
ax1.set_xlabel('Burst Size (kB)')
ax1.set_ylabel('Minimum Queue Size (kB)')
ax1.grid(True)

####################################################################################### TN Class B
q_TNtheta = [1538, 6152, 15380, 15380, 30760, 61520]
T_theta = 1538
B_max = 175000
Gamma_theta = 32000000

b = range(T_theta, int(B_max*1.5) ,4614)
q_tnb = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        q_tnb[i][j] = queue_size_max(T_theta, b_TNA, R_min, b[j], q_TNtheta[i], suma_q_s, Gamma_TNA, Gamma_theta)

fig2, ax2 = plt.subplots()
fig2.suptitle('Burst Size and Quantum influence on TN Class B Queue Size')
ax2.plot([valor / 1000 for valor in b], q_tnb[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax2.plot([valor / 1000 for valor in b], q_tnb[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax2.plot([valor / 1000 for valor in b], q_tnb[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], q_tnb[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax2.plot([valor / 1000 for valor in b], q_tnb[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax2.plot([valor / 1000 for valor in b], q_tnb[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax2.set_xlabel('Burst Size (kB)')
ax2.set_ylabel('Minimum Queue Size (kB)')
ax2.grid(True)
ax2.legend()


###################################################################################### TN Class C
q_TNtheta = [1538, 3076, 4614, 7690, 7690, 7690]
T_theta = 1088
B_max = 121500
Gamma_theta = 56800000 #Gamma_Telemetry + Gamma_eMBB

b = range(T_theta, int(B_max*1.5) ,2176)
q_tnc = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        q_tnc[i][j] = queue_size_max(T_theta, b_TNA, R_min, b[j], q_TNtheta[i], suma_q_s, Gamma_TNA, Gamma_theta)

fig3, ax3 = plt.subplots()
fig3.suptitle('Burst Size and Quantum influence on TN Class C Queue Size')
ax3.plot([valor / 1000 for valor in b], q_tnc[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax3.plot([valor / 1000 for valor in b], q_tnc[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax3.plot([valor / 1000 for valor in b], q_tnc[2], label='q_TNB=15380, q_TNC=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], q_tnc[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], q_tnc[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax3.plot([valor / 1000 for valor in b], q_tnc[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax3.set_xlabel('Burst Size (kB)')
ax3.set_ylabel('Minimum Queue Size (kB)')
ax3.grid(True)
ax3.legend()

###################################################################################### TN Class D
q_TNtheta = [1538, 1538, 1538, 1538, 3076, 3076]
T_theta = 130
B_max = 615200
Gamma_theta = 5000000

b = range(T_theta, int(B_max*1.5) ,2176)
q_tnd = np.zeros((len(q_TNtheta), len(b)))

for i in range(len(q_TNtheta)):
    for j in range(len(b)):
        suma_q_s = sum(q_s[i])
        q_tnd[i][j] = queue_size_max(T_theta, b_TNA, R_min, b[j], q_TNtheta[i], suma_q_s, Gamma_TNA, Gamma_theta)

fig3, ax3 = plt.subplots()
fig3.suptitle('Burst Size and Quantum influence on TN Class D Queue Size')
ax3.plot([valor / 1000 for valor in b], q_tnd[0], label='q_TNB=1538, q_TNC=1538, q_TND=1538', color='#0040FF', marker='o', linestyle='-')
ax3.plot([valor / 1000 for valor in b], q_tnd[1], label='q_TNB=6152, q_TNC=3076, q_TND=1538', color='#DF0101', marker='s', linestyle='-')
ax3.plot([valor / 1000 for valor in b], q_tnd[2], label='q_TNB=15380, q_tnd=4614, q_TND=1538', color='red', marker='D', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], q_tnd[3], label='q_TNB=15380, q_TNC=7690, q_TND=1538', color='orange', marker='*', linestyle='-.')
ax3.plot([valor / 1000 for valor in b], q_tnd[4], label='q_TNB=30760, q_TNC=7690, q_TND=3076', color='green', marker='^', linestyle='--')
ax3.plot([valor / 1000 for valor in b], q_tnd[5], label='q_TNB=61520, q_TNC=7690, q_TND=3076', color='purple', marker='p', linestyle='--')
ax3.set_xlabel('Burst Size (kB)')
ax3.set_ylabel('Minimum Queue Size (kB)')
ax3.grid(True)
ax3.legend()

plt.show()



##### Valores por defecto:
q_defaults = []
suma_q_s = sum(q_s[2])
b_TNA = 30272
q_defaults.append(np.floor(Gamma_TNA * 1538 / R_min + b_TNA))
q_defaults.append(queue_size_max(1538, b_TNA, R_min, 106096, 15380, suma_q_s, Gamma_TNA, 32000000))
q_defaults.append(queue_size_max(1088, b_TNA, R_min, 69210, 4614, suma_q_s, Gamma_TNA, 56800000))
q_defaults.append(queue_size_max(130, b_TNA, R_min, 129191, 1538, suma_q_s, Gamma_TNA, 5000000))


# Mostramos la tabla
print(q_defaults)

