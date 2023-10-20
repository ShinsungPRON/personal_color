# +------------+--------------+-----------------------------------------------------------+
# |   Author   |     Date     |                         Changed                           |
# +------------+--------------+-----------------------------------------------------------+
# |  Andrew A. |  2023/10/18  | Initial release                                           |
# +------------+--------------+-----------------------------------------------------------+

from colormath.color_objects import LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color
import color_extractor.dominant_color as dominant_color
import color_extractor.face_detector as face_detector
import random
import numpy as np
import cv2
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def is_warm(lab_b, a):
    """
    :param lab_b:
    [cheek, eyebrow, eye]의 Lab b값들입니다.
    :param a:
    [cheek, eyebrow, eye]의 가중치들입니다.
    :return:
    0: 쿨톤
    1: 웜톤
    """
    # 기준값
    warm_b_std = [11.6518, 11.71445, 3.6484]
    cool_b_std = [4.64255, 4.86635, 0.18735]

    warm_dist = 0
    cool_dist = 0

    for i in range(3):
        warm_dist += abs(lab_b[i] - warm_b_std[i]) * a[i]
        print(warm_dist)
        cool_dist += abs(lab_b[i] - cool_b_std[i]) * a[i]
        print(cool_dist)

    if warm_dist <= cool_dist:
        return 1  # 웜톤
    else:
        return 0  # 쿨톤


def is_spr(hsv_s, a):
    """
    :param hsv_s:
    [cheek, eyebrow, eye]의 HSV S값들입니다.
    :param a:
    [cheek, eyebrow, eye]의 가중치들입니다.
    :return:
    0: 가을
    1: 봄
    """
    # skin, hair, eye
    spr_s_std = [18.59296, 30.30303, 25.80645]
    fal_s_std = [27.13987, 39.75155, 37.5]

    spr_dist = 0
    fal_dist = 0

    body_part = ['skin', 'eyebrow', 'eye']
    for i in range(3):
        spr_dist += abs(hsv_s[i] - spr_s_std[i]) * a[i]
        print(spr_dist)
        fal_dist += abs(hsv_s[i] - fal_s_std[i]) * a[i]
        print(fal_dist)

    if spr_dist <= fal_dist:
        return 1
    else:
        return 0


def is_smr(hsv_s, a):
    '''
    파라미터 hsv_s = [skin_s, hair_s, eye_s]
    a = 가중치 [skin, hair, eye]
    질의색상 hsv_s값에서 summer의 hsv_s, winter의 hsv_s값 간의 거리를
    각각 계산하여 summer가 가까우면 1, 반대 경우 0 리턴
    '''
    # skin, eyebrow, eye
    smr_s_std = [12.5, 21.7195, 24.77064]
    wnt_s_std = [16.73913, 24.8276, 31.3726]
    a[1] = 0.5  # eyebrow 영향력 적기 때문에 가중치 줄임

    smr_dist = 0
    wnt_dist = 0

    body_part = ['skin', 'eyebrow', 'eye']
    for i in range(3):
        smr_dist += abs(hsv_s[i] - smr_s_std[i]) * a[i]
        print(smr_dist)
        wnt_dist += abs(hsv_s[i] - wnt_s_std[i]) * a[i]
        print(wnt_dist)

    if (smr_dist <= wnt_dist):
        return 1  # summer
    else:
        return 0  # winter


def extract_personal_color_from(image):
    face_parts = face_detector.FacePart(image)

    dominant_colors = [dominant_color.DominantColor(face_parts.get_part(part)).get_dominant_color()
                       for part in face_parts.available_parts]

    cheek = np.mean([dominant_colors[0], dominant_colors[1]], axis=0)
    eye = np.mean([dominant_colors[2], dominant_colors[3]], axis=0)
    eyebrow = np.mean([dominant_colors[4], dominant_colors[5]], axis=0)

    Lab_b = []
    hsv_s = []

    for part in (cheek, eyebrow, eye):
        rgb = sRGBColor(part[0], part[1], part[2], is_upscaled=True)  # RGB로 변환
        lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor)  # LAB으로 변환
        hsv = convert_color(rgb, HSVColor, through_rgb_type=sRGBColor)  # HSV로 변환
        Lab_b.append(float(format(lab.lab_b, ".2f")))
        hsv_s.append(float(format(hsv.hsv_s, ".2f")) * 100)


    Lab_weight = [30, 20, 5]
    hsv_weight = [10, 1, 1]

    if (is_warm(Lab_b, Lab_weight)):
        if (is_spr(hsv_s, hsv_weight)):
            tone = '봄웜톤 (spring)'
        else:
            tone = '가을웜톤 (fall)'
    else:
        if (is_smr(hsv_s, hsv_weight)):
            tone = '여름쿨톤 (summer)'
        else:
            tone = '겨울쿨톤 (winter)'

    print(tone)


def white_balance(img):
    img_LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(img_LAB[:, :, 1])
    avg_b = np.average(img_LAB[:, :, 2])
    img_LAB[:, :, 1] = img_LAB[:, :, 1] - ((avg_a - 128) * (img_LAB[:, :, 0] / 255.0) * random.randrange(-20, 20) * 0.1)
    img_LAB[:, :, 2] = img_LAB[:, :, 2] - ((avg_b - 128) * (img_LAB[:, :, 0] / 255.0) * random.randrange(-20, 20) * 0.1)
    balanced_image = cv2.cvtColor(img_LAB, cv2.COLOR_LAB2BGR)
    return balanced_image



if __name__ == '__main__':
    # img = cv2.imread("../../ShowMeTheColor/res/test/nwinter/3.jpg")
    img = cv2.imread("/Users/flyahn06/Desktop/img3.png")
    cv2.imshow("Raw", img)
    img2 = white_balance(img)
    cv2.imshow("Whitebalanced", img2)
    cv2.waitKey(0)

    extract_personal_color_from(img)
    extract_personal_color_from(img2)
