#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test3_results"

#Process each file passed as an argument
for file in "$@"; do
    output_latency_file="${output_folder}/$(basename "$file")"

    # Extract latency values
    latency_values=$(sudo grep 'ms' "$file" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}' | grep -v '^$')

    # Save latency values to the output file
    echo "$latency_values" > "$output_latency_file.tmp"
    head -n -1 "$output_latency_file.tmp" > "$output_latency_file"
    rm "$output_latency_file.tmp"
done

echo "Latency data saved to $output_latency_file"

cd test3_results
./vectorization.sh latency_h5 40 10
./vectorization.sh latency_h8 40 10
./vectorization.sh latency_h9 40 10
./vectorization.sh latency_h3 20 10
./vectorization.sh latency_h10 20 10 
./vectorization.sh latency_h2 60 20
./vectorization.sh latency_h4 60 20

echo "Vectorizing files" 
