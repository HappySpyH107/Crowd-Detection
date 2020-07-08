
import cvlib as cv
import cv2
import time
from cvlib.object_detection import draw_bbox

while True:

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ok, image = cam.read()
    cv2.imwrite("image.png", image)
    cam.release()

    # read input image
    image = cv2.imread('image.png')

    # apply object detection
    bbox, label, conf = cv.detect_common_objects(image)

    output_image = draw_bbox(image, bbox, label, conf)

    cv2.imwrite("output_image.png", output_image)

    crowd = label.count('person')
    print(crowd)

    if crowd == 0:
        status = "Empty"
    elif crowd >= 1:
        status = "Low crowd"
    elif crowd > 20:
        status = "High crowd"

    print(status)
    time.sleep(10)


