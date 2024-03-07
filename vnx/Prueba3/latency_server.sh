#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test3_results"

#Process each file passed as an argument
output_jitter_file="${output_folder}/jitter_h1"
output_latency_file="${output_folder}/latency_h1"
output_latency_max_file="${output_folder}/latency_h1_max"
output_latency_min_file="${output_folder}/latency_h1_min"

# Extract jitter values
jitter_values=$(sudo awk '/sec/ {print $9}' "$1" | grep -v '^$')

# Save jitter values to the output file
echo "$jitter_values" > "$output_jitter_file.tmp"

# Delete last line (avg BW)
head -n -1 "$output_jitter_file.tmp" > "$output_jitter_file"

# Delete temporal file
rm "$output_jitter_file.tmp"

echo "Jitter data saved to $output_jitter_file"

# Extract latency values
latency_avg_values=$(sudo grep 'ms' "$1" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}' | grep -v '^$')
latency_avg_values=$(sudo grep 'ms' "$1" | awk -F '[ /]+' '{gsub("/", " ", $16); print $16}' | grep -v '^$')
latency_avg_values=$(sudo grep 'ms' "$1" | awk -F '[ /]+' '{gsub("/", " ", $17); print $17}' | grep -v '^$')

# Save latency values to the output file
echo "$latency_avg_values" > "$output_latency_file.tmp"
echo "$latency_max_values" > "$output_latency_max_file.tmp"
echo "$latency_min_values" > "$output_latency_min_file.tmp"

# Delete last line
head -n -1 "$output_latency_file.tmp" > "$output_latency_file"
head -n -1 "$output_latency_max_file.tmp" > "$output_latency_max_file"
head -n -1 "$output_latency_min_file.tmp" > "$output_latency_min_file"

# Delete temporal file
rm "$output_latency_file.tmp"
rm "$output_latency_max_file.tmp"
rm "$output_latency_min_file.tmp"

echo "Latency data saved"
