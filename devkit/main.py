from machine import Pin, WDT
import time

from config import *

import display_manager as display

import servo_lock as lock

import rfid_reader

import network_manager

import camera_manager

import security_manager

# ======================================
# WATCHDOG
# ======================================

wdt = WDT(timeout=10000)

# ======================================
# GPIO
# ======================================

led_green = Pin(4, Pin.OUT)

led_red = Pin(15, Pin.OUT)

buzzer = Pin(26, Pin.OUT)

# ======================================
# BUZZER
# ======================================

def beep(delay=0.1, times=1):

    for _ in range(times):

        buzzer.on()

        time.sleep(delay)

        buzzer.off()

        time.sleep(delay)

# ======================================
# ACCESS GRANTED
# ======================================

def access_granted():

    security_manager.access_success()

    print("ACCESS GRANTED")

    display.show(
        "ACCESS OK",
        "WELCOME"
    )

    led_green.on()

    beep(0.08, 1)

    lock.unlock()

    camera_manager.request_capture()

    time.sleep(3)

    lock.lock()

    led_green.off()

# ======================================
# ACCESS DENIED
# ======================================

def access_denied():

    print("ACCESS DENIED")

    display.show(
        "ACCESS FAIL",
        "TRY AGAIN"
    )

    led_red.on()

    beep(0.2, 2)

    time.sleep(1)

    led_red.off()

    if security_manager.access_failed():

        display.show(
            "SYSTEM LOCK",
            "WAIT 30 SEC"
        )

# ======================================
# MAIN
# ======================================

def main():

    lock.lock()

    display.show(
        "SMART LOCK",
        "BOOTING..."
    )

    network_manager.connect_wifi()

    display.show(
        "READY",
        "SCAN CARD"
    )

    while True:

        wdt.feed()

        if security_manager.is_locked():

            display.show(
                "SYSTEM",
                "LOCKED"
            )

            time.sleep(1)

            continue

        card = rfid_reader.read_card()

        if card is not None:

            print("CARD:", card)

            if card in AUTHORIZED_CARDS:

                access_granted()

            else:

                access_denied()

            display.show(
                "READY",
                "SCAN CARD"
            )

            time.sleep(2)

        time.sleep(0.2)

# ======================================
# START
# ======================================

main()