# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/10/18  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+
import cv2

import dominant_color
import face_detector


def extract_personal_color_from(image):
    face_parts = face_detector.FacePart(image)

    dominant_colors = [dominant_color.DominantColor(face_parts.get_part(part)).get_dominant_color()
                       for part in face_parts.available_parts]

    print(dominant_colors)


if __name__ == '__main__':
    extract_personal_color_from(cv2.imread("../test/face.png"))