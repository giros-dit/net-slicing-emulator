#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test_results/files"

#Process each file passed as an argument
for file in "$@"; do
    output_latency_file="${output_folder}/latency_$(basename "$file")"
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
    latency_values=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}' | grep -v '^$')
    latency_values_max=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $17); print $17}' | grep -v '^$')

    # Save latency values to the output file
    echo "$bandwidth_values" > "$output_bandwidth_file.tmp"
    head -n -1 "$output_bandwidth_file.tmp" > "$output_bandwidth_file"
    rm "$output_bandwidth_file.tmp"
    echo "$latency_values" > "$output_latency_file.tmp"
    head -n -1 "$output_latency_file.tmp" > "$output_latency_file"
    rm "$output_latency_file.tmp"
    echo "$latency_values_max" > "$output_latency_file_max.tmp"
    head -n -1 "$output_latency_file_max.tmp" > "$output_latency_file_max"
    rm "$output_latency_file_max.tmp"

done


echo "Latency data saved"
echo "Bandwidth data saved"

cd test_results

./aconditioning.sh files/bandwidth_metrics1 40 
./aconditioning.sh files/bandwidth_metrics2 60
./aconditioning.sh files/bandwidth_metrics3 30
./aconditioning.sh files/bandwidth_metrics4 40
./aconditioning.sh files/latency_max_metrics1 40
./aconditioning.sh files/latency_max_metrics2 60
./aconditioning.sh files/latency_max_metrics3 30
./aconditioning.sh files/latency_max_metrics4 40
./aconditioning.sh files/latency_metrics1 40
./aconditioning.sh files/latency_metrics2 60
./aconditioning.sh files/latency_metrics3 30
./aconditioning.sh files/latency_metrics4 40

./vectorization.sh files/bandwidth_metrics1 20 40 
./vectorization.sh files/bandwidth_metrics2 20 20
./vectorization.sh files/bandwidth_metrics3 40 30
./vectorization.sh files/bandwidth_metrics4 40 20
./vectorization.sh files/latency_max_metrics1 20 40
./vectorization.sh files/latency_max_metrics2 20 20
./vectorization.sh files/latency_max_metrics3 40 30
./vectorization.sh files/latency_max_metrics4 40 20
./vectorization.sh files/latency_metrics1 20 40
./vectorization.sh files/latency_metrics2 20 20
./vectorization.sh files/latency_metrics3 40 30
./vectorization.sh files/latency_metrics4 40 20

./aconditioning.sh files/bandwidth_metrics1_with_zeros 100
./aconditioning.sh files/bandwidth_metrics2_with_zeros 100
./aconditioning.sh files/bandwidth_metrics3_with_zeros 100
./aconditioning.sh files/bandwidth_metrics4_with_zeros 100
./aconditioning.sh files/bandwidth_metrics5 100
./aconditioning.sh files/latency_metrics1_with_zeros 100
./aconditioning.sh files/latency_metrics2_with_zeros 100
./aconditioning.sh files/latency_metrics3_with_zeros 100
./aconditioning.sh files/latency_metrics4_with_zeros 100
./aconditioning.sh files/latency_metrics5 100
./aconditioning.sh files/latency_max_metrics1_with_zeros 100
./aconditioning.sh files/latency_max_metrics2_with_zeros 100
./aconditioning.sh files/latency_max_metrics3_with_zeros 100
./aconditioning.sh files/latency_max_metrics4_with_zeros 100
./aconditioning.sh files/latency_max_metrics5 100
