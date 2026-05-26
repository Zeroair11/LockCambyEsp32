import network
import time

from config import *

def connect_wifi():

    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    if not wlan.isconnected():

        wlan.connect(
            WIFI_SSID,
            WIFI_PASS
        )

        timeout = 20

        while (
            not wlan.isconnected()
            and timeout > 0
        ):

            print("CONNECTING...")

            time.sleep(1)

            timeout -= 1

    if wlan.isconnected():

        print("WIFI OK")

        print(wlan.ifconfig())

        return True

    else:

        print("WIFI FAIL")

        return False