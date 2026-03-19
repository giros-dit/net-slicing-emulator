#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test_results/files"

#Process each file passed as an argument
for file in "$@"; do
    output_latency_file_max="${output_folder}/latency_max_$(basename "$file")"
    output_bandwidth_file="${output_folder}/bandwidth_$(basename "$file")"  # Output file name

    # Extract bandwidth values
    bandwidth_values=$(grep -E '\[ *[0-9]+\] .* (Mbits/sec|Kbits/sec|bits/sec)' "$file" | awk '{
        for (i=1; i<=NF+1; i++) {
            if ($i ~ /Kbits\/sec/) {
                printf "%f\n", $(i-1)/1000;
            } else if ($i ~ /Mbits\/sec/) {
                print $(i-1);
            }
            else if ($i ~ /bits\/sec/){
	        if ($(i-1) == 0) {
                    print 0;
                } else {
                    printf "%f\n", $(i-1)/1000000;
                }
            }
        }
    }')


    # Extract values
    latency_values_max=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $17); print $17}' | grep -v '^$')

    # Save latency values to the output file
    echo "$bandwidth_values" >> "$output_bandwidth_file"
    echo "$latency_values_max" >> "$output_latency_file_max"
done


echo "Latency data saved"
echo "Bandwidth data saved"

cd test_results
./vectorization.sh files/bandwidth_metrics1_burst 100 0
./vectorization.sh files/bandwidth_metrics2_burst 100 0
./vectorization.sh files/bandwidth_metrics3_burst 100 150
./vectorization.sh files/bandwidth_metrics4_burst 100 150
./vectorization.sh files/bandwidth_metrics5_burst 100 0
./vectorization.sh files/latency_max_metrics1_burst 100 0
./vectorization.sh files/latency_max_metrics2_burst 100 0
./vectorization.sh files/latency_max_metrics3_burst 100 150
./vectorization.sh files/latency_max_metrics4_burst 100 150
./vectorization.sh files/latency_max_metrics5_burst 100 0

./vectorization.sh files/bandwidth_metrics3 0 150
./vectorization.sh files/latency_max_metrics3 0 150
./vectorization.sh files/bandwidth_metrics6 450 0
./vectorization.sh files/latency_max_metrics6 450 0


mv files/bandwidth_metrics3_with_zeros files/bandwidth_metrics3
mv files/latency_max_metrics3_with_zeros files/latency_max_metrics3
mv files/bandwidth_metrics6_with_zeros files/bandwidth_metrics6
mv files/latency_max_metrics6_with_zeros files/latency_max_metrics6


#sudo rm -f bandwidth_metrics1_burst bandwidth_metrics2_burst bandwidth_metrics3_burst bandwidth_metrics4_burst bandwidth_metrics5_burst latency_max_metrics1_burst latency_max_metrics2_burst latency_max_metrics3_burst latency_max_metrics4_burst latency_max_metrics5_burst latency_metrics1_burst latency_metrics2_burst latency_metrics3_burst latency_metrics4_burst latency_metrics5_burst

./aconditioning.sh files/bandwidth_metrics1
./aconditioning.sh files/bandwidth_metrics2
./aconditioning.sh files/bandwidth_metrics3
./aconditioning.sh files/bandwidth_metrics4
./aconditioning.sh files/bandwidth_metrics5
./aconditioning.sh files/bandwidth_metrics6
./aconditioning.sh files/latency_max_metrics1
./aconditioning.sh files/latency_max_metrics2
./aconditioning.sh files/latency_max_metrics3
./aconditioning.sh files/latency_max_metrics4
./aconditioning.sh files/latency_max_metrics5
./aconditioning.sh files/latency_max_metrics6
./aconditioning.sh files/bandwidth_metrics1_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics2_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics3_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics4_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics5_burst_with_zeros
./aconditioning.sh files/latency_max_metrics1_burst_with_zeros
./aconditioning.sh files/latency_max_metrics2_burst_with_zeros
./aconditioning.sh files/latency_max_metrics3_burst_with_zeros
./aconditioning.sh files/latency_max_metrics4_burst_with_zeros
./aconditioning.sh files/latency_max_metrics5_burst_with_zeros
