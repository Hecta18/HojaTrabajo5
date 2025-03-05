#fase1: codigo
#simulacion que tiene que mostrar tiempo promedio por proceso y la desviacion estandar entre los tiempos de los procesos
# grafica x = #procesos, y = tiempo promedio

#fase2: pruebas segun intervalos
#3 pruebas: 10, 5, 1
#   numero de procesos por prueba: 25, 50, 100, 150, 200

#fase3: pruebas segun procesadores y memoria
#   memoria 200
#   memoria 100, 6 instrucciones por unidad de tiempo (velocidad de procesador)
#   memoria 100, velocidad de procesador normal, 2 procesadores

import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la simulación
RANDOM_SEED = 42
t_service = 6  # Tiempo de servicio por cliente
t_arrive = 2  # Intervalo de llegada de clientes
q_register = 3  # Cantidad de registros disponibles
t_simulation = 25  # Tiempo total de simulación

# Función que simula un cliente
def client(env, name, register, service_times):
    print(f'{name} llega al banco en la unidad de tiempo No.{env.now:.1f}')
    with register.request() as req:
        yield req
        print(f'{name} comienza a ser atendido en la unidad de tiempo No.{env.now:.1f}')
        yield env.timeout(t_service)
        print(f'{name} termina de ser atendido en la unidad de tiempo No.{env.now:.1f}')
        service_times.append(env.now)

# Función que genera clientes
def generate_clients(env, register, service_times):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / t_arrive))
        i += 1
        env.process(client(env, f'Cliente {i}', register, service_times))

# Función que ejecuta la simulación
def simulate_bank():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    register = simpy.Resource(env, capacity=q_register)
    service_times = []

    env.process(generate_clients(env, register, service_times))
    env.run(until=t_simulation)
    return service_times

# Ejecutar simulaciones y almacenar resultados
def run_simulations():
    service_times = simulate_bank()
    if service_times:
        avg_time = sum(service_times) / len(service_times)
        std_dev = np.std(service_times)
        print(f'Tiempo promedio por cliente: {avg_time:.2f}')
        print(f'Desviación estándar de los tiempos de servicio: {std_dev:.2f}')
    else:
        print('No hubo clientes durante la simulación.')
    return service_times

# Generar gráficos
def plot_results(service_times):
    plt.figure()
    plt.hist(service_times, bins=10, edgecolor='black')
    plt.xlabel('Tiempo de servicio')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de tiempos de servicio')
    plt.grid(True)
    plt.savefig("distribucion_tiempos_servicio.png")
    plt.show()

    avg_time = sum(service_times) / len(service_times)
    std_dev = np.std(service_times)

    plt.figure()
    plt.bar(['Promedio', 'Desviación Estándar'], [avg_time, std_dev], color=['blue', 'orange'])
    plt.ylabel('Tiempo')
    plt.title('Tiempo promedio y desviación estándar')
    plt.grid(True)
    plt.savefig("promedio_desviacion_estandar.png")
    plt.show()

if __name__ == "__main__":
    service_times = run_simulations()
    plot_results(service_times)
    print("Simulación completada. Gráficas guardadas.")