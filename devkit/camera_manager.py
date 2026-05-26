import urequests

from config import *

def request_capture():

    try:

        url = (
            "http://{}/capture_and_upload"
        ).format(CAM_IP)

        response = urequests.get(url)

        print(response.text)

        response.close()

    except Exception as e:

        print(e)