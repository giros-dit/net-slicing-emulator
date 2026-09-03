from pathlib import Path
from scapy.all import rdpcap, IP, UDP
from scapy.plist import PacketList
from collections import defaultdict
import matplotlib.pyplot as plt
import struct
import tikzplotlib

BASE_DIR = Path(__file__).resolve().parent
CAPTURES_DIR = BASE_DIR / "capturas"
step = 0.01
step_lat = 0.005
step_pdv = 0.1
step_pkt_loss = 0.01

def flow_key_for_ip(ip, prefix):
    mapping = {
        "10.0.0.": {
            "10.0.0.2": "TNB",
            "10.0.0.3": "TNB",
            "10.0.0.4": "TNC",
            "10.0.0.5": "TNC",
            "10.0.0.6": "TNA",
            "10.0.0.7": "TNA",
        },
        "10.3.0.": {
            "10.3.0.2": "TNB",
            "10.3.0.3": "TNB",
            "10.3.0.4": "TNC",
            "10.3.0.5": "TNC",
            "10.3.0.6": "TNA",
            "10.3.0.7": "TNA",
            "10.3.0.8": "TNX",
        },
    }
    return mapping.get(prefix, {}).get(ip)

def build_sent_metrics(pkts, t0, prefix):
    bw_sent_by_flow = defaultdict(lambda: defaultdict(float))
    sent_dict = {}
    for pkt in pkts:
        if IP in pkt and UDP in pkt:
            src_ip = pkt[IP].src
            actual_prefix = "10.3.0." if src_ip.startswith("10.3.0.") else prefix
            flow_id = flow_key_for_ip(src_ip, actual_prefix)
            if flow_id is None:
                continue

            interval = int((pkt.time - t0) / step + 1)
            bw_sent_by_flow[flow_id][interval] += len(pkt) * 8

            seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
            key = (flow_id, pkt[IP].dst, seq)
            sent_dict[key] = pkt.time
    return bw_sent_by_flow, sent_dict

def build_received_metrics(pkts_received, sent_dict, t0, prefix):
    bw_by_flow = defaultdict(lambda: defaultdict(float))
    delay_by_flow = defaultdict(list)
    for pkt in pkts_received:
        if IP in pkt and UDP in pkt:
            src_ip = pkt[IP].src
            actual_prefix = "10.3.0." if src_ip.startswith("10.3.0.") else prefix
            flow_id = flow_key_for_ip(src_ip, actual_prefix)
            if flow_id is None:
                continue

            seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
            key = (flow_id, pkt[IP].dst, seq)
            recv_time = pkt.time
            if key in sent_dict:
                delay = recv_time - sent_dict[key]
                delay_by_flow[flow_id].append((recv_time, delay))
                interval = int((recv_time - t0) / step + 1)
                bw_by_flow[flow_id][interval] += len(pkt) * 8
    return bw_by_flow, delay_by_flow

def build_packet_loss_metrics(pkts_sent, pkts_received, t0):
    sent_dict = {}
    lost_by_flow_interval = defaultdict(lambda: defaultdict(int))
    for pkt in pkts_sent:
        if IP in pkt and UDP in pkt:
            seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
            key = (pkt[IP].src, pkt[IP].dst, seq)
            sent_dict[key] = pkt.time

    for pkt in pkts_received:
         if IP in pkt and UDP in pkt:
            seq = struct.unpack("!I", bytes(pkt[UDP].payload)[:4])[0]
            key = (pkt[IP].src, pkt[IP].dst, seq)
            if key in sent_dict:
                del sent_dict[key]  # Marked as received

    for (src_ip, dst_ip, seq), sent_time in sent_dict.items():
        interval = int((sent_time - t0) / step_pkt_loss + 1)
        lost_by_flow_interval[src_ip][interval] += 1

    intervals = list(range(1, int((max(pkt.time for pkt in pkts_sent) - t0) / step_pkt_loss) + 2))
    for src_ip in lost_by_flow_interval:
        for interval in intervals:
            if interval not in lost_by_flow_interval[src_ip]:
                lost_by_flow_interval[src_ip][interval] = 0

    return lost_by_flow_interval

def plot_packet_loss(path_name, lost_by_src_ip, save_path):
    plt.figure(figsize=(10, 7))
    loss_colors = {}

    for src_ip, intervals in sorted(lost_by_src_ip.items()):
        if not intervals:
            continue

        x = sorted(intervals)
        y = [intervals[interval] for interval in x]
        color = plt.rcParams["axes.prop_cycle"].by_key()["color"][len(loss_colors) % 10]
        loss_colors[src_ip] = color
        plt.plot(
            [interval * step_pkt_loss * 1000 for interval in x],
            y,
            label=src_ip,
            color=color,
            marker="o",
            markersize=2,
            linewidth=1,
        )
    plt.xlabel("t (ms)")
    plt.ylabel("Paquetes perdidos por intervalo")
    plt.title(f"Paquetes perdidos por IP origen - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.legend()
    #tikzplotlib.save(str(save_path), axis_width="\\textwidth", axis_height="0.7\\textwidth")

def plot_bw_generated(path_name, flows, bw_sent_by_flow, save_path):
    plt.figure(figsize=(10, 7))
    for flow_id in flows:
        intervals = bw_sent_by_flow.get(flow_id, {})
        if not intervals:
            continue
        x = sorted(intervals)
        y = [bw_sent_by_flow[flow_id][i] / step / 1e6 for i in x]
        style = flow_styles.get(flow_id, {})
        plt.plot(
            [i * step * 1000 for i in x],
            y,
            label=style.get("label", flow_id),
            color=style.get("color"),
            marker=style.get("marker"),
            linestyle=style.get("linestyle"),
            markersize=style.get("markersize"),
            linewidth=style.get("linewidth"),
        )
    plt.xlabel("t (ms)")
    plt.ylabel("BW generado (Mbps)")
    plt.title(f"BW generado - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.tight_layout()
    tikzplotlib.save(str(save_path), axis_width="\\textwidth", axis_height="0.7\\textwidth")

def plot_bw_received(path_name, flows, bw_by_flow, save_path):
    plt.figure(figsize=(10, 7))
    for flow_id in flows:
        intervals = bw_by_flow.get(flow_id, {})
        if not intervals:
            continue
        x = sorted(intervals)
        y = [bw_by_flow[flow_id][i] / step / 1e6 for i in x]
        style = flow_styles.get(flow_id, {})
        plt.plot(
            [i * step * 1000 for i in x],
            y,
            label=style.get("label", flow_id),
            color=style.get("color"),
            marker=style.get("marker"),
            linestyle=style.get("linestyle"),
            markersize=style.get("markersize"),
            linewidth=style.get("linewidth"),
        )
    plt.xlabel("t (ms)")
    plt.ylabel("BW recibido (Mbps)")
    plt.title(f"BW recibido - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.tight_layout()
    tikzplotlib.save(str(save_path), axis_width="\\textwidth", axis_height="0.7\\textwidth")

def plot_delay(path_name, flows, delay_by_flow, t0, save_path):
    plt.figure(figsize=(10, 7))
    for flow_id in flows:
        groups = delay_by_flow.get(flow_id, [])
        if not groups:
            continue
        interval_map = defaultdict(list)
        for recv_time, delay in groups:
            interval = int((recv_time - t0) / step_lat + 1)
            interval_map[interval].append(delay)

        x = []
        y = []
        for interval in sorted(interval_map):
            x.append(interval * step_lat * 1000)
            y.append(max(interval_map[interval]) * 1000)
        style = flow_styles.get(flow_id, {})
        plt.plot(
            x,
            y,
            label=style.get("label", flow_id),
            color=style.get("color"),
            marker=style.get("marker"),
            linestyle=style.get("linestyle"),
            markersize=style.get("markersize"),
            linewidth=style.get("linewidth"),
        )
    plt.xlabel("t (ms)")
    plt.ylabel("Latency (ms)")
    plt.title(f"Delay - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.ylim(0, 50)
    plt.tight_layout()
    tikzplotlib.save(str(save_path), axis_width="\\textwidth", axis_height="0.7\\textwidth")

path1_flows = ["TNA", "TNB", "TNC", "TND", "TNX"]
path2_flows = ["TNA", "TNB", "TNC", "TND"]

flow_styles = {
    "TNA": dict(label="TNA", color="#0040FF", marker="o", linestyle="-", markersize=2, linewidth=1),
    "TNB": dict(label="TNB", color="#006600", marker="*", linestyle="-", markersize=2, linewidth=1),
    "TNC": dict(label="TNC", color="orange", marker="^", linestyle="-", markersize=2, linewidth=1),
    "TND": dict(label="TND", color="#610B0B", marker="p", linestyle="-", markersize=2, linewidth=1),
    "TNX": dict(label="TNX", color="#7B1FA2", marker="s", linestyle="-", markersize=2, linewidth=1),
}

def plot_pdv_consecutive(path_name, flows, delay_by_flow, t0, save_path):
    """
    PDV calculado como la diferencia absoluta de delay entre
    paquetes consecutivos. Para cada step se representa el
    máximo valor obtenido.
    """
    plt.figure(figsize=(10, 7))

    for flow_id in flows:
        all_pdv = []
        groups = delay_by_flow.get(flow_id, [])
        if len(groups) < 2:
            continue

        # Ordenar por instante de recepción
        groups = sorted(groups, key=lambda x: x[0])

        interval_map = defaultdict(list)

        previous_delay = None

        for recv_time, delay in groups:
            if previous_delay is not None:
                pdv = abs(delay - previous_delay)
                all_pdv.append(pdv)
                interval = int((recv_time - t0) / step_pdv + 1)
                interval_map[interval].append(pdv)
            previous_delay = delay

        mean_pdv = sum(all_pdv) / len(all_pdv)
        print(
            f"{path_name} - {flow_id}: "
            f"PDV medio entre paquetes consecutivos = "
            f"{mean_pdv * 1000:.3f} ms"
        )

        x = []
        y = []

        for interval in sorted(interval_map):
            x.append(interval * step_pdv * 1000)
            y.append(max(interval_map[interval]) * 1000)

        style = flow_styles.get(flow_id, {})

        plt.plot(
            x,
            y,
            label=style.get("label", flow_id),
            color=style.get("color"),
            marker=style.get("marker"),
            linestyle=style.get("linestyle"),
            markersize=style.get("markersize"),
            linewidth=style.get("linewidth"),
        )

    plt.xlabel("t (ms)")
    plt.ylabel("PDV (ms)")
    plt.title(f"PDV entre paquetes consecutivos - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.ylim(bottom=0)
    plt.tight_layout()
    #tikzplotlib.save(str(save_path), axis_width="\\textwidth", axis_height="0.7\\textwidth")


def plot_pdv_min_delay(path_name, flows, delay_by_flow, t0, save_path):
    """
    PDV calculado como delay - delay_min_global.
    Para cada step se representa el máximo valor obtenido.
    """
    plt.figure(figsize=(10, 7))

    for flow_id in flows:
        groups = delay_by_flow.get(flow_id, [])
        if not groups:
            continue

        # Delay mínimo del experimento para este flujo
        min_delay = min(abs(delay) for _, delay in groups)

        interval_map = defaultdict(list)

        all_pdv = []

        for recv_time, delay in groups:
            pdv = delay - min_delay
            all_pdv.append(pdv)

            interval = int((recv_time - t0) / step_pdv + 1)
            interval_map[interval].append(pdv)

        mean_pdv = sum(all_pdv) / len(all_pdv) if all_pdv else 0.0

        print(
            f"{path_name} - {flow_id}: "
            f"PDV medio respecto al valor mínimo = "
            f"{mean_pdv * 1000:.3f} ms"
        )

        x = []
        y = []

        for interval in sorted(interval_map):
            x.append(interval * step_pdv * 1000)
            y.append(max(interval_map[interval]) * 1000)

        style = flow_styles.get(flow_id, {})

        plt.plot(
            x,
            y,
            label=style.get("label", flow_id),
            color=style.get("color"),
            marker=style.get("marker"),
            linestyle=style.get("linestyle"),
            markersize=style.get("markersize"),
            linewidth=style.get("linewidth"),
        )

    plt.xlabel("t (ms)")
    plt.ylabel("PDV (ms)")
    plt.title(f"PDV respecto al delay mínimo - {path_name}")
    plt.grid(True)
    plt.xlim(0, 5000)
    plt.ylim(bottom=0)
    plt.tight_layout()

for exp_name in ["exp1", "exp2"]:
    pkts_sent_path1 = rdpcap(str(CAPTURES_DIR / f"{exp_name}_PE1-e1.pcap"))
    pkts_sent_path2 = rdpcap(str(CAPTURES_DIR / f"{exp_name}_PE3-e1.pcap"))
    pkts_received_path1 = rdpcap(str(CAPTURES_DIR / f"{exp_name}_PE2-e2.pcap"))
    pkts_received_path2 = rdpcap(str(CAPTURES_DIR / f"{exp_name}_PE4-e2.pcap"))

    path1_extra_packets = [pkt for pkt in pkts_sent_path2
                           if IP in pkt and pkt[IP].src == "10.3.0.8"]
    pkts_sent_path1 = PacketList(
        res=list(pkts_sent_path1) + path1_extra_packets,
        name=pkts_sent_path1.listname,
    )
    pkts_sent_path2 = PacketList(
        res=[pkt for pkt in pkts_sent_path2
             if not (IP in pkt and pkt[IP].src == "10.3.0.8")],
        name=pkts_sent_path2.listname,
    )

    path1_t0 = min(pkt.time for pkt in pkts_sent_path1 if IP in pkt)
    bw_sent_path1, sent_dict_path1 = build_sent_metrics(pkts_sent_path1, path1_t0, "10.0.0.")
    bw_received_path1, delays_path1 = build_received_metrics(pkts_received_path1, sent_dict_path1.copy(), path1_t0, "10.0.0.")
    packet_loss_path1 = build_packet_loss_metrics(pkts_sent_path1, pkts_received_path1, path1_t0)
    plot_bw_generated(f"Path 1 - {exp_name}", path1_flows, bw_sent_path1, BASE_DIR / f"results/bw_gen_path1_{exp_name}.tex")
    plot_bw_received(f"Path 1 - {exp_name}", path1_flows, bw_received_path1, BASE_DIR / f"results/bw_recv_path1_{exp_name}.tex")
    plot_delay(f"Path 1 - {exp_name}", path1_flows, delays_path1, path1_t0, BASE_DIR / f"results/latency_path1_{exp_name}.tex")
    plot_packet_loss(f"Path 1 - {exp_name}", packet_loss_path1, BASE_DIR / f"results/packet_loss_path1_{exp_name}.tex")

    path2_t0 = min(pkt.time for pkt in pkts_sent_path2 if IP in pkt)
    bw_sent_path2, sent_dict_path2 = build_sent_metrics(pkts_sent_path2, path2_t0, "10.3.0.")
    bw_received_path2, delays_path2 = build_received_metrics(pkts_received_path2, sent_dict_path2.copy(), path2_t0, "10.3.0.")
    packet_loss_path2 = build_packet_loss_metrics(pkts_sent_path2, pkts_received_path2, path2_t0)
    plot_bw_generated(f"Path 2 - {exp_name}", path2_flows, bw_sent_path2, BASE_DIR / f"results/bw_gen_path2_{exp_name}.tex")
    plot_bw_received(f"Path 2 - {exp_name}", path2_flows, bw_received_path2, BASE_DIR / f"results/bw_recv_path2_{exp_name}.tex")
    plot_delay(f"Path 2 - {exp_name}", path2_flows, delays_path2, path2_t0, BASE_DIR / f"results/latency_path2_{exp_name}.tex")
    plot_packet_loss(f"Path 2 - {exp_name}", packet_loss_path2, BASE_DIR / f"results/packet_loss_path2_{exp_name}.tex")

plt.show()