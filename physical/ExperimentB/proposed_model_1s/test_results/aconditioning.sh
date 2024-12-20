input_file="$1"
lines="$2"

while true; do
    # Contar el número de líneas en el archivo
    lineas=$(wc -l < "$input_file")
    # Verificar si el número de líneas es mayor que 1498
    if [ "$lineas" -gt "$lines" ]; then
        sed -i '$d' "$input_file"
    else
        break  # Salir del bucle si el número de líneas es menor o igual a 1498
    fi
done
