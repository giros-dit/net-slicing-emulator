#!/bin/bash

# Verificar la cantidad correcta de argumentos
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 input_file num_zeros_beginning num_zeros_end"
    exit 1
fi

input_file="$1"
num_zeros_beginning="$2"
num_zeros_end="$3"

output_file="${input_file}_with_zeros"

# Generate zeros at the beggining
for ((i=1; i<=num_zeros_beginning; i++)); do
    echo "0" >> "$output_file"
done

cat "$input_file" >> "$output_file"

# Generate zeros at the end
for ((i=1; i<=num_zeros_end; i++)); do
    echo "0" >> "$output_file"
done
