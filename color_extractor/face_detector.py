import copy
from collections import OrderedDict
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

FACIAL_LANDMARKS_IDXS = OrderedDict([
    ("nose", (27, 35)),
    ("jaw", (0, 17))
])

FACIAL_LANDMARKS_IDXS_CHEEK = OrderedDict([
    ("left_cheek", ())
])


class FacePart:
    def __init__(self, image_path, predictor_path):
        self._facial_marks = dict()
        self._available_parts = ["nose", "jaw", "left_cheek", "right_cheek"]

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)

        image = cv2.imread(image_path)
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 여기서 얼굴이 인식됨 (rects는 얼굴이 있는 좌표 집합)
        # type: dlib.rectanges(dlib.rectangle)
        rects = detector(gray, 1)

        # TODO: 테스트
        # rect = rects[0]
        # cv2.rectangle(image, (rect.tl_corner().x, rect.tl_corner().y), (rect.br_corner().x, rect.br_corner().y), (0, 0, 255))
        # cv2.imshow("face", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        for (point_index_start, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            print(shape)

            for (name, (point_index_start, point_index_end)) in FACIAL_LANDMARKS_IDXS.items():
                # i는 인덱스 시작점, j는 인덱스 끝점
                # 참고: https://pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup.jpg
                print(name, point_index_start, point_index_end)
                temp = []
                for x, y in shape[point_index_start:point_index_end]:
                    temp.append((x, y))
                # 리스트 참조를 끊기 위해 깊은 복사 사용
                self._facial_marks[name] = copy.deepcopy(temp)

            for name, pointindexes in FACIAL_LANDMARKS_IDXS_CHEEK.items():
                pass



        for name, pointlist in self._facial_marks.items():
            for point in pointlist:
                print(point)
                cv2.circle(image, point, 3, (255, 0, 0))

        cv2.imshow("face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
        if part not in self._available_parts:
            raise ValueError("{} is not available.".format(part))

        # TODO: cv2 이미지 리턴


if __name__ == '__main__':
    face = FacePart("../test/face.png", "../resources/shape_predictor_68_face_landmarks.dat")
