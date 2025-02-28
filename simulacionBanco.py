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
#t significa tiempo, q significa cantidad
#---variables atencion al cliente
t_service = 6
t_arrive = 2
q_register = 3
#---variables cuenta de banco
limite_retiro = 100
deposito = 10
retiro = 10
t_transaccion = 5
t_simulation = 25 #varia segun la prueba
#implementar que se determine por input

def client(nombre, cuenta, env):
    println(f'{nombre} llega al banco en la unidad de tiempo No.{env.now:.1f}')
    #:.1f redondea a 1 decimal
    
    
# Iniciar la simulación
env.process()
env.run(until=t_simulation)