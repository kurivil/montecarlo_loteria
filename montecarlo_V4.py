import random
from collections import Counter
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def generate_combination(weighted_numbers, num_to_play):
    return tuple(sorted(random.sample(weighted_numbers, num_to_play)))

def montecarlo_lottery_simulation(numbers, frequencies, num_to_play, iterations, processes):
    weighted_numbers = [num for num, freq in zip(numbers, frequencies) for _ in range(int(freq * 1000))]
    
    with Pool(processes) as pool:
        combinations = list(tqdm(pool.imap(lambda _: generate_combination(weighted_numbers, num_to_play), range(iterations)), total=iterations, desc="Simulando"))
    
    most_common_combination, count = Counter(combinations).most_common(1)[0]
    return most_common_combination, count

if __name__ == "__main__":
    print("Bienvenido al simulador de lotería por Montecarlo")
    print(f"Procesadores disponibles: {cpu_count()}")
    
    num_available = int(input("Ingrese la cantidad total de números disponibles: "))
    num_to_play = int(input("Ingrese la cantidad de selecciones por sorteo: "))
    iterations = int(input("Ingrese la cantidad de iteraciones: "))
    processes = int(input(f"Ingrese la cantidad de procesos a utilizar (máximo {cpu_count()}): "))
    
    numbers = list(range(1, num_available + 1))
    frequencies = [1.743, 1.706, 1.704, 1.767, 1.791, 1.717, 1.735, 1.755, 1.765, 1.815,
                   1.748, 1.778, 1.746, 1.697, 1.750, 1.710, 1.706, 1.746, 1.719, 1.707,
                   1.734, 1.705, 1.713, 1.744, 1.770]  # Ajustar según el orden de entrada
    
    most_common_combination, count = montecarlo_lottery_simulation(numbers, frequencies, num_to_play, iterations, processes)
    
    print(f"Combinación más común: {most_common_combination} (apareció {count} veces)")
