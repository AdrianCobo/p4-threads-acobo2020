#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import signal
import sys
import threading

pulsadorGPIO1 = 16
ledGPIO1=20

def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def edge1():
    pulsado1 = False
    while True:
            GPIO.wait_for_edge(pulsadorGPIO1, GPIO.RISING)
            if not pulsado1:
                time.sleep(0.1)
                pwm.ChangeDutyCycle(100)
                pulsado1 = True
                time.sleep(0.1)
            else:
                pulsado1 = False
                pwm.ChangeDutyCycle(0)
                time.sleep(0.1)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulsadorGPIO1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup (ledGPIO1, GPIO.OUT)
    pwm = GPIO.PWM(ledGPIO1,100)
    pwm.start (0)

    hilo1 = threading.Thread(target=edge1)
    hilo1.start()

    signal.signal(signal.SIGINT, callbackSalir)
    signal.pause()
    time.sleep(0.1)#liberamos el procesador