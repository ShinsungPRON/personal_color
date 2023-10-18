# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/07/14  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/07/14  | All methods in FacePart() will return cv2.image           |
# +------------+--------------+-----------------------------------------------------------+

import copy
from collections import OrderedDict
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import os

# 재정의: 필요한 부분만 뽑음
# 형식: (이름, (모델 포인트 기준 인덱스 시작점, 모델 포인트 기준 인덱스 끝점))
FACIAL_LANDMARKS_IDXS = OrderedDict([
    ("nose", (27, 35)),
    ("jaw", (0, 17))
])

# 형식: (이름, (모델 포인트 기준 좌표*))
FACIAL_LANDMARKS_IDXS_CHEEK = OrderedDict([
    ("left_cheek", (1, 2, 3, 4, 31, 36)),
    ("right_cheek", (16, 15, 14, 13, 35, 45))
])
resources_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources"))
model_path = os.path.join(resources_dir, "shape_predictor_68_face_landmarks.dat")


@lambda _: _()
def predictor():
    try:
        _predictor = dlib.shape_predictor(model_path)
    except FileNotFoundError:
        exit("Unable to open data file.")
    else:
        return _predictor


detector = dlib.get_frontal_face_detector()


class FacePart:
    available_parts = ["nose", "jaw", "left_cheek", "right_cheek"]

    def __init__(self, image):
        # 인식된 얼굴 부분의 좌표가 들어갈 사전
        self._facial_marks = dict()
        # 인식할 부분

        self.image = image
        # self.image = imutils.resize(self.image, width=500)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # 여기서 얼굴이 인식됩니다. (rects는 얼굴이 있는 좌표 집합)
        # type: dlib.rectanges(dlib.rectangle)
        self.rects = detector(self.gray, 1)  # 여러 얼굴 처리... TODO: 한 얼굴 처리로 바꾸기

        for (i, rect) in enumerate(self.rects):  # 필요 없는 루프
            shape = predictor(self.gray, rect)
            shape = face_utils.shape_to_np(shape)
            # shape 형식: https://pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup.jpg

            # FACIAL_LANDMARKS_IDXS_CHEEK, FACIAL_LANDMARKS_IDXS 형식이 다르므로
            # 두 개로 나눠서 처리함

            # FACIAL_LANDMARKS_IDXS 처리
            for (name, (point_index_start, point_index_end)) in FACIAL_LANDMARKS_IDXS.items():
                temp = []
                for x, y in shape[point_index_start:point_index_end]:
                    temp.append([x, y])
                # 리스트 참조를 끊기 위해 깊은 복사 사용
                temp = np.array(temp)
                self._facial_marks[name] = copy.deepcopy(temp)

            # FACIAL_LANDMARKS_IDXS_CHEEK 처리
            for name, points in FACIAL_LANDMARKS_IDXS_CHEEK.items():
                temp = []
                for point in points:
                    temp.append([(p := shape[point])[0], p[1]])
                temp = np.array(temp)
                self._facial_marks[name] = copy.deepcopy(temp)

    def _show_points(self):
        if not len(self.rects): return self.image

        clone = self.image.copy()
        for name, pointlist in self._facial_marks.items():
            for point in pointlist:
                if name in ("nose", "jaw"):
                    cv2.circle(clone, point, 3, (255, 0, 0))
                else:

                    cv2.circle(clone, point, 1, (255, 255, 0))

        cv2.putText(clone, "nose", self._facial_marks["nose"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        cv2.putText(clone, "jaw", self._facial_marks["jaw"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        cv2.putText(clone, "left_cheek", self._facial_marks["left_cheek"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
        cv2.putText(clone, "right_cheek", self._facial_marks["right_cheek"][0], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)

        return clone

    def _show_entire_points(self):
        if not len(self.rects): return self.image
        clone = self.image.copy()

        shape = predictor(self.gray, self.rects[0])
        shape = face_utils.shape_to_np(shape)

        for i, (x, y) in enumerate(shape):
            cv2.circle(clone, (x, y), 1, (0, 0, 255))
            cv2.putText(clone, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

        return clone

    def get_part(self, part: str):
        """
        얼굴의 한 부분을 opencv의 이미지 형식으로 리턴합니다.
        :param part:
        찾을 얼굴 부분입니다.
        nose, jaw, left_cheek, right_cheek 중 하나입니다.
        :return:
        찾은 얼굴 부분을 이미지로 돌려줍니다.

        :exception ValueError:
        찾을 얼굴 부분이 없는 경우 발생합니다.
        """
        if not len(self.rects): return self.image
        if part not in self.available_parts:
            raise ValueError("{} is not available.".format(part))

        x, y, w, h = cv2.boundingRect(self._facial_marks[part])
        crop = self.image[y:y+h, x:x+w]
        adj_points = np.array([np.array([p[0]-x, p[1]-y]) for p in self._facial_marks[part]])

        # 마스크 설정
        mask = np.zeros((crop.shape[0], crop.shape[1]))
        cv2.fillConvexPoly(mask, adj_points, 1)
        mask = mask.astype(np.bool_)
        crop[np.logical_not(mask)] = [255, 0, 0]

        return crop


if __name__ == '__main__':
    face = FacePart(cv2.imread("../test/face.png"))
    cv2.imshow("face", face._show_entire_points())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for p in face.available_parts:
        cv2.imshow(p, face.get_part(p))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
