from machine import Pin, PWM
import time

servo = PWM(Pin(13), freq=50)

def set_angle(angle):

    duty = int((angle / 180) * 75 + 40)

    servo.duty(duty)

    time.sleep(0.4)

    servo.duty(0)

def lock():

    set_angle(0)

def unlock():

    set_angle(90)