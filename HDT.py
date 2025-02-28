import simpy  # Librería para simulación de eventos discretos
import random  # Generación de números aleatorios
import matplotlib.pyplot as plt  # Gráfico

# Configuración de la simulación
RANDOM_SEED = 42  # Semilla para reproducibilidad
MEMORY_CAPACITY = 100  # Memoria RAM total del sistema
CPU_CAPACITY = 1  # Número de CPUs disponibles
INSTRUCTIONS_PER_CYCLE = 3  # Instrucciones ejecutadas por ciclo

# Parámetros de prueba
num_processes_list = [25, 50, 100]  # Diferentes cantidades de procesos a probar
intervals = [10, 5, 1]  # Intervalos de llegada de procesos

# Función que simula un proceso
def process(env, name, ram, cpu, memory_needed, instructions):
    yield ram.get(memory_needed)  # Solicita memoria RAM
    with cpu.request() as req:
        yield req  # Espera turno en CPU
        while instructions > 0:
            yield env.timeout(1)  # Simula uso del CPU
            instructions -= min(INSTRUCTIONS_PER_CYCLE, instructions)
    ram.put(memory_needed)  # Libera memoria RAM
    process_times.append(env.now)

# Función que ejecuta la simulación
def simulate_system(num_processes, arrival_interval):
    global process_times
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    ram = simpy.Container(env, init=MEMORY_CAPACITY, capacity=MEMORY_CAPACITY)
    cpu = simpy.Resource(env, capacity=CPU_CAPACITY)
    process_times = []

    def generate_processes(env):
        for i in range(num_processes):
            memory_needed = random.randint(1, 10)
            instructions = random.randint(1, 10)
            env.process(process(env, f'P{i}', ram, cpu, memory_needed, instructions))
            yield env.timeout(random.expovariate(1.0 / arrival_interval))

    env.process(generate_processes(env))
    env.run()
    return sum(process_times) / len(process_times)

# Ejecutar simulaciones y almacenar resultados
results = {interval: [] for interval in intervals}
for interval in intervals:
    for num_processes in num_processes_list:
        avg_time = simulate_system(num_processes, interval)
        results[interval].append((num_processes, avg_time))

# Generar gráfico
plt.figure()
for interval, data in results.items():
    x, y = zip(*data)
    plt.plot(x, y, marker='o', label=f'Intervalo {interval}')
plt.xlabel('Número de procesos')
plt.ylabel('Tiempo promedio')
plt.title('Simulación de procesos')
plt.legend()
plt.grid(True)
plt.savefig("simulacion_procesos.png")
plt.show()

print("Simulación completada. Gráfica guardada.")
