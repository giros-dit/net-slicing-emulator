#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test_results/files"

#Process each file passed as an argument
for file in "$@"; do
    output_bandwidth_file="${output_folder}/bandwidth_$(basename "$file")"  # Output file name

    # Extract bandwidth values
    bandwidth_values=$(grep -E '\[ *[0-9]+\] .* (Mbits/sec|Kbits/sec|bits/sec)' "$file" | awk '{
        for (i=1; i<=NF; i++) {
            if ($i ~ /Kbits\/sec/) {
                printf "%f\n", $(i-1)/1000;
            } else if ($i ~ /Mbits\/sec/) {
                print $(i-1);
            }
            else if ($i ~ /bits\/sec/){
                printf "%f\n", $(i-1)/1000000;
            }
        }
    }')


    # Save bandwidth values to the output file
    echo "$bandwidth_values" > "$output_bandwidth_file"
done


cd test_results
./vectorization.sh files/bandwidth_metrics1_sender_burst 100 0
./vectorization.sh files/bandwidth_metrics2_sender_burst 100 0
./vectorization.sh files/bandwidth_metrics3_sender_burst 100 0
./vectorization.sh files/bandwidth_metrics4_sender_burst 100 150
./vectorization.sh files/bandwidth_metrics5_sender_burst 100 0

./aconditioning.sh files/bandwidth_metrics1_sender_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics2_sender_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics3_sender_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics4_sender_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics5_sender_burst_with_zeros
./aconditioning.sh files/bandwidth_metrics1_sender
./aconditioning.sh files/bandwidth_metrics2_sender
./aconditioning.sh files/bandwidth_metrics3_sender
./aconditioning.sh files/bandwidth_metrics4_sender
./aconditioning.sh files/bandwidth_metrics5_sender

