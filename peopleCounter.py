from picamera import PiCamera
import cv2
import time
import cvlib as cv
from cvlib import detect_common_objects
import BlynkLib
import datetime
import requests
import base64

camera = PiCamera()

BLYNK_AUTH = 'eW3cMsZ6qaHSANLaz28pS3sZ_Jo75ovo'
blynk = BlynkLib.Blynk(BLYNK_AUTH)


while True:

    camera.capture('/home/pi/PycharmProjects/crowdDetection/image.jpg')
    # read input image
    image = cv2.imread('image.jpg')
    # apply object detection
    bbox, label, conf = cv.detect_common_objects(image)

    crowd = label.count('person')
    print(crowd)

    if crowd == 0:
        status = "Empty"
    elif crowd >= 1:
        status = "Low crowd"


        with open("image.jpg", "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": "5c312507482cb88aa06da3a1a9ba7a4c",
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)

    elif crowd > 20:
        status = "High crowd"

    print(status)

    now = datetime.datetime.now()
    Time = now.strftime("%H:%M:%S")
    blynk.run()
    blynk.virtual_write(0, status)
    blynk.virtual_write(1, Time)

    time.sleep(2)

