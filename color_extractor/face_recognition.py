# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/07/14  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+
import time

# Real-time face point
import cv2
from face_detector import FacePart
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)

    face = FacePart(frame)
    cv2.imshow("face", face._show_entire_points())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()

