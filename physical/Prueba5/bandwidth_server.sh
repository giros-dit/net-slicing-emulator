#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 file1 [file2 file3 ...]"
    exit 1
fi

#Folder to save the results
output_folder="test5_results"

#Process each file passed as an argument
for file in "$@"; do

    output_file="${output_folder}/bandwidth_$(basename "$file")"  # Output file name

    # Extract values
    bandwidth_values=$(sudo grep -E '\[ *[0-9]+\] .* Mbits/sec' "$file" | awk '{for(i=1;i<=NF;i++) if($i == "Mbits/sec") print $(i-1)}')

    # Save bandwidth values to the output file
    echo "$bandwidth_values" > "$output_file.tmp"

    # Delete last line (avg BW)
    head -n -1 "$output_file.tmp" > "$output_file"

    # Delete temporal file
    rm "$output_file.tmp"

    echo "Bandwidth data saved to $output_file"
done
