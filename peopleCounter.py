from picamera import PiCamera
import cv2
import time
import cvlib as cv
import BlynkLib
import datetime
import requests
import base64
from cvlib.object_detection import draw_bbox
import httplib2 as http  # External library
from urllib.parse import urlparse
import json
import math

x =0

camera = PiCamera()

BLYNK_AUTH = 'eW3cMsZ6qaHSANLaz28pS3sZ_Jo75ovo'
blynk = BlynkLib.Blynk(BLYNK_AUTH)


while True:

    blynk.run()

    now = datetime.datetime.now()

    camera.capture('/home/pi/PycharmProjects/crowdDetection/image.jpg')
    # read input image
    image = cv2.imread('image.jpg')
    # apply object detection
    bbox, label, conf = cv.detect_common_objects(image)

    output_image = draw_bbox(image, bbox, label, conf)

    cv2.imwrite("output_image.png", output_image)

    crowd = label.count('person')
    print(crowd)

    blynk.run()


    if crowd == 0:
        status = "Empty"
        blynk.virtual_write(1, " ")
        x =0
        blynk.virtual_write(3, 1, '', '', "value")
    elif crowd >= 1:
        status = "Low crowd"

        if x == 0:
            if __name__ == "__main__":
                # Authentication parameters
                headers = {'AccountKey': 'NXpFdS3XQnqaH4jIc2g6kQ==',
                           'accept': 'application/json'}  # this is by default

                # API parameters
                uri = 'http://datamall2.mytransport.sg/'  # Resource URL
                path = 'ltaodataservice/BusArrivalv2?BusStopCode=75279'

            # Build query string & specify type of API call
            target = urlparse(uri + path)
            method = 'GET'
            body = ''

            # Get handle to http
            h = http.Http()

            # Obtain results
            response, content = h.request(target.geturl(), method, body, headers)

            blynk.run()

            # Parse JSON to print
            jsonObj = json.loads(content)

            z = len(jsonObj['Services'])

            BusService = ['', '', '', '', '']
            firstBus = ['', '', '', '', '']
            Bus1 = ['', '', '', '', '']
            BusTiming1 = ['', '', '', '', '']
            BusArr1 = ['', '', '', '', '']
            min1 = ['', '', '', '', '']
            lat = ['', '', '', '', '']
            long = ['', '', '', '', '']

            for x in range(z):
                BusService[x] = jsonObj['Services'][x]['ServiceNo']
                firstBus[x] = jsonObj['Services'][x]['NextBus']['EstimatedArrival']
                lat[x] = jsonObj['Services'][x]['NextBus']['Latitude']
                long[x] = jsonObj['Services'][x]['NextBus']['Longitude']

                Bus1[x] = (firstBus[x].replace("T", " ")).replace("+08:00", "")
                BusTiming1[x] = datetime.datetime.strptime(Bus1[x], '%Y-%m-%d %H:%M:%S')
                BusArr1[x] = ((BusTiming1[x] - now).total_seconds()) / 60
                min1[x] = math.trunc(BusArr1[x])

                print(BusService[x])
                print(min1[x])
                print("\n")
                
            blynk.virtual_write(1, " ")

            for x in range(z):
                if min1[x] > 10:
                    print(BusService[x])
                    blynk.notify("High Crowd! Please deploy additional bus  " + BusService[x])
                    blynk.virtual_write(1, BusService[x])
                    blynk.virtual_write(3, 1, lat[x], long[x], "value")

            blynk.notify("High Crowd, no additional deployment of buses are required")

            blynk.run()

            print("uploading photo")


            with open("output_image.png", "rb") as file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": "5c312507482cb88aa06da3a1a9ba7a4c",
                    "image": base64.b64encode(file.read()),
                }
                res = requests.post(url, payload)
            print("uploading done")


            x = 1
            blynk.run()



    elif crowd > 15:
        status = "High crowd"
        blynk.virtual_write(1, " ")
        x =0
        blynk.virtual_write(3, 1, '', '', "value")

    print(status)

    blynk.virtual_write(0, status)
    blynk.virtual_write(2, crowd)
    blynk.run()




