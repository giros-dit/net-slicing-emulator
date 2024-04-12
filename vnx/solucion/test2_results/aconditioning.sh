input_file="$1"

while true; do
    # Contar el número de líneas en el archivo
    lineas=$(wc -l < "$input_file")
    # Verificar si el número de líneas es mayor que 1498
    if [ "$lineas" -lt 120 ]; then
        # Buscar la última línea distinta de 0 y su número de línea
        #last_line=$(awk '!/^0$/{line=$0; num=NR} END{print line, num}' "$input_file")
        #last_line_num=$(echo "$last_line" | awk '{print $2}')
        #if [ -n "$last_line" ]; then  # Verificar si se encontró una línea distinta de 0
        #    sed -i "${last_line_num}d" "$input_file"  # Eliminar la última línea distinta de 0 del archivo
        #else
        #    break  # Si no se encontró ninguna línea distinta de 0, salir del bucle
        #fi
        echo "0" >> "$input_file"
    else
        break  # Salir del bucle si el número de líneas es menor o igual a 1498
    fi
done
