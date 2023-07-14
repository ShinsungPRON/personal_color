# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/07/14  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+
import time

# Real-time face point
import cv2
from color_extractor import face_detector

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()

    frame = cv2.flip(frame, 1)

    face = face_detector.FacePart(frame)
    cv2.imshow("face", face._show_points())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()

