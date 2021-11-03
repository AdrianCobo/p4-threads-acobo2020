import RPi.GPIO as GPIO
import time
import threading
import signal
import sys

pulsadorGPIO1 = 16
pulsadorGPIO2 = 21
ledGPIO1=20
ledGPIO2=12

def encender2leds(pulsado1,pulsado2):#metodo para encender 2 leds a la vez
    if (not pulsado1) and (not pulsado2):
        pwm.ChangeDutyCycle(100)
        pulsado1 = True
        pwm2.ChangeDutyCycle(100)
        pulsado2 = True
        time.sleep(0.1)

def endenderled(pulsado,pwm):#metodo para encender solo el led que toque
    if not pulsado:
                time.sleep(0.1)
                pwm.ChangeDutyCycle(100)
                pulsado = True
                time.sleep(0.1)

def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)



def ejecucion():

    pulsado1 = False#variables booleanas que nos van a sevir para evitar rebotes
    pulsado2 = False

    while True:
        if (not GPIO.input(pulsadorGPIO1) and (not GPIO.input(pulsadorGPIO2))):#si estan los dos botones presionados
            encender2leds(pulsado1,pulsado2)

        elif not GPIO.input(pulsadorGPIO1): #si el boton 1 esta presionado
            endenderled(pulsado1,pwm)

        elif not GPIO.input(pulsadorGPIO2):#si el boton 2 esta presionado
            endenderled(pulsado2,pwm2)

        else :#sino se apagan los leds y se reestablecen las variables booleanas
            pulsado1 = False
            pwm.ChangeDutyCycle(0)
            pulsado2 = False
            pwm2.ChangeDutyCycle(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    # Activamos resistencia pull_up_down en modo HIGH, esto es:
    # - HIGH: estado por defecto del GPIO (no se ha pulsado).
    # - LOW: estado del GPIO cuando se ha pulsado el boton.
    GPIO.setup(pulsadorGPIO1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pulsadorGPIO2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #indicamos que el pin que vamos a usar para los leds , va a ser de salida
    GPIO.setup (ledGPIO1, GPIO.OUT)
    GPIO.setup (ledGPIO2, GPIO.OUT)
    #creamos un objeto PWM con los mines de los leds a usar y la frecuencia de trabajo como parametros:
    pwm = GPIO.PWM(ledGPIO1,100)
    pwm2 = GPIO.PWM(ledGPIO2,100)
    #establecemos el ciclo de trabajo o DutyCyle a 0 para que empiecen los leds apagados
    pwm.start (0)
    pwm2.start (0)
    time.sleep(0.1)
    pulsado1 = False#variables booleanas que nos van a sevir para evitar rebotes
    pulsado2 = False

    hilo1 = threading.Thread(target=ejecucion)
    hilo1.start()

    signal.signal(signal.SIGINT, callbackSalir)
    signal.pause()