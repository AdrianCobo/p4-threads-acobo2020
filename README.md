# P4-Threads

## (CC-BY-NC-SA) Adrián Cobo Merino

El objetivo de este esta práctica es tener la primera toma de contacto con los threads.

### Ejercicio1

En el ejercicio 1, aparte de corregir el problema del rebote añadiendo una condición booliana como flag, hemos hecho que la ejecución del
bucle infinito se realizada por un thread,permitiendonos asi, poder hacer otras cosas con el hilo pricipal como finalizar el programa 
usando control+c

```python
    hilo1 = threading.Thread(target=ejecucion) #ejecucion es el metodo con el bucle infinito
    hilo1.start()
        
    signal.signal(signal.SIGINT, callbackSalir)
    signal.pause()
```

### Ejercicio2

El esquema de los gpios utilizados es el mismo para los 3 programas y se intuye en: 

```python
GPIO.setmode(GPIO.BCM)
pulsadorGPIO1 = 16
pulsadorGPIO2 = 21
ledGPIO1=20
ledGPIO2=12
```
Para el programa sinInterrupcionesMejorado.py, hemos modificado el programa sinInterrupcionesMejorado.py entregado en la practica anterior
y hemos hecho como en el ejercicio1, es decir, hemos hecho que el bucle infinito sea ejecutada por un hilo que hemos creado 
permitiendonos continuar con la ejecucion del programa en el hilo principal y poder cerrar por ejemplo el programa con control+c.

Para el programa InterrupcionesMejorado.py nos encontramos con el problema de que el metodo wait_for_edge pasa un testigo al primer hilo
que lo ejecuta, impidiendonos asi poder controlar dos leds a la vez aun usando dos hilos pues hasta que no slotase el testigo el primer
hilo, no podría hacer nada el segundo. Para solucionar esto, hemos hecho InterrupcionesMejorado.py e InterrupcionesMejorado2.py los cuales 
al ser lanzados desde 2 terminales diferentes, si que nos permitirán controlar los dos botones a la vez, usando 2 hilos distintos.

Finalmente para el programa interrupcionEventMejorado.py,hemos creado 2 hilos que van a crear otros dos hilos en total con la función
add_event_detect, ya que add_event_detect ya crean hilos que van a estar pendientes de lo que pase en los pines indicados y actuar en función
de lo que tenan programada. Es algo redundante pero nos sirve para ver que efectivamente un hilo puede crear otros hilos.

**Importante: antes de usar estos programa ejecuta el programa GPIOCLEANUP.py para limpiar los GPIOS**

**A destacar:**

1)En los programas cuya lógica requieren que el hilo ejecute un bucle infinito, al hacer join de ese hilo, saltan los siguientes warnings:

```python
Traceback (most recent call last):
  File "/home/pi/Desktop/practica4/p4-threads-acobo2020/interrupcionEdgeBueno.py", line 34, in <module>
    hilo1.join()
  File "/usr/lib/python3.7/threading.py", line 1032, in join
    self._wait_for_tstate_lock()
  File "/usr/lib/python3.7/threading.py", line 1048, in _wait_for_tstate_lock
    elif lock.acquire(block, timeout):
KeyboardInterrupt
```
No he logrado saber a que se deben, por ello,utilizo la clase signal, la cual al utilizar el callback programado para salir nos deberia de 
limpiar todos los hilos creados; pero, siempre que uso este método, me saltan los siguientes errores también:

```python
Traceback (most recent call last):
  File "/home/pi/Desktop/practica4/p4-threads-acobo2020/interrupcionEdgeBueno.py", line 34, in <module>
    hilo1.join()
  File "/usr/lib/python3.7/threading.py", line 1032, in join
    self._wait_for_tstate_lock()
  File "/usr/lib/python3.7/threading.py", line 1048, in _wait_for_tstate_lock
    elif lock.acquire(block, timeout):
KeyboardInterrupt
```

Esos warnings no impiden el funcionamiento del programa y dejarían de salir si quitase el callback para salir. Esto no debería de tener 
ningún problema pues al finalizar el programa con control+c, el sistema operativo deberia borrar los hilos creados por el programa, pero 
prefiero mantener los warnings y asegurarme de que elimino los hilos pues es importante para el programador hacerse cargo de los hilos que 
crea.

2)La lógica del programa sinInterrupcionesMejorado.py nos permite encender el led al mantener pulsado el botón, y apagarlo al soltar, pero en
los programas InterrupcionesMejorado.py,InterrupcionesMejorado2.py y interrupcionEventMejorado.py tenemos que pulsar el botón correspondiente
al led una vex para encender, y otra para apagar.

Para cualquier duda: <a.cobo.2020@alumos.urjc.es>
