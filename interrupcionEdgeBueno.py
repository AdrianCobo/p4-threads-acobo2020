#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import signal
import sys
import threading

pulsadorGPIO = 16

def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def ejecucion():
    pulsado = False
    while True:

        GPIO.wait_for_edge(pulsadorGPIO, GPIO.RISING)
        if not pulsado:
            print("El boton se ha pulsado")
            pulsado = True
        else:
            pulsado = False
        time.sleep(0.1)#liberamos el procesador

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulsadorGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    hilo1 = threading.Thread(target=ejecucion)
    hilo1.start()

    signal.signal(signal.SIGINT, callbackSalir)
    signal.pause()