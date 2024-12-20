#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 $1 file1 [file2 file3 ...]"
    exit 1
fi

x="$1"
shift #Deletes $1

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

metrics=("bandwidth" "latency_max" "latency")
values=(40 60 30 40)
for j in {1..4}; do
  for metric in "${metrics[@]}"; do
    ./aconditioning.sh "files/${metric}_metrics${j}_${x}" "${values[$((j-1))]}"
  done
done

for metric in "${metrics[@]}"; do
    ./vectorization.sh "files/${metric}_metrics1_${x}" 20 40
    ./vectorization.sh "files/${metric}_metrics2_${x}" 20 20
    ./vectorization.sh "files/${metric}_metrics3_${x}" 40 30
    ./vectorization.sh "files/${metric}_metrics4_${x}" 40 20
done

for j in {1..5}; do  
  for metric in "${metrics[@]}"; do
    ./aconditioning.sh "files/${metric}_metrics${j}_${x}" 100
  done
done
