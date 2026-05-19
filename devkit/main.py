from mfrc522 import MFRC522
from machine import Pin, PWM
import network
import urequests
import time

# ========================================
# LED
# ========================================
led_green = Pin(2, Pin.OUT)

# ========================================
# SERVO
# ========================================
servo = PWM(Pin(13), freq=50)

# ========================================
# SERVO FUNCTION
# ========================================
def set_angle(angle):

    duty = int((angle / 180) * 75 + 40)
    servo.duty(duty)

# khóa mặc định
set_angle(0)

# ========================================
# WIFI STA
# ========================================
STA_SSID = ":v"
STA_PASS = "ngocancut"

# ========================================
# AP MODE
# ========================================
AP_SSID = "ESP_GATEWAY"
AP_PASS = "12345678"

# ========================================
# SERVER CONFIG
# ========================================
SERVER_URL = "http://10.69.106.161:5000/upload"

# ========================================
# ESP32-CAM IP
# ========================================
CAM_IP = "192.168.4.2"

# ========================================
# AUTHORIZED CARDS
# ========================================
AUTHORIZED_CARDS = [
    3857600436,
    2385517062
]

# ========================================
# WIFI APSTA
# ========================================
def start_wifi():

    print("STARTING WIFI...")

    # STA
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(STA_SSID, STA_PASS)

    print("Connecting STA...")

    timeout = 20

    while not sta.isconnected() and timeout > 0:
        time.sleep(1)
        print("...")
        timeout -= 1

    if sta.isconnected():
        print("STA OK")
        print(sta.ifconfig())
    else:
        print("STA FAILED")

    # AP
    ap = network.WLAN(network.AP_IF)

    ap.active(False)
    time.sleep(1)

    ap.active(True)

    ap.config(
        essid="ESP_GATEWAY"
    )

    time.sleep(3)

    print("AP STARTED")
    print(ap.ifconfig())

# ========================================
# RFID RC522
# ========================================
rdr = MFRC522(
    sck=18,
    mosi=23,
    miso=19,
    rst=22,
    cs=5
)

# ========================================
# REQUEST IMAGE FROM CAM
# ========================================
def request_capture():

    try:

        print("REQUEST CAMERA...")

        url = "http://{}/capture".format(CAM_IP)

        response = urequests.get(url)

        if response.status_code == 200:

            image_data = response.content

            print("IMAGE RECEIVED")
            print("SIZE:", len(image_data))

            upload_to_server(image_data)

        else:
            print("CAM ERROR:", response.status_code)

        response.close()

    except Exception as e:
        print("CAPTURE ERROR:", e)


# ========================================
# UPLOAD IMAGE TO SERVER
# ========================================
def upload_to_server(image_data):

    try:

        print("UPLOADING...")

        headers = {
            "Content-Type": "image/jpeg"
        }

        response = urequests.post(
            SERVER_URL,
            data=image_data,
            headers=headers
        )

        print("SERVER:", response.text)

        response.close()

    except Exception as e:
        print("UPLOAD ERROR:", e)


# ========================================
# MAIN
# ========================================
def main():

    start_wifi()

    print("SMART LOCK READY")

    while True:

        rdr.init()

        stat, tag_type = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:

            stat, uid = rdr.SelectTagSN()

            if stat == rdr.OK:

                card = int.from_bytes(bytes(uid), "little", False)

                print("CARD ID:", card)

                # =========================
                # AUTH CHECK
                # =========================
                if card in AUTHORIZED_CARDS:

                    print("ACCESS GRANTED")

                    led_green.on()

                    # mở khóa
                    set_angle(90)

                    # capture image
                    request_capture()

                    time.sleep(3)

                    # khóa lại
                    set_angle(0)

                    led_green.off()

                else:

                    print("ACCESS DENIED")

        time.sleep(0.2)

# ========================================
# START
# ========================================
main()