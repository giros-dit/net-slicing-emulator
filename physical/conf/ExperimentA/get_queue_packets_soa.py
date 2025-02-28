import subprocess
import time

# Función para extraer y guardar el valor de backlog de una clase específica
def save_backlog(backlog_list):
    result = "tc -s -d class show dev enp4s0 | grep -E -A 2 'class prio 1:' | grep backlog | awk '{{print $3}}' | sed 's/p//' | tr '\n' ',' | sed 's/,$//'" 
    backlog = subprocess.check_output(result, shell=True, text=True).strip()
    values = [int(value) for value in backlog.split(',')]
    for i, value in enumerate(values):
        backlog_list[i].append(value)


def save_packetloss(pktloss_list):
    result = "tc -s -d class show dev enp4s0 | grep -E -A 2 'class prio 1:' | grep dropped | awk '{{print $7}}' | sed 's/,//g' | tr '\n' ',' | sed 's/,$//'"
    packetloss = subprocess.check_output(result, shell=True, text=True).strip()
    values = [int(value) for value in packetloss.split(',')]
    # Asignar los valores a las listas correspondientes
    for i, value in enumerate(values):
        pktloss_list[i].append(value)




# Duración máxima en segundos
duration = 100
delta = 1
# Número de clases
num_queues = 3
# Crear una lista vacía para cada clase
backlogs = [[] for _ in range(num_queues)]
pktloss = [[] for _ in range(num_queues)]
# Calcular el número de iteraciones
iterations = int(duration / delta)


# Bucle para ejecutar el procesamiento un número específico de iteraciones
for _ in range(iterations):
    # Guardar tiempo de inicio del bucle
    loop_start = time.time()

    save_backlog(backlogs)
    save_packetloss(pktloss)

    # Obtener el tiempo de finalización del bucle
    loop_end = time.time()
    
    # Dormir antes de la siguiente iteración
    time.sleep(delta - (loop_end - loop_start))

# Sacar los valores de backlog_list y guardarlos en un archivo
for i, list in enumerate(backlogs):
    with open(f'/root/clase_{i + 1}_backlog', 'a') as file:
        for v in list:
            file.write(f'{v}\n')

for i, list in enumerate(pktloss):
    with open(f'/root/clase_{i + 1}_pktloss', 'a') as file:
        for v in list:
            file.write(f'{v}\n')
