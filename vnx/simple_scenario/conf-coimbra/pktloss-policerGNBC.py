import subprocess
import time
import sys
import re

# ---------------- ARGUMENTO ----------------
TAG = sys.argv[1]  # TN o NTN

# ---------------- CONFIG ----------------
duration = 100
delta = 1

# Clases
classes = ["1:20", "1:21", "1:30", "1:4", "1:31"]
num_queues = len(classes)

# aquí guardamos DROPPED acumulado (no rate)
pktloss = [[] for _ in range(num_queues)]

iterations = int(duration / delta)

# ---------------- GET DROPPED ----------------
def get_dropped(class_id):
    cmd = f"tc -s class show dev ifb0 | grep '{class_id}' -A 10"

    try:
        out = subprocess.check_output(cmd, shell=True, text=True)

        match = re.search(r"dropped\s+(\d+)", out)

        return int(match.group(1)) if match else 0

    except:
        return 0


# ---------------- LOOP ----------------
for _ in range(iterations):

    loop_start = time.time()

    for i, c in enumerate(classes):
        dropped = get_dropped(c)
        pktloss[i].append(dropped)

    loop_end = time.time()

    time.sleep(max(0, delta - (loop_end - loop_start)))


# ---------------- SAVE FILES ----------------
for i, lst in enumerate(pktloss):
    with open(f'/root/clase_{i + 1}_pktloss{TAG}', 'a') as file:
        for v in lst:
            file.write(f'{v}\n')
