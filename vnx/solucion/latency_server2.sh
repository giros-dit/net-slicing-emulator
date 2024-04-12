#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test2_results"

#Process each file passed as an argument
for file in "$@"; do
    output_latency_file="${output_folder}/latency_$(basename "$file")"
    output_latency_file_max="${output_folder}/latency_max_$(basename "$file")"
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


    # Extract latency values
    latency_values=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}' | grep -v '^$')
    latency_values_max=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $17); print $17}' | grep -v '^$')



    # Save bandwidth values to the output file
    echo "$bandwidth_values" > "$output_bandwidth_file"
    echo "$latency_values" > "$output_latency_file"
    echo "$latency_values_max" > "$output_latency_file_max"

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

cd test2_results
./vectorization.sh bandwidth_metrics2 40 40
./vectorization.sh bandwidth_metrics3 40 20
./vectorization.sh latency_max_metrics1 20 60
./vectorization.sh latency_max_metrics5 40 40
./vectorization.sh latency_metrics2 40 40
./vectorization.sh latency_metrics3 40 20
./vectorization.sh bandwidth_metrics1 20 60
./vectorization.sh bandwidth_metrics5 40 40
./vectorization.sh latency_max_metrics2 40 40
./vectorization.sh latency_max_metrics3 40 20
./vectorization.sh latency_metrics1 20 60
./vectorization.sh latency_metrics5 40 40

./aconditioning.sh bandwidth_metrics2_with_zeros
./aconditioning.sh bandwidth_metrics3_with_zeros
./aconditioning.sh latency_max_metrics1_with_zeros
./aconditioning.sh latency_max_metrics4
./aconditioning.sh latency_max_metrics5_with_zeros
./aconditioning.sh latency_metrics2_with_zeros
./aconditioning.sh latency_metrics3_with_zeros
./aconditioning.sh bandwidth_metrics1_with_zeros
./aconditioning.sh bandwidth_metrics4
./aconditioning.sh bandwidth_metrics5_with_zeros
./aconditioning.sh latency_max_metrics2_with_zeros
./aconditioning.sh latency_max_metrics3_with_zeros
./aconditioning.sh latency_metrics1_with_zeros
./aconditioning.sh latency_metrics4
./aconditioning.sh latency_metrics5_with_zeros


