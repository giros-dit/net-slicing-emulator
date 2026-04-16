import matplotlib.pyplot as plt
import numpy as np

SKIP = 5
N_POINTS = 100

HANDOVER_T = 40
TOTAL_T = 80
fsizex = 5
fsizey = 4

# ---------------- LOADER ----------------
def load_bw(path, skip=SKIP, n_points=N_POINTS):
    values = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            values.append(1538 / 1472 * float(line.replace(",", ".")))

    data = np.array(values, dtype=float)

    if len(data) <= skip:
        return np.array([], dtype=float)

    data = data[skip:]
    return data[:n_points]


def make_time(n, start, end):
    if n == 0:
        return np.array([])
    return np.linspace(start, end, n, endpoint=False)


def plot_segment(ax, x, y, **kwargs):
    if len(y) == 0:
        return
    ax.plot(x, y, **kwargs)


# ---------------- DATA (ONLY TN) ----------------
tn_video = load_bw("filesTN/bandwidth_metricsSTN1")
tn_telemetry = load_bw("filesTN/bandwidth_metricsSTN2")
tn_embb = load_bw("filesTN/bandwidth_metricsSTN3")
tn_be = load_bw("filesTN/bandwidth_metricsSTN5")
tn_urllc = load_bw("filesTN/bandwidth_metricsSTN4")


# ---------------- TIME ----------------
x_tn = make_time(N_POINTS, 0, HANDOVER_T)
x_after = make_time(N_POINTS, HANDOVER_T, TOTAL_T)


# ---------------- COLORS ----------------
colors = {
    "video": "#610B0B",
    "telemetry": "#BEF781",
    "embb": "orange",
    "be": "#F5A9BC",
    "urllc": "#0040FF",
}

fig, ax = plt.subplots(figsize=(fsizex, fsizey))


# ---------------- BEFORE HANDOVER ----------------
plot_segment(ax, x_tn, tn_video, label="RD: Video", color=colors["video"], marker="*", linestyle="-.", markersize=3)
plot_segment(ax, x_tn, tn_telemetry, label="RD: Telemetry", color=colors["telemetry"], marker="D", linestyle="-.", markersize=3)
plot_segment(ax, x_tn, tn_embb, label="eMBB: VC", color=colors["embb"], marker="^", linestyle="--", markersize=3)
plot_segment(ax, x_tn, tn_be, label="eMBB: BE", color=colors["be"], marker="p", linestyle="--", markersize=3)
plot_segment(ax, x_tn, tn_urllc, label="URLLC", color=colors["urllc"], marker="o", linestyle="-", markersize=3)


# ---------------- AFTER HANDOVER (REUSING TN DATA) ----------------
plot_segment(ax, x_after, tn_video, color=colors["video"], marker="*", linestyle="--", markersize=3, label="_nolegend_")
plot_segment(ax, x_after, tn_telemetry, color=colors["telemetry"], marker="D", linestyle="--", markersize=3, label="_nolegend_")
plot_segment(ax, x_after, tn_embb, color=colors["embb"], marker="^", linestyle="--", markersize=3, label="_nolegend_")
plot_segment(ax, x_after, tn_be, color=colors["be"], marker="p", linestyle="--", markersize=3, label="_nolegend_")
plot_segment(ax, x_after, tn_urllc, color=colors["urllc"], marker="o", linestyle="--", markersize=3, label="_nolegend_")


# ---------------- HANDOVER LINE ----------------
ax.axvline(HANDOVER_T, color="black", linestyle="--", linewidth=1.4)


# ---------------- SHADED REGIONS ----------------
ax.axvspan(0, HANDOVER_T, color="gray", alpha=0.08)
ax.axvspan(HANDOVER_T, TOTAL_T, color="blue", alpha=0.06)


# ---------------- TEXT LABELS ----------------
ymax = ax.get_ylim()[1]

ax.text(
    HANDOVER_T - 2,
    ymax * 0.92,
    "QoS before HO \n w/ RD slice",
    ha="right",
    va="top",
    fontsize=11,
    color="black"
)

ax.text(
    HANDOVER_T + 2,
    ymax * 0.92,
    "QoS after HO \n w/o RD slice",
    ha="left",
    va="top",
    fontsize=11,
    color="black"
)


# ---------------- STYLE ----------------
ax.set_xlabel("t (s)", fontsize=14)
ax.set_ylabel("BW (Mbps)", fontsize=14)

ax.tick_params(axis="both", labelsize=12)

ax.set_xlim(0, TOTAL_T)
ax.grid(True, alpha=0.3)

ax.legend(fontsize=11)

fig.tight_layout()



plt.savefig("figuresA/bw_handover_combined.png", dpi=300, bbox_inches="tight")


import numpy as np
import matplotlib.pyplot as plt

# ---------------- LOAD ----------------
def load_file(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            try:
                data.append(float(line.strip()))
            except:
                data.append(0.0)
    return np.array(data)


# ---------------- TN LOAD ----------------
tn_video = load_file('filesTN/clase_1_pktlossTN')
tn_telemetry = load_file('filesTN/clase_2_pktlossTN')
tn_vc = load_file('filesTN/clase_3_pktlossTN')
tn_urllc = load_file('filesTN/clase_4_pktlossTN')
tn_be = load_file('filesTN/clase_5_pktlossTN')


# ---------------- HANDOVER ----------------
HO = 40
TOTAL_T = 100


# ---------------- TIME AXIS (CONTINUOUS) ----------------
x_tn = np.arange(len(tn_video))

# second segment is CONTINUATION, not restart
x_after = np.arange(HO, len(tn_video))


# ---------------- STYLE ----------------
colors = {
    "video": "#4A0E0E",
    "telemetry": "#4F6B2A",
    "vc": "#B35C00",
    "urllc": "#0B3D91",
    "be": "#7A1F5C"
}

size = 3
fig, ax = plt.subplots(figsize=(fsizex, fsizey))


# =======================
# BEFORE HANDOVER (TN)
# =======================
ax.plot(x_tn[:HO], tn_video[:HO],
        color=colors["video"], linestyle='-', marker='*', markersize=size,
        label='RD Video')

ax.plot(x_tn[:HO], tn_telemetry[:HO],
        color=colors["telemetry"], linestyle='-', marker='D', markersize=size,
        label='RD Telemetry')

ax.plot(x_tn[:HO], tn_vc[:HO],
        color=colors["vc"], linestyle='-',
        label='eMBB VC')

ax.plot(x_tn[:HO], tn_be[:HO],
        color=colors["be"], linestyle='-',
        label='eMBB BE')

ax.plot(x_tn[:HO], tn_urllc[:HO],
        color=colors["urllc"], linestyle='-',
        label='URLLC')


# =======================
# AFTER HANDOVER (CONTINUATION OF TN)
# =======================
ax.plot(x_after, tn_video[HO:],
        color=colors["video"], linestyle='--', marker='*', markersize=size,
        label="_nolegend_")

ax.plot(x_after, tn_telemetry[HO:],
        color=colors["telemetry"], linestyle='--', marker='D', markersize=size,
        label="_nolegend_")

ax.plot(x_after, tn_vc[HO:],
        color=colors["vc"], linestyle='--',
        label="_nolegend_")

ax.plot(x_after, tn_be[HO:],
        color=colors["be"], linestyle='--',
        label="_nolegend_")

ax.plot(x_after, tn_urllc[HO:],
        color=colors["urllc"], linestyle='--',
        label="_nolegend_")


# ---------------- HANDOVER LINE ----------------
ax.axvline(HO, color="black", linestyle="--", linewidth=1.4)


# ---------------- SHADED REGIONS ----------------
ax.axvspan(0, HO, color="gray", alpha=0.08)
ax.axvspan(HO, TOTAL_T, color="blue", alpha=0.06)


# ---------------- TEXT LABELS ----------------
ymax = ax.get_ylim()[1]

ax.text(
    HO - 2,
    ymax * 0.92,
    "QoS before HO \n w/ RD slice ",
    ha="right",
    va="top",
    fontsize=11,
    color="black"
)

ax.text(
    HO + 2,
    ymax * 0.92,
    "QoS after HO \n w/o RD slice",
    ha="left",
    va="top",
    fontsize=11,
    color="black"
)


# ---------------- AXES ----------------
ax.set_xlabel("Time (s)", fontsize=14)
ax.set_ylabel("Packet Loss", fontsize=14)

ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.tick_params(labelsize=12)

ax.set_xlim(0, TOTAL_T)

plt.tight_layout()
plt.savefig("figuresA/plot_pktloss_TN_only.png", dpi=300)
