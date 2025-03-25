import random
import multiprocessing
from collections import Counter
import csv
from tqdm import tqdm

# Parámetros de la simulación
num_simulaciones = int(input("Introduce el número de simulaciones (default 4496388): ") or 4496388)  # Número de iteraciones de Montecarlo
n_total = int(input("Introduce el total de números posibles (default 25): ") or 25)  # Total de números posibles
k_seleccion = int(input("Introduce la cantidad de números por combinación (default 14): ") or 14)  # Cantidad de números por combinación

# Número de núcleos a utilizar, automáticamente detectados
num_procesos = int(input(f"Introduce el número de procesos (default {multiprocessing.cpu_count()}): ") or multiprocessing.cpu_count())  # Núcleos disponibles

# Función para generar una simulación de Montecarlo
def simulacion_montecarlo(_):
    # Generamos una combinación aleatoria de k números entre 1 y n_total
    return tuple(sorted(random.sample(range(1, n_total + 1), k_seleccion)))  # Usamos tuple y ordenamos para contar combinaciones únicas

# Función para contar los números +más frecuentes
def contar_frecuencias(simulaciones):
    # Contamos las frecuencias de cada número entre 1 y n_total
    contador = Counter([num for combinacion in simulaciones for num in combinacion])
    return contador

# Función para contar las combinaciones más frecuentes
def contar_combinaciones(simulaciones):
    # Contamos cuántas veces aparece cada combinación de números
    return Counter(simulaciones)

# Realizamos las simulaciones
if __name__ == '__main__':
    # Creamos una lista para almacenar las simulaciones
    simulaciones = []

    # Ejecutamos las simulaciones en paralelo utilizando multiprocessing con barra de progreso
    with multiprocessing.Pool(processes=num_procesos) as pool:
        # Usamos imap_unordered para poder actualizar tqdm mientras se ejecutan las simulaciones
        for combinacion in tqdm(pool.imap_unordered(simulacion_montecarlo, range(num_simulaciones)), total=num_simulaciones):
            # Almacenamos cada combinación en la lista 'simulaciones'
            simulaciones.append(combinacion)

    # Contamos las frecuencias de aparición de cada número
    frecuencias = contar_frecuencias(simulaciones)

    # Contamos las combinaciones más frecuentes
    combinaciones_frecuentes = contar_combinaciones(simulaciones)

    # Mostramos las frecuencias de los números más comunes
    print("Frecuencias de aparición de cada número:")
    for num, count in frecuencias.most_common():
        print(f"Número {num}: {count} veces")

    # Mostramos la combinación que más salió
    combinacion_mas_frecuente, veces = combinaciones_frecuentes.most_common(1)[0]
    print(f"\nLa combinación más frecuente fue: {combinacion_mas_frecuente}, que salió {veces} veces")

    # Guardamos los resultados en un archivo CSV
    with open("resultados_simulacion.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Número", "Frecuencia"])
        for num, count in frecuencias.items():
            writer.writerow([num, count])

        # Agregar la combinación más frecuente al CSV
        writer.writerow([])
        writer.writerow(["Combinación más frecuente", "Veces"])
        writer.writerow([combinacion_mas_frecuente, veces])

    print("Los resultados han sido guardados en 'resultados_simulacion.csv'.")
