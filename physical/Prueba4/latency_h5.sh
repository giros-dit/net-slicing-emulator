#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

output_name_file="$1"


#Folder to save the results
output_folder="test4_results"

#Process each file passed as an argument
output_latency_file="${output_folder}/$(basename "$output_name_file")"

for file in "$@"; do
    if [ -f "$file" ]; then
        avg_latency=$(tail -n 1 "$file" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}')
	if [ -z "$avg_latency" ]; then
            avg_latency=$(tail -n 2 "$file" | awk -F '[ /]+' '{gsub("/", " ", $15); print $15}' prueba)
        fi
        echo "$avg_latency" >> "$output_latency_file"
    fi
done

echo "Latency data saved to $output_latency_file"
