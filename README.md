# HojaTrabajo5
Tarea para la clase de "Algoritmos y Estructuras de Datos" de la UVG.

Inverstigación:
### 📌 **Colas con SimPy: Uso de `Resource` y `Container`**  

En **SimPy**, una biblioteca de simulación de eventos discretos en Python, se pueden modelar **colas** utilizando las clases `Resource` y `Container`. Estas clases permiten simular escenarios como servidores, estaciones de trabajo, máquinas en producción, entre otros.

---

## 🔹 **1. `Resource`: Simulación de Servidores (Colas FIFO)**  
Un **`Resource`** en SimPy representa un recurso limitado que puede ser solicitado (`request`) y liberado (`release`).  
Se usa para modelar sistemas con colas como bancos, estaciones de servicio, atención médica, etc.

### ✨ **Ejemplo: Simulación de una fila en un banco**  
Clientes llegan a un banco y solicitan atención a un cajero (recurso).  
```python
import simpy
import random

# Parámetros del sistema
TIEMPO_SERVICIO = 5   # Tiempo medio de servicio
INTERVALO_LLEGADA = 3  # Intervalo entre llegadas
NUM_CAJEROS = 2       # Número de cajeros disponibles
TIEMPO_SIMULACION = 20

def cliente(env, nombre, banco):
    """Simula la llegada de un cliente al banco y su espera por un cajero."""
    print(f"{nombre} llega al banco en el tiempo {env.now:.2f}")
    
    with banco.request() as cajero:
        yield cajero  # Espera turno para ser atendido
        print(f"{nombre} comienza a ser atendido en {env.now:.2f}")
        yield env.timeout(random.expovariate(1.0 / TIEMPO_SERVICIO))  # Tiempo de atención
        print(f"{nombre} termina su atención en {env.now:.2f}")

def generar_clientes(env, banco):
    """Genera clientes en intervalos aleatorios."""
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / INTERVALO_LLEGADA))  # Tiempo entre llegadas
        i += 1
        env.process(cliente(env, f"Cliente {i}", banco))

# Configuración del entorno de SimPy
env = simpy.Environment()
banco = simpy.Resource(env, capacity=NUM_CAJEROS)  # Cola con 2 cajeros

# Iniciar la simulación
env.process(generar_clientes(env, banco))
env.run(until=TIEMPO_SIMULACION)
```

### 📌 **Explicación:**
- Los **clientes** llegan en intervalos aleatorios (`random.expovariate`).
- **Solicitan atención** (`request()`), se **atienden** (`timeout()`) y **se van** (`release()`).
- Se usa una **cola FIFO**: los primeros en llegar son los primeros en ser atendidos.
- **`Resource(capacity=N)`** controla el número de servidores disponibles.

---

## 🔹 **2. `Container`: Manejo de Inventarios y Recursos Compartidos**  
Un **`Container`** en SimPy representa un almacén o tanque de recursos, permitiendo **agregar (`put`) y retirar (`get`)** unidades.

### ✨ **Ejemplo: Simulación de un tanque de gasolina en una estación**  
Un camión de gasolina llena un tanque y los autos van retirando gasolina.
```python
import simpy
import random

# Parámetros
CAPACIDAD_TANQUE = 100  # Litros de gasolina
RELLENO_TANQUE = 20     # Litros agregados en cada recarga
CONSUMO_AUTO = 10       # Litros que consume cada auto
INTERVALO_AUTOS = 3     # Tiempo entre llegadas de autos
TIEMPO_SIMULACION = 20

def auto(env, nombre, tanque):
    """Simula un auto que necesita gasolina."""
    print(f"{nombre} llega a la gasolinera en {env.now:.2f}")
    
    with tanque.get(CONSUMO_AUTO) as req:
        yield req
        print(f"{nombre} carga {CONSUMO_AUTO} litros en {env.now:.2f}")

def rellenar_tanque(env, tanque):
    """Simula la llegada del camión de gasolina para reabastecer el tanque."""
    while True:
        yield env.timeout(5)  # Cada 5 unidades de tiempo llega el camión
        if tanque.level < CAPACIDAD_TANQUE:
            yield tanque.put(RELLENO_TANQUE)
            print(f"Tanque rellenado en {env.now:.2f}, nivel actual: {tanque.level}")

# Configuración del entorno de SimPy
env = simpy.Environment()
tanque = simpy.Container(env, init=50, capacity=CAPACIDAD_TANQUE)  # Comienza con 50 litros

# Procesos
env.process(rellenar_tanque(env, tanque))
for i in range(5):  # Inicialmente 5 autos
    env.process(auto(env, f"Auto {i+1}", tanque))
    yield env.timeout(INTERVALO_AUTOS)

# Iniciar la simulación
env.run(until=TIEMPO_SIMULACION)
```

### 📌 **Explicación:**
- Un **tanque de gasolina (`Container`)** almacena combustible con capacidad limitada.
- Los autos **toman gasolina (`get()`)**, y si no hay suficiente, esperan.
- Un camión **rellena el tanque (`put()`)** cada cierto tiempo.

---

## 🔹 **Comparación entre `Resource` y `Container`**
| **Característica** | **Resource** | **Container** |
|------------------|------------|------------|
| Modelo | Servidores, procesos con espera | Inventarios, almacenamiento de recursos |
| Tipo de acceso | FIFO (primero en llegar, primero atendido) | Cantidad definida, no en orden |
| Ejemplo | Atención en un banco | Tanque de gasolina |

---
### 📌 **Definiciones:** 
**intervalos(definición):** Tiempo promedio entre llegadas de procesos (a menor el valor, mayor la cantidad de procesos).

### **Referencias:**
ChatGPT. (2025, 18 de febrero). Conclusiones sobre el proyecto de carrito impulsado por energía potencial gravitatoria. OpenAI. https://chat.openai.com/
