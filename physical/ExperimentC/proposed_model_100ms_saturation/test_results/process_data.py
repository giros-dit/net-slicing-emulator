import os
import numpy as np

def sum_rows(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
        for line1, line2 in zip(f1, f2):
            value1 = float(line1.strip().replace(',','.'))
            value2 = float(line2.strip().replace(',','.'))
            result = value1 + value2
            out.write(str(result) + '\n')

def max_rows (file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
        for line1, line2 in zip(f1, f2):
            if str(line1).strip() == '-':
                value1 = float(0)
            else:
                value1 = float(line1.strip())
            if str(line2).strip() == '-':
                value2 = float(0)
            else:
                value2 = float(line2.strip())
            result = max(value1, value2)
            out.write(str(result) + '\n')

def latency_avg(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as out:
        for line1, line2 in zip(f1, f2):
            packets1, latency1 = line1.split()
            packets2, latency2 = line2.split()
            if packets1 == 0 or str(latency1).strip() == '-':
                avg_latency = float(0)
            elif packets2 == 0 or str(latency2).strip() == '-':
                avg_latency = float(latency1)
            else:
                avg_latency = (float(latency1) * float(packets1) + float(latency2) * float(packets2)) / (float(packets1) + float(packets2))
            out.write(str(avg_latency) + '\n')

latency_files = [f"files/latency_metrics{i}" for i in range(1, 6)]
latency_burst_files = [f"files/latency_metrics{i}_burst_with_zeros" for i in range(1, 6)]
latency_avg_output_files = [f"files/lat_metrics{i}" for i in range(1, 6)]

bandwidth_files = [f"files/bandwidth_metrics{i}" for i in range(1, 6)]
bandwidth_burst_files = [f"files/bandwidth_metrics{i}_burst_with_zeros" for i in range(1, 6)]
bandwidth_output_files = [f"files/bw_metrics{i}" for i in range(1, 6)]

latency_max_files = [f"files/latency_max_metrics{i}" for i in range(1, 6)]
latency_max_burst_files = [f"files/latency_max_metrics{i}_burst_with_zeros" for i in range(1, 6)]
latency_max_output_files = [f"files/lat_max_metrics{i}" for i in range(1, 6)]

for lat_file, lat_burst_file, lat_output_file in zip(latency_files, latency_burst_files, latency_avg_output_files):
    latency_avg(lat_file, lat_burst_file, lat_output_file)


for bw_file, bw_burst_file, bw_output_file in zip(bandwidth_files, bandwidth_burst_files, bandwidth_output_files):
    sum_rows(bw_file, bw_burst_file, bw_output_file)


for lat_file, lat_burst_file, lat_output_file in zip(latency_max_files, latency_max_burst_files, latency_max_output_files):
    max_rows(lat_file, lat_burst_file, lat_output_file)



