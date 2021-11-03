#!/usr/bin/env python3

import signal
import sys
import RPi.GPIO as GPIO
import time
import threading

pulsadorGPIO1 = 16
pulsadorGPIO2 = 21
ledGPIO1=20
ledGPIO2=12

flag1 = 0
flag2 = 0

def callbackSalir (senial, cuadro): # señal y estado cuando se produjo la interrup.
    GPIO.cleanup () # limpieza de los recursos GPIO antes de salir
    sys.exit(0)

def callbackBotonPulsado1 (canal):
    global flag1
    if flag1 == 0:
        pwm.ChangeDutyCycle(100)
        flag1 = 1
    else:
        pwm.ChangeDutyCycle(0)
        flag1 = 0


def callbackBotonPulsado2 (canal):
    global flag2
    if flag2 == 0:
        pwm2.ChangeDutyCycle(100)
        flag2 = 1
    else:
        pwm2.ChangeDutyCycle(0)
        flag2 = 0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulsadorGPIO1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pulsadorGPIO2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup (ledGPIO1, GPIO.OUT)
    GPIO.setup (ledGPIO2, GPIO.OUT)
    pwm = GPIO.PWM(ledGPIO1,100)
    pwm.start (0)
    pwm2 = GPIO.PWM(ledGPIO2,100)
    pwm2.start (0)

    hilo1 = threading.Thread(target=GPIO.add_event_detect(pulsadorGPIO1, GPIO.FALLING,
      callback=callbackBotonPulsado1, bouncetime=200))
    hilo1.start()

    hilo2 = threading.Thread(target=GPIO.add_event_detect(pulsadorGPIO2, GPIO.FALLING,
      callback=callbackBotonPulsado2, bouncetime=200))
    hilo2.start()

    hilo1.join()
    hilo2.join()
    signal.signal(signal.SIGINT, callbackSalir) # callback para CTRL+C que limpia todos los hilos anteriores
    signal.pause() # esperamos por hilo/callback CTRL+C antes de acabar para que no se acabe solo el principal